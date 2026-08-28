---
id: core_quiz
title: AI Datacenter Engineering Core 五级测验
concepts: [quiz, engineering_reasoning, technical_diligence]
prerequisites: [modern_ai_datacenter, engineering_to_strategy]
level: [1, 2, 3, 4, 5]
status: draft
last_verified: 2026-08-24
source_date: 2026-08-24
---

# AI Datacenter Engineering Core 五级测验

这不是名词考试。每级要求更长的因果链：准确语言 → mechanism → architecture → trade-off → strategy。先闭卷回答，再对照rubric；能说出“缺什么信息”比假装精确更重要。

## 使用方法

- 每题先写system boundary、workload与目标metric。
- 画图时标出state、data、control、bandwidth与latency。
- 数量题必须写assumptions、units与sanity check。
- Strategy题必须给falsifier。
- Level通过标准：至少五题中四题达到rubric，且无关键概念错误。

## Level 1 — Terminology

### Q1. Bandwidth 与 Latency

为什么高bandwidth link仍可能有较高single-request latency？给出一个memory例和一个network例。

**Rubric：** 区分单位时间吞吐与单请求完成时间；提到serialization、propagation、queue、protocol或dependency。

### Q2. Peak、Utilization 与 Delivered Performance

分别定义三者，并解释为什么不能互换。

**Rubric：** Peak是理论/规格上限；utilization需定义有效工作；delivered绑定真实workload、software、system与time。

### Q3. Training、Prefill 与 Decode

分别指出主要live state与常见目标metric。

**Rubric：** Training含weights/activations/gradients/optimizer；prefill建立KV并关注TTFT；decode读KV迭代并关注ITL/cost/token。

### Q4. Scale-up 与 Scale-out

边界来自什么，而不是距离名称？

**Rubric：** Tightly coupled semantics、latency/bandwidth、failure/coherence/programming domain；scale-out偏packet/routed/large domain。

### Q5. Yield

区分die yield、target-bin yield与final package yield。

**Rubric：** denominator明确；target bin含speed/power；final含多dies/bonds/assembly/test。

### Q6. Product Status

Announced、Sampling、Production、Shipping与Deployed分别能支持什么强度的claim？

**Rubric：** 不把roadmap/demo当volume；deployment还需客户规模与reliability。

## Level 2 — Mechanism

### Q1. HBM 为什么提供高带宽

从wide I/O、short reach、TSV/stack、channels/banks解释，同时列出三个代价。

### Q2. SerDes 链路

画TX→channel→RX，解释equalization、CDR、FEC与retimer各解决什么，不允许说“让信号更强”作为完整答案。

### Q3. DRAM Read

从controller command到bank/row buffer/data return，解释row hit与row conflict。

### Q4. RDMA Transfer

从GPU/host memory到remote memory画出registered memory、NIC DMA、switch queue、transport与completion。

### Q5. Cold Plate

解释heat从junction到coolant的路径；提高flow为何可能收益递减？

### Q6. Voltage Droop

用R、L、C与load transient解释，指出decoupling与VRM control各覆盖的时间尺度角色。

**Level 2 Rubric：** 每题必须写因果mechanism与至少一个failure mode，不能只列定义。

## Level 3 — Architecture

### Q1. LLM Serving System

画prefill/decode、KV cache、scheduler、GPU/HBM、scale-up、NIC与scale-out。指出TTFT、ITL、throughput各在哪里受限。

### Q2. Distributed Training

给定DP×TP×PP×EP组合，画rank groups并标注all-reduce、all-gather/reduce-scatter、point-to-point与all-to-all。

### Q3. Pluggable、LPO 与 CPO

画三种conversion placement，比较DSP、electrical reach、service、thermal与yield boundary。

### Q4. Chiplet System

画compute chiplets、active/base/I/O die、D2D PHY/protocol/coherence、HBM与package。指出哪个block可能成为single point。

### Q5. AI Rack

画compute/switch trays、busbar/power shelf、NIC/optics、cold plate/manifold/CDU与management。标四个failure domains。

### Q6. Compiler Stack

画framework graph→IR→fusion/layout→kernel→runtime→hardware→counter feedback，并指出两个fallback。

**Level 3 Rubric：** 图必须包含state、data/control path、shared resources与boundary，且能解释删掉任一block的结果。

## Level 4 — Trade-off

### Q1. 为什么不最大化 Occupancy？

答案需覆盖register spill、shared memory、ILP与stall evidence。

### Q2. 为什么不扩大 Tensor Parallel 到整个 Cluster？

覆盖collective frequency、latency、topology与替代parallel dimensions。

### Q3. 为什么不全部使用 CPO？

覆盖serviceability、laser、package yield、test与supply boundary。

### Q4. 为什么不把所有logic 3D Stack？

覆盖thermal path、power delivery、bond yield、KGD与repair。

### Q5. 为什么不追求最高 Rack Density？

覆盖facility power/cooling、weight、service、failure blast radius与delivered compute。

### Q6. 为什么不全部 Dual-source？

覆盖qualification、fungibility、economics、learning与transfer time。

**Level 4 Rubric：** 每题至少三个alternatives、四个trade-offs、一个second-order bottleneck与选择条件。

## Level 5 — Strategy & Diligence

### Q1. Spec Sheet Translator

[Estimate] 某accelerator matrix peak提高 (2.5	imes)，HBM bandwidth提高 (35%)，capacity提高 (50%)。哪些workloads最不可能获得 (2.5	imes)？列十个缺失输入。

### Q2. Value Migration

HBM bandwidth wall缓解后，价值最可能向哪些components/capabilities迁移？给base/upside/downside和falsifiers。

### Q3. Vendor Claim Audit

厂商声称“DPU释放三成host cores”。把它拆成metric、baseline、packet distribution、feature set、power、software和TCO subclaims，设计测试。

### Q4. Capacity Diligence

公司称“产能翻倍”。列出从announced tool到good systems的完整证据链，并指出五种definition drift。

### Q5. TCO Bridge

建立新旧rack的price→delivered throughput→power/cooling→availability→deployment→cost/useful work bridge。标出最敏感变量。

### Q6. Investment Thesis

选择optics、advanced packaging或liquid cooling之一，写一页thesis：constraint、timing、value capture、moat、substitutes、supply、evidence、risk与observable falsifier。

**Level 5 Rubric：** 结论必须有boundary、source labels、status/date、quantitative bridge、sensitivity与falsifier；不能以“市场很大”替代value capture。

## 答题评分表

| 维度 | 0 | 1 | 2 |
|---|---|---|---|
| Boundary | 未定义 | 部分定义 | workload/metric/system/time完整 |
| Mechanism | 名词堆砌 | 基本因果 | data/state/control与physics清楚 |
| Alternatives | 无 | 单一替代 | 多方案及选择条件 |
| Quantitative | 无 | 公式无sanity | assumptions/units/range/sensitivity |
| Evidence | 无来源 | 单一claim | source/status/date/confidence |
| Strategy | 只谈TAM | 有TCO | value capture/moat/falsifier闭环 |

每题满分十二分；十至十二为“可用于工程对话”，七至九为“需补一轮”，低于七回到对应核心文章。


## 基础概念桥接

练习的目标不是背答案，而是展示推理链。每道题先写已知、未知、单位、边界和假设，再做数量级计算；最后指出替代方案、最敏感输入、证伪测试和 bottleneck 迁移。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。


## 进阶工程术语桥接

本篇进一步需要掌握：微操作、流水线冒险、并行度、shape、动态批处理、尾延迟、数量级与单位经济性。阅读这些术语时，不只记中英文对应，还要补齐系统位置、正常路径、饱和或失败路径、直接 counter、端到端结果、产品状态和证据等级。若工程会议出现“已解决”“无开销”“已量产”，应立即追问 workload、boundary、configuration、status/date、failure mode 与 falsifier。

延伸阅读：[进阶工程术语手册](../31_glossary/advanced_engineering_terms_handbook.md)。
