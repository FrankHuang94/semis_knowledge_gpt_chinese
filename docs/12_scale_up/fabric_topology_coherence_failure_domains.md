# Scale-up Fabric：Topology、Coherence 与 Failure Domain 的共同设计

Scale-up 的目标不是简单“把更多 accelerator 连在一起”，而是让一组设备在低延迟、高带宽和可预测语义下共同处理一份工作。连接数量增长后，物理 wiring、switch radix、routing、coherence scope、collective pattern 与故障恢复必须一起设计。

## Topology 从 traffic 开始

~~~mermaid
flowchart LR
  W[Workload graph] --> C[Communication matrix]
  C --> T[Topology]
  T --> R[Routing]
  R --> Q[Queue / contention]
  Q --> L[Collective latency]
  F[Link or device failure] --> R
  S[Coherence semantics] --> C
~~~

全连接提供较短路径，却让每个设备的端口和 package edge 随规模增长；ring 简单且链路利用可预测，但 collective latency 随参与者增加；switch-based fabric 提供更灵活路径，却引入 radix、buffer、arbiter 和故障域；分层 topology 限制局部通信成本，但 placement 错误会迫使流量跨层。

## Coherence 不是免费的便利

一致性可让多个设备共享地址空间和缓存语义，降低编程负担；代价是目录、snoop、ordering、invalidations 与状态存储。scope 越大，控制流量和验证空间越大。许多 accelerator workload 更适合显式消息和 collective，因为数据所有权在 phase 边界清楚；细粒度共享则可能从 coherence 获益。

为什么不让整个 rack 完全 coherent？因为故障、延迟和状态空间会跨越太大边界；一个慢节点或链路可能阻塞更广范围。chosen design 常把强语义限制在较小 scale-up domain，再通过显式网络连接 scale-out domain。

## Failure domain

峰值带宽设计必须与 degraded mode 一起评估。链路失败后能否 reroute；路径变长是否破坏 collective balance；设备退出是否需要重启整个 domain；firmware update 能否滚动进行；错误是被隔离、重试，还是扩散为 hang。冗余链路提高可用性，却增加成本和静态功耗；快速 failover 若缺少拥塞重新平衡，也可能制造新的 incast。

可用吞吐可近似写成：

\[
Throughput_{\text{useful}}=Throughput_{\text{healthy}}\times Availability\times Efficiency_{\text{degraded}}
\]

[Estimate] 仅比较 healthy-state bandwidth 会高估大系统价值。规模增加后，单元故障率不变也会让“总有一个故障”的概率上升。

## Placement 与软件

runtime 必须知道 topology，才能把 tensor parallel、pipeline stage 或 expert 放到合适邻域。拓扑隐藏得越彻底，编程简单性越高，但调度器也越难避免热点。硬件自动路由、compiler placement 与 collective library 应共享同一 cost model；版本不一致会让物理优势失效。

## Diligence 问题

- 宣称的 scale-up size 是可寻址、可互联，还是在目标 workload 下有效？
- 对称带宽是否因 routing、protocol overhead 或热点而下降？
- coherence 覆盖哪些 memory、atomic 与 ordering 语义？
- 单链路、单 switch、单设备和 firmware failure 如何隔离？
- topology-aware placement 失败时，性能和可用性下降多少？
- cable、connector、retimer、optics 与 service workflow 是否进入系统 BOM？

## 资料

- [Compute Express Link Specifications](https://computeexpresslink.org/cxl-specification/) [Primary Source]
- [NVIDIA NCCL User Guide](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/) [Vendor Claim]
- [Ultra Ethernet Consortium Specifications](https://ultraethernet.org/specifications/) [Primary Source]


## 基础概念桥接

先区分 scale-up domain、scale-out network、topology、bisection、coherence scope 和 collective pattern。可连接数量不等于有效规模；routing、placement、failure domain、cabling 和 degraded efficiency 决定实际可用性。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。
