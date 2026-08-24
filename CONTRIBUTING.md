# 贡献与写作规范

## 先做 gap analysis

新增内容前先检查：已有解释在哪里、读者需要哪些 prerequisite、需要深化的是 intuition、architecture、quantitative analysis 还是 strategy。除非存在独立学习目标，不要为一个术语新建短页面。

## WHY → HOW → WHAT

文章首先回答“如果没有它会怎样”“问题为什么存在”，再进入实现与定义。默认使用：

```text
Problem → Constraint → Alternatives → Choice → Implementation
→ Trade-off → New Bottleneck → System Effect → Strategy
```

## Major article checklist

- front matter 包含 id、title、concepts、prerequisites、level、status、last_verified
- 顶部给出三次阅读建议
- system position、architecture、dataflow、trade-off visual 各至少一个
- 解释关键 equation 的变量、单位、适用边界
- 至少 2–4 个 design alternatives 和 3 个 why-not
- 包含 workload mapping、engineer language、misconceptions
- 包含 Engineering → Strategy 表与 diligence questions
- 事实和数字就近引用，来源录入 references
- 不确定时写“当前公开资料不足”，不得补猜数字

## 语言

解释性正文以中文为主。标准工程术语保留英文；第一次出现可写“算术强度（Arithmetic Intensity）”，后续直接使用英文。避免生造现实工程交流中不用的译名。

## Sources

优先 IEEE/ACM、会议论文、标准组织与厂商 architecture paper。Marketing material 只能支持“厂商声称”，不能自动视为独立事实。引用格式见 `references/README.md`。

## Pull request / commit scope

每次提交应形成可理解的知识增量；结构、内容、生成物尽量分开。更新文章时同步检查 backlinks、concept metadata、navigation、quiz 与 glossary。
