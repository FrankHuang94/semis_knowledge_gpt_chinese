---
id: prefill_vs_decode
title: Prefill vs Decode：一次 LLM 请求为什么像两种不同 workload
concepts: [prefill, decode, kv_cache, attention, continuous_batching, serving_slo]
prerequisites: [training_vs_inference, transformer, matrix_multiplication, memory_hierarchy]
level: [2, 3, 4]
status: draft
last_verified: 2026-08-23
source_date: 2026-08-23
---

# Prefill vs Decode：一次 LLM 请求为什么像两种不同 workload

> 第一次阅读：Sections 1–8  
> 第二次阅读：Sections 9–18  
> 深入阅读：Sections 19–26

## 阅读前后

**I should understand before:** Transformer attention、GEMM、training vs inference 的基本差异。  
**I should understand after:** 能画出一次自回归 LLM 请求的 prefill/decode dataflow，估算 KV cache，解释 TTFT 与 ITL 为什么对应不同瓶颈，并判断 batching、paging、quantization、speculative decoding 与 P/D disaggregation 的适用边界。

## 1. 先告诉我为什么需要它

用户发送 prompt 后，LLM 不会以完全相同的方式处理所有 token：

1. **Prefill** 一次处理 prompt 中许多已知 token，建立每层 KV cache，并产生第一个输出 token 所需的状态。
2. **Decode** 每轮只新增一个或少量 token，读取已有 KV cache，生成下一个 token，然后重复。

它们运行同一组 weights，却有不同 shape、并行度、算术强度和服务指标。把两者混成一个“tokens/s”，会掩盖用户为什么等不到首 token、为什么生成速度慢，以及硬件究竟是 compute-bound 还是 memory-bound。

## 2. 一句话直觉

**Prefill 把整段 prompt 并行编码成可复用的 KV state；decode 以严格的 token dependency 逐步读取 weights 与不断增长的 KV cache。**

## 3. 它在一次请求哪里？

~~~mermaid
sequenceDiagram
    participant U as User
    participant S as Scheduler
    participant G as Accelerator
    participant M as KV Memory
    U->>S: prompt tokens
    S->>G: prefill batch
    G->>M: write K/V for every layer and prompt position
    G-->>U: first output token (TTFT)
    loop each generated token
      S->>G: decode step
      M->>G: read prior K/V
      G->>M: append new K/V
      G-->>U: next token (ITL/TPOT)
    end
~~~

TTFT 主要覆盖排队、tokenization、prefill 和首轮 sampling；ITL/TPOT 主要描述后续 decode cadence。End-to-end latency 还取决于 output length。

## 4. 前置知识：causal attention

对某层某个 token，attention 使用：

\[
Q=XW_Q,\quad K=XW_K,\quad V=XW_V
\]

\[
\operatorname{Attention}(Q,K,V)=
\operatorname{softmax}\left(\frac{QK^\top}{\sqrt{d}}\right)V
\]

Causal mask 保证位置 \(t\) 只能看见不晚于 \(t\) 的 token。生成到第 \(t+1\) 个 token 时，过去 token 的 K/V 不会变化，因此可缓存；新 token 只需计算自己的 Q/K/V，并用 Q 查询历史 K/V。

## 5. 从第一性原理理解

### 5.1 Prefill 为什么并行

Prompt 已全部已知。虽然 causal attention 有依赖语义，但每层可通过矩阵运算同时计算多个 token 的 projections 和 attention。大 \(M\)、\(N\)、\(K\) 维度形成较大的 GEMM，weights 可被许多 prompt tokens 复用，算术强度通常较高。

### 5.2 Decode 为什么串行

第 \(t+1\) token 依赖第 \(t\) token 的输出。标准 autoregressive sampling 无法在不知道当前 token 时精确计算后续 token。因此一次 decode iteration 的 token 维度很小；如果 batch 也不大，矩阵退化成 GEMV 或 skinny GEMM，读取 weights 的 bytes 很难被足够运算摊薄。

### 5.3 KV cache 为什么存在

若不缓存 K/V，每生成一个 token 都要重新计算此前所有 token 的 K/V。缓存用 memory capacity 与 bandwidth 换取计算避免。Sequence 越长、并发越高，KV 占用越大；它从优化手段变成 serving capacity 的核心约束。

## 6. Follow the Data

~~~mermaid
flowchart LR
    P[Prompt tokens] --> E[Embedding]
    E --> PF[Prefill: wide GEMMs + attention]
    W[Weights in HBM] --> PF
    PF --> KV[(KV cache)]
    PF --> T1[First token]
    T1 --> D[Decode: one step]
    W --> D
    KV --> D
    D --> KV
    D --> TN[Next token]
    TN --> D
~~~

每一层 decode 都要访问该层 weights，并读取与当前 attention 相关的历史 K/V。Weights、KV 和 intermediate buffers 的实际 bytes 由 quantization、GQA/MQA、tensor parallel layout、kernel fusion 和 cache hierarchy 决定。

## 7. Architecture：两个 phase 的对照

| 维度 | Prefill | Decode |
|---|---|---|
| 已知 token 数 | prompt 全部已知 | 每轮新 token 通常为 1 |
| 常见 compute shape | 宽 GEMM、attention | GEMV/skinny GEMM、incremental attention |
| 并行来源 | prompt tokens × batch × heads | concurrent sequences × heads |
| weight reuse | 同次调用中跨多个 tokens | 单 sequence 很低，靠 batching |
| KV 行为 | 批量写入 | 每轮读历史并 append |
| 常见 bound | compute、attention、长上下文 memory | HBM bandwidth、KV bandwidth、latency、scheduler |
| 用户指标 | TTFT | ITL/TPOT、generation rate |
| 调度风险 | 长 prompt 阻塞其他请求 | batch churn、finished sequence holes |

## 8. 关键 engineering parameters

| 参数 | 定义 | 为什么重要 | 容易混淆 |
|---|---|---|---|
| TTFT | 请求到首 token 的时间 | 交互开始速度 | 不等于 prefill kernel time |
| ITL | 相邻输出 token 间隔 | 流式阅读体验 | 平均值会隐藏 jitter |
| TPOT | 每输出 token 时间 | 常近似 decode cadence | 定义需说明是否含 queue |
| Throughput | 单位时间输出/处理 tokens | capacity/TCO | input 与 output tokens 应分开 |
| KV capacity | 可容纳的 active token state | concurrency 上限 | 不是 HBM 剩余容量的简单除法 |
| Goodput | 满足 SLO 的有效吞吐 | 连接性能和服务目标 | peak tokens/s 不是 goodput |
| Batch occupancy | 每 decode step 的 active sequences | weight reuse 与效率 | batch size 随时变化 |
| Prefix hit rate | 可复用 prefix 的请求比例 | 可减少重复 prefill | 需含 lookup/eviction 成本 |

## 9. 关键 equations 与 worked example

### 9.1 KV cache 容量

对常见 decoder Transformer，若每层保存 K 与 V，粗略容量：

\[
M_{\text{KV}}=
B\times S\times L\times 2\times H_{\text{KV}}\times D_h\times b
\]

其中：

- \(B\)：并发 sequences；
- \(S\)：每条 sequence 已缓存 token 数；
- \(L\)：层数；
- 2：K 与 V；
- \(H_{\text{KV}}\)：KV heads 数；
- \(D_h\)：每 head 维度；
- \(b\)：每元素 bytes。

例：\(L=80\)、\(H_{\text{KV}}=8\)、\(D_h=128\)、BF16 \(b=2\)。每 token：

\[
80\times2\times8\times128\times2=327{,}680\text{ bytes}\approx0.3125\text{ MiB}
\]

若总 active context 为 100,000 tokens，raw KV 约 31.25 GiB。实际系统还需 block metadata、alignment、fragmentation、workspace 和 weights；tensor parallel 可能把 KV 分片。

若使用传统 multi-head attention，\(H_{\text{KV}}\) 可能等于 query heads，容量更大；MQA/GQA 通过共享 KV heads 降低 KV bytes，但可能改变 quality 或 kernel/data-layout trade-off。

### 9.2 Decode 的 bandwidth lower bound

若一次 decode step 必须从 HBM 读取 \(W\) bytes 的 weights、有效带宽为 \(BW\)，且 weight traffic 不能从 cache 命中，则：

\[
t_{\text{step}}\ge \frac{W}{BW}
\]

[Estimate] 例如读取 70 GB quantized weights、有效 HBM 带宽 3 TB/s：

\[
t\ge 70/3000\text{ s}\approx23.3\text{ ms}
\]

这是极简 lower bound：未计 KV、communication、kernel inefficiency、sampling 与 synchronization。Batching 可让同一批 weight bytes 服务更多 sequences，提高 tokens/s，却不一定同比降低单请求 latency。

### 9.3 End-to-end latency

\[
T_{\text{E2E}}\approx T_{\text{queue}}+T_{\text{prefill}}+
N_{\text{out}}\times T_{\text{decode step}}
\]

实际首 token 已由首轮 decode/prefill 边界定义，公式用于直觉而非严格 profiling。

## 10. Bottleneck 怎么判断

- **TTFT 随 prompt length 快速上升**：检查 prefill compute、attention complexity 和 chunking。
- **ITL 随 batch 增大先改善后恶化**：可能 weight reuse 先提升，随后 KV/queue/collective 压力占主导。
- **短 prompt 也有高 TTFT**：queueing、cold start、tokenization 或 scheduling 可能主导。
- **长 context decode 变慢**：KV read 与 attention 工作随 context 增长。
- **HBM 仍有空闲却无法接请求**：可能 allocator fragmentation、reserved workspace、per-request limits 或 SLO admission 约束。
- **GPU utilization 高但 goodput 低**：可能长 prefill 阻塞 decode，或执行了违反 SLO 的工作。

## 11. Design Space

| 方案 | 解决什么 | 代价 | 适用条件 |
|---|---|---|---|
| Continuous batching | 提高 decode batch occupancy | scheduler/metadata 复杂 | 请求长度异构 |
| Paged KV | 降 fragmentation、支持动态增长 | page table、indirection、kernel integration | 高并发、ragged sequence |
| Chunked prefill | 限制长 prompt 对 decode 的阻塞 | 更多调度与边界 overhead | 混合 prefill/decode |
| Prefix caching | 避免重复 prompt 计算 | cache capacity、eviction、一致性 | system prompt/shared prefix 高复用 |
| KV quantization | 降 capacity/bandwidth | quality、dequant、kernel coverage | KV 成为主瓶颈 |
| MQA/GQA | 减 KV heads | architecture/quality trade-off | 模型设计阶段 |
| Speculative decoding | 一次验证多个候选 token | draft cost、acceptance 变化 | 易预测 token、合适 verifier |
| P/D disaggregation | 分别优化 phase、隔离干扰 | KV transfer、network、orchestration | 大规模稳定服务 |
| Larger batch | 增 weight reuse | queueing、KV、tail latency | 高流量或离线 |

## 12. 为什么最终需要 phase-aware scheduling

若把 prefill 和 decode 当作相同 jobs 先来先服务，长 prompt 的大计算块可能延迟许多活跃 decode sequence，造成 ITL spike。若永远优先 decode，新请求可能迟迟得不到首 token。

Scheduler 因此要在 TTFT、ITL、throughput 与 fairness 之间做 policy：限制 token budget、把 prefill 切块、动态合并 decode、设 priority，或把两阶段放到不同 worker。最佳策略取决于 arrival、prompt/output 分布、硬件 memory、network 与 SLO，而不是一个固定 batch size。

## 13. 为什么不……？

### 为什么不每次 decode 都重算整个 prompt？

这会重复 projection 和历史 K/V 计算，使生成长度增加时工作量急剧放大。KV cache 用 memory 换掉这些重复 compute。

### 为什么不把所有 HBM 都分给 KV？

Weights、runtime workspace、communication buffer、allocator reserve 与容错余量仍需要 memory。把可用空间推到 100% 会增加 OOM、fragmentation 和 admission failure。

### 为什么不无限增大 batch 提高 throughput？

Batch formation 增加 queueing；更大 batch 占更多 KV；每 step 时间可能上升，tail latency 违反 SLO。吞吐最优点不是 goodput 最优点。

### 为什么不把 prefill 和 decode 永远拆到不同芯片？

拆分可隔离 phase 并匹配硬件，但必须搬运 KV state。若 prompt 短、规模小或 network 慢，transfer 与调度成本可能超过收益。

### 为什么 speculative decoding 不能消除串行性？

它让较小 draft model 猜多个 token，再由 target model 并行验证。若 acceptance 低，额外 draft/verification 工作不能转化为足够 accepted tokens；最终语义仍需逐序列确认。

## 14. Trade-offs

~~~mermaid
flowchart LR
    B[More batching] --> R[Better weight reuse]
    R --> K[More KV + longer step]
    K --> L[Tail latency pressure]
    L --> P[Paging / chunking / priorities]
    P --> X[Runtime complexity]
~~~

性能不是 kernel 单点最优，而是 arrival process、scheduler、memory allocator 与 accelerator 的闭环。

## 15. Second-order effects

1. **Paged KV 把 OS 概念带入 accelerator runtime。** 价值从固定 tensor allocation 转向 block manager、scheduler 和 page-aware attention kernels。
2. **P/D 分离提升 network 与 memory semantics 的价值。** KV 传输需要带宽、低延迟、路由和生命周期管理。
3. **GQA/MQA 改变 silicon demand。** 减 KV bytes 后，weights 或 compute 可能重新主导。
4. **Long context 改变容量规划。** “每请求平均 tokens”不足以描述 tail；少量超长请求可占据大量 KV。
5. **Prefix caching 依赖 workload locality。** 产品流量与 prompt structure 会形成 software/data advantage，不能从芯片 spec 推导。

## 16. Workload mapping

| 场景 | Prefill/Decode 比重 | 最重要优化 |
|---|---|---|
| Chat，短 prompt 长回答 | decode 重 | ITL、weight/KV bandwidth、speculation |
| RAG，长上下文短回答 | prefill 重 | TTFT、chunked prefill、prefix reuse |
| Coding agent，长历史长输出 | 两者都重 | KV capacity、phase isolation、context policy |
| Batch summarization | 大 prefill、可放宽 latency | batching、throughput |
| Shared system prompt API | 重复 prefix | prefix caching |
| Offline synthetic data | decode 很重、SLO 宽松 | large batch、throughput/energy |

## 17. Real Product / system mechanisms

[Primary Source] vLLM 的 PagedAttention 论文借鉴 virtual memory paging，把 KV cache 切成 blocks，目标是减少 fragmentation 与冗余，从而提高 serving batch capacity。论文结果必须按其模型、硬件与 workload 边界解读，不能直接当作任意部署的固定倍数。

[Primary Source] Google speculative decoding 工作指出 autoregressive 生成 K 个 token 需要 K 次串行 target-model execution，并通过 draft + parallel verification 在不改变输出分布的前提下减少 target steps。收益依赖 acceptance 与实现。

[Primary Source] NVIDIA TensorRT-LLM 文档提供 KV cache、in-flight batching、quantization 与 disaggregated serving 的实现接口。作为厂商软件来源，它适合确认机制与支持状态；产品性能仍需在目标 SLO 下独立测量。

## 18. Product evolution

~~~mermaid
flowchart LR
    A[Static batching] --> B[Continuous batching]
    B --> C[KV fragmentation]
    C --> D[Paged KV]
    D --> E[Long context / high concurrency]
    E --> F[KV quantization + GQA]
    F --> G[Phase interference]
    G --> H[Chunked prefill / P-D disaggregation]
~~~

演进不是“一个优化取代全部旧机制”，而是 runtime 逐层管理更动态的 token state。

## 19. Engineers actually say

- “We are decode-bound.”：要问是 weight bandwidth、KV bandwidth、collective 还是 scheduler。
- “TTFT is dominated by queueing.”：增加 prefill FLOPS 可能不能解决。
- “KV utilization is 90%.”：要问 logical occupancy、physical blocks、reserved memory 与 fragmentation。
- “Continuous batching keeps the GPU full.”：GPU full 不等于 p99 goodput 高。
- “We disaggregate P and D.”：要问 KV transfer path、placement、failure semantics 和跨池负载平衡。
- “Spec decode gives 2×.”：要问 acceptance、draft overhead、model/task 和质量等价性。

## 20. 听到这些话意味着什么？

“每秒 10,000 tokens”必须拆成 input/output tokens，给出 prompt/output distribution、batch、TTFT/ITL SLO 与 precision。“支持 1M context”是功能上限，不是高并发下可持续性能。“KV cache 命中”需区分 prefix reuse 与普通 decode 对自身 KV 的读取。

## 21. 我应该追问工程师什么？

1. Prompt、output、并发和 arrival 的完整分布而非平均值是什么？
2. TTFT 中 queue、prefill、network、tokenization 各占多少？
3. ITL 如何随 context、batch 和 tensor parallel degree 变化？
4. Input 与 output throughput 是否分开报告？
5. KV 每 token bytes 如何由 layers、KV heads、head dimension 与 precision 推导？
6. Physical KV utilization、fragmentation 与 eviction rate 是多少？
7. Scheduler 如何处理长 prefill、priority 与 starvation？
8. Prefix cache 的真实 hit rate、eviction 和 correctness boundary？
9. Speculative acceptance rate 与 draft/verifier cost 各是多少？
10. P/D disaggregation 时 KV 走什么 link，搬运多少 bytes，是否与 compute overlap？
11. OOM 或 worker failure 后 request/KV 如何恢复？
12. 报告的 throughput 中有多少满足 TTFT 与 ITL SLO？

## 22. Common misconceptions

1. **“Prefill 等于 training。”** Prefill 只有 forward 且参数不更新；它只是 shape 和算术强度更像大 batch compute。
2. **“Decode 一次只算一个 token，所以很便宜。”** 它可能每步读取大部分 weights，并重复很多串行 steps。
3. **“KV cache 只影响容量。”** 长 context 下 KV read 也影响 bandwidth 与 latency。
4. **“更多 HBM 自动带来更低 ITL。”** Capacity、bandwidth、cache、kernel、interconnect 和 scheduler 都可能限制。
5. **“平均 latency 足够。”** 交互服务通常被 p95/p99 和 jitter 定义。

## 23. Engineering → Strategy

| Engineering change | System effect | Product effect | Business effect | Strategic implication |
|---|---|---|---|---|
| Paged KV | 降 fragmentation | 提高并发/goodput | 降 cost/token | Runtime 与 kernel integration 构成 moat |
| GQA/MQA | 降 KV bytes | 长 context/并发改善 | 降 memory 成本 | Model architecture 影响 hardware demand |
| Chunked prefill | 隔离长 prompt | 改善 ITL tail | 更稳定 SLO | Scheduler policy 产生产品差异 |
| Speculative decode | 减 target serial steps | 更快 generation | 可能降低 serving cost | 需要模型组合与 acceptance know-how |
| P/D disaggregation | phase-specific utilization | 独立扩缩容 | 提高 fleet efficiency | Network/orchestrator 进入 value stack |
| KV quantization | 增 capacity/降 traffic | 支持更多请求 | 延后 HBM 扩容 | Quality validation 是商业门槛 |

## 24. 投资 / M&A Technical Diligence

- **Workload:** benchmark 是否反映目标 prompt/output/arrival distribution？
- **Algorithm:** attention、GQA、speculation 或 cache 是否改变 output quality？
- **Architecture:** prefill 与 decode 的真实 bottleneck 各是什么？
- **Memory:** KV 公式、allocator、fragmentation、reserve 与 OOM policy 是否透明？
- **Silicon:** low-batch GEMV、skinny GEMM 与 attention kernel efficiency？
- **Network:** model sharding/P-D transfer 是否被计入？
- **Software:** scheduler、paging、prefix cache、priority 与 observability 成熟度？
- **Operations:** rolling update、failure、tenant isolation 与 abuse handling？
- **Economics:** cost/token 是否只计算满载 accelerator，还是含 idle 与 redundancy？
- **Moat:** 优势能否被开源 runtime 或 incumbent kernel update 复制？

## 25. 五个必须记住的 takeaway

1. Prefill 并行处理已知 prompt，decode 逐步生成未知 token；同一模型产生两种 workload。
2. TTFT 对应首 token 路径，ITL/TPOT 对应生成 cadence；必须连同 throughput 和 tail 一起看。
3. KV cache 用 memory 换避免重复计算，其容量随 active tokens、layers、KV heads 和 precision 线性增长。
4. Decode 常靠 batching 摊薄 weight reads，但 batching 会增加 queue、KV 与 tail latency。
5. 最佳 serving 性能来自 model architecture、memory、kernel、scheduler 和流量形态的共同设计。

## 26. 三个真正值得继续思考的问题

1. P/D disaggregation 普及后，KV 是否会成为一种需要独立协议、fabric 与 tiering 的系统对象？
2. 当 long-context 模型通过 GQA、compression 或 recurrent state 降低 KV，decode 瓶颈会回到 weights 还是 compute？
3. 如果 serving runtime 能按 SLO 动态选择 quantization、speculation 与 placement，硬件 benchmark 应如何重新定义？

## Sources

- [Primary Source] [Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180)
- [Primary Source] [Google Research — Fast Inference from Transformers via Speculative Execution](https://research.google/pubs/fast-inference-from-transformers-via-speculative-execution/)
- [Primary Source] [NVIDIA TensorRT-LLM — KV Cache System](https://nvidia.github.io/TensorRT-LLM/advanced/kv-cache-system.html)
- [Primary Source] [NVIDIA TensorRT-LLM — Disaggregated Serving](https://nvidia.github.io/TensorRT-LLM/features/disaggregated-serving.html)
- [Primary Source] [NVIDIA TensorRT-LLM — In-flight Batching](https://nvidia.github.io/TensorRT-LLM/advanced/gpt-attention.html)
- [Primary Source] [Attention Is All You Need](https://papers.neurips.cc/paper/7181-attention-is-all-you-need)


## 基础概念桥接

先把训练、prefill、decode、embedding、recommendation 与 multimodal 拆成不同 phase。明确 weights、activations、gradients、optimizer state、KV cache 的生命周期，再写 batch、sequence、precision、arrival distribution 和 SLO。模型名称本身不是硬件需求。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。


## 进阶工程术语桥接

本篇进一步需要掌握：微操作、流水线冒险、并行度、shape、动态批处理、尾延迟、数量级与单位经济性。阅读这些术语时，不只记中英文对应，还要补齐系统位置、正常路径、饱和或失败路径、直接 counter、端到端结果、产品状态和证据等级。若工程会议出现“已解决”“无开销”“已量产”，应立即追问 workload、boundary、configuration、status/date、failure mode 与 falsifier。

延伸阅读：[进阶工程术语手册](../31_glossary/advanced_engineering_terms_handbook.md)。
