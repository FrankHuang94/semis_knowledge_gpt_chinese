# Technical Interview Field Guide：从口语信号判断技术成熟度

同一句“我们已经验证”可能表示仿真通过、实验室样片工作、客户正在评估，也可能表示大规模生产运行。技术访谈需要同时尊重工程师的上下文，又把压缩语言还原为可判断状态。

## 五条访谈轨道

### 一、Problem 与 workload

要求一个具体客户场景：输入、输出、规模、SLO、现有方案和最痛 failure。若回答始终停留在“市场需要更快”，说明需求边界尚不清楚。继续问 workload distribution，而非只问最佳样本。

### 二、Architecture 与 why-not

请对方画 dataflow，并说明至少两个未采用方案。成熟团队通常能说出自己方案的劣势、适用边界和历史决策；只描述优点可能意味着设计尚未经过真实约束。

### 三、Measurement 与 falsifier

询问测量点、版本、配置、误差和重复性。让对方给出一个会让自己改变判断的结果。不能被证伪的“更高效”“更灵活”不是工程主张。

### 四、Manufacturing 与 deployment

把“works”拆为 simulation、emulation、tapeout、first silicon、bring-up、qualification、sampling、production、shipping 和 deployed。对于系统产品，还要问 installation、commissioning、failure recovery、upgrade 和 support staffing。

### 五、Economics 与 ownership

追踪 BOM、yield、utilization、software effort、spares 和 customer migration。问哪一项由公司控制，哪一项依赖 foundry、memory、substrate、标准组织或客户环境。技术优势若依赖不可控 constraint，其商业兑现率应折价。

## Signal table

| 回答信号 | 可能含义 | 跟进 |
|---|---|---|
| 给范围和条件，不只给单点 | 理解 variation | 要求分布与边界样本 |
| 主动提供失败案例 | 有真实迭代闭环 | 问 root cause 与防复发 |
| 能解释 why-not | 设计空间经过比较 | 询问条件变化后的切换点 |
| 频繁依赖“未来软件” | silicon feature 尚未兑现 | 查 operator coverage 与日期 |
| 用客户 logo 代替规模 | 商业状态可能被放大 | 问 workload、数量和持续时间 |
| 回避逐站良率或 P99 | 平均指标掩盖风险 | 请求 waterfall 与原始日志 |
| 所有风险都由 partner 负责 | ownership 模糊 | 画接口与 escalation path |

这些是调查方向，不是自动定罪。初创团队早期缺少数据很正常，关键是能否诚实定义未知、设计学习计划并按期关闭。

## 交叉验证

同一问题分别问 architecture、software、manufacturing、sales 和 customer-support 团队。答案不完全一致很正常；真正风险是关键名词的定义、产品状态或责任边界互相冲突。对冲突建立 reconciliation table，不在会议中仓促选边。

访谈材料按证据等级处理：原始 log、spec 与 issue record 通常高于记忆；客户 reference 高于匿名 logo；重复测量高于单次 demo；真实目标产品高于 test vehicle。仍要注意每种证据都有 selection bias。

## 结束时必须带走什么

- 一张经对方纠正的 architecture/dataflow 图；
- 三个最高影响 dependency；
- 至少一个真实失败与修复；
- 关键 metric 的 boundary；
- 产品状态与 as-of date；
- 下一项证据、owner 和预计时间；
- 如果假设失败，价值迁移到哪里。

访谈结论应写成概率更新：“由于看到了什么，哪项假设从何种置信度变到何种置信度”，而不是“团队很强”或“工程师说没问题”。这使多个访谈可累积，也让后来者能审计判断。


## 基础概念桥接

工程师口语是压缩上下文。“跑满”“带宽够”“production ready”“良率很好”都必须还原为 metric、boundary、condition、status、evidence 和 falsifier。记录原话与自己的解释分开，再用 teach-back 校准。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。


## 进阶工程术语桥接

本篇进一步需要掌握：graph lowering、autotuning、ABI、firmware、observability、canary、fault injection 与 blast radius。阅读这些术语时，不只记中英文对应，还要补齐系统位置、正常路径、饱和或失败路径、直接 counter、端到端结果、产品状态和证据等级。若工程会议出现“已解决”“无开销”“已量产”，应立即追问 workload、boundary、configuration、status/date、failure mode 与 falsifier。

延伸阅读：[进阶工程术语手册](../31_glossary/advanced_engineering_terms_handbook.md)。
