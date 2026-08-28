# Case：如何审计一家 CPO Startup 的 Manufacturability

## 1. Optical demo不是可量产产品

假设 startup展示一块 co-packaged optics样机：switch/accelerator ASIC旁放置 optical engines，宣称降低 electrical I/O power、提高 bandwidth density并解决 front-panel pluggable极限。Demo能证明 link工作，却没有证明 yield、fiber attach、laser、thermal、test、repair、supply与 field service成立。

审计目标是追踪一条 optical port从 wafer到 rack的完整 good-port economics：

<code>Photonic die → EIC → bonding → laser → fiber attach → package → board → calibration → system test → field replacement</code>

任一环节的良率、cycle time或不可维修性都可能决定商业结果。

~~~mermaid
flowchart LR
  P[Photonic wafer] --> D[Known-good PIC]
  E[Electronic IC] --> B[Bond PIC/EIC]
  D --> B
  L[Laser source] --> O[Optical engine]
  B --> O
  O --> F[Fiber attach]
  F --> C[Co-package with ASIC]
  C --> T[Test / burn-in]
  T --> R[Rack deployment]
~~~

## 2. 先定义 architecture variant

CPO不是单一产品。需要明确：

- 光源在 package内、board上还是 external laser source；
- photonic IC与 electronic IC是 2D、2.5D还是3D；
- optical engines围绕 switch ASIC还是 compute；
- fiber是 connectorized、permanently attached还是 optical circuit switch；
- control/monitoring在哪；
- package内 electrical reach多长；
- 故障时更换 engine、package、line card还是整机；
- 使用 standard interface还是 proprietary。

[Primary Source] OIF co-packaging framework与 module implementation agreements尝试规范应用、mechanical/electrical/optical边界。符合接口能减少生态摩擦，但不会自动保证共同封装良率和 field replaceability。

## 3. Product claim waterfall

“比 pluggable省电”必须拆为：

1. SerDes/retimer省掉多少；
2. EIC/PIC/laser/TEC/control消耗多少；
3. ASIC与 optics thermal coupling是否降频；
4. External laser与 distribution是否计入；
5. FEC/DSP变化；
6. cooling/fan/pump变化；
7. spare与低良率的 embodied cost；
8. 同 reach、BER、payload与环境条件。

[Estimate] 若 pluggable路径相对 power为100，其中长 reach SerDes与 module DSP占45；CPO把这部分降到15，却新增 laser distribution 8、package control 5与额外 cooling 4，则净值为87，只改善13%，不是“相关电气部分降低三分之二”所暗示的总系统结果。

## 4. Yield tree

假设一套 package需要一颗 switch ASIC、八个 optical engines、fiber attach与 final assembly。[Estimate] 各 optical engine良率96%，单颗 switch good概率90%，fiber attach整体95%，final assembly97%：

<code>Y = 0.90 × 0.96^8 × 0.95 × 0.97 ≈ 59.8%</code>

若 optical engine良率提高到99%，组合良率约76%。这说明多 engine产品对单 engine yield极敏感。Repair/rework、冗余 engines或 known-good assembly sequence可能改变经济性，必须问真实流程。

Startup若只报 PIC wafer yield，而忽略 EIC bond、fiber attach与 final switch package，就是用局部良率代表 final good port。

## 5. Known-good optical engine有多难

Electrical die可通过 probe测试逻辑与 I/O；photonic die测试需要光耦合、wavelength、insertion loss、modulator、detector与 temperature条件。Wafer-level optical test的 coupling、alignment与 throughput决定成本。

如果只有 fiber attach后才能完整测量，坏 die会消耗昂贵 assembly。Temporary coupler、grating、edge coupling与 built-in monitor各有 insertion loss和 area代价。要求 startup展示 test coverage、seconds/unit、correlation与 escape，而不只展示设备照片。

## 6. Fiber attach与 alignment

Optical coupling对 x/y/z、angle、surface与 adhesive变化敏感。Passive alignment吞吐高但需要精确 fiducial与 process；active alignment寻找最大 optical power，可能慢且昂贵。Curing会移动位置，thermal cycling和 vibration会造成长期 drift。

Diligence需要 process capability分布，不是最佳样品：

- coupling loss mean与 tail；
- cycle time；
- first-pass yield与 rework；
- supplier/equipment；
- temperature/humidity/vibration aging；
- connector contamination与 cleaning；
- automation roadmap与 capex。

## 7. Laser architecture

External laser可以把高热、低寿命或难集成光源移出主 package，并允许某种更换；代价是 laser distribution、connector/splitter、power budget与共同故障。On-package laser缩短 optical path，却增加 thermal与 assembly复杂度。

必须建立 laser failure model：一个 laser影响几个 ports？是否有 redundancy？切换需要多久？光功率监控能否提前预警？更换是否停 switch？Laser lifetime在目标 junction与 duty cycle下如何？

## 8. Thermal coupling

Switch ASIC是高热源，photonic/EIC对 temperature、wavelength与 noise敏感。把 optics靠近 ASIC减少 electrical reach，却让 thermal设计更难。Heat spreader、cold plate、TIM与 package warpage必须同时服务不同 die heights与 limits。

温度变化还可能需要 heater/TEC或 tuning，抵消部分 power收益。应看 full-load traffic、ambient/coolant corner下的 optical margin、ASIC frequency与 laser power，而不是室温桌面 demo。

## 9. Test与 repair strategy

CPO使 optics不再是简单 front-panel FRU。Field故障可能要求更换 line card、switch package甚至整机。降低 connector/retimer数量可能提高 reliability，但单个 optical engine failure的 replacement cost更高。

候选策略：

- 冗余 spare engine/lanes；
- optical engine可在 package边缘 rework；
- socketed/connectorized optical engine；
- external laser可更换；
- package级 repair；
- 系统级 graceful degradation。

每种策略牺牲 density、loss、cost或 complexity。Startup必须说明 warranty reserve与 RMA logistics。

## 10. Standards与 interoperability

[Primary Source] OIF发布 co-packaging framework和 co-packaged module implementation agreement，为 mechanical、electrical、optical与管理接口提供共同语言。标准成熟能扩大 laser、fiber与 module生态，但 proprietary integration仍可能在 bond pitch、thermal、firmware与 calibration形成 lock-in。

审计 startup在标准中控制什么：核心 IP、贡献、必需 patent、reference design还是仅声称兼容。Interoperability应由至少两个独立供应商组合与公开 test plan证明。

## 11. Supply chain map

CPO横跨：

- switch/accelerator silicon foundry；
- EIC process；
- silicon photonics foundry；
- laser wafer与 packaging；
- advanced package/interposer/substrate；
- fiber array/connector；
- precision alignment equipment；
- OSAT/test；
- firmware与 system OEM。

最慢、最低良率或最集中环节决定 output。Startup的 fabless模型不会消除 process integration责任；若供应商之间 yield attribution不清，root cause和 warranty会拖长。

## 12. Manufacturing learning curve

要求按 build批次查看：

- lots、units与 dates；
- first-pass yield；
- top defect Pareto；
- rework rate；
- test time；
- operator vs automated steps；
- supplier changes；
- reliability sample；
- field hours。

只展示累计 yield会掩盖最近 process regression。真正的 ramp evidence是 defect category逐步关闭、variation收窄、cycle time下降且 volume上升。

## 13. Market timing与替代路径

CPO在 pluggable、LPO、AEC、retimer改进与更高 SerDes之间竞争。客户可能先用 LPO降低 module DSP，保留 front-panel replaceability；或用 CPO只解决最高 radix switch。Startup的 adoption模型应按 reach、port density与 power wall分段。

如果下一代 pluggable在目标系统仍可满足 power和 faceplate，客户会推迟制造风险更高的 CPO。CPO需要证明不是“可工作”，而是某个系统在 alternative下已经无法经济扩展。

## 14. Red flags与 falsifiers

### Red flags

- 用 optical link demo代表 multi-engine package；
- 只报 PIC yield；
- power不含 laser/cooling；
- fiber attach仍手工；
- reliability只有短期 room-temperature；
- field replaceability回答含糊；
- 标准兼容没有 multi-vendor test；
- volume forecast超过关键设备 throughput；
- partnership press release代替 capacity agreement。

### 决定性 evidence

- multi-lot final good-port yield；
- automated fiber attach cycle与 Cpk；
- target temperature下长时 reliability；
- switch ASIC full load不降频；
- customer rack trial与 failure data；
- documented repair/RMA economics；
- signed capacity与 second source；
- OIF-compatible independent interoperability。

## 15. Engineering → Strategy

| Constraint | 可能赢家 | 价值捕获 |
|---|---|---|
| Electrical reach/power | CPO photonics/EIC | engine ASP/IP |
| Fiber attach | automation/equipment | tool/process moat |
| Package integration | foundry/OSAT | advanced packaging |
| Laser reliability | laser supplier | qualified source |
| Test complexity | photonic test | equipment/software |
| Field service | system OEM | platform control |
| Standards | ecosystem | adoption/price pressure |

Startup若只控制 PIC design而把 test、assembly、laser与 customer integration交给伙伴，可能拥有重要 IP却无法控制 schedule和 margin。反之，垂直整合提高控制，也需要更多 capex与制造人才。

## 16. Technical diligence questions

1. 具体 CPO architecture与可更换 boundary？
2. Final good-port yield tree及 top defects？
3. Wafer/engine/package/system各层 test coverage与 time？
4. Fiber attach method、automation、Cpk与 aging？
5. Laser topology、redundancy与 shared failure？
6. Full-load thermal与 optical margin？
7. Power是否含 ELS、control、FEC与 cooling？
8. Repair、degraded mode、RMA与 warranty成本？
9. OIF/其他标准的实际 interoperability？
10. 每个关键 process的 supplier、capacity与 second source？
11. 与 LPO/pluggable/AEC的客户决策边界？
12. 哪个 manufacturing metric在未来两个季度必须改善？

## 17. Takeaways

1. CPO价值由 final good optical port决定，不由单条 link demo决定。
2. 多 engine组合让单 engine yield、fiber attach与 test成为一阶经济变量。
3. 把 optics靠近 ASIC减少 electrical reach，却增加 thermal和 service难题。
4. 标准化降低接口风险，无法替代 process integration。
5. 投资结论应建立在多 lot yield、自动化、可靠性和客户 field data上。

## Sources

- [Primary Source] [OIF Co-Packaging Implementation Agreements](https://www.oiforum.com/technical-work/implementation-agreements-ias/)
- [Primary Source] [OIF Co-Packaging Framework](https://www.oiforum.com/oif-releases-co-packaging-framework-implementation-agreement/)
- [Primary Source] [OIF 3.2T Co-Packaged Module IA](https://www.oiforum.com/wp-content/uploads/OIF-Co-Packaging-3.2T-Module-01.0.pdf)
- [Primary Source] [Broadcom TH5 Bailly CPO material](https://docs.broadcom.com/doc/th5-51.2t-bailly-cpo)


## 基础概念桥接

案例中的数字必须进入统一 waterfall：理论峰值到 kernel、application、system、availability-adjusted output，再到单位经济性。为 base、upside、downside 分别写依赖和触发器，避免把最好条件的演示直接当财务预测。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。


## 进阶工程术语桥接

本篇进一步需要掌握：profile、compliance、certification、sampling、production、shipping、design win、attach rate 与 value migration。阅读这些术语时，不只记中英文对应，还要补齐系统位置、正常路径、饱和或失败路径、直接 counter、端到端结果、产品状态和证据等级。若工程会议出现“已解决”“无开销”“已量产”，应立即追问 workload、boundary、configuration、status/date、failure mode 与 falsifier。

延伸阅读：[进阶工程术语手册](../31_glossary/advanced_engineering_terms_handbook.md)。
