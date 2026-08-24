# AI Workloads

> 目标：把 model execution 翻译成 compute、memory、network 与服务指标，而不是只记算法名称。

硬件需求来自 workload。即使使用同一个 Transformer，training、prefill 与 decode 也会产生不同的 state、shape、parallelism、data movement 与 objective function。

## Cornerstone sequence

1. [Training vs Inference：同一个模型，为什么需要两套系统思维](training_vs_inference.md)
2. [Prefill vs Decode：一次 LLM 请求为什么像两种不同 workload](prefill_vs_decode.md)
3. [Distributed Training 与 Collectives：DP、TP、PP、EP 如何变成 Network Traffic](distributed_training_collectives.md)
4. 下一步：MoE、recommendation 与 multimodal workloads。

先读 Training vs Inference，建立“模型制造”与“在线生产”的目标差异；再读 Prefill vs Decode，把 inference 继续拆成 compute-intensive 与 memory/latency-sensitive phases。

~~~mermaid
flowchart LR
    T[Training<br/>forward + backward + update] --> W[Weights]
    W --> P[Prefill<br/>many prompt tokens]
    P --> K[KV cache]
    K --> D[Decode<br/>iterative token]
    T -->|state + collective| SYS[System requirements]
    P -->|TTFT + compute| SYS
    D -->|ITL + memory| SYS
~~~

## 本模块默认问题

1. Model phase 的目标指标是什么：time-to-quality、TTFT、ITL、throughput 还是 cost/token？
2. Live state 是 weights、activations、gradients、optimizer state 还是 KV cache？
3. Shape 与 batch 能否给 matrix units 足够 reuse？
4. Bottleneck 是 compute、capacity、bandwidth、latency、communication 还是 scheduling？
5. 为提高利用率牺牲了 convergence、quality、tail latency 还是 reliability？
6. Benchmark 是否匹配真实 sequence、arrival、precision、SLO 与 system boundary？
7. 优化后价值迁移到 memory、fabric、runtime 还是 model architecture？
