---
id: engineering_to_strategy
title: Engineering → Strategy：从 Bottleneck、Design Choice 到 Value Capture
concepts: [engineering_to_strategy, value_migration, tco, moat, switching_cost, roadmap_risk]
prerequisites: [bottleneck_shifting, system_boundary, manufacturing_supply_chain]
level: [2, 3, 4, 5]
status: draft
last_verified: 2026-08-24
source_date: 2026-08-24
---

# Engineering → Strategy：从 Bottleneck、Design Choice 到 Value Capture

> 第一次阅读：Sections 1–8  
> 第二次阅读：Sections 9–18  
> 深入阅读：Sections 19–26

## 阅读前后

读前应理解 [Bottleneck Map](../00_start_here/follow_the_bottleneck.md)、[Modern AI Datacenter](../20_rack_cluster_datacenter/modern_ai_datacenter.md) 与 [Manufacturing & Supply Chain](../22_manufacturing_supply_chain/manufacturing_supply_chain.md)。读后应能把engineering delta翻译为system performance、BOM/TCO、supplier leverage、switching cost、moat、risk与可证伪预测。

## 1. 先告诉我为什么需要它

Strategy讨论常从market size、ASP或roadmap slide开始，却跳过产品为什么有价值。Engineering改变只有在解除目标workload的constraint、能被制造部署、并让某个参与者捕获收益时，才成为战略价值。

同一个technical win可能让component ASP上升，也可能通过系统简化让总成本下降；可能强化platform，也可能标准化接口并削弱lock-in。需要一条因果链连接physics与economics。

## 2. 一句话直觉

**先找谁限制useful work，再看新方案把瓶颈移到哪里、谁控制新稀缺资源、客户是否愿意为系统结果付费。**

## 3. 默认推理链

~~~mermaid
flowchart LR
  W[Workload objective] --> B[Bottleneck]
  B --> D[Design choice]
  D --> P[Delivered performance]
  P --> E[System economics]
  E --> V[Value capture]
  D --> N[New bottleneck]
  N --> R[Roadmap risk / value migration]
~~~

## 4. 前置知识

System boundary、workload/SLO、utilization、yield、capacity、BOM、TCO、gross margin、switching cost、standard、ecosystem、qualification、roadmap与scenario analysis。

## 5. Step 1：定义目标函数

Training看time-to-quality/goodput；inference看cost/token、TTFT/ITL与availability；cloud看revenue/constraint；facility看useful compute/power。没有目标函数，“更快”“更省电”无法排序。

## 6. Step 2：定位 Bottleneck

用Roofline、traffic、power/thermal、capacity与timeline确定当前constraint。Bottleneck必须绑定workload与boundary：kernel memory-bound不代表rack memory-bound；optics省电不代表job更快。

## 7. Step 3：列 Design Alternatives

至少比较维持现状、incremental fix、architectural shift与software workaround。记录每个方案解决什么、付出什么、依赖什么、何时可用。Chosen design不必physics最优，可能是qualification、ecosystem或time-to-market最优。

## 8. Step 4：Performance Waterfall

[
Delivered=Peak	imes Kernel efficiency	imes Memory efficiency	imes Fabric efficiency	imes Availability
]

每个factor必须用同一workload和boundary。Vendor peak只是一层；software coverage、thermal throttle、straggler与failure会折损。

## 9. Step 5：System Economics

从component price扩展到good-system cost、power/cooling、network、software/license、deployment、spares、downtime与operations。Savings可能来自少买hardware、延后facility、提高utilization或缩短time-to-revenue。

## 10. Value Migration

旧bottleneck解除后，新约束吸引capex与margin。例如compute提升使HBM/package/optics/power更稀缺；CPO可能减少retimer却增加optical packaging/test。Value不是永远留在最先进silicon。

## 11. Value Capture

Technical value由谁捕获取决于scarcity、differentiation、substitutability、contracting与customer visibility。Component可关键但被标准化；software可不在BOM却控制platform adoption。要区分value creation与value capture。

## 12. Moat Taxonomy

- Physics/process：难复制的device、yield或packaging。
- Architecture：system partition/dataflow优势。
- Software/data：compiler、kernels、telemetry、tuning corpus。
- Ecosystem：developers、standards、qualified partners。
- Capacity/operations：installed tools、learning、deployment/service。
- Contract/control：interfaces、allocation、long-term commitments。

Moat需说明持续时间与绕过路径。

## 13. Switching Cost

迁移成本包括code port、performance tuning、model validation、data/control integration、hardware qualification、spares、training与organizational risk。Open API降低部分成本，但performance portability和operations仍可lock-in。

## 14. 为什么不按 Peak Spec 排名？

Peak忽略workload、precision、shape、memory/network、power与software。只有当constraint在对应compute pipe且能持续feed，peak delta才传导到output。

## 15. 为什么不按 Component ASP 判断价值？

高ASP可能反映scarcity，也可能被system savings抵消；低ASP component可能卡住整机。应计算incremental system value与supplier bargaining，不是只看BOM占比。

## 16. 为什么不把 Standards 当成 Commoditization？

Standard定义接口，未必标准化implementation、yield、software、qualification或operations。它可扩大市场，也可把差异化上移/下移。看哪一层仍有performance/learning curve。

## 17. 为什么不把 Capacity Announcement 当成 Supply？

Capex、tool delivery、installation、qualification、yield ramp与customer approval之间有长链。Announced、installed、qualified和good output必须分开。

## 18. 量化例：System Value Bridge

[Estimate] 假设新accelerator系统价格高 (20%)，但相同workload的delivered throughput高 (50%)，power高 (10%)。简化的hardware cost/work单位比：

[
rac{1.2}{1.5}=0.80
]

即hardware cost/useful throughput下降约 (20%)。若software利用率只有旧系统的 (70%)，则优势可能消失。此例说明strategy模型必须包含delivered、not peak。

## 19. Time Dimension

Technology可长期优越却错过deployment window。Roadmap分析要列sample、qualification、volume、software readiness、facility readiness与customer adoption。Early share、learning和ecosystem可能形成路径依赖。

## 20. Scenarios 与 Sensitivities

Base/upside/downside不应只改market CAGR；应改关键engineering变量：yield、HBM supply、software efficiency、power cap、network utilization、qualification delay。找出结论对哪个变量最敏感。

## 21. Competitive Mapping

比较竞争者时保持同boundary：chip vs chip、rack vs rack、service vs service。记录make/buy、critical suppliers、proprietary/open interfaces、software coverage、installed base与migration tools。Winning product可能来自balanced system，而非每项spec第一。

## 22. Engineer Language Decoder

| 说法 | 战略翻译 | 追问 |
|---|---|---|
| “breakthrough” | 哪个constraint被移除 | 新瓶颈？ |
| “platform” | 控制哪些interfaces/workflows | switching cost来源？ |
| “open ecosystem” | 哪层可替换 | performance/qualification可移植吗？ |
| “supply secured” | contract/qualified/good output | 期限与priority？ |
| “TCO advantage” | 哪些cost与utilization假设 | sensitivity？ |

## 23. 常见误解

Engineering最好不等于商业赢家；first mover不等于长期moat；垂直整合不总能捕获价值；开放不等于无差异化；短缺价格不等于结构性margin。

## 24. Evidence Discipline

每项事实标记Primary Source、Independent、Vendor Claim、Estimate或Inference；产品状态标记Announced、Sampling、Production、Shipping、Deployed、Roadmap或Rumored。重要结论必须能追溯输入与日期。

## 25. Strategy Questions

1. 客户目标函数是什么？
2. 当前constraint在哪里？
3. 方案为何现在可行？
4. 付出哪些new bottlenecks？
5. Delivered performance waterfall？
6. Good-system/TCO变化？
7. 谁控制稀缺资源？
8. 替代/绕过路径？
9. Switching cost与adoption friction？
10. 哪个observable能证伪 thesis？

## 26. 小结

Engineering → Strategy不是给技术加商业术语，而是保持因果链：workload→constraint→choice→delivered result→economics→capture→new constraint。每个thesis都应有时间、状态、证据与falsifier。

下一步阅读 [Technical Diligence](../27_technical_diligence/technical_diligence_playbook.md)。

## Sources

- [OIF Implementation Agreements](https://www.oiforum.com/technical-work/implementation-agreements-ias/)
- [OCP Specifications](https://www.opencompute.org/wiki/Open_Rack/SpecsAndDesigns)
- [TSMC Annual Reports](https://investor.tsmc.com/english/annual-reports)


## 基础概念桥接

先把技术主张还原为 workload、bottleneck、constraint、alternatives、chosen design 和 second-order effect，再讨论市场。价值捕获取决于 IP、产能、认证、生态、客户迁移和成本曲线；技术领先不自动等于 moat。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。
