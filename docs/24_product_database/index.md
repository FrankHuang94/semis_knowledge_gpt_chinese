# Product Database

产品记录以 status 和 `last_verified` 为核心，严格区分 Announced、Sampling、Production、Shipping、Deployed、Roadmap 与 Rumored。

## 当前 validated records

| Product / Platform | Company | Category | Status |
|---|---|---|---|
| GB200 NVL72 | NVIDIA | rack-scale system | Shipping |
| Instinct MI355X | AMD | datacenter GPU | Production |
| EC2 Trn2 | AWS | cloud accelerator instance | Deployed |
| Cloud TPU Ironwood | Google | cloud accelerator | Deployed |
| BlueField-3 / ConnectX-8 | NVIDIA | DPU / SuperNIC | Deployed |
| CoWoS Platform | TSMC | packaging service | Production |
| Gaudi 3 | Intel | AI accelerator | Shipping |
| Neoverse CSS V3 | Arm | compute subsystem IP | Announced |
| HBM3E 8H | Samsung | high-bandwidth memory | Production |
| Tomahawk 6 | Broadcom | Ethernet switch ASIC | Shipping |
| Scorpio X-Series | Astera Labs | AI fabric switch | Production |
| HiWire AEC | Credo | active electrical cable | Production |
| CoolChip CDU family | Vertiv | liquid cooling | Announced |

完整 architecture、old/new bottleneck、missing disclosures 与 sources 见 [data/products.yaml](https://github.com/FrankHuang94/semis_knowledge_gpt_chinese/blob/main/data/products.yaml)。

## Generation time series

[data/product_generations.yaml](https://github.com/FrankHuang94/semis_knowledge_gpt_chinese/blob/main/data/product_generations.yaml) 把 generation、milestone date、status 与 relation 分开，当前覆盖 Tomahawk、Samsung HBM3E、Astera Scorpio 与 Arm Neoverse CSS。它解决两个常见错误：

1. 用 successor 的发布替代 predecessor 的真实 deployment；
2. 把 Sampling、initial Production 与 broad Shipping 合并成一个“已量产”。

例如 Scorpio 的 2024 pre-production、2026 initial production 与更高 radix 版本 shipping 是三个不同 milestone；数据库保留每个时间点，而不是覆盖旧状态。[Primary Source]

## 使用纪律与复核

Status 不是质量评分；Shipping 不等于 large-scale Deployed。任何性能比较回到 workload、software、power、system boundary 与 date。高波动记录默认每 90 天复核一次，[Estimate]，watchlist 见 [data/source_reviews.yaml](https://github.com/FrankHuang94/semis_knowledge_gpt_chinese/blob/main/data/source_reviews.yaml)。
