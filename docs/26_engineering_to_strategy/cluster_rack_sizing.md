# Cluster 与 Rack Sizing：从 Workload SLO 倒推可部署系统

## 1. Sizing不是“模型参数除以 GPU memory”

Sizing必须同时满足 capacity、compute、memory bandwidth、network、power、cooling、availability与 deployment timing。模型能放进一组 accelerators只证明静态容量可行；在目标 sequence、batch、precision、parallelism和 SLO下，可能仍被 decode bandwidth、collective或 rack power限制。

正确顺序是：

<code>Business demand → Workload contract → Useful throughput/device → Devices → Network topology → Racks → Facility → Headroom</code>

若从 vendor rack数量开始，再寻找需求填满，模型会系统性高估利用率。

~~~mermaid
flowchart LR
  D[Demand + SLO] --> W[Workload distribution]
  W --> U[Useful work per accelerator]
  U --> N[Accelerator count]
  N --> F[Scale-up/scale-out fabric]
  F --> R[Racks]
  R --> P[Power + cooling]
  P --> H[Failure/growth headroom]
~~~

## 2. 固定 workload contract

Training至少定义 model、tokens、target quality、global batch、precision、parallelism与 deadline。Inference至少定义 model、input/output token distribution、arrival、TTFT、inter-token、tail、availability与 quality。

同一个“70B模型”可以是短 prompt offline throughput、长 context interactive serving、fine-tuning或 pretraining；需要的 compute/memory/network完全不同。Contract必须包含 software版本和 production status，否则 sizing会用未来优化填补当前缺口。

## 3. 从单设备 delivered performance开始

不要用 peak FLOPS。以经过 benchmark/profiler验证的 useful metric：

- training：tokens/s/device或 step time；
- serving：在 tail SLO下 requests/tokens/s/device；
- recommendation：queries/s和 embedding hit；
- HPC：time-to-solution。

[Estimate] 需求为每天八百六十四亿 output tokens，单 device在目标 SLO下 delivered为每秒一千 tokens，基础 devices为：

<code>86,400,000,000 / (1,000 × 86,400) = 1,000</code>

若 steady-state utilization目标70%、maintenance/failure reserve15%、增长 reserve20%：

<code>Required = 1,000 / 0.70 × 1.15 × 1.20 ≈ 1,972 devices</code>

Reserve不能重复：若 measured utilization已包含维护或 arrival seasonality，需避免双算。

## 4. Capacity fit与并发

每 device可用 memory不是物理 capacity。要扣除系统 reserve、weights、KV/activation、workspace、communication buffers、fragmentation与故障迁移余量。

Serving可写：

<code>Concurrency/device = usable KV capacity / weighted KV per request</code>

Weighted必须来自真实 context分布，而非 maximum或平均其中一个。Training则同时检查 parameters、gradients、optimizer state、activations与 checkpoint staging。若依靠 sharding才能 fit，网络 traffic也必须进入 sizing。

## 5. Parallelism与最小部署单位

Tensor/pipeline/expert parallel会把单 replica扩展到多个 devices；replica数量必须是 parallel group size的倍数。Scale-up island、baseboard或 rack topology又会形成离散单位。需求需要一千零一颗 GPU，不代表能买一千零一颗；可能必须按八卡、七十二卡或整 rack向上取整。

离散 rounding会在小规模显著增加闲置。Portfolio可通过混合 SKU、共享 pool或调度不同 model减少浪费，但增加 software和 inventory复杂度。

## 6. Network sizing

先画 traffic matrix，再数 ports。Training需要每种 collective的message、频率、parallel group和 overlap；serving需要 model parallel collective、KV handoff、request ingress与 storage。

对每层计算：

<code>Required payload = exposed bytes / allowed communication time</code>

再除以 protocol、topology、contention和 failure efficiency。不要把 line rate当 payload。Rail、leaf-spine、oversubscription与降级状态应分别计算。

## 7. Rack sizing

Rack不是 devices除以每 rack模块数。还受：

- IT power与 transient；
- busbar/PSU/VRM；
- air或 liquid cooling；
- CDU与 facility water；
- floor loading；
- cable/optics管理；
- service clearance；
- control/management switches；
- spare slots和 fire domain。

[Estimate] 每 rack IT设备相对功率120，facility允许每 rack设计功率150，冷却可移除140，则 power不是第一限制，cooling ceiling只剩20 headroom。若新代设备使 IT升到145，即使供电仍可，cooling已超界，需要减密度或改 facility。

## 8. Facility与 energization

Facility capacity要区分 utility reservation、substation/transformer、UPS/generator、PDU、rack busway和实际 energized date。Nameplate MW若没有 commissioning和 downstream distribution，不能支持部署。

Cooling同样区分 heat rejection、chiller/dry cooler、facility water、CDU、secondary loop与 cold plate。Supply/return temperature和 delta-T必须与 IT equipment class匹配。[Primary Source] ASHRAE数据中心指南强调 IT equipment environmental envelope与 facility design要对齐。

## 9. Availability与 spare

N+1并非完整可靠性。需要定义 failure domain：device、baseboard、host、rack、switch、CDU、power feed还是 region。一个 spare GPU无法替代坏 NVLink island；一个 spare rack若同一 CDU失败也无用。

可用 capacity：

<code>Installed × schedule utilization × healthy fraction × performance-in-degraded-mode</code>

Spares分为 cold、warm、hot。Hot spare消耗 power/capacity却恢复快；cold spare需要装机和 qualification。维修时间、供应 lead time与 failure correlation决定比例。

## 10. Queueing与 utilization

高平均 utilization通常提高 economics，却让 burst、长任务和 failure产生长 queue。Training允许排队但有 deadline；interactive inference受 tail SLO。Sizing应通过 arrival/time-series simulation，而非只用年度平均。

可采用三个场景：

- nominal：正常 mix和维护；
- peak：季节/发布/训练集中；
- degraded：一台 switch/CDU/rack failure。

若 degraded只能通过违反 SLO维持，reserve是纸面数字。

## 11. Build-vs-buy 与 deployment lag

自建需考虑 site、power/cooling construction、server qualification、network bring-up和 software acceptance；云租用降低前期 lag，却有 availability、price、egress和 lock-in。混合方案可用 cloud吸收 burst或代际过渡，但 model/data移动和环境一致性有成本。

NPV模型必须把上线日期放入。便宜20%但晚半年交付的 cluster，可能损失更多训练/产品收入。

## 12. Sensitivity与 decision table

| 变量 | Base | Downside | 影响路径 |
|---|---|---|---|
| Delivered/device | profiler | software迟到 | devices/racks增加 |
| Utilization | scheduler | demand碎片 | capacity增加 |
| Failure rate | field | correlated bug | reserve增加 |
| Power/rack | qualified | derating | rack数量增加 |
| Network efficiency | measured | congestion | step/SLO下降 |
| Deployment date | contract | construction delay | NPV下降 |

只对真正主导变量做精细预测。把未知参数写成 range，比给出虚假小数更可靠。

## 13. Why-not

### 为什么不按 peak sizing

Peak忽略 workload utilization、memory、communication、runtime和 SLO，会系统性少买。

### 为什么不把 utilization设为百分之百

任何 burst、straggler、maintenance或 failure都会导致 queue爆炸；调度也需要形状/parallel group匹配。

### 为什么不一次买满三年需求

代际进步、需求不确定与软件变化会造成过早折旧；但分期购买又面临供应、兼容性和重复 qualification。应把 option value与 reservation premium比较。

## 14. Engineers actually say

- “We need ten thousand GPUs.”：问需求、delivered/device、利用率和日期。
- “The model fits.”：问所有 state、workspace、fragmentation与 failover。
- “This rack supports full density.”：问 power、cooling、service和 degraded。
- “The network is non-blocking.”：问 traffic matrix与 failure。
- “We have twenty percent headroom.”：问在哪个层和是否重复。
- “Cloud is more expensive.”：问上线时间、利用率与 option value。

## 15. Technical diligence questions

1. Demand与 SLO time series？
2. Delivered performance的 benchmark contract？
3. Capacity/parallelism最小单位与 rounding？
4. Network traffic和 exposed communication？
5. Rack power、transient、cooling与 service boundary？
6. Facility energized和 commissioned日期？
7. Failure domain、repair time与 spare策略？
8. Nominal/peak/degraded queue结果？
9. Software、hardware与 construction schedule dependency？
10. 最大 sensitivity和可证伪 evidence？

## 16. Takeaways

1. Sizing从 demand和 useful performance倒推，不从 peak或产品数量开始。
2. Memory fit、parallelism和 topology产生离散最小单位。
3. Rack与 facility power/cooling可能先于 silicon限制部署。
4. Headroom必须对应具体 failure、burst和增长，避免重复。
5. 上线时间与 option value和硬件价格同样重要。

## Primary sources

- [Primary Source] [ASHRAE Data Center Resources](https://www.ashrae.org/technical-resources/bookstore/datacom-series)
- [Primary Source] [ASHRAE AI Data Center Site Planning](https://www.ashrae.org/technical-resources/ai-data-center-framework/site-planning)
- [Primary Source] [Open Compute Project Advanced Cooling Solutions](https://www.opencompute.org/wiki/Cooling_Environments_Advanced_Cooling_Solutions)


## 基础概念桥接

先把技术主张还原为 workload、bottleneck、constraint、alternatives、chosen design 和 second-order effect，再讨论市场。价值捕获取决于 IP、产能、认证、生态、客户迁移和成本曲线；技术领先不自动等于 moat。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。


## 进阶工程术语桥接

本篇进一步需要掌握：profile、compliance、certification、sampling、production、shipping、design win、attach rate 与 value migration。阅读这些术语时，不只记中英文对应，还要补齐系统位置、正常路径、饱和或失败路径、直接 counter、端到端结果、产品状态和证据等级。若工程会议出现“已解决”“无开销”“已量产”，应立即追问 workload、boundary、configuration、status/date、failure mode 与 falsifier。

延伸阅读：[进阶工程术语手册](../31_glossary/advanced_engineering_terms_handbook.md)。
