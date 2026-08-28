# Channel Budget、Compliance 与 Production Test：眼图通过以后

SerDes link 从 package、PCB trace、via、connector、cable 到 receiver 形成完整 channel。设计阶段的仿真、实验室 compliance 和量产测试回答不同问题：仿真探索 corner，compliance 检查标准边界，production test 用有限时间筛选 variation。任何一层都不能独自证明 fleet reliability。

## Budget 分解

~~~mermaid
flowchart LR
  T[Tx] --> P1[Package]
  P1 --> B[Board / vias]
  B --> C[Connector / cable]
  C --> P2[Package]
  P2 --> R[Rx]
  J[Jitter] -.-> T
  X[Crosstalk / noise] -.-> B
  E[Equalization] -.-> R
~~~

channel budget 要同时处理 insertion loss、return loss、crosstalk、jitter、noise 和 equalization capability。把每项最坏值简单相加可能过度保守，因为它们未必相关；只用 typical 值又会低估 process、voltage、temperature 与装配 variation。chosen design 使用统计与 corner 分析，并保留可制造 margin。

## Compliance 不等于 interoperability

标准 fixture 和 pattern 让不同设备可比较，却未覆盖所有真实 traffic、连接器污染、板弯、retimer firmware 和多 lane 串扰。两个单独通过 compliance 的 endpoint 组合后仍可能失败。需要 channel-specific simulation、系统互操作和 margin sweep。

为什么不把 equalizer 做得无限强？更多 taps、训练和 DSP 增加功耗、latency、面积与收敛风险；retimer 可重建信号，却增加成本、热、固件和故障点；更短 channel 降低电气难度，却约束系统布置。选择必须连接 rack topology 与 service。

## Production reality

量产不能对每条 lane 做实验室级长测。测试方案会选择快速 proxy、loopback、BIST 与 sampling，随后通过系统 burn-in 和 field telemetry 补充。测试时间下降可提高出货，却增加 escape；guardband 过大降低 false pass，也可能误杀良品和限制最高 bin。

diligence 应查看 margin distribution 而非单条 eye diagram：不同 lot、温度、lane、connector 和老化后的 BER；训练失败、retrain 和 flap；production tester 与 system result 的 correlation。修复一个 SI 问题后，功耗或 thermals 可能成为下一限制。

## 资料

- [PCI-SIG Specifications and Compliance](https://pcisig.com/specifications) [Primary Source]
- [OIF Implementation Agreements](https://www.oiforum.com/technical-work/implementation-agreements-ias/) [Primary Source]
- [IEEE 802.3 Ethernet Working Group](https://www.ieee802.org/3/) [Primary Source]


## 基础概念桥接

先区分 bit rate、symbol rate、encoding、eye、jitter、noise、loss、equalization 与 BER。channel 是 Tx、package、board、connector、cable 和 Rx 的整体。实验室 compliance、系统 interoperability 和 production test 提供不同证据。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。


## 进阶工程术语桥接

本篇进一步需要掌握：serialization、loss、equalization、FEC、queue、ECN、PFC、retransmission 与 link budget。阅读这些术语时，不只记中英文对应，还要补齐系统位置、正常路径、饱和或失败路径、直接 counter、端到端结果、产品状态和证据等级。若工程会议出现“已解决”“无开销”“已量产”，应立即追问 workload、boundary、configuration、status/date、failure mode 与 falsifier。

延伸阅读：[进阶工程术语手册](../31_glossary/advanced_engineering_terms_handbook.md)。
