# CPU Host Orchestration：Accelerator 为什么仍会等主机

加速器承担规则张量计算后，CPU 并没有消失。它负责请求接入、数据解码、内存管理、kernel launch、collective orchestration、存储与网络控制、错误处理和运行时调度。若这些工作不能及时供给 accelerator，昂贵计算单元会以“GPU utilization 不高”的形式等待。

## 控制路径与数据路径

~~~mermaid
flowchart LR
  R[Request / dataset] --> C[CPU preprocess]
  C --> H[Host memory]
  H --> D[DMA / I/O]
  D --> A[Accelerator]
  C --> L[Runtime launch]
  L --> A
  A --> N[NIC / storage]
  E[Errors / interrupts] --> C
~~~

瓶颈可能来自单线程 Python、解码、page fault、NUMA placement、small launch overhead、I/O interrupt、host-device copy 或锁竞争。平均 CPU utilization 很低也不能排除问题：一个关键线程、一个 memory controller 或一个 NUMA link 饱和，就可能限制整个 pipeline。

## Alternatives

**把预处理放 CPU**兼容性好、易调试，但可能需要大量 cores 和 DRAM bandwidth；**放 GPU**减少 copy，却与模型争夺 HBM 和 compute；**专用 DPU/accelerator**可隔离基础设施任务，却增加数据路径和软件分割；**离线预处理**降低在线负担，却牺牲数据新鲜度与灵活性。

chosen design 应按算子特征、数据位置、batch 和 SLO 划分，而不是按“CPU 慢、GPU 快”的标签。小而分支密集的任务可能更适合 CPU，大批规则变换更适合 accelerator。

## Feeding pipeline

多级 buffer 可以重叠读取、解码、copy 与计算，但 buffer 过深会增加内存、陈旧数据和 tail；异步 launch 可隐藏主机延迟，却使错误定位更难；pinned memory 提高 DMA 可预测性，却减少 OS 可回收内存。NUMA 错误会让数据绕行 socket interconnect，尤其在多 NIC、多 GPU 主机中形成隐蔽瓶颈。

[Estimate] 可用流水线吞吐由最慢阶段决定，而端到端 latency 是各阶段等待与服务时间之和。提高 accelerator kernel 吞吐后，CPU preprocess 或 storage 立刻可能成为新墙。

## Diligence

- profiler 是否同时覆盖 CPU threads、runtime、DMA 与 accelerator？
- 数据从 storage 到 device 经过几次 copy？
- NUMA、NIC、GPU affinity 是否自动且可观察？
- dynamic batching 和 backpressure 如何工作？
- CPU 或 driver failure 是否会重启全部 accelerators？
- 性能数字是否包含 preprocessing、warm-up 与 postprocessing？

## 资料

- [Linux kernel NUMA memory policy](https://docs.kernel.org/admin-guide/mm/numa_memory_policy.html) [Primary Source]
- [PyTorch DataLoader documentation](https://pytorch.org/docs/stable/data.html) [Primary Source]
- [NVIDIA CUDA Best Practices Guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/) [Vendor Claim]


## 基础概念桥接

先区分 core、thread、instruction、cycle、IPC、frequency、cache miss 和 branch misprediction。CPU 擅长低延迟控制和复杂分支，不等于所有阶段都应留在 CPU。主机 orchestration、NUMA、I/O 与 accelerator feeding 也属于端到端关键路径。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。
