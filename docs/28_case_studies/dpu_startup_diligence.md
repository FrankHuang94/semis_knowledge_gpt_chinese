# Case：如何审计一家宣称“释放一半 Host CPU”的 DPU Startup

## 1. Investment memo不能从 TAM开始

假设一家 DPU startup宣称：把 networking、storage与 security offload到 card后，可释放一半 host CPU、降低 tail、提高 isolation，并在现有 server中即插即用。这些主张横跨 datapath、software、security、fleet operations与 economics，任何一层不成立都会让收入假设失效。

审计目标不是证明 DPU概念有价值，而是回答三个决策问题：

1. 哪些具体 workloads稳定消耗 host资源？
2. Startup能以可量产、可维护的软件栈卸载多少？
3. 节省能否转成更少 server、更多可售 compute或更高 SLO，而非空闲 core？

~~~mermaid
flowchart LR
  C[Vendor claim<br/>50% CPU saved] --> W[Workload contract]
  W --> P[Packet/data path]
  P --> S[Software coverage]
  S --> O[Operations + security]
  O --> E[Server/rack economics]
  E --> D{Investment decision}
~~~

## 2. 先重写 claim

“释放一半 CPU”至少需要以下 boundary：

- Baseline CPU型号、core数、frequency与 power mode；
- traffic type、packet-size、flow-length与 encryption/storage feature；
- throughput、p95/p99 latency与 loss目标；
- offload前后 server、NIC、memory与 software版本；
- host上还有哪些 application work；
- DPU自身 power、cores、memory与 failure；
- steady state、burst、rule churn与 attack pattern；
- savings是 cycles、reserved cores还是实际减少 hosts。

若 vendor不能填完，claim仍是 marketing phrase。Technical team应把它改写为“在指定 traffic和 SLO下，host reserved cores从 A降到 B，同时 application throughput不降、DPU power和 failure已计入”。

## 3. Architecture walkthrough

要求工程师在白板画出每个 packet：

1. Port进入 PHY/MAC；
2. parser与 classification；
3. fixed-function、match-action或 accelerator；
4. state lookup与 policy；
5. DMA到 host/GPU/storage；
6. miss/exception进入 embedded cores或 host；
7. completion、telemetry与 error；
8. control plane如何下发与回滚规则。

对每个 box记录最大 rate、state capacity、latency、power与 overload behavior。最关键的不是 nominal fast path，而是 feature组合后的 fast-path coverage和 slow-path ceiling。

如果 encryption、overlay、firewall、storage compression不能同时 line-rate，客户必须选择功能或接受性能下降；若首次 flow进入 slow path，短流 workload可能完全由 embedded CPU限制。

## 4. Controlled benchmark matrix

| 维度 | 至少覆盖 |
|---|---|
| Packet | 小/大、burst、fragment、reorder |
| Flow | 短/长、connection churn、elephant/mice |
| Features | tunnel、ACL、crypto、storage单独与组合 |
| State | table occupancy、miss、aging、update |
| Host | idle与 application saturated |
| Failure | link flap、DPU reboot、rule server loss |
| Security | malformed、tenant escape、key rotation |
| Software | cold boot、upgrade、rollback、mixed versions |

结果按 host cycles、reserved cores、application throughput、p99、DPU utilization、drop与 power报告。Vendor自己选择的长流/大 packet通常最容易 offload，不能代表 cloud traffic。

## 5. CPU savings模型

[Estimate] Baseline server中 infrastructure占24个 cores，其中：

- network datapath 10；
- virtual switch/policy 5；
- storage 6；
- security/telemetry 3。

Startup在目标版本分别覆盖90%、70%、50%、40%，但 exception与 control消耗被卸载部分的20%。净节省：

<code>(10×0.9 + 5×0.7 + 6×0.5 + 3×0.4) × (1-0.2) = 13.36 cores</code>

这约占 infrastructure cores的56%，却可能只占整台 server总 cores的一小部分。只有当13个 cores能提高 VM density、减少 sockets或避免额外 server时，才形成经济价值。模型最敏感变量通常是 production feature coverage，不是 datapath peak。

## 6. Power与 rack economics

DPU增加 card、memory、PSU与 cooling负担。若节省 CPU cycles只是让 CPU闲置但不降 power cap、不减少 hosts，rack power未必明显下降。反之，若能把每台 server可售 vCPU提高，固定网络、rack与软件成本可被更多 revenue units摊薄。

TCO需包含：

- card与spares；
- DPU power及 airflow；
- host core/socket/server变化；
- license按 core收费的变化；
- engineering、qualification与 on-call；
- firmware/security lifecycle；
- failure导致的 capacity headroom；
- vendor support与 supply。

## 7. Software moat还是 services trap

要求普通客户团队在没有 startup现场工程师的情况下完成：

1. 安装 driver/BSP；
2. 接入 orchestrator；
3. 部署 policy；
4. 运行 profiler与 debug；
5. 滚动升级；
6. 模拟故障并 rollback；
7. 导出 telemetry到现有平台。

若每次 workload需要手工 P4/firmware、专属 kernel patch或 vendor调参，收入可能依赖 services，gross margin与 scaling假设应调整。真正的软件 moat表现为更多客户与 feature组合复用同一 control plane，而不是更多定制代码。

## 8. Trust boundary验证

DPU声称 zero trust时，审计：

- secure boot与 root of trust；
- firmware signing、key ownership与 rotation；
- host是否能 DMA或 reset越权；
- BMC与 management network；
- tenant policy isolation；
- debug port与 manufacturing keys；
- attestation与 audit log；
- compromised DPU如何隔离和恢复。

独立 Arm cores不自动等于独立 trust。若 host driver仍可重写 critical tables，或 vendor持有全局 recovery key，security故事需要重画。

## 9. Failure-domain反转

把 network、storage与 security集中到 DPU可以隔离 host，却也让一张 card成为多项服务的共同故障点。应测：

- DPU OS crash时已有 flows；
- storage write的 ordering与 durability；
- fail-open或 fail-closed；
- host能否临时 fallback；
- rolling reboot影响；
- firmware bug blast radius；
- spare replacement与 reprovision时间。

“基础设施继续运行”必须通过 fault injection证明。Failover若回到 CPU，需要预留足够 host headroom，否则故障时整个 rack过载。

## 10. Supply与 manufacturing

Startup需要 NIC/SerDes、embedded CPU、memory、PCIe、security IP、board、connector与 firmware。即使 chip fab有产能，advanced substrate、card assembly、optics/cable与 qualification可能限制交付。

审计 BOM中 single-source parts、mask ownership、foundry/OSAT agreements、test time、yield、RMA与 second source。客户不会只买 silicon；他们买可替换、可支持的 card/platform。

## 11. Commercial wedge

最可信的 wedge通常具有：

- 明确且昂贵的 host tax；
- 稳定 feature set；
- 大规模同质 fleet；
- operator控制 hardware与 software；
- core savings能转成 revenue或 server；
- 强 isolation需求；
- 可持续 deployment团队。

Enterprise单台 server可能没有足够规模回收复杂度；hyperscaler有价值却也可能自研。Startup要证明自己处在“客户有痛点但不愿自研”的狭窄区间。

## 12. Red flags与 falsifiers

### Red flags

- 只展示 microbenchmark或单 feature；
- 把 idle CPU下降当 server savings；
- 不披露 slow-path hit；
- SDK每客户分支；
- line-rate但不含 crypto/policy组合；
- upgrade需要停机；
- security只谈 secure boot；
- silicon sampling却按 shipping收入预测；
- hyperscaler pilot没有 paid production scope。

### 会改变结论的 evidence

- 三个独立客户在 production达到同类 savings；
- 客户自行完成升级与故障恢复；
- feature组合下 p99与 power可复现；
- server consolidation或可售 capacity有财务证据；
- firmware CVE response与 lifecycle经过验证；
- qualified second source与量产良率。

## 13. Evidence matrix

| Claim | 当前证据 | 需要补强 | 决策影响 |
|---|---|---|---|
| 50% CPU saved | vendor lab | customer production counters | 收入/TCO核心 |
| Line-rate security | 单 feature demo | 组合+小 packet | 产品适配 |
| Zero trust | architecture slide | threat model/penetration | 风险 |
| Easy deployment | vendor install | customer rolling upgrade | scaling |
| Broad TAM | server count | workload-qualified sockets | 估值 |
| Shipping soon | tape-out/card | yield/qualification/PO | timing |

## 14. Investment committee synthesis

Bull case：host infrastructure tax持续增长，客户需要隔离，startup以可复用 software覆盖高价值 features，节省转成可售 compute，并通过 card量产和多客户复制形成 platform。

Bear case：固定 NIC迅速吸收常见 offload，CPU cores变便宜，DPU软件仍定制化，客户自研 control plane，card power/故障抵消 savings，startup被困在 pilot。

关键不是预测“DPU市场增长”，而是跟踪三个 leading indicators：production feature coverage、客户独立运营能力、每台 deployment的可验证 cash savings。

## 15. Diligence questions

1. 50%对应哪些 cores、traffic、features与 SLO？
2. Fast/slow path覆盖与 worst-case ceiling？
3. 节省是否导致更少 server或更多 revenue capacity？
4. DPU自身 power、failure与 headroom？
5. 软件能否跨客户复用与滚动升级？
6. Trust ownership、keys与 host DMA边界？
7. 故障时 fail-open/closed/fallback？
8. Silicon/card status与量产 qualification？
9. 与下一代 fixed-function NIC差异？
10. 客户为何买而不自研或继续 CPU？

## 16. Takeaways

1. 把 headline CPU savings重写成同 workload、SLO与 system boundary的可测命题。
2. Production feature coverage与 slow path比 peak packet rate更重要。
3. Core savings只有转成 server、license或可售 capacity才是价值。
4. DPU新增一套软件、安全和故障生命周期。
5. 投资判断应由客户可复现的 cash savings驱动，而非 server TAM。

## Sources

- [Primary Source] [Linux Kernel NAPI Documentation](https://docs.kernel.org/networking/napi.html)
- [Primary Source] [NVIDIA BlueField Modes of Operation](https://docs.nvidia.com/networking/display/bluefieldbsp453/modes%2Bof%2Boperation)
- [Primary Source] [NVIDIA BlueField Management](https://docs.nvidia.com/networking/display/bluefieldbmcv2601/bluefield-management)


## 基础概念桥接

案例中的数字必须进入统一 waterfall：理论峰值到 kernel、application、system、availability-adjusted output，再到单位经济性。为 base、upside、downside 分别写依赖和触发器，避免把最好条件的演示直接当财务预测。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。
