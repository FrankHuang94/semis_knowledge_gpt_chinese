---
id: end_to_end_ai_system_case
title: End-to-End Case：如何审计一套“更快、更省电、可量产”的 AI Rack
concepts: [case_study, performance_waterfall, tco, technical_diligence, supply_chain]
prerequisites: [modern_ai_rack, engineering_to_strategy, technical_diligence]
level: [3, 4, 5]
status: draft
last_verified: 2026-08-24
source_date: 2026-08-24
---

# End-to-End Case：如何审计一套“更快、更省电、可量产”的 AI Rack

本案例使用虚构系统 Project Atlas。所有规格均为教学用 [Estimate]，不代表任何真实产品。目标是展示从claim到decision memo的完整workflow。

## 1. 原始 Claim

[Estimate] Atlas厂商称：

- Matrix peak比baseline高 (2.0	imes)。
- HBM bandwidth高 (50%)，capacity高 (40%)。
- Rack IT power高 (20%)。
- Scale-up domain扩大 (2.0	imes)。
- 相同LLM workload训练时间缩短 (45%)。
- 已“production ready”。

第一步不是相信或反驳，而是拆解definitions。

## 2. 定义目标与 Boundary

目标：相同model、dataset、quality target与time horizon下的time-to-quality和total cost。Boundary：rack hardware、scale-out network allocation、power/cooling、software/license、deployment与availability。排除facility construction需明确写出，而不是默认为零。

## 3. Claim Table

| Claim | 缺失 |
|---|---|
| Peak (2.0	imes) | precision、sparsity、clock、power |
| HBM +50% | effective/peak、channels、workload traffic |
| Domain (2.0	imes) | topology、bisection、latency、failure |
| Training -45% | model、parallel plan、baseline tuning、quality |
| Production ready | sample/qualified/shipping/good output |

## 4. Architecture Sketch

~~~mermaid
flowchart LR
  GPU[Compute + HBM] <--> SU[Scale-up switches]
  GPU <--> NIC[NIC / RDMA]
  NIC <--> SO[Scale-out fabric]
  PSU[Power shelves / busbar] --> GPU
  CDU[CDU / manifold] --> GPU
  SW[Compiler + kernels + collectives] -. controls .-> GPU
~~~

必须补充tray count、GPU count、HBM per device、NIC placement、optical ports、cooling coverage与failure partition。

## 5. Workload Decomposition

Training step拆为input、forward、backward、collectives、optimizer、checkpoint与sync。记录各阶段compute、HBM bytes、communication bytes与critical path。若baseline有较大input或network stall，matrix peak不会同比传导。

## 6. Roofline First Pass

[Estimate] Baseline peak (500 	ext{TFLOP/s})、HBM (4 	ext{TB/s})，ridge (125 	ext{FLOP/byte})。Atlas peak (1000 	ext{TFLOP/s})、HBM (6 	ext{TB/s})，ridge约 (167 	ext{FLOP/byte})。

Arithmetic intensity低于旧ridge的kernels主要受bandwidth；介于两ridge间的kernel在Atlas上可能仍memory-bound。Peak提升比bandwidth快，会让balanced software要求更高。

## 7. Kernel Coverage

列出GEMM/attention/norm/embedding/optimizer/custom ops的runtime share。对每项检查precision、Tensor Core path、fusion、layout、register spill与fallback。Vendor demo若只覆盖大GEMM，不能解释完整speedup。

## 8. Distributed Plan

为DP/TP/PP/EP建立rank map。更大scale-up domain可能减少scale-out traffic，也可能增加collective steps、switch dependency与failure blast radius。用actual collective sizes而非aggregate fabric spec。

## 9. Communication Estimate

[Estimate] 若每step有 (20 	ext{GB}) exposed collective payload，baseline effective collective bandwidth (200 	ext{GB/s})，Atlas (300 	ext{GB/s})，忽略latency的时间从 (100 	ext{ms}) 降到约 (67 	ext{ms})，只节省 (33 	ext{ms})。需要与claimed step-time delta对账。

## 10. Power / Cooling

[Estimate] Baseline rack (100 	ext{kW})，Atlas (120 	ext{kW})。若throughput提升 (1.6	imes)，IT energy/work约为：

[
rac{1.2}{1.6}=0.75
]

即理论下降 (25%)。但必须加入pump/fan、thermal throttle、power cap与facility constraint。

## 11. Availability

Scale-up domain增大可能让switch/cooling/power common failure影响更多devices。定义availability-adjusted goodput：

[
Goodput=Nominal throughput	imes Availability	imes Useful utilization
]

若Atlas repair time更长，headline throughput可能被抵消。

## 12. Manufacturing

拆BOM：logic dies、HBM stacks、interposer/RDL、substrate、switch ASIC、NIC、optics、power shelves、cold plates/CDU。对每项记录source、capacity、yield、qualification、allocation与lead time。

## 13. “Production Ready” Evidence

要求：released silicon revision、final package、repeatable system test、firmware/software release、customer qualification、weekly good output、shipping、field data与service procedure。只完成prototype integration应标Integrated Prototype。

## 14. Cost Bridge

[Estimate] Baseline rack price设为 (1.0)，Atlas (1.35)；delivered throughput若 (1.6)，hardware cost/work为 (0.844)，理论改善约 (16%)。若software efficiency使实际只有 (1.3)，ratio为 (1.038)，优势消失。

## 15. Deployment Time

增加liquid cooling、weight、power与fiber需求可能延长site readiness。若Atlas晚部署一个quarter，time-to-revenue损失需与per-rack advantage比较。Shipping date不是productive date。

## 16. Alternatives

- 继续购买更多baseline racks。
- Software optimization提高旧系统utilization。
- 使用smaller scale-up domain配更多scale-out。
- 延迟一代等待supply/price成熟。
- Hybrid fleet按workload分配。

Chosen alternative需看constraint与timeline。

## 17. Evidence Matrix

| Area | 当前证据 | 需要 |
|---|---|---|
| Silicon | vendor benchmark | raw counters、多shapes |
| Network | aggregate spec | collective p50/p99、topology |
| Power | nameplate | wall power、transient、cap |
| Cooling | design | CDU/flow/site acceptance |
| Manufacturing | roadmap | yield/good output/qualified sources |
| Customer | pilot | paid deployment/renewal |

## 18. Sensitivities

结论最可能对software efficiency、HBM supply、availability、facility delay与rack price敏感。每项设break-even；不要只给optimistic/base/pessimistic文字。

## 19. Falsifiers

- End-to-end gain低于 (1.25	imes)。
- HBM/package qualification延迟。
- Availability-adjusted throughput不优于baseline。
- Facility retrofit使productive deployment延后一周期。
- 核心operators大量fallback。
- Customer不扩大pilot。

[Estimate] Threshold仅作教学示例。

## 20. Interview Plan

Architecture：为什么domain扩大；performance：critical path；software：coverage/fallback；network：collectives；power/thermal：sustained limits；manufacturing：yield/capacity；operations：MTTR；customer：integration/output。

## 21. Preliminary Thesis

Atlas可能在compute-heavy、large-model、fast-domain-sensitive workload创造value；对memory-latency、small-batch或facility-constrained deployment，优势较弱。Value capture取决于software coverage、HBM/package supply与rack integration control。

## 22. Risks

Balanced-system risk、supply matching、software maturity、facility power/cooling、failure blast radius、price premium、baseline optimization与roadmap delay。

## 23. Decision Gates

Gate A：reproducible workload gain。  
Gate B：software coverage。  
Gate C：qualified good-system output。  
Gate D：site readiness。  
Gate E：availability/TCO proof。  

每gate有owner、date、evidence与go/no-go threshold。

## 24. One-page Memo Template

- Decision / confidence。
- Workload/boundary。
- Engineering delta。
- Delivered performance waterfall。
- TCO/value capture。
- Manufacturing/deployment status。
- Top risks与falsifiers。
- Next evidence。

## 25. What Changed the Answer?

若新证据只提高peak，不改变critical path，thesis不变；若software覆盖或HBM supply改善，confidence提升；若facility delay与MTTR恶化，system value下降。明确更新规则可防止confirmation bias。

## 26. 小结

End-to-end case的核心纪律是让每个headline经过workload、architecture、performance、power/thermal、manufacturing、deployment与economics七道门。最终结论不是“技术好不好”，而是在哪些条件下创造并捕获多少可持续价值。
