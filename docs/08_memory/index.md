# Memory

> 目标：从 cell、array、hierarchy 与 data placement 理解 memory wall，而不是把 bandwidth 和 capacity 当成两个孤立规格。

Memory subsystem 的任务是让正确的数据在正确时间、以足够低的 energy 到达 compute。第一篇建立从 register 到 storage 的 hierarchy；第二篇进入 DRAM cell、bank、row buffer、commands 与 timing，为后续 HBM 和 CXL 奠定基础。

## Cornerstone sequence

1. [Memory Hierarchy：为什么算力必须被多层数据供给系统包围](memory_hierarchy.md)
2. [DRAM：从一个电容到 AI 系统的容量与带宽墙](dram.md)
3. [Roofline Model：把算力、带宽与 workload 放到同一张图](roofline_model.md)
4. [HBM：为什么 AI 加速器必须把 DRAM 堆到封装旁边](../09_hbm/hbm.md)
5. 下一步：memory controller、virtual memory 与 memory pooling。

~~~mermaid
flowchart LR
    C[Compute] <--> R[Register / SRAM]
    R <--> L[Cache / Scratchpad]
    L <--> D[DRAM]
    D --> H[HBM / DDR / GDDR choices]
    D --> T[Host / Tiered Memory]
    H --> P[Package + Power + Supply]
~~~

## 本模块默认问题

1. 需要保存的 working set 多大、lifetime 多长、由谁共享？
2. 限制是 latency、bandwidth、capacity、transaction efficiency 还是 reliability？
3. 数据在哪一层复用，谁负责 placement、tiling、prefetch 与 eviction？
4. Peak GB/s 中有多少是 sustained、useful、SLO-compliant bandwidth？
5. 增加 cache、channels、data rate 或 stacks 会牺牲什么？
6. Memory 改动如何牵动 controller、PHY、package、power、thermal 与 yield？
7. Bottleneck 解除后是否转移到 software、fabric 或 compute supply？
