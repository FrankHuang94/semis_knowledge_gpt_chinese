---
id: gpu_execution_kernel_performance
title: GPU Execution 与 Kernel Performance：Warp、Occupancy、Tiling、Coalescing 与 Stall
concepts: [gpu_execution, kernel, warp, occupancy, tiling, coalescing, stall]
prerequisites: [gpu, tensor_core, memory_hierarchy, roofline]
level: [2, 3, 4]
status: draft
last_verified: 2026-08-24
source_date: 2026-08-24
---

# GPU Execution 与 Kernel Performance：Warp、Occupancy、Tiling、Coalescing 与 Stall

> 第一次阅读：Sections 1–8  
> 第二次阅读：Sections 9–18  
> 深入阅读：Sections 19–26

## 阅读前后

读前需理解 [GPU Architecture](gpu_architecture.md)、[Tensor Core](tensor_core.md)、[Memory Hierarchy](../08_memory/memory_hierarchy.md) 与 [Roofline](../08_memory/roofline_model.md)。读后应能从 grid/block/warp、register/shared memory、memory access、instruction mix与synchronization解释kernel为何未达到peak，并选择profiling指标验证。

## 1. 先告诉我为什么需要它

同一GPU上，两个数学等价kernel可以相差很大。原因不是FLOPS消失，而是threads如何分组、memory transactions是否有效、data是否复用、warps是否足够隐藏latency、register是否spill、branches是否diverge，以及launch/synchronization是否把小工作切得过碎。

Kernel optimization就是把algorithm映射到GPU execution与memory hierarchy，同时避免从一个wall撞向另一个wall。

## 2. 一句话直觉

**GPU靠many ready warps隐藏latency，靠tiling复用数据，靠coalescing减少无效bytes；occupancy只是“可调度库存”，不是performance本身。**

## 3. Execution hierarchy

~~~mermaid
flowchart TB
  G[Grid] --> B[Thread blocks]
  B --> W[Warps]
  W --> T[Threads / lanes]
  SM[SM] --> SCH[Warp schedulers]
  SCH --> W
  SM --> RF[Registers]
  SM --> SH[Shared memory / L1]
  SH --> L2[L2]
  L2 --> HBM[HBM]
~~~

## 4. 前置知识

SIMT、warp、block、SM、register、shared memory、cache、HBM、latency、throughput、dependency、branch、arithmetic intensity、GEMM与Tensor Core。

## 5. Kernel lifecycle

CPU/runtime launch grid；blocks被分配到SM；每个block占用register/shared-memory与thread slots；warps在instructions ready时被scheduler选择；loads穿过memory hierarchy；completion与stream dependencies决定后续work。

Launch是异步提交，但跨streams/events、host sync或data dependencies可产生global bubbles。

## 6. Warp Scheduling 与 Latency Hiding

一个warp遇到long-latency load时，scheduler尝试发射另一个ready warp。需要足够independent warps与instructions，但资源限制会减少resident warps。若所有warps同时等待同一memory/fabric event，高occupancy也隐藏不了latency。

## 7. Occupancy

Occupancy通常是resident warps相对hardware上限的比例。它受threads/block、register/thread、shared memory/block与architecture limits共同约束。更高occupancy提供更多latency-hiding机会，却可能迫使register减少、增加spill或采用更差tile。

目标是足够occupancy，不是最大occupancy。

## 8. Register 与 Spill

Register是thread私有、低latency storage。Large tile、unrolling与更多accumulators提高reuse，但增加register pressure。当compiler无法分配，values会spill到local memory；“local”在address scope上私有，physical path可能进入cache/HBM，成本很高。

## 9. Shared Memory 与 Tiling

Block协同把global data加载到shared memory，多次复用后再写回。Tiling提高arithmetic intensity，也增加barriers、bank conflict、shared capacity与edge handling。Double buffering/software pipeline可重叠load与compute，但再增加register/shared需求。

## 10. Memory Coalescing

Warp threads的global accesses若落入少量aligned memory segments，hardware可合并transactions；scattered pattern搬运大量unused bytes。Data layout、stride、alignment与thread mapping决定useful-byte ratio。

[Primary Source] CUDA Programming Guide与Best Practices将coalescing列为关键memory optimization；具体transaction规则依architecture与cache mode，不应死记为跨世代常数。

## 11. Cache 与 Locality

L1/shared配置、L2 reuse与HBM traffic共同决定latency/bandwidth。Cache hit rate高不一定好：若反复访问无用metadata，仍浪费capacity。应看requested vs transferred bytes、reuse distance与which level serviced。

## 12. Branch Divergence

同一warp lanes走不同branch时，hardware可能串行执行paths并mask lanes。Divergence cost取决于path length、reconvergence与data distribution。把threads重排可提高branch coherence，却可能破坏coalescing或load balance。

## 13. Tensor Core Feeding

Tensor Core只在operands按支持shape/precision进入matrix instruction时工作。Data需要从HBM→L2→shared→register fragments并满足layout/alignment。Peak MMA throughput很高，因此address calculation、conversion、epilogue与synchronization更容易成为比例瓶颈。

## 14. 为什么不总用最大 Block？

Large block可能增加warps，但也占用更多register/shared resources，使每SM只能resident少量blocks，降低scheduling flexibility。Small block有更多placement freedom，却增加block overhead并可能无法合作加载tile。

## 15. 为什么不总追求最高 Occupancy？

Compute-bound kernel若已有足够ILP，增加warps未必增速；降低register以提高occupancy可能造成spill。Memory-bound random accesses即使高occupancy也受bandwidth/latency墙。要用stall reasons与resource sensitivity验证。

## 16. 为什么不把所有数据都放 Shared Memory？

Shared capacity有限、按block scope、需要explicit movement和barrier。低reuse data搬进shared只增加traffic；跨blocks reuse可能更适合L2。Tile选择必须覆盖reuse、capacity与synchronization成本。

## 17. 为什么不把 Kernel 无限 Fusion？

Fusion减少launch和intermediate HBM traffic，却增大register pressure、instruction cache、scheduling constraints与compilation complexity。Producer/consumer shapes不匹配时，materialization可改善parallelism。最佳fusion边界由traffic saved与resource loss共同决定。

## 18. 量化例：Coalescing Waste

[Estimate] 假设warp逻辑上请求 (128) bytes useful data。Coalesced mapping恰好搬运 (128) bytes；strided mapping若触发 (32) 个独立 (32)-byte transactions，则搬运 (1{,}024) bytes，useful-byte efficiency只有：

[
eta=rac{128}{1024}=12.5%
]

具体segment与cache行为依GPU architecture；例子只说明相同logical loads可能产生完全不同physical traffic。

## 19. Roofline 与 Stall Taxonomy

Roofline先判断compute vs memory upper bound；profiler再分解instruction dependency、memory throttle、memory dependency、barrier、not-selected、execution-pipe busy等stall。Counter是证据，不是结论：需关联source、timeline与controlled experiment。

## 20. Launch、Streams 与 Graphs

Small kernels可能被launch latency与host orchestration主导。Streams允许independent work overlap；events表达dependency；graphs可减少重复launch overhead。Overlap只有在hardware engines、resources与dependencies允许时成立，timeline应验证而非假定。

## 21. Workload Mapping 与 Second-order Effects

Prefill大GEMM更易compute-bound；decode小batch/irregular memory更易latency或bandwidth-bound；embedding/sparse kernels受gather与imbalance；attention随sequence、tile与KV layout变化。优化kernel后，bottleneck可能迁移到launch、communication、CPU feeding或power。

## 22. Engineer language decoder

| 说法 | 应翻译成 | 追问 |
|---|---|---|
| “low occupancy” | 哪个resource限制resident warps | stall真的因无ready warp吗？ |
| “memory bound” | 哪层、bandwidth还是latency | requested/transferred bytes？ |
| “tensor core utilization” | 哪种instruction与active cycles | feeding/epilogue成本？ |
| “fused” | 少了哪些launch和traffic | register/spill变化？ |
| “coalesced” | warp access映射到多少transactions | alignment和tail呢？ |

## 23. 常见误解

1. **Occupancy等于utilization。**
2. **Cache hit高就高效。**
3. **Tensor Core存在就会被使用。**
4. **Fusion越多越好。**
5. **Profiler top counter就是root cause。**

每个判断都应通过单变量实验：改变block、tile、layout、precision或fusion，并观察performance与traffic如何响应。

## 24. Product 与 Documentation Grounding

- [Primary Source] [CUDA Programming Guide](https://docs.nvidia.com/cuda/cuda-programming-guide/) 定义thread hierarchy、memory与execution model。
- [Primary Source] [CUDA Best Practices Guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/) 给出coalescing、occupancy与optimization methodology。
- [Vendor Claim] Peak throughput或tool-derived utilization必须带architecture、precision、clock、power、kernel shape与counter definition。

## 25. Engineering → Strategy 与 Diligence

Hardware value只有通过compiler、libraries与kernels实现。成熟kernel ecosystem、profiling、backward compatibility与developer productivity可形成moat；新accelerator若要求重写大量layout/fusion才能达到peak，会增加adoption cost。

尽调应问：

1. Benchmark是end-to-end还是isolated kernel？
2. Shape、batch、precision与data layout？
3. Achieved bandwidth/compute与Roofline距离？
4. Register/shared use、spill与occupancy？
5. Requested/transferred bytes与coalescing？
6. Kernel launch/sync占比？
7. Fusion前后traffic与resource变化？
8. Performance对shape/sequence敏感度？
9. Compiler/library版本与autotuning time？
10. 优化是否牺牲accuracy、generality或maintainability？

## 26. 小结与延伸

GPU performance来自execution、memory与software mapping的联合效率。先用Roofline定位bound，再用timeline、traffic、resource与stall实验找因果，不要用单一occupancy或peak FLOPS解释。

下一步阅读 [Distributed Training & Collectives](../07_ai_workloads/distributed_training_collectives.md)。

## Sources

- [NVIDIA — CUDA Programming Guide](https://docs.nvidia.com/cuda/cuda-programming-guide/)
- [NVIDIA — CUDA Best Practices Guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/)


## 基础概念桥接

先区分 thread、warp、block、SM、occupancy、utilization、register、shared memory 和 HBM。线程很多不等于计算单元忙碌；shape、tiling、coalescing、fusion 与 kernel coverage 决定峰值能否兑现。低精度或稀疏还必须通过质量约束。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。
