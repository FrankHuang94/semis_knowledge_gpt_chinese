# Monolithic vs Chiplet：Die Partition 是成本、互连与组织边界的共同选择

## 1. 为什么“大芯片切小”不是自动更便宜

Monolithic SoC把主要功能集成在一颗 die上；chiplet system把 compute、I/O、cache、memory interface或 accelerator拆成多个 dies，再通过 package内 die-to-die互连组合。Chiplet可以改善 yield、复用 IP、混合 process node并突破 reticle/area限制，但会引入 PHY/protocol、package routing、latency、power、test与供应协调。

因此问题不是“chiplet是否取代 monolithic”，而是某个功能切分点能否创造足够的 yield、reuse或 heterogeneity收益，覆盖 die-to-die和 assembly成本。

~~~mermaid
flowchart LR
  M[Monolithic SoC] --> I1[On-die wires]
  C[Chiplet System] --> D1[Compute die]
  C --> D2[I/O die]
  C --> D3[Cache / accelerator die]
  D1 <--> F[Die-to-die fabric]
  D2 <--> F
  D3 <--> F
  F --> P[Package + Test + Power + Thermal]
~~~

## 2. Monolithic 的优势

On-die wire通常具有较低 latency、较高 bandwidth density与较低 energy/bit，不需要额外 bump、PHY与 package crossing。Clock、coherency、reset、security与 debug可以在单一 design hierarchy内完成，wafer test和 product qualification边界较清楚。

对面积适中、volume明确、功能耦合紧密且同一 process适合所有 block的产品，monolithic可能是更简单、更低风险的答案。它也避免多 die assembly yield与 known-good-die logistics。

代价是大 die defect exposure、reticle限制、mask/NRE集中，以及模拟/I/O/SRAM等不一定随先进 node同等受益的 block也被迫一起迁移。任何一个 block延期都可能拖累整个 tape-out。

## 3. Chiplet 的四类价值

### Yield partition

把大 die切成多个较小 dies，单 die良率可能提高；但 final package需要所有 dies与 bonds共同成功。是否省钱取决于 die area、defect density、wafer cost、test coverage、assembly yield与 package cost。

### Process heterogeneity

Compute可使用先进 logic node，I/O、analog、cache或 security可留在更成熟、成本更合适的 process。收益来自“每个 block用合适工艺”，不是简单的旧节点更便宜。

### IP 与产品复用

同一 I/O die、base die或 accelerator tile可以跨产品组合，缩短衍生 SKU周期并摊薄验证。复用只有在接口、floorplan、power、firmware与 lifecycle真正稳定时成立；复制 RTL文件不等于已验证 chiplet平台。

### Scale beyond one die

多个 compute tiles可增加总 transistor与 memory interfaces，避开单 reticle边界。代价是跨 die traffic、coherence和 physical integration变成一等架构问题。

## 4. 计算：只看单 die yield会得出错误结论

[Estimate] Monolithic die良率为55%，每片 wafer得到100个 gross dies，则约55个 good dies。Chiplet方案把功能切为四颗，单颗良率提高到88%；假设每套需要四颗、die供应平衡，理论组合概率为：

<code>0.88^4 = 0.60</code>

再假设六组关键 interface各有99.5%成功率、assembly成功率97%：

<code>Y_package = 0.88^4 × 0.995^6 × 0.97 ≈ 56.5%</code>

最终并没有远高于 monolithic。Chiplet仍可能因 wafer utilization、不同 die size、node mix与复用获益，但必须用 good-package cost而不是单 die yield判断。

## 5. Partition 应沿什么边界切

好的 boundary通常具有高内部 locality、相对稳定的接口、可独立测试和较低跨界 traffic。候选包括 I/O、cache、compute tiles、analog、security与 memory controller。

差的 boundary会让高频细粒度 dependency穿过 D2D link，增加 latency、serialization与 coherence state；或让一个 die无法独立测试，KGD失去意义。Architecture team应建立 traffic matrix，按 bandwidth、latency、ordering、coherence与 failure要求排序，再决定切分。

## 6. 为什么不把每个功能都做成小 chiplet

过细切分会增加 PHY面积、bump数量、package routing、clock/reset domain、test step与 inventory组合。每条 interface都需要 protocol、error handling、versioning和 security。小 die数量增多还扩大 assembly机会与 thermal interaction。

模块化软件的直觉不能直接映射到 silicon。物理 boundary有固定 energy、latency与 manufacturing成本；只有需要独立缩放、独立工艺或高复用的 block值得跨 die。

## 7. 为什么不坚持一颗大 die

当 die接近 reticle、defect exposure高、portfolio需要多 SKU，或 I/O/analog不值得迁移先进 node时，monolithic成本和 schedule风险会快速上升。一个 block的 bug可能报废整颗 die，库存也无法重用。

Chiplet允许分别迭代 compute与 I/O，并可能用冗余 tile或 binning构建不同 SKU。但这些收益依赖成熟 D2D、package和 test infrastructure；没有平台能力时，第一次 chiplet产品可能更慢、更贵。

## 8. Die-to-die 不只是 PHY

D2D stack至少包含 physical link、link/error management、protocol、可能的 cache coherency、software discovery与 security。UCIe旨在标准化 package内 D2D physical、protocol与 software model。[Primary Source] 标准化降低接口重新发明成本，但“符合 UCIe”不自动保证任意 dies能混装：bump map、package technology、power、clock、thermal、test、firmware与 commercial qualification仍需协同。

Custom D2D可以为特定 package优化 density与 energy，却增加 vendor lock-in和 IP验证。选择取决于内部复用与外部生态哪个更重要。

## 9. Coherence 与 NUMA

多个 compute dies共享 memory时，系统要选择统一 coherent domain、分区 NUMA或 software-managed placement。全 coherence简化编程，却增加 directory、snoop/metadata、latency与 verification；NUMA减少协议负担，却要求 software感知 locality。

Chiplet系统看似一颗 package，软件却可能观察到不同 memory distance、bandwidth与 failure domain。把所有差异隐藏在硬件里可能浪费资源；全部暴露给 programmer又损害可用性。Compiler/runtime与 OS成为关键。

## 10. Test、repair 与 inventory

KGD要求 wafer probe能覆盖足够逻辑、PHY与 memory；未装配时无法完全测试的 path会留下 escape。Assembly后还需 package-level test、burn-in与 system qualification。若一颗昂贵 die在最后失败，其他 good dies与 package价值可能一同损失。

Inventory也复杂：不同 bin、revision与 supplier的 dies必须按 compatibility matrix组合。某一小 chiplet短缺可能阻塞整套产品，形成“最便宜 die成为出货瓶颈”的反直觉结果。

## 11. Thermal 与 power

拆 die增加总边界与放置自由度，可把热源分散，也可能把多个高功率 tile挤在 package内。D2D PHY、active interposer/base die和更长 power path增加热与 IR drop。3D stacking还会形成垂直 thermal resistance。

Floorplan必须把 hotspot、HBM、VRM与 cold plate共同优化。一个逻辑上漂亮的 partition若无法供电或散热，不是可量产 architecture。

## 12. Product reality：识别真正的平台复用

看到厂商宣称“modular chiplet architecture”时，要求：

1. 哪些 dies跨 SKU或 generation复用？
2. 每颗 die的 node、area、supplier与 status？
3. D2D是 custom还是 standard，protocol与 bandwidth条件？
4. Package技术、substrate/interposer与 assembly source？
5. KGD coverage与 final test flow？
6. Coherence/NUMA由谁管理？
7. Die revision能否独立更新，compatibility如何？
8. 缺一颗 die时 inventory能否替代？
9. Good-package cost与 monolithic baseline？
10. Field failure能否定位或关闭单 tile？

## 13. Second-order effects

1. 小 die yield改善后，package assembly与 substrate可能成为新瓶颈。
2. Node heterogeneity节省 wafer cost，却增加多工艺 qualification与 schedule coupling。
3. IP复用缩短设计，也可能让旧 I/O die限制新 compute。
4. 标准 D2D扩大供应选择，但 common denominator可能牺牲定制效率。
5. 更多 SKU组合提高市场覆盖，也增加 inventory与 validation矩阵。
6. Active base die改善 routing/coherence，却成为单点良率与 thermal瓶颈。
7. Chiplet生态成熟后，价值可能从单一 SoC design迁到 D2D IP、packaging与 integration software。

## 14. Engineers actually say

- “Smaller dies yield better.”：问 final good-package yield与 cost。
- “We can mix nodes.”：问每个 block为何适合该 node、接口与 qualification。
- “The chiplet is reusable.”：问已在哪些 SKU复用、revision compatibility。
- “UCIe makes it interoperable.”：问 package/bump/power/test与 multi-vendor实证。
- “It looks like one GPU.”：问 NUMA、coherence、failure与 profiler可见性。
- “We can add more tiles.”：问 fabric bisection、memory与 power如何扩展。

## 15. Engineering → Strategy

| 选择 | 收益 | 风险 | 价值控制点 |
|---|---|---|---|
| Monolithic | 低 latency、简单验证 | 大 die yield/NRE | leading-edge foundry |
| Chiplet partition | yield/reuse/heterogeneity | package与接口 | integration platform |
| Custom D2D | 高效率 | lock-in | proprietary IP |
| Standard D2D | 生态与复用 | common denominator | consortium/IP/test |
| Active base die | routing/coherence | 单点与热 | base-die provider |
| Multi-source dies | resilience | qualification | system integrator |

## 16. Technical diligence questions

1. Partition traffic matrix与 locality evidence？
2. Monolithic与 chiplet的 full cost/yield model？
3. D2D latency、energy、bandwidth与 error behavior？
4. KGD、assembly、final test与 field return coverage？
5. Coherence/NUMA和 software placement？
6. Package power、thermal、warpage与 mechanical margin？
7. 每个 die的 capacity、lead time与 second source？
8. Revision mixing、security与 firmware lifecycle？
9. 实际复用节省了多少 schedule/NRE，而非 roadmap设想？
10. Bottleneck解除后是否转移到 packaging、HBM或 substrate？

## 17. Takeaways

1. Chiplet不是自动低成本；必须比较 final good-package economics。
2. 最佳 partition沿 locality、工艺、复用与可测试边界切分。
3. D2D包含 PHY、protocol、coherence、software与 security。
4. Chiplet把设计风险分散，也把 package、test和 inventory变成核心架构。
5. 竞争优势来自可重复使用的 integration platform，而不只是把 die切开。

## Primary sources

- [Primary Source] [UCIe Consortium Specifications](https://www.uciexpress.org/specifications)
- [Primary Source] [TSMC 3DFabric Technology](https://3dfabric.tsmc.com/schinese/dedicatedFoundry/technology/3DFabric.htm)
- [Primary Source] [TSMC CoWoS Technology](https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/cowos.htm)
