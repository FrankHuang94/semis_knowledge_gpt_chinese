---
id: roofline_model
title: Roofline Model：把 Peak FLOPS、Memory Bandwidth 与 Workload 放到同一张图
concepts: [roofline, arithmetic_intensity, compute_bound, memory_bound]
prerequisites: [matrix_multiplication, memory_hierarchy, bandwidth, gpu]
level: [2, 3, 4]
status: draft
last_verified: 2026-08-24
source_date: 2026-08-24
---

# Roofline Model：把 Peak FLOPS、Memory Bandwidth 与 Workload 放到同一张图

> 第一次阅读：Sections 1–8  
> 第二次阅读：Sections 9–18  
> 深入阅读：Sections 19–26

## 阅读前后

读前需要FLOP/s、bytes/s、[Memory Hierarchy](memory_hierarchy.md)与GEMM；读后应能计算Arithmetic Intensity、ridge point与performance upper bound，并知道Roofline是方向盘而非预测器。

## 1. 为什么需要它

Peak FLOPS只说明算术管线，memory bandwidth只说明供给。Application performance取更紧约束。Roofline把workload每byte运算量、compute roof与memory roof放到同一图。

## 2. 一句话直觉

每搬一个byte做得越少，越受bandwidth限制；复用足够高后，compute peak才成为上限。

## 3. 图怎么读

~~~mermaid
flowchart LR
  L[Low AI<br/>memory-bound] --> R[Ridge point]
  R --> H[High AI<br/>compute-bound]
  BW[Bandwidth raises slope] --> L
  CP[Compute raises flat roof] --> H
~~~

真实图使用log-log axes，斜线 \(BW\times AI\) 与水平线 \(P_{peak}\) 相交。

## 4. 定义

\[
AI=\frac{\text{useful operations}}{\text{bytes across chosen boundary}}
\]

Boundary可以是HBM、L2、L1、host-device或network；不同boundary得到不同AI。Operations也必须说明FLOP、integer、tensor与sparse counting。

## 5. 第一性原理

\[
T\ge\max\left(\frac{F}{P_{peak}},\frac{Q}{BW}\right)
\]

\[
P_{\text{attainable}}\le\min(P_{peak},BW\times AI)
\]

运算不能快过算术资源，数据不能快过供给。

## 6. Follow the Data

~~~mermaid
flowchart LR
  H[HBM bytes Q] --> C[Cache / tile]
  C --> O[Operations F]
  R[Reuse/fusion/batch] -->|raises AI| C
  B[Bandwidth] -->|sloped roof| O
  P[Compute peak] -->|flat roof| O
~~~

Tiling、fusion、batching减少远端bytes使点右移；更快HBM抬斜roof；更多matrix units抬平roof。

## 7. 三方 contract

| 输入 | 来源 | 风险 |
|---|---|---|
| Compute roof | datatype/frequency/units | marketing peak |
| BW roof | spec或microbenchmark | raw非sustained |
| AI | workload/counters | ideal非realized |
| Achieved | profiler | counting不一致 |

## 8. Parameters

AI、peak/achieved FLOP/s、peak/achieved GB/s、ridge point、cache traffic、precision、batch/shape、power state必须一起报告。

## 9. Worked example

[Estimate] 假设compute roof 1 PFLOP/s、sustained HBM 4 TB/s：

\[
AI_{\text{ridge}}=10^{15}/(4\times10^{12})=250\text{ FLOP/byte}
\]

AI=50时：

\[
P\le4\text{ TB/s}\times50=200\text{ TFLOP/s}
\]

Compute翻倍但BW/AI不变，upper bound仍约200 TFLOP/s。Square GEMM的operations约 \(2n^3\)，理想bytes约 \(O(n^2)\)，但tile重复读、padding与小shape会降低realized AI。

## 10. Bottleneck判断

点靠斜线：减少bytes或增有效BW。靠平线：优化compute。远低两条：检查latency、occupancy、dependency、launch、divergence、communication或software overhead。

## 11. Design Space

More HBM抬斜线；more compute抬平线；tiling/cache/fusion右移点；low precision同时减少bytes并抬compute；batching增reuse但增加latency；compression增加codec代价。

## 12. 为什么这么简单

少量参数即可排除错误优化方向。复杂simulation更精确但需要实现细节；Roofline适合信息不完整时建立可证伪upper bound。

## 13. 为什么不……？

不只看utilization，因为可能执行padding；不只看GB/s，因为可能latency-bound；不把所有cache traffic混为一个boundary；不把整个model画一个点，因为prefill/decode/kernels差异巨大。

## 14. Trade-off

~~~mermaid
flowchart LR
  F[Fusion/larger tile] --> I[AI rises]
  I --> R[Register/shared rises]
  R --> O[Occupancy falls]
  O --> L[Latency hiding weakens]
~~~

## 15. Second-order effects

Compute增长快于BW把更多workload推入memory-bound。低precision会重排两个roof与ridge；HBM问题解决后可能转向L2、NoC或network。

## 16. Workload mapping

Training大GEMM通常AI高；prefill随prompt/batch增reuse；decode读weights/KV且AI低；embedding/graph常memory/latency bound；HPC取决于blocking。

## 17. Real tool

[Primary Source] NVIDIA Nsight Compute绘制achieved point、memory/compute boundaries与ridge。  
[Independent] Berkeley Roofline paper把operational intensity、bandwidth与peak performance合并，并增加其他ceilings。

## 18. Evolution

Compute先升 → ridge右移 → memory wall → HBM/cache/fusion → on-chip/network/power新roof。

## 19–20. Engineers actually say / 翻译

“Left of ridge”“on bandwidth roof”“far below both”“realized AI lower than algorithmic AI”“moved bottleneck to L2”分别指memory first-order bound、接近BW、存在第三约束、实际traffic偏高、近层成为新瓶颈。

## 21. 追问

Boundary？Ops counting？BW peak还是measured？precision/power？per-kernel还是average？actual bytes/cache？离roof多远？batch/shape？communication是否包含？新瓶颈？

## 22. Misconceptions

Memory-bound不要求HBM 100%；compute-bound不等于已优化；AI不是hardware常数；Roofline不预测tail latency；整个LLM没有单一AI。

## 23. Engineering → Strategy

Compute增速超过BW提高HBM/cache/compiler价值；software提高AI延长silicon寿命；low precision让numerics ecosystem变重要；hierarchical bottleneck让价值迁移到SRAM/NoC/package。

## 24. Technical Diligence

索取raw counters、boundary、operation definition、precision、SLO、power与full-model waterfall；警惕不可实现peak roof、理想bytes与cherry-picked kernels。

## 25. 五个 takeaway

1. \(P\le\min(P_{peak},BW\times AI)\)。
2. Ridge是first-order分界。
3. AI必须注明boundary与actual traffic。
4. 低于两roof要找第三约束。
5. Roofline选择方向，不替代profiling。

## 26. 开放问题

MoE/dynamic serving如何画分布式Roofline？Network/power如何加入多维ceilings？Useful token/s如何替代FLOP/s？

## Sources

- [Primary Source] [NVIDIA Nsight Compute Roofline](https://docs.nvidia.com/nsight-compute/ProfilingGuide/#roofline-charts)
- [Primary Source] [NVIDIA Deep Learning Performance](https://docs.nvidia.com/deeplearning/performance/dl-performance-getting-started/index.html)
- [Independent] [Berkeley Roofline Paper](https://escholarship.org/uc/item/3qf383m0)
