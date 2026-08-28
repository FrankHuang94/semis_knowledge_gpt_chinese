# 3D Integration 的 Power、Thermal 与 Mechanical Co-design

三维堆叠缩短互连并提高单位面积功能密度，也把多个 die 的功耗、热膨胀、应力和供电路径压进更小体积。平面 floorplan 可以把热源分开，垂直堆叠却会让上层或中间层的热必须穿过其他材料与界面。互连优势与可靠性代价必须共同计算。

## 耦合路径

~~~mermaid
flowchart TB
  D1[Top die] --> T[Thermal path]
  D2[Bottom die] --> T
  P[Power delivery] --> D1
  P --> D2
  M[CTE / warpage] --> I[Bond / TSV / bump]
  T --> M
  I --> S[Signal integrity]
  I --> Y[Yield / reliability]
~~~

## Floorplan alternatives

把高功耗 logic 靠近 cold plate 可降低 junction temperature，却让下层 memory 或 I/O 的信号和供电路径改变；把 cache 堆在 compute 上可提高带宽，却可能形成 hotspot；face-to-face bonding 提供高密度互连，但 test access、repair 和 assembly sequence 更复杂；interposer 保留较好的散热和已知良品选择，却占更多面积。

为什么不把所有功能垂直堆叠？thermal resistance、power delivery、yield multiplication 和测试可访问性会先成为约束。为什么不只降低频率解决热？这会牺牲性能，且 leakage、memory retention 与邻近 die 温度仍可能受影响。

## Mechanical 与 lifetime

不同材料的热膨胀系数不一致，温度循环会在 bond、TSV、underfill 和 package 中产生应力。局部 hotspot 不只是温度问题，也改变应力梯度。更薄 die 缩短 TSV、改善堆叠高度，却更易翘曲和破裂。材料与结构选择必须覆盖 assembly、board attach、运输和 field cycles。

[Estimate] package yield 与 lifetime reliability 都取决于多个界面；早期 test vehicle 若尺寸、功率分布或材料不同，不能直接代表目标产品。

## Co-design 与验证

architecture 应向 package team提供真实 activity map，而不是单一 TDP；thermal simulation 要反馈 DVFS 和 placement；mechanical model 要反馈 keep-out 与 bond pattern；test strategy 要在 tapeout 前定义 access 和 repair。若这些工作按组织顺序串行完成，问题通常在最昂贵阶段才暴露。

diligence 应要求多物理场模型与实测 correlation、不同 workload hotspot、warpage distribution、thermal cycling、bond resistance、known-good strategy 和 failure analysis。解决互连瓶颈后，价值可能迁移到 cooling、materials、bonding equipment、EDA 与 test。

## 资料

- [IEEE 1838 Standard for 3D Stacked IC Test Access](https://standards.ieee.org/ieee/1838/6846/) [Primary Source]
- [imec 3D System Integration](https://www.imec-int.com/en/what-we-offer/research-portfolio/3d-system-integration) [Independent]
- [JEDEC Standards and Documents](https://www.jedec.org/standards-documents) [Primary Source]


## 基础概念桥接

先区分 chiplet、die-to-die PHY、protocol、active/passive base die、2.5D 与 3D。可组合性还需要 power、clock、thermal、security、debug、yield ownership 和 warranty；接口标准不能自动创造开放市场。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。


## 进阶工程术语桥接

本篇进一步需要掌握：IR drop、thermal resistance、warpage、hybrid bonding、wafer sort、process window 与 qualification。阅读这些术语时，不只记中英文对应，还要补齐系统位置、正常路径、饱和或失败路径、直接 counter、端到端结果、产品状态和证据等级。若工程会议出现“已解决”“无开销”“已量产”，应立即追问 workload、boundary、configuration、status/date、failure mode 与 falsifier。

延伸阅读：[进阶工程术语手册](../31_glossary/advanced_engineering_terms_handbook.md)。
