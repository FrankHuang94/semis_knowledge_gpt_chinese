---
id: chiplet_3d
title: Chiplet 与 3D Integration：Die Partition、D2D Protocol、Coherence 与 Thermal
concepts: [chiplet, die_to_die, ucie, coherence, three_d_integration, active_base_die]
prerequisites: [advanced_packaging, cache_coherence, serdes, yield, thermal]
level: [2, 3, 4]
status: draft
last_verified: 2026-08-24
source_date: 2026-08-24
---

# Chiplet 与 3D Integration：Die Partition、D2D Protocol、Coherence 与 Thermal

> 第一次阅读：Sections 1–8  
> 第二次阅读：Sections 9–18  
> 深入阅读：Sections 19–26

## 阅读前后

读前需理解 [Advanced Packaging](../16_advanced_packaging/advanced_packaging.md)、[PCIe/CXL](../10_pcie_cxl_io/pcie_vs_cxl.md)、cache coherence 与 yield。读后应能从 workload和physical constraints选择 die partition，区分 PHY/protocol/coherence layers，并判断 2D/2.5D/3D 的 latency、energy、thermal、test 与 ecosystem取舍。

## 1. 先告诉我为什么需要它

先进 SoC 同时包含 compute、cache、memory controllers、SerDes、analog、security 与 power management。这些 blocks不一定适合同一 process，也不一定按同一节奏演进。Chiplet 把 system partition成多个 dies，使IP复用、process mixing、SKU组合与reticle扩展成为可能。

但 die boundary 不是抽象线。跨边界需要 PHY、clock、protocol、routing、power与test；distributed cache/coherence会引入latency和failure modes。3D 缩短 wires，却把 heat 与 power stacking变成主要约束。

## 2. 一句话直觉

**Chiplet 把 monolithic design problem 变成 interface 与 integration problem；3D 再把 wire problem 变成 thermal、power、test 和 yield problem。**

## 3. 系统位置

~~~mermaid
flowchart TB
  C0[Compute chiplets] <--> BASE[Cache / fabric / active base die]
  IO[I/O die] <--> BASE
  HBM[HBM] <--> PKG[Interposer / bridge]
  BASE <--> PKG
  PHY[D2D PHY] --- C0
  PROTO[Protocol / coherence] --- BASE
~~~

## 4. 前置知识

Die/reticle/yield、package routing、microbump/hybrid bonding、PHY、flit、flow control、cache coherence、NUMA、clock domain crossing、power delivery、thermal resistance与known-good-die。

## 5. 第一性原理：边界成本

把 block 跨 die 移动会增加：

[
Cost_{boundary}=Energy/bit+Latency+Area_{PHY}+Protocol overhead+Test+Yield risk
]

Chiplet benefit则来自 smaller-die yield、reuse、process optimization、parallel development与SKU flexibility。正确 partition 需要让长期复用和manufacturing benefit大于每次访问的 boundary cost。

## 6. 如何选择 Die Partition

常见 partition：

- Compute tiles：复制相同 cores/accelerators，便于scale SKU。
- I/O die：把SerDes、memory controllers与analog留在成熟process。
- Cache/base die：集中LLC、fabric、memory routing或power functions。
- Domain-specific dies：media、security、network、AI engine。
- Memory-on-logic：以vertical bandwidth换thermal complexity。

高频、细粒度、强coherence traffic更不适合跨较慢boundary；独立、可复用、process需求不同的blocks更适合chiplet化。

## 7. D2D Layer Stack

~~~mermaid
flowchart TB
  APP[Architecture semantics] --> COH[Coherence / memory / streaming protocol]
  COH --> ADAPT[Adapter / flit / retry / flow control]
  ADAPT --> PHY[D2D PHY / clocking]
  PHY --> BOND[Bumps / hybrid bonds / package wires]
~~~

“支持 UCIe”只说明某些 layers符合规范，不代表任意dies可直接组合。Coherence model、address map、security、boot、power state、mechanical stack与test仍需system agreement。

## 8. PHY：Parallel vs Serialized

Short-reach package links可用大量低速parallel wires，降低equalization与energy/bit；较长 package reach或低bump density可能使用更高serialization。PHY还需 clocking、deskew、lane repair、training、CRC/retry与power states。

Interface efficiency应按 useful payload、not raw wires × rate 计算。

## 9. Protocol 与 Flow Control

D2D protocol决定packet/flit format、credits、retry、ordering、error reporting与management。Streaming link可简单高效；load/store或coherent link需要address、snoop、ordering与failure semantics。Protocol越丰富，interoperability潜力越高，也增加state、latency与verification。

## 10. Coherence across Chiplets

Shared coherent memory让software视图简单，却需要directory/snoop、ordering与cache state迁移。跨die latency会放大 cache miss penalty，热点line可能制造fabric traffic。Alternatives包括non-coherent DMA、message passing、software-managed scratchpad与partitioned address spaces。

Coherence是software convenience与hardware communication cost之间的交易。

## 11. Active Base Die

Active base die可放fabric、cache、power management、clock与test logic，上方叠compute tiles。它能缩短vertical links并集中shared functions，却可能成为yield、thermal、bandwidth与single-point-of-failure中心。Base die process不必最先进，但必须支撑routing、power与known-good stacking flow。

## 12. 3D Thermal

Vertical stack的total power不是唯一问题；heat source位置与thermal path更重要。靠近cold plate的top die较易散热，bottom die可能被上层覆盖；inter-die bonding layers增加thermal interfaces。Temperature变化又影响leakage、timing与bond reliability，形成正反馈。

Thermal-aware floorplanning可能把cache或low-power logic放在特定层，而不是追求最高logic density。

## 13. Power 与 Clock

3D stack需要把power穿过substrate/base/TSV/bonds送到各层，同时维持IR drop与transient response。Clock跨dies要处理skew、jitter与independent power states。若一个chiplet可独立sleep，protocol必须管理isolation、state retention与wake latency。

## 14. 为什么不把所有 Blocks 都做成 Chiplets？

每个边界都付出PHY、protocol、bump、routing、latency和test。Small blocks若无reuse/process benefit，monolithic wiring更优。过度partition还增加供应商、version matrix与integration schedule。

## 15. 为什么不让不同 Vendors 任意 Mix-and-Match？

Common physical/protocol standard只是起点。Die dimensions、bump map、power rails、thermal limits、boot/security、coherence、test、warranty与liability仍需协同。开放chiplet市场需要可验证的interface contracts和business rules，不只是PHY compliance。

## 16. 为什么不全部使用 Coherence？

Coherence让general software容易，却产生directory/snoop traffic、state storage与ordering constraints。Accelerator pipeline或streaming dataflow常用explicit transfers更高效。选择应从programming model和sharing granularity出发。

## 17. 为什么不全部 3D？

3D提供最高interconnect density，却增加heat stacking、power delivery、bond yield、test access和repair困难。若2.5D已满足bandwidth，horizontal placement可能有更好的cooling与manufacturing margin。

## 18. 量化例：Boundary Overhead

[Estimate] 假设一个chiplet workload每次有用operation需要跨D2D搬运 (64) bytes，interface总energy为 (0.5 	ext{pJ/bit})，则仅传输energy约：

[
E=64	imes8	imes0.5 	ext{pJ}=256 	ext{pJ}
]

若通过tiling把同一数据在local memory复用八次，平均每次operation的boundary energy可降为约 (32 	ext{pJ})。这不是任何产品spec；它说明 software locality与chiplet partition必须co-design。

## 19. Yield 与 Known-Good-Die

Chiplet可提高单die yield，却增加die count、bonds、assembly与final test。Pre-bond test难以完全覆盖high-speed interface和thermal interaction；post-bond failure可能报废多个良品。Repair lanes、redundant links、binning与graceful degradation可改善economics，但需要architecture支持。

## 20. Verification 与 Lifecycle

Monolithic SoC已有复杂verification；multi-die还要验证protocol compatibility、reset sequence、power states、clocking、error injection、firmware组合和partial failure。各chiplet roadmap不同时，interface versioning与backward compatibility决定reuse是否兑现。

## 21. Workload Mapping 与 Second-order Effects

Large cache、AI compute和HBM适合高bandwidth package integration；I/O die适合process复用；latency-sensitive shared state可能留on-die。Chiplet解决reticle/yield后，bottleneck会迁移到package capacity、D2D energy、coherence traffic、thermal、test或integration schedule。

## 22. Engineer language decoder

| 说法 | 应翻译成 | 追问 |
|---|---|---|
| “disaggregated die” | 哪些functions跨boundary | traffic与latency多少？ |
| “UCIe compatible” | PHY/adapter/protocol哪一层 | package、boot、coherence已互操作吗？ |
| “active base” | base上有哪些logic/state | yield、thermal与failure影响？ |
| “3D bandwidth” | raw还是payload，何种traffic | power与temperature corner？ |
| “chiplet ecosystem” | 已qualified哪些vendors/dies | liability与test谁负责？ |

## 23. 常见误解

1. **Chiplet 等于 Lego。** Physical、protocol、power和business contracts仍高度定制。
2. **Smaller die yield高，所以package便宜。** Final good-package economics才有意义。
3. **3D link latency近似零。** PHY、clock、protocol与queue仍存在。
4. **Coherence自动提供统一性能。** NUMA和traffic hotspots仍需software管理。
5. **开放标准消灭vendor lock-in。** Packaging rules、tools、firmware与qualification仍可形成moat。

## 24. Product 与标准 grounding

- [Primary Source] [UCIe Consortium Resources](https://www.uciexpress.org/ucie-resources) 发布当前specification与开放chiplet ecosystem材料。
- [Primary Source] [Intel Foundry Advanced Packaging](https://www.intel.com/content/www/us/en/foundry/packaging.html) 描述EMIB、Foveros与hybrid-bond based integration design space。
- [Primary Source] [TSMC SoIC](https://www.tsmc.com/english/dedicatedFoundry/technology/SoIC_inDepth) 描述其3D stacking与integration路线。
- [Vendor Claim] Vendor的bandwidth density、energy与yield必须按payload、PHY mode、test vehicle、temperature和production status核验。

## 25. Engineering → Strategy 与 Diligence

Chiplet价值可能从单一leading-edge die迁移到reusable IP、D2D interface、packaging rules、test、EDA、firmware与ecosystem governance。标准化降低部分integration friction，却可能把差异化移到coherence、base die、package与software。

尽调应问：

1. Partition由workload还是organizational boundary驱动？
2. Traffic matrix、payload efficiency与latency distribution？
3. PHY/protocol/coherence各使用什么标准或定制？
4. Cross-die error如何detect、retry和contain？
5. Pre/post-bond test coverage与escape rate？
6. 3D thermal model如何用silicon data校准？
7. Base die是否成为bandwidth或failure bottleneck？
8. Versions、boot、security与power states如何兼容？
9. Good-package cost是否含bond/test/scrap？
10. Multi-vendor liability与root-cause owner是谁？

## 26. 小结与延伸

Chiplet不是封装同义词，而是一种把architecture切开再用physical/protocol contracts重组的system method。3D缩短wire，却要求把thermal、power、test和yield提前到architecture阶段。

下一步阅读 [Power Delivery](../18_power_delivery/index.md)、[Thermal & Cooling](../19_thermal_cooling/index.md) 与 [Modern AI Rack](../20_rack_cluster_datacenter/modern_ai_rack.md)。

## Sources

- [UCIe Consortium — Resources](https://www.uciexpress.org/ucie-resources)
- [Intel Foundry — Advanced Packaging](https://www.intel.com/content/www/us/en/foundry/packaging.html)
- [TSMC — SoIC](https://www.tsmc.com/english/dedicatedFoundry/technology/SoIC_inDepth)
