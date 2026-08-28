# Attention、KV Cache 与 MoE：模型结构如何变成 Memory 和 Network Traffic

> 第一次阅读：1–7 节。第二次阅读：8–13 节。深入阅读：14 节以后。

## 1. 先告诉我为什么需要它

“模型有多少 parameter”无法说明 serving bottleneck。Dense attention 会让每个新 token 读取历史 key/value；context、batch、layer 数与 KV head 数共同决定 KV capacity 和 bandwidth。MoE 让每个 token 只激活部分 expert，降低相对总参数量的 compute，却必须把 token dispatch 到拥有目标 expert 的 device，形成 load imbalance 与 All-to-All traffic。

因此模型 architecture 会直接选择 hardware：Attention 决定 GEMM shape、KV cache 与 memory access；MoE router 决定 expert placement、network topology、buffer 和 tail latency。

## 2. 一句话直觉

Attention 是“当前 query 应该从哪些历史表示取信息”；KV cache 用 memory 保存已算过的历史 key/value，避免每生成一个 token 都重算整个 prefix。MoE 是“每个 token 只走少数 expert”，用 routing 与 communication 换取更大的 parameter capacity。

## 3. Transformer block 的 dataflow

~~~mermaid
flowchart LR
  X[Hidden states] --> QKV[Q / K / V projections]
  QKV --> SCORE[QK^T scores]
  SCORE --> SM[Scale + mask + Softmax]
  SM --> AV[Scores × V]
  AV --> O[Output projection]
  O --> FFN[Dense FFN or MoE]
  FFN --> Y[Next layer]
  KVC[(KV cache)] --> SCORE
  QKV --> KVC
~~~

Scaled dot-product attention 的核心为：

[
Attention(Q,K,V)=softmaxleft(rac{QK^T}{sqrt{d_k}}ight)V
]

Q 与 K 的乘积决定关联权重，Softmax 形成归一化分布，再对 V 加权求和。实际系统还包含 causal mask、position encoding、head partition、normalization、residual、kernel fusion 与 layout。

## 4. Prefill 为什么与 decode 不同

Prefill 同时处理整个 prompt，可形成较大的 matrix，Q、K、V projection 与 attention 更容易获得 parallelism；但标准 dense self-attention 的 score matrix 随 sequence length 呈平方增长。优化 kernel 会分块计算并避免把完整 score matrix 写回 HBM，但总计算与 memory access 仍受 sequence、head 和 implementation 影响。

Decode 每次通常只为每个 sequence 产生一个新 query。新 K/V 写入 cache，新 Q 与所有历史 K 做 dot product，再按权重读取历史 V。GEMM 变窄、历史 cache 随 context 增长，arithmetic intensity 下降，所以 decode 更容易受 HBM bandwidth、capacity、memory fragmentation 与 scheduler 影响。

把 prefill 和 decode 合并成一个 tokens/s 会掩盖 Time to First Token（TTFT）与 Time per Output Token（TPOT）的冲突：批量 prefill 可提高 throughput，却可能阻塞 decode tail latency；优先 decode 又可能降低 accelerator utilization。

## 5. KV cache size 如何估算

标准 multi-head attention 的 KV cache 一阶容量可写为：

[
Bytes_{KV}=2 	imes L 	imes S 	imes B 	imes H_{KV} 	imes D 	imes bytes
]

2 表示 K 与 V，(L) 是 layer 数，(S) 是 cached sequence length，(B) 是并发 sequence，(H_{KV}) 是 KV head 数，(D) 是每 head dimension。若使用 Multi-Query Attention（MQA）或 Grouped-Query Attention（GQA），多个 query head 共享较少 KV head，可显著降低 cache；代价是模型 quality、training choice 与 kernel support 的权衡。

### Worked example

假设 80 layers、8 KV heads、head dimension 128、context 16k、BF16 两 bytes、batch 1：

[
2 	imes 80 	imes 16{,}384 	imes 8 	imes 128 	imes 2
approx 5.0 GiB
]

结果约 5 GiB per sequence，[Estimate] 尚未计 allocator overhead、alignment、temporary workspace 与 model weights。并发 32 个同长度 session 时，仅 KV 约 160 GiB，[Estimate]，说明 context window 是 capacity promise，不代表可以按该长度高并发服务。

TensorRT 的 KV cache interface 公开了 batch、KV head、maximum sequence 与 head dimension 等 shape，并支持按 sequence write index 更新新 token 的 K/V。[Primary Source] 这正体现 cache 是持续增长、需要独立 allocation 与更新的 state。

## 6. KV cache 的 design space

| 方案 | 改善 | 代价 |
|---|---|---|
| MQA/GQA | 减少 KV heads 与 bytes | model architecture/quality 约束 |
| KV quantization | 减少 capacity/bandwidth | quantization error、scale 与 kernel |
| Paged allocation | 降低 fragmentation、支持动态长度 | page table、indirection、scheduler |
| Prefix sharing | 多请求复用共同 prefix | cache identity、lifetime、安全隔离 |
| Sliding window | 限定读取历史范围 | 丢失远距离 full attention |
| Eviction/compression | 减少保留 token | 任务依赖的 quality 风险 |
| Offload | 用 host/CXL/remote memory 扩容 | latency、bandwidth 与 fault domain |

Paged KV 不减少理论每 token bytes，而是改善 variable-length sequence 的物理分配和复用。Compression 或 eviction 才改变保留信息量，但验证不能只用单一 needle benchmark；summarization、retrieval、reasoning、code 与 rare long-range dependency 的敏感度不同。

## 7. 为什么不……？

### 为什么不每步重新计算所有 K/V？

它节省 persistent memory，却把每个 decode step 变成对整个 prefix 的重复 forward compute，通常极不经济。Cache 是用 memory 换 compute。

### 为什么不把 context 全放进 cache？

更长 context 线性增加 KV capacity 和每步读取，减少可并发 session，并扩大 tail latency。系统必须做 admission control，而不是只公布 maximum context。

### 为什么不把 KV 全部量化到最低 bit？

K/V quantization error 会改变 attention score 与加权结果，并可能跨 layer、跨 output token 累积。不同 layer/head/outlier 的 sensitivity 不同。

### 为什么不把 KV offload 到便宜 memory？

Decode 每 token 都需要读相关历史 state，较高 latency 或较低 bandwidth 会直接进入 critical path。只有 prefetch、locality、分层 policy 与 workload SLO 匹配时 offload 才有价值。

## 8. MoE 到底改变什么

Dense FFN 对所有 token 使用同一组 parameter。MoE layer 有多个 expert，router 为每个 token 选择 top-k expert。总 parameter capacity 可以很大，但每 token 只执行少数 expert，从而把“parameter count”与“activated compute”分开。

~~~mermaid
flowchart LR
  T[Tokens on each GPU] --> R[Router logits + top-k]
  R --> P[Permute / bucket by expert]
  P --> A2A[All-to-All dispatch]
  A2A --> E[Local expert GEMMs]
  E --> A2AR[All-to-All return]
  A2AR --> U[Unpermute + combine]
~~~

如果 expert 分布在不同 GPU，token 必须重新排列、跨网络 dispatch，执行 expert，再返回原 data-parallel/tensor-parallel ownership。NVIDIA Megatron Core 的公开配置明确包含 allgather、alltoall 与 flex token dispatcher 选项，[Primary Source] 说明 dispatcher 是实际 software/hardware design choice，而不是模型论文里的抽象箭头。

## 9. Expert parallelism 与 load balance

Expert Parallelism（EP）把 expert 分布到不同 rank。优点是每个 rank 只保存/计算部分 expert；代价是 token routing 引入 communication。Token Parallelism、Tensor Parallelism、Data Parallelism 和 Pipeline Parallelism 还会与 EP 组合，形成不同 process group 与 collective boundary。

Router 可能把过多 token 发给热门 expert。若每个 expert 预留 capacity，热门 expert 可能 overflow、drop 或 reroute token；若动态接受全部 token，最慢 expert 决定 layer tail latency。Load-balancing loss、capacity factor、expert replication 与 routing policy 都在 quality、compute waste 和 tail latency间取舍。

即使平均 token 均匀，也要看 microbatch 级 skew。Collective 需要等待 peer，短时间 hotspot 足以造成 bubble。MoE 的 network 问题因此不只看 aggregate bytes，还看 message size、fan-out、synchronization、topology locality 与 incast。

## 10. MoE communication 估算

若某 layer 每个 rank 有 (T) tokens、hidden size (H)、每元素 (b) bytes、top-k 为 (k)，单次 dispatch 的 payload 量级为：

[
Bytes_{dispatch}approx T 	imes H 	imes b 	imes k
]

还要有 return traffic，且 metadata、padding、alignment 与 collective algorithm 增加开销。假设每 rank 4096 tokens、hidden 8192、BF16 两 bytes、top-2：

[
4096 	imes 8192 	imes 2 	imes 2 approx 128 MiB
]

单向 payload 约 128 MiB per rank per MoE layer，[Estimate] 返回再增加相近量级。该例用于数量级，不代表所有模型；实际 token 数、parallel mapping、local expert 命中与 precision 会改变流量。

## 11. 为什么不……MoE 版

### 为什么不为每个 token 激活所有 expert？

那会退化为超大的 dense layer，失去 sparse activation 的 compute 优势。

### 为什么不把所有 expert 放在每个 GPU？

复制可减少通信，却增加 weight memory 与 update synchronization，降低可支持的总 expert 数。

### 为什么不让 router 永远选择最优 expert？

“最优”可能把大量 token集中到少数 expert，造成 capacity overflow 与 tail latency。必须在 specialization 与 balance 间权衡。

### 为什么不只增加 network bandwidth？

All-to-All 还受 latency、message size、topology、endpoint injection、buffer、software permutation 与 synchronization 影响；只扩大 link 不修复 imbalance，最慢 rank 仍主导。

## 12. Attention 与 MoE 的共同 second-order effects

KV compression 释放 memory 后，系统可以接纳更多 session，反而提高 aggregate memory traffic 和 scheduling pressure；更长 context 提高模型能力后，prefill compute 与 TTFT 增加。MoE 减少 activated compute 后，network 与 router 更显著；提高 network 后，expert GEMM shape 过小或 load skew 又成为瓶颈。

模型与系统是闭环：GQA、KV precision、expert count、top-k、capacity factor、parallel mapping 和 batching 都会改变 hardware utilization。不能把 model quality benchmark 与 infrastructure benchmark分开优化后再假设二者可无损组合。

## 13. Product / workload mapping

Training 需要保存 activation、执行 backward，并为 MoE weight/gradient 选择 parallel collective；通信往往更规则但规模大。Inference prefill 看 prompt length、batch 与 attention kernel；decode 看 KV bytes/token、active session、memory bandwidth 与 tail latency。Agentic workload 会产生多轮、分支、工具等待与 cache lifetime，平均 sequence 模型更难描述。

Serving engine 需要 continuous batching、paged KV、prefix caching、admission control、preemption 与 observability。硬件的 HBM capacity 只有在 allocator 和 scheduler 能高效填充时才成为可售 serving capacity。

## 14. Engineers actually say

- “KV cache dominates.”：追问是 capacity、bandwidth、fragmentation 还是 allocation latency。
- “We are decode-bound.”：追问 batch、context distribution、TPOT SLO 与 weight/KV traffic。
- “The experts are imbalanced.”：追问平均还是 tail、router distribution、capacity factor 与 dropped token。
- “MoE is network-bound.”：追问 dispatch payload、locality、message size、permutation 与 collective wait。
- “We use paged KV.”：这说明 allocation strategy，不自动证明 cache bytes 下降。
- “Long context is supported.”：追问最大长度下可并发多少 request、TTFT/TPOT 与 memory reserve。

## 15. Engineering → Strategy

| Architecture choice | System effect | Product effect | Strategic implication |
|---|---|---|---|
| GQA/MQA | KV bytes 下降 | 更高 serving concurrency | model architecture 与 accelerator co-design |
| KV quantization | capacity/bandwidth 下降 | quality validation 增加 | software recipe 与 telemetry 重要 |
| Paged/prefix cache | utilization 上升 | serving engine 差异化 | runtime 可形成 switching cost |
| More experts / low top-k | parameter capacity 上升 | All-to-All 与 imbalance | networking value capture 上升 |
| Expert replication | communication 下降 | HBM capacity 上升 | memory/network trade-off 决定 BOM |
| Longer context | product capability 上升 | TTFT/KV cost 上升 | pricing/admission policy 必须匹配 |

## 16. Technical diligence questions

1. KV size 公式中的 layer、KV head、head dimension、precision 和 overhead 各是多少？
2. Context length 的生产分布是什么，不只 maximum？
3. TTFT、TPOT、throughput 与 tail percentile 如何共同报告？
4. Paged KV 的 fragmentation、page size、copy 与 eviction cost 多大？
5. KV quantization 在哪些任务、长度、layer 与 rare case 验证？
6. Prefix cache 如何隔离 tenant、处理版本与回收？
7. MoE 的 expert count、top-k、capacity factor 与 dropped-token policy？
8. All-to-All payload、permutation、network wait 各占 layer 时间多少？
9. Expert placement 是否利用 node/rack locality？
10. Load balance 看平均还是 per-microbatch tail？
11. Training 与 inference 使用相同 router/precision/parallel mapping 吗？
12. 哪些结果来自理想 synthetic workload，哪些来自生产 arrival/context 分布？

## 17. Takeaways

1. KV cache 用 memory 换掉 decode 对历史 K/V 的重复计算。
2. Context、concurrency、KV heads、layers 与 precision 共同决定 serving capacity。
3. MoE 用 routing 和 All-to-All 换取 sparse parameter capacity。
4. Attention 与 MoE 都会把模型选择转成 HBM、network、scheduler 与 tail-latency 约束。
5. 评价产品应使用真实 request distribution 与 SLO，不只单个最大 context 或模型参数量。

## Primary sources

- [Primary Source] [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [Primary Source] [NVIDIA TensorRT：KV Cache](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/transformers-kv-cache.html)
- [Primary Source] [Switch Transformers](https://arxiv.org/abs/2101.03961)
- [Primary Source] [NVIDIA Megatron Core：MoE](https://docs.nvidia.com/megatron-core/developer-guide/nightly/user-guide/features/moe.html)
- [Primary Source] [NVIDIA Megatron Core：MoE dispatcher configuration](https://docs.nvidia.com/megatron-core/developer-guide/latest/apidocs/core/core.transformer.transformer_config.html)


## 基础概念桥接

先把训练、prefill、decode、embedding、recommendation 与 multimodal 拆成不同 phase。明确 weights、activations、gradients、optimizer state、KV cache 的生命周期，再写 batch、sequence、precision、arrival distribution 和 SLO。模型名称本身不是硬件需求。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。


## 进阶工程术语桥接

本篇进一步需要掌握：微操作、流水线冒险、并行度、shape、动态批处理、尾延迟、数量级与单位经济性。阅读这些术语时，不只记中英文对应，还要补齐系统位置、正常路径、饱和或失败路径、直接 counter、端到端结果、产品状态和证据等级。若工程会议出现“已解决”“无开销”“已量产”，应立即追问 workload、boundary、configuration、status/date、failure mode 与 falsifier。

延伸阅读：[进阶工程术语手册](../31_glossary/advanced_engineering_terms_handbook.md)。
