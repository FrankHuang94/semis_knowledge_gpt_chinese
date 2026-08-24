# Queue、Buffer 与 Telemetry：网络拥塞必须在哪里被看见

AI fabric 的拥塞不是“带宽不够”四个字。多个 sender 在相近时间向同一 receiver 或端口发流，会让 arrival rate 暂时超过 service rate，queue 增长、延迟扩大，最终丢包或触发 flow control。buffer 只能吸收时间差，不能创造长期容量。

## Queue 的基本账本

\[
Q(t+\Delta t)=\max(0,Q(t)+A(t)-S(t))
\]

[Estimate] \(A\) 是到达 bytes，\(S\) 是服务 bytes。只要长期到达率超过服务率，任何有限 buffer 都会耗尽；若平均率较低但 burst 相关，buffer 和反馈时延决定是否出现 tail。

~~~mermaid
flowchart LR
  G[GPU senders] --> N[NIC queues]
  N --> I[Ingress buffer]
  I --> F[Switch fabric]
  F --> E[Egress queue]
  E --> R[Receiver]
  E -.ECN / telemetry.-> N
  X[Pause / loss] -.-> N
~~~

## 为什么不无限加 buffer

更大 buffer 可吸收 burst，却增加芯片面积、功耗和 worst-case latency；长 queue 还会形成 bufferbloat，使 congestion signal 太晚。浅 buffer 降低成本和延迟，却要求更快的 end-host pacing 与反馈。共享 buffer 提高统计利用率，但一个热点可能侵占其他端口；静态切分隔离更强，却浪费闲置容量。

PFC 可暂停某个 priority，避免丢包，却可能传播 pause、产生 head-of-line blocking，甚至形成 deadlock 风险；ECN 在丢包前标记拥塞，让 sender 降速，但反馈经过网络和软件后才生效。选择不是 PFC 或 ECN 二选一，而是 loss recovery、pacing、queue policy、routing 与 telemetry 的组合。

## Telemetry 应回答什么

端口平均利用率无法解释微突发。需要观察 queue occupancy distribution、ECN marks、pause duration、drops、retransmission、flow completion、path changes 与 timestamp correlation。NIC、switch 和 application clocks 若无法对齐，团队只会看到“训练变慢”，无法把 step-time spike 关联到具体 queue。

chosen design 应定义从 application collective 到 NIC queue、switch port 和 receiver 的统一 trace identity。高频 telemetry 本身也有成本：采样、导出和存储会占控制资源，因此可采用低成本常驻 counters，加触发式 packet/queue snapshot。

## 二阶效应

通过 pacing 消除 incast 后，发送端可能无法填满链路；改变 routing 分散热点后，packet reordering 与 collective skew 上升；提高 buffer 后，丢包减少但 P99 更差；关闭 PFC 后，retransmission 和 CPU/NIC recovery 负载增加。每次优化都要回到 useful step time，而不是局部网络指标。

## Procurement tests

1. 构造同步 incast、背景流与不同 message size；
2. 在满载时注入 link flap 和 receiver slowdown；
3. 比较平均吞吐、P99 queue、collective completion 与恢复时间；
4. 验证 telemetry 是否定位到端口、queue、flow 和 job；
5. 检查 firmware 更新后 congestion profile 是否回归；
6. 确认运维人员能从告警走到可执行 remediation。

## 资料

- [IETF Explicit Congestion Notification](https://datatracker.ietf.org/doc/html/rfc3168) [Primary Source]
- [Ultra Ethernet Consortium Specifications](https://ultraethernet.org/specifications/) [Primary Source]
- [Open Compute Project Networking](https://www.opencompute.org/projects/networking) [Primary Source]
