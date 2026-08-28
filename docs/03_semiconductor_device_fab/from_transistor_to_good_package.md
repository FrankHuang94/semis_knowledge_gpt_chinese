# 从 Transistor 到 Good Package：Fab、Yield 与量产爬坡

> 第一次阅读：1–7 节。第二次阅读：8–13 节。深入阅读：14 节以后。

## 1. 先告诉我为什么需要它

一张 architecture diagram 能证明功能上“应该如何工作”，却不能证明这个产品能以可接受的良率、成本、周期和供应规模交付。AI accelerator 把 leading-edge logic、HBM、large interposer、substrate、high-speed I/O 与 liquid-cooled system 绑定起来，任何一个 manufacturing step 的 qualified good output 不足，整机出货都会受限。

因此制造问题不能简化为“哪家 foundry、哪个 node”。真正应追踪的是从 design rules、mask、wafer fabrication、die sort、advanced packaging 到 final test 的 cumulative yield，以及每一步的 cycle time、tool capacity、rework、qualification 和 learning rate。

## 2. 一句话直觉

芯片制造是在 wafer 上反复沉积、图形化、刻蚀、掺杂与处理材料，逐层构造 transistor 和 interconnect。每一步都必须在极小 process window 内重复；微小 variation 不一定立刻造成开路或短路，也可能变成 frequency、leakage、HBM link margin 或长期可靠性的分布。

## 3. 从 design 到 system 的链条

~~~mermaid
flowchart LR
  A[Architecture] --> B[RTL / Physical Design]
  B --> C[PDK / DRC / Signoff]
  C --> D[Mask set]
  D --> E[Wafer start]
  E --> F[FEOL devices]
  F --> G[MOL contacts]
  G --> H[BEOL interconnect]
  H --> I[Wafer sort]
  I --> J[Known good die]
  J --> K[2.5D / 3D package]
  K --> L[Package test]
  L --> M[Board / system test]
  M --> N[Qualified good system]
  N -. failure learning .-> B
  N -. process learning .-> E
~~~

这一链条有两个经常被忽略的反馈环。第一，fab 的 silicon data 会修正 design margin、library 与 future tape-out；第二，package 和 system failure 会回溯到 wafer、bump、substrate、assembly、firmware 或 board。没有可追溯的数据结构，团队只能看到“final test fail”，却无法迅速判断根因与责任边界。

## 4. FEOL、MOL 与 BEOL

Front End of Line（FEOL）主要形成 transistor：隔离、well、gate stack、source/drain 与相关结构。Middle of Line（MOL）把 device terminal 接到局部互连。Back End of Line（BEOL）构造多层 metal 与 dielectric，把数十亿 transistor 连接成实际 circuit。

先进 node 的价值不仅是“transistor 更小”。Process Design Kit（PDK）提供 device model、design rule、standard cell、memory compiler、I/O 与 reliability 约束。设计团队必须在这些规则下完成 timing、power、IR drop、electromigration 与 physical verification。Foundry 的 process capability 只有通过可用 PDK、IP、EDA flow、yield learning 和 customer support 才能转成产品。

更密的 transistor 可以缩小 logic area，但 SRAM、analog、I/O、ESD 与 global interconnect 未必按同样比例缩放。一个 mixed-function die 的成本与 PPA 不能只根据 node 名字外推。

## 5. Lithography 为什么关键但不是全部

ASML 将 photolithography 描述为投影系统：光通过承载 pattern 的 mask/reticle，经 optics 缩小并聚焦到 photosensitive wafer 上，再步进到下一个曝光区域。[Primary Source] Lithography 决定哪些区域在后续 etch、implant 或 deposition 中被选择，是 layer-to-layer pattern fidelity 的核心。

分辨率与 wavelength、numerical aperture 和 process factor 有关，但打印更小 feature 不等于自动获得好 yield。Focus、dose、overlay、mask error、resist、etch bias、wafer topography 与 stochastic defect 都会影响最终图形。Metrology 与 inspection 测量实际 wafer，再由 process control 调整 scanner、recipe 和其他设备。

EUV 可减少某些 multi-patterning steps，但设备、mask、pellicle、resist、source power、defect control 和维护形成新的复杂度。减少 mask layer 可能缩短 cycle、减少 overlay opportunity；可它不会消除 deposition、etch、clean、CMP、implant、anneal 和 inspection 等其他步骤。

## 6. Deposition、etch、implant 与 CMP 的因果关系

Deposition 添加材料薄膜；etch 选择性移除材料；implant 或其他掺杂方法改变 semiconductor 的 carrier 特性；anneal 修复晶格并激活 dopant；Chemical Mechanical Planarization（CMP）把表面重新磨平，为下一层 lithography 提供焦深和 topography 条件。

这些步骤不是独立菜单。Film thickness variation 会改变 etch profile；etch roughness 会影响 resistance 与 leakage；CMP dishing 或 erosion 会影响后续 overlay 和 metal resistance；contamination 可能跨多个 chamber 或 lot 传播。制造 know-how 很大一部分在 recipe interaction、equipment matching、fault detection 与 excursion containment，而不只在单台 tool 的 nominal capability。

## 7. Yield 不是一个数字

Yield 至少要分清：

- Wafer yield：wafer 是否完成流程并进入测试；
- Die yield：wafer 上多少 die 满足功能和 parametric limit；
- Binning yield：多少 die 达到目标 frequency、power 或 link grade；
- Assembly yield：die、interposer、HBM、bump、substrate 组合是否成功；
- Final-test yield：完整 package 是否通过功能、性能和可靠性筛选；
- System yield：board、cooling、power、firmware 和 network 组合是否成为可部署系统。

Intel 的公开说明强调，die size 与 defect density 都影响 usable die percentage；在相同 defect density 下，较小 die 通常有更高 yield。[Primary Source] 但 advanced package 的整体 yield 不能简单等同于各 die yield：还要考虑 known-good-die 筛选覆盖、bump/interconnect 数量、warpage、assembly sequence、test access 和 rework policy。

## 8. 简化 yield model 与边界

一个用于建立直觉的 Poisson 模型是：

[
Y_{die} approx e^{-D_0 A}
]

其中 (D_0) 是单位面积 defect density，(A) 是 die area。它表达“面积越大，遇到随机致命 defect 的机会越高”。真实 fab 常使用能描述 defect clustering 的模型，并把 systematic defect、parametric yield、edge exclusion 与 redundancy 分开，所以该公式只能做 sensitivity，不应直接代替公司内部 yield。

### Worked example

若 defect density 为每平方厘米 0.10 个，[Estimate] 一个 600 mm² die 即 6 cm²，则简化 yield 为：

[
Y approx e^{-0.10 	imes 6} approx 55%
]

若相同功能拆成两个各 300 mm² die，单 die 简化 yield 约为 74%，[Estimate] 两颗都好的裸 die 概率仍约为 55%；看起来没有改善。Chiplet economics 的潜在收益来自能够在 wafer sort 后只选择 good die、复用不同 node、减少 reticle-size 单片风险，并可能通过 redundancy 改善组合；代价则是额外 D2D interface、package area、test、assembly yield 与设计复杂度。只说“smaller die yield 更高”是不完整的。

## 9. Gross die、good die 与 cost

每片 wafer 可排多少 gross die，受 wafer diameter、die area、scribe street、edge loss 与 layout geometry 影响。Cost per good die 的一阶关系是：

[
Cost_{good die} approx
rac{Wafer cost}{Gross die 	imes Die yield}
]

但产品 economics 还要加入 mask/NRE 摊销、wafer sort、package、HBM、substrate、final test、scrap timing 与 inventory。若一个 expensive HBM stack 在最后 assembly step 才发现 logic die fail，损失远高于裸 die；所以 test coverage 和 assembly sequence 会改变期望成本。

对于 multi-die package，还要问 failed component 是否可 rework。若不可 rework，一处 assembly defect 可能报废整套昂贵 components。Known-good-die 只能降低把明显坏 die 装进去的概率，不能检测所有 latent defect，也不能保证 die 在 package stress、thermal coupling 与高速 interface 下仍通过。

## 10. Cycle time、WIP 与 capacity

Nominal wafer starts per month 不是 shipment。产品要经过许多 re-entrant steps，多次回到同类 lithography、etch、deposition 或 metrology tool。任何 bottleneck tool 的 downtime、recipe qualification、queue、rework 和 preventive maintenance 都会增加 cycle time 与 work-in-process（WIP）。

Little’s Law 提供基本直觉：

[
WIP = Throughput 	imes Cycle Time
]

若 throughput 不变而 cycle time 上升，系统中被占用的 wafer 与 working capital 增加；更重要的是 engineering feedback 变慢，yield learning loop 拉长。新 node ramp 的价值不只在最终 mature yield，还在 defect learning 和 process-window 收敛速度。

Capacity 也不是完全 fungible。同一 fab 内不同 product 可能需要不同 mask layer、tool recipe、queue priority 和 qualification；不同 site 或 vendor 间迁移更要重新做 design、process、reliability 和 customer qualification。把总 wafer capacity 当作可随时切换的统一池，会高估供给弹性。

## 11. 为什么不……？

### 为什么不把 die 做得尽量小？

拆分会增加 die-to-die PHY、latency、power、package routing、test 与 software/firmware complexity。某些 tightly coupled logic 跨 die 后会损失 bandwidth density 或增加 coherence cost。

### 为什么不等所有 process 完全成熟再 tape-out？

等待会错过 market window，也失去与 foundry 一起学习的机会。Leading customer 常用更多 design margin、redundancy 或较低初始 volume 换取提前上市；代价是 early yield、binning 和工程资源。

### 为什么不通过 final test 抓出所有 defect？

越晚发现，已经投入的 package、memory 与 assembly 价值越高；某些 latent reliability defect 又无法靠短时间 final test 完全暴露。测试本身也消耗时间、设备和 coverage 开发。

### 为什么不把所有 block 放到最先进 node？

Analog、I/O、SRAM scaling、voltage tolerance 与 cost 未必同步受益。Mature node chiplet 可能更便宜、已验证，但异构集成增加 interface 与 package 风险。

## 12. Manufacturing bottleneck shifting

改善 lithography 后，etch uniformity 或 metrology throughput 可能主导；提高 die yield 后，HBM availability 或 package assembly yield 成为瓶颈；增加 package capacity 后，substrate、test socket、burn-in 或 liquid-cooled system integration 可能限制 good rack output。

因此供应链分析必须沿“qualified good output”逐级跟踪：

~~~mermaid
flowchart LR
  W[Wafer starts] --> DY[Good logic die]
  M[HBM wafers] --> HY[Qualified HBM stacks]
  DY --> P[Package assembly]
  HY --> P
  S[Substrate / interposer] --> P
  P --> FT[Final test]
  FT --> SYS[Board + rack integration]
  SYS --> DEP[Deployed capacity]
~~~

箭头的最窄处才是系统供应 bottleneck。只宣布扩充上游 nominal capacity，不代表下游已完成 tool install、recipe qualification、yield ramp 和 customer approval。

## 13. Engineers actually say

- “Yield is ugly.”：要追问是 catastrophic defect、parametric fail、binning、assembly 还是 final-test yield。
- “We are in risk production.”：说明 process/design 已进入早期制造，但不等于稳定 volume production。
- “The line is excursion-limited.”：异常偏移和 containment 影响 output；追问 affected lots、root cause 与 recovery。
- “We need more learning cycles.”：关键是 cycle time、wafer split 与 measurement-to-action 速度。
- “Known good die is not good enough.”：现有 sort coverage 无法预测 package 条件下的 interface、thermal 或 latent fail。
- “Capacity is qualified, not installed.”：tool 在场不等于 recipe、staff、yield 与 customer qualification 完成。

## 14. Engineering → Strategy

| Engineering fact | System effect | Economic effect | Strategic implication |
|---|---|---|---|
| larger die | fewer gross die、defect exposure 高 | cost/good die 上升 | chiplet 与 redundancy 更有价值 |
| more mask/process steps | cycle 与 variation opportunity 增加 | WIP/NRE/learning 成本 | mature process ecosystem 有优势 |
| complex package | bandwidth density 上升 | assembly/test/scrap 风险 | packaging capacity 成控制点 |
| better sort coverage | 少浪费昂贵组件 | test 成本增加但 scrap 降低 | test IP 与 data loop 形成 know-how |
| faster learning | yield 更快收敛 | time-to-volume 缩短 | customer/foundry collaboration 有 moat |
| non-fungible capacity | supply response 慢 | allocation premium | nominal capex 不能直接等同供给 |

“领先 node”不是单一设备资产，而是 PDK、EDA、IP、mask、process integration、tool matching、yield data、customer feedback 与 operations 的复合能力。

## 15. Technical diligence questions

1. 报告的 yield 是 die、bin、assembly、final test 还是 system yield？
2. Yield 的分母是什么，排除了哪些 engineering wafer 或 rework？
3. 主要 fail pareto 是 random defect、systematic design interaction 还是 parametric margin？
4. Current 与 mature yield target 各是多少，证据来自多少 wafer/lot？
5. Cycle time、queue time 与 bottleneck tool utilization 如何？
6. 哪些 capacity 已安装、已 process-qualified、已 customer-qualified？
7. Known-good-die test 覆盖哪些 D2D/HBM/thermal failure？
8. Package fail 是否可 rework，报废时损失哪些组件？
9. Alternate site、tool 或 supplier 的 qualification 需要多久？
10. Yield learning data 如何回到 design rule、test limit 和下一代 architecture？
11. 成本模型是否包含 mask/NRE、test、scrap timing、inventory 与低 bin？
12. 量产瓶颈是 wafer、HBM、interposer、substrate、assembly、test 还是 rack integration？

## 16. Takeaways

1. Process node 只有通过 PDK、design、yield 和 volume operations 才成为产品能力。
2. Yield 是贯穿 die、bin、assembly、test 与 system 的乘法链。
3. Chiplet 重新分配 die yield 与 package/test 风险，不保证更便宜。
4. Nominal capacity、installed capacity、qualified capacity 与 good output 是四个不同概念。
5. 制造 moat 常来自更快 learning loop 与跨 design-fab-package-test 的数据闭环。

## Primary sources

- [Primary Source] [ASML：Lithography principles](https://www.asml.com/en/technology/lithography-principles)
- [Primary Source] [ASML：Measuring accuracy and pattern fidelity control](https://www.asml.com/technology/lithography-principles/measuring-accuracy)
- [Primary Source] [Intel：Explaining Common Chip Terms — yield 与 PPA](https://newsroom.intel.com/tech101/explaining-common-chip-terms)
- [Primary Source] [Intel Foundry：systems foundry、known-good-die 与 advanced packaging](https://www.intel.com/content/www/us/en/foundry/library/fact-sheet.html)
- [Primary Source] [TSMC eFoundry：wafer yield、WAT、quality 与 lot visibility](https://www.tsmc.com/english/dedicatedFoundry/services/eFoundry)


## 基础概念桥接

先区分 device、process step、wafer、die、package 与 good system。节点名称不是单一物理尺寸，工艺成熟度也不能由一片样品代表。讨论性能时同时记录 process、voltage、temperature；讨论产能时同时记录 cycle time、yield、qualification 和 product mix。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。
