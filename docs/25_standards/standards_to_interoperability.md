# 从 Standard Compliance 到 Interoperability：通过测试不等于系统可替换

标准的价值是降低接口不确定性，让不同团队和供应商可以并行设计。但标准通常只覆盖可观察行为的一部分；电气 margin、optional feature、firmware、management、security、thermal 与 support policy 仍会造成组合风险。因此“符合标准”是必要条件，不是可替换性的充分条件。

## 四层兼容

~~~mermaid
flowchart TB
  E[Electrical compliance] --> P[Protocol compliance]
  P --> S[Semantic compatibility]
  S --> O[Operational interoperability]
  O --> V[Commercial substitutability]
~~~

**电气层**关注 signaling、timing、channel 与误码；**协议层**关注 packet、state machine、retry 与 ordering；**语义层**关注 software 看到的 memory、coherence、device 与 error behavior；**运营层**覆盖 discovery、telemetry、upgrade、reset、security 和 failure recovery。商业可替换还需要供货、qualification、warranty 与支持。

## 为什么标准会保留 optionality

强制所有实现支持全部功能会提高一致性，却增加低端产品成本并拖慢标准形成；保留 optional features 允许创新和分层，却产生 capability negotiation 与组合矩阵。标准组织常用 profiles、compliance tests 和 interoperability events 收敛差异，但测试不可能穷举所有拓扑、版本和错误时序。

版本号相同也不保证行为完全一致。一个设备可能只支持基础 profile，另一个支持扩展；firmware bug 可能在边界状态触发；host、switch 和 endpoint 对模糊条款的解释也可能不同。采购必须记录 feature bitmap、版本、errata 和经过验证的组合。

## Compliance、Certification 与 Plugfest

compliance test 通常检查单个实现是否满足规定要求；certification 可能由联盟定义标志和测试流程；plugfest 让多家实现互连，发现规范文字未覆盖的交互问题。三者提供不同证据，均不能代替目标系统的 workload acceptance。

chosen design 应建立分层验证：先做 electrical/protocol conformance，再做多供应商 matrix，然后做目标拓扑、压力、升级与故障注入。测试结果要绑定 firmware、board revision、cable 和 configuration，不能只保存“通过”两个字。

## 二阶效应

标准成功会扩大市场和供应选择，也会把竞争从基础接口移向实现质量、软件、功耗、管理和服务；接口稳定后，系统集成者可能获得更多价值。相反，过早的专有扩展可提供性能，却制造锁定和升级协调。开放并不自动等于低成本：多供应商 validation 和责任划分也需要组织能力。

## Diligence 问题

1. 宣称支持的是哪个版本、profile 和 optional features？
2. compliance 由谁执行，测试报告能否复查？
3. 与哪些 host、switch、endpoint、cable 和 firmware 组合验证？
4. reset、hot-plug、错误注入和升级过程中是否保持语义？
5. 标准未定义的 management 与 security 由谁负责？
6. 第二供应商是否真正 qualified，还是只在 roadmap 上兼容？
7. errata 如何传播到客户配置与软件 workaround？

## 资料

- [PCI-SIG Specifications](https://pcisig.com/specifications) [Primary Source]
- [Compute Express Link Specifications](https://computeexpresslink.org/cxl-specification/) [Primary Source]
- [JEDEC Standards and Documents](https://www.jedec.org/standards-documents) [Primary Source]
- [IEEE Standards Association](https://standards.ieee.org/) [Primary Source]


## 基础概念桥接

先区分 specification、version、profile、optional feature、compliance、certification、plugfest 和 interoperability。符合标准不保证可替换；真实 host、switch、endpoint、cable、firmware 与错误路径仍需组合验证。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。


## 进阶工程术语桥接

本篇进一步需要掌握：profile、compliance、certification、sampling、production、shipping、design win、attach rate 与 value migration。阅读这些术语时，不只记中英文对应，还要补齐系统位置、正常路径、饱和或失败路径、直接 counter、端到端结果、产品状态和证据等级。若工程会议出现“已解决”“无开销”“已量产”，应立即追问 workload、boundary、configuration、status/date、failure mode 与 falsifier。

延伸阅读：[进阶工程术语手册](../31_glossary/advanced_engineering_terms_handbook.md)。
