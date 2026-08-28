# Conference Learning Loop：从一场演讲变成可维护知识

会议材料的价值不在于当天记住多少缩写，而在于能否把新主张放进已有 knowledge graph，并随着产品状态、标准和制造证据变化持续更新。Hot Chips、ISSCC、OFC、SC、GTC 与 OCP 的信息类型不同：架构会议强调 design choice，电路会议强调实现，光通信会议强调 link 与器件，开发者会议常混合产品发布和软件生态。统一摘录会丢失这些边界。

## 六阶段工作流

~~~mermaid
flowchart LR
  I[Inbox] --> E[Extract claims]
  E --> P[Prerequisite map]
  P --> B[Backlinks]
  B --> U[Product / case update]
  U --> S[Strategy implication]
  S --> O[Open questions]
  O -.新证据.-> E
~~~

### 一、Capture：保存可复查的原始边界

记录会议、日期、session、speaker、organization、材料 URL、页码或时间戳。截图不是证据终点；要保存可定位的 deck、paper、video 或 transcript。若内容只在现场口头出现，明确标为 [Vendor Claim] 并记录听取时间，不把它升级为事实。

### 二、Extract：把叙事拆成原子主张

每条 claim 只描述一个可判断命题，并强制填写 metric、unit、boundary、condition、product status、as-of date 与 evidence class。例如“带宽翻倍”必须追问接口还是系统、单向还是双向、峰值还是持续、何种编码和配置。没有这些字段的摘录进入待补证队列，而不是正文。

### 三、Prerequisite：补齐理解依赖

新术语常建立在旧概念上。先链接 memory hierarchy、SerDes、packaging、power 或 compiler 等前置文章，再决定是否需要新页面。若一个概念只是一篇 cornerstone 的局部机制，应补段落与 backlink，不应制造短小孤岛。

### 四、Reconcile：与已有记录对账

对照 company、product、standard 与 interface database。相同产品的新名称可能只是 marketing rename；相同指标可能改变 precision、sparsity 或 system boundary；roadmap 日期也可能滑动。更新时保留旧记录和日期，形成时间序列，不覆盖历史。

### 五、Translate：从技术变化到系统与策略

强制写出：解决了什么 bottleneck；牺牲什么；为何不用替代方案；新瓶颈移到哪里；谁控制 IP、capacity、qualification 和 ecosystem；哪些收入池扩大或被压缩。这一步防止“新功能列表”冒充战略分析。

### 六、Close or carry：关闭或进入 open questions

若证据足以支持结论，更新正文、案例和 glossary；若仍缺独立验证，建立 open question，写清下一条能改变判断的证据。开放问题必须有 owner、review date 与触发器，否则会变成遗忘清单。

## 一次处理的最小产物

- 一份结构化 inbox note；
- 至少一个 prerequisite/backlink；
- 需要时更新 product status 或 generation lineage；
- 一段 strategy implication；
- 零至数个可证伪 open questions；
- source freshness 日期。

## 为什么不追求实时全覆盖

直播式记录速度快，却容易复制厂商语言并产生重复页面；等所有资料齐全再写最严谨，却会错过决策窗口。chosen design 是两速系统：当天建立带证据等级的 provisional note，随后在固定 review window 内完成核验。未核验内容不进入 authoritative table。

## 质量闸门

1. 是否能回到原始页码或时间戳？
2. 是否区分 announced、sampling、production、shipping、deployed、roadmap 与 rumored？
3. 数字的单位、条件和 system boundary 是否完整？
4. 是否寻找反例、替代解释或独立证据？
5. 是否更新相关 backlink，而非只新增孤页？
6. 三个月后其他人能否复现当时为何得出该判断？

会议处理速度不是目标；被后续证据校正的成本、漏掉的重要变化和错误传播范围才是更好的运营指标。

## 资料

- [Hot Chips Symposium](https://hotchips.org/) [Primary Source]
- [IEEE ISSCC](https://www.isscc.org/) [Primary Source]
- [OFC Conference](https://www.ofcconference.org/) [Primary Source]
- [Open Compute Project](https://www.opencompute.org/) [Primary Source]


## 基础概念桥接

演讲材料同时包含机制、规格、路线图和营销，四者证据门槛不同。记录页码、时间戳、status 与 as-of date；把 claim 拆成原子命题，更新 prerequisites、backlinks、product lineage、strategy implication 和 open questions。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。
