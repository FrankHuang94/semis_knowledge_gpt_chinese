# Compute-bound vs Memory-bound：从一句诊断到可证伪的 Performance Model

## 1. “受算力限制”不是 profiler上的一个颜色

Compute-bound表示在给定实现和边界下，提高有效 arithmetic throughput最可能缩短时间；memory-bound表示数据供给的 bandwidth、latency或 transaction efficiency更主导。它们不是 workload的永久属性：shape、batch、precision、cache、fusion、tiling、hardware与 software版本变化后，瓶颈可以迁移。

同一个 Transformer中，大矩阵乘法可能接近 compute-bound，decode小 batch的 weight读取可能 memory-bandwidth-bound，embedding gather可能 latency/transaction-bound，collective又受 network限制。正确单位是“某个 phase中的某个 kernel或 pipeline”，不是“这个模型”。

~~~mermaid
flowchart TD
  K[Kernel / Phase] --> O[Count useful operations]
  K --> B[Count bytes by memory level]
  O --> AI[Arithmetic intensity]
  B --> AI
  AI --> R[Compare with machine balance]
  R --> P[Profiler: stalls / occupancy / transactions]
  P --> X[Experiment: change compute or bytes]
  X --> D[Bound diagnosis]
~~~

## 2. Roofline给出第一条可证伪边界

Arithmetic Intensity定义为每次从目标 memory level移动一 byte所完成的 operations。Machine balance是 peak operations除以 peak bandwidth。若 workload intensity低于 ridge point，理论 roofline由 bandwidth决定；高于 ridge point，则由 compute peak决定。

<code>P_bound = min(P_peak, Bandwidth × Arithmetic Intensity)</code>

[Primary Source] Berkeley Lab的 Roofline材料强调把 arithmetic intensity与 machine ceilings放在同一图上。这里的关键是“目标 memory level”：用 HBM bytes、L2 bytes或片上 SRAM bytes会得到不同 intensity。把 cache hit后的 bytes和 HBM peak混在一起会制造虚假结论。

## 3. Operations 与 bytes应如何数

Operations可以来自 algorithm、compiler IR、hardware counter或 kernel工具；必须统一 FMA计数、sparsity、masked lanes与有效 work。Bytes要区分 requested、transacted、cache-line、read/write、compression前后与 protocol overhead。

一个 GEMM的理论 data reuse很高，但若 tile不合适、cache thrash或边界 padding严重，实际 bytes会增加。一个 elementwise kernel理论每元素工作少，若与前后算子 fusion，就能避免中间 tensor写回，intensity会显著上升。

因此模型至少保留三列：

| 层 | 需要记录 |
|---|---|
| Algorithm | 理想 ops、最少 bytes |
| Implementation | tile、fusion、padding、layout |
| Hardware | 实际 transactions、stall、active cycles |

## 4. Worked example：为什么 peak翻倍可能几乎没用

[Estimate] 某 accelerator peak为1000相对 compute单位，HBM bandwidth为4相对 bandwidth单位，ridge point为250 operations/byte。Kernel A intensity为50，则 roofline ceiling为200；Kernel B intensity为500，则 roofline ceiling为1000。

若下一代 compute peak翻倍而 bandwidth不变：

- Kernel A ceiling仍为200，理论 speedup接近1；
- Kernel B ceiling从1000变为2000，若其他效率不变，可能接近2；
- 新 ridge point变为500，原本边界附近的 kernel更容易变 memory-bound。

这说明算力升级会制造新的 memory wall。产品比较应按目标 kernel intensity分布加权，而不是把所有 workload乘 headline speedup。

## 5. Memory-bound也要继续拆

### Bandwidth-bound

有足够 outstanding requests，访问较连续，但总 bytes接近可用 bandwidth ceiling。优化方向是减少 bytes、提高 reuse、压缩/量化、fusion或增加 bandwidth。

### Latency-bound

依赖链或并行 request不足，单次 access等待无法被隐藏。即使 aggregate bandwidth很低，增加 bandwidth也不一定有用。Pointer chasing、小 batch gather与同步 metadata常见。

### Transaction-bound

小而不合并的访问使每个 useful byte触发更大 transaction；bank conflict、TLB miss、cache-line waste或 read/write turnaround主导。优化 layout、coalescing、page与 batching比增加 pin rate有效。

### Capacity-bound

工作集放不进目标层，触发 paging、remote access、recomputation或减小 batch。它不是运行时 bandwidth的同义词，但会改变整个 schedule。

## 6. Compute-bound也要继续拆

Arithmetic pipeline可能被 instruction issue、dependency、tensor-core shape、occupancy、register pressure、special-function unit或 branch限制。Profiler显示高 compute utilization不等于所有 operations有业务价值：padding、masked lanes与重复计算也会占满 datapath。

低 occupancy不必然坏。如果单个 warp有足够 ILP且 kernel接近 peak，增加 occupancy没有收益；反之，register spill为提高 occupancy而发生，可能把 compute-bound变成 memory-bound。

## 7. 三类验证实验

### 改 compute，不改 bytes

降低 precision、使用更强 matrix instruction或改变 clock。如果时间几乎不变，compute可能不是第一约束；但 precision也会改变 bytes与 kernel path，需要控制变量。

### 改 bytes，不改数学

Fusion、cache blocking、压缩、改变 batch reuse。若时间随外部 bytes减少而下降，支持 memory-bound诊断。必须测实际 transactions，而非只看源代码 tensor大小。

### 改 problem shape

增加 batch、矩阵维度或 sequence。若大 shape利用率显著提高，原问题可能被 launch、tail tile或并行度限制。若 performance随 working set超过 cache突然下降，说明 hierarchy边界。

## 8. 为什么不只看 utilization

“GPU utilization”常表示一段时间内设备有 kernel运行，不表示 matrix units有用地工作。Memory controller utilization高也可能来自无效 transaction。指标必须具体到 active cycles、eligible warps、stall reason、tensor pipe、cache hit、HBM read/write与 achieved occupancy。

一个服务可同时有设备 utilization高、单请求 latency差：continuous batching让机器忙，但长队列增加等待。Hardware efficiency与 user SLO应分开。

## 9. 为什么不把所有 kernel fusion

Fusion减少 launch和中间 memory traffic，但会增大 register/live range、降低 occupancy、限制 scheduler重排，并让 compilation与 cache复杂。过大 kernel的一个慢路径会阻塞其他 work；dynamic shape也可能造成大量 specialization。

应该按 bytes saved与新增 resource pressure判断，并保留 profiler证据。Fusion不是风格偏好，而是改变 memory/compute balance的实验。

## 10. 为什么不靠更大 cache解决 memory-bound

Cache只对 reuse distance可覆盖的数据有效。Streaming weight、一次性 activation或随机大 embedding不会因 cache变大自动命中。Cache增加还消耗 die area、leakage与 access latency，并可能减少 compute。

更重要的是 software要产生 locality。若 scheduler在 requests之间频繁切换 working set，或 layout使相邻 lanes访问分散，cache capacity会被浪费。

## 11. Pipeline层面的瓶颈迁移

Kernel优化后，host launch、data loader、network collective、queue或 storage可能变主导。端到端时间可以写成关键路径而不是所有阶段简单相加，因为 copy、compute与 communication可能 overlap。

优化前必须画 timeline：哪些操作串行、哪些并行、哪项决定最后 completion。把一个完全隐藏的 kernel加速不会改变 step/request time；把一个小但暴露在 barrier前的 tail消除，可能价值很大。

## 12. Second-order effects

1. 更低 precision同时改变 compute peak、bytes与 accuracy。
2. Fusion减少 HBM traffic，却可能增加 register spill。
3. Batch提高 reuse和 compute efficiency，却增加 queue与 tail latency。
4. Cache增加可能把 bottleneck移到 crossbar或 bank ports。
5. Compression减少 bytes，却增加 decode compute与 metadata。
6. Kernel加速后，collective overlap窗口缩短，exposed communication反而增加。
7. Hardware peak升级后，software shape与 data placement价值上升。

## 13. Engineers actually say

- “This is memory-bound.”：问哪一层、bandwidth/latency/transaction/capacity哪一种。
- “We hit ninety percent utilization.”：问哪个 counter与 useful work。
- “Roofline says compute-bound.”：问 operations、bytes与 ceiling如何定义。
- “Fusion makes it faster.”：问 bytes saved、register、occupancy与 shape coverage。
- “The cache is too small.”：问 reuse distance与 miss分类。
- “The new GPU gives no speedup.”：问 machine balance与 bottleneck迁移。

## 14. Engineering → Strategy

| 诊断 | 最可能的投入 | 新瓶颈 | 价值受益方 |
|---|---|---|---|
| Compute-bound | datapath/precision/kernel | memory/network | accelerator IP |
| HBM bandwidth-bound | HBM、tiling、compression | package/supply | memory与packaging |
| Latency-bound | cache、prefetch、parallelism | control complexity | CPU/runtime |
| Transaction-bound | layout/coalescing | compiler | software platform |
| Capacity-bound | more memory/sharding | fabric | HBM/CXL/network |
| Launch/queue-bound | graphs/runtime/scheduler | observability | serving software |

## 15. Technical diligence questions

1. Bound结论对应哪个 kernel、phase、shape与 software版本？
2. Operations和每层 bytes如何计算、能否复现？
3. Peak、sustained microbenchmark与 application ceiling分别是多少？
4. Profiler中的 stall、occupancy、cache与 transactions是否支持结论？
5. 哪个 controlled experiment能推翻诊断？
6. Fusion/tiling覆盖多少 production shapes？
7. Optimization是否改变 accuracy、tail或 power boundary？
8. Kernel加速是否落在 end-to-end critical path？
9. 下一代 machine balance变化后哪些 kernel会迁移？
10. 价值应投入 silicon、memory、package还是 software？

## 16. Takeaways

1. Compute-bound和 memory-bound是实现与边界相关的可变诊断。
2. Roofline提供上界，profiler和 controlled experiment负责验证。
3. Memory-bound必须拆成 bandwidth、latency、transaction与 capacity。
4. Utilization不等于 useful work，kernel speedup也不等于 end-to-end speedup。
5. 最有价值的优化是移动 critical-path bottleneck，而不是提高最漂亮的 counter。

## Primary sources

- [Primary Source] [Berkeley Lab Roofline Performance Model](https://amcr.lbl.gov/departments/computer-science-department/ppan/roofline-performance-model/)
- [Primary Source] [NVIDIA CUDA Best Practices Guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html)
- [Primary Source] [AMD HIP Programming Model](https://rocm.docs.amd.com/projects/HIP/en/latest/understand/programming_model.html)
