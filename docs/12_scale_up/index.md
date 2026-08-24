# Scale-up

> Scale-up不是一个机箱标签，而是为紧耦合accelerator state与collectives设计的latency、bandwidth、semantics与fault domain。

## Cornerstone

1. [Scale-up vs Scale-out：为什么 AI 集群需要两张不同性格的网络](scale_up_vs_scale_out.md)
2. 前置：[SerDes](../11_serdes_signal_integrity/serdes.md)、[PCIe/CXL](../10_pcie_cxl_io/pcie_vs_cxl.md)
3. 后续：[AI Ethernet / RDMA](../13_scale_out_networking/ai_ethernet_rdma.md)、Collectives、Switch/NIC/DPU。

~~~mermaid
flowchart LR
  P[Parallelism] --> C[Collective]
  C --> T[Traffic matrix]
  T --> O[Topology]
  O --> B[Bisection / tail / fault]
~~~


## 深化阅读

- [Scale-up Fabric：Topology、Coherence 与 Failure Domain](fabric_topology_coherence_failure_domains.md)
