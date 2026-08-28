---
id: manufacturing_supply_chain
title: Semiconductor Manufacturing 与 Supply Chain：从 Wafer Start 到 Good AI System
concepts: [semiconductor_manufacturing, wafer_start, yield, cycle_time, capacity, supply_chain]
prerequisites: [device_fab, advanced_packaging, hbm, yield]
level: [2, 3, 4]
status: draft
last_verified: 2026-08-24
source_date: 2026-08-24
---

# Semiconductor Manufacturing 与 Supply Chain：从 Wafer Start 到 Good AI System

> 第一次阅读：Sections 1–8  
> 第二次阅读：Sections 9–18  
> 深入阅读：Sections 19–26

## 阅读前后

读前需理解基本fab flow、[HBM](../09_hbm/hbm.md)、[Advanced Packaging](../16_advanced_packaging/advanced_packaging.md) 与 [Chiplet/3D](../17_chiplet_3d_integration/chiplet_3d.md)。读后应能从wafer starts、die yield、cycle time、HBM、substrate、assembly/test推导good-system output。

## 1. 先告诉我为什么需要它

AI accelerator不是一片wafer直接变成rack。Logic wafers、HBM、interposer/RDL、substrate、assembly、test、board、optics、power和cooling必须按正确版本与时间汇合。任何一步短缺都会让其他昂贵components等待。

Supply chain分析要从finished good倒推。真正metric是单位时间交付多少经过qualification的good systems。

## 2. 一句话直觉

**System output由最慢且不可替代的qualified step限制；wafer capacity只有乘上yield、mix、cycle time与后段配套后才变成可售产品。**

## 3. End-to-end flow

~~~mermaid
flowchart LR
  W[Logic wafer] --> DS[Die sort]
  M[HBM wafers] --> ST[Stacking / test]
  I[Interposer / RDL] --> PKG[Advanced packaging]
  DS --> PKG
  ST --> PKG
  S[Substrate] --> PKG
  PKG --> FT[Final / system test]
  FT --> BD[Board / rack integration]
  O[Optics + power + cooling] --> BD
  BD --> DEP[Qualified deployment]
~~~

## 4. 前置知识

Wafer、die、mask、lithography、etch/deposition/CMP、WIP、cycle time、yield、binning、KGD、substrate、OSAT、capacity utilization、lead time与qualification。

## 5. 从 Wafer Start 到 Good Die

[
Good dies=Wafer starts	imes Dies/wafer	imes Yield
]

Yield包括defect、parametric、speed/power bins与test coverage。目标SKU可用率比泛化的“良率”更有意义。

## 6. Yield Learning

Ramp时systematic/random defects、design-rule sensitivity、process control与test escapes逐步改善。Learning速度取决于volume、inspection/metrology、failure analysis与design-fab feedback。“Yield improving”要问起点、斜率、target bin与measurement maturity。

## 7. Cycle Time 与 WIP

Fab包含大量设备访问、queue、batch、hold与rework。高utilization可提高设备output，却会放大queue和cycle-time variance。Hot lots能加速一批，也可能扰乱其他lots。Working capital与delivery predictability因此受WIP位置影响。

## 8. Tool Capacity 与 Product Mix

Lithography、etch、deposition、implant、CMP、metrology各有throughput和recipe mix。不同产品消耗不同layer count与tool time；wafer starts不可跨process等价。增加tool还需facility、installation、qualification、operators与spares。

## 9. HBM Supply Chain

HBM需要DRAM wafers、KGD、TSV/stacking、base/interface die、test与accelerator qualification。限制可在memory fab、stack assembly、test或vendor-specific qualification。Generation与stack变化还会牵动package、thermal与controller。

## 10. Advanced Packaging 与 Substrate

Large AI package需要interposer/RDL、organic substrate、fine-pitch bonding、underfill、lid、assembly与final test。Package area/layers增加会提高warpage、cycle time和yield sensitivity。Logic die有货不代表后段已匹配。

## 11. Test、Binning 与 KGD

Wafer sort尽早筛坏die；package test验证D2D/HBM；system test在real workload/thermal下发现marginal failure。Test减少field escapes，却增加ATE time。Binning提高economic yield，但增加inventory matching。

## 12. Capacity Equation

对串联系统可用近似：

[
Output=min(C_{logic},C_{HBM},C_{package},C_{test},C_{rack})	imes Y_{final}
]

最贵环节不一定是constraint；最小qualified capacity才是。

## 13. 为什么不只扩 Leading-edge Wafers？

若HBM、package、substrate、test或facility deployment受限，更多logic wafers只增加WIP。Expansion必须沿final BOM同步。

## 14. 为什么不保持大量 Safety Stock？

Inventory缓冲disruption，但先进产品价值高、版本变化快。过多stock面临obsolescence、mix mismatch与capital cost。关键是选择合适decoupling point。

## 15. 为什么不全部 Dual-source？

Second source需要design portability、process/package/test qualification、software支持与volume economics。Qualified不等于可立即转量；低volume双源还可能减慢learning。

## 16. 为什么不按 Nominal Capacity？

Nominal capacity忽略uptime、yield、mix、maintenance、qualification、cycle time和allocation。应建模good units per time与delivery distribution。

## 17. Geography 与韧性

多地fabs可能共享equipment、chemicals、mask data、IP、sub-tier suppliers与shipping lanes。Geographic diversity减少部分regional risk，却增加qualification与coordination。要画到sub-tier和utilities。

## 18. 量化例：Good Package Output

[Estimate] 假设每周 (1{,}000) 片logic wafers，每片 (60) gross dies，target-bin yield (70%)；每package需两颗logic dies，HBM支持 (18{,}000) packages，packaging capacity (16{,}000)，final yield (90%)。

Logic支持 (21{,}000) packages，最终：

[
Good=min(21{,}000,18{,}000,16{,}000)	imes0.9=14{,}400/week
]

这是简化估算，只说明constraint来自minimum。

## 19. Allocation 与 Lead Time

Supplier commit可能是reservation、wafer allocation、shipment forecast或non-cancellable order。Lead time也分manufacturing、queue、transport、qualification与site deployment。要检查contractual priority、flexibility与cancel liability。

## 20. Quality 与 Traceability

Excursion可能影响一批或跨批。Lot/wafer/die/package traceability、SPC、containment和root cause决定blast radius。Too-fast ramp可能产生latent reliability；too-slow qualification会错过market window。

## 21. Demand Cyclicality 与 Bullwhip

Long lead time、double ordering与低visibility放大需求波动。Shortage期夸大orders，capacity到位后inventory correction。AI demand还需区分training buildout、inference fleet、replacement与speculative reservation。

## 22. Engineer language decoder

| 说法 | 翻译 | 追问 |
|---|---|---|
| “capacity sold out” | 哪个step/node/time | committed还是forecast？ |
| “good yield” | 哪种yield与bin | denominator？ |
| “dual sourced” | design/qualified/volume-ready | 转量多久？ |
| “lead time” | 到wafer/package/deployment | queue占比？ |
| “supply constrained” | 最小good-output step | 下一瓶颈？ |

## 23. 常见误解

Wafer starts不等于chips；die yield不等于system yield；capex宣布不等于capacity可用；second source不等于fungible supply；inventory增长也不自动等于需求下降。

## 24. Primary Sources 与 Freshness

- [Primary Source] [TSMC 2025 Annual Report](https://investor.tsmc.com/static/annualReports/2025/english/index.html) 讨论technology、manufacturing footprint、capacity planning与advanced packaging。
- [Primary Source] [ASML 2025 Annual Report](https://www.asml.com/en/investors/annual-report/2025) 提供lithography、supplier ecosystem、capex cycle与risk背景。
- [Primary Source] [TSMC CoWoS](https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/cowos.htm) 描述S/R/L routes与production status。
- [Vendor Claim] Capacity、yield与roadmap数字需按report date和definition复核。

## 25. Engineering → Strategy 与 Diligence

Value capture取决于谁控制稀缺qualified capacity、yield data、design rules与allocation。尽调应问final constraint、capacity unit/mix、yield denominator、cycle time/WIP、HBM/package matching、contract priority、sub-tier single source、qualification path、excursion traceability与double ordering。

## 26. 小结与延伸

Supply chain不是BOM名单，而是一条带yield、cycle time、qualification与allocation的flow。用good systems per time建模，才能找到真实constraint与价值迁移。

下一步阅读 [Software / Hardware Co-design](../21_software_hardware_codesign/software_hardware_codesign.md)。

## Sources

- [TSMC — 2025 Annual Report](https://investor.tsmc.com/static/annualReports/2025/english/index.html)
- [ASML — 2025 Annual Report](https://www.asml.com/en/investors/annual-report/2025)
- [TSMC — CoWoS](https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/cowos.htm)


## 基础概念桥接

先区分 wafer starts、WIP、throughput、cycle time、die yield、assembly yield、qualified capacity 与 good shipments。设备已安装不代表产品可出货；材料、HBM、substrate、test、客户认证和地理风险都会迁移约束。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。
