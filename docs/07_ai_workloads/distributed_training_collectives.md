---
id: distributed_training_collectives
title: Distributed Training 与 Collectives：DP、TP、PP、EP 如何变成 Network Traffic
concepts: [distributed_training, data_parallel, tensor_parallel, pipeline_parallel, expert_parallel, collective]
prerequisites: [training, gpu_execution, scale_up, scale_out, rdma]
level: [2, 3, 4]
status: draft
last_verified: 2026-08-24
source_date: 2026-08-24
---

# Distributed Training 与 Collectives：DP、TP、PP、EP 如何变成 Network Traffic

> 第一次阅读：Sections 1–8  
> 第二次阅读：Sections 9–18  
> 深入阅读：Sections 19–26

## 阅读前后

读前需理解 [Training vs Inference](training_vs_inference.md)、[Scale-up vs Scale-out](../12_scale_up/scale_up_vs_scale_out.md)、[AI Ethernet/RDMA](../13_scale_out_networking/ai_ethernet_rdma.md) 与 GPU execution。读后应能从模型/optimizer/microbatch推导DP、TP、PP、EP产生的collectives、通信量、latency sensitivity、topology mapping与overlap条件。

## 1. 先告诉我为什么需要它

单颗accelerator受compute、HBM capacity与time限制。Distributed training把weights、activations、optimizer states或examples分到多个ranks。Partition解决单卡边界，却需要同步state；每种parallelism都会产生特定traffic。

Cluster performance不是GPU数量相加，而是最慢rank完成compute、communication与input pipeline后的step time。Collective tail、straggler或topology mismatch会让所有accelerators等待。

## 2. 一句话直觉

**Parallelism把本地memory/compute问题换成collective communication与synchronization问题；先画state如何切分，才能知道网络要搬什么。**

## 3. Parallel dimensions

~~~mermaid
flowchart TB
  MODEL[Training state] --> DP[Data Parallel]
  MODEL --> TP[Tensor Parallel]
  MODEL --> PP[Pipeline Parallel]
  MODEL --> EP[Expert Parallel]
  DP --> AR[Gradient All-Reduce / Sharding collectives]
  TP --> AG[All-Gather / Reduce-Scatter]
  PP --> P2P[Activation point-to-point]
  EP --> A2A[Token All-to-All]
~~~

## 4. 前置知识

Forward/backward、gradient、optimizer state、activation、rank、microbatch、collective、all-reduce、all-gather、reduce-scatter、all-to-all、ring/tree、bandwidth、latency、bisection与overlap。

## 5. Step Time Model

[
T_{step}=T_{compute}+T_{exposed comm}+T_{input}+T_{sync}+T_{recovery amortized}
]

Communication若与compute overlap，只有unhidden部分进入critical path。Overlap需要dependency-ready chunks、independent engines/resources与network progress；“async API”不等于实际隐藏。

## 6. Data Parallelism

每个rank保存model replica并处理不同examples，backward后需要聚合gradients。Classic DP常用all-reduce；sharded variants把parameters、gradients、optimizer states分散，使用reduce-scatter与all-gather降低memory，却增加通信frequency与lifecycle complexity。

## 7. Tensor Parallelism

将matrix或tensor维度切到多个ranks。单layer内常需all-reduce、all-gather或reduce-scatter，因此communication频繁且latency-sensitive，适合映射到high-bandwidth scale-up domain。Partition axis影响collective type与intermediate size。

## 8. Pipeline Parallelism

把layers分成stages，microbatches沿pipeline传activations/gradients。它主要产生neighbor point-to-point traffic，并引入pipeline bubble。更多microbatches可提高utilization，却增加activation memory、schedule与tail sensitivity。

## 9. Expert Parallelism

MoE把experts分到ranks，router将tokens送到selected experts，形成all-to-all。Traffic受token distribution与capacity policy影响，可能hotspot/imbalance。Nominal sparsity减少compute，不保证network更轻。

## 10. Collective Semantics

- All-Reduce：所有ranks得到reduced full result。
- Reduce-Scatter：reduce后每rank保留一片。
- All-Gather：收集各rank片段并让所有rank得到full result。
- All-to-All：每rank把不同片段发给所有destinations。
- Broadcast/Reduce：root与其他ranks的一对多/多对一。
- Send/Recv：pipeline或irregular neighbor transfer。

[Primary Source] NCCL文档明确指出Reduce-Scatter后接All-Gather在语义上可等价All-Reduce，但实际schedule、buffer与overlap可能不同。

## 11. Ring 与 Tree

Ring把large message分块沿环传递，bandwidth utilization好但steps随rank count增长；tree减少logical steps，适合latency-sensitive/smaller messages，但root/link load与topology mapping不同。Hierarchical算法先rack内后rack间，匹配scale-up/scale-out差异。

## 12. Communication Volume

Ring all-reduce每rank发送/接收量近似与tensor size成比例，并随rank数趋向固定倍数；但completion time还受per-step latency、link bandwidth、contention与algorithm影响。Volume不是唯一metric，path与concurrency同样重要。

## 13. Topology Mapping

TP group应优先放高bandwidth低latency domain；DP可跨更大scale-out；PP stages要考虑activation size与compute balance；EP需要高bisection与adaptive routing。Rank order决定ring/tree经过哪些links，错误mapping可跨越慢boundary多次。

## 14. 为什么不只用 Data Parallel？

DP简单且scales throughput，但每rank保留full model/state，受HBM capacity；global batch增加还影响optimization。Model太大时必须TP/PP/sharding，通信与software复杂度上升。

## 15. 为什么不把 Tensor Parallel 扩到整个 Cluster？

TP每layer频繁同步，对latency与bandwidth敏感。跨rack fabric较慢且contention高时，扩大TP会增加exposed communication。通常在fast domain内TP，再用DP/PP跨domain；具体边界由layer size与network决定。

## 16. 为什么不无限增加 Microbatches？

更多microbatches减少pipeline bubble，但增加activation storage、scheduler overhead与gradient semantics复杂度；microbatch过小还降低GEMM效率。Bubble、kernel efficiency与memory必须共同优化。

## 17. 为什么不总把 Communication Overlap 掉？

Collective依赖gradient/activation ready；communication engine可能与compute共享HBM/SM/PCIe；chunks太小增加latency，太大延迟start；congestion与stragglers让tail暴露。Overlap是资源调度，不是API flag。

## 18. 量化例：Communication 是否暴露

[Estimate] 假设一个gradient bucket为 (4 	ext{GB})，effective collective bandwidth为 (200 	ext{GB/s})，忽略latency则通信约 (20 	ext{ms})。若其后独立backward compute还能运行 (12 	ext{ms})，理想overlap后仍暴露约：

[
T_{exposed}approxmax(20-12,0)=8 	ext{ms}
]

真实系统还受chunking、contention、rank skew、memory bandwidth与protocol overhead影响。

## 19. ZeRO/FSDP 类 Sharding

Sharding降低每rank model-state memory，但在layer使用前all-gather parameters、backward后reduce-scatter gradients。Memory savings换communication frequency、prefetch、buffer与state-management。选择stage应从capacity shortfall与network headroom出发。

## 20. Stragglers 与 Reliability

Synchronous step由最慢rank决定。Thermal throttle、ECC recovery、network congestion、data loader、OS noise或bad link都可成为straggler。Large jobs的component-hours更高，failure probability上升；checkpoint interval与restart time进入effective throughput。

## 21. Workload Mapping 与 Second-order Effects

Dense transformer以DP/TP/PP组合；MoE再加EP；long sequence改变activation与attention communication；optimizer/precision改变state bytes。Collective优化后，bottleneck可能迁移到HBM copies、kernel granularity、CPU orchestration、storage或power synchronization。

## 22. Engineer language decoder

| 说法 | 应翻译成 | 追问 |
|---|---|---|
| “linear scaling” | 哪个range与efficiency baseline | batch/quality是否相同？ |
| “communication hidden” | timeline上多少bytes不在critical path | 共享HBM资源吗？ |
| “topology aware” | groups/ranks如何映射physical links | failure后remap呢？ |
| “sharded” | params/grad/optimizer哪部分 | all-gather频率与buffer？ |
| “network bound” | 哪个collective、message size与link | congestion还是endpoint？ |

## 23. 常见误解

1. **GPU增加会同比缩短time。**
2. **Collective bandwidth等于link bandwidth。**
3. **All-reduce只有一种算法。**
4. **MoE稀疏所以通信小。**
5. **Average step time足以评价large job。**

应同时看scaling efficiency、p50/p99 step、exposed communication、goodput与recovery-amortized time。

## 24. Product 与 Documentation Grounding

- [Primary Source] [NCCL Collective Operations](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/collectives.html) 定义all-reduce、all-gather、reduce-scatter、all-to-all等语义。
- [Primary Source] [PyTorch Pipeline Parallelism](https://docs.pytorch.org/docs/stable/distributed.pipelining.html) 描述stage partition、microbatch schedule与parallel techniques组合。
- [Vendor Claim] Library benchmark必须注明topology、message sizes、ranks、algorithm/protocol、NIC/GPU placement与contention。

## 25. Engineering → Strategy 与 Diligence

Distributed training moat横跨accelerator fabric、NIC/switch、collective library、compiler、scheduler、reliability与observability。Hardware bandwidth若software不能自动mapping/overlap，价值难兑现；proprietary scale-up可提高performance，也提高platform switching cost。

尽调应问：

1. DP/TP/PP/EP dimensions与physical mapping？
2. 每step各collective bytes/message distribution？
3. Exposed vs overlapped communication？
4. Collective algorithm如何按size/topology选择？
5. Bisection、oversubscription与congestion headroom？
6. Rank skew/p99 step来源？
7. Sharding节省memory付出多少traffic？
8. Failure、checkpoint与restart goodput？
9. Scaling是否保持batch、quality与time-to-target？
10. Software tuning多少是manual且model-specific？

## 26. 小结与延伸

Distributed training的第一步不是选网络，而是画state partition；collectives是parallelism的物理账单。把group映射到topology、把communication与compute overlap，并按goodput而非peak throughput评价系统。

下一步连接 [GPU Execution](../06_gpu_accelerator/gpu_execution_kernel_performance.md)、[AI Ethernet/RDMA](../13_scale_out_networking/ai_ethernet_rdma.md) 与后续quantitative cluster sizing。

## Sources

- [NVIDIA — NCCL Collective Operations](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/collectives.html)
- [NVIDIA — NCCL Documentation](https://docs.nvidia.com/deeplearning/nccl/)
- [PyTorch — Pipeline Parallelism](https://docs.pytorch.org/docs/stable/distributed.pipelining.html)
