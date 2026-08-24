# Scale-out Networking

> 从collective traffic与incast出发理解packet fabric，不把Ethernet、RDMA、ECN、PFC当成孤立缩写。

## Cornerstone

1. [Topology-Aware Collectives](topology_aware_collectives.md)
2. [Ethernet vs InfiniBand：Fabric Operating Model](ethernet_vs_infiniband.md)
3. [AI Ethernet 与 RDMA：为什么高带宽网络仍会被 Congestion、Loss 与 Tail Latency 击败](ai_ethernet_rdma.md)
4. 前置：[Scale-up vs Scale-out](../12_scale_up/scale_up_vs_scale_out.md)、[SerDes](../11_serdes_signal_integrity/serdes.md)
5. 后续：Collectives、Leaf-Spine/Clos、Switch ASIC、NIC/DPU、Datacenter Optics。

~~~mermaid
flowchart LR
  G[GPU memory] --> N[NIC / RDMA]
  N --> L[Leaf]
  L --> S[Spine]
  S --> R[Remote NIC/GPU]
  C[Congestion feedback] -.-> N
~~~
