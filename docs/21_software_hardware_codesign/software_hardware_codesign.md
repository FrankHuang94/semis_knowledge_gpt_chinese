---
id: software_hardware_codesign
title: Software / Hardware Co-design：Graph、Compiler、Kernel、Runtime 与 Silicon 如何闭环
concepts: [software_hardware_codesign, compiler_ir, graph_compiler, kernel_library, autotuning, runtime]
prerequisites: [gpu_execution, tensor_core, memory_hierarchy, distributed_training]
level: [2, 3, 4]
status: draft
last_verified: 2026-08-24
source_date: 2026-08-24
---

# Software / Hardware Co-design：Graph、Compiler、Kernel、Runtime 与 Silicon 如何闭环

> 第一次阅读：Sections 1–8  
> 第二次阅读：Sections 9–18  
> 深入阅读：Sections 19–26

## 阅读前后

读前需理解 [GPU Execution](../06_gpu_accelerator/gpu_execution_kernel_performance.md)、[Tensor Core](../06_gpu_accelerator/tensor_core.md) 与 [Distributed Training](../07_ai_workloads/distributed_training_collectives.md)。读后应能把model graph逐层lower到IR、fusion/layout、kernels、runtime与hardware，并判断peak specs为何可能无法转化为portable performance。

## 1. 先告诉我为什么需要它

Framework表达的是operators与graphs，hardware执行的是instructions、memory transactions和collectives。中间还有shape specialization、precision、layout、fusion、tiling、kernel selection、memory planning与runtime。任何一层mapping不好，silicon就会idle。

Co-design用workload feedback共同改变ISA、memory hierarchy、compiler、libraries与model structure，使useful performance、portability和developer cost联合最优。

## 2. 一句话直觉

**Hardware提供可能性，compiler/library/runtime决定可达性；moat是从model intent到silicon counters的快速反馈闭环。**

## 3. Software stack

~~~mermaid
flowchart TB
  M[Model / framework graph] --> IR[Stable high-level IR]
  IR --> OPT[Canonicalize / fusion / layout / precision]
  OPT --> LIR[Target-specific IR]
  LIR --> KL[Library / generated kernels]
  KL --> RT[Runtime / memory / collectives]
  RT --> HW[Compute + memory + fabric]
  HW -. counters .-> OPT
~~~

## 4. 前置知识

Graph、operator、IR、SSA、pass、lowering、code generation、autotuning、ABI、shape、layout、precision、fusion、memory planning与profiling。

## 5. Why Intermediate Representations

Framework ops太high-level，machine instructions太specific。Multi-level IR在不同抽象层保留语义，使canonicalization、fusion、layout与target lowering分离。Stable interface允许framework与backend独立演进；semantics、versioning和debug决定它是否真portable。

## 6. Graph Capture 与 Dynamic Shape

Data-dependent shape、control flow与host side effects阻碍whole-graph optimization。Compiler可specialize常见shapes并fallback others。Specialization提高性能，却增加compile time、code cache与version matrix。Serving shape distribution必须进入设计。

## 7. Canonicalization

同一计算有多种graph形式。Canonicalization把patterns变成统一表示，便于后续passes，同时保持numerics、side effects与shape constraints。[Primary Source] MLIR文档把canonicalization作为multi-level IR共享基础设施，说明co-design需要可组合转换。

## 8. Fusion

Fusion减少launch与intermediate HBM traffic，并共享tile；代价是register/shared pressure、code size、parallelism和compile complexity。Memory-bound chain常受益，large compute ops之间未必。

## 9. Layout

Row/column-major、blocked/tiled layouts影响coalescing、Tensor Core和collectives。Layout conversion本身搬data。Whole-graph optimizer要避免每个operator局部最优而边界反复transpose。

## 10. Precision 与 Quantization

Lower precision提高throughput/capacity/bandwidth efficiency，但需scale、accumulation、calibration与error control。Hardware支持格式不等于graph覆盖；conversion overhead和unsupported ops会吃掉收益。

## 11. Kernel Library 与 Generation

Hand-tuned libraries对common shapes可靠；generated kernels覆盖long tail并specialize。Library维护成本高，generator依赖cost model和compiler quality。成熟stack通常混合dispatch与JIT/autotune。

## 12. Autotuning

Tile、block、warps、pipeline stages与algorithm构成大search space。Autotuning可用measurement或cost model。Search可amortize于长期workload，但dynamic serving难承受。Cache key、driver/hardware版本与reproducibility是production问题。

## 13. Runtime 与 Memory Planning

Runtime管理buffers、streams、events、graphs、collective communicators和dependencies。Memory planner复用lifetime不重叠的buffers；runtime也决定prefetch、KV placement、batching和failure handling。

## 14. 为什么不让 Compiler 自动解决一切？

Compiler只能优化可见语义；opaque custom ops、alias、dynamic state、numerical constraints与distributed placement会限制。Cost model也可能失配。Human kernels仍重要，但经验应反馈进compiler。

## 15. 为什么不只依赖 Hand-tuned Libraries？

Model/shape/precision变化快，library无法覆盖全部组合。只用libraries产生coverage gaps和layout boundaries；generated code提高coverage，却要验证numerics、predictability与compile overhead。

## 16. 为什么不暴露所有 Hardware Details？

过多target details破坏portability并增加author负担；过少又难表达sparsity、memory scope或collective intent。应在IR逐层增加target information，并保留fallback。

## 17. 为什么不逐 Operator 优化？

End-to-end layout、fusion、memory peak、overlap与communication可能反转单-op choice。Fastest GEMM若要求昂贵transpose，整体更慢。Optimization boundary必须覆盖真实request/step。

## 18. 量化例：Fusion 的 Traffic Value

[Estimate] 两个elementwise ops之间materialize (1 	ext{GB}) tensor，write+read增加 (2 	ext{GB}) HBM traffic。若effective bandwidth为 (1 	ext{TB/s})，理想traffic time：

[
T=rac{2 	ext{GB}}{1000 	ext{GB/s}}=2 	ext{ms}
]

Fusion最多先消除这部分；若spill/occupancy损失更大，实际会变慢。

## 19. Portability

Portable IR/ABI降低framework×backend组合爆炸，但lowest-common-denominator限制unique hardware。Custom call提供escape hatch，却会重建lock-in。要区分correctness、functional coverage与performance portability。

## 20. Compilation Modes

AOT适合stable deployment与fast startup；JIT适合shape specialization；online autotuning追求best performance但增加warm-up。Production需要artifact cache、rollback与reproducible build。

## 21. Distributed Co-design

Compiler可表达sharding、insert collectives、schedule overlap和layout；runtime映射groups到topology。若parallel plan与network分离，collective会跨慢links。Distributed IR还需placement、replication与failure semantics。

## 22. Engineer language decoder

| 说法 | 翻译 | 追问 |
|---|---|---|
| “compiler optimized” | 哪些passes/shapes | fallback与compile time？ |
| “portable” | correctness/coverage/performance | custom ops？ |
| “fused” | 少了哪些buffers | resource pressure？ |
| “automatic sharding” | objective/topology inputs | robustness？ |
| “zero overhead” | 哪个baseline | JIT/runtime含吗？ |

## 23. 常见误解

Framework支持不等于高性能；IR标准不自动带来performance portability；fusion不是越多越好；hardware op存在不代表compiler会用；single-op benchmark不代表model speed。

## 24. Primary Sources

- [Primary Source] [MLIR Documentation](https://mlir.llvm.org/docs/) 说明multi-level IR与dialect/pass infrastructure。
- [Primary Source] [OpenXLA StableHLO](https://openxla.org/stablehlo) 提供framework/compiler之间的portable operation set。
- [Primary Source] [CUDA Programming Guide](https://docs.nvidia.com/cuda/cuda-programming-guide/) 提供target execution/memory semantics。
- [Vendor Claim] Compiler speedup需注明graph、shapes、precision、baseline、compile time与fallback。

## 25. Engineering → Strategy 与 Diligence

Software stack把hardware feature变成accessible performance，也是switching cost来源。Moat来自IR、kernel corpus、autotuning data、profiling、integration与backward compatibility。

尽调应问model→IR→kernel path、shape/precision coverage、fallback、compile/warm-up、fusion/layout traffic、numerical validation、new-feature enablement time、distributed mapping、regression tests与customer custom code。

## 26. 小结与延伸

Software/hardware co-design是持续反馈系统：workload intent经IR、compiler、kernel与runtime落到silicon，counters再返回优化。能缩短这个loop的平台，更容易把新hardware转成end-to-end value。

下一步进入 Engineering-to-Strategy、Technical Diligence、quizzes与quantitative toolkit。

## Sources

- [MLIR — Documentation](https://mlir.llvm.org/docs/)
- [OpenXLA — StableHLO](https://openxla.org/stablehlo)
- [NVIDIA — CUDA Programming Guide](https://docs.nvidia.com/cuda/cuda-programming-guide/)


## 基础概念桥接

先区分 framework graph、IR、lowering、fusion、kernel、runtime、driver 与 firmware。硬件 feature 只有被正确导入、覆盖、调试和部署才产生价值。首次编译、warm cache、dynamic shape、fallback 与版本回归需要分别测量。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。


## 进阶工程术语桥接

本篇进一步需要掌握：graph lowering、autotuning、ABI、firmware、observability、canary、fault injection 与 blast radius。阅读这些术语时，不只记中英文对应，还要补齐系统位置、正常路径、饱和或失败路径、直接 counter、端到端结果、产品状态和证据等级。若工程会议出现“已解决”“无开销”“已量产”，应立即追问 workload、boundary、configuration、status/date、failure mode 与 falsifier。

延伸阅读：[进阶工程术语手册](../31_glossary/advanced_engineering_terms_handbook.md)。
