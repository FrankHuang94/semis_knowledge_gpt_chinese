# SerDes & Signal Integrity

> 为什么现代 chip 无法只靠增加 parallel wires？本模块从 pin、skew 与 channel loss出发，而不是从缩写定义出发。

## Cornerstone

1. [SerDes 与 Signal Integrity：为什么更高速率会换来更小 Margin、更高 Power 与更短 Reach](serdes.md)
2. 前置：[PCIe vs CXL](../10_pcie_cxl_io/pcie_vs_cxl.md)
3. 后续：Scale-up、Ethernet switch、Datacenter Optics、LPO/CPO 与 Chiplet PHY。

~~~mermaid
flowchart LR
  TX[Serializer + FFE] --> CH[Package/PCB/Cable Loss]
  CH --> RX[CTLE + CDR + DFE]
  RX --> F[FEC]
  F --> B[Recovered bits]
~~~

核心纪律：永远同时报告 bit rate、baud、modulation、loss、BER、FEC、energy/bit、reach、PVT margin 与test boundary。
