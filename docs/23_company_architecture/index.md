# Company Architecture Database

这里不按市值或新闻热度描述公司，而是记录它控制哪些 architecture layers、依赖哪些 manufacturing steps、软件生态与客户 switching cost 在哪里。

## 当前覆盖

| Ecosystem layer | Companies | 主要 control points |
|---|---|---|
| Accelerators / systems | NVIDIA、AMD、Intel、AWS、Google | compute、scale-up、compiler、cloud deployment |
| CPU IP / custom silicon | Arm、Broadcom、Marvell | CPU subsystem、SerDes、switch/custom ASIC |
| Foundry / packaging | TSMC、Intel、Samsung | process、yield、2.5D/3D packaging、capacity |
| HBM / memory | SK hynix、Micron、Samsung | DRAM process、stacking、test、qualification |
| Connectivity | Broadcom、Marvell、Astera Labs、Credo | switch、retimer、CXL/PCIe、AEC、optical DSP |
| Power / cooling | Vertiv、Schneider Electric | rack/facility power、CDU、controls、service |

## 如何读公司记录

每家公司都拆成 architecture control points、manufacturing dependencies、software ecosystem、customer switching cost、supplier dependencies、moat hypotheses 与 diligence questions。这里的 moat 一律是待验证假设，不是结论。

例如，Astera Labs 的“连接性组合 + diagnostics”只有在多代平台 qualification、firmware lifecycle 与 field telemetry 能持续缩短客户导入时间时才可能形成防御性；Vertiv 或 Schneider Electric 的“全设施方案”也必须落到 commissioning、service response、spares 和跨电气/热控制回路的实际集成。

完整字段与 primary sources 见 [data/companies.yaml](https://github.com/FrankHuang94/semis_knowledge_gpt_chinese/blob/main/data/companies.yaml)。

## Freshness policy

每条记录必须有 `last_verified` 与 `sources`。公司层默认每 180 天复核一次，[Estimate]；发生 annual report、重大架构变化、并购或供应链变化时立即触发复核。高波动产品与标准的具体队列见 [data/source_reviews.yaml](https://github.com/FrankHuang94/semis_knowledge_gpt_chinese/blob/main/data/source_reviews.yaml)。
