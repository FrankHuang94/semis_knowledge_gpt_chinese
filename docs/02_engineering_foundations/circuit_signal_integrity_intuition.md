# 电路与 Signal Integrity 直觉：从 RC delay 到高速链路 margin

> 第一次阅读：1–6 节。第二次阅读：7–12 节。深入阅读：13 节以后。

## 1. 先告诉我为什么需要它

GPU die、package、PCB、connector、cable 和 optical module 之间传输的并不是抽象 bit，而是随时间变化的电压与电流。速率提高时，导线不再能被当作“理想连接”；loss、reflection、crosstalk、jitter 和 power-supply noise 会共同缩小接收端可判决的 eye。于是更快 SerDes 需要更复杂 equalization、FEC、retimer 或更短 reach，并把功耗、成本和故障点带入系统。

同一组基础也解释片上 timing、PDN、HBM routing 和 package design。战略人员不需要成为 analog designer，但必须能把“signal margin is tight”翻译成 channel budget、manufacturing tolerance、power 和 qualification 问题。

## 2. 一句话直觉

电压像“推动电荷的势差”，电流是电荷流动速率；R、C、L 决定能量如何损耗、储存与延迟。频率足够高或边沿足够快时，一段 trace 必须被视为 transmission line，几何结构和材料决定 characteristic impedance，任何不连续都会让部分能量反射。

## 3. 系统位置

~~~mermaid
flowchart LR
  TX[TX logic] --> SER[Serializer]
  SER --> DRV[Driver]
  DRV --> PKG1[Package]
  PKG1 --> PCB[PCB trace / vias]
  PCB --> CONN[Connector / cable]
  CONN --> PKG2[Package]
  PKG2 --> EQ[CTLE / FFE / DFE]
  EQ --> CDR[Clock recovery]
  CDR --> DES[Deserializer]
  DES --> RX[RX logic]
  J[Clock jitter] -.-> DRV
  X[Crosstalk / noise] -.-> PCB
  P[PDN noise] -.-> EQ
~~~

End-to-end margin 属于整条 channel，不能只看 SerDes silicon。TX package、board stack-up、via、connector、cable、RX package 和 equalizer 设置必须作为组合验证。

## 4. R、C、L 与 impedance

Resistance 把电能转成热，并造成 DC voltage drop。Capacitance 储存电场能量，节点改变电压时需要充放电。Inductance 储存磁场能量，会抵抗电流快速变化。高速系统中的“地”也不是无限低 impedance 的理想参考；return path 的几何与不连续会影响 loop inductance、common-mode noise 和辐射。

最简单的一阶 RC 时间常数为：

[
	au = RC
]

它不是完整 gate-delay 模型，但建立了关键方向：更大 load capacitance、更长或更窄的 resistive wire 会使边沿变慢。边沿变慢会压缩采样窗口，也会让后级在门限附近停留更久，增加对 noise 的敏感性。

Impedance 是电压与电流的频域关系。Resistor 的 impedance 近似不随频率变化；capacitor 与 inductor 的 impedance 随频率变化，所以同一 interconnect 对 DC、低频和高速 edge 呈现不同响应。这也是“万用表测通”不能证明高速 channel 可用的原因。

## 5. 什么时候导线变成 transmission line

如果信号沿导线传播所需时间与 edge rise/fall time 同一数量级，就不能假设整根线同时处于一个电压。Driver 发出的电磁波沿 trace 与 reference plane 前进；接收端看到的是延迟后的波形。

AMD 的 PCB 指南指出，signal trace 与 reference plane 一起形成 transmission line，controlled impedance 是良好 signal integrity 的基础。[Primary Source] Characteristic impedance 由 trace geometry 和周围 dielectric 决定，而不是由“这根线静态电阻很小”决定。

当 load impedance 与 line impedance 不匹配时，部分能量被反射。反射可能造成 overshoot、undershoot、ringing 或多次 crossing。Via stub、connector、package transition、plane split 和不当 breakout 都可能形成 discontinuity。

### Single-ended 与 differential

Single-ended signal 相对 reference plane 表达电压。Differential pair 用两条互补信号的差值表达信息，能抑制一部分共同耦合的噪声，并改善 return path，但并不免疫 skew、pair asymmetry、mode conversion 与 crosstalk。

常见高速 differential channel 会按指定 differential impedance 设计。AMD 文档给出典型 50 Ω odd-mode、100 Ω differential 的关系，[Primary Source] 但实际目标必须以对应 protocol、package 与 board stack-up 为准，不能把该数值机械套到所有接口。

## 6. Eye diagram 到底表达什么

Eye diagram 把许多 unit interval 的波形叠加。Eye height 代表采样时刻的 voltage margin；eye width 代表 timing margin。Loss 和 bandwidth limitation 让边沿变慢并产生 inter-symbol interference；jitter 左右移动 crossing；noise 上下移动电压；reflection 和 crosstalk 让波形产生 pattern-dependent distortion。

一个“眼睛张开”的图仍不完整。必须知道它是 simulation 还是 measurement、采样点在哪里、是否经过 equalization、对应 BER 目标、channel corner、temperature、voltage、pattern、lane aggressor 和 FEC 假设。

BER 是错误 bit 的比例；实际系统更关心 post-FEC uncorrectable error、burst behavior、link flap 和 tail reliability。平均 BER 好看并不保证没有相关性错误，也不保证连接器老化、温度漂移或多个 aggressor 同时活动时仍稳定。

## 7. Loss、ISI 与 equalization

高频分量通常衰减更严重，使原本陡峭的 edge 被拉平。前一个 bit 的残余响应影响后一个 bit，形成 inter-symbol interference（ISI）。Channel 越长、材料 loss 越大、transition 越多，receiver 看到的波形越难判决。

工程师可在 TX 使用 FFE / pre-emphasis，预先改变不同 symbol 的幅度；RX 使用 CTLE 提升高频成分，使用 DFE 根据已判决 symbol 消除 post-cursor ISI。Equalization 不是恢复“原始完美波形”的魔法：增益也会放大 noise，DFE 可能 error propagation，adaptive loop 需要 convergence 与 telemetry，所有处理都消耗 power、area 与 validation effort。

Retimer 完成接收、时钟恢复和重新发送，可以切断 jitter/loss budget，但增加 latency、power、cost、firmware、thermal 和 failure point。Redriver 主要进行 analog signal conditioning，通常不能像 retimer 那样建立新的 clock domain。选择取决于 channel loss、reach、protocol transparency、latency 和 serviceability。

## 8. Jitter、noise 与 crosstalk

Jitter 是事件相对理想时间的偏移，可含 random 与 deterministic 成分。Clock source、PLL、power-supply noise、data-dependent ISI 和 crosstalk 都能贡献 jitter。把所有 jitter 简单相加可能过度保守或错误乐观，真实 budget 需要考虑统计性质与相关性。

Crosstalk 来自邻近导体间电容与电感耦合。Aggressor 的 edge 越快、并行距离越长、间距越小，victim 越可能受到干扰。增加 spacing、改变 layer、使用 ground reference、错开 routing 或降低 simultaneous switching 可以改善，但会消耗 routing area 或 package escape capacity。

Power noise 会改变 driver/receiver threshold、PLL phase 和 gate delay。Signal integrity（SI）与 power integrity（PI）因此不能完全分开：同一批 lanes 同时翻转可能造成 supply droop，再把 timing noise 注入 link。

## 9. Channel budget 与 design space

| 手段 | 改善 | 代价 / 新风险 |
|---|---|---|
| 更低-loss 材料 | 延长 electrical reach | PCB 成本、供应商与加工窗口 |
| 更宽 trace / 更大 spacing | 降 loss/crosstalk | routing density 下降 |
| 更强 TX swing | voltage margin 上升 | power、EMI、receiver stress |
| 更多 equalization | 抵消 ISI | power、noise amplification、adaptation |
| FEC | 降低 residual BER | latency、overhead、burst limit |
| Retimer | 重置 channel budget | power、成本、firmware、故障点 |
| Optics | 大幅延长 reach | E/O conversion、module power、成本、维护 |

Co-design 的核心是把 scarce margin 分配给 package、board、connector 和 cable，而不是要求某一方无限吸收所有损耗。

## 10. 为什么不……？

### 为什么不把 TX swing 无限提高？

更大 swing 增加 driver power、switching noise 与 electromagnetic emission，也可能超过 receiver 或 device reliability limit。它不会消除 reflection、frequency-dependent loss 或 jitter。

### 为什么不全部依赖更强 equalizer？

Equalizer 只能处理模型和动态范围允许的失真。严重 notch、mode conversion、随机 noise、burst interference 或失去 timing information 不能无损恢复；更强 DSP 还会增加 PHY power。

### 为什么不每段都加 retimer？

Retimer 会增加 BOM、board area、thermal load、firmware lifecycle 和 field failure surface。大量 retimer 还会把供应约束与 qualification 时间带入平台。

### 为什么不全部换 optics？

短 reach 下，copper 可能更便宜、更低 latency、维护简单。Optics 引入 laser、modulator、photodiode、DSP、connector cleanliness 和 thermal control。合理 boundary 取决于 reach、bandwidth density、energy/bit、reliability 与 service model。

## 11. Worked example：为什么 edge rate 比 clock frequency 更关键

假设控制信号只以 100 MHz 重复，但 driver 的 rise time 为 200 ps。决定它是否表现为 transmission line 的不是 100 MHz 基频，而是 200 ps edge 包含的高频成分。[Inference] 如果 board trace propagation 约为 150 ps/in，[Estimate]，几英寸 trace 的 flight time 已与 rise time 同量级，就必须检查 impedance、return path、termination 与 reflection。

这解释了为什么“接口频率不高”不能自动免除 SI 分析，也解释为什么换用更快 I/O cell 可能让原本稳定的 board 出问题：逻辑功能没变，但 edge spectrum 变了。

## 12. Second-order effects

提高 lane rate 可减少同等 aggregate bandwidth 所需 lane 数，却会缩短 reach、提高 equalization/FEC power，并增加 retimer 或 optics 需求。改用 PAM4 提高每 symbol bit 数，会缩小相邻 voltage level 间距，对 noise 和 linearity 更敏感。增加 FEC 改善 BER 后，latency、coding overhead 与 correlated burst 成为新限制。缩短 electrical channel 后，optical engine 或 switch packaging 位置又影响 serviceability 与 thermal。

最终 bottleneck 可能从 front-panel bandwidth 移到 package escape、connector density、PHY power、optical yield 或 field repair，而不是简单“链路更快”。

## 13. Engineers actually say

- “Signal margin is tight.”：综合 voltage/timing budget 剩余很少；追问最坏 corner、dominant impairment 和 guardband。
- “The channel has a nasty notch.”：某频段 insertion loss 明显恶化，可能来自 via、connector 或 resonance；平均 loss 不能描述。
- “We are equalization-limited.”：TX/RX 可补偿范围或 noise amplification 已接近边界。
- “There are link flaps.”：链路反复 up/down，可能比少量 corrected BER 更破坏 collective job。
- “The package is eating the budget.”：die-to-ball transition 已消耗显著 loss/reflection margin，board 余量被压缩。
- “It passes compliance but not the system.”：标准测试覆盖的 channel/model 与真实多 aggressor、firmware、thermal 组合存在差异。

## 14. Strategy 与 diligence

Signal integrity IP 不只是一组 analog block。可持续能力可能来自 channel modeling、package/board co-design、IBIS-AMI model 质量、adaptation firmware、test coverage、connector/cable ecosystem 与大规模 field telemetry。

应追问：

1. Claimed reach 对应什么 board material、connector、via 数、temperature 与 BER？
2. Pre-FEC 与 post-FEC 指标分别是什么？错误是否呈 burst？
3. Equalizer 需要多少 training time，失败时如何 fallback？
4. Package、PCB、connector、cable 各消耗多少 channel budget？
5. 是否在所有 adjacent lanes 活动时测试 crosstalk？
6. Compliance test 与目标系统 topology 有哪些差异？
7. Retimer 的 latency、power、firmware update 与 telemetry 如何？
8. Connector aging、污染、插拔和温度循环如何 qualification？
9. Simulation model 是否由 measured silicon/board correlation？
10. Field link flap 的 root-cause closure 时间和责任边界是什么？

## 15. Engineering → Strategy

| 工程变化 | 系统结果 | 价值捕获 | 风险 |
|---|---|---|---|
| lane rate 上升 | lane 数下降、reach 变紧 | SerDes、retimer、low-loss material | PHY power、qualification |
| 更强 FEC/equalization | residual error 下降 | DSP/PHY IP | latency、complexity |
| electrical → optical | reach 与 density 改善 | optics、laser、packaging | cost、serviceability |
| CPO | electrical path 缩短 | switch/optical co-packaging | yield、thermal、repair |
| richer telemetry | faster root cause | silicon + software vendor | firmware integration |

## 16. Takeaways

1. 高速 bit 是电磁波形，不是理想 0/1。
2. Edge rate、flight time、impedance 与 return path 决定 transmission-line behavior。
3. Eye、BER、FEC、link flap 和 field reliability 必须放在一起看。
4. Equalization、retimer 与 optics 都是在重新分配 channel budget，不是免费修复。
5. SI/PI、package、board、firmware 与 operations 构成一个共同系统。

## Primary sources

- [Primary Source] [AMD UG583：Transmission Lines](https://docs.amd.com/r/en-US/ug583-ultrascale-pcb-design/Transmission-Lines)
- [Primary Source] [AMD UG583：Trace Characteristic Impedance Design](https://docs.amd.com/r/en-US/ug583-ultrascale-pcb-design/Trace-Characteristic-Impedance-Design-for-High-Speed-Transceivers)
- [Primary Source] [AMD XAPP1392：System-Level SI Analysis](https://docs.amd.com/r/en-US/xapp1392-pcb-chan-design-guidelines/System-Level-SI-Analysis)
- [Primary Source] [AMD/Xilinx：Signal Integrity Tips and Tricks](https://docs.amd.com/api/khub/documents/0cnBFpU4_p6~hs37twE4yQ/content)


## 基础概念桥接

先区分数值表示、组合逻辑、时序状态、时钟、流水线与测量误差。工程上相同功能可有不同 timing、power、area 和 reliability；公式成立也不代表测量边界正确。先做量纲与数量级检查，再进入电路或架构细节。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。


## 进阶工程术语桥接

本篇进一步需要掌握：微操作、流水线冒险、并行度、shape、动态批处理、尾延迟、数量级与单位经济性。阅读这些术语时，不只记中英文对应，还要补齐系统位置、正常路径、饱和或失败路径、直接 counter、端到端结果、产品状态和证据等级。若工程会议出现“已解决”“无开销”“已量产”，应立即追问 workload、boundary、configuration、status/date、failure mode 与 falsifier。

延伸阅读：[进阶工程术语手册](../31_glossary/advanced_engineering_terms_handbook.md)。
