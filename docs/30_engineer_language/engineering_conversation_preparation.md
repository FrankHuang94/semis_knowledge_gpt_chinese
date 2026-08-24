# Engineering Conversation Preparation：把一次会议设计成证据采集

和工程师交流的目标不是证明自己懂术语，而是在有限时间内定位约束、理解选择并取得可复查证据。好问题来自预先画出的 system boundary；坏问题往往过宽，使回答者只能复述宣传材料。

## 会前：建立假设树

先写一句决策：这次对话要支持采购、投资、合作、产品规划还是故障诊断。随后建立三层假设：

1. **价值假设**：客户指标真的改善吗？
2. **机制假设**：改善来自哪段 dataflow？
3. **兑现假设**：软件、制造、供应和部署能否持续交付？

~~~mermaid
flowchart TB
  D[Decision] --> V[Value hypothesis]
  V --> M[Mechanism]
  M --> X[Execution dependencies]
  X --> E[Evidence request]
  E --> F[Falsifier]
~~~

准备一张最小架构图，把 workload、state、bytes、控制路径和测量边界标出。对每个未知项写“若答案为否，决策是否改变”。不会改变决策的问题降低优先级。

## 会中：使用漏斗而不是审讯

先让对方描述真实 workload 和 failure story，再逐步缩小到 metric、条件与证据。推荐顺序：

- “客户在没有这个功能时，首先在哪里失败？”
- “你们考虑过哪些替代方案，为什么没有选？”
- “这个数字从哪里量，包含哪些组件？”
- “在什么 shape、温度、软件版本或良率下不成立？”
- “解决后，瓶颈移动到哪里？”
- “能否给一个最近的反例或回归？”
- “下一条会改变你判断的证据是什么？”

记录原话与自己的解释分开。数字旁边立即写 unit、boundary、configuration、date 和 evidence owner；听不懂时用 teach-back：“我的理解是……如果我画这条路径是否正确？”这比用另一个术语掩盖误解更有效。

## 处理模糊表达

“跑满”要拆成执行单元利用率、memory bandwidth、tokens per second 或 business SLO；“production ready”要拆成状态、规模、持续时间、客户数量和支持模式；“yield 很好”要拆成哪一站、哪一产品、起始基数与趋势；“TCO 更低”要拆成分子、分母、利用率和时间范围。

当回答者说“这不是问题”时，不急于反驳，追问“由哪一层吸收”“谁监控”“在何种规模下验证”。很多架构优势本质上是把复杂度转移给 compiler、operations 或供应链。

## 会后：二十四小时内完成闭环

1. 将 notes 转成 claim ledger，不保留只有形容词的句子；
2. 标记 source class、confidence 与缺口；
3. 对照已有文章、产品记录和 interface schema；
4. 用简单算术检查数量级；
5. 写出 contradictions 与 alternative explanations；
6. 发送少量高价值 follow-up，而不是整份问卷；
7. 把未解决项送入 open questions，并设置 review trigger。

## 为什么不问完整清单

长问卷看似严谨，却容易得到法务化、不可追问的回答；纯自由讨论有深度，却可能漏掉关键边界。chosen design 是“固定骨架 + 自适应深挖”：所有会议都覆盖 workload、metric、boundary、status、evidence 和 falsifier，但把时间集中在最影响决策的两三个假设上。

## 质量自检

- 结论是否明确区分事实、厂商主张、估算和推断？
- 是否获得至少一个 why-not 与一个真实 failure mode？
- 是否知道谁拥有下一步证据以及何时可获得？
- 是否记录对方最强反对意见？
- 是否能用一张图向未参会者复述 dataflow？
- 会议是否真正改变了某个概率或决策？

成熟的工程对话不以问题数量衡量，而以不确定性下降和错误假设被及时暴露来衡量。
