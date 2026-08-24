# HBM

> HBM 是 DRAM、TSV stacking、wide I/O、memory controller 与 advanced packaging 的共同系统，不是一条孤立规格。

## Cornerstone

1. [HBM：为什么 AI 加速器必须把 DRAM 堆到封装旁边](hbm.md)
2. 前置：[DRAM](../08_memory/dram.md)、[Memory Hierarchy](../08_memory/memory_hierarchy.md)、[Roofline](../08_memory/roofline_model.md)
3. 后续：[Advanced Packaging](../16_advanced_packaging/index.md)、Power/Thermal 与 product case studies。

~~~mermaid
flowchart LR
  W[Memory Wall] --> H[Wide-I/O stacked DRAM]
  H --> P[Interposer / package]
  H --> T[TSV / bonding / test]
  H --> E[Power / thermal]
  P --> S[Supply / yield / cost]
~~~

阅读时始终同时问：raw bandwidth、useful bandwidth、usable capacity、energy/bit、stack/package yield 和 supplier qualification。


## 深化阅读

- [HBM Scaling：Capacity、Bandwidth、Thermal 与 Yield](hbm_scaling_tradeoffs.md)
