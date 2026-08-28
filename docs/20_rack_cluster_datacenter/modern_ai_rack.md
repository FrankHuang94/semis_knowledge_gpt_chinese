---
id: modern_ai_rack
title: Modern AI Rack：为什么机柜已经成为计算机
concepts: [ai_rack, rack_scale_system, busbar, liquid_cooling, cdu, failure_domain, serviceability]
prerequisites: [gpu, hbm, scale_up, scale_out, optics, advanced_packaging]
level: [2, 3, 4]
status: draft
last_verified: 2026-08-24
source_date: 2026-08-24
---

# Modern AI Rack：为什么机柜已经成为计算机

> 第一次阅读：Sections 1–8  
> 第二次阅读：Sections 9–18  
> 深入阅读：Sections 19–26

## 阅读前后

读前需理解 [现代 AI 数据中心](modern_ai_datacenter.md)、[Scale-up vs Scale-out](../12_scale_up/scale_up_vs_scale_out.md)、[Datacenter Optics](../15_optics/datacenter_optics.md) 与 [Advanced Packaging](../16_advanced_packaging/advanced_packaging.md)。读后应能把 rack 当作 compute、network、power、cooling、mechanical、firmware 与 operations 的联合系统，并用可用算力而非 nameplate specs 评价它。

## 1. 先告诉我为什么需要它

当 accelerator 功率、HBM bandwidth 与 scale-up link density持续上升，server 已无法独立决定性能。GPU tray 需要 switch trays、busbar、power shelves、manifold、cold plates、NICs、optics、management 和 rack-level control 才能成为可部署产品。

Rack-scale design 的收益是缩短高速互连、集中供电散热、预验证整套 topology，并把多个 trays 暴露为一个大计算域。代价是 failure blast radius、设施依赖、installation complexity、service coordination 与 stranded capacity。现代 AI rack 因此不是装服务器的柜子，而是一台以机架为机箱的计算机。

## 2. 一句话直觉

**Rack 把 silicon 的 compute density 变成 facility 可接受的电、热、光纤与维修边界；任何一条供应链没有闭环，峰值算力都只是不可持续的 nameplate。**

## 3. Rack 系统图

~~~mermaid
flowchart TB
  GRID[Facility power] --> PDU[PDU / power shelves]
  PDU --> BUS[DC busbar]
  BUS --> CT[Compute trays]
  BUS --> ST[Scale-up switch trays]
  CT <--> ST
  CT <--> NIC[NIC / scale-out network]
  NIC <--> OPT[Optics / fiber]
  CT --> COLD[Cold plates]
  ST --> COLD
  FWS[Facility water] <--> CDU[CDU / heat exchanger]
  CDU <--> MAN[Manifold]
  MAN <--> COLD
  BMC[BMC / rack manager / telemetry] -. control .-> CT
  BMC -. control .-> PDU
  BMC -. control .-> CDU
~~~

## 4. 前置知识

Rack unit、tray、busbar、PSU/PDU、AC/DC conversion、redundancy、scale-up fabric、NIC、leaf/spine、cold plate、manifold、CDU、flow/pressure、thermal resistance、BMC、firmware、availability 与 mean time to repair。

## 5. 第一性原理：rack 的约束方程

Rack usable performance 受最紧资源限制，可抽象为：

[
P_{usable}=min(P_{compute},P_{memory},P_{fabric},P_{power},P_{cooling})	imes A	imes U
]

其中 (A) 是 availability，(U) 是 workload utilization。Compute trays 增加会同时消耗 power、coolant flow、switch ports 与 cable space。若任何共享资源达到上限，再加 accelerator 只会产生 throttling、queueing 或 stranded silicon。

## 6. Follow the Power

1. Facility medium/low-voltage distribution 到 rack input。
2. PDU/power shelf 完成 protection 与 conversion。
3. DC busbar 向 compute 和 switch trays 分配大电流。
4. Board VRM 把 bus voltage 转成 chip rails。
5. Package power network 把电送到 transistor switching。
6. Control plane 监测 current、voltage、temperature 并执行 power cap。

Higher distribution voltage 可减少同功率下 current 与 copper loss，但增加 conversion、safety 与 connector requirements。Rack power architecture 是 efficiency、fault isolation、serviceability 和 facility compatibility 的折中。

## 7. Follow the Heat

1. Transistor switching 与 leakage 变成 heat。
2. Die、TIM、lid 把热传到 cold plate 或 heatsink。
3. Coolant 经 tray hoses/blind-mate connectors 进入 manifold。
4. Rack loop 把 heat 送到 CDU heat exchanger。
5. Facility water loop 把热带到 chiller、cooling tower 或 dry cooler。
6. Fans 仍处理未接液冷的 memory、storage、power 与 management components。

Liquid cooling 不是取消 air cooling。Hybrid rack 常同时存在 liquid loop 与 airflow；pump、fan、water temperature、dew point、water chemistry 和 leak detection 都进入 computing SLO。

## 8. Follow the Data

~~~mermaid
flowchart LR
  HBM1[GPU/HBM] <--> SU[Scale-up fabric]
  SU <--> HBM2[Peer GPU/HBM]
  HBM1 <--> NIC[NIC / RDMA]
  NIC <--> TOR[Leaf / TOR]
  TOR <--> OPT[Optics]
  OPT <--> CLUSTER[Scale-out fabric]
  MGMT[Management network] -. provision / telemetry .-> HBM1
~~~

Rack 内可能同时存在 scale-up、scale-out、storage、front-end 与 out-of-band management networks。它们的 topology、latency、failure policy 与 security boundary 不同；“一张高速网络”不能替代全部功能。

## 9. Compute trays

Compute tray 将 CPUs、GPUs、HBM、NICs、local storage、VRMs、cold plates 与 service connectors 组合成可替换单元。Tray 边界决定 firmware ownership、failure isolation、cable blind mate、weight、technician access 与 spare strategy。

越大的 tray 可减少 connectors，却增加更换时被移除的 good components。越小的 tray 易维修，却增加 cabling、power conversion 和 management endpoints。

## 10. Scale-up switch trays 与 cabling

Rack-scale fabric 用 switch trays 和高密铜缆/背板连接 accelerators。短 copper 可降低 optical conversion power 和 latency，但 bend radius、connector force、routing、airflow 与 installation sequence 都会限制 topology。Switch failure 可能切断多个 compute trays，因此 redundancy、degraded mode 与 partitioning 必须明确。

## 11. Scale-out NIC、Switch 与 Optics

Rack 对外通过 NIC/HCA 和 optics 接入 cluster fabric。Optical ports 可能在 compute trays、dedicated network racks 或 top-of-rack/leaf switches；不同位置改变 fiber count、service path、thermal 和 oversubscription。Nominal NIC bandwidth 必须与 PCIe、GPU direct path、fabric bisection 和 congestion control共同核验。

## 12. Power shelves、Busbar 与冗余

Power shelf 把多个 PSUs 组合并向 busbar 供电；busbar 减少大量独立电源线。冗余不是简单多装一个 PSU：要验证 shared controller、busbar segment、breaker、input feed、firmware 和 current sharing 是否仍是 single point of failure。

Rack power cap 还可能由 utility allocation、row PDU、cable ampacity 或 cooling capacity触发，而不是 PSU nameplate。

## 13. Cold plate、Manifold 与 CDU

Cold plate 必须在有限 pressure drop 下从 hot components 带走 heat；manifold 要均匀分流并允许 tray isolation；CDU 在 facility 与 technology cooling loops 之间换热、泵送、过滤、监测和控制。

Temperature、flow 与 pressure相互作用。提高 flow 可改善部分 heat transfer，却增加 pump power、erosion、vibration 与 pressure risk；降低 supply temperature可增加 cooling margin，却带来 condensation 与 facility energy代价。

## 14. 为什么不继续使用传统 Air Cooling？

Air 简单、成熟且容易维修，但 heat capacity、fan power、noise 与 airflow space 限制高 density。Liquid 可在较小体积搬运更多 heat，并支持 warmer-water heat rejection；它引入 plumbing、leak、water chemistry、commissioning 与 facility retrofit。低密 racks 仍可能以 air 为最优。

## 15. 为什么不把所有网络都放在 Rack 内？

Rack 内 fabric 可降低 latency，但 large cluster 仍需 scale-out。把更多 switches 塞进 compute rack 会争夺 power、cooling、RU 和 service space，并把 network lifecycle 与 accelerator lifecycle 绑定。Dedicated network racks 能独立扩展，却增加 optics、fiber 和 hop distance。

## 16. 为什么不把整 Rack 当作一个不可分割故障域？

Large coherent/scale-up domain 提高 usable memory 与 communication performance，但一个 shared switch、busbar、cooling loop 或 control-plane bug 可能影响更多 accelerators。Partitioning、graceful degradation 与 workload checkpoint 策略必须匹配 failure economics；最大 domain 不等于最佳 availability-adjusted throughput。

## 17. 为什么不追求最高 Rack Density？

Density 减少 floor space 与 cable distance，却提高 power/heat flux、installation weight、fire/safety、maintenance clearance 和 upstream infrastructure concentration。若 facility 无法连续供电散热，或者 technician 更换一次需要更长 downtime，高 density 会降低 delivered compute。

## 18. 量化例：从 IT Power 到热流与可用算力

[Estimate] 假设一个 rack 的 IT load 为 (120 	ext{kW})，其中 (85%) 由 liquid loop 移除，则 liquid heat load 为：

[
Q_{liq}=120 	ext{kW}	imes0.85=102 	ext{kW}
]

若目标 coolant temperature rise 为 (10^circ	ext{C})，以 water-like coolant 的比热近似 (4.18 	ext{kJ/(kg·K)})，所需 mass flow：

[
dot m=rac{102 	ext{kJ/s}}{4.18 	ext{kJ/(kg·K)}	imes10 	ext{K}}approx2.44 	ext{kg/s}
]

这是 first-pass energy balance，不含 flow maldistribution、cold-plate pressure drop、pump curve、water chemistry、altitude、redundancy 与 transient。它说明 rack spec 必须映射到 manifold/CDU/facility capacity，而不是只看 accelerator TDP。

## 19. Availability-adjusted economics

Purchased compute 与 delivered compute 之间有 waterfall：

[
Compute_{delivered}=Peak	imes Software efficiency	imes Fabric efficiency	imes Thermal availability	imes Fleet availability
]

Rack integration 可提高 performance，却可能延长 qualification、deployment 与 repair。应按 tokens、training progress 或 useful work per facility constraint 衡量，而不是只按 accelerators per rack。

## 20. Commissioning 与 deployment

Rack 到达机房后仍需 floor loading、power whip/busway、coolant flush、pressure test、fiber dressing、firmware alignment、network validation、burn-in 与 workload acceptance。Factory-integrated rack 能减少现场组装，却要求运输 shock、tilt、door/elevator、rigging 与 spares提前设计。

“Shipping” 与 “productive deployment” 之间的时间是关键商业指标。

## 21. Firmware、Telemetry 与 Control

BMC、rack manager、switch OS、NIC firmware、CDU controller、power controller 和 cluster scheduler形成一套 distributed control system。传感器需要统一 time、identity 与 topology；否则无法把 GPU throttling 关联到 coolant、power 或 congestion。

Automated remediation 必须避免 control loops 打架：power capping、thermal throttling、job rescheduling 和 network rerouting可能同时反应，造成 oscillation 或扩大故障。

## 22. Engineer language decoder

| 工程师说法 | 应翻译成 | 追问 |
|---|---|---|
| “rack-scale GPU” | 哪些 memory/compute 被何种 fabric 连接 | failure 与 software domain 多大？ |
| “liquid cooled” | 哪些 components、多少 heat fraction | 剩余 air path 与 CDU 边界？ |
| “N+1” | 哪些 components 有冗余 | shared bus/control/manifold 仍会共因失效吗？ |
| “factory integrated” | 哪些 tests 在出厂完成 | site acceptance 还需什么？ |
| “high density” | 每 rack 的 useful work 与 facility demand | deployment/repair 是否变慢？ |

## 23. 常见误解

1. **Rack power 等于 accelerator TDP 总和。** Switch、NIC、memory、fans、pumps 与 conversion loss都存在。
2. **Liquid cooling 消灭了 airflow。** Hybrid components和power shelves仍需 air path。
3. **Scale-up 越大越好。** Software efficiency、failure domain 与 cost决定有效边界。
4. **机柜预集成就能即插即用。** Facility interfaces、commissioning 与 firmware仍需验证。
5. **Peak rack FLOPS 可比较采购价值。** Availability、utilization 与 workload mapping不可缺失。

## 24. Product 与 standards grounding

- [Primary Source] [OCP Open Rack specifications](https://www.opencompute.org/wiki/Open_Rack/SpecsAndDesigns) 提供 rack、busbar、power shelf 与 blind-mate manifold 等公开接口基础。
- [Primary Source] [OCP Project Deschutes](https://ocpprodweb3.opencompute.org/documents/ocp-specification-deschutes-final-2025-09-05-pdf) 展示高密 AI pod 的 CDU requirements 如何成为公开基础设施规范。
- [Vendor Claim] [NVIDIA DGX GB Rack Scale Systems User Guide](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html) 描述 compute trays、NVLink switch trays、passive copper backplane、power shelves、busbar 与 liquid manifolds 的产品级整合；配置与可用性应按部署状态持续核验。
- [Inference] 公开架构说明显示 rack 已成为 accelerator platform 的产品边界，但不同 vendors 的 power、cooling 与 service partition 仍会共存。

## 25. Engineering → Strategy 与 Diligence

Rack-scale integration 把价值从单颗 accelerator 扩展到 switches、copper/optics、power shelves、busbar、cold plates、manifolds、CDU、firmware、installation 和 service。平台 vendor 若控制 reference design 与 qualification，可提高 switching cost；facility/operator 则承担 retrofit、commissioning 与 fleet availability。

尽调应问：

1. Rack 的 power、cooling、weight、floor 与 facility interface envelope？
2. Peak、sustained 与 availability-adjusted workload output分别是多少？
3. Scale-up fabric 允许哪些 degraded modes与partition？
4. PSU、busbar、manifold、CDU与controller的真实failure domains？
5. Liquid loop覆盖哪些 components，剩余 air load是多少？
6. Installation 到 productive workload 的 critical path？
7. Firmware/telemetry能否定位 power、thermal、network与silicon root cause？
8. Field-replaceable unit多大，常见维修需要排空coolant吗？
9. Spares、technician、leak response与rollback procedure是否成熟？
10. Supply constraint在accelerator、switch、optics、power、cooling还是site construction？

## 26. 小结与延伸

Modern AI rack 是 silicon 与 facility 的共同 architecture。最好的 rack 不是 nameplate compute 最大，而是在真实 workload、power、cooling、network、failure 与 service约束下持续交付最多 useful work。

至此 Phase 1 的主链闭环：从 token、compute、memory、I/O、SerDes、network、optics、package，一直追到 rack 的电、热与运维。下一阶段将把每个模块展开为 Core Curriculum，并补齐 [Power Delivery](../18_power_delivery/index.md)、[Thermal & Cooling](../19_thermal_cooling/index.md)、product database 与 quantitative toolkit。

## Sources

- [Open Compute Project — Open Rack Specifications](https://www.opencompute.org/wiki/Open_Rack/SpecsAndDesigns)
- [Open Compute Project — Project Deschutes CDU Specification](https://ocpprodweb3.opencompute.org/documents/ocp-specification-deschutes-final-2025-09-05-pdf)
- [NVIDIA — DGX GB Rack Scale Systems Hardware Guide](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)
- [NVIDIA — Multi-Node NVLink Systems](https://docs.nvidia.com/multi-node-nvlink-systems/index.html)


## 基础概念桥接

先把 rack 当成计算机：compute、memory、network、power、cooling、firmware、controls 与 operations 共同决定 useful work。nameplate 数量不等于 commissioned capacity；安装、验收、故障恢复、spares 与维护窗口必须进入 TCO。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。


## 进阶工程术语桥接

本篇进一步需要掌握：graph lowering、autotuning、ABI、firmware、observability、canary、fault injection 与 blast radius。阅读这些术语时，不只记中英文对应，还要补齐系统位置、正常路径、饱和或失败路径、直接 counter、端到端结果、产品状态和证据等级。若工程会议出现“已解决”“无开销”“已量产”，应立即追问 workload、boundary、configuration、status/date、failure mode 与 falsifier。

延伸阅读：[进阶工程术语手册](../31_glossary/advanced_engineering_terms_handbook.md)。
