# Compiler、Graph Lowering 与 Kernel Fusion：Software 如何兑现 Silicon

## 1. 高层 graph不能直接运行在 datapath上

Framework graph描述 matmul、attention、normalization等语义；compiler必须完成 shape/precision推导、layout、fusion、tiling、vectorization、memory planning、code generation与 runtime scheduling。每次 lowering都可能创造或丢失 locality。

~~~mermaid
flowchart LR
  G[Framework graph] --> H[StableHLO / IR]
  H --> F[Fusion + layout]
  F --> T[Tiling + vectorization]
  T --> M[Memory planning]
  M --> K[Kernel / executable]
  K --> P[Profiler feedback]
  P -.retune.-> F
~~~

[Primary Source] OpenXLA把 StableHLO/HLO映射到 backend，并把 fusion称为 GPU后端最重要的优化之一。MLIR提供多层 dialect与 tiling/fusion基础设施。IR不是文档细节，而是 hardware feature能否被发现和组合的控制点。

## 2. Fusion的收益

把 elementwise、bias、activation或 reduction与 producer/consumer合并，可避免中间 tensor写回 HBM、减少 launch和同步。收益近似：

<code>Saved bytes = removed writes + removed reads</code>

对于低 arithmetic intensity链条，bytes减少可显著移动 Roofline。Fusion还可保留 value在 register/shared memory。

## 3. Fusion的成本

更大 kernel增加 live ranges、register、shared memory与 code size，可能降低 occupancy或造成 spill。Dynamic shape产生许多 specialization；编译时间和 binary cache增长。一个复杂 fused kernel也更难 debug，并可能限制 independent ops overlap。

[Estimate] Fusion前两个 kernels各用40 registers、分别高 occupancy；fusion后 live state需要90 registers并发生 spill。虽然省去中间 tensor，新增 local-memory traffic可能抵消。必须用 profiler验证。

## 4. Layout propagation

Tensor logical shape相同，不同 physical layout会改变 coalescing、bank conflict与 matrix instruction匹配。若相邻 ops需要不同 layout，compiler可能插入 transpose/copy。单个 kernel很快，但 hidden layout conversion可主导 graph。

优秀 compiler在 graph级传播 layout，比较“一次转换换多次高效 compute”与保持通用 layout。产品 benchmark应披露 conversion是否计时。

## 5. Tiling与 memory hierarchy

Tile决定每层 data reuse和 parallel work。过小增加 overhead，过大超 register/shared memory或产生 tail。Optimal tile依赖 shape、dtype、architecture和 concurrent workload。

Auto-tuning能搜索，但成本高且 benchmark shape可能过拟合。Production需要 shape buckets、cache key、fallback与 compile-latency策略。

## 6. Dynamic shape与 graph break

Input length、batch、MoE routing和 control flow会让静态 graph假设失效。Compiler可生成 dynamic kernels、guard+specialization或 fallback eager。Guard miss触发 recompile会造成 tail，尤其在线 serving。

“支持 dynamic shape”应拆为正确运行、无需重编译、性能稳定和 memory安全。四者不同。

## 7. Numerical lowering

高层 dtype不等于 hardware accumulation。Compiler决定 cast、scaling、accumulator、reduction order与 fallback。低 precision优化必须通过 end-to-end quality；不同 fusion会改变 operation order和 rounding。

Fast-math flag可能提升速度却改变 NaN、denormal或 associativity。HPC和 training的接受边界不同。

## 8. Runtime与 scheduler

Compiled kernels还需 command queue、stream、event、memory allocator与 collective coordination。Graph capture减少 host launch，但可能降低 dynamic scheduling和 communication overlap。Serving continuous batching又要求快速改变 batch。

Software stack的价值在 compiler与 runtime共同选择，而非编译器单独峰值。

## 9. Why-not

- 为什么不 fusion所有 ops：resource pressure、compile time与并发。
- 为什么不手写所有 kernels：shape/architecture组合不可扩展。
- 为什么不只依靠 auto-tuner：搜索成本、过拟合和 determinism。
- 为什么不保持一个通用 layout：会浪费 hardware locality。
- 为什么不每个 shape专门编译：cache爆炸与在线 tail。

## 10. Product reality

要求从 framework输入到 executable拿到：

- graph breaks与 unsupported ops；
- fusion groups；
- layout conversions；
- tile/config；
- compile/cache time；
- kernel count；
- spill/occupancy；
- bytes与 critical path；
- software/hardware version；
- fallback比例。

若性能依赖 vendor工程师手工维护 model-specific patch，software moat可能同时是 services bottleneck。

## 11. Engineering → Strategy

| Compiler能力 | 工程价值 | 商业意义 |
|---|---|---|
| Fusion | 少 bytes/launch | silicon utilization |
| Layout | 用好 datapath | architecture portability |
| Auto-tune | shape优化 | onboarding |
| Dynamic shape | serving覆盖 | production adoption |
| Numerical lowering | 低精度质量 | model trust |
| Cache/runtime | 低 tail | SLO |
| Debug/profiling | root cause | ecosystem |

## 12. Diligence questions

1. 支持的 graph/operator/shape覆盖？
2. Fusion节省 bytes还是造成 spill？
3. Layout conversions多少、是否计时？
4. Compile latency和 cache hit？
5. Dynamic guard miss与 fallback p99？
6. 低 precision accumulation和 quality？
7. Collective能否与 compiled backward overlap？
8. 客户能否独立获得性能？
9. 新 architecture bring-up需要多久？
10. Benchmark多少来自 software release而非 silicon？

## 13. Takeaways

1. Compiler把 graph语义转为 locality、tiles和 machine instructions。
2. Fusion用更大 kernel换更少 memory与 launch。
3. Layout和 hidden conversion常比单 kernel peak重要。
4. Dynamic shape、compile cache和 fallback决定 production tail。
5. Software maturity是 delivered silicon的重要组成。

## Primary sources

- [Primary Source] [OpenXLA GPU Architecture Overview](https://openxla.org/xla/gpu_architecture)
- [Primary Source] [OpenXLA Operation Semantics](https://openxla.org/xla/operation_semantics)
- [Primary Source] [MLIR Documentation](https://mlir.llvm.org/)
