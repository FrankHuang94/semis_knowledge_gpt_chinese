# Case：Advanced Packaging Supplier Diligence——有产能不等于有良率

## 决策情境

目标公司声称拥有先进封装扩产能力，可承接大尺寸逻辑 die、多颗 HBM 与复杂 substrate。投资人最容易把“设备已安装”“洁净室面积”或“设计产能”当成可销售产出。真正问题是：在目标 package geometry、材料组合与质量门槛下，每月能交付多少 qualified good packages。

## 从 nominal capacity 到 good output

\[
G=W\times D\times Y_{\text{die}}\times Y_{\text{assembly}}\times Y_{\text{test}}\times U
\]

[Estimate] \(W\) 是投入量，\(D\) 是每单位投入对应的候选封装数，\(Y\) 分别代表已知良品、组装和终测良率，\(U\) 吸收设备利用、产品切换与合格率。任何一项都不能用企业平均值代替目标产品数据。

~~~mermaid
flowchart LR
  K[Known good die] --> A[Attach / bonding]
  H[HBM] --> A
  S[Substrate / interposer] --> A
  A --> U[Underfill / molding]
  U --> T[Test]
  T --> Q[Qualification]
  Q --> G[Good shipments]
  R[Rework / scrap] -.-> A
~~~

## 尽调分层

**技术层**：检查 die size、bump pitch、warpage、alignment、thermal budget、interconnect resistance 与 repair strategy。实验室成功必须能映射到 process window。

**制造层**：逐站查看 tool-of-record、cycle time、WIP、queue、changeover、sampling plan、SPC 和 excursion history。瓶颈设备不是最贵设备，而是约束 good output 的工序。

**供应层**：substrate、HBM、underfill、temporary carrier 与 test socket 都可能限制爬坡。dual source 只有在第二来源完成目标产品 qualification 后才算有效。

**质量层**：查看 reliability vehicle 与真实产品的相似度，确认 thermal cycling、mechanical stress、humidity 和 field return 的闭环。

## 为什么不立即满产

快速提高 starts 会增加 WIP，却可能让未稳定工艺产生更多 scrap；加速 qualification 会缩短风险发现时间，却把失效推到客户；通过扩大 inspection 抓缺陷会降低逃逸，却增加 cycle time 且不修复根因。

chosen design 应采用分阶段 gate：工程批验证结构，pilot line 验证重复性，limited production 验证供应和测试，volume ramp 再扩大投入。每个 gate 绑定 yield、可靠性和 cycle-time 条件，而非日历日期。

## 证据请求

- 目标 package 的逐站 yield waterfall 与按周趋势；
- defect pareto、返工率、报废成本和 excursion closure；
- constraint tool uptime、备件 lead time 与扩容计划；
- supplier qualification matrix 与材料变更通知机制；
- test coverage、false fail、escape 和 field correlation；
- customer acceptance criteria 与实际签收记录。

[Inference] 若公司只提供“最高月产能”而回避 product-mix、良率与 qualification，其收入预测高度依赖尚未证明的制造学习曲线。

## 二阶效应与估值

提高 assembly yield 后，HBM allocation 或 substrate becomes constraint；增加 test coverage 后，tester 和 socket 产能可能成为新瓶颈；良率提升也可能降低单位需求量，改变设备采购节奏。估值模型应把收入拆成 capacity × qualified utilization × yield × price，并对 ramp delay、返工和客户集中度做敏感性分析。

## 资料

- [TSMC Annual Reports](https://investor.tsmc.com/english/annual-reports) [Primary Source]
- [JEDEC Standards and Documents](https://www.jedec.org/standards-documents) [Primary Source]
- [imec Advanced Packaging](https://www.imec-int.com/en/what-we-offer/research-portfolio/advanced-packaging) [Independent]


## 基础概念桥接

案例中的数字必须进入统一 waterfall：理论峰值到 kernel、application、system、availability-adjusted output，再到单位经济性。为 base、upside、downside 分别写依赖和触发器，避免把最好条件的演示直接当财务预测。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。
