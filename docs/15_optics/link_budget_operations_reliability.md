# Optical Link Budget 与 Operations：能亮不等于能长期运行

数据中心光链路必须在 transmitter、fiber、connector、splitter、receiver 与老化 margin 之间闭合预算。实验室短线能建立 link，不代表穿过真实布线、温度与维护周期后仍有足够误码和功率 margin。光学选择同时是物理层、供应链和运维设计。

## Budget 账本

\[
Margin=P_{\text{Tx,min}}-Loss_{\text{path,max}}-Sensitivity_{\text{Rx}}-Penalty
\]

[Estimate] path loss 包含 fiber、connector、splice 与污染；penalty 包含色散、串扰、反射、老化和实现 margin。所有输入都应使用同一 operating condition，不能把典型发射功率与最坏接收灵敏度随意组合。

~~~mermaid
flowchart LR
  T[Laser / Tx] --> C1[Connector]
  C1 --> F[Fiber plant]
  F --> C2[Connector]
  C2 --> R[Rx]
  D[Diagnostics] -.-> T
  D -.-> R
  O[Cleaning / service] -.-> C1
~~~

## 为什么不把发射功率调高

更高 optical power 可扩大 budget，却增加激光功耗、热和可靠性压力，也可能让 receiver 过载。更强 FEC 可容忍更差 raw BER，却增加 latency、功耗和错误相关性风险。更短 reach optics 通常成本低、功耗小，但限制布线；更长 reach 提高部署弹性，却可能使用更复杂 modulation 与 optics。

chosen design 要从实际 fiber map、patch panel 数、最坏温度、维护污染和 spare policy 出发。采购同一 nominal reach 的 transceiver，也要比较 host electrical interface、DSP、FEC、management 与互操作组合。

## Operations

DOM telemetry 提供 optical power、temperature 和 alarms，但阈值告警常晚于性能劣化。应保存每条链路基线与趋势，把 FEC corrections、uncorrectable errors、flaps、temperature 与更换记录关联。清洁 connector 是低成本措施，却需要流程、工具和责任；盲目换模块可能暂时恢复 link，但掩盖 fiber plant 根因。

pluggable 模块便于现场更换，却增加 cage、connector 和 thermal boundary；CPO 缩短 electrical reach，却把 optics service 与 switch package 绑定。运营数据而非单次 demo 决定哪种架构在 fleet 中成本更低。

## Diligence

- budget 是否使用最坏值并包含老化、污染和修复余量？
- FEC 前后 error counters 能否导出并关联 job？
- 多供应商模块、switch 和 firmware 是否做过 matrix validation？
- 现场更换、清洁、库存与 root-cause 流程需要多久？
- 高温和风扇故障时是否降额或 flap？
- 链路故障后的 routing 是否制造 congestion shock？

## 资料

- [IEEE 802.3 Ethernet Working Group](https://www.ieee802.org/3/) [Primary Source]
- [OIF Implementation Agreements](https://www.oiforum.com/technical-work/implementation-agreements-ias/) [Primary Source]
- [Open Compute Project Networking](https://www.opencompute.org/projects/networking) [Primary Source]


## 基础概念桥接

先区分 wavelength、laser、modulator、fiber、connector、receiver、FEC、link budget 与 reach。能亮不等于长期可运行；温度、污染、老化、校准、现场更换和多供应商验证决定 fleet economics。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。


## 进阶工程术语桥接

本篇进一步需要掌握：serialization、loss、equalization、FEC、queue、ECN、PFC、retransmission 与 link budget。阅读这些术语时，不只记中英文对应，还要补齐系统位置、正常路径、饱和或失败路径、直接 counter、端到端结果、产品状态和证据等级。若工程会议出现“已解决”“无开销”“已量产”，应立即追问 workload、boundary、configuration、status/date、failure mode 与 falsifier。

延伸阅读：[进阶工程术语手册](../31_glossary/advanced_engineering_terms_handbook.md)。
