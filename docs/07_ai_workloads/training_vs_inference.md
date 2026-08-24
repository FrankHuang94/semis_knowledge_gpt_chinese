---
id: training_vs_inference
title: Training vs Inference：同一个模型，为什么需要两套系统思维
concepts: [training, inference, forward_pass, backward_pass, optimizer_state, parallelism, serving_slo]
prerequisites: [gpu, matrix_multiplication, tensor_core, transformer]
level: [2, 3, 4]
status: draft
last_verified: 2026-08-23
source_date: 2026-08-23
---

# Training vs Inference：同一个模型，为什么需要两套系统思维

> 第一次阅读：Sections 1–8  
> 第二次阅读：Sections 9–18  
> 深入阅读：Sections 19–26

## 阅读前后

**I should understand before:** GPU、GEMM、Tensor Core、Transformer 的基本 dataflow。  
**I should understand after:** 能从目标函数、state、parallelism、precision、SLO 和 economics 判断一套硬件或系统更适合 training 还是 inference，并识别“同一峰值 FLOPS”背后的错误类比。

## 1. 先告诉我为什么需要区分

Training 与 inference 都会执行同一个模型的 forward pass，因此很容易被简化成“训练算得更多，推理算得更少”。这个说法没有错，却会让采购、架构和投资判断错在最关键的地方。

Training 的目标是通过大量样本反复更新参数，使 loss 达到质量目标。系统必须保存 activation、计算 gradient、维护 optimizer state，并在多卡之间同步模型状态。它追求的是 **time-to-train、有效 tokens/s、收敛质量与训练成功率**。

Inference 的目标是在模型参数固定后，把请求变成预测或 token。它常受用户可感知的 latency、吞吐、并发、可用性和每 token 成本约束。对于自回归 LLM，推理内部又分成计算密集的 prefill 与串行、memory-sensitive 的 decode。

因此，training 优化的是一项有限但超大规模的“模型制造过程”；inference 优化的是一个持续运行、需求波动、SLO 驱动的“在线生产系统”。

## 2. 一句话直觉

**Training 是在大量并行数据上反复计算 forward + backward + update 来改变模型；inference 是用固定模型在请求约束下执行 forward，而价值由每个合格结果的成本与响应时间决定。**

## 3. 它们在整个 AI 生命周期哪里？

~~~mermaid
flowchart LR
    D[Data] --> T[Training<br/>forward + backward + update]
    T --> C[Checkpoint / Weights]
    C --> O[Optimization<br/>quantize / compile / shard]
    O --> I[Inference Serving]
    I --> R[Requests / Feedback]
    R -. data flywheel .-> D
~~~

Training 输出 checkpoint；checkpoint 经过量化、编译、分片、蒸馏或 serving-specific optimization 后进入 inference。线上反馈可能回流成下一轮数据，但这不意味着两阶段可以使用同一套性能指标。

## 4. 前置知识：一次训练 step 多了什么？

设模型为 \(y=f(x;\theta)\)，参数为 \(\theta\)，loss 为 \(L(y,\hat y)\)。

Inference 通常只需要：

\[
\hat y=f(x;\theta)
\]

Training 的一个 step 还需要：

\[
g=\nabla_\theta L(f(x;\theta),y)
\]

\[
\theta_{t+1}=\operatorname{Optimizer}(\theta_t,g_t,s_t)
\]

其中 \(s_t\) 是 momentum、variance 等 optimizer state。Backward 依赖 forward 中的中间 activation；optimizer 可能需要 master weights 与额外状态。因此训练的 live state 远大于仅保存 weights 的 inference。

## 5. 从第一性原理理解两者差异

### 5.1 计算图是否只向前

Inference 的主图是 forward。Training 需要 reverse-mode automatic differentiation：从 loss 开始沿计算图反向传播。对大多数 dense neural network，backward 不只是“再跑一次 forward”；它要分别计算 input gradient 与 weight gradient，并产生通信和状态更新。

### 5.2 参数是否变化

Inference 中 weights 在一个部署版本内基本只读，允许 aggressive caching、packing、quantization、kernel fusion 与离线编译。Training 每个 step 都改变参数，还必须保持 optimizer 与 distributed replicas 的一致性。

### 5.3 请求是否独立

Training 样本可形成大 global batch，通过 gradient accumulation 和并行化追求设备利用率。在线 inference 请求到达时间、prompt 长度、生成长度和 SLO 不同；scheduler 必须在 batching efficiency 与 tail latency 之间做交换。

### 5.4 正确性的定义不同

Training 正确性最终是 convergence 与 target quality，不是单次 kernel 的数值误差。Inference 正确性还包括 model quality、output distribution、determinism、安全约束与服务可用性。更低 precision 是否可用，必须看 end-to-end quality，而非 datatype 名称。

## 6. Follow the Data

~~~mermaid
flowchart TB
    subgraph Training
      DB[Dataset / tokens] --> FW[Forward]
      W1[Weights] --> FW
      FW --> A[Saved activations]
      FW --> L[Loss]
      L --> BW[Backward]
      A --> BW
      BW --> G[Gradients]
      G --> AR[Collective / reduction]
      AR --> OP[Optimizer states + update]
      OP --> W1
    end
    subgraph Inference
      Q[Requests] --> B[Dynamic batching]
      W2[Read-mostly weights] --> F2[Forward]
      B --> F2
      F2 --> K[KV / intermediate state]
      K --> F2
      F2 --> OUT[Predictions / tokens]
    end
~~~

Training 的 data movement 重点是 activations、gradients、optimizer states、checkpoint 和 collectives。Inference 的重点是 weights reuse、request batching、KV cache、token scheduling 与 host/network I/O。

## 7. Architecture：系统为什么分化

| 维度 | Training | Inference |
|---|---|---|
| 主操作 | forward + backward + optimizer | forward；LLM 为 prefill + iterative decode |
| 参数 | 每 step 更新 | 部署版本内只读 |
| 主要 state | weights、gradients、activations、optimizer | weights、KV cache、request state |
| 常见 parallelism | data、tensor、pipeline、expert、sequence | tensor/pipeline/expert；replica 与 request-level batching |
| 目标 | time-to-quality、tokens/s、scaling efficiency | TTFT、ITL/TPOT、throughput、tail latency、cost/token |
| batch | 通常大且可计划 | 动态、ragged、由流量与 SLO 限制 |
| precision | 受 gradient range 与 convergence 约束 | 通常更容易量化，但受 quality 约束 |
| failure cost | 长作业回滚、lost accelerator-hours | 用户请求失败、SLO breach、capacity loss |
| 生命周期 | 任务型、checkpoint 驱动 | 长期在线、多租户、弹性扩缩 |

硬件不必被永久标成“training chip”或“inference chip”。真正要问的是：给定 workload、software stack、scale 与 SLO，它能否把昂贵 silicon 保持在有效工作状态。

## 8. 关键 engineering parameters

| 参数 | Training 含义 | Inference 含义 | 常见误区 |
|---|---|---|---|
| Effective throughput | 达到质量要求的 samples/tokens per second | 满足 SLO 的 requests/tokens per second | 把 peak throughput 当有效吞吐 |
| Time-to-quality | 到指定 loss/accuracy 的 wall time | 通常不是主指标 | 只量每 step 时间而忽略收敛 |
| TTFT | 不常用 | Time To First Token | 只报平均值 |
| ITL / TPOT | 不常用 | Inter-token latency / time per output token | 与 end-to-end latency 混用 |
| Scaling efficiency | 多设备相对理想线性扩展 | 分片后延迟/吞吐变化 | 只报设备数 |
| Model FLOP utilization | 有效模型运算相对理论峰值 | 也可用，但受 batch/shape 影响更大 | 不说明 precision 与 sparsity |
| Memory footprint | model + gradients + activations + optimizer | weights + KV + runtime workspace | 忽略 fragmentation |
| Availability | 作业容错、checkpoint recovery | p99/p999、failover、rolling update | 把 benchmark 当 production |

## 9. 关键 equations 与 worked example

### 9.1 参数状态的数量级

若模型有 \(P\) 个参数，简单估算每参数训练状态：

- BF16/FP16 weight：2 bytes；
- gradient：2 bytes；
- FP32 master weight：4 bytes；
- Adam first and second moments：8 bytes。

未计 activation、temporary buffer 与 allocator overhead 时：

\[
M_{\text{train,state}}\approx 16P \text{ bytes}
\]

纯 16-bit inference weights：

\[
M_{\text{infer,weights}}\approx 2P \text{ bytes}
\]

一个 70B 参数模型仅上述状态约为：

\[
70\times10^9\times16 \approx 1.12\text{ TB}
\]

而 16-bit weights 约 140 GB。这只是用于说明量级；ZeRO/FSDP sharding、低精度 optimizer、offload 与 quantization 会改变每设备占用，activation 和 KV cache 则另算。

### 9.2 Training compute 的粗略估算

对 dense decoder-only Transformer，常见 first-order estimate 是训练每 token 约 \(6P\) FLOPs：

\[
F_{\text{train}}\approx 6PT
\]

其中 \(T\) 为训练 tokens。这个近似把 forward 约 \(2P\) 和 backward 约 \(4P\) 合并，忽略 attention 的 sequence-dependent 项、embedding、optimizer 与 MoE sparsity 等。

若 \(P=70\)B、\(T=1\)T：

\[
F\approx 6\times70\times10^9\times10^{12}=4.2\times10^{23}\text{ FLOPs}
\]

这不是采购报价；它是检查数量级、utilization 和 completion time 是否自洽的起点。

### 9.3 Inference economics

\[
\text{Cost per token}=
\frac{\text{annualized server + power + network + ops cost}}
{\text{SLO-compliant useful tokens}}
\]

分母必须是满足质量、可用性和 latency 约束的 token，不是离线最大 batch 下的峰值 token。

## 10. Bottleneck 如何迁移

### Training

- 大 GEMM 利用率高时，可能 compute-bound；
- model state 与 activation 放不下时，capacity-bound；
- tensor/data parallel collective 暴露时，communication-bound；
- pipeline bubble、straggler、checkpoint 或 input pipeline 会造成系统级 idle；
- power/thermal throttling 会让理论 throughput 无法持续。

### Inference

- 大 batch prefill 可能 compute-bound；
- decode 常反复读取 weights 与 KV，可能 memory-bandwidth 或 latency-bound；
- low traffic 时 batching 不足，利用率受 arrival process 限制；
- high traffic 时 queueing 与 tail latency 成为边界；
- disaggregated serving 中 KV transfer、network 和 orchestration 可能成为新瓶颈。

## 11. Design Space

| 选择 | Training 倾向 | Inference 倾向 | 代价 |
|---|---|---|---|
| 更大 batch | 提高 GEMM 与 collective efficiency | 提高吞吐但增加等待 | latency、memory |
| 更低 precision | 降 bytes、增 throughput，需保证 convergence | 可进一步量化，需校准 quality | accuracy、fallback |
| Activation checkpointing | 省 memory，重算 forward | 通常无对应价值 | compute 增加 |
| Weight/KV offload | optimizer/parameter offload 可扩模型 | 扩容量但增加 latency | interconnect traffic |
| Replication | data parallel | 扩吞吐和 availability | 复制 weights 的 capacity |
| Model sharding | 模型过大与 scale 需要 | 单卡放不下或 latency 目标 | communication、复杂度 |
| Compile/fusion | 提高 step efficiency | 减少 launch/DRAM traffic | shape flexibility、build time |

## 12. 为什么最终形成不同系统

Training 可以容忍较长单个 step latency，只要长期吞吐、收敛和扩展效率高。它因此接受大 batch、同步 collectives、复杂 sharding 和定期 checkpoint。

Inference 面向外部 arrival process。即使同一个 kernel 更快，排队、batch formation、KV allocation、token sampling 和 network serialization 仍可能主导用户体验。因此 serving 系统需要 admission control、continuous batching、priority、autoscaling、cache policy 与 observability。

它们共享 accelerator，却围绕不同 objective function 形成不同 software/hardware co-design。

## 13. 为什么不……？

### 为什么不直接用 training benchmark 选择 inference hardware？

Training benchmark 测到目标质量的时间；inference benchmark必须指定 scenario、latency constraint、batch、accuracy 与 power。大 batch 下领先不代表在线 p99 领先。

### 为什么不让 inference 永远使用最大 batch？

请求必须等待 batch 形成；batch 越大，queueing 与 KV/state 占用越高。若流量不足或 SLO 严格，最大吞吐点可能不可部署。

### 为什么不把 training 全部改成最低 precision？

Gradient 可能跨很大动态范围，optimizer accumulation 与 reductions 也有数值要求。低精度必须结合 scaling、accumulation format、stochastic rounding 或 recipe，并以 convergence 验证。

### 为什么不为两者各造完全独立 silicon？

两者仍共享 dense/sparse matrix compute、HBM、interconnect 与 compiler ecosystem。专用化能提高局部效率，但会牺牲 volume、flexibility、利用率池化和软件复用。

## 14. Trade-offs

~~~mermaid
flowchart LR
    C[Lower precision / larger batch] --> U[Higher utilization]
    U --> N[More communication or queueing]
    N --> S[Convergence risk or SLO pressure]
    S --> O[Need software scheduling + numerics]
~~~

Training 的代价常出现在 convergence、collective、checkpoint 和 job reliability；inference 的代价常出现在 tail latency、quality、capacity fragmentation 与 traffic variability。

## 15. Second-order effects

1. **Training compute 增长会放大 network value。** 单卡更快后，collective 占比上升，scale-up fabric、NIC 与 topology 变得更重要。
2. **Inference 增长会放大 memory capacity value。** 模型副本与 KV cache 决定并发，capacity 可能与 bandwidth 同样重要。
3. **更低 precision 把 moat 推向 software。** 格式支持不是终点，recipe、calibration、kernel coverage 与 fallback 决定可用性能。
4. **可靠性进入性能公式。** Training restart 浪费 accelerator-hours；inference outage 浪费已部署 capacity 并影响用户。
5. **需求形态改变最佳硬件。** 稳定高流量可形成大 batch；稀疏或突发流量更需要低 batch efficiency 与弹性。

## 16. Workload mapping

| Workload | 主导特征 | 优先指标 |
|---|---|---|
| Foundation model pretraining | 超大 token、长作业、distributed | time-to-quality、MFU、scaling、reliability |
| Fine-tuning / post-training | 数据较小、方法多样、频繁迭代 | iteration speed、flexibility、memory |
| Embedding / ranking inference | 可批处理、输出固定 | throughput、p99、cost/query |
| LLM online serving | ragged prompt、iterative decode、KV | TTFT、ITL、tokens/s、cost/token |
| Offline generation | 可放宽 latency、可大 batch | total throughput、energy/token |
| Edge inference | power/capacity/thermal 严格 | latency、energy、model footprint |

## 17. Real Product 与 benchmark 解释

[Primary Source] MLPerf Training 把性能定义为训练到指定 quality target 的 wall-clock time，而 MLPerf Inference 按部署 scenario 测量模型执行，并带有 accuracy、latency 和 power 等规则。两者存在的意义正是：不能用一套数字替代另一套系统目标。

[Primary Source] NVIDIA mixed-precision training guidance强调 lower precision 可减少 memory 与 bandwidth，并要求保留必要的 higher-precision state 和 loss scaling。这里应视为机制与软件 recipe 的来源，不应把厂商给出的 speedup 自动外推到任意模型。

[Primary Source] Google GPipe 展示 pipeline parallelism 如何让超出单加速器 memory 的网络跨设备训练，同时引入 microbatch 与 pipeline schedule。它说明 training scaling 不只是增加芯片数量，而是管理 state、dependency 与 bubble。

## 18. Product evolution

~~~mermaid
flowchart LR
    A[Model too large] --> B[Shard state / parallel training]
    B --> C[Communication wall]
    C --> D[Faster fabrics + overlap]
    D --> E[Compute and power wall]
    E --> F[Lower precision + specialized matrix]
    F --> G[Memory / reliability / software wall]
~~~

Inference 的演进则常是：

\[
\text{larger model}\rightarrow\text{quantization/sharding}\rightarrow
\text{higher concurrency}\rightarrow\text{KV pressure}\rightarrow
\text{paging/batching/disaggregation}
\]

每次优化都会把价值迁移到新的系统层。

## 19. Engineers actually say

- “The run is at 45% MFU.”：有效模型 FLOPs 只占理论峰值的一部分，需拆解 bubble、communication、kernel 与 downtime。
- “We are optimizer-state bound.”：容量问题不一定来自 weights，可能来自 master weights 与 moments。
- “Serving is SLO-bound, not throughput-bound.”：离线还能增加 batch，但线上 tail latency 不允许。
- “Quantization is not free.”：需要校准、kernel coverage、quality evaluation 和可能的 dequant overhead。
- “The cluster scales to 1,024 GPUs.”：必须追问相对多少卡、何种 parallelism、何种 model/sequence 与是否包含故障。

## 20. 听到这些话意味着什么？

“训练和推理都能跑”只代表功能覆盖；要问各自利用率与总成本。“支持 FP8/FP4”只代表 datapath 或软件路径存在；要问训练 convergence、推理 quality 与端到端覆盖。“线性扩展”必须给 baseline、规模区间和通信隐藏比例。

## 21. 我应该追问工程师什么？

1. Training 的 target quality、tokens、global batch 和 completion time 是什么？
2. Forward、backward、optimizer、communication、input 与 checkpoint 各占多少 wall time？
3. 每设备 weights、gradients、activations、optimizer state 和 fragmentation 分别多少？
4. Parallelism 组合是什么，为什么选择它？
5. 发生节点故障时恢复多少时间、丢失多少工作？
6. Inference 的 arrival distribution、prompt/output length 与 concurrency 分布是什么？
7. 报告的是 TTFT、ITL、end-to-end 还是平均 latency？p99 呢？
8. 吞吐数字是否在同一 accuracy、precision、batch 与 SLO 下？
9. Quantization 的模型覆盖、quality delta 与 fallback 比例是多少？
10. 低流量、突发流量和多租户条件下利用率如何？
11. 单机性能改善后，network、memory、power 哪个先成为新瓶颈？
12. 单位有效 token 的 fully loaded cost 包含哪些项目？

## 22. Common misconceptions

1. **“Training 就是 inference 的三倍计算。”** 这是粗略 FLOP 直觉，忽略 state、communication、optimizer、checkpoint 与 convergence。
2. **“Inference 不需要高端 interconnect。”** 大模型分片、MoE、prefill/decode disaggregation 仍可能依赖高带宽低延迟通信。
3. **“低 precision 对 inference 总是安全。”** 部分模型、层、任务或 sampling setting 对量化敏感。
4. **“Throughput 最高就是 TCO 最低。”** 若吞吐违反 SLO 或只在不现实 batch 达成，不能进入有效分母。
5. **“模型能装入 memory 就够了。”** 还需容纳 runtime workspace、KV、fragmentation 和故障冗余。

## 23. Engineering → Strategy

| Engineering change | System effect | Product effect | Business effect | Strategic implication |
|---|---|---|---|---|
| 更低 training precision | 减 bytes、增 matrix throughput | 更快 time-to-train | 降低一次模型迭代成本 | 数值 recipe 与软件栈成为 moat |
| 更大 HBM | 容纳 state/KV | 更大模型或并发 | 提高可售 workload 范围 | Memory 与 packaging 价值上升 |
| 更强 scale-up | 降 sharding/collective 时间 | 大模型扩展更好 | cluster ASP 与平台黏性提高 | Fabric control 影响平台权力 |
| Better serving scheduler | 提高 SLO-compliant utilization | 相同硬件服务更多请求 | 降 cost/token | Runtime 可产生接近 silicon 的价值 |
| 训练/推理解耦产品线 | 针对目标优化 | SKU 与部署选择增加 | 市场细分、库存复杂 | Volume 与 specialization 的权衡 |

## 24. 投资 / M&A Technical Diligence

- **Physics:** 性能是否受 package power、HBM power 或 cooling 限制？
- **Architecture:** datapath 对 training backward 和 inference ragged shapes 覆盖如何？
- **Silicon:** 支持的 datatype 是 native 还是组合模拟？
- **Memory:** 报告是否包括完整 state、KV、workspace 与 fragmentation？
- **Network:** 目标规模下 collective 或 model-shard traffic 多大？
- **Software:** framework、compiler、kernel、scheduler 与 observability 成熟度？
- **Quality:** training convergence 和 inference accuracy 如何验证？
- **Operations:** checkpoint、failover、rolling update 和 multi-tenancy 是否 production-ready？
- **Economics:** cost/token 或 time-to-quality 是否按完整系统与合理 utilization 计算？
- **Moat:** 优势来自可复制 benchmark tuning，还是 silicon + software + deployment data 的闭环？

## 25. 五个必须记住的 takeaway

1. Training 改变参数，inference 使用参数；这个差异决定 state、communication 与目标函数。
2. Training 看 time-to-quality；inference 看 SLO-compliant throughput、latency 与 cost，而非同一个峰值数字。
3. 训练的 memory 不只是 weights，推理的 memory 也不只是 weights：前者有 activation/gradient/optimizer，后者有 KV/request state。
4. 更快 matrix compute 会把 training 瓶颈推向 communication，把 LLM inference 瓶颈推向 memory 与 scheduling。
5. Durable advantage 通常来自 accelerator、memory、fabric、numerics 和 runtime 的共同设计。

## 26. 三个真正值得继续思考的问题

1. 当 inference 消耗超过 pretraining，产品 roadmap 会从峰值训练 FLOPS 转向哪些 SLO/TCO 指标？
2. Training 与 inference 的低精度格式是否会长期分化，还是被统一的 scale metadata 与 software recipes 合并？
3. 当 runtime 能通过 batching、paging、speculation 和 disaggregation 改变硬件利用率时，价值捕获会从 silicon 向哪一层移动？

## Sources

- [Primary Source] [MLCommons — MLPerf Training](https://mlcommons.org/benchmarks/training/)
- [Primary Source] [MLCommons — MLPerf Inference Documentation](https://docs.mlcommons.org/inference/index_gh/)
- [Primary Source] [NVIDIA — Train With Mixed Precision](https://docs.nvidia.com/deeplearning/performance/mixed-precision-training/index.html)
- [Primary Source] [Google Research — GPipe: Efficient Training of Giant Neural Networks](https://research.google/pubs/gpipe-efficient-training-of-giant-neural-networks-using-pipeline-parallelism/)
- [Primary Source] [Google Research — TensorFlow-Serving](https://research.google/pubs/tensorflow-serving-flexible-high-performance-ml-serving/)
- [Primary Source] [Attention Is All You Need](https://papers.neurips.cc/paper/7181-attention-is-all-you-need)
