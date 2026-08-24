# PCIe / CXL / I/O

> 从 transaction semantics 一直追到 electrical lane，理解“协议支持”为什么不等于 application performance。

## Cornerstone

1. [CXL 与 Tiered Memory：Pool 不等于 Local](cxl_tiered_memory.md)
2. [PCIe vs CXL：同一条 PHY 上，I/O、Cache Coherence 与 Memory Semantics 如何分工](pcie_vs_cxl.md)
3. 后续阅读：[SerDes 与 Signal Integrity](../11_serdes_signal_integrity/serdes.md)、[Memory Hierarchy](../08_memory/memory_hierarchy.md)、Scale-up 与 CXL product cases。

~~~mermaid
flowchart TB
  A[Software / Driver / OS] --> T[Transaction semantics]
  T --> D[Data link / flow control]
  D --> P[PHY / SerDes]
  P --> C[Electrical channel]
  T --> X[PCIe I/O or CXL cache/mem]
~~~

每次看到 GT/s 或 CXL-ready，继续问 negotiated width、payload efficiency、round-trip latency、coherence scope、HDM placement、switch oversubscription 与 OS support。
