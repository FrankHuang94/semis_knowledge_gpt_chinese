# Ethernet vs InfiniBand：AI Scale-out 选择的是一套 Fabric Operating Model

## 1. 为什么不能只比较端口速度

Ethernet 与 InfiniBand 都能承载高性能分布式计算，但它们不是两根“谁更快”的线缆。真正差异分布在 link/transport semantics、routing、congestion control、loss recovery、RDMA、management、telemetry、multi-tenancy 与供应生态。

同一物理速率下，collective completion time 可能因 topology、message size、incast、queueing、packet reordering、NIC behavior 和 software stack 而完全不同。比较必须从目标 workload 与运营边界开始：是单租户训练 pod、共享云、HPC MPI、storage、还是同时承载东西向通用流量？

~~~mermaid
flowchart LR
  A[GPU/CPU Memory] --> H[NIC / HCA]
  H --> L[Leaf Switch]
  L --> S[Spine]
  S --> R[Remote Endpoint]
  CC[Congestion Control] -.feedback.-> H
  M[Fabric Manager / Controller] -.routes.-> L
  T[Telemetry] -.observes.-> CC
~~~

## 2. 共同目标：把 remote data movement 变成可预测服务

两种 fabric 都需要 serializer、PHY、cable/optics、switch ASIC、queues、routing 与 endpoint adapter。它们都必须面对传播、serialization、buffer、contention、failure 与 software overhead。

RDMA 也不是 InfiniBand 的同义词。[Primary Source] IBTA 说明 InfiniBand 原生定义 channel-based switched fabric 与 RDMA semantics；RoCE 则让 RDMA transport 运行在 Ethernet layer 2/3 网络上。于是实际比较经常是“InfiniBand stack”与“经过数据中心增强并运行 RoCE 的 Ethernet stack”，而不是“RDMA 对 Ethernet”。

## 3. Ethernet 的 architecture posture

Ethernet 的战略优势是广泛标准、供应商生态、运营人才、IP routing 与已有 tooling。它可以服务 AI、storage、front-end 和通用 cloud traffic，并与现有 automation 和 security architecture衔接。

但普通 best-effort Ethernet 并不自动满足 synchronized AI traffic。RoCE 环境需要正确的 ECN、congestion-control algorithm、buffer design、load balancing、telemetry 与 loss/reordering behavior。PFC 可以在某些设计中抑制 loss，却可能引入 pause propagation、head-of-line blocking 与 deadlock风险；无损不能被理解为“打开一个开关”。

Ethernet 的可组合性越强，configuration state space 越大。多 vendor interoperability 是潜在价值，也意味着 qualification matrix、firmware差异与责任边界更复杂。

## 4. InfiniBand 的 architecture posture

InfiniBand 从一开始就围绕 switched fabric、queue pairs、reliable transport、RDMA 与 subnet management 组织。统一的 fabric semantics 有助于把 routing、credit、service level 与 endpoint behavior做成相对完整的系统。

[Primary Source] IBTA 把 InfiniBand 描述为 server/storage interconnect architecture，并说明 subnet manager 可以管理多路径与路由。对希望获得紧密集成、低 jitter 与成熟 HPC software 的集群，这种 vertically integrated operating model 很有吸引力。

代价是 ecosystem 与采购控制可能更集中，企业现有 Ethernet 团队的工具和流程不一定直接复用。若 front-end、storage 和 compute fabric 分离，运维需要管理两套网络；若合并，又要验证不同 traffic class 的隔离。

## 5. Packet fabric 中真正决定结果的层

### Endpoint injection

GPU 或 host memory 必须通过 PCIe、scale-up fabric 或 direct memory interface 到达 NIC/HCA。Adapter 的 DMA engine、queue depth、registration cache、packet pacing 与 collective offload 可能先于 switch 限制性能。

### Switch forwarding

Switch radix、buffer、pipeline、routing table、ECMP/adaptive routing 与 telemetry决定 traffic如何穿过 Clos。Headline switching capacity 是所有 port 的理论 aggregate，不代表某个 collective 在拥塞下获得等额 payload。

### Congestion control

Feedback 必须在 queue 失控前影响 sender。太慢会积累 queue 与 tail；太激进会降低 utilization；多个 control loop相互作用可能振荡。算法还必须处理 elephant collective、background mice、incast 与 failure-induced reroute。

### Transport 与 recovery

Loss、reordering、timeout 与 retransmission 粒度决定一次局部错误会浪费多少工作。严格 ordering 简化上层，却可能把单个迟到 packet 变成 head-of-line stall；更灵活的 out-of-order 需要 endpoint reorder state 与更复杂验证。

### Software collective

NCCL、MPI、UCX 或框架选择 ring、tree、hierarchical 与 topology-aware algorithm。网络硬件再快，若 rank mapping、chunk size、overlap 或 synchronization不当，application scaling仍然很差。

## 6. 计算：Raw rate 不是 exposed communication

[Estimate] 一个 ring All-Reduce 的 message 为 8 GiB、ranks 为 8、有效 payload bandwidth 为 200 GiB/s。每个 rank 的理想 traffic 约为：

<code>2 × (8 - 1) / 8 × 8 = 14 GiB</code>

理想传输时间约 <code>14 / 200 = 0.07 秒</code>。若 backward compute 能 overlap 0.05 秒，[Estimate] 暴露在 step critical path 上的 communication约 0.02 秒。

选择 fabric 时要比较的是这个 exposed time 在真实 topology、并发 job 和 tail下的分布。端口 rate 增加一倍，若 effective payload、routing 或 overlap没有同比改善，step time不会一倍缩短。

## 7. 为什么不全部使用 InfiniBand

第一，已有 Ethernet fleet、automation、security 和人才是重大 sunk capability。第二，多 vendor sourcing 与标准 IP network 对许多 cloud operator有战略价值。第三，不是所有 traffic 都需要 RDMA 级 latency；把 control、storage、tenant 与 AI traffic 放入同一专用 fabric可能降低灵活性。第四，采购、升级节奏和供应集中风险需要计入。

当 operator 有能力把 RoCE congestion、routing、telemetry 与 qualification做成产品时，Ethernet 的开放生态可以转化为长期控制力。若缺少这种系统工程能力，“标准”不会自动变成可预测性能。

## 8. 为什么不全部使用 Ethernet

第一，通用 Ethernet stack 的可配置性可能成为运维复杂度。第二，AI collective 的 synchronized incast 和长流对 queue/control loop提出更苛刻要求。第三，多 vendor 的 fault attribution 可能跨 NIC、switch、optics、firmware 与 software。第四，成熟的 InfiniBand ecosystem 可能让特定 HPC/AI deployment更快达到稳定性能。

关键不是 Ethernet 是否“能做到”，而是目标组织能否持续完成 tuning、validation、telemetry 和 incident response，并让这些成本低于专用 fabric 的 premium与集中风险。

## 9. 为什么不把两个 fabric 同时装满

双 fabric 可以隔离 failure domain、分开 compute 与 storage，或支持迁移；但它增加 NIC/port/optics/cable、rack power、布线、inventory、software routing 和 on-call 复杂度。闲置冗余不是免费可靠性，必须证明故障时 application 能切换、性能仍满足 SLO，且 runbook经过演练。

混合架构更常见的合理形式是分层：节点内部 scale-up，训练 pod 内高性能 scale-out，pod 外用通用 Ethernet；或者保留管理网络与数据网络的清晰边界。

## 10. Topology 与 oversubscription

无论协议，Clos/leaf-spine 的 bisection、uplink/downlink、rail mapping 与故障降级决定 collective path。Non-blocking 不是单一布尔值：必须说明对哪组 endpoints、在哪种同时通信 pattern、考虑多少失败和 maintenance。

Rail-optimized design 可以让每个 accelerator port连接到特定 fabric plane，减少随机 ECMP uncertainty；代价是 topology-aware scheduler与故障映射更复杂。Adaptive routing可以绕开拥塞，却需要稳定的 telemetry与避免 packet spraying副作用。

## 11. Multi-tenancy 与 isolation

共享 fabric 的目标不是最高单 job throughput，而是在 noisy neighbor、burst、failure 与 adversarial configuration 下保持可预测性。需要考虑 queue/service class、rate limiting、admission control、routing isolation、encryption、telemetry access 与 control-plane权限。

InfiniBand 与 Ethernet 都可以构建隔离，机制与运营模式不同。Diligence 要看最坏情况下的 measurement，而不是单租户空网 benchmark。

## 12. Product reality：如何读网络发布

看到“更高 bandwidth、ultra-low latency、lossless、adaptive routing、AI-optimized”时，要求把 claim拆为：

- line rate、payload 与 application goodput；
- single hop、end-to-end、median 与 tail；
- zero congestion、designed load 与 oversubscribed load；
- 单 flow、all-to-all 与 collective；
- switch-only、NIC-to-NIC 与 GPU-to-GPU；
- 同 vendor stack 还是 interoperability matrix；
- shipping silicon、production firmware 与 preview feature；
- 正常、link failure、switch failure 与 maintenance状态。

[Primary Source] IEEE 802.3 Working Group维护 Ethernet standards；IBTA维护 InfiniBand architecture与 RoCE相关规范。标准合规证明协议接口，不证明具体 fabric在目标 workload下的 delivered performance。

## 13. Second-order effects

1. 更高速端口减少完成时间，也提高 incast burst slope，对 congestion loop反应速度要求更高。
2. 更大 switch radix减少层数，却提高 package I/O、power、thermal 与 optics密度。
3. 更强 collective offload降低 host工作，却增加 firmware与 vendor dependency。
4. Adaptive routing提高利用率，却让性能复现和故障定位更难。
5. Lossless机制减少 retransmission，却可能扩大 pause与 head-of-line影响。
6. 统一 fabric提高资源利用率，也扩大 shared failure domain。
7. 更开放的供应链降低集中风险，却增加 qualification与 integration成本。

## 14. Engineers actually say

- “The fabric is non-blocking.”：问 endpoint集合、traffic matrix、失败假设与 oversubscription。
- “We run lossless Ethernet.”：问 PFC/ECN/CC组合、pause telemetry与 deadlock prevention。
- “Latency is sub-microsecond.”：问测量 boundary、message size、percentile与 queue load。
- “RDMA bypasses the CPU.”：问 setup/control path、memory registration与 exception处理。
- “Adaptive routing fixes hotspots.”：问 feedback delay、reordering与 oscillation。
- “InfiniBand is plug-and-play.”：问 subnet manager、firmware matrix与 operational ownership。
- “Ethernet gives multi-vendor choice.”：问哪些组合真正被共同验证。

## 15. Engineering → Strategy

| 选择 | 工程收益 | 运营代价 | 战略含义 |
|---|---|---|---|
| Ethernet/RoCE | 生态、IP整合、供应选择 | tuning与 qualification | operator software能力成为 moat |
| InfiniBand | 紧密 RDMA fabric | 生态集中、双网运维 | integrated vendor捕获更多价值 |
| 单一 fabric | 资源共享、简化布线 | failure domain扩大 | platform control价值上升 |
| 分离 fabric | 隔离与可预测 | 重复设备与流程 | 专用网络供应机会 |
| Adaptive routing | 更高利用率 | telemetry/control复杂 | switch+NIC co-design |
| Collective offload | 降低 exposed time | firmware dependency | endpoint IP价值上升 |

## 16. Technical diligence questions

1. 目标 collective、message distribution、job size与 topology是什么？
2. GPU-to-GPU goodput和 p99 completion time如何，而不只是 port rate？
3. ECN/PFC/credit/CC参数如何设置，谁负责 tuning？
4. Oversubscription与 rail mapping在 failure后如何变化？
5. NIC、switch、optics、firmware与 collective library的 qualification matrix？
6. 多租户背景流下 scaling efficiency与 tail如何？
7. Packet loss、reordering、link flap与 switch reboot如何恢复？
8. Telemetry能否定位到 queue、path、flow与 rank？
9. 升级 firmware是否需要停集群，rollback如何？
10. 三年 TCO是否包含 optics、cable、spares、人才与 incident cost？

## 17. Takeaways

1. Ethernet与 InfiniBand比较的是完整 fabric operating model，不只是端口速度。
2. RDMA可以运行在 InfiniBand或 Ethernet/RoCE上。
3. Endpoint、switch、congestion、transport、collective software任何一层都能成为瓶颈。
4. “开放”与“集成”都同时带来收益和成本。
5. 决策指标是目标负载下可预测、可运维、可降级的 useful communication。

## Primary sources

- [Primary Source] [IEEE 802.3 Ethernet Working Group](https://www.ieee802.org/3/index.html)
- [Primary Source] [InfiniBand Trade Association：About InfiniBand](https://infinibandta.org/about-infiniband/)
- [Primary Source] [IBTA：InfiniBand Architecture Specification FAQ 与 RoCE说明](https://infinibandta.org/ibta-specification/)
- [Primary Source] [NVIDIA RDMA Aware Networks Programming User Manual](https://docs.nvidia.com/rdma-aware-networks-programming-user-manual-1-7.pdf)


## 基础概念桥接

先区分 packet、frame、flow、queue、buffer、routing、congestion、loss 与 collective。线速不是应用吞吐，平均利用率也看不到 microburst。消息尺寸、incast、ECN、PFC、retransmission、topology 和 job placement 必须联合测试。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。
