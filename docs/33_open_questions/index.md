# Open Questions：用可证伪问题管理未知

本目录记录行业仍未解决、公开资料不足或存在多种可行路径的问题。问题不是“以后再研究”的停车场，而是带有决策影响、当前证据、候选解释、falsifier、owner 与 review trigger 的研究队列。

## 问题卡片格式

每个问题必须回答：

- **Decision relevance**：答案会改变哪项采购、投资、合作或架构选择？
- **Current belief**：目前最可能的解释及置信度；
- **Constraints**：physics、architecture、software、manufacturing、supply 与 ecosystem 边界；
- **Alternatives**：至少两个可行路径，以及各自 why-not；
- **Evidence gap**：缺少哪类 primary 或 independent evidence；
- **Falsifier**：什么观察会推翻当前判断；
- **Value migration**：若某一路径成功，利润、IP、产能和控制点移向哪里；
- **Owner / trigger**：谁在何种事件后复核。

~~~mermaid
flowchart LR
  D[Decision] --> Q[Open question]
  Q --> H[Competing hypotheses]
  H --> E[Evidence plan]
  E --> U[Belief update]
  U --> A[Article / product / case]
  U --> Q
~~~

## Active backlog

### 一、Electrical I/O scaling 的经济边界在哪里？

更高符号率节省 lane 与 package edge，却提高 equalization、retimer、功耗和 validation 成本。需跟踪真实 channel reach、BER margin、connector/cable ecosystem 与每个 delivered bit 的系统成本。若 optics 或更短 reach chiplet link 提前跨越成本点，价值将从传统 electrical PHY 向 photonics、packaging 或 switch architecture 移动。

### 二、Memory wall 会由哪一层首先缓解？

候选路径包括更大 HBM、片上 SRAM、compression、sparsity、CXL tiering、PIM 和模型结构改变。单项改善会把瓶颈移到 capacity、latency、software placement 或 power。关键证据不是峰值带宽，而是目标 workload 的 bytes moved、reuse 与端到端 cost per useful token。

### 三、GPU 与 rack power 是否逼近设施可部署上限？

芯片额定功率增长并不自动等于更高可用算力。需要观察负载瞬态、rack distribution、liquid-cooling adoption、utility interconnect 和 commissioning cycle。若 facility lead time 比 silicon cadence 更慢，价值可能迁移到 power delivery、cooling、site selection 和 workload efficiency。

### 四、HBM thermal 与 stack height 的共同边界是什么？

更高堆叠提高容量，却增加热路径、机械应力、bonding 和 test 难度。关键未知是目标产品的温度分布、repair/test strategy 与 volume yield，而不是单个 technology vehicle。

### 五、CPO manufacturability 何时超过 pluggable 的运营优势？

CPO 可缩短 electrical reach，却把 optics、laser、package test 与 field service 绑在一起。需要观察可更换性、fiber attach、known-good strategy、laser architecture 和客户维护数据。量产发布不等于 fleet economics 已成立。

### 六、Chiplet interoperability 会停在 electrical compatibility 还是到达可组合市场？

标准接口可定义 signaling 和 protocol，但 timing、power、thermal、security、debug、yield ownership 与 commercial warranty 仍需共同解决。若多数产品继续由单一厂商闭环，标准价值更可能是内部复用而非开放 marketplace。

### 七、Scale-up topology 的最佳边界会随模型如何变化？

全连接、switch-based 与分层 topology 在 latency、bandwidth、radix、fault isolation 和 cable complexity 上取舍不同。MoE、long-context 与 inference batching 会改变 traffic。需要用真实 collective trace 和 failure recovery，而非只比较 bisection bandwidth。

### 八、Optical I/O 会先进入哪一层？

候选入口包括 board edge、package edge、die-to-die 与 memory fabric。越接近 compute，electrical savings 越大，thermal、laser delivery、assembly 和 test 越困难。关键触发器是可靠量产、可维护封装和系统级能效，而非单链路 demo。

### 九、PIM adoption 的 software contract 是什么？

把计算靠近 memory 可减少 data movement，却要求 programming model、coherence、precision、debug 和 workload stability。若 operator 演进快于 hardware cycle，通用 accelerator 仍可能胜出。需寻找重复部署、compiler support 与客户迁移成本证据。

### 十、AI Ethernet 能否在大规模训练中实现可预测尾延迟？

标准生态和供应商选择是优势，但 congestion control、telemetry、buffer、routing 与 operations 必须协同。关键验证是 incast、故障与多租户条件下的 step-time distribution，而非单流吞吐。

### 十一、先进封装 constraint 会从设备移向材料还是 test？

扩产某一 bonding tool 后，substrate、HBM、carrier、underfill、probe、socket 或 reliability qualification 可能成为下一约束。需要逐站 yield、WIP、cycle time 与 supplier qualification 数据建立 constraint map。

### 十二、Accelerator software moat 如何量化？

operator coverage、compiler quality、kernel library、debug、deployment 和 developer habit 共同形成 moat。下载量或 benchmark 数量都不充分。更好的 leading indicators 是新模型 time-to-first-run、无手改覆盖、升级成功率、回归关闭时间和客户自助率。

## 复核节奏

- **事件触发**：新标准版本、first silicon、qualification、shipping、重大客户部署或 field failure；
- **时间触发**：高影响问题至少季度复核，低影响问题半年复核；
- **结论触发**：置信度显著改变时，必须同步更新相关 article、product record、case study 与 strategy implication；
- **关闭条件**：不是“已有答案”，而是剩余不确定性不再影响当前决策。关闭时保留历史假设和导致更新的证据。

任何 open question 若没有 falsifier 和 next evidence，只是主题名称；任何结论若没有 review trigger，很快会变成过期事实。
