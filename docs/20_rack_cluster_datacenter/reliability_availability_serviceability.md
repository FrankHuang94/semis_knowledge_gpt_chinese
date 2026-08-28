# Reliability、Availability、Serviceability：AI Cluster 的 Delivered Compute

## 1. 峰值算力乘以失败概率才接近现实

大集群由 GPU、CPU、HBM、NIC、switch、optics、cable、power、cooling、storage和 software组成。单 component很可靠，数量扩大后仍会频繁出现事件。系统价值取决于多少时间在完成有效训练或满足 inference SLO。

<code>Delivered work = Peak × Utilization × Healthy fraction × Recovery efficiency</code>

~~~mermaid
flowchart LR
  F[Fault] --> D[Detect]
  D --> I[Isolate]
  I --> R[Retry/Repair]
  R --> V[Validate]
  V --> S[Return to service]
  T[Telemetry] -.-> D
~~~

## 2. Reliability、availability与 serviceability

Reliability：一段时间内不失败的概率。Availability：需要服务时可用的比例，受 repair time影响。Serviceability：能否快速检测、定位、隔离、更换和验证。

同样 failure rate下，把恢复从数小时降到数分钟可显著提高 availability。昂贵 redundancy若无法自动 failover，实际价值有限。

## 3. Failure domain

必须标 component fault会影响：

- 一个 lane；
- 一个 accelerator；
- 一台 host；
- 一个 scale-up island；
- 一台 switch/rail；
- 一个 rack；
- 一个 CDU/power feed；
- 一个 job或 tenant；
- 整个 cluster。

更大 rack-scale domain提高通信，也扩大 shared switch/power/control故障。Architecture要允许局部隔离和 degraded operation。

## 4. Error分类

Correctable error被 ECC/FEC/重试处理，但频率上升可能预示 aging。Uncorrectable error触发 page retirement、link reset、device reset或 job failure。Silent data corruption最危险：任务继续但结果错误。

Telemetry需关联 memory ECC、PCIe/AER、link BER/FEC、thermal/power、kernel错误和 application anomaly。只看 device-down会错过先兆。

## 5. Checkpoint interval

经典权衡：更频繁 checkpoint增加 steady overhead，更稀疏会在失败后重算更多。[Estimate] 若 checkpoint暂停2分钟、平均每10小时发生 job-impacting failure，粗略最优 interval在几十分钟量级；真实还要计异步写、恢复、failure correlation与 checkpoint size。

关键是 end-to-end恢复：发现、停止、重排、读取、验证和 warm-up，不只是写文件速度。

## 6. Redundancy与 degraded mode

Spare links、lanes、cores、ranks、hosts和 racks可提高可用性。Redundancy需要 routing/scheduler/software实际使用。一个 spare GPU若不在同 topology group或没有 matching HBM，不一定可替换。

Degraded mode应定义 performance：link降速、少一 rail、关闭一 tile或 reduced power后，是否仍满足 SLO。能运行不等于可服务。

## 7. Blast radius与 change management

Firmware、driver、compiler、BIOS和 network config更新可能同时影响大量节点，correlated failure比独立硬件更危险。Canary、staged rollout、rollback与 mixed-version compatibility是 RAS。

配置管理要保留 lineage：哪个 lot、firmware、rack、coolant loop与 job。没有关联数据，root cause只能猜。

## 8. Observability budget

Telemetry也消耗 bandwidth、storage与工程。应优先保留能预测或定位的 signals，统一时间同步和 IDs。Sampling平均可能漏掉短 transient；全量又成本过高。

最小事件记录：timestamp、component、topology、firmware、workload、symptom、corrective action和 outcome。

## 9. Why-not

- 为什么不为所有 component做2N：成本、power和复杂度。
- 为什么不只看 MTBF：忽略 repair与 correlated failure。
- 为什么不自动 retry所有错误：可能重复 corruption或 retry storm。
- 为什么不立即更换有 correctable error的器件：需要 threshold和趋势。
- 为什么不把所有节点同版本升级：扩大 blast radius。

## 10. Engineering → Strategy

| RAS能力 | 工程收益 | 商业价值 |
|---|---|---|
| ECC/FEC | correct errors | 少 job loss |
| Telemetry | 早检测 | 降 MTTR |
| Isolation | 小 blast radius | availability |
| Checkpoint | 减重算 | delivered throughput |
| Spares | 快替换 | SLO |
| Canary/rollback | 控制变更 | 软件风险 |
| Traceability | root cause | warranty/supplier |

## 11. Diligence questions

1. Field failure rate按 component与 lot？
2. Failure domain和 correlated paths？
3. Correctable趋势与 retirement policy？
4. Silent corruption检测？
5. Detect/isolate/repair/validate各多久？
6. Checkpoint与恢复总成本？
7. Degraded mode性能和 SLO？
8. Spare location和 topology compatibility？
9. Firmware rollout/rollback和 canary？
10. Peak到 delivered work的完整 waterfall？

## 12. Takeaways

1. 大集群必然频繁遇到局部事件，设计目标是控制影响和恢复。
2. Availability同时取决于 failure rate和 repair time。
3. 更大 integration domain会扩大 shared failure。
4. Checkpoint、spares、telemetry和 change control共同决定 delivered compute。
5. RAS应进入 TCO和产品比较，而非附录。

## Primary sources

- [Primary Source] [ASHRAE Data Center Resources](https://www.ashrae.org/technical-resources/bookstore/datacom-series)
- [Primary Source] [Linux PCI Error Recovery](https://docs.kernel.org/PCI/pci-error-recovery.html)


## 基础概念桥接

先把 rack 当成计算机：compute、memory、network、power、cooling、firmware、controls 与 operations 共同决定 useful work。nameplate 数量不等于 commissioned capacity；安装、验收、故障恢复、spares 与维护窗口必须进入 TCO。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。
