# NRZ vs PAM4：每个 Symbol 多装一位，为什么系统反而更难

## 1. 问题不是“调制方式谁更先进”

高速 SerDes受限于 channel loss、package/PCB reach、connector、crosstalk、clock recovery与 energy/bit。最直觉的扩展方式是提高 symbol rate或增加 lanes；但 symbol rate越高，channel高频损耗通常越严重，lane越多又消耗 package perimeter、pins、routing与 optics。

NRZ用两个幅度电平表示一个 bit；PAM4用四个幅度电平表示两个 bits。PAM4在相同 bit rate下可以降低 symbol rate，减轻一部分高频 channel压力；代价是每个眼图的垂直间隔更小，receiver必须区分更多 level，linearity、noise、jitter与 FEC要求提高。

~~~mermaid
flowchart LR
  B[Input bits] --> M{Modulation}
  M -->|NRZ: 1 bit/symbol| N[Two levels]
  M -->|PAM4: 2 bits/symbol| P[Four levels]
  N --> C[Channel loss + noise]
  P --> C
  C --> E[Equalization + CDR]
  E --> F[FEC / BER target]
  F --> D[Recovered bits]
~~~

## 2. Symbol、bit 与 baud必须分开

Bit rate是每秒传递的 bit数；baud是每秒 symbol数。NRZ每个 symbol携带一位，PAM4理想上每个 symbol携带两位。因此同样的 bit rate下，PAM4 baud约为 NRZ的一半。

这并不意味着系统难度减半。PAM4需要三个 decision thresholds和三个 eye openings；transmitter/receiver线性、level mismatch、ISI与 noise都会影响各眼。Gray coding可以让相邻 level错误通常只错一位，但不能消除原始 symbol error。

工程师说“lane speed”时，必须追问是 raw bit rate、baud、编码后 line rate还是 FEC后的 payload。

## 3. 为什么 PAM4的 margin更小

把总幅度归一化为 0到3。NRZ只需区分低和高，理想电平间距为3；PAM4需要区分 0、1、2、3，相邻间距只有1。相同总 swing与 noise条件下，decision margin显著收缩。

[Estimate] 若归一化 noise amplitude为0.25：

- NRZ相邻间距为3，noise占间距约 8%；
- PAM4相邻间距为1，noise占间距 25%。

这只是直觉模型，真实 link还受 transmitter nonlinearity、equalization、jitter、crosstalk、reference noise与 sampling影响。它解释了为什么 PAM4常与更强 DSP、training和 FEC一起出现。

## 4. Transmitter 与 receiver发生了什么变化

NRZ transmitter选择两个 level；PAM4 transmitter需要合成四个更准确的 level，并控制 RLM、rise/fall、pre-emphasis与 jitter。Receiver不再只有一个 slicer threshold，而是需要多 threshold、可能更复杂的 ADC/DSP、CTLE/FFE/DFE与 clock recovery。

Channel本身没有因为 modulation改变而变理想。Package、via、connector、PCB与 cable仍产生 insertion loss、return loss、reflection与 crosstalk。PAM4降低 Nyquist frequency是一项收益，但眼图收缩和 DSP复杂度是交换条件。

## 5. BER 与 FEC为什么进入核心路径

Raw BER描述 FEC前错误；post-FEC BER才接近系统交付的 bit error目标。PAM4较小 margin使 raw error管理更重要，FEC用冗余和 latency换可靠性。FEC不是“免费纠错”：它增加编码开销、block latency、power与 uncorrectable error tail。

分析产品时应同时要求 pre-FEC BER distribution、FEC type、coding gain、latency、post-FEC target与 error telemetry。只给“符合标准”不足以判断在目标 channel、temperature、aging与 manufacturing variation下还有多少 margin。

## 6. 为什么不继续提高 NRZ symbol rate

提高 NRZ baud保留较大的 vertical eye，却把更多能量推向 channel高频区。Insertion loss、skin effect、dielectric loss与 discontinuity变得更严重，equalizer、package与 board要求提高。到某个点，使用更低 baud的多电平 modulation能以较低 lane count达到目标 bit rate。

但转折点依赖 reach、channel material、connector数量、power和 cost。短而优质的 die-to-die channel与长 PCB/cable不应采用相同结论。

## 7. 为什么不使用更多并行 lanes

更多 lanes可保持较低 per-lane rate和较大 margin，却消耗 bump/pin、SerDes macro、package routing、PCB layers、connector与 optics数量。Lane-to-lane skew、clocking、deskew buffer和 yield也会增加。

在 package edge已拥挤的 accelerator/switch上，per-lane rate是重要 scaling lever；在低成本、短 reach系统里，更多较慢 lanes可能更容易验证。正确指标是 aggregate bandwidth除以 package area、power、cost与 failure exposure。

## 8. 为什么不直接上 PAM8或更高阶

更高阶 PAM每 symbol携带更多 bits，但相邻 level更密，linearity、SNR、DSP与 FEC负担继续上升。若为了恢复 margin而提高 swing、power或使用复杂 ADC，系统收益可能消失。制造测试与 channel qualification也会更难。

调制阶数不是技术进步刻度，而是 channel、CMOS、DSP、package与 power共同优化的结果。某一代选择 PAM4，不代表下一代必然 PAM8；更高 baud、更多 lanes、coherent optics或 parallel optical I/O都可能竞争。

## 9. Equalization不能创造信息

FFE、CTLE与 DFE可以补偿可预测的 frequency response或已检测 symbol造成的 ISI，但会放大 noise、受 tap数量和 adaptation限制。CDR恢复 sampling phase，也无法消除所有随机 jitter。若 channel存在深 notch、严重 reflection或串扰，equalizer可能没有足够 margin。

因此 channel设计必须在 silicon前完成 statistical eye、COM或等价分析，并用 package/board/cable模型覆盖 PVT。Post-silicon tuning是收敛工具，不是替代物理设计。

## 10. 一个 end-to-end link budget

[Estimate] 假设 transmitter、package、board、connector与 receiver的 margin penalty分别为 0.15、0.20、0.25、0.10、0.15 个归一化单位，总 penalty为0.85。若初始 eye margin为1.00，只剩0.15。

把 board material改善使 penalty从0.25降到0.15，margin变0.25；增加更强 FEC可能改善交付 BER，却不增加 analog eye。这个 waterfall帮助决定钱应花在 silicon DSP、package、board、retimer还是 FEC，而不是只责怪“SerDes不够好”。

## 11. Product reality：如何读“某代 SerDes”

[Primary Source] IEEE 802.3工作组的公开技术材料记录了高速 Ethernet PMD对 NRZ、PAM4、reach与 power的权衡。看到产品写“PAM4 SerDes”时应追问：

1. Raw bit rate与 baud分别是多少？
2. Electrical reach与 target channel loss？
3. Package/board/connector reference channel？
4. Pre-FEC与 post-FEC BER target？
5. FEC overhead、latency与 telemetry？
6. Tx/Rx equalization能力与 training过程？
7. Power按 lane、PHY还是包含 FEC？
8. PVT、aging与 manufacturing margin？
9. 与 optics接口边界在哪里？
10. 实测 silicon还是 simulation？

## 12. Second-order effects

1. PAM4降低 baud，却提高 ADC/DSP、FEC与测试复杂度。
2. 更强 FEC改善可靠性，却增加 latency和 power。
3. 更高 lane rate减少 lanes，却让 retimer或 optics更早进入系统。
4. Equalization增强可延长 reach，也可能放大 noise并增加 adaptation时间。
5. 更小 margin提高 package、connector与 board供应商的 qualification价值。
6. Link power增加后会影响 switch faceplate、rack thermal与 port economics。
7. BER tail变差会从 physical layer传导到 transport retransmission和 collective stall。

## 13. Engineers actually say

- “PAM4 doubles the bandwidth.”：问是在相同 baud、lane和 overhead下的 raw rate，还是 payload。
- “The eye is open.”：问 statistical eye、BER contour、PVT与 sample size。
- “FEC cleans it up.”：问 pre-FEC distribution、latency和 uncorrectable tail。
- “The channel is within spec.”：问完整 topology、connector、via与 model correlation。
- “Equalization will recover it.”：问 noise enhancement、tap范围和 adaptation。
- “We can just add lanes.”：问 package perimeter、routing、skew、power与 optics count。

## 14. Engineering → Strategy

| 变化 | 获得 | 付出 | 价值迁移 |
|---|---|---|---|
| NRZ提高 baud | 简单 levels | 高频 loss | board/package材料 |
| 转向 PAM4 | 每 symbol更多 bits | margin/DSP/FEC | SerDes IP、DSP、test |
| 更多 lanes | 较低 per-lane难度 | pins/routing | packaging |
| 更强 FEC | 更低 post-FEC error | latency/power | codec IP |
| Retimer加入 | 重建 signal | cost/power/管理 | retimer vendor |
| 光学边界前移 | 更长 reach | optics制造 | optical ecosystem |

## 15. Technical diligence questions

1. Link budget按哪些 component分解？
2. Raw rate、baud、payload与 aggregate如何换算？
3. Pre-FEC BER在 channel、temperature与 aging corner下的分布？
4. Equalizer training需要多久，失败如何恢复？
5. Retimer、redriver或 optics是否进入 BOM？
6. Power与 latency按哪个 boundary报告？
7. Channel model与测量 correlation如何？
8. Production test覆盖哪些 pattern与 margin？
9. Field telemetry能否看到 error trend而不只 link-down？
10. 下一代 rate会把 bottleneck移到 package、board还是 optics？

## 16. Takeaways

1. NRZ与 PAM4交换的是 symbol rate和 signal margin，不是简单的新旧替代。
2. PAM4每 symbol携带更多 bits，却需要更强 linearity、DSP、FEC与测试。
3. Equalization与 FEC能管理损伤，不能取消 channel physics。
4. 选择必须同时优化 lane count、reach、power、package、BER与 cost。
5. 调制变化会把价值推向 SerDes IP、test、retimer、board与 optics。

## Primary sources

- [Primary Source] [IEEE 802.3 Ethernet Working Group](https://www.ieee802.org/3/index.html)
- [Primary Source] [IEEE P802.3bs 400GbE Task Force public materials](https://www.ieee802.org/3/bs/public/14_11/index.shtml)
- [Primary Source] [PCI-SIG：PCI Express Base specifications](https://pcisig.com/specification-overview/pci-express-base)


## 基础概念桥接

先区分 bit rate、symbol rate、encoding、eye、jitter、noise、loss、equalization 与 BER。channel 是 Tx、package、board、connector、cable 和 Rx 的整体。实验室 compliance、系统 interoperability 和 production test 提供不同证据。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。


## 进阶工程术语桥接

本篇进一步需要掌握：serialization、loss、equalization、FEC、queue、ECN、PFC、retransmission 与 link budget。阅读这些术语时，不只记中英文对应，还要补齐系统位置、正常路径、饱和或失败路径、直接 counter、端到端结果、产品状态和证据等级。若工程会议出现“已解决”“无开销”“已量产”，应立即追问 workload、boundary、configuration、status/date、failure mode 与 falsifier。

延伸阅读：[进阶工程术语手册](../31_glossary/advanced_engineering_terms_handbook.md)。
