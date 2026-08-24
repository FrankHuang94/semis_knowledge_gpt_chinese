---
id: thermal_cooling
title: Thermal 与 Cooling：从 Junction 到 Facility 的 Heat、Flow 与 Reliability
concepts: [thermal, heat_flux, thermal_resistance, cold_plate, manifold, cdu, liquid_cooling]
prerequisites: [power_delivery, advanced_packaging, modern_ai_rack]
level: [2, 3, 4]
status: draft
last_verified: 2026-08-24
source_date: 2026-08-24
---

# Thermal 与 Cooling：从 Junction 到 Facility 的 Heat、Flow 与 Reliability

> 第一次阅读：Sections 1–8  
> 第二次阅读：Sections 9–18  
> 深入阅读：Sections 19–26

## 阅读前后

读前需理解 [Power Delivery](../18_power_delivery/power_delivery.md)、[Advanced Packaging](../16_advanced_packaging/advanced_packaging.md) 与 [Modern AI Rack](../20_rack_cluster_datacenter/modern_ai_rack.md)。读后应能沿 junction、TIM、lid、cold plate、coolant、manifold、CDU 与 facility loop追踪heat，使用thermal resistance与energy balance做first-pass sizing，并判断air、direct liquid与immersion的适用边界。

## 1. 先告诉我为什么需要它

几乎所有进入IT equipment的electric power最终变成heat。若heat不能足够快离开junction，temperature上升会增加leakage、降低timing margin、触发throttling并加速materials aging。AI rack的power density使cooling从设施配套变成silicon/package architecture input。

Cooling不创造算力，但它决定多少nameplate compute能持续运行。更强cooling也不是免费：pump/fan power、pressure、water quality、leak、mechanical stress、facility retrofit与service都进入TCO。

## 2. 一句话直觉

**Heat必须跨过一串thermal resistances并被流体带走；降低其中一个阻力只会把瓶颈移到下一个interface、flow path或facility heat rejection。**

## 3. Heat path

~~~mermaid
flowchart LR
  J[Junction / hotspots] --> DIE[Die]
  DIE --> TIM[TIM]
  TIM --> LID[Lid / heat spreader]
  LID --> CP[Cold plate]
  CP --> TCS[Technology cooling loop]
  TCS --> MAN[Manifold]
  MAN --> CDU[CDU / heat exchanger]
  CDU --> FWS[Facility water]
  FWS --> REJ[Chiller / tower / dry cooler]
~~~

## 4. 前置知识

Heat、temperature、thermal resistance/capacitance、conduction、convection、specific heat、mass flow、pressure drop、dew point、water chemistry、reliability acceleration与control loop。

## 5. 第一性原理：Thermal Resistance

Steady-state temperature rise近似：

[
Delta T=Q R_{	heta}
]

串联path的total resistance近似相加。Hotspot不由average package power单独决定，还取决于spatial heat flux、die size、TIM voids、lid spreading、cold-plate microchannels与coolant temperature。

Transient阶段还需thermal capacitance；短power spike可能被material mass吸收，长sustained workload最终达到steady state。

## 6. Follow the Heat

1. Switching/leakage在transistors产生heat。
2. Heat在silicon内横向/纵向扩散。
3. TIM填充die/lid或lid/cold-plate微观空隙。
4. Cold plate通过solid conduction与fluid convection取热。
5. Coolant沿tray和manifold带走enthalpy。
6. CDU将technology loop与facility loop交换heat并控制flow/temperature。
7. Facility system向环境或可利用热源排放。

任何interface的contact、flow或control异常都可能造成局部throttle，而rack平均temperature仍正常。

## 7. Air Cooling

Air system由heatsink、fans、duct、cold/hot aisle与CRAH/CRAC组成。优势是dry、成熟、易service；限制是低volumetric heat capacity、fan power、noise、filter/pressure与大量space。Airflow bypass、recirculation与cable obstruction会让nominal CFM失去意义。

## 8. Direct-to-Chip Liquid Cooling

Cold plate直接接触CPU/GPU/lid，coolant以更高heat capacity搬运热。它适合高heat flux且保留dry electronics environment；仍需air处理DIMM/storage/VRM/PSU等未接液组件。

Design要同时管理thermal resistance、pressure drop、flow balance、material compatibility、leak detection、quick disconnect与service drain。

## 9. Immersion Cooling

Single-phase immersion把electronics浸在dielectric fluid中，fluid被循环换热；two-phase依靠boiling/condensation搬热。Immersion能消除传统air path并覆盖更多components，却改变materials compatibility、service、fluid aging、connector、fire/environment与vendor warranty。

它不是液冷的单一终点，而是另一套mechanical/operations ecosystem。

## 10. Cold Plate Design

Microchannels提高surface area与heat transfer，但更细channels增加pressure drop、clogging与manufacturing sensitivity。Cold plate要覆盖die hotspot、保持flatness/contact pressure，并与TIM、lid、socket load与package warpage兼容。

Best thermal test还需考虑flow distribution和mounting variation，而不只看ideal lab sample。

## 11. Manifold 与 Flow Balance

Rack manifold把supply分到多trays再汇回return。Parallel branches会因pressure drop差异产生maldistribution；hot tray可能得不到足够flow。Balancing valves、orifices、sensors与control可改善分配，但增加points of failure和commissioning工作。

Blind-mate connector提高service速度，也要验证leak、insertion force、cycles与air ingress。

## 12. CDU 与 Loop Separation

CDU包含heat exchanger、pumps、filters、reservoir、valves、sensors与controls。它隔离technology cooling system与facility water system，使IT侧可使用更低pressure、更洁净、兼容材料的loop，并控制dew point和leak volume。

CDU capacity不能只看thermal nameplate；要看flow、available pressure、approach temperature、redundancy、part-load efficiency与fault response。

## 13. Water Chemistry 与 Reliability

Coolant pH、conductivity、oxygen、particles与biological growth会影响corrosion、erosion、galvanic couples、seal与clogging。Mixed metals需材料兼容性验证。Leak detection既要快速，也要避免false positives导致不必要shutdown。

Cooling reliability是一套fluid maintenance program，不只是采购cold plates。

## 14. 为什么不把 Coolant 温度降到最低？

Lower inlet temperature提高junction margin，但可能需要chiller energy并接近dew point造成condensation。Warmer water可改善facility efficiency与heat reuse潜力，却提高silicontemperature或所需flow/heat-exchanger area。最优点取决于climate、SLO与hardware limits。

## 15. 为什么不无限提高 Flow？

Higher flow通常改善convection并降低coolant temperature rise，但pressure drop和pump power随flow非线性上升，还可能增加erosion、vibration与noise。若bottleneck在TIM或die spreading，提高flow收益很小。

## 16. 为什么不全用 Liquid？

Low-power components与legacy facilities可能用air更便宜、更成熟。Liquid增加plumbing、commissioning、training与failure procedures。Hybrid design能集中处理hot components，同时保留air生态，但需要两套cooling path。

## 17. 为什么不只看平均 Temperature？

On-die hotspots、transient、sensor location与thermal lag使average掩盖局部风险。Reliability与timing由worst junction和duration决定；flow blockage可能先影响单tray。需要spatial、temporal telemetry与workload correlation。

## 18. 量化例：Coolant Flow

[Estimate] 假设需要移除 (100 	ext{kW}) heat，允许coolant升温 (10^circ	ext{C})，以water-like coolant比热 (4.18 	ext{kJ/(kg·K)}) 近似：

[
dot m=rac{Q}{c_pDelta T}
=rac{100 	ext{kJ/s}}{4.18 	ext{kJ/(kg·K)}	imes10 	ext{K}}
approx2.39 	ext{kg/s}
]

这是energy balance下限式估算，不含pump curve、branch imbalance、pressure drop、redundancy、fluid property变化与control margin。

## 19. PUE 与边界纪律

PUE比较facility total energy与IT energy，但不能单独说明tokens/J、water、carbon、availability或thermal margin。提高IT utilization可能改善facility摊销，却增加hotspots与network load。Cooling评价应同时看 facility overhead 与 useful workload output。

## 20. Thermal Throttling 与 Software

Firmware可根据junction、VRM、HBM或coolant sensors限制frequency/power；scheduler可迁移job或错峰。Reactive throttling保护hardware，但会产生tail与synchronized slowdown。Predictive control需要可靠sensors、workload forecast与防止多个loops oscillate。

## 21. Workload Mapping 与 Second-order Effects

Training通常sustained high load；decode更bursty并受traffic；memory-bound workload可能power较低但HBM hotspot仍高；network/optics有不同temperature limits。Cooling解决junction wall后，bottleneck可迁移到pump power、CDU capacity、water availability、facility permitting或serviceability。

## 22. Engineer language decoder

| 说法 | 应翻译成 | 追问 |
|---|---|---|
| “liquid cooled” | 哪些components和heat fraction | 剩余air load？ |
| “cooling capacity” | 在何种supply temp/flow/pressure | redundancy与approach？ |
| “safe temperature” | 哪个sensor、duration与margin | hotspot/junction呢？ |
| “warm-water ready” | 允许的inlet与performance | 是否需要throttle？ |
| “leak proof” | detection、containment与service | field data和failure procedure？ |

## 23. 常见误解

1. **Power 等于需要排出的heat但边界无关。** IT、pump/fan与conversion位置必须区分。
2. **Liquid cooling等于无fan。** Hybrid systems仍有air-cooled components。
3. **低junction温度总是更好。** Facility energy与condensation有trade-off。
4. **最大CDU kW足以sizing。** Flow、pressure与temperature条件同样关键。
5. **一次无泄漏测试证明长期可靠。** Cycling、corrosion、service与aging必须覆盖。

## 24. Product 与 Standards Grounding

- [Primary Source] [OCP Liquid Cooling Cold Plate Requirements](https://www.opencompute.org/documents/ocp-acs-liquid-cooling-cold-plate-requirements-pdf) 讨论cold plate、CDU、TCS/FWS、materials与measurement边界。
- [Primary Source] [OCP Project Deschutes](https://ocpprodweb3.opencompute.org/documents/ocp-specification-deschutes-final-2025-09-05-pdf) 提供高密AI设施CDU requirements与service/labeling框架。
- [Vendor Claim] [NVIDIA rack hardware guide](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html) 展示compute/switch liquid cooling、manifold与air-cooled remainder的hybrid product implementation；具体性能需按配置验证。

## 25. Engineering → Strategy 与 Diligence

Cooling约束决定silicon power、package、rack density、facility site与deployment速度。Value可能迁移到cold plates、quick disconnects、manifolds、CDUs、pumps、heat exchangers、sensors、coolant与operations software。

尽调应问：

1. Thermal数字的boundary与test workload？
2. Junction-to-coolant resistance distribution？
3. Cold-plate pressure drop与manufacturing variation？
4. Rack branches如何flow balance和isolate？
5. CDU capacity对应何种inlet/flow/pressure？
6. Fluid/material compatibility与maintenance interval？
7. Leak detection、containment、shutdown与recovery？
8. Cooling failure下thermal ride-through多长？
9. Facility retrofit、water、permitting与commissioning critical path？
10. Delivered tokens/J和availability是否含pump/fan/chiller？

## 26. 小结与延伸

Thermal & cooling是一条从nanometer hotspot到facility heat rejection的series path。最优设计把silicon、package、rack、fluid与controls共同优化，并按sustained useful work评价。

下一步连接 [Modern AI Rack](../20_rack_cluster_datacenter/modern_ai_rack.md)、未来的 Manufacturing/Supply Chain 与 quantitative rack sizing工具。

## Sources

- [OCP — Liquid Cooling Cold Plate Requirements](https://www.opencompute.org/documents/ocp-acs-liquid-cooling-cold-plate-requirements-pdf)
- [OCP — Project Deschutes](https://ocpprodweb3.opencompute.org/documents/ocp-specification-deschutes-final-2025-09-05-pdf)
- [NVIDIA — Rack Scale Systems Hardware](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)
