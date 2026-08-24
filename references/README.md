# Citation Framework

引用的目的不是装饰 bibliography，而是让读者区分“公开事实、厂商主张、估算与推断”。

## 标签

- **[Primary Source]**：标准组织、同行评审论文、会议论文、厂商正式 architecture paper、datasheet。
- **[Independent]**：可信的第三方 engineering research 或测量。
- **[Vendor Claim]**：厂商 performance、efficiency、readiness 或 roadmap 主张，尚未独立验证。
- **[Estimate]**：给定假设下的计算；必须列输入与公式。
- **[Inference]**：由公开 block diagram、spec 或产业信息推导；明确说明推理链和替代解释。

## 就近引用

关键数字和产品状态在同一句或同一段落引用，不把所有 URL 堆在文末后让读者猜对应关系。Major article 文末仍保留按主题分组的 sources，便于复查。

## Source record

建议字段：`id`、`title`、`organization`、`url`、`published`、`accessed`、`source_type`、`supports`、`notes`。

## Freshness

产品文章 front matter 必须有 `last_verified`、`source_date`、`product_status`。Roadmap 与 rumored 信息不得写成已量产事实。规格冲突时保留冲突并解释口径，而不是静默选择一个数字。
