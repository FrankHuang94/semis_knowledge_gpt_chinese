# Retimer vs Redriver：放大一个受损波形，还是重新生成一条 Link

## 1. 两者解决的不是同一种损伤

随着 SerDes rate提高，package、PCB、connector与 cable的 insertion loss、reflection和 jitter会压缩 eye。Redriver与 retimer都用于 channel extension，但机制不同：

- Redriver是非 protocol-aware的模拟/线性扩展器，均衡并放大输入波形；
- Retimer是 physical-layer protocol-aware设备，恢复 data与 clock，再发送一份新的 signal，并把长 channel分为两个电气 segment。

[Primary Source] PCI-SIG对两者的定义正是这种区别。最简直觉是：redriver改善已经存在的 waveform；retimer判决 bit后重新计时与发射。

~~~mermaid
flowchart TD
  A[Endpoint A] --> C1[Lossy channel]
  C1 --> R{Extension}
  R -->|Redriver| AMP[CTLE / Gain / Driver]
  R -->|Retimer| REC[EQ + CDR + Logic + New TX]
  AMP --> C2[Remaining channel]
  REC --> C3[New link segment]
  C2 --> B[Endpoint B]
  C3 --> B
~~~

## 2. Redriver能做什么

Redriver常包含 CTLE、gain与 output driver，用于补偿 high-frequency loss、调整 amplitude与改善接收端 eye。它透明、latency低、cost/power通常较小，适合损伤主要来自可补偿 attenuation且 jitter预算仍充足的 channel。

它不能把随机 jitter擦掉，也不能像完整 receiver一样可靠重建每个 bit。输入 signal若已严重闭合，放大也会同时放大 noise；错误 equalization还会造成 over/under-shoot。Redriver前后的 channel仍是同一个 end-to-end link budget。

## 3. Retimer能做什么

Retimer包含 receiver equalization、clock/data recovery、protocol-aware state与新的 transmitter。它把一条困难 channel变成两个独立 segment，每段分别满足电气预算。CDR重新建立 timing reference，因此可以切断一部分 uncorrelated jitter积累。

Protocol awareness意味着 retimer要参与 link training、speed/width变化、polarity/lane处理与错误管理。[Primary Source] PCI-SIG说明 PCIe retimer会参与 link equalization，并与上下游端口协同调整 data rate与 link width。

代价是更多 silicon、power、latency、firmware、management与 interoperability testing。Retimer本身也可能成为 link failure和 security boundary。

## 4. 损伤分类决定选择

| Channel问题 | Redriver | Retimer |
|---|---|---|
| 可预测高频 attenuation | 通常有效 | 有效 |
| 输入 eye仍有 margin | 合适 | 可能过度 |
| 随机/不相关 jitter累积 | 无法重置 | CDR可部分隔离 |
| 长 reach需分段 | 仍是一条 link | 形成两个 segment |
| Protocol training | 不参与 | 参与 |
| 最低 latency/power | 优势 | 代价较高 |
| 复杂拓扑与诊断 | 能力有限 | 可有 telemetry |
| Firmware/compatibility | 较简单 | 更复杂 |

实际还要考虑标准允许数量、拓扑、lane reversal、reset、sideband与 compliance。

## 5. 计算：Loss budget为何不等于 jitter budget

[Estimate] 假设 endpoint允许总 channel loss预算为 28 dB，board、connector与 cable合计30 dB。Redriver提供8 dB高频增益后，amplitude budget看似转正；但若 channel已引入超过接收端容忍的随机 jitter，增益不会重建 timing。

Retimer若放在中点，可以把 loss分成15 dB与15 dB两个 segment，并分别恢复 data/clock。这个例子没有证明 retimer一定成功：每段仍要满足 return loss、crosstalk、PVT与 protocol timing，而且 retimer自身增加 latency与 failure probability。

## 6. 为什么不总是用 redriver

Redriver便宜、低功耗、低延迟，但只有在输入 signal质量足以继续线性处理时才有效。长 reach、多 connector、复杂 backplane或高 rate下，uncorrelated jitter和 noise可能超出能力。把 gain调高不能创造 SNR，反而可能造成 saturation。

另一个问题是可调性与生产 variation。实验室 golden board可通过，量产 board、connector与温度 corner可能失败。若 redriver缺少足够 telemetry，field issue难以定位是 upstream、channel还是 downstream。

## 7. 为什么不总是用 retimer

Retimer会增加 BOM、power、thermal、latency与 validation。每个器件都有 firmware、reset、clock与 management需求；多 vendor endpoint/retimer组合扩大 compatibility matrix。对于短而优质的 channel，retimer只增加复杂度。

Retimer还占用 board area并可能需要 heatsink与 airflow。高密度 server或 switch中，许多 lanes乘以每 lane功耗会变成 rack级影响。选择应证明它扩展的 topology/reach价值高于长期维护成本。

## 8. 为什么不直接换更好的 PCB或 cable

改善材料、缩短 trace、优化 connector与 via可以从源头降低 loss，通常最稳健。但机械 layout、serviceability、card placement、cost与供应可能不允许。高端 low-loss laminate也需要 stack-up控制、fabrication yield与 vendor qualification。

工程上应比较整个系统：更好 board、AEC、redriver、retimer、optical link或重新布局。单器件价格最低的方案不一定带来最低 field failure与最快 design closure。

## 9. Retimer把“一条 link”变成管理系统

Protocol-aware器件必须处理 enumeration前后的行为、firmware版本、lane mapping、equalization、error counter与 reset sequencing。平台要能发现 retimer、读取 health、更新 firmware并在失败时判断能否降速或降宽。

这给 observability带来机会：segment-level counters可帮助定位哪一侧 margin变差。但若 telemetry不标准或不可被 fleet系统采集，retimer只增加一个黑盒。

## 10. Product reality：验证而不是相信“compliant”

PCI-SIG维护 retimer test specifications与 integrators list。[Primary Source] 进入 compliance program可降低基本 interoperability风险，但 system vendor仍须验证目标 CPU/GPU/switch、board、cable、BIOS/firmware与 workload power state组合。

需要覆盖：

- cold/warm boot与 surprise reset；
- link speed/width negotiation；
- low-power state进入与退出；
- lane reversal/polarity与 bifurcation；
- correctable/uncorrectable error；
- firmware upgrade/rollback；
- temperature、voltage、aging与 marginal channel；
- hot-plug、cable replacement与 degraded operation。

## 11. Second-order effects

1. Retimer延长 electrical reach，可能推迟 optics，却增加 board power与热。
2. Redriver降低 BOM，却把更多 margin责任留给 endpoint与 channel。
3. 更高 SerDes rate会扩大 retimer市场，也可能推动 optical I/O绕过长电气 channel。
4. Protocol-aware telemetry提高 serviceability，却形成 firmware和 management依赖。
5. 多 retimer topology增加可达距离，也增加 latency、故障点与 compatibility。
6. 更严格 channel qualification提高材料与 connector供应商价值。
7. Retimer supply shortage可能限制整机出货，即使 compute silicon充足。

## 12. Engineers actually say

- “The redriver opens the eye.”：问在哪个 PVT corner、pre/post equalization与 BER contour。
- “The retimer resets the channel.”：问分段预算、added latency与 protocol state。
- “It is transparent.”：问 software-transparent是否也意味着 management-free。
- “We passed compliance.”：问具体组合、版本与 system stress。
- “We can tune it in BIOS.”：问量产 calibration、fallback与 field update。
- “The board needs two retimers.”：问是否比较过 layout、material、AEC或 optics。

## 13. Engineering → Strategy

| 方案 | 工程收益 | 主要代价 | 战略含义 |
|---|---|---|---|
| Redriver | 低成本/延迟的 loss补偿 | 不重建 jitter | 模拟 SI IP |
| Retimer | 重建 signal、分段 | power/firmware | protocol-aware silicon |
| 更好 PCB | 根源改善 | material/fab cost | laminate与制造 |
| AEC | 更长 copper reach | cable power/管理 | cable silicon |
| Optical | 长 reach与密度 | optics制造 | 光器件供应 |
| 重新布局 | 少器件 | 机械限制 | system co-design |

## 14. Technical diligence questions

1. Channel failure来自 attenuation、reflection、crosstalk还是 jitter？
2. 完整 COM/eye/loss budget与 measurement correlation？
3. Redriver输入 eye在最坏 corner是否仍可线性恢复？
4. Retimer把 link分成几段，每段 margin多少？
5. Added latency、power、thermal与 BOM按整机汇总？
6. 支持哪些 endpoint、switch、cable与 firmware版本？
7. Fleet如何采集 segment error与执行 firmware升级？
8. Failure时能否降速/降宽，SLO如何？
9. Compliance之外做了哪些 system stress与 aging？
10. 下一代 rate是否需要更换 board、connector或进入 optics？

## 15. Takeaways

1. Redriver均衡放大 waveform；retimer恢复 bit/clock并重新发射。
2. Loss可补偿不代表 jitter可恢复，必须先分类 channel损伤。
3. Retimer提高 reach与 margin，却带来 power、latency、firmware和供应风险。
4. Compliance是起点，目标平台组合与 PVT验证才决定量产。
5. 选择应比较整条 channel与生命周期，而不是单器件单价。

## Primary sources

- [Primary Source] [PCI-SIG：Retimers vs Redrivers](https://pcisig.com/blog/pci-express%C2%AE-retimers-vs-redrivers-eye-popping-difference)
- [Primary Source] [PCI-SIG FAQ：What are Retimers and when are they needed?](https://pcisig.com/what-are-retimers-and-when-are-they-needed)
- [Primary Source] [PCI-SIG PCI Express Base specifications](https://pcisig.com/specification-overview/pci-express-base)
- [Primary Source] [PCI-SIG Integrators List](https://pcisig.com/developers/integrators-list)


## 基础概念桥接

先区分 bit rate、symbol rate、encoding、eye、jitter、noise、loss、equalization 与 BER。channel 是 Tx、package、board、connector、cable 和 Rx 的整体。实验室 compliance、系统 interoperability 和 production test 提供不同证据。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。


## 进阶工程术语桥接

本篇进一步需要掌握：serialization、loss、equalization、FEC、queue、ECN、PFC、retransmission 与 link budget。阅读这些术语时，不只记中英文对应，还要补齐系统位置、正常路径、饱和或失败路径、直接 counter、端到端结果、产品状态和证据等级。若工程会议出现“已解决”“无开销”“已量产”，应立即追问 workload、boundary、configuration、status/date、failure mode 与 falsifier。

延伸阅读：[进阶工程术语手册](../31_glossary/advanced_engineering_terms_handbook.md)。
