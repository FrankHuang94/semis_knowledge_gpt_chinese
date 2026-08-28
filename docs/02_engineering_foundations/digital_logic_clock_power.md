# 数字逻辑、时钟与功耗：为什么“一个开关”最终限制 AI 芯片

> 第一次阅读：1–7 节。第二次阅读：8–13 节。深入阅读：14 节以后。

## 1. 先告诉我为什么需要它

架构图里常见的是 SM、Tensor Core、cache、NoC 和 memory controller，但物理芯片不会执行这些抽象名词。它只允许晶体管改变节点电压，再由组合逻辑产生新结果，由寄存器在时钟边沿保存状态。任何“增加 core、提高频率、扩大 cache”的提案，最终都要同时回答三件事：信号能否在一个 clock period 内传播完，供电是否允许这些节点同时翻转，产生的热是否能被移走。

如果不了解这层约束，就容易把 peak FLOPS 当成可以自由堆叠的资源。真实设计中，逻辑深度、wire delay、clock skew、setup/hold margin、动态功耗和 leakage 会共同决定可用频率、voltage、面积和 yield。

## 2. 一句话直觉

数字电路不是“0 和 1 的数学世界”，而是把连续且带噪声的电压解释成离散状态的工程系统。Clock 给状态更新规定节拍；timing closure 证明每条受约束路径都能在最坏工艺、电压、温度条件下准时到达。

## 3. 它在系统哪里？

~~~mermaid
flowchart LR
  A[Workload / Algorithm] --> B[Architecture]
  B --> C[RTL: registers + logic]
  C --> D[Synthesis / standard cells]
  D --> E[Placement + routing]
  E --> F[Timing / power / IR-drop signoff]
  F --> G[Die]
  G --> H[Package / board / system]
  H -. field feedback .-> B
~~~

Architecture 规定“需要多少并行、多少状态、每周期做什么”；physical design 回答“在给定 process、面积、voltage 与 frequency 下能否实现”。两者不是先设计 architecture、再由后端被动实现的单向关系。高性能芯片需要反复迭代：如果 global wire 太长，可能改变 floorplan；如果 register file 端口太多，可能把结构 bank 化；如果 clock tree 功耗过高，可能降低频率或增加 gating。

## 4. 从 transistor as switch 到 gate

MOSFET 的 gate voltage 控制 channel 是否易于导通。CMOS inverter 用互补的 nMOS 与 pMOS，使稳态时通常只有一侧导通，从而在理想逻辑状态下减少持续直流电流。NAND、NOR 等 gate 再组合成 adder、comparator、multiplexer 和 decoder。

关键直觉不是记 truth table，而是理解每个输出节点都有 capacitance。要改变逻辑状态，就必须对这个 capacitance 充电或放电。驱动能力有限、负载越大、wire 越长，电压跨过接收端逻辑门限所需时间越长。因此一个门的 delay 不只由“几纳米制程”决定，还由 fan-out、cell size、输入 slew、wire RC、温度和供电压降决定。

### Combinational 与 sequential logic

Combinational logic 的输出只取决于当前输入；sequential logic 还依赖过去状态。Flip-flop 或 latch 把一个时间连续的网络切成周期边界。没有这些边界，一条巨大的组合路径可能需要很长时间才稳定，设计也难以在多个操作之间保持可控状态。

寄存器并非免费。每插入一级 pipeline，都增加 clocked elements、clock tree load、面积、功耗和 latency；还可能增加 bypass、hazard control、replay 或 flush 的复杂度。Pipeline 提高的是可重叠工作的 throughput 潜力，不会自动降低单个任务的 end-to-end latency。

## 5. Clock 到底做什么

Clock 是分布到大量 sequential elements 的周期性参考。它不是“芯片速度”本身，而是设计承诺：每个边沿之间，指定的数据路径必须完成 launch、logic propagation、routing 和 capture。

最简 setup 约束可以写成：

[
T_{clk} ge t_{cq} + t_{logic} + t_{wire} + t_{setup} + t_{skew} + t_{uncertainty}
]

左边是 clock period，右边依次包含 launching register 的 clock-to-Q、组合逻辑、互连、接收寄存器 setup、clock skew 与额外不确定性。频率是 period 的倒数，因此提高频率等于压缩所有这些预算。

Hold 检查方向相反：新数据不能太快冲到接收端，以免接收寄存器在同一边沿附近抓到错误状态。Setup violation 常通过减逻辑、加 pipeline、换更快 cell 或提高 voltage 修复；hold violation 常通过加 delay cell、改 routing 或调整 clock tree 修复。一个修复可能损害另一个 corner，所以“timing closed”意味着跨多组 process-voltage-temperature corner 与工作模式同时满足，而不是典型实验室条件下跑通一次。

## 6. Critical path 与 timing closure

Critical path 是当前最吃紧的受约束路径。它可能位于整数 ALU、address generation、cache tag compare、crossbar select、NoC router、wide reduction 或 control fan-out。优化该路径后，第二差路径会成为新 critical path；这正是 physical design 版本的 bottleneck shifting。

Timing closure 是一组统计与最坏情形约束的收敛过程。工程团队会关注 worst negative slack、total negative slack、violating endpoint 数量，以及这些 violation 是否集中于同一结构。只报“目标 3 GHz”而不说明 voltage、corner、die temperature、功能模式和 signoff margin，信息是不完整的。[Inference]

### 为什么 wire 越来越重要

Transistor 缩小能减小部分 gate capacitance 与局部距离，但 chip-level distance 不会按同样比例消失。更大的 die、更多单元和更复杂 routing 会让 global wire、repeaters 与 clock distribution 占据显著预算。于是 architecture 会采用 hierarchy：local register file、banked cache、分区 NoC、distributed scheduler。这些结构不仅为逻辑模块化，也是为了限制 wire length 与 fan-out。

## 7. Dynamic power 与 leakage

常用的一阶动态功耗关系是：

[
P_{dynamic} approx alpha C V^2 f
]

其中 (alpha) 是 switching activity，(C) 是有效被充放电 capacitance，(V) 是 voltage，(f) 是 frequency。公式告诉我们：频率近似线性增加动态功耗，而 voltage 以平方项影响能量；但降低 voltage 会减慢 transistor，缩小 timing margin。为了追求更高 frequency 而升压，功耗可能增长得比 frequency 更快。

Leakage 是没有发生有用切换时仍存在的电流。温度升高常使 leakage 增加，进一步产生热，形成正反馈。Clock gating 可以让空闲 block 的寄存器停止翻转，power gating 可切断更深度空闲区域，但后者要付出 isolation、state retention、wake-up latency、rush current 与 verification 成本。

## 8. Pipeline 的 design space

| 选择 | 得到什么 | 付出什么 | 适合什么 |
|---|---|---|---|
| 更深 pipeline | 更短 stage、潜在更高 frequency | 更多寄存器、latency、clock power、flush cost | 高吞吐且可充分并行 |
| 更宽 datapath | 每周期更多工作 | area、routing、operand supply、utilization 风险 | 数据并行稳定 |
| 更大 cell / buffer | 更强 drive、改善 slew | capacitance、动态功耗、拥塞 | 关键高 fan-out path |
| 更低 voltage/frequency | 更好能效和热余量 | 峰值 throughput 下降 | power-capped fleet |
| 更多 local replication | 缩短 wire、减 fan-out | area、一致性与控制复杂度 | 大规模分区设计 |

“更深”和“更宽”经常互相强化问题：更宽需要更多 wiring 与 control，导致 stage 难以变短；更深又增加跨 stage 的状态和调度复杂度。

## 9. 为什么不……？

### 为什么不无限提高 clock？

更短 period 会增加 timing closure 难度；为了速度使用更大 cell、更强 buffer 与更高 voltage，又增加 power、IR drop、热和 clock distribution 成本。系统在固定 rack power 下可能反而减少可部署芯片数。

### 为什么不每隔很短距离插一个 register？

Register 与 clock tree 本身消耗能量和面积，并增加 pipeline latency、control state、flush/replay 成本。对于 branch-heavy CPU，错误预测要清空更多 stage；对于 GPU，过深 pipeline 也需要足够并行 warp 来隐藏 latency。

### 为什么不把所有单元都做成最快的 cell？

高 drive cell 通常更大、输入 capacitance 更高，增加上游负载和 routing congestion。局部路径变快，邻近路径、功耗或布线可能变坏。Physical optimization 必须看全图而不是单个 gate。

### 为什么不把 voltage 降到最低？

Voltage 降低会减弱 drive current、拉长 delay，并压缩对 noise、variation、droop 的容忍度。低压能效 sweet spot 取决于 workload、silicon bin、temperature 与可靠性目标。

## 10. Worked example：频率提升为什么不是免费性能

假设一个 block 原先在 1.0 V、1.5 GHz 工作，动态功耗为 120 W。为了达到 1.8 GHz，需要把 voltage 提到 1.08 V；若 activity 与 capacitance 近似不变：

[
rac{P_2}{P_1} approx
left(rac{1.08}{1.0}ight)^2
left(rac{1.8}{1.5}ight)
approx 1.40
]

动态功耗约变成 168 W，[Estimate] 即 frequency 提升 20%，动态功耗却约提升 40%。若系统原本已受 power 或 cooling 限制，实际可能需要降低其他单元频率、减少 active units，或触发 thermal throttling，因此 application throughput 未必增加 20%。

## 11. Workload mapping

Training 大型 GEMM 常有足够并行度，较容易从 pipeline throughput 与宽 datapath 获益，但受 memory 和 collective stall 时，继续提高 core frequency 的回报下降。Decode 的小 batch 或 memory-bound 阶段，经常等待 KV cache 与 HBM；此时 clock 更高可能主要增加空转能耗。Database 与 control-heavy workload 更敏感于 branch、cache miss 与 single-thread latency。HPC 需要按 kernel 区分：dense compute、stencil、graph 的瓶颈完全不同。

所以频率不能脱离“active cycle 中做了多少有用工作”讨论。真正指标是 useful work per joule、per dollar、per rack，以及在目标 tail latency 下的 sustained throughput。

## 12. Second-order effects

逻辑变快以后，operand delivery 可能成为瓶颈；扩大 register file 后，端口、wire 与 scheduler 可能主导；增加 pipeline 后，branch/replay cost 上升；降低 voltage 后，variation 和 droop margin 更紧；增加 clock gating 后，power-state verification 与 wake-up scheduling 更复杂。

这说明“compute wall”并非只靠更先进 process 解决。Architecture 会转向 specialized datapath、locality、sparsity、lower precision 与 software scheduling，因为减少不必要的数据移动和切换，往往比让所有 transistor 更快更有效。

## 13. Engineers actually say

- “We cannot close timing.”：至少一组受约束路径在目标 corner 没有足够 slack。追问 violation 类型、corner、endpoint 与预计修复对 power/area 的影响。
- “The path is wire-dominated.”：cell delay 已不是主项，floorplan、placement、routing 或 hierarchy 需要改变。
- “Clock power is too high.”：大量 sequential load 与 clock tree switching 正侵蚀 power budget；追问 gating coverage 与 useful activity。
- “We need another stage.”：团队考虑用 latency、state 与 verification 成本交换 frequency。
- “Typical silicon is fine.”：这不等于 production signoff；追问 slow corner、temperature、droop、aging 与 binning。

## 14. Engineering → Strategy

| Engineering change | System effect | Product effect | Business implication |
|---|---|---|---|
| 更高 frequency + voltage | power density 上升 | cooling/VRM 要求提高 | rack 可部署量与 TCO 可能恶化 |
| 更深 pipeline | throughput 潜力提高 | latency 与控制复杂度增加 | workload 适配决定 benchmark 外推性 |
| 更激进 low-voltage | 能效提高 | variation 与 binning 敏感 | yield、qualification、fleet policy 重要 |
| hierarchy / replication | wire delay 下降 | area 与 coherence 增加 | architecture know-how 难由 spec 看出 |
| power gating | idle power 下降 | wake-up 与验证复杂 | software/firmware 成为交付条件 |

真正难复制的部分往往不是某个 gate，而是 architecture、physical implementation、signoff methodology、silicon characterization、binning 与 runtime power management 的闭环。

## 15. Diligence questions

1. 目标 frequency 对应哪个 voltage、temperature、process corner 与工作模式？
2. 是所有 block 同频，还是多个 clock/voltage domain？
3. Critical paths 是 logic-dominated 还是 wire-dominated？
4. Timing margin 是否包含 droop、aging、jitter 与 on-die variation？
5. Peak benchmark 是否依赖高于量产默认值的 frequency 或 power mode？
6. Clock gating 与 power gating 覆盖率如何测量？
7. Silicon bring-up 后改变了哪些 guardband？
8. Binning 分布和最低可售 bin 的 economics 如何？
9. Pipeline 改动对 latency、branch/replay 与 software scheduling 有何影响？
10. 哪些结论来自 pre-silicon model，哪些已有 production silicon 证据？

## 16. Takeaways

1. 数字逻辑依赖连续电压、有限 delay 与噪声 margin，不是无成本的抽象 0/1。
2. Clock period 是一份 end-to-end timing budget；frequency 只是其倒数。
3. Pipeline 用 latency、寄存器和控制复杂度换 throughput 潜力。
4. 动态功耗受 activity、capacitance、voltage 平方和 frequency 共同影响。
5. Timing、power、thermal、yield 与 workload utilization 必须一起判断。

## Primary sources

- [Primary Source] [Berkeley：Digital Integrated Circuits 参考书与研究入口](https://people.eecs.berkeley.edu/~bora/Copy%20of%20publications.html)
- [Primary Source] [IEEE IRDS 2024：Emerging Logic and Alternative Information Processing Devices](https://irds.ieee.org/images/files/pdf/2024/2024IRDS_BC.pdf)
- [Primary Source] [AMD/Xilinx：I/O and Clock Planning Design Flow](https://docs.amd.com/r/2024.1-English/ug899-vivado-io-clock-planning/I/O-and-Clock-Planning-Design-Flow-Steps)


## 基础概念桥接

先区分数值表示、组合逻辑、时序状态、时钟、流水线与测量误差。工程上相同功能可有不同 timing、power、area 和 reliability；公式成立也不代表测量边界正确。先做量纲与数量级检查，再进入电路或架构细节。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。
