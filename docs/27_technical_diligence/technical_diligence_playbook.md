---
id: technical_diligence_playbook
title: Technical Diligence Playbook：如何拆 Claim、验证 Evidence、识别 Scale-up Risk
concepts: [technical_diligence, claim_decomposition, evidence_ladder, falsification, reproducibility]
prerequisites: [engineering_to_strategy, system_boundary, product_status]
level: [3, 4, 5]
status: draft
last_verified: 2026-08-24
source_date: 2026-08-24
---

# Technical Diligence Playbook：如何拆 Claim、验证 Evidence、识别 Scale-up Risk

> 第一次阅读：Sections 1–8  
> 第二次阅读：Sections 9–18  
> 深入阅读：Sections 19–26

## 阅读前后

读前需理解 [Engineering → Strategy](../26_engineering_to_strategy/engineering_to_strategy.md) 与完整AI system chain。读后应能把marketing claim拆成可测试subclaims，建立evidence ladder，设计falsification tests，并覆盖performance、manufacturing、software、reliability、supply与deployment readiness。

## 1. 先告诉我为什么需要它

Technical diligence不是判断团队“聪不聪明”，而是判断一项claim在明确boundary、conditions与timeline下是否成立、可重复、可规模化，并能产生经济价值。Prototype可证明physics，却不证明yield、cost、reliability或customer adoption。

最危险的问题通常不是明显造假，而是definition drift：lab metric被写成product metric，single component被写成system result，announced roadmap被写成available supply。

## 2. 一句话直觉

**把每个形容词改写成带单位、条件、baseline、状态和日期的命题，再问什么证据能支持或推翻它。**

## 3. Claim decomposition

~~~mermaid
flowchart LR
  C[Marketing claim] --> M[Metric + unit]
  C --> B[Boundary + baseline]
  C --> W[Workload + conditions]
  C --> S[Status + scale]
  C --> T[Timeline]
  M --> F[Falsification test]
  B --> F
  W --> F
  S --> F
~~~

## 4. 前置知识

Hypothesis、measurement、baseline、confidence、sample bias、system boundary、benchmark、yield、qualification、production status与total cost。

## 5. 把 Claim 写成 Testable Statement

“更快”改为：在某model/shape/precision/software/power/system size下，相对某baseline，某metric改善多少。“量产”改为：在某site/line，经过某customer qualification，以某good-output rate shipping。

缺少任一关键限定，结论先记为unknown。

## 6. Evidence Ladder

从弱到强：

1. Concept slide / simulation。
2. Component lab demo。
3. Integrated prototype。
4. Repeated third-party test。
5. Pilot line / sampling customers。
6. Qualified production output。
7. Field deployment与reliability data。
8. Repeat purchase / scaled economics。

不同claim需要不同evidence。Physics claim可由demo支持，supply claim不能。

## 7. Source Hierarchy

Primary technical docs、standards、papers、regulatory/financial filings优先；independent testing补充；vendor claim保留标签；estimate公开inputs；inference展示推导。避免把多篇转述当多份独立证据。

## 8. Benchmark Integrity

检查workload、dataset/model、precision、batch/sequence、software、power、thermal、system size、network、baseline tuning、warm-up、duration与statistic。平均值可隐藏tail，single kernel可隐藏host/network，peak可隐藏utilization。

## 9. Reproducibility

记录hardware revision、firmware、driver/compiler/library、configuration、seed、commands、environment与raw outputs。不能复现不必等于错误，但confidence应下降，并识别缺少的是access、method还是stability。

## 10. Performance Waterfall Audit

从peak到delivered逐层检查kernel coverage、memory/communication、power/thermal、availability与end-to-end output。若claim只改善非constraint block，system value有限。

## 11. Manufacturing Readiness

询问process node/PDK、tapeout/wafer status、die size、yield denominator、test coverage、package/substrate/HBM sources、assembly line、cycle time、capacity、quality system与customer qualification。Prototype assembly与repeatable production是两件事。

## 12. Software Readiness

检查framework/operator/shape/precision coverage、fallback、compiler stability、kernel tuning、debug/profiling、deployment、upgrade与customer code changes。Demo可能靠hand-tuned path，long tail决定adoption cost。

## 13. Reliability 与 Service

Coverage包括temperature/power cycling、aging、error containment、firmware recovery、field replaceable units、spares、MTTR、telemetry与root cause。Rack-scale product还需facility、coolant、power与network failure modes。

## 14. 为什么不只做专家访谈？

Expert提供context与hypotheses，但可能有selection、memory、employer与visibility bias。Interview应与documents、measurements和cross-functional evidence交叉。

## 15. 为什么不要求所有 Raw Data 才前进？

Early diligence常无法获得全部raw data。可先做bounded inference、列missing evidence与decision thresholds。关键是不要把absence变成certainty，也不要因为不完整而停止所有分析。

## 16. 为什么不只看 Customer Logo？

Logo可能代表evaluation、pilot、small purchase、production或strategic partnership。要问use case、deployment scale、paid status、renewal、expansion、reference permission与customer concentration。

## 17. 为什么不把 NDA Information 当作更可信？

Confidential不等于accurate。仍需definition、measurement、sample、date和internal consistency。记录可分享结论与source restrictions，避免无法审计的“有人告诉我”。

## 18. 量化例：Claim Sensitivity

[Estimate] 一项产品称end-to-end throughput提升 (2	imes)。若只有 (60%) 工作可走accelerated path，accelerated部分提升 (3	imes)，其余不变，Amdahl近似：

[
Speedup=rac{1}{0.6/3+0.4}=1.67	imes
]

若另有 (10%) integration overhead，结果更低。例子说明必须核验coverage与system overhead，而非只看fast path。

## 19. Falsification Matrix

对每个核心thesis列：

- Claim。
- Required conditions。
- Supporting evidence。
- Contradicting evidence。
- Test/observable。
- Threshold。
- Owner/date。
- Decision impact。

好问题不是“你确定吗”，而是“什么结果会让你改变结论”。

## 20. Red Flags

Metric定义反复变化；baseline故意弱；只展示best run；拒绝说明失败率；product status模糊；yield无denominator；capacity混同announcement；software依赖单一expert；客户无法描述paid deployment；所有风险都被称为execution。

## 21. Interview Routing

Architecture问dataflow/bottleneck；silicon问timing/power/area；package问yield/thermal/test；software问coverage/fallback；manufacturing问WIP/cycle/capacity；customer问integration/output；operations问failure/MTTR。让同一claim跨团队回答，检查一致性。

## 22. Engineer Language Decoder

| 说法 | Diligence翻译 | 追问 |
|---|---|---|
| “production ready” | 哪个qualification/status | good output与客户？ |
| “validated” | 谁、何test、多少samples | raw distribution？ |
| “industry leading” | metric/baseline/date | comparable conditions？ |
| “no bottleneck” | boundary/workload | 瓶颈移到哪？ |
| “customer demand” | pipeline/order/deployment | paid/renewal？ |

## 23. Common Failure Modes

把simulation当silicon；把single die当package；把package当rack；把peak当application；把sampling当shipping；把signed LOI当revenue；把capacity reservation当good supply；把technical feasibility当unit economics。

## 24. Deliverable Structure

Executive conclusion；claim/evidence table；system architecture；performance waterfall；manufacturing/supply readiness；software/deployment；risk/falsifier；open questions；source log。每个结论标confidence与last verified。

## 25. 核心问题清单

1. Claim的metric/boundary/baseline？
2. Evidence ladder到哪层？
3. Result能否复现？
4. Workload是否representative？
5. Constraint是否真的解除？
6. Yield/capacity/qualification状态？
7. Software coverage和fallback？
8. Failure/service model？
9. Unit economics与sensitivity？
10. 哪个observable会推翻结论？

## 26. 小结

Technical diligence的产物不是“通过/不通过”印章，而是一张可更新的claim-evidence-risk map。最强结论同时说明成立条件、证据等级、未知项、falsifier与下一步验证。

下一步使用 quizzes、Fermi exercises 与 case studies训练。

## Sources

- [IEEE 802.3 Working Group](https://www.ieee802.org/3/)
- [OIF Implementation Agreements](https://www.oiforum.com/technical-work/implementation-agreements-ias/)
- [OCP Specifications](https://www.opencompute.org/wiki/Open_Rack/SpecsAndDesigns)


## 基础概念桥接

尽调先定义决策和可证伪假设，再建立 evidence ladder。区分 primary source、independent evidence、vendor claim、estimate 与 inference；同时检查 mechanism、performance、power、manufacturing、software、deployment 和 economics。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。


## 进阶工程术语桥接

本篇进一步需要掌握：profile、compliance、certification、sampling、production、shipping、design win、attach rate 与 value migration。阅读这些术语时，不只记中英文对应，还要补齐系统位置、正常路径、饱和或失败路径、直接 counter、端到端结果、产品状态和证据等级。若工程会议出现“已解决”“无开销”“已量产”，应立即追问 workload、boundary、configuration、status/date、failure mode 与 falsifier。

延伸阅读：[进阶工程术语手册](../31_glossary/advanced_engineering_terms_handbook.md)。
