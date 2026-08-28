---
id: engineer_language_decoder
title: Engineer Language Decoder：把口语主张变成 Metric、Boundary 与追问
concepts: [engineer_language, claim_decomposition, metric, system_boundary]
prerequisites: [technical_diligence, engineering_to_strategy]
level: [2, 3, 4, 5]
status: draft
last_verified: 2026-08-24
source_date: 2026-08-24
---

# Engineer Language Decoder：把口语主张变成 Metric、Boundary 与追问

工程师口语通常是高度压缩的context，不应按字面接受，也不应当作“营销”。正确动作是恢复被省略的workload、boundary、metric、condition、status与trade-off。

## 使用规则

听到一句话，按六步展开：

1. 哪个system boundary？
2. 哪个workload/traffic？
3. 哪个metric与statistic？
4. 相对哪个baseline？
5. 在什么condition/status/date？
6. 优化后bottleneck移到哪里？

## Performance

| 口语 | 可能含义 | 必问 |
|---|---|---|
| “跑满了” | 某pipe active或某counter高 | 是useful work、issue还是busy？ |
| “接近peak” | 特定precision/shape kernel高效 | end-to-end coverage多少？ |
| “memory bound” | HBM、cache、latency或capacity之一 | 哪层traffic/counter支持？ |
| “latency隐藏了” | ready work覆盖stall | timeline上exposed多少？ |
| “线性扩展” | 某scale range throughput近比例 | batch/quality/cost是否相同？ |
| “尾延迟可控” | p99在某load/SLO内 | arrival、queue与failure条件？ |

## GPU / Kernel

| 口语 | 翻译 | 必问 |
|---|---|---|
| “occupancy低” | resident warps受resource限制 | stall真因无ready warp？ |
| “Tensor Core用了” | 发射MMA instructions | feeding/epilogue与active cycles？ |
| “已经fusion” | 合并部分ops | traffic、spill与coverage变化？ |
| “访存连续” | 逻辑index邻近 | physical transactions/useful bytes？ |
| “compiler会优化” | 某pass可能识别pattern | shape/fallback/version？ |
| “只是个kernel问题” | local code可能限制 | system critical path占比？ |

## Memory / HBM

| 口语 | 翻译 | 必问 |
|---|---|---|
| “带宽够了” | average demand低于某ceiling | burst、efficiency、which level？ |
| “容量够用” | 某model/context/batch可放入 | fragmentation、checkpoint、headroom？ |
| “row hit很好” | access locality匹配open row | bank balance与tail呢？ |
| “cache解决了” | working set有reuse | miss path与traffic reduction？ |
| “加HBM就行” | memory wall被怀疑 | package、controller、software与power？ |
| “memory pooling” | remote/tiered capacity可访问 | latency、failure、placement policy？ |

## I/O / SerDes

| 口语 | 翻译 | 必问 |
|---|---|---|
| “link up” | training成功并建立连接 | BER、margin、temperature/aging？ |
| “channel有margin” | 在某test条件通过 | loss budget与worst corner？ |
| “PAM4翻倍” | symbol承载更多bits | baud、SNR、FEC与energy/bit？ |
| “retimer解决了” | 重置electrical budget | power、latency、topology与failure？ |
| “PCIe兼容” | 某generation/features通过 | performance、ordering、switch/IOMMU？ |
| “CXL ready” | PHY/protocol可能支持 | host firmware、memory tiering、qualified devices？ |

## Networking / Collectives

| 口语 | 翻译 | 必问 |
|---|---|---|
| “无损网络” | 通过flow control降低drop | PFC/ECN、deadlock、recovery？ |
| “网络没堵” | average port utilization低 | queue tail、incast、path collision？ |
| “RDMA绕过CPU” | data path减少host copy | registration、PCIe与control overhead？ |
| “collective已overlap” | 部分communication并行 | exposed bytes/time与shared HBM？ |
| “topology aware” | rank/path选择考虑连接 | failure/rebalancing与actual mapping？ |
| “all-reduce很快” | 某message/ranks benchmark | algorithm、protocol、contention？ |

## Optics

| 口语 | 翻译 | 必问 |
|---|---|---|
| “DSP-free” | module内删除某retiming DSP | host equalization/FEC责任？ |
| “CPO ready” | 某engine/package demo | qualification、laser、service、yield？ |
| “interoperable” | 通过某MSA/IA matrix | hosts/modules/temperature coverage？ |
| “lower power” | 某component boundary | laser/host SerDes/cooling含吗？ |
| “long reach” | 某fiber/FEC/BER条件 | engineering reserve？ |
| “光取代铜” | conversion point向silicon移动 | 哪个reach/cost/service segment？ |

## Packaging / Chiplet

| 口语 | 翻译 | 必问 |
|---|---|---|
| “yield benefit” | smaller die可能提高yield | final good-package cost？ |
| “known-good-die” | 通过某pre-bond tests | high-speed/thermal coverage？ |
| “reticle-busting” | package span超单die | routing、power、yield？ |
| “UCIe compatible” | 某layer遵循标准 | coherence、boot、package互操作？ |
| “hybrid-bond ready” | process capability存在 | volume、defect、alignment？ |
| “3D bandwidth高” | vertical link density高 | heat、power与payload efficiency？ |

## Power / Thermal / Rack

| 口语 | 翻译 | 必问 |
|---|---|---|
| “rack power” | input/IT/silicon之一 | boundary与peak/transient？ |
| “N+1” | 某层多一个unit | shared bus/controller/feed？ |
| “liquid cooled” | 部分components接液 | heat fraction与remaining air？ |
| “cooling capacity” | 特定flow/temp/pressure | redundancy与approach？ |
| “high density” | 更多IT power/space | service、weight、facility与goodput？ |
| “factory integrated” | 部分assembly/test前置 | site commissioning还需什么？ |

## Manufacturing / Supply

| 口语 | 翻译 | 必问 |
|---|---|---|
| “良率很好” | 某yield达到内部阈值 | denominator、bin、maturity？ |
| “产能翻倍” | nominal/installed/qualified之一 | mix、good output与date？ |
| “sold out” | reservation/commit高 | take-or-pay、priority与downstream？ |
| “双源” | design或qualification存在 | ready volume与switch time？ |
| “量产” | process进入某生产状态 | weekly good units/customer shipments？ |
| “lead time改善” | 某区段缩短 | queue、cycle、transport还是qualification？ |

## Software / Platform

| 口语 | 翻译 | 必问 |
|---|---|---|
| “framework支持” | 能correctness运行 | performance/shape/precision coverage？ |
| “portable” | code或IR可迁移 | performance与custom ops？ |
| “自动调优” | search/cost model选variant | warm-up、cache与reproducibility？ |
| “平台” | 多层产品被统一 | control point与switching cost？ |
| “开放” | 某interface公开 | implementation/qualification/software是否可替换？ |
| “backward compatible” | 某API/ABI保持 | performance、semantics与support window？ |

## Business / Strategy

| 口语 | 翻译 | 必问 |
|---|---|---|
| “TCO更低” | 特定cost/useful output模型 | inputs、utilization、time horizon？ |
| “客户需求强” | pipeline/order/deployment之一 | paid、renewal、expansion？ |
| “技术护城河” | 某能力难复制 | duration、substitute、bypass？ |
| “供应有保障” | contract或allocation | qualified good output与期限？ |
| “市场标准” | adoption或formal spec | installed base、compliance与control？ |
| “规模经济” | fixed cost摊薄或learning | utilization、yield与diseconomies？ |

## Meeting Notes 模板

| 字段 | 记录 |
|---|---|
| 原话 | |
| Speaker / function | |
| 可能含义 | |
| Boundary / workload | |
| Metric / baseline | |
| Evidence / status / date | |
| Follow-up | |
| Falsifier | |
| Strategy implication | |

## 小结

Decoder的目标不是挑语病，而是把compressed expertise恢复成可验证模型。好的追问具体、尊重context，并能帮助工程师指出真正constraint。


## 基础概念桥接

工程师口语是压缩上下文。“跑满”“带宽够”“production ready”“良率很好”都必须还原为 metric、boundary、condition、status、evidence 和 falsifier。记录原话与自己的解释分开，再用 teach-back 校准。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。


## 进阶工程术语桥接

本篇进一步需要掌握：graph lowering、autotuning、ABI、firmware、observability、canary、fault injection 与 blast radius。阅读这些术语时，不只记中英文对应，还要补齐系统位置、正常路径、饱和或失败路径、直接 counter、端到端结果、产品状态和证据等级。若工程会议出现“已解决”“无开销”“已量产”，应立即追问 workload、boundary、configuration、status/date、failure mode 与 falsifier。

延伸阅读：[进阶工程术语手册](../31_glossary/advanced_engineering_terms_handbook.md)。
