# Case：AI Ethernet Fabric 采购——端口速度不是集群吞吐

## 决策情境

一家模型公司准备扩建训练集群。两个方案都宣称“AI-ready Ethernet”：方案甲使用更高端口速率和较浅 oversubscription，价格高、交付较慢；方案乙声称依靠标准交换机与拥塞控制即可获得相近结果。采购问题不是谁的 datasheet 更大，而是谁能在目标 collective、故障与运维条件下交付更多有效训练步。

## 把 workload 翻译成 traffic

先收集模型并行方式、每步计算时间、每轮 collective bytes、消息尺寸分布、GPU 数量与 placement。通信时间可近似为：

\[
T_{\text{comm}}\approx \alpha N_{\text{phases}}+\frac{B_{\text{collective}}}{BW_{\text{effective}}}
\]

[Estimate] \(\alpha\) 吸收软件、NIC、switch hop 与同步延迟；有效带宽必须从实测得到，不能用端口 line rate 代替。

~~~mermaid
flowchart LR
  M[Model parallelism] --> C[Collective graph]
  C --> P[Placement]
  P --> T[Fabric traffic]
  T --> Q[Queue / congestion]
  Q --> S[Step time]
  F[Failure / reroute] --> Q
~~~

## Alternatives

**甲：专门构建的无损或近无损 fabric。** 优点是遥测、collective tuning 和供应商责任边界较完整；缺点是成本、锁定和交付周期。

**乙：开放 Ethernet 组件组合。** 优点是供应链和采购弹性；缺点是交换机、NIC、cabling、firmware 与 congestion policy 的系统集成责任落到买方。

**丙：分阶段混合部署。** 关键训练 pod 使用严格设计，低通信 workload 使用通用网络；可优化资本效率，却增加调度和运维复杂度。

chosen design 应由 loss recovery、ECN/PFC 行为、buffer pressure、routing entropy、telemetry 和故障收敛共同决定。不是所有训练都要求 lossless，也不是打开 PFC 就等于无拥塞。

## 证伪测试

1. 用真实 collective mix，而不是单流 bandwidth benchmark。
2. 同时制造 incast、长短流竞争与链路故障，观察 P99 step time。
3. 检查端口、lane、transceiver、fiber 与 switch radix 是否形成可布线 topology。
4. 比较 steady state 与 link flap、NIC reset、ECMP rebalance 后的恢复。
5. 把 job placement 和 topology awareness 打开与关闭，识别软件依赖。

[Inference] 若供应商性能只在单一 topology、固定 message size 和无故障条件成立，其优势更像调优点而非可扩展架构。

## 经济模型

总成本应包含 switches、NIC、optics、cabling、spares、installation、管理软件和网络工程团队。分母使用可用训练吞吐：

\[
Cost_{\text{step}}=\frac{Annualized\ fabric\ cost}{Completed\ useful\ steps}
\]

新一代端口可能减少设备数，却提高单端口 optics 功耗、散热和替换成本。布线层减少后，failure domain 也可能扩大。便宜的 BOM 若带来更多重试、checkpoint rollback 或人工调参，未必有更低 cost per step。

## Investment conclusion

网络供应商的 moat 不只在 switch silicon；还在端到端验证、拥塞遥测、自动化配置、故障定位与生态兼容。采购合同应绑定目标 workload 的 acceptance test、固件升级回归、长期 optics 供应和故障响应，而不是绑定峰值规格。

## 资料

- [NVIDIA NCCL User Guide](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/) [Vendor Claim]
- [Ultra Ethernet Consortium Specifications](https://ultraethernet.org/specifications/) [Primary Source]
- [Open Compute Project Networking](https://www.opencompute.org/projects/networking) [Primary Source]
