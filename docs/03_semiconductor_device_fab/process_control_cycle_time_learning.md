# Process Control、Cycle Time 与 Learning Rate：Fab 为什么不能靠加班爬坡

半导体制造把数百至上千个相互依赖步骤串成长期流程。产能、良率和 cycle time 不是独立 KPI：增加 wafer starts 会提高设备负载和 WIP，排队变长使反馈更晚，良率学习速度可能反而下降。真正目标是稳定增加单位时间的 good die，而不是让每台设备都忙碌。

## 制造反馈环

~~~mermaid
flowchart LR
  S[Wafer starts] --> W[WIP]
  W --> T[Process steps]
  T --> M[Metrology / inspection]
  M --> A[Analysis]
  A --> C[Recipe correction]
  C --> T
  T --> Y[Yield]
  Y --> G[Good die]
  Q[Queue time] -.-> T
~~~

Little's Law 提供第一阶关系：

\[
WIP=Throughput\times Cycle\ Time
\]

[Estimate] 若 throughput 没有同步提高，增加 WIP 只会延长 cycle time。更长 cycle time 又让一次工艺改动更晚得到终测反馈，减慢 learning loop。

## Bottleneck 与 variability

平均设备利用率接近满载时，小幅停机、rework 或 recipe change 会造成非线性排队。constraint tool 可能随 product mix 改变：某产品需要更多 lithography passes，另一产品受 etch、implant、metrology 或 test 限制。因此 fab-wide average capacity 无法代表目标产品 capacity。

批处理设备提高单位运行效率，却要等待 lot 聚合；快速放行减少等待，却可能降低设备利用。更多 inspection 提高缺陷可见性，却占 metrology capacity；减少 sampling 加快流动，却可能扩大 excursion。chosen design 是风险分层 sampling、关键层高覆盖与异常触发加测。

## Learning rate

良率提升来自 defect localization、root cause、process window 扩大和 design-manufacturing feedback。只看累积 wafer 数会混淆产品复杂度、设备代际与团队经验。更好的问题是：每轮假设需要多久获得有判别力的数据；改善能否跨 lot、tool 和时间重复；是否以牺牲 performance guardband 换取 yield。

为什么不直接复制成熟节点 recipe？新材料、pitch、device structure 和 design rules 改变相互作用，旧经验只能提供起点。为什么不等工艺完全稳定再扩产？客户窗口和学习所需样本不允许无限等待。合理 ramp 使用受控 starts 和明确 gate，在学习速度与 scrap exposure 之间平衡。

## 二阶效应与商业判断

缩短 cycle time 会降低 working capital 并加快问题闭环，但若靠跳过维护或 measurement 达成，会增加未来 excursion；增加 redundant tool 提高 resilience，却需要匹配 qualification，备用设备未经常运行也未必是真冗余。良率上升后，封装、测试或客户 qualification 可能成为下一个约束。

diligence 应要求目标产品的 WIP age、cycle-time distribution、constraint tool uptime、hold/rework、defect pareto、按 lot yield 和 recipe change history。产能声明必须区分 installed、qualified、available、allocated 与 good-output capacity。

## 资料

- [TSMC Annual Reports](https://investor.tsmc.com/english/annual-reports) [Primary Source]
- [SEMI Standards](https://www.semi.org/en/standards) [Primary Source]
- [IRDS Reports](https://irds.ieee.org/editions) [Independent]
