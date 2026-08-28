# Commissioning 与 Acceptance Testing：安装完成为什么还不能交付算力

AI rack 从工厂出货到可运行，需要经历 site readiness、机械安装、供电、液冷、网络、firmware、burn-in、性能基线和故障演练。每个子系统单独“通过”仍可能在联合负载下失败。commissioning 的任务是证明整条系统在目标 envelope 和 degraded mode 中可重复运行。

## 验收层级

~~~mermaid
flowchart TB
  F[Factory acceptance] --> S[Site readiness]
  S --> I[Installation]
  I --> C[Component checks]
  C --> X[Integrated systems test]
  X --> W[Workload soak]
  W --> H[Handover baseline]
~~~

Factory test 证明设备离厂时工作；site test 检查电力、水、网络和结构边界；integrated systems test 验证 UPS、pump、valve、switch、control 与自动降载的联动；workload soak 才能暴露同步功率、热不均、collective 和软件稳定性。

## 为什么不只跑 benchmark

短 benchmark 可验证峰值，却覆盖不了热稳态、memory error accumulation、link flap、leak alarm、冗余切换和维护操作。只做恒定假负载易测试配电，却不能复制 accelerator 的瞬态和通信相关性。chosen design 应组合 synthetic stress、真实 workload replay、故障注入和长时间 soak。

验收脚本必须定义前置状态、通过阈值、测量点、持续时间、失败处理和复测条件。若阈值在现场临时协商，项目会把工程缺口变成商业争议。

## Boundary 与 ownership

facility team、general contractor、OEM、network vendor、cooling vendor 和 software operator 常使用不同工具。应建立共同 event timeline，并为每项告警定义 owner 与 escalation。一个 rack 性能低可能源于供液流量、power cap、光链路 error、firmware 或调度；没有跨层 telemetry 就只能更换部件猜测。

[Estimate] 可交付容量应以通过 acceptance 的 racks 乘以 availability-adjusted throughput 计算，而不是以已运到现场的 nameplate 数量计算。

## Handover

交付物应包括 as-built 图、firmware/configuration manifest、序列号与拓扑、thermal/power/network baseline、阈值、spares、维护步骤、已知问题和复测脚本。任何后续 upgrade 都要能与该基线比较。

## Diligence

- site acceptance 与 product qualification 的边界是否清楚？
- N+1 切换时是否在真实 workload 下保持 SLO？
- 哪些 failure injection 已执行，哪些只在文档声明？
- 基线能否追到单 rack、单链路和单 coolant branch？
- 失败 rack 如何隔离而不阻塞整批交付？
- 运营团队是否实际演练换件、排液、回滚和恢复？

## 资料

- [Open Compute Project Rack and Power](https://www.opencompute.org/projects/rack-and-power) [Primary Source]
- [OCP Advanced Cooling Solutions](https://www.opencompute.org/projects/advanced-cooling-solutions) [Primary Source]
- [AMD Instinct System Acceptance](https://instinct.docs.amd.com/projects/system-acceptance/en/latest/) [Vendor Claim]


## 基础概念桥接

先把 rack 当成计算机：compute、memory、network、power、cooling、firmware、controls 与 operations 共同决定 useful work。nameplate 数量不等于 commissioned capacity；安装、验收、故障恢复、spares 与维护窗口必须进入 TCO。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。
