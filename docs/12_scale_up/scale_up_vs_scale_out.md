---
id: scale_up_vs_scale_out
title: Scale-up vs Scale-out：为什么 AI 集群需要两张不同性格的网络
concepts: [scale_up, scale_out, topology, collective_communication, fault_domain]
prerequisites: [gpu, pcie, serdes, training, inference]
level: [2, 3, 4]
status: draft
last_verified: 2026-08-24
source_date: 2026-08-24
---

# Scale-up vs Scale-out：为什么 AI 集群需要两张不同性格的网络

> 第一次阅读：Sections 1–8  
> 第二次阅读：Sections 9–18  
> 深入阅读：Sections 19–26

## 阅读前后

读前需理解 GPU、[PCIe/CXL](../10_pcie_cxl_io/pcie_vs_cxl.md)、[SerDes](../11_serdes_signal_integrity/serdes.md)与training/inference；读后能从parallelism、collective、latency、bandwidth、topology、reliability与software解释两个domain为何共存。

## 1. 先告诉我为什么需要它

模型超过一颗accelerator的compute或memory后，state与operations必须分布。若每个layer的tensor shards要频繁交换，communication处于critical path，需要像“扩大一台机器”那样低latency、高bandwidth、强ordering与高有效利用率，这形成Scale-up domain。

当系统扩大到更多hosts/racks，物理distance、ports、cabling、failure与operational scale迫使网络采用routing、packet switching、statistical multiplexing与分层topology，这形成Scale-out。二者不是“机内/机外”标签，而是不同coupling强度与failure assumptions。

## 2. 一句话直觉

**Scale-up让多个accelerators尽量像一台更大的共享计算机；Scale-out让很多独立failure domains通过可路由网络合作。**

## 3. 系统位置

~~~mermaid
flowchart TB
  subgraph SU[Scale-up pod/domain]
    G1[GPU] <--> US[Scale-up switch/fabric]
    G2[GPU] <--> US
    G3[GPU] <--> US
    G4[GPU] <--> US
  end
  G1 --> N1[NIC]
  G2 --> N2[NIC]
  N1 --> LEAF[Leaf switch]
  N2 --> LEAF
  LEAF <--> SPINE[Spine]
  SPINE <--> R[Other racks / pods]
~~~

Boundary随产品演进，可覆盖board、tray、rack甚至pod；定义必须由semantics、topology、latency与software domain确认。

## 4. 前置知识

DP/TP/PP/EP；Reduce、All-Reduce、All-Gather、Reduce-Scatter、All-to-All；hop、diameter、bisection bandwidth、oversubscription、failure domain。

## 5. 第一性原理：通信强度决定网络

若一次phase计算时间 \(T_c\)，通信时间粗略：

\[
T_{comm}\approx \alpha N_{steps}+\frac{V}{BW_{\text{effective}}}
\]

\(\alpha\)是每step/hop的latency，\(V\)是bytes。小message/严格依赖更怕latency；大collective更怕effective bandwidth与contention。Scale-up降低\(\alpha\)并提高紧耦合BW；Scale-out优化规模、routing与容错。

## 6. Follow the Data：tensor parallel layer

~~~mermaid
sequenceDiagram
  participant A as GPU A
  participant F as Scale-up Fabric
  participant B as GPU B
  A->>A: local GEMM shard
  B->>B: local GEMM shard
  A->>F: partial tensor
  B->>F: partial tensor
  F-->>A: collective result
  F-->>B: collective result
  A->>A: next layer
  B->>B: next layer
~~~

若collective未完成，下一层可能无法开始。因此tail、straggler与topology比average GB/s重要。

## 7. Architecture comparison

| 维度 | Scale-up | Scale-out |
|---|---|---|
| 目标 | 扩大单一compute/memory domain | 连接hosts/racks/pods |
| Semantics | load/store/atomics或collective-friendly | packet/RDMA/message |
| Coupling | 强 | 相对弱 |
| Latency | 极敏感 | 可容忍更多stack/hops |
| Topology | all-to-all、switched fabric、mesh | Clos/leaf-spine、多级 |
| Routing | 简化/受控 | ECMP/adaptive |
| Failure | domain内影响较大 | route around/fault isolation |
| Scale | ports/power/cable限制 | 更大节点数 |
| Software | topology-aware collectives | distributed runtime/network |

## 8. 关键 parameters

Per-accelerator injection BW、bisection BW、diameter/hops、switch radix、collective latency、effective BW、oversubscription、routing entropy、tail latency、fault recovery、energy/bit、cables/optics与software topology awareness。

## 9. Worked example：All-Reduce traffic

Ring All-Reduce由Reduce-Scatter + All-Gather组成。每rank payload \(S\)、\(N\) ranks时，理想每rank发送量：

\[
V_{\text{ring}}\approx2\frac{N-1}{N}S
\]

[Estimate] \(N=8,S=1\) GB时每rank约1.75 GB。若effective link BW 400 GB/s，serialization lower bound约4.4 ms，未计step latency、protocol、contention与imbalance。增加GPU不让每rank bytes消失，只让计算与communication比例改变。

## 10. Bottleneck

Scale-up受injection、switch radix/bisection、collective schedule、hot links与fabric reliability限制；scale-out受NIC、leaf uplink oversubscription、ECMP collision、congestion、packet loss、optical reach与job placement限制。两张网络间的handoff也可能是瓶颈。

## 11. Design Space

| 方案 | 优点 | 代价 |
|---|---|---|
| Direct all-to-all | 低hop/高BW | ports/cables O(N²) |
| Mesh/torus | 少ports/locality | diameter/routing |
| Switched scale-up | radix/灵活性 | switch power/cost |
| Clos scale-out | scalable path diversity | 多级cabling/oversubscription |
| Hierarchical collectives | 匹配两domain | software复杂 |
| In-network reduction | 减traffic | switch state/precision/lock-in |

## 12. 为什么最终两层共存

一个fabric同时追求极低latency、memory-like semantics、上千节点、long reach、开放routing、强fault isolation与低成本会过度复杂。分层让hot synchronous traffic留在scale-up，跨failure-domain traffic走scale-out；runtime用hierarchical collectives连接两者。

## 13. 为什么不……？

- 不用一个巨型switch：radix、package SerDes、power、yield、cabling与single failure domain不可无限扩。
- 不全部做all-to-all direct：ports/cables按N²增长。
- 不全部用Ethernet代替scale-up：通用packet stack与拥塞域可能不满足fine-grained critical path。
- 不全部用proprietary scale-up扩全datacenter：reach、routing、operations、vendor lock-in与cost。
- 不总走最短路径：多个flows会hash到同一links，adaptive/non-minimal可绕拥塞。

## 14. Trade-off

~~~mermaid
flowchart LR
  D[Larger scale-up domain] --> H[Fewer software boundaries]
  H --> F[Larger fault domain]
  F --> P[More radix/power/cabling]
  P --> O[Operational complexity]
~~~

## 15. Second-order effects

更大scale-up提高model fit与collective效率，却提高switch/PHY/package价值与vendor lock-in；scale-out更快后瓶颈转到host/NIC injection与collective software；optical content随reach/radix上升。

## 16. Workload mapping

TP/EP频繁通信偏scale-up；DP gradient可跨scale-out但需要大带宽；PP看stage transfer与bubble；MoE all-to-all对tail/congestion敏感；inference replica traffic适合scale-out，model-sharded decode更依赖scale-up。

## 17. Real architecture directions

[Primary Source] UALink Consortium把scale-up定义为accelerator/switch低latency、高bandwidth domain，并公开load/store/atomic与pod规模目标。具体产品可用性必须与spec status分开。  
Ethernet/InfiniBand提供scale-out routing/RDMA生态；NVIDIA NVLink等专有fabric展示vertical integration路径。规格不能替代end-to-end collective measurement。

## 18. Evolution

Direct links → small switched node → rack/pod scale-up → hierarchical collectives → larger radix/reach → power/optics/fault wall → open standards与in-network compute竞争。

## 19–20. Engineer language

“Bisection-limited”“one-hop domain”“oversubscribed uplink”“topology-aware placement”“collective tail dominates”“failure takes out the pod”分别指cut capacity、diameter、uplink ratio、scheduler匹配、最慢flow决定与fault domain过大。

## 21. 追问

Parallelism/collective？message分布？injection/effective BW？diameter？bisection？oversubscription？routing/adaptive？tail？failure recovery？NIC/fabric handoff？energy/bit？cables/optics？collective library？目标规模下实测？

## 22. Misconceptions

Scale-up不等于“机内”；scale-out不等于“慢”；更多links不自动提高bisection；non-blocking不能脱离traffic matrix；拓扑图相同不代表semantics/latency相同。

## 23. Engineering → Strategy

更大scale-up提高platform control与switching cost；开放标准扩大multi-vendor但需interop成熟；高radix推动SerDes/optics/package；hierarchical software成为silicon差异能否兑现的关键。

## 24. Technical Diligence

验证silicon、switch radix、PHY/reach、effective collective BW、tail、failure、management、cabling、power、software与客户部署。Moat可能在fabric protocol、switch silicon、topology algorithms、collective library、telemetry与installed base组合。

## 25. 五个 takeaway

1. Scale-up/scale-out由coupling与semantics定义。
2. Parallelism决定collective，collective决定traffic。
3. Bisection、tail与topology比aggregate port sum更重要。
4. 扩domain会扩大power/cabling/fault。
5. 最佳系统以hierarchical collectives连接两张网络。

## 26. 开放问题

Scale-up domain应扩到多大？In-network compute如何保持numerical/programmability？开放scale-up何时达到production interop？

## Sources

- [Primary Source] [UALink Consortium — Specifications](https://ualinkconsortium.org/specification/)
- [Primary Source] [UALink 1.0 Specification Overview](https://ualinkconsortium.org/wp-content/uploads/2025/04/UALink-1.0-Specification-Overview_FINAL-1.pdf)
- [Primary Source] [UALink About / Scale-up Semantics](https://ualinkconsortium.org/about-ualink/)
