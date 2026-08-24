# 2.5D vs 3D Integration：横向铺开与垂直堆叠如何交换距离、热与良率

## 1. 几何定义只是起点

2.5D通常把多个 dies并排放在 silicon interposer、RDL或 bridge上，通过高密度横向连接通信；3D则把 active/passive dies垂直堆叠，以 microbump或 hybrid bonding等形成更短、更密的垂直连接。现实产品可能同时使用两者：logic-on-logic 3D stack再与 HBM或 I/O die放在 2.5D package中。

选择的目标不是“堆得更高”，而是在 bandwidth density、latency、package area、power delivery、thermal、test、yield与 capacity之间找到可制造点。

~~~mermaid
flowchart TB
  subgraph A[2.5D]
    C1[Compute Die] --- I[Interposer / RDL / Bridge]
    C2[Compute / I/O Die] --- I
    H[HBM] --- I
  end
  subgraph B[3D]
    T[Top Active Die]
    M[Bond Interface]
    D[Bottom / Base Die]
    T --- M
    M --- D
  end
  A --> S[System choice]
  B --> S
~~~

## 2. 2.5D 的 architecture posture

并排布局让每颗 die较容易接触 heat spreader/cold plate，hotspots可在平面分散；HBM stacks与 compute可通过宽 interposer/RDL互连。它适合大 package、多 compute tiles与 memory integration。

代价是横向距离、interposer/bridge面积、substrate routing与 package footprint。大 interposer存在制造、handling、warpage与成本挑战；RDL/bridge方案在 density、reach和 design flexibility上各有边界。Package越大，power delivery与 mechanical可靠性越难。

[Primary Source] TSMC将 CoWoS描述为面向 HPC/AI的 2.5D平台，可整合多个 SoC与 HBM。引用它应理解为 vendor平台说明，不是所有 2.5D方案的通用性能保证。

## 3. 3D 的 architecture posture

垂直 stacking缩短 die-to-die距离，提高连接密度并减少 package footprint。它可以把 cache堆在 compute上、把 compute放在 active base die上，或把不同功能层按 process优化。

但上层 die的热必须穿过其他 layers或受限的散热路径；power/clock/test也必须垂直穿越。Thermal coupling可能迫使 top/bottom die降频，抵消互连收益。Stack越复杂，bond defect、die warpage、alignment与 known-good-die要求越高。

3D最有价值的场景通常是高度通信、面积受限、可将热源合理分层的 block，而不是把所有高功率逻辑简单叠在一起。

## 4. Connection density 改变 architecture

2.5D与3D都让 die-to-die比 board SerDes更短、更宽，可减少重型 PHY与 energy/bit。3D垂直 bond pitch进一步缩小后，跨 die interface可以更接近 on-die network：更多 wires、更低单 wire速度、更细粒度 partition。

但 connection density提高也增加 design规则、power grid、test access与 defect sensitivity。逻辑架构能否使用这些 wires取决于 coherence、clock domain、floorplan和 compiler/runtime，不是 bond数量本身。

## 5. 计算：连接数不是 useful bandwidth

[Estimate] 某 3D interface有一万个 data connections，每个每 cycle传一位，clock为相对频率1；raw bandwidth记为10,000单位。考虑 ECC/repair保留10%、protocol效率85%、traffic locality70%，useful bandwidth为：

<code>10,000 × 0.90 × 0.85 × 0.70 = 5,355</code>

若把 connections加倍但 locality因 partition不佳降到40%，结果变：

<code>20,000 × 0.90 × 0.85 × 0.40 = 6,120</code>

物理连接翻倍只带来约14% useful提升。[Estimate] Floorplan和 data placement可能比 bump headline更重要。

## 6. 为什么不把所有 dies都放在 2.5D 平面

Package面积、interposer/RDL reach、substrate escape与 power delivery会限制横向扩展。更长 D2D wire增加 latency与 energy，package机械变形和 assembly equipment也有尺寸边界。大平面还会增加 expensive package材料，即使 dies本身良率不错。

当两个 block需要极高 bandwidth density且适合垂直 thermal安排时，3D可以更有效；当主要需求是整合 HBM和多个高功率 compute时，2.5D的散热与可测试性通常更友好。

## 7. 为什么不把所有 dies垂直堆叠

热是第一反对理由，但不是唯一理由。Stack需要 KGD、bond yield、alignment、TSV/power delivery与新 test flow；一层失败可能损失整套 stack。垂直层数增加后，repair与 debug更难，design schedule跨多个 die团队耦合。

许多 I/O、analog、HBM和高功率 block也不适合被埋在 stack中。3D应被视为稀缺的高密度连接资源，用于能从短距离获得最大系统收益的边界。

## 8. 为什么不只使用 organic substrate

Organic substrate成本和生态成熟，但 routing pitch、via与 electrical characteristics限制超高密度 D2D。可以用更高速 SerDes减少 wires，却增加 PHY面积、power与 latency。Silicon interposer、bridge或 RDL提供更细 routing，但成本和 capacity更高。

选择常是混合：局部 bridge承担高密度 link，organic substrate承担较长距离与外部 escape；或 RDL fan-out在成本与密度之间折中。

## 9. Thermal 是 dataflow 的约束

如果上层 cache die低功率、下层 compute高功率，stack可能可控；如果两层都是高功率 compute，hotspots叠加。Thermal throttling会改变 frequency、memory timing、leakage与 reliability，进而改变 performance waterfall。

Thermal simulation必须与 workload power map联动，而不是只用均匀 TDP。不同 model phase、sparsity与 collective会让 hotspot移动。Cold plate接触面、TIM、die thickness与 microfluidic等方案都改变可行边界，同时增加制造复杂度。

## 10. Power delivery 与 signal integrity

更多 vertical connections不只用于 data，还要分给 power/ground、clock、test与 repair。Current density、IR drop与 electromigration限制 active layers。若 power从 package底部穿过 base die到 top die，base die grid与 TSV资源会成为关键。

2.5D中，长 package power path、HBM与 compute并列也会产生 droop与 noise coupling。Package architecture必须同时优化 data和 power；只展示漂亮的 D2D bandwidth图不完整。

## 11. Yield、KGD 与 test

2.5D需要验证每颗 die、interposer/RDL、microbumps与 final assembly；3D还增加层间 bond和堆叠后不可直接触达的 nodes。Wafer-to-wafer可提供高吞吐，但要求两片 wafer的 die匹配与 yield；die-to-wafer选择性更强，handling和 throughput不同。

Test access architecture应在 RTL阶段设计。若只能在 final stack发现错误，昂贵 good dies与 packaging会被一起损失。Repair lane、redundant bond与 built-in self-test可以提高 recoverability，但占用 area与 connections。

## 12. Product reality：区分平台名称与物理机制

[Primary Source] TSMC 3DFabric把 CoWoS、InFO与 SoIC归为不同 2.5D/3D integration选项。厂商平台名称很重要，因为 design rules、capacity、tool flow与 qualification绑定于具体生态；但跨公司比较时必须还原为：

- interposer、RDL、bridge或 direct bond；
- bump/bond pitch与 usable connections；
- passive还是 active base die；
- die-to-wafer、wafer-to-wafer或其他 assembly；
- HBM/logic位置；
- power与 thermal path；
- KGD、repair与 final test；
- production status、supplier与 capacity。

## 13. Second-order effects

1. 更密 D2D降低 communication energy，却让 thermal成为主导墙。
2. 2.5D扩大 package后，substrate、interposer与 CoWoS类 capacity可能限制出货。
3. 3D提高 transistor density，却可能因降频无法兑现 peak。
4. Active base die改善 routing，也引入额外 silicon yield与 firmware。
5. 更小 bond pitch提高 bandwidth density，同时增加 alignment、particle与 metrology要求。
6. Repair提高 yield，却增加 protocol、routing与 test。
7. 先进封装成为 architecture后，foundry/OSAT、EDA、material与 equipment共同捕获价值。

## 14. Engineers actually say

- “3D gives on-die-like bandwidth.”：问 useful bandwidth、protocol、power与 locality。
- “Thermals are manageable.”：问 workload hotspot、junction分布与 throttling。
- “The interposer is passive.”：问 routing、power plane、defect与 cost。
- “We use hybrid bonding.”：问 pitch、alignment、yield、repair与 production volume。
- “All dies are known good.”：问 test coverage和 assembly-induced failure。
- “The package is scalable.”：问 size、warpage、substrate escape、capacity与 tool limit。

## 15. Engineering → Strategy

| 方案 | 主要价值 | 新约束 | 价值控制点 |
|---|---|---|---|
| 2.5D interposer | 多 die+HBM、较好散热 | 面积/成本/capacity | foundry packaging |
| RDL/fan-out | 密度与成本折中 | warpage/design rules | OSAT/foundry |
| Embedded bridge | 局部高密连接 | placement/assembly | bridge IP |
| 3D stacking | 短距离、高密度 | thermal/yield/test | bonding/equipment |
| Active base die | routing/coherence | 单点/功耗 | base-die platform |
| Hybrid 2.5D+3D | 系统最优化 | 复杂度最高 | full-stack integrator |

## 16. Technical diligence questions

1. 为什么目标 partition需要 2.5D或3D，而非 monolithic/board？
2. Raw与 useful D2D bandwidth、latency、energy如何？
3. Worst-case workload thermal map与 throttling？
4. Power delivery、IR drop与 electromigration margin？
5. Die、bond、interposer与 assembly yield model？
6. KGD coverage、repair与 final test成本？
7. Package size、warpage与 mechanical qualification？
8. Foundry/OSAT、substrate、bonding equipment与 HBM capacity？
9. Platform status是 prototype、qualified还是 volume production？
10. 下一代扩展先撞到 thermal、power、package area还是 yield？

## 17. Takeaways

1. 2.5D横向整合，3D垂直堆叠，现实常是混合。
2. 3D用更短连接换 thermal、power与 test难题。
3. 2.5D更利于多高功率 dies与 HBM，却受 package面积和供应限制。
4. Raw connection density只有经过 locality与 protocol才变 useful bandwidth。
5. 先进封装的竞争力来自可量产的 design-manufacturing platform。

## Primary sources

- [Primary Source] [TSMC CoWoS](https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/cowos.htm)
- [Primary Source] [TSMC 3DFabric](https://3dfabric.tsmc.com/schinese/dedicatedFoundry/technology/3DFabric.htm)
- [Primary Source] [TSMC InFO](https://3dfabric.tsmc.com/schinese/dedicatedFoundry/technology/InFO.htm)
- [Primary Source] [UCIe Consortium Specifications](https://www.uciexpress.org/specifications)
