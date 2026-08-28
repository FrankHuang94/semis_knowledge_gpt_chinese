# Yield Economics：从 Wafer Yield 到 Good System 与现金流

## 1. Yield不是一个百分比

Semiconductor产品经历 wafer fabrication、wafer sort、die preparation、stack/bond、package、final test、board和 system acceptance。每层都有 yield、rework、cycle time和成本。只报 wafer yield可能掩盖昂贵后段损失；只报 final yield又无法定位改善点。

决策单位是：

<code>Cost per qualified good system = 全部投入、加工、测试与报废成本 / 客户可接受输出</code>

~~~mermaid
flowchart LR
  W[Wafer starts] --> D[Good dies]
  D --> K[Known-good-die]
  K --> A[Assembly]
  A --> P[Good packages]
  P --> B[Boards]
  B --> S[Qualified systems]
  R[Rework / scrap] -.每层.-> W
~~~

## 2. 基础 die-yield直觉

随机 defect越多、die面积越大，good die概率通常越低。简单 Poisson启发式：

<code>Y_die = exp(-D0 × A)</code>

D0是 defect density，A是 die area。真实缺陷会 clustering，设计冗余、critical area和工艺层不同，因此常用更适合的负二项或经验模型。公式用于 sensitivity，不是由 marketing die size精确算良率。

[Estimate] 若 <code>D0×A=0.5</code>，Poisson yield约61%；把面积减半，约78%。但两颗小 die组成产品的组合概率约 <code>0.78²=61%</code>，尚未计 D2D与 assembly。Chiplet收益还来自 wafer utilization、node mix和 binning，不是数学魔法。

## 3. Edge loss与 gross dies

Wafer边缘放不下完整矩形 die，gross dies不是 wafer area简单除 die area。Die越大，edge loss相对更高。Scribe lanes、test structures和 exclusion zone也减少可用面积。

Gross-die模型需要 wafer diameter、die dimensions和 placement算法。公开估算应标 [Estimate]，并对 gross dies范围而非单值做 sensitivity。

## 4. Parametric 与 functional yield

Functional yield回答电路是否工作；parametric yield回答 frequency、power、leakage、memory margin和 SerDes是否达到目标 bin。可工作的 die不一定能卖成最高 SKU。

Binning把 variation转成不同产品，改善 total sellable yield，但受市场 mix限制。若低 bin需求不足，它仍可能被折价或报废。Revenue yield应按每个 bin ASP和需求计算，而不是把所有 functional dies视为同价。

## 5. Wafer sort与 KGD

更强 wafer test可以在昂贵 package前筛掉坏 die，提高 assembly输入质量；代价是 tester time、probe card、DFT面积和 false reject。某些 path只有装配后可测试，KGD永远不是绝对。

测试经济学比较：

<code>Expected downstream scrap avoided > incremental test cost + good die false rejects</code>

Advanced package中一颗坏 die可能损失多个 HBM和 substrate，因此前段 test价值上升。

## 6. Package组合 yield

[Estimate] 一个 module需要四颗 logic chiplets、六个 HBM stacks、十组关键 bond。Logic KGD各98%、HBM各97%、bond各99.7%、其余 assembly95%：

<code>Y = 0.98^4 × 0.97^6 × 0.997^10 × 0.95 ≈ 70%</code>

若只看98% logic yield，会严重高估 output。不同 failure不独立：warpage、thermal或 process excursion可能同时影响多个位置，因此实际 tail更差。

## 7. Rework与 redundancy

如果坏 HBM或 optical engine可在中间阶段替换，effective yield会提高，但 rework有识别、拆除、清洁、再 attach与 reliability成本。重复 rework可能损害 good components。

Redundant lanes、spare cores、repair rows可以把部分 defect转成降级 bin。设计团队应比较冗余 area/power与 scrap saved。Repair信息还要安全存储、在 boot时加载并可追溯。

## 8. Cycle time与 WIP

Yield改善不只增加 output，还减少 WIP占用、返工、排队和现金被锁定。一个两个月流程中，早期 defect到最后才发现，会消耗后续所有 cycle和材料。

Little定律直觉：<code>WIP = Throughput × Cycle time</code>。同样 output下，cycle time缩短会减少 WIP与响应时间。Capacity紧张时，减少返工可能比增加设备更快提高 good output。

## 9. Learning curve

Ramp初期 defect Pareto不断变化：design、mask、process window、tool matching、material、assembly和 test program。成熟学习应表现为：

- first-pass yield上升；
- rework下降；
- defect concentration关闭；
- distribution收窄；
- cycle time稳定；
- 多 lot、多 tool、多 site一致；
- customer return与 inline data相关。

一次 best lot不是 learning。按周平均可能掩盖 tool-to-tool或 product mix；需要 cohort和 control chart。

## 10. Design yield与 manufacturing yield

Design marginality会在 PVT corner表现为系统性低 yield，不能靠 fab清洁解决。DFM、redundancy、timing/power margin和 package co-design决定 manufacturability。Manufacturing defect则通过 process control、equipment和材料改善。

Root cause归属影响合同与毛利。Foundry、fabless、OSAT、substrate和 memory vendor若没有共同 data sharing，问题会在供应商之间循环。

## 11. Cost stack

Good-unit成本至少包括：

- wafer与 mask/NRE摊销；
- wafer sort与 burn-in；
- good dies/HBM；
- interposer/bridge/substrate；
- assembly与 test；
- rework/scrap；
- logistics与 inventory；
- warranty/RMA；
- capacity reservation；
- yield ramp工程。

Early product的低 yield可能由高 ASP吸收，但若客户要求固定价格，supplier承担学习风险。长期 agreement中谁承担 scrap和 price-down非常关键。

## 12. Yield与 capacity的乘法

Nameplate starts × yield = output。新增20% capacity但 yield从80%降到65%，good output反而略降。Ramp团队如果为追 volume扩大 process window之外的 tools/material，可能牺牲质量。

[Estimate] 原 line每周10,000 starts、80% yield，输出8,000；扩到12,000但 yield65%，输出7,800。正确 incentive是 good qualified output和 field quality，不是 starts或 tool utilization。

## 13. Why-not

### 为什么不追求百分之百 yield

最后几个缺陷可能需要极高 test、冗余和 process成本；经济最优不是数学最大。高端 scarce product与低价 commodity的最优点不同。

### 为什么不把所有测试放最后

晚发现会浪费 expensive downstream inputs，且 root cause更难定位。

### 为什么不认为 chiplet一定改善 yield

组合、bond和 package yield可能抵消单 die提升；必须算 full stack。

## 14. Engineering → Strategy

| Yield lever | 工程成本 | 商业价值 |
|---|---|---|
| 小 die/chiplet | D2D/package | wafer utilization/reuse |
| More test | time/DFT | 避免后段 scrap |
| Redundancy | area/power | repair/binning |
| Rework | cycle/reliability | salvage |
| Process control | capex/data | stable output |
| Binning | validation/SKU | revenue yield |
| Supplier sharing | IP/coordination | faster root cause |

## 15. Technical diligence questions

1. Yield按 wafer、die、stack、package还是 system？
2. Functional、parametric、sellable和 revenue yield？
3. Gross dies与 defect model假设？
4. KGD coverage、false reject和 test time？
5. 每个 assembly interface yield与相关性？
6. Rework次数、成功率和 reliability？
7. Defect Pareto、lot/tool/site分布？
8. Cycle time、WIP和返工queue？
9. Good-unit cost对 yield的 sensitivity？
10. Field return是否反馈到 inline control？

## 16. Takeaways

1. Yield必须沿 wafer到 qualified system逐层建模。
2. Good-package组合概率可能抵消小 die的高单体良率。
3. Test、rework、redundancy和 binning共同决定 revenue yield。
4. Yield改善同时释放材料、设备、WIP和现金。
5. 管理应以 good qualified output和 field quality为目标，而非 starts。

## Primary sources

- [Primary Source] [TSMC 2025 Annual Report：Quality、3DFabric 与 Capacity](https://investor.tsmc.com/static/annualReports/2025/english/index.html)
- [Primary Source] [UCIe Consortium Specifications：Compliance and Test](https://www.uciexpress.org/specifications)


## 基础概念桥接

先区分 wafer starts、WIP、throughput、cycle time、die yield、assembly yield、qualified capacity 与 good shipments。设备已安装不代表产品可出货；材料、HBM、substrate、test、客户认证和地理风险都会迁移约束。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。


## 进阶工程术语桥接

本篇进一步需要掌握：IR drop、thermal resistance、warpage、hybrid bonding、wafer sort、process window 与 qualification。阅读这些术语时，不只记中英文对应，还要补齐系统位置、正常路径、饱和或失败路径、直接 counter、端到端结果、产品状态和证据等级。若工程会议出现“已解决”“无开销”“已量产”，应立即追问 workload、boundary、configuration、status/date、failure mode 与 falsifier。

延伸阅读：[进阶工程术语手册](../31_glossary/advanced_engineering_terms_handbook.md)。
