---
id: power_delivery
title: Power Delivery：从 Utility 到 Transistor 的 Voltage、Current、Loss 与 Transient
concepts: [power_delivery, vrm, busbar, pdn, voltage_droop, power_cap]
prerequisites: [voltage, current, resistance, capacitance, modern_ai_rack]
level: [2, 3, 4]
status: draft
last_verified: 2026-08-24
source_date: 2026-08-24
---

# Power Delivery：从 Utility 到 Transistor 的 Voltage、Current、Loss 与 Transient

> 第一次阅读：Sections 1–8  
> 第二次阅读：Sections 9–18  
> 深入阅读：Sections 19–26

## 阅读前后

读前需理解 voltage/current/power、resistance/inductance/capacitance、[Advanced Packaging](../16_advanced_packaging/advanced_packaging.md) 与 [Modern AI Rack](../20_rack_cluster_datacenter/modern_ai_rack.md)。读后应能追踪 utility 到 transistor 的 conversion chain，解释 conduction loss、VRM、PDN、droop、decoupling、redundancy 与 power cap，并把 nameplate power 转成 delivered compute。

## 1. 先告诉我为什么需要它

AI compute 提高 switching density，也提高 current与load transient。Facility提供高压AC，transistor需要低压、稳定、快速响应的多条rails；中间每次conversion、connector、busbar、trace、bump与package都有loss、impedance和failure risk。

Power delivery不是“给芯片足够瓦数”。它要在静态效率、动态voltage margin、redundancy、safety、cost与service之间维持可用rail。供电不足会导致frequency cap、timing error或reset；过度margin则消耗铜、silicon、空间和energy。

## 2. 一句话直觉

**高压适合远距离搬 power，低压适合 transistor；电压逐级下降时 current 上升，因此越靠近 die，conductor、VRM 与 PDN 越容易成为 performance constraint。**

## 3. Power chain

~~~mermaid
flowchart LR
  U[Utility / substation] --> UPS[UPS / generator]
  UPS --> PDU[PDU / busway]
  PDU --> PS[Power shelf / PSU]
  PS --> BUS[DC busbar]
  BUS --> VRM[Board VRM]
  VRM --> PKG[Package PDN]
  PKG --> DIE[On-die grid]
  DIE --> TR[Transistors]
  CTRL[Telemetry / power control] -. cap .-> VRM
~~~

## 4. 前置知识

(P=VI)、(P_{loss}=I^2R)、Ohm’s law、inductance、capacitance、AC/DC、conversion efficiency、power factor、redundancy、thermal derating、load-line与transient response。

## 5. 第一性原理：为什么提高 Distribution Voltage

给定功率 (P)，current为：

[
I=rac{P}{V}
]

Conduction loss为：

[
P_{loss}=I^2R=rac{P^2R}{V^2}
]

提高distribution voltage会降低同功率的current与copper loss，但需要合适的conversion、insulation、connector、protection与safety。越靠近chip，电压必须降低，current急升，physical cross-section与impedance成为约束。

## 6. Follow the Power

1. Grid/substation把power送到facility distribution。
2. UPS/generator处理短时与备用供电。
3. PDU/busway分配到rows/racks。
4. Power shelf/PSU完成AC/DC或DC/DC conversion。
5. Busbar把rack DC送到trays。
6. Board multiphase VRM产生core、HBM、SerDes与aux rails。
7. Package bumps/planes与on-die grid送到switching transistors。
8. Cooling system移除conversion与compute产生的heat。

每一层都要问 input/output voltage、efficiency、headroom、transient、redundancy与telemetry。

## 7. Conversion Efficiency Cascade

若多级conversion efficiencies为 (eta_i)，总效率：

[
eta_{total}=prod_i eta_i
]

单级看似很小的loss会累积并全部变成heat。移除一级conversion可能提高效率，却改变fault isolation、voltage compatibility、hold-up、service与vendor boundary。

## 8. PSU 与 Power Shelf

PSU执行rectification、power factor correction、isolation与regulated output；power shelf组合多个PSUs、current sharing、management与redundancy。Shelf output通过busbar送给payload。

[Primary Source] OCP Open Rack V3 power shelf规范公开了窄范围 (48 	ext{V}) rack distribution及ripple/noise、addressing与connector要求，说明rack power是interface standard而非仅有wattage。

## 9. Busbar 与 Connector

Busbar用大cross-section低阻导体集中分配current，减少独立cables。它仍有contact resistance、hotspot、fault current、arc/safety、segment与service问题。Connector insertion cycles、alignment、contamination与temperature rise都可能比bulk copper更早失败。

## 10. VRM：为什么要 Multiphase

Chip rail低压大电流，单一phase的switch/inductor难以同时满足efficiency与transient。Multiphase VRM交错开关，分担current并提高effective ripple frequency。更多phases增加components、control与area；轻载时可phase shedding提高效率。

VRM位置越接近die，path impedance越低，但占用board/package area并增加local heat。

## 11. PDN 与 Decoupling

Power Delivery Network包含VRM、planes、vias、bumps、package metal、on-die grid与decoupling capacitors。Load突然上升时，远端VRM来不及响应，local caps先供charge。不同frequency范围由不同位置的caps与control loop承担。

目标不是“更多电容”，而是让target impedance在relevant spectrum下满足droop budget，并避免resonance。

## 12. Voltage Droop 与 Load Line

Transient近似：

[
Delta Vapprox IR+Lrac{dI}{dt}+rac{1}{C}int Delta I,dt
]

降低nominal voltage节能，却减少timing/droop margin。Load-line允许voltage随current下降以减少overshoot并配合silicon guardband。Workload power spikes因此可能比average TDP更限制frequency。

## 13. Power Gating、DVFS 与 Cap

Clock gating减少switching，power gating切断idle block leakage，DVFS改变voltage/frequency，rack scheduler可设置power cap。它们把electrical constraint变成software control问题：cap若不理解workload phases，会牺牲job completion；smart scheduling可把不同power profiles错峰。

## 14. 为什么不直接把 Facility Voltage 送到 Chip？

Transistor无法承受facility voltage，board/package也无法以极高voltage直接分配到logic rail。必须conversion与isolation。减少stages有潜在效率收益，但每级同时提供regulation、protection、fault containment与compatibility。

## 15. 为什么不把 Voltage 降到更低？

Dynamic energy近似随 (CV^2) 降低，但frequency/timing、noise margin、variation与droop会恶化。更低voltage为同功率带来更高current，加重IR loss。最佳点由silicon、PDN、workload与cooling共同决定。

## 16. 为什么不给每个 Rack 无限冗余？

冗余提高availability，却增加capital、space、conversion loss与idle capacity。N+1、N+N或shared reserve适合不同failure model。若两个feeds共享上游breaker/controller，形式冗余并不消除共因故障。

## 17. 为什么不按 TDP 配电？

TDP不是精确instantaneous draw，也不覆盖switch、NIC、storage、fans、pumps与conversion loss。实际设计要看peak/transient、diversity、power cap、thermal derating、startup/inrush与failure mode。按平均值配电会在同步phase失败；按所有峰值简单相加又可能过度建设。

## 18. 量化例：Rack Busbar Current 与 Loss

[Estimate] 假设 rack IT load为 (120 	ext{kW})，busbar voltage为 (50 	ext{V})，忽略conversion与冗余，则current约：

[
I=rac{120{,}000}{50}=2{,}400 	ext{A}
]

若完整busbar/contact等效resistance为 (100 muOmega)，conduction loss：

[
P_{loss}=I^2Rapprox576 	ext{W}
]

这是简化估算；实际分支、contact、temperature、current sharing与fault condition必须建模。它说明低压rack distribution为何对毫欧以下的阻抗都敏感。

## 19. Reliability 与 Protection

Breaker/fuse、over-current/over-voltage、grounding、isolation、arc protection、pre-charge与hold-up共同决定fault是否被contain。Telemetry需要采样足够快并可关联到tray/workload。Power shelf、busbar或VRM failure应有明确degraded mode、replace procedure与root-cause data。

## 20. Workload Mapping

Training可能长时间高utilization并有collective-synchronized power phases；decode随batch与traffic波动；MoE造成局部hot experts与network/power bursts；checkpoint/storage产生不同CPU/NIC pattern。Power cap应按useful work/J与SLO，而不是统一frequency削减。

## 21. Second-order Effects

供电能力提高后，bottleneck可能迁移到cooling、package current density、VRM area、facility interconnect、utility queue或deployment permitting。更高rack voltage减少copper，却增加conversion与safety ecosystem；更大power domain提高density，也扩大fault blast radius。

## 22. Engineer language decoder

| 说法 | 应翻译成 | 追问 |
|---|---|---|
| “rack power” | input、IT还是silicon boundary | 含cooling和conversion吗？ |
| “efficient PSU” | 哪个load/voltage/temperature点 | fleet load distribution呢？ |
| “N+1” | 哪一级与何种failure | shared upstream是什么？ |
| “power limited” | utility、PDU、busbar、VRM还是PDN | telemetry如何定位？ |
| “lower voltage” | dynamic energy与timing trade | current/droop如何变化？ |

## 23. 常见误解

1. **Watts只决定电费。** Power同时决定current、copper、VRM、thermal与performance。
2. **高效率spec适用于所有load。** Efficiency curve随load与temperature变化。
3. **更多decoupling一定更好。** Placement、ESR/ESL与resonance关键。
4. **Power cap只减少峰值。** 可能改变latency、throughput与job synchronization。
5. **双路供电没有single point。** Busbar/controller/firmware仍可共因失效。

## 24. Product 与 Standards Grounding

- [Primary Source] [OCP Open Rack V3 Power Shelf](https://www.opencompute.org/documents/ocp-open-rack-v3-power-shelf-rev-1-0-1-pdf) 定义 rack power shelf electrical/mechanical/management边界。
- [Primary Source] [OCP Open Rack Specs](https://www.opencompute.org/wiki/Open_Rack/SpecsAndDesigns) 汇总 busbar、power shelf、connector与monitoring interfaces。
- [Vendor Claim] [NVIDIA rack hardware guide](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html) 展示power shelves、busbar与compute/switch trays的产品级integration；具体power与redundancy需按配置和部署状态核验。

## 25. Engineering → Strategy 与 Diligence

Power architecture影响utility interconnect、copper、PSU/VRM silicon、rack density、cooling与time-to-deploy。价值可迁移到high-voltage distribution、power semiconductors、magnetics、busbar/connectors、telemetry与controls。

尽调应问：

1. Power数字在哪个boundary测量？
2. Peak、average、transient与inrush distribution？
3. Conversion efficiency curve和thermal derating？
4. Rack/row/facility各级headroom与redundancy？
5. Busbar/contact temperature与fault current validation？
6. VRM/PDN droop在真实workload下多少？
7. Power cap对tokens/job time与SLO影响？
8. Telemetry采样、校准与root-cause resolution？
9. Common-mode failure与black-start procedure？
10. Utility/permitting是否比hardware supply更慢？

## 26. 小结与延伸

Power delivery是一条从utility到transistor的impedance、conversion与control chain。系统优化目标不是最低单级loss，而是在真实workload下以安全、可维修和可扩展方式提供最大useful compute。

下一步阅读 [Thermal & Cooling](../19_thermal_cooling/thermal_cooling.md) 与 [Modern AI Rack](../20_rack_cluster_datacenter/modern_ai_rack.md)。

## Sources

- [OCP — Open Rack V3 Power Shelf](https://www.opencompute.org/documents/ocp-open-rack-v3-power-shelf-rev-1-0-1-pdf)
- [OCP — Open Rack Specifications](https://www.opencompute.org/wiki/Open_Rack/SpecsAndDesigns)
- [NVIDIA — Rack Scale Systems Hardware](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)
