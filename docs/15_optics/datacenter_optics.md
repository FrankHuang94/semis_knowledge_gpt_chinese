---
id: datacenter_optics
title: Datacenter Optics：为什么高速 SerDes 最终必须把比特变成光
concepts: [optics, optical_transceiver, pluggable_optics, lpo, cpo, modulator, photodiode]
prerequisites: [serdes, signal_integrity, scale_out, ethernet, switch]
level: [2, 3, 4]
status: draft
last_verified: 2026-08-24
source_date: 2026-08-24
---

# Datacenter Optics：为什么高速 SerDes 最终必须把比特变成光

> 第一次阅读：Sections 1–8  
> 第二次阅读：Sections 9–18  
> 深入阅读：Sections 19–26

## 阅读前后

读前需理解 [SerDes](../11_serdes_signal_integrity/serdes.md)、[Scale-up vs Scale-out](../12_scale_up/scale_up_vs_scale_out.md) 与 [AI Ethernet / RDMA](../13_scale_out_networking/ai_ethernet_rdma.md)。读后应能沿 switch ASIC 到 fiber 的完整链路解释 pluggable、LPO、CPO、direct detection、coherent、DSP、FEC、laser 与 packaging 的取舍。

## 1. 先告诉我为什么需要它

Switch radix 与 lane rate 上升时，electrical channel 的 insertion loss、reflection、crosstalk 与 jitter 更难控制。更强 SerDes、retimer 与 PCB 材料可以延长 reach，却付出 power、latency、area 与成本；铜线也越来越粗重。跨机架、跨机房的数据移动因此把 electrical bits 转成 photons。

光纤不是“没有损耗的高速电线”。系统只是把瓶颈转移到 electrical-optical conversion、laser、modulator、photodiode、TIA、DSP、FEC、connector cleanliness、thermal drift、test、yield 与 field service。

## 2. 一句话直觉

**Copper 擅长短距离可维护连接，fiber 擅长更远距离和更高密度；optical architecture 的本质是决定 conversion 离 switch silicon 多近，以及为 reach 与 margin 支付多少 DSP、power 和制造复杂度。**

## 3. 系统位置

~~~mermaid
flowchart LR
  ASIC[Switch ASIC] --> ES[Electrical SerDes]
  ES --> PCB[Package + PCB channel]
  PCB --> TX[DSP / Driver / Modulator]
  LASER[Laser] --> TX
  TX --> FIBER[Fiber]
  FIBER --> RX[Photodiode / TIA / DSP]
  RX --> HOST[Peer electrical SerDes]
~~~

## 4. 前置知识

Transmission line、PAM4、equalization、CDR、BER、FEC、switch radix、lane、wavelength、attenuation、dispersion、reflection、thermal control 与 link budget。

## 5. 第一性原理：electrical reach wall

Electrical conductor 的 loss 随 frequency、length、材料和 geometry 增加。提高 baud rate 会把更多 signal energy 推向 channel 更难传输的频段；receiver eye 变小，需要 equalization、coding 和更精细时钟恢复。

Optical carrier 在 fiber 中可跨越更长距离，但 conversion 仍需要 electrical signal 驱动 modulator，在另一端把微弱光功率变成 current 并恢复 bits。Link margin 可写成：

[
M=P_{TX}-L_{fiber}-L_{connector}-L_{coupling}-P_{RX,required}
]

Margin 不是免费冗余：提高 launch power、降低 receiver sensitivity、减少 connector 或增强 DSP 都有 power、cost、reliability 或 manufacturability 代价。

## 6. Follow the Data：一个 packet 如何变成光

1. Switch packet engine 完成 lookup、queueing 与 scheduling。
2. MAC/PCS 做 framing、lane distribution 与 FEC。
3. Electrical SerDes 输出高速 waveform。
4. Transceiver DSP 可均衡并重新定时；driver 控制 modulator。
5. Laser 提供 optical carrier，modulator 把 data 映射到光强或相位。
6. Fiber、connector 与 mux/demux 传输不同 wavelengths。
7. Photodiode 把 photons 转成 current；TIA 放大。
8. DSP/CDR/FEC 恢复 bits，再进入远端 switch 或 NIC。

任何一个 block 的 margin、thermal 或 yield 不足，都能让“端口已点亮”与“长期低错误运行”成为两回事。

## 7. Transceiver architecture

| Block | 保存/改变什么 | 主要约束 |
|---|---|---|
| Laser | 提供 carrier | efficiency、linewidth、aging、thermal |
| Modulator | 把 electrical data 写到光上 | drive voltage、loss、linearity |
| Mux / demux | 合并或分离 wavelengths | insertion loss、alignment |
| Fiber / connector | 传输与连接 | loss、dispersion、contamination |
| Photodiode | 光转电流 | responsivity、bandwidth、noise |
| TIA | 放大微弱 current | noise、gain、linearity、power |
| DSP / CDR | equalize、retime、recover | power、latency、algorithm |
| FEC | 用 redundancy 修正错误 | overhead、latency、coding gain |

## 8. Direct detection 与 coherent

Intensity modulation/direct detection 主要检测光功率变化，architecture 较简单，适合常见 datacenter reach。Coherent receiver 结合 local oscillator 与 DSP 恢复 amplitude、phase 和 polarization，能提高 spectral efficiency、容忍 dispersion 并支持更长 reach，却增加 optics、DSP、power 与 calibration。

[Primary Source] OIF 的 800ZR Implementation Agreement 面向相干可互操作接口，并把特定 DCI reach、form factor 与 FEC/profile 写成实现约束；它不能直接推出所有 datacenter links 都应 coherent。

## 9. Pluggable optics

Pluggable module 把 laser、modulator、receiver 与大量 conversion electronics 放在 faceplate 可插拔模块中。优势是 standards、multi-vendor qualification、field replacement 与故障隔离；代价是 ASIC 到 faceplate 的 electrical trace、front-panel density、airflow 与 module thermal。

它不是落后方案，而是 serviceability 与 ecosystem 的强组合。许多架构争论不是“谁的 physics 最先进”，而是“谁承担 field failure 与 inventory complexity”。

## 10. LPO：Linear Pluggable Optics

LPO 尝试删除 transceiver 内完整 retiming DSP，让 host SerDes 通过线性 analog path 驱动 optics。潜在收益是更低 power 与 latency；代价是 electrical-optical channel 共同进入 host equalization budget，link margin、interoperability、test 与 vendor partition 更困难。

“少一个 DSP”不等于“少所有 DSP”。Switch SerDes、FEC、monitoring 与控制仍存在；系统需要证明不同 hosts、modules、temperatures 和 aging conditions 下的 end-to-end margin。

## 11. CPO：Co-Packaged Optics

CPO 把 optical engines 放到 switch package 附近，显著缩短最高速 electrical trace。它能缓解 PCB reach 与 front-panel density，但把 laser distribution、fiber attach、thermal isolation、package yield、test、repair 与 supply chain 放进同一系统。

~~~mermaid
flowchart TB
  P[Pluggable: ASIC → long electrical → module] --> S[更易维护 / electrical power较高]
  L[LPO: ASIC → linear module] --> M[更低DSP power / margin耦合]
  C[CPO: ASIC → short electrical → optical engine] --> I[最高integration / service复杂]
~~~

## 12. 为什么不一直使用 Copper？

Copper 在短 reach、低成本、连接器维护与低 conversion complexity 上仍有优势。问题是 aggregate bandwidth、cable bulk、loss 与 SerDes power 会随 lane rate 和 reach 恶化。正确边界不是“optics 取代 copper”，而是 conversion point 随 system density 向 silicon 靠近。

## 13. 为什么不把所有 DSP 都删掉？

DSP 提供 channel equalization、retiming、monitoring 与 margin separation。删除它能节能，却让 host、module、fiber 与环境成为一个联合 channel；qualification space 变大。若 system vendor 控制全栈，LPO 更可管理；若追求任意互换，retimed pluggable 的责任边界更清晰。

## 14. 为什么不立刻全部使用 CPO？

CPO 的 electrical benefit 不会自动解决 optical attach、laser failure、package yield、field replaceability 与 thermal coupling。Faceplate module 坏了可换 module；co-packaged engine 坏了可能影响更大的 assembly。只有当 saved SerDes power/density 价值超过 manufacturing 与 service penalty，CPO 才形成系统收益。

## 15. 为什么不在所有距离都用 Coherent？

Coherent 的 reach 与 spectral efficiency 来自更复杂 receiver、local oscillator 与 DSP。短距 link 若 direct detection 已有足够 margin，coherent 的额外 power、cost 和 control 未必合理。Architecture 要匹配 reach distribution，而不是追求最复杂 modulation。

## 16. 量化例：从 switch capacity 到 port count

[Estimate] 假设 switch aggregate bidirectional capacity 为 (51.2 	ext{Tb/s})，每个 optical port 提供 (800 	ext{Gb/s}) line rate，则理想端口数：

[
N_{ports}=rac{51.2 	ext{Tb/s}}{0.8 	ext{Tb/s}}=64
]

这只是 front-panel arithmetic，不是 delivered fabric throughput。FEC、protocol overhead、lane mapping、oversubscription、failed lanes 与 traffic pattern 都会降低有效能力。若每端口 optics power 降低，乘以大量端口后才转化为 switch-level thermal headroom；必须用同一 traffic 与 error target 比较。

## 17. Link budget 与 penalty stack

真正设计应把 transmitter optical power、receiver sensitivity、fiber attenuation、connector/splice、mux、dispersion penalty、reflection、aging 与 engineering reserve 放入同一 budget。各团队分别“留一点 margin”可能造成过度设计；完全不留则在 temperature corner 或污染后失败。

## 18. Reliability、test 与 service

Optical failure 不只来自 laser。Fiber bend、dirty connector、coupling drift、TIA saturation、firmware、thermal runaway 与 manufacturing variation 都可能造成 intermittent errors。Diligence 应询问 burn-in、loopback、BER distribution、FEC correction telemetry、field replaceability、spares 和 root-cause partition。

## 19. Workload mapping

- Scale-out collectives 重视 aggregate bandwidth、tail latency 与大量并发 links。
- Storage/front-end network 更重兼容性、reach、cost 与 service。
- Campus/DCI 需要更长 reach，coherent 的价值上升。
- Scale-up optics 若出现，会更关注 latency、power、reliability 与 tight synchronization。
- Sparse MoE traffic 使 oversubscription、burst 与 topology 可能比 nominal optical rate 更重要。

## 20. Second-order effects

Optics 解决 electrical reach 后，bottleneck 可能迁移到 switch radix、fiber routing、connector operations、laser supply、test time、package thermal 或 network software。更低 optical power 也可能允许更多 ports，反而提高整机总功率。提高 lane rate 会减少 fibers/ports，却放大 single-link failure impact。

## 21. Engineer language decoder

| 工程师说法 | 应翻译成 | 追问 |
|---|---|---|
| “DSP-free” | module 内删去哪些 retiming/equalization | host SerDes 与 FEC 还承担什么？ |
| “CPO-ready” | engine、package、laser、fiber attach 到哪一阶段 | prototype、qualified 还是 deployed？ |
| “interoperable” | 在哪个 MSA/IA、test matrix 和 temperature corner | 与哪些 hosts/modules 验证？ |
| “lower power” | 哪个 system boundary 的 energy/bit | 是否含 laser、host SerDes 与 cooling？ |
| “longer reach” | 在何种 fiber、BER 与 FEC 下 | engineering margin 多大？ |

## 22. 常见误解

1. **Fiber 没有 latency。** Propagation、DSP、FEC、queue 与 conversion 都存在。
2. **端口 line rate 等于 application throughput。** Protocol 和 traffic efficiency 不能忽略。
3. **CPO 只是把 module 搬近 ASIC。** 它重写 package、test、laser 与 service boundary。
4. **LPO 等于无 equalization。** Equalization 与 FEC 只是重新分配。
5. **Optical spec 足以预测 fabric。** Topology、routing、congestion 与 failure 更可能决定 job completion time。

## 23. Product 与 standards grounding

- [Primary Source] [OIF Implementation Agreements](https://www.oiforum.com/technical-work/implementation-agreements-ias/) 提供 400ZR、800ZR 等已发布 interoperability profiles。
- [Primary Source] [OIF 800ZR IA](https://www.oiforum.com/wp-content/uploads/OIF-800ZR-01.0.pdf) 定义相干接口的 application、FEC 与 optical requirements。
- [Primary Source] IEEE 802.3 Ethernet standards 定义 PHY/PCS/PMD 边界；实际 module form factor 还常由行业 MSA 约束。
- [Vendor Claim] 任何 LPO/CPO power 或 density 优势都应回到 test conditions、host、reach、FEC 与 system boundary 核验。

## 24. Engineering → Strategy

价值可能从 PCB/retimer 向 silicon photonics、laser、optical DSP、packaging、fiber attach、test 与 network operations 迁移。Pluggable 支持开放模块生态；CPO 可能加强 switch/package/optics 的平台整合与 qualification moat。判断赢家不能只看 component ASP，要看 yield ownership、field failure cost、second source 与谁拥有 end-to-end telemetry。

## 25. Technical Diligence Questions

1. 目标 reach distribution 与 fiber plant 是什么？
2. Power 数字是否包含 host SerDes、laser 与 cooling？
3. Pre-FEC BER distribution 和 post-FEC target 是什么？
4. Worst-case temperature、aging 与 connector loss margin 多大？
5. LPO 如何跨 host/module vendors qualification？
6. CPO optical engine 或 laser failure 如何隔离和维修？
7. 哪些步骤限制 yield、test throughput 与 capacity？
8. Standards compliance 到底覆盖 electrical、optical 还是 management？
9. Telemetry 能否区分 fiber、module、host 与 congestion failure？
10. Delivered cost 是否包含 spares、cleaning、repair 和 downtime？

## 26. 小结与延伸

Datacenter optics 不是单一器件，而是一条从 switch silicon 到 fiber plant 的责任链。Pluggable、LPO 与 CPO 会长期共存，因为它们优化不同的 power、reach、margin、interoperability 与 service boundary。

下一步连接 [Advanced Packaging](../16_advanced_packaging/advanced_packaging.md)、[Modern AI Datacenter](../20_rack_cluster_datacenter/modern_ai_datacenter.md) 与未来的 Modern AI Rack。

## Sources

- [OIF — Implementation Agreements](https://www.oiforum.com/technical-work/implementation-agreements-ias/)
- [OIF — 800ZR Implementation Agreement](https://www.oiforum.com/wp-content/uploads/OIF-800ZR-01.0.pdf)
- [IEEE 802.3 Ethernet Working Group](https://www.ieee802.org/3/)


## 基础概念桥接

先区分 wavelength、laser、modulator、fiber、connector、receiver、FEC、link budget 与 reach。能亮不等于长期可运行；温度、污染、老化、校准、现场更换和多供应商验证决定 fleet economics。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。


## 进阶工程术语桥接

本篇进一步需要掌握：serialization、loss、equalization、FEC、queue、ECN、PFC、retransmission 与 link budget。阅读这些术语时，不只记中英文对应，还要补齐系统位置、正常路径、饱和或失败路径、直接 counter、端到端结果、产品状态和证据等级。若工程会议出现“已解决”“无开销”“已量产”，应立即追问 workload、boundary、configuration、status/date、failure mode 与 falsifier。

延伸阅读：[进阶工程术语手册](../31_glossary/advanced_engineering_terms_handbook.md)。
