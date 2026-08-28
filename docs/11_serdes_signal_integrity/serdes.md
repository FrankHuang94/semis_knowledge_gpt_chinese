---
id: serdes
title: SerDes 与 Signal Integrity：为什么更高速率会换来更小 Margin、更高 Power 与更短 Reach
concepts: [serdes, nrz, pam4, eye_diagram, jitter, equalization, cdr, fec, retimer]
prerequisites: [voltage, impedance, transmission_line, bandwidth, pcie]
level: [2, 3, 4]
status: draft
last_verified: 2026-08-24
source_date: 2026-08-24
---

# SerDes 与 Signal Integrity：为什么更高速率会换来更小 Margin、更高 Power 与更短 Reach

> 第一次阅读：Sections 1–8  
> 第二次阅读：Sections 9–18  
> 深入阅读：Sections 19–26

## 阅读前后

**I should understand before:** voltage/current、impedance、RC、transmission line与binary data。  
**I should understand after:** 能画出TX-channel-RX chain，区分NRZ/PAM4、baud/bit rate、CTLE/FFE/DFE、CDR/FEC、redriver/retimer，并从loss、jitter、BER、eye与reach判断高速I/O claim。

## 1. 先告诉我为什么需要它

若chip之间用宽parallel bus，每增加bandwidth就要更多pins、package traces与simultaneous switching；不同wires的skew让共同clock越来越难。SerDes把低速并行bits序列化到少量高速差分lanes，在另一端恢复clock和data。

代价是：PCB trace、connector、package via与cable在高frequency下像有损filter。Symbol变短、eye变小、reflection/crosstalk/jitter占比上升，必须用equalization、CDR、FEC与更昂贵channel补偿。

## 2. 一句话直觉

**SerDes用时间换pins；速率越高，channel抹掉的高频细节越多，receiver必须花更多analog/digital power猜回原来的symbols。**

## 3. Signal chain

~~~mermaid
flowchart LR
  P[Parallel data] --> PCS[PCS / coding / FEC]
  PCS --> SER[Serializer]
  SER --> TX[Driver + TX FFE]
  TX --> CH[Package + PCB + connector/cable]
  CH --> RX[AFE + CTLE/VGA]
  RX --> CDR[Clock & Data Recovery]
  CDR --> DFE[Sampler + DFE]
  DFE --> DES[Deserializer]
  DES --> DEC[FEC decode / PCS]
~~~

不同协议对PCS/FEC位置与实现不同，但从symbols到electrical waveform再恢复bits的链条相似。

## 4. 前置物理

Transmission line由characteristic impedance、loss、reflection与delay描述。若source/load/trace阻抗不匹配，波会反射。Copper的skin effect与dielectric loss随frequency恶化；via stub、connector与package discontinuity产生notch。Crosstalk把邻lane能量耦合进来。

## 5. NRZ vs PAM4

NRZ每symbol两个levels，携带1 bit；PAM4有四levels，理想每symbol携带2 bits。因此同bit rate下PAM4约用一半symbol rate，缓解channel bandwidth；但四levels只给三个更小vertical eyes，对noise、linearity与jitter更敏感，raw BER通常更差，需要FEC与复杂DSP。

\[
R_{\text{bit}}=R_{\text{baud}}\log_2(M)
\]

[Estimate] 112 Gb/s PAM4的理想symbol rate约56 GBd；实际line rate、coding与FEC依protocol。

## 6. Follow the Data

1. PCS划分blocks/lanes并加入coding/FEC。
2. Serializer按baud输出symbols。
3. TX FFE预加重transitions以抵消channel loss。
4. Channel造成attenuation、ISI、reflection、crosstalk与jitter。
5. RX CTLE提升高频、VGA调幅度。
6. CDR估计sampling phase。
7. Sampler/DFE用past decisions减post-cursor ISI。
8. FEC纠正剩余errors，超出能力则uncorrectable。

## 7. Architecture blocks

| Block | 解决什么 | 代价/风险 |
|---|---|---|
| PLL/clocking | 低jitter时钟 | analog power、spurs |
| Serializer | 并转串 | mux timing |
| TX FFE | precursor/postcursor ISI | swing/power |
| CTLE | 高频loss | noise amplification |
| VGA/AGC | amplitude | settling/linearity |
| CDR | sampling phase/frequency | jitter tracking、latency |
| ADC/slicer | waveform decision | power/area |
| DFE | postcursor ISI | error propagation |
| FEC | residual BER | overhead/latency |
| Lane deskew | 多lane alignment | buffers/latency |
| Training | adapt taps/equalization | startup/interop |

## 8. 关键 parameters

Gb/s、GBd、dB insertion/return loss、Nyquist frequency、TX/RX jitter、eye height/width、COM、pre-FEC BER、post-FEC BER、FEC latency、energy/bit、reach、lanes、PVT margin与test coverage。

## 9. Equations 与 worked example

Decibel voltage ratio：

\[
Loss_{dB}=20\log_{10}\left(\frac{V_{out}}{V_{in}}\right)
\]

[Estimate] 若channel在关键frequency损失20 dB，voltage amplitude约剩 \(10^{-1}=10\%\)。Equalizer可重塑frequency response，却会放大noise，不能创造已丢失的SNR。

Lane aggregation：

\[
BW_{\text{gross}}=N_{\text{lanes}}\times R_{\text{lane}}
\]

Useful bandwidth还需乘coding/FEC/protocol效率。一个“224G SerDes”也必须问它是electrical bit rate、PAM4 lane rate、双向aggregate还是marketing class。

## 10. Bottleneck与症状

Eye闭合可能来自loss、reflection、crosstalk、jitter、power noise或equalization不当；BER waterfall可能在温度/电压/corner失效；link training降速/降宽；FEC corrected errors升高但业务暂时无错，是margin预警；retimer解决reach后可能增加latency、power与failure points。

## 11. Design Space

| 选择 | 优点 | 代价 | 场景 |
|---|---|---|---|
| Wider parallel | 低per-pin speed | pins/skew/routing | 短距on-package |
| NRZ | 大eye、简单 | 高baud | 较低rate/short reach |
| PAM4 | 2 bits/symbol | SNR/FEC/DSP | 56G+ class links |
| Better PCB/cable | less loss | material/connector cost | board/copper reach |
| Redriver | analog boost、低latency | 不重定时、noise累积 | moderate loss |
| Retimer | CDR后重新发送 | power/latency/cost | long/high-loss |
| Optics | long reach/isolation | module/laser/DSP cost | rack间/高rate |

## 12. 为什么最终这样设计

High-volume links选择serial differential signaling减少pins，protocol规定channel budget、training与FEC，使不同vendor在限定loss/BER下interop。Equalization分布在TX/RX，避免任何一端承担全部复杂度；retimer/optics在channel超过direct-attach budget时插入。

## 13. 为什么不……？

### 为什么不直接提高clock？

Unit interval缩短，而channel loss/jitter不同比缩小，margin更差；PLL与I/O power增加。

### 为什么不无限equalization？

CTLE放大noise，DFE会error propagation，TX FFE牺牲main cursor，ADC/DSP耗电；低SNR信息无法免费恢复。

### 为什么不全部用retimer？

每颗增加power、latency、BOM、management与failure rate，并需protocol qualification。

### 为什么不全部换optics？

短距electrical通常成本、latency、serviceability更优；optics还需laser、coupling、thermal、packaging与manufacturing生态。

### 为什么不一直用NRZ？

达到相同bit rate需更高baud，高频loss可能超过channel能力；PAM4用vertical margin换frequency margin。

## 14. Trade-off

~~~mermaid
flowchart LR
  R[Higher lane rate] --> E[Smaller eye / more loss]
  E --> Q[More EQ + FEC]
  Q --> P[More power + latency]
  P --> S[Shorter reach / retimers]
  S --> O[Earlier optics]
~~~

## 15. Second-order effects

SerDes rate上升推动advanced PCB、low-loss copper、connectors、retimers与optics；PHY占switch/accelerator power/area增加；FEC/latency影响scale-up collectives；reach缩短改变rack topology与service model。

## 16. Workload mapping

Training collectives看aggregate BW与tail/reliability；decode disaggregation更敏感latency；storage/NIC看throughput；scale-up需低latency、强reliability；scale-out可接受更多protocol/FEC以换reach；optical I/O试图把electrical boundary拉近die。

## 17. Real product evidence

[Primary Source] Broadcom BCM56980 datasheet展示56.25 Gb/s PAM4/28.125 Gb/s NRZ、TX FIR、RX equalizer与14-tap DFE，说明SerDes不是单一serializer，而是完整mixed-signal adaptation chain。  
[Primary Source] PCI-SIG解释PCIe 6.0因PAM4与FEC采用固定256-byte FLIT。PHY改变会反向改变link-layer framing。  
[Primary Source] IEEE ISSCC公开224 Gb/s PAM4 receiver材料展示高loss compensation与energy/bit研究边界；research demo不等于production reach/yield。

## 18. Evolution

Parallel bus → NRZ SerDes → higher baud/loss → PAM4 + stronger EQ/FEC → retimer density增加 → electrical reach wall → optics向switch/package靠近。

## 19. Engineers actually say

“Channel loss is 30 dB at Nyquist”“eye margin is tight”“DFE is chasing crosstalk”“pre-FEC BER is degrading”“link trained down”“we need another retimer”“the PHY is power-limited”。

## 20. 听到这些话意味着什么

需问完整channel definition、corner与mask；equalizer可能在补非stationary noise；FEC尚能纠错但margin下降；interop或SI导致降档；reach超budget；I/O而非logic开始限制system power。

## 21. 追问工程师

1. NRZ/PAM4、bit rate/baud？
2. Channel insertion/return loss到哪frequency？
3. Package/PCB/connector/cable各贡献？
4. Eye在TX、TP还是RX decision point？
5. Pre/post-FEC BER与target？
6. FEC类型/latency/overhead？
7. TX FFE/CTLE/DFE taps与adaptation？
8. Jitter decomposition与clock source？
9. PVT/aging/crosstalk margin？
10. Retimer数量与hop latency/power？
11. Energy/bit boundary？
12. Compliance vs真实系统channel？
13. Production test time/coverage？
14. Yield/interop field data？

## 22. Common misconceptions

1. Gb/s等于GB/s。
2. PAM4比NRZ“快四倍”——每symbol是2 bits。
3. Eye diagram漂亮就保证系统BER——capture condition与统计深度重要。
4. FEC消除物理问题——它只在correction budget内。
5. Retimer与redriver相同——前者恢复clock/data并重新发送。
6. Optics消除SerDes——optical module仍有electrical/optical serialization与DSP。

## 23. Engineering → Strategy

| Engineering | System | Business | Strategy |
|---|---|---|---|
| Higher rate | fewer lanes/port | denser switch | PHY IP价值 |
| More EQ/FEC | extend channel | power/latency | DSP/retimer需求 |
| Better materials | reach/margin | PCB/connector ASP | supply qualification |
| Reach wall | optics更近 | optical content增加 | CPO/LPO opportunity |
| Strong test/model | yield/interop | faster deployment | data/validation moat |

## 24. Technical Diligence

验证measurement setup、channel model、silicon而非simulation、PVT、BER confidence、FEC margin、energy/bit、reach、package/board、retimer、compliance、production test与field interoperability。Moat通常在analog design、DSP/adaptation algorithms、models、layout、lab data与customer qualification组合。

## 25. 五个 takeaway

1. SerDes用时间与复杂接收机换pins/routing。
2. PAM4降低baud但缩小vertical margin。
3. Equalization、CDR与FEC共同恢复link，均有power/latency代价。
4. Rate上升使reach下降并推动retimer/optics。
5. 评估必须同时看rate、loss、BER、FEC、power、reach与PVT。

## 26. 三个开放问题

224G/更高速率下direct copper的经济reach剩多少？DSP/ADC power何时让optical I/O更优？Chiplet/package内link应选择超宽低速还是serial high-speed？

## Sources

- [Primary Source] [Broadcom BCM56980 Switch/SerDes Datasheet](https://docs.broadcom.com/doc/56980-DS)
- [Primary Source] [PCI-SIG — PCIe 6.0 FLIT, PAM4 and FEC](https://pcisig.com/what-flit-mode-and-why-did-pci-sig-move-unit-data-exchange)
- [Primary Source] [IEEE ISSCC — 224 Gb/s PAM4 Receiver](https://resourcecenter.ieee.org/education/isscc-deep-dives/sscs2023dd0010)
- [Primary Source] [Broadcom BCM81356 PAM4 PHY/Retimer Datasheet](https://docs.broadcom.com/doc/81356-DS2)


## 基础概念桥接

先区分 bit rate、symbol rate、encoding、eye、jitter、noise、loss、equalization 与 BER。channel 是 Tx、package、board、connector、cable 和 Rx 的整体。实验室 compliance、系统 interoperability 和 production test 提供不同证据。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。
