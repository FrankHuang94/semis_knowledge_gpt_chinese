# Pluggable、LPO 与 CPO：Optical I/O 应该放在哪里？

## 1. 问题从哪里来

Switch ASIC 的 aggregate bandwidth 与 SerDes lane rate 上升后，ASIC 到 front-panel module 的 PCB electrical channel 更难维持 signal margin。更强 DSP、equalization、retimer 和 low-loss material 可以延长 reach，却增加 power、latency、cost 与 thermal。Optical architecture 的核心问题因此不是“要不要光”，而是在哪里完成 retiming、electrical-to-optical conversion、laser 与 service boundary。

## 2. 三种位置

~~~mermaid
flowchart LR
  subgraph P[Retimed Pluggable]
    A1[Switch ASIC] --> E1[Long PCB SerDes] --> D1[Module DSP] --> O1[Optical engine]
  end
  subgraph L[Linear Pluggable / LPO]
    A2[Switch ASIC DSP/SerDes] --> E2[Controlled PCB] --> O2[Linear optical module]
  end
  subgraph C[Co-Packaged Optics]
    A3[Switch ASIC] --> E3[Very short electrical] --> O3[Co-packaged optical engine] --> F3[Fiber]
  end
~~~

Retimed pluggable 把 module 做成较独立的 electrical receiver/transmitter：host channel 的 distortion 由 module DSP/retimer 恢复，再驱动 optics。它有成熟 faceplate service model 和 multi-vendor ecosystem，但 host SerDes 与 module DSP 可能重复部分处理。

LPO 移除或简化 module 内 DSP，让 host ASIC 的 linear electrical output 直接驱动 optical components，降低 module power/latency，却把 end-to-end analog channel、calibration 与 interoperability 责任推给 switch + module co-design。

CPO 把 optical engine 放到 switch ASIC 邻近 package，显著缩短 high-speed electrical trace。OIF 已发布 co-packaging framework 与 3.2 Tb/s co-packaged module Implementation Agreement，[Primary Source] 说明机械、electrical、optical、management 与 interoperability boundary 都需要共同定义。

## 3. Follow the Signal

Retimed pluggable 的 bit 经 ASIC SerDes、package、PCB、connector 进入 module DSP，再经过 driver、modulator、fiber、photodiode 与 receiver。LPO 仍走 front panel，但 host 到 module 的 linear channel margin 更紧。CPO 则在 package 邻近完成 E/O，front panel 主要处理 fiber connector，不再让每个 lane 的最高速 electrical signal 走完整 PCB。

缩短 electrical reach 可以减少 insertion loss、reflection 与 equalization，但不会消除 laser、modulator、photodiode、fiber attach、thermal、test 和 control。瓶颈从 board signal integrity 移到 photonic packaging、fiber routing、optical engine yield 与 field service。

## 4. Design space

| 维度 | Retimed pluggable | LPO | CPO |
|---|---|---|---|
| Electrical reach | 较长，由 DSP 恢复 | 较长但 margin 紧 | 极短 |
| Module power | 较高 | 较低潜力 | 较低 link power 潜力 |
| Service | 单 module 热插拔 | 单 module 热插拔 | engine 与 switch 耦合 |
| Interoperability | 边界较清楚 | end-to-end SI 更敏感 | package/fiber/laser/management 新边界 |
| Thermal | faceplate module hotspot | DSP power 降低 | optics 靠近高功耗 ASIC |
| Yield/scrap | module 与 switch 分开 | module 与 switch 分开 | expensive components 组合良率 |
| Upgrade | module 可独立替换 | 仍较灵活 | optical generation 与 ASIC 耦合 |

三种方案会长期共存，因为 reach、port count、power budget、field repair、volume 与 vendor capability 不同。OIF 仍同时推进 linear interface、external laser 与 co-packaging，正反映市场不是单一路径。[Primary Source]

## 5. LPO 为什么难

去掉 module DSP 后，host SerDes、PCB、connector、linear driver/modulator 和 receiver 的 variation 必须在系统级闭环。Module 不再把 electrical input 重新判决成干净 bit，host 与 optics 的 transfer function、temperature 和 aging 更直接耦合。

这会提高 switch vendor 的 SI/PI、calibration、firmware 与 qualification责任。Lab 中一组 matched component 工作，不等于 multi-vendor、全温度、全 lane aggressor、connector aging 与 mass-production distribution 都有 margin。LPO 的低 power 价值必须扣除更强 host SerDes、额外 calibration 和可能降低 reach/port flexibility 的代价。

## 6. CPO 为什么诱人

CPO 的主要收益不是“光更快”，而是避免高速 electrical lane 穿过长 PCB。更短 trace 可降低 equalization/retimer 需求，提高 bandwidth density，并可能减少 link flap。Broadcom 已公开 Tomahawk 6 Davisson CPO switch 的 Shipping 状态，[Primary Source] 但一个 vendor/product milestone 不能外推成所有 network 的默认 architecture。

CPO 也允许把 optical engine 按 package 周边排列，并考虑 external laser source：把 laser 放到可维护、热环境较好的位置，再送 light 到 package。代价是更多 fiber attach、connector与 laser-distribution failure mode。

## 7. 为什么不……？

### 为什么不现在全部用 CPO？

Switch ASIC 与 optics 形成更大 failure domain。若一个 optical engine fail，如何 repair、是否能 bypass、是否要更换整台 switch，都会影响 fleet economics。Package assembly/test 也必须避免一个坏 engine 报废昂贵 ASIC。

### 为什么不全部用 LPO？

Linear channel margin、vendor interoperability 与 field variation 可能不够。对较长 reach、复杂 connector 或 broad multi-vendor deployment，retimed module 提供更清楚 boundary。

### 为什么不永远保留 retimed pluggable？

随着 lane rate 与 radix 上升，PCB reach、DSP power、faceplate thermal 与 connector density 越来越昂贵。重复 retiming 的 energy/bit 会侵蚀 system power。

### 为什么不把 laser 也紧贴 ASIC？

Laser 对温度敏感，又是寿命与维修关键器件。外置 laser 可把 heat 与 replacement boundary 分开，但引入 light distribution、connector 与 redundant-source control。

## 8. Worked example：power 不能只算 module

假设 64-port switch 的 retimed optical module 每个 18 W，而 LPO 每个 12 W，[Estimate] module 层节省 384 W。若 LPO 为保持 margin 让 host SerDes 与 cooling 合计多消耗 120 W，[Estimate]，net 节省约 264 W，而不是宣传的 384 W。若 qualification 导致 port reach 或 usable yield下降，还要计入额外 switch、spares 与 operations。

CPO 比较也必须以完整 chassis 为 boundary：ASIC、optical engine、external laser、fans/pumps、control、fiber management 与 redundancy都要计入。单 engine energy/bit 不能直接等于 deployed network TCO。

## 9. Second-order effects

降低 optics power 后，switch radix 可继续上升，于是 single ASIC failure 影响更多 ports；缩短 electrical path 后，package/fiber attach 变成 yield bottleneck；提高 integration 后，供应商控制点从独立 module ecosystem 转向 switch silicon、silicon photonics、advanced packaging 和 system software。

CPO 还改变采购与责任：pluggable 模式下 switch、module 可分别 qualification；CPO 模式下 system vendor 需要承担更大 integrated warranty 与 root-cause responsibility。这可能增加 full-stack vendor moat，也可能让客户担忧 lock-in。

## 10. Engineers actually say

- “We are faceplate-power limited.”：front-panel module 的 power/thermal 限制 port density。
- “The host-to-module margin is gone.”：ASIC 到 pluggable 的 electrical budget 无法继续扩展。
- “It is linear-drive.”：追问是否 LPO、RTLR 或其他 partition，DSP/retiming 在哪里。
- “The laser is external.”：追问 redundancy、distribution loss、connector、service 与 failure containment。
- “CPO is production.”：追问具体 SKU、volume、deployment、field hours 与 repair model，不要把 Announced 混成 Deployed。

## 11. Engineering → Strategy

| 改变 | 系统影响 | 价值转移 | 风险 |
|---|---|---|---|
| Retimed → LPO | module power 降低 | host SerDes/SI 与 system vendor | margin、interoperability |
| Pluggable → CPO | electrical reach 缩短 | silicon photonics/packaging/switch | yield、repair、lock-in |
| External laser | 热与 service boundary 改善 | laser distribution ecosystem | connector与 shared failure |
| Higher radix | switch 数与层级可降 | merchant/custom switch ASIC | blast radius、fiber density |
| Integrated telemetry | root cause 加快 | full-stack vendor | software dependency |

## 12. Diligence questions

1. DSP、CDR、FEC、driver 与 laser 分别在哪里？
2. Power claim 的 boundary 是 module、port、ASIC 还是 chassis？
3. Channel margin 覆盖哪些 board、temperature、aging 与 aggressor？
4. Multi-vendor interoperability 还是 matched solution？
5. CPO optical engine fail 后能否 isolate、bypass 或 field replace？
6. ASIC、photonic die、fiber attach 与 package 的 cumulative yield？
7. External laser 是否有 redundancy，shared failure domain 多大？
8. Fiber routing、cleaning、connector 与 technician workflow 如何变化？
9. Status 是 Announced、Sampling、Shipping 还是 Deployed？
10. 真实 fleet 的 link flap、field hours、repair time 与 spare strategy？

## 13. Takeaways

1. Pluggable、LPO、CPO 的本质是重新选择 retiming、E/O 与 service boundary。
2. LPO 用更紧 system margin 换 module power；CPO 用 integration 换短 electrical reach。
3. 低 energy/bit 必须在完整 chassis 与 operations boundary 下验证。
4. CPO 把 bottleneck 移向 photonic packaging、yield、fiber与 repair。
5. Adoption 取决于 volume、reliability和责任模型，不只技术可行性。

## Primary sources

- [Primary Source] [OIF Implementation Agreements：linear、external laser 与 co-packaging](https://www.oiforum.com/technical-work/implementation-agreements-ias/)
- [Primary Source] [OIF Co-Packaging Framework](https://www.oiforum.com/oif-releases-co-packaging-framework-implementation-agreement/)
- [Primary Source] [OIF current 224G linear-interface work](https://www.oiforum.com/technical-work/current-work/)
- [Primary Source] [Broadcom Tomahawk 6 Davisson CPO shipping announcement](https://www.broadcom.com/company/news/product-releases/63626)
- [Vendor Claim] [Arista NetDL white paper：LPO system positioning](https://www.arista.com/assets/data/pdf/Arista-Netdi-Whitepaper.pdf)


## 基础概念桥接

先区分 wavelength、laser、modulator、fiber、connector、receiver、FEC、link budget 与 reach。能亮不等于长期可运行；温度、污染、老化、校准、现场更换和多供应商验证决定 fleet economics。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。
