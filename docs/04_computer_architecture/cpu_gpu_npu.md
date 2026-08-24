# CPU vs GPU vs NPU：不是谁更快，而是谁为哪一种不确定性付费

## 1. 先从问题开始

CPU、GPU 与 NPU 不是一条从“通用”到“先进”的排行榜，而是三种资源配置哲学。CPU 为控制流、低延迟、单线程依赖与不可预测性付出大量晶体管；GPU 为大量相似工作与延迟隐藏配置更多并行执行单元；NPU 则把某类张量数据流、片上搬运和数值格式进一步固化，以换取更高的单位面积与单位能量有效工作。

真正的选择题是：工作负载中有多少结构可以在编译时看见？有多少并行性可以稳定提取？数据能否被分块并复用？控制分支是否频繁？模型和算子会不会快速变化？只有回答这些问题，“该用哪种处理器”才有意义。

~~~mermaid
flowchart LR
  W[Workload] --> C{控制流是否不可预测}
  C -->|高| CPU[CPU<br/>低延迟与通用控制]
  C -->|低| P{是否有大规模规则并行}
  P -->|中等或形状多变| GPU[GPU<br/>SIMT 与软件可编程]
  P -->|高且稳定| NPU[NPU<br/>专用张量数据流]
  CPU --> H[异构系统]
  GPU --> H
  NPU --> H
~~~

## 2. 三种架构分别在优化什么

### CPU：缩短一条关键依赖链

现代 CPU 的核心问题是“下一条真正有用的指令什么时候能执行”。乱序执行、分支预测、投机执行、复杂 cache hierarchy、低延迟互连与精细异常语义，都在减少单个 thread 被依赖和不确定 memory access 阻塞的时间。

这种设计非常适合 operating system、database control path、request parsing、serialization、branch-heavy code、稀疏且难预测的数据结构，以及必须快速响应的小任务。代价是每个执行 lane 周围需要大量 control logic；当同一种乘加可以在许多数据上规则重复时，CPU 的通用性开销会显得昂贵。

### GPU：用大量 ready work 隐藏等待

GPU 不要求一条 thread 始终低延迟，而是维持大量 warps/wavefronts。当一个 warp 等 memory 或 dependency 时，scheduler 选择另一个 ready warp。相似 thread 被组织成 SIMT 执行，规则的 memory access 可以合并，shared memory/scratchpad 用于 tile reuse。

[Primary Source] NVIDIA CUDA Programming Guide 把 thread、block、warp、SM 与 memory spaces 作为编程模型，并说明分支分歧、register 与 shared-memory 使用会影响可驻留并行度。GPU 的优势因此不是“有很多 core”这么简单，而是硬件、编译器、kernel library 和数据布局共同制造足够的并行 ready work。

### NPU：把常见张量路径变成数据流机器

NPU 是宽泛类别，不是统一 ISA。常见设计会把矩阵乘加阵列、vector/post-processing 单元、片上 SRAM、DMA、collective 或 host interface 组合成一个由 compiler 调度的数据流。它减少通用 instruction fetch、复杂 control 与随机 cache 行为，让权重和 activation 以更确定的节奏穿过阵列。

[Primary Source] Google 的 TPU 论文展示了一个面向数据中心推理的 domain-specific accelerator：核心思想是用矩阵单元、软件管理 memory 与更确定的执行模型换取性能和能效。重点不是复制某一代 TPU 的规格，而是理解 domain specialization 如何把“不可预测性成本”移出 datapath。

## 3. 同一个矩阵乘法，为什么结果仍不同

矩阵乘法只定义数学，不定义执行。系统还必须决定：

- tile 放在 register、SRAM 还是外部 DRAM；
- 哪一维映射到 lane、warp、core 或 array；
- data layout 是否允许连续传输；
- 边界尺寸是否需要 padding；
- accumulation precision 与 rounding；
- activation、normalization、routing 能否 fusion；
- 多 device 时在哪一层切分与通信；
- 编译时已知 shape 还是运行时动态 shape。

CPU 可用 vector ISA 和 cache blocking；GPU 用 warps、shared memory 与 tensor/matrix instructions；NPU 可能用 systolic 或 spatial dataflow。对大而规则的 GEMM，NPU 或 GPU 往往能提高有效阵列占用；对很小、分支多、启动开销占比高的任务，CPU 可能更快完成。判断依据是 end-to-end latency 与 delivered throughput，不是单个 datapath 的 peak。

## 4. 计算：利用率比峰值更能决定赢家

[Estimate] 假设三种设备的 headline peak 分别为 1、10、20 个相对单位。某个动态 shape workload 在 CPU、GPU、NPU 上的有效利用率分别为 60%、18%、7%，再考虑数据搬运与 runtime 后的可用系数分别为 90%、75%、55%。

有效结果为：

- CPU：<code>1 × 0.60 × 0.90 = 0.54</code>
- GPU：<code>10 × 0.18 × 0.75 = 1.35</code>
- NPU：<code>20 × 0.07 × 0.55 = 0.77</code>

NPU 虽有最高 peak，却被 shape、fallback 与搬运打折；GPU 在这个假设下获胜。若 compiler 把 NPU 利用率提高到 20%、把更多算子融合，结果会反转。这个例子不是产品 benchmark，而是说明 architecture choice 必须经过 performance waterfall。

## 5. 为什么不把所有任务都放到 GPU

第一，控制流与小任务可能无法制造足够并行度。第二，kernel launch、synchronization 与 host-device handoff 会成为固定成本。第三，操作系统、网络 control plane、storage management 和 failure recovery 需要成熟的 privilege、interrupt 与 exception 语义。第四，GPU memory capacity 是昂贵资源，把低价值 state 全部放进去可能挤出模型和 KV cache。

因此现实系统仍用 CPU 做 orchestration、pre/post-processing、metadata、scheduler 与 exception path，再让 GPU 承担密集张量计算。所谓“CPU 不重要”通常只是把 CPU 时间排除在 benchmark boundary 之外。

## 6. 为什么不为每个模型做专用 ASIC

专用化必须偿还 NRE、验证、compiler、量产和机会成本。模型结构、precision、sequence、sparsity 与 operator mix 变化时，固定数据流可能出现低利用率或无法支持的 fallback。产品从 architecture freeze 到大规模部署存在时间差；若 workload 在这段时间改变，理论效率无法转成收入。

更现实的做法是选择可复用的 specialization：可编程 matrix/vector 单元、灵活 memory movement、有限但高价值的 operator set，以及能在 software release 中扩展的 compiler/runtime。NPU 的竞争力常来自“足够专用、又没有专用到过时”。

## 7. 为什么不只看每瓦 TOPS

TOPS/W 只有在相同 precision、quality、sparsity、utilization 与 system boundary 下才可比。设备更节能但需要更多 host、network 或 idle capacity，rack-level energy 可能不降；设备更快但 software porting 需要一年，deployment NPV 可能更差；低精度 peak 更高但 accuracy 不达标，则不是同一工作负载。

更好的指标包括：

- 达到目标质量的 time-to-train；
- 满足 tail-latency SLO 的 requests 或 tokens；
- 每个 rack、每瓦 wall power、每美元的 useful work；
- 支持的 production operator 覆盖率与 fallback 比例；
- compiler 更新速度、debuggability 与迁移成本；
- failure、checkpoint 与 degraded mode 下的交付能力。

## 8. 异构系统才是常态

~~~mermaid
sequenceDiagram
  participant C as CPU
  participant G as GPU/NPU
  participant M as Device Memory
  participant N as NIC/Fabric
  C->>G: dispatch graph / command
  G->>M: load tiles and state
  G->>G: tensor + vector kernels
  G->>N: collective / remote access
  N-->>G: synchronized data
  G-->>C: completion / exception
~~~

CPU、GPU、NPU 之间的边界会产生新瓶颈：数据复制、address translation、coherency、queue depth、launch latency、memory ownership 与 observability。统一虚拟地址可以简化编程，但不消除物理 locality；自动迁移减少显式 copy，却可能在错误时刻制造 page fault 和 fabric traffic。

架构团队需要决定哪些 graph segment 常驻 accelerator、哪些 state 由 host 管理、fallback 在何处发生，以及发生 failure 时谁能重启而不扩大 blast radius。

## 9. Software 是第四种架构

硬件提供可能性，compiler 决定 mapping，library 决定常见路径，runtime 决定排队与并发。一个 peak 较低但拥有成熟 kernel、profiling、distributed runtime 和 framework integration 的平台，可能长期提供更高 delivered performance。

NPU 尤其依赖 graph lowering、shape specialization、layout propagation、fusion、memory planning 与 quantization tooling。若每个新模型都需要 vendor 工程师手工修 kernel，产品本质上仍处于 services-heavy 阶段。软件栈是否让普通客户独立获得性能，是 technical diligence 的核心。

## 10. Second-order effects

1. 更强的矩阵阵列会提高 machine balance，反而让 memory-bound operator 更突出。
2. 更多片上 SRAM 改善 reuse，却占用 die area、增加 leakage，并可能降低阵列数量。
3. 更低 precision 提高吞吐，也增加 calibration、accumulation、outlier 与验证负担。
4. 更确定的数据流可改善 tail，但对动态 routing 和 irregular sparsity 可能浪费。
5. 异构设备越多，scheduler、coherency、telemetry 与 fleet qualification 越复杂。
6. 专用平台获得规模后，compiler 与 model architecture 可能围绕它共同演化，形成生态反馈。

## 11. Engineers actually say

- “This part is latency sensitive.”：问 latency 是单 thread、kernel launch、memory、queue 还是 end-to-end tail。
- “The GPU is underutilized.”：问是没有 ready warps、memory stall、small shapes、divergence 还是 host starvation。
- “The accelerator supports the model.”：支持是能运行、能通过 accuracy、能达到 SLO，还是 production-optimized？
- “We fall back to the CPU.”：问 fallback frequency、copy boundary 与 p99 代价。
- “The compiler handles it.”：要求看编译报告、fusion、spill、layout conversion 与 unsupported ops。
- “Our TOPS/W is better.”：固定 precision、quality、system power 与 workload utilization。

## 12. Engineering → Strategy

| 工程选择 | 直接收益 | 新风险 | 价值可能迁移 |
|---|---|---|---|
| 更多 CPU control | 低延迟、兼容性 | 面积与能效 | CPU IP、memory 与 software |
| GPU SIMT | 通用并行吞吐 | utilization 波动 | kernel library、HBM、fabric |
| NPU dataflow | 单位成本与能效 | workload drift | compiler、custom silicon、云平台 |
| 片上 SRAM 增加 | reuse 与确定性 | die area、yield | SRAM compiler、packaging |
| 更低 precision | 高吞吐、低 bytes | accuracy 风险 | quantization tooling |
| 异构整合 | 各取所长 | orchestration 复杂 | runtime、coherency、interconnect |

战略上不要问“谁会替代谁”，而要问哪类工作从通用 compute 迁到专用 datapath、迁移速度由什么限制、谁控制 software entry point，以及客户是否愿意承担 portability 风险。

## 13. Technical diligence questions

1. 目标 workload 的 operator、shape、precision 与 control-flow 分布是什么？
2. Peak 到 delivered 的每个 loss bucket 多大？
3. Unsupported operator 在哪里执行，数据如何移动？
4. Compiler 能否稳定复现 vendor benchmark，还是依赖手工 kernel？
5. Dynamic shape、sparsity、MoE routing 与长序列如何处理？
6. 片上 memory 的 placement 由硬件、compiler 还是 programmer 管理？
7. 多设备 collective、checkpoint 与 failure recovery 是否 production-ready？
8. 同质量、同 SLO、同 wall-power boundary 的比较结果是什么？
9. 客户迁移、debug、profiling 与版本锁定成本多大？
10. 下一代模型变化时，哪项固定假设最可能失效？

## 14. Takeaways

1. CPU 为不确定性和低延迟付费，GPU 为大量可调度并行付费，NPU 为稳定张量数据流专用化。
2. 数学算子相同，不代表 mapping、memory movement 与 delivered performance 相同。
3. Peak 只有经过 utilization、搬运、runtime 与 SLO waterfall 后才有决策意义。
4. 现实答案通常是异构系统，边界本身会产生新 bottleneck。
5. 长期竞争力来自 hardware、compiler、library、runtime 与 workload 共演化。

## Primary sources

- [Primary Source] [NVIDIA CUDA Programming Guide：Programming Model](https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html)
- [Primary Source] [NVIDIA CUDA Programming Guide：SIMT Kernels](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html)
- [Primary Source] [Google Research：In-Datacenter Performance Analysis of a Tensor Processing Unit](https://research.google/pubs/in-datacenter-performance-analysis-of-a-tensor-processing-unit/)
- [Primary Source] [Google Research：A Learned Performance Model for the TPU](https://research.google/pubs/a-learned-performance-model-for-the-tensor-processing-unit/)
