# Case：HBM 与 Advanced Packaging Capacity Investment——“需求很强”之后怎么建模

## 1. Capacity thesis必须从 good systems倒推

AI accelerator需求增长会同时拉动 logic wafer、HBM、base die/interposer、substrate、CoWoS类 assembly、test、board、power与 cooling。投资者若只用 GPU units乘每颗 HBM stacks，会忽略 yield、mix、qualification、inventory timing和最小瓶颈。

目标是构建一条可审计 capacity chain：

<code>Demanded systems → qualified accelerator modules → good packages → matched HBM stacks + logic dies → wafer starts + assembly tools</code>

Output由最小的 qualified、matched capacity决定，不由最大 installed nameplate决定。

~~~mermaid
flowchart LR
  L[Logic good dies] --> M{Matched kit}
  H[Qualified HBM stacks] --> M
  I[Interposer/base die] --> M
  S[Substrate] --> M
  M --> P[Advanced packaging]
  P --> T[Final test/yield]
  T --> B[Boards/racks]
~~~

## 2. Status与 source纪律

截至 2026-08-24：

- Samsung页面把 12-layer HBM3E描述为 Mass Production/Production。[Vendor Claim]
- SK hynix表示 HBM3E已量产，并在2025年完成 HBM4开发与 mass-production readiness；“准备量产”不等同于所有客户 Production/Deployed。[Vendor Claim]
- TSMC年度报告把多种 CoWoS/SoIC阶段分别描述为 volume production、development或预计进入 production。[Primary Source]

数据库必须保留 Announced、Sampling、Production、Shipping、Deployed、Roadmap或 Rumored，不把 development、sample、qualified与 revenue shipment混为一谈。客户 qualification往往比供应商“量产准备”更晚，也可能按 accelerator平台分别完成。

## 3. Demand不是一个数字

HBM demand取决于：

- accelerator shipments；
- 每 module stack数量；
- stack capacity/layers/generation；
- good-stack yield；
- engineering samples与 spares；
- 客户 mix和 bin；
- inventory days；
- platform ramp/cannibalization；
- inference/training配置；
- package attach yield。

更高 capacity stack可能减少 stack数量，也可能让产品提高总 memory。Generational transition会同时存在 HBM3E/HBM4，老设备与新设备不可完全 fungible。

## 4. Worked bottleneck model

[Estimate] 某季度各环节可支持的 qualified module-equivalents：

- logic good dies：120,000；
- matched HBM kits：105,000；
- interposer/substrate：115,000；
- advanced packaging starts：100,000；
- final yield：92%。

Good output：

<code>min(120000,105000,115000,100000) × 0.92 = 92,000 modules</code>

Logic扩产20%不改变 output。Packaging扩到125,000后，HBM成为瓶颈，output约96,600。只有同时提高 HBM到120,000，output才约110,400。[Estimate]

这类模型比“每个环节都增长”更重要，因为它暴露投资的边际价值与下一瓶颈。

## 5. Installed、qualified与 effective capacity

Installed tools不等于 output。Effective capacity需要：

<code>Tools × Throughput × Uptime × Yield × Qualified mix</code>

新 line可能处于 installation、process qualification、customer qualification或 yield ramp。Cycle time也会让当季 capex在数季后才变 shipment。设备可处理某类 package，不代表能处理目标尺寸、warpage、bump pitch与 HBM stack。

管理层口径常用 wafer/month、units/month、revenue capacity或 percentage growth，必须统一成同一 good-product boundary。

## 6. HBM自身是多段流程

HBM需要 DRAM wafer、KGD、TSV、thinning、stacking/bonding、base die、test与 customer qualification。更多 layers提高 capacity，却增加 die匹配、bond和 thermal挑战。单 die yield高不保证 stack yield。

[Vendor Claim] Samsung HBM3E页面给出特定 12-layer产品的 up to 1,180 GB/s与9.2 Gbps规格；这些是产品页 peak条件，不是所有 stack的 production yield或 application bandwidth。投资模型应使用 good qualified stacks而非 raw DRAM bits。

## 7. Advanced package是另一条 yield tree

Package将 logic、HBM、interposer/RDL/bridge与 substrate组合。Final yield受到：

- KGD escape；
- microbump/hybrid bond；
- interposer/RDL defect；
- substrate/warpage；
- underfill/molding；
- power/thermal interaction；
- final test；
- reworkability。

昂贵 package后段失败会损失多个 good inputs。Capacity价值因此同时来自 tool count、process yield与 test/repair，不应只估算新增厂房面积。

## 8. Qualification与 allocation

HBM不是完全 commodity。不同 vendor/generation可能需要 PHY、timing、thermal、firmware与 package共同 qualification。Accelerator vendor可能 dual-source，但每个 source的 volume、bin与 platform支持不同。

Allocation还受 long-term agreement、prepayment、take-or-pay与 strategic customer priority影响。Spot price无法代表真正可获得 capacity。Diligence需要区分 contracted、reserved、qualified、delivered与 accepted。

## 9. Bottleneck迁移的投资含义

当 packaging短缺时，CoWoS/OSAT设备、substrate与 test价值上升；扩产后，HBM wafer或 stacking可能成为约束；HBM放量后，power/cooling与 rack deployment可能限制 installed compute。投资不能静态持有“永远短缺”的叙事。

Leading indicators包括：

- tool delivery与 move-in；
- qualification lots；
- cycle time与 first-pass yield；
- supplier inventory；
- accelerator platform launch；
- customer capex与 power delivery；
- package size/stack count变化；
- rework与 RMA。

## 10. Why-not：为什么不无限扩 HBM

HBM capex具有周期与产品代际风险。若 accelerator demand低于预期、memory capacity per unit变化、stack层数提高或客户集中，新增 capacity可能过剩。General DRAM与 HBM工艺/packaging资源的 fungibility有限，转换并非即时。

HBM vendor还必须协调 logic base die、TSMC/packaging伙伴与客户 qualification。过快扩产可能降低 yield、增加 write-off与 price pressure。合理策略是以 long-term demand visibility和 modular ramp管理，而不是只看当前 premium。

## 11. Why-not：为什么不由 accelerator vendor自行封装

垂直整合可以控制 schedule和 IP，却需要巨额工艺、设备、材料、yield learning与供应关系。Foundry/OSAT已有规模与工程生态，能服务多个客户；但集中也形成 capacity dependency。

Accelerator vendor更可能通过预付款、共同开发、dedicated lines、design rules和 multi-sourcing加强控制，而非完全复制制造。谁承担 capex、yield和 obsolescence风险决定 economics。

## 12. Pricing与 margin bridge

ASP上涨可能来自更高 layer/capacity、短缺、复杂 package或长期合同，并不等于 unit margin同比增长。需要扣除：

- more dies per stack；
- advanced node base die；
- stacking/test time；
- lower early yield；
- outsourced packaging fee；
- depreciation；
- scrap/rework；
- customer qualification；
- inventory reserve。

Revenue growth还可能由 mix而非 units驱动。用 bit shipment、stack shipment、good kit与 revenue交叉验证。

## 13. Scenario tree

| Scenario | Demand | Yield/ramp | 结果 |
|---|---|---|---|
| Bull | accelerator强、memory/unit升 | 按期 | HBM/package长期紧 |
| Base | 增长但代际切换 | 正常学习 | bottleneck轮换 |
| Bear demand | deployment受power限制 | capacity到位 | price/mix压力 |
| Bear execution | demand强 | qualification/yield迟 | revenue推迟、客户切换 |
| Technology shift | 新架构减少外部 bytes | 旧capacity受压 | 价值迁到新 stack/base die |

概率应随 evidence更新，而不是季度后解释。

## 14. Red flags与 falsifiers

### Red flags

- 把 announced capacity当 qualified output；
- 不给 cycle time/yield；
- HBM3E与HBM4完全 fungible；
- 用 GPU订单重复计算 cloud capex；
- 忽略 customer concentration；
- 只看 wafer starts不看 stacking/package；
- 认为 price永远因结构短缺上涨；
- 用 supplier“ready”代表 platform Deployed。

### 关键 evidence

- 客户 qualification与 shipment；
- multi-quarter good-stack yield；
- package tool uptime与 cycle；
- signed allocation/LTA；
- accelerator board/rack deployment；
- inventory与 receivables；
- product mix和 base-die source；
- power/cooling capacity兑现。

## 15. Engineering → Strategy

| 工程约束 | 资本配置 | 可能赢家 | 风险 |
|---|---|---|---|
| DRAM wafer | fab/equipment | memory vendor | cycle |
| Stacking/bond | advanced tools | HBM leader/equipment | yield |
| Base die | logic foundry | foundry/IP | node cost |
| CoWoS/RDL | packaging lines | foundry/OSAT | capacity lag |
| Substrate | material/fab | substrate supplier | warpage |
| Final test | testers/handlers | test vendor | coverage |
| Rack power | facility | power/cooling | deployment delay |

## 16. Technical diligence questions

1. Demand用 modules、stacks、bits还是 revenue建模？
2. 每 platform stack count、layers与 generation？
3. Installed到 qualified good output的 bridge？
4. 每环节 yield、cycle time、uptime与 mix？
5. Customer qualification和 allocation状态？
6. HBM/base die/package供应是否互锁？
7. Generation transition的 tool/product fungibility？
8. ASP增长来自 mix、shortage还是 value？
9. 下一 bottleneck和过剩点在哪里？
10. Power/cooling是否限制最终 deployment？
11. Bear case下 depreciation与 inventory？
12. 哪些 leading indicators能在财报前验证？

## 17. Takeaways

1. HBM投资模型必须从 good deployed systems向上游倒推。
2. Output由最小 qualified matched capacity与 final yield决定。
3. Vendor production readiness不等于 customer-qualified deployment。
4. Bottleneck会在 HBM、package、substrate、test与 facility之间迁移。
5. 资本回报取决于 timing、mix、yield和合同，不只取决于 AI需求方向。

## Primary sources

- [Primary Source] [TSMC 2025 Annual Report](https://investor.tsmc.com/static/annualReports/2025/english/index.html)
- [Primary Source] [TSMC CoWoS](https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/cowos.htm)
- [Vendor Claim] [Samsung HBM3E](https://semiconductor.samsung.com/dram/hbm/hbm3e/)
- [Vendor Claim] [SK hynix HBM4 development and mass-production readiness](https://news.skhynix.com/en/sk-hynix-completes-worlds-first-hbm4-development-and-readies-mass-production/)


## 基础概念桥接

案例中的数字必须进入统一 waterfall：理论峰值到 kernel、application、system、availability-adjusted output，再到单位经济性。为 base、upside、downside 分别写依赖和触发器，避免把最好条件的演示直接当财务预测。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。
