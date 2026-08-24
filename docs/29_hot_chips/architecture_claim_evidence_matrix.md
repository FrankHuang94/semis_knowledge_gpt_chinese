# Architecture Claim Evidence Matrix：如何给发布会主张分配置信度

架构演讲通常同时包含机制、规格、路线图和商业定位。四者不能使用同一种证据标准。机制可以通过 dataflow 和约束推导；规格需要条件完整的官方文件；路线图需要时间标签；商业价值还要有客户部署、制造和成本证据。

## 证据矩阵

| 主张类型 | 最低可接受证据 | 常见误判 | 下一步 |
|---|---|---|---|
| 架构机制 | 方框图、接口定义、compiler/runtime 路径 | 把模块名称当成真实 dataflow | 画出 bytes、state 与 control |
| 峰值规格 | 带 dtype、sparsity、configuration 的表格 | 不同边界直接相除 | 建 performance waterfall |
| 系统性能 | workload、batch、shape、SLO、软件版本 | kernel benchmark 代替服务 | 复现端到端 trace |
| 功耗与能效 | measurement point、稳态/峰值、冷却边界 | TDP 当电表读数 | 追到 rack 与 facility |
| 制造与供货 | qualification、yield、产能、ship evidence | announced 当 shipping | 建状态和日期序列 |
| 经济价值 | 可用吞吐、利用率、维护与迁移成本 | BOM 当 TCO | 建 sensitivity 与 falsifier |

## Claim ledger

每条主张使用如下结构：

- **原文**：不改变语气地摘录；
- **规范化命题**：主体、动作、对象、边界、时间；
- **Evidence class**：[Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]；
- **Status / as-of**：产品状态和核验日期；
- **Dependencies**：成立需要哪些软件、器件、制造和客户条件；
- **Falsifier**：看到什么证据就降低置信度；
- **Decision impact**：该主张若真或假，会改变哪个决策。

置信度不是给厂商打分，而是暴露“我们凭什么相信”。同一厂商可以在架构机制上高置信、量产日期上低置信。

## 典型冲突如何处理

**官方数字与第三方测试不同**：先对齐精度、batch、系统规模、软件版本和 power boundary；若仍不同，保留两者，不求平均值。

**paper 与产品不同**：paper 证明可能性，不证明 shipping implementation。检查 die photo、software exposure、product manual 和客户可访问性。

**路线图前后变化**：保留每次声明的日期与措辞，将延期本身视为执行证据。不要用最新页面覆盖旧承诺。

**客户 logo 与部署不同**：logo 可能代表评估、合作或采购。只有 workload、规模、时间与生产状态足够清晰时，才标记 deployed。

## 从矩阵到决策

将关键主张按“影响 × 不确定性”排序。高影响、高不确定性的项目优先设计验证；低影响项目不应耗费同等 diligence。验证也要考虑成本：能用 source reconciliation 解决的，不一定需要昂贵 benchmark；能由客户 reference call 证伪的，不必先建完整实验室。

最终结论应包含 base、upside 与 downside case。upside 只能使用尚未证实但有路径的假设；base 使用当前可验证状态；downside 把最关键 dependency 失败后的 value migration 写清。这样 conference note 才能进入投资、采购或合作决策，而不是停在“很有意思”。

## 快速复核问题

1. 这是 mechanism、spec、status 还是 economics claim？
2. 来源能否支持当前句子的精确边界？
3. 数字是否通过算术和物理 sanity check？
4. 是否存在产品代际或命名混淆？
5. 哪个独立观察最能降低不确定性？
6. 结论过期时由什么事件触发复核？
