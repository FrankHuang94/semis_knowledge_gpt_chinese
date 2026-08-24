---
id: advanced_packaging
title: Advanced Packaging：为什么 AI 芯片的边界已经超出单颗 Die
concepts: [advanced_packaging, interposer, rdl, emib, microbump, hybrid_bonding, known_good_die]
prerequisites: [hbm, gpu, yield, signal_integrity, thermal]
level: [2, 3, 4]
status: draft
last_verified: 2026-08-24
source_date: 2026-08-24
---

# Advanced Packaging：为什么 AI 芯片的边界已经超出单颗 Die

> 第一次阅读：Sections 1–8  
> 第二次阅读：Sections 9–18  
> 深入阅读：Sections 19–26

## 阅读前后

读前需理解 [HBM](../09_hbm/hbm.md)、GPU、SerDes、基本 wafer/die/yield 与 thermal。读后应能比较 monolithic die、organic MCM、silicon interposer、embedded bridge、RDL fan-out、2.5D 与 3D，并把 bandwidth、power、thermal、warpage、test、yield 与供应链放在同一个系统边界。

## 1. 先告诉我为什么需要它

单颗 die 同时受 reticle、defect yield、design complexity、I/O perimeter、power delivery 与 thermal 限制。AI 系统又希望把大 compute silicon、多堆 HBM、I/O dies 与高速 links 放得更近。Advanced packaging 通过 interposer、RDL、bridge、TSV、microbump 或 hybrid bonding 把多个 dies 组合为一个高带宽系统。

它不是“把芯片粘在一起”。Package 必须完成 mechanical support、power delivery、signal routing、heat removal、die protection、test access 与 board connection。更密 integration 会减少 data-movement energy，却把更多已知良品投入一次昂贵 assembly，形成 package-level yield 与 capacity risk。

## 2. 一句话直觉

**Advanced packaging 用更短、更宽的 die-to-die wires 延伸 silicon system，但每缩短一段 wire，都可能增加 alignment、warpage、thermal、test、yield 和供应协调难度。**

## 3. 系统 cross-section

~~~mermaid
flowchart TB
  COOL[Cold plate / heatsink] --> TIM[TIM + lid]
  TIM --> C1[Compute die]
  TIM --> C2[I/O or compute chiplet]
  H1[HBM stack] <--> INT[Interposer / RDL / bridge]
  C1 <--> INT
  C2 <--> INT
  INT --> SUB[Organic substrate]
  SUB --> BGA[BGA to board]
  VRM[Board VRM] --> BGA
~~~

## 4. 前置知识

Wafer、die、reticle、defect density、yield、bump、RDL、substrate、TSV、impedance、IR drop、thermal resistance、coefficient of thermal expansion、known-good-die 与 design-for-test。

## 5. 第一性原理：为什么 die 要分开

大 die 可以用 on-die wires 获得高带宽和低 latency，却可能受到 reticle 与 defect yield 影响。拆成 chiplets 可让 compute、I/O、analog 或 cache 使用不同 process，并提高 design reuse；但 die-to-die interface 比 on-die wire 更耗能、更慢，并需要 protocol、PHY、bump、routing 与 test。

核心问题不是“chiplet 是否更先进”，而是：

[
Value_{system}=Good assemblies 	imes Performance - Package cost - Test cost - Failure cost
]

任何只比较 die yield、不比较 assembly yield、known-good-die、package cost 与 repairability 的结论都不完整。

## 6. Follow the Data

~~~mermaid
flowchart LR
  CORE[Compute tile] --> PHY[D2D PHY]
  PHY --> BUMP[Microbump / hybrid bond]
  BUMP --> ROUTE[Interposer / RDL / bridge]
  ROUTE --> MC[Memory or I/O die]
  MC --> HBM[HBM stack]
~~~

Die-to-die bandwidth 来自 many short wires；实际 delivered bandwidth 还受 interface efficiency、clocking、repair lanes、routing congestion、thermal throttling 与 software placement 影响。

## 7. Architecture alternatives

| 方案 | Connectivity | 优势 | 主要代价 |
|---|---|---|---|
| Monolithic | on-die metal | latency/energy 最优、单一设计 | reticle、yield、process compromise |
| Organic MCM | substrate traces | 成熟、低成本、大尺寸 | pitch/routing density 较低 |
| Silicon interposer | fine-pitch silicon routing | HBM/wide I/O、高密度 | cost、area、yield、capacity |
| Embedded bridge | local silicon bridge | 高密局部连接、少用整片 interposer | placement/routing/test |
| RDL fan-out | redistribution layers | 大 package、灵活 routing | warpage、layer/yield control |
| 3D stacking | vertical bonds/TSV | 极短 links、高 density | heat、test、bond yield |
| Hybrid bonding | fine-pitch direct metal/dielectric bond | 更高密、更低 parasitic 潜力 | surface quality、alignment、KGD |

## 8. Interposer、RDL 与 bridge

Silicon interposer 提供精细 routing 和 TSV，可连接 compute dies 与 HBM；RDL 在 mold/wafer/panel 上重布线，避免整片厚 silicon；embedded bridge 只在需要高密连接的位置放 silicon。三者不是简单世代关系，而是 routing density、package size、cost、warpage、power delivery 与 capacity 的不同解。

[Primary Source] TSMC 将 CoWoS-S、CoWoS-R、CoWoS-L 分别描述为 silicon interposer、RDL interposer 与 local silicon interconnect 路线；这证明 design space 分叉，而非只有一种“最佳封装”。

## 9. Microbump 与 Hybrid Bonding

Microbump 通过 solder-based joints 建立垂直连接，工艺成熟但 pitch、parasitic 与 bump height 有限制。Hybrid bonding 让 dielectric 与 metal 接合，可缩小连接 pitch、降低 parasitic，并支持更高 density；它要求更平整洁净表面、精密 alignment、die handling 与严格 defect control。

更细 pitch 的意义不是“数字越小越好”，而是每毫米可放更多 links、降低每 link data rate 或缩短 wires；代价是 inspection、repair 与 yield sensitivity。

## 10. 2.5D 与 3D

2.5D 把 dies 并排放在高密 routing layer 上，heat sources 较容易分别接触冷却面。3D 把 active dies 垂直堆叠，wire 极短且 footprint 小，但上层/下层 heat path、power delivery、test access 与 thermal coupling 更难。

3D 的问题往往不是能否 bonded，而是组合后能否供电、散热、测试并长期可靠运行。

## 11. Power Delivery

Current 从 board VRM 经 BGA、substrate planes、bumps 与 on-die grid 到 transistor。更多 dies 与 HBM 增加 current、瞬态与 routing contention；signal routes、power vias 和 thermal structures争夺有限 package area。

Voltage droop 近似受路径 impedance 与 current transient 共同决定：

[
Delta V approx I R + Lrac{dI}{dt}
]

Package architecture 因此会限制 boost frequency、simultaneous switching 与 usable compute，不只是“承载芯片”。

## 12. Thermal 与 mechanical coupling

不同材料的 coefficient of thermal expansion 不同。Large package 经 reflow 与运行温度循环会 warpage，影响 bump contact、underfill、lid 与 board assembly。Compute die、HBM 与 optical/electrical I/O 也有不同温度偏好。

降低 one-die thermal resistance 不代表整 package 更冷；heat spreading、neighbor heating、cooling contact、pump/fan power 和 mechanical pressure 必须共同验证。

## 13. Known-Good-Die 与测试

在 assembly 前筛出 defective dies 可避免把坏 die 与昂贵良品一起封装。但裸 die 的高速 I/O、thermal corner 与 full-system interaction 不一定能完全在 wafer probe 覆盖。Package 后仍需 structural test、link training、memory test、burn-in 与 system stress。

Diligence 要问 test coverage 与 escape rate，而不只是“每颗 die 都测过”。

## 14. 为什么不做一颗更大的 Monolithic Die？

On-die connectivity 最好，但大 die 受到 reticle、defect exposure、design schedule、mask cost 与 process mixing 限制。Chiplet 还能复用 I/O/cache tile 并组合不同 SKU。不过若 interface overhead 高、package yield 低或 workload 无法利用 modularity，小 die 不一定更便宜。

## 15. 为什么不把所有东西都 3D 堆叠？

Vertical link 很短，但 heat 必须穿过其他 dies/adhesives，power 与 test access 更困难，任何 bond defect 都影响更昂贵的 stack。Memory-on-logic、cache-on-compute 与 logic-on-logic 的 power density 不同，不能用同一结论。

## 16. 为什么不只看 Die Yield？

Package 的 good output 取决于所有 dies、bonds、routing、substrate、assembly 与 test。Die yield 提高可能被更多 interfaces 与 assembly steps 抵消。还要计入 capacity、cycle time、scrap value、rework 与 field reliability。

## 17. 为什么不统一一种 Chiplet Interface？

开放 interface 有利于 ecosystem 与 reuse，但不同场景在 bandwidth density、latency、coherence、reach、power、clock 与 security 上需求不同。标准 PHY/protocol 也不能自动解决 mechanical stack-up、thermal、power delivery、KGD 与 business liability。

## 18. 量化例：从 die yield 到 package yield

[Estimate] 假设一个 package 使用四颗 compute chiplets，每颗筛选后可用率为 (0.95)，四条关键 assembly interface 每条成功率为 (0.995)，其他 substrate/assembly 合格率为 (0.97)。若暂以独立事件近似：

[
Y_{package}=0.95^4	imes0.995^4	imes0.97approx0.77
]

这不是实际工厂预测，因为 defect correlation、repair、binning、test escapes 与 rework 都被忽略；它只说明“单颗 die yield 很高”仍不等于 final package yield 高。Package economics 应按 good assemblies，而不是 started dies 计算。

## 19. Manufacturing flow

1. Fabricate and wafer-test each die type。
2. Thin、dice、inspect 并建立 known-good-die inventory。
3. Fabricate interposer/RDL/bridge 与 organic substrate。
4. Pick-and-place、bond、underfill、mold 或 lid attach。
5. Assemble HBM 与其他 components。
6. Electrical/optical structural test、burn-in 与 system test。
7. Bin、traceability、failure analysis 与 shipment。

Multi-vendor flow 会增加 handoff、cycle time 与 blame allocation；capacity 可能由最稀缺一步而非最昂贵 die 决定。

## 20. Workload mapping

- Dense training 重视 HBM bandwidth、all-reduce links 与 sustained thermal。
- Decode 重视 HBM capacity/bandwidth、power efficiency 与 fleet serviceability。
- Chiplet cache 适合对 locality 敏感且能容忍 die boundary 的 workload。
- I/O die 可复用 SerDes 与 memory controllers，但可能成为 centralized bottleneck。
- 3D logic 对 bandwidth density 有吸引力，却必须验证真实 duty cycle 下 thermal throttling。

## 21. Second-order effects

封装缓解 reticle 和 memory wall 后，bottleneck 可能迁移到 HBM supply、substrate/interposer capacity、bonding tools、test time、cold plate、board warpage 或 package-level yield。Chiplet modularity也可能增加 SKU/inventory complexity；更高 integration 会提高 failure blast radius。

## 22. Engineer language decoder

| 工程师说法 | 应翻译成 | 追问 |
|---|---|---|
| “reticle-busting” | system silicon 超出单 exposure 可实现范围 | routing/package 如何跨越边界？ |
| “known-good-die” | 已通过哪些 pre-bond tests | 高速 I/O 与 thermal corner 覆盖吗？ |
| “yield benefit” | die、assembly 还是 final tested yield | 是否按 good package cost 比较？ |
| “hybrid-bond ready” | process demo、qualified flow 或 volume | pitch、alignment、defect distribution？ |
| “heterogeneous integration” | 哪些 process/dies 被组合 | interface、power、thermal 与责任如何分割？ |

## 23. 常见误解

1. **Chiplet 一定降低成本。** 只有 good-package economics 支持时成立。
2. **Interposer 是被动且简单的。** Routing、TSV、power、yield 与 test 都关键。
3. **Package 不影响 performance。** IR drop、signal loss 与 thermal throttling 会改变可用性能。
4. **更细 bond pitch 自动带来更高 bandwidth。** PHY、routing、clocking 与 workload 必须跟上。
5. **先进封装只是 foundry 后段。** Memory、substrate、OSAT、equipment、test 与 cooling 都进入关键路径。

## 24. Product 与技术 grounding

- [Primary Source] [TSMC CoWoS](https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/cowos.htm) 说明 silicon interposer、RDL 与 local silicon interconnect 的并行路线。
- [Primary Source] [TSMC SoIC](https://www.tsmc.com/english/dedicatedFoundry/technology/SoIC_inDepth) 描述其 3D silicon stacking 与 bonding integration。
- [Primary Source] [Intel Foundry Advanced Packaging](https://www.intel.com/content/www/us/en/foundry/packaging.html) 描述 EMIB、Foveros 与相关 assembly/test 平台。
- [Vendor Claim] 各厂商的 density、power、yield 与 roadmap 指标只有在 process、test vehicle、volume status 和 system boundary 可比时才应横向比较。

## 25. Engineering → Strategy 与 Diligence

Advanced packaging 把竞争从单颗 die 扩展为 co-design 与 capacity orchestration。Moat 可能来自 interposer/RDL design rules、bonding recipe、thermal solution、KGD/test data、HBM qualification 与 ecosystem，而不只来自专利。供应风险也从 wafer starts 扩展到 substrates、memory、tools、assembly、test 和 cooling。

尽调应问：

1. Package 中每种 die、memory 与 substrate 的供应来源？
2. Critical yield loss 发生在 wafer、bond、routing、assembly 还是 test？
3. Reported yield 的 denominator 是什么？
4. Package power/thermal simulation 与 production telemetry 如何关联？
5. Warpage、temperature cycling 与 field reliability 如何验证？
6. 哪些 dies 真正 known-good，哪些 failure 只能 post-package 发现？
7. Capacity bottleneck 对应哪台 tool、哪道工序与 qualification lead time？
8. Interface 是否支持 repair lanes、redundancy 与 graceful degradation？
9. Good-package cost 如何处理 scrap、rework、binning 与 inventory？
10. Second source 是否共享相同 design rules 与 test flow？

## 26. 小结与延伸

Advanced packaging 是 architecture，不是装配附件。它同时决定 die partition、HBM、I/O、power、thermal、yield、capacity 与最终 economics。最佳方案总是 workload 与 manufacturing system 的联合最优，而不是 interconnect density 单点最优。

下一步阅读 [Chiplet & 3D](../17_chiplet_3d_integration/index.md)、[Power Delivery](../18_power_delivery/index.md)、[Thermal & Cooling](../19_thermal_cooling/index.md) 与未来的 Modern AI Rack。

## Sources

- [TSMC — CoWoS](https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/cowos.htm)
- [TSMC — SoIC](https://www.tsmc.com/english/dedicatedFoundry/technology/SoIC_inDepth)
- [Intel Foundry — Advanced Packaging](https://www.intel.com/content/www/us/en/foundry/packaging.html)
