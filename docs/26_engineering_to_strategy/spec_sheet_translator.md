# Spec Sheet Translator 与 System Performance Waterfall

## 1. 为什么需要专门的 translator

产品页把复杂系统压缩成少数最大值：某种 precision 的 peak FLOPS、HBM capacity/bandwidth、SerDes rate、TDP 与互连 aggregate bandwidth。它们回答“理论上安装了多少资源”，却没有证明目标 workload 能以目标 accuracy、latency、power、system size 和 software 版本使用这些资源。

Translator 的任务不是把单位翻译成中文，而是把每个数字恢复成完整条件，并沿 performance waterfall 追踪它在哪里被打折。

## 2. 从 Peak 到 Useful Performance

~~~mermaid
flowchart TD
  P[Peak arithmetic throughput] --> F[目标 workload 可用 precision / sparsity]
  F --> K[Kernel tile / shape / fusion efficiency]
  K --> M[Memory hierarchy / HBM efficiency]
  M --> C[Communication / collective efficiency]
  C --> S[Multi-device scaling efficiency]
  S --> R[Runtime / scheduler / data pipeline]
  R --> U[Fleet utilization / failures / queueing]
  U --> A[Useful application performance]
~~~

可以把 sustained performance 写成启发式乘积：

[
P_{useful}=P_{peak}	imeseta_{precision}	imeseta_{kernel}	imes
eta_{memory}	imeseta_{communication}	imeseta_{runtime}	imeseta_{fleet}
]

这些效率不是彼此完全独立，不能用一个乘法预测器替代 measurement；公式的价值是迫使分析者列出每个 loss bucket。Communication stall 会改变 kernel occupancy，thermal throttling 会改变 peak，batch policy 会同时改变 memory 与 latency。

## 3. 看到 FLOPS / TOPS

先问：

1. 对应 FP64、FP32、TF32、BF16、FP8、FP4 还是 INT？
2. Multiply 与 accumulate 分别是什么 precision？
3. 是否包含 structured sparsity？
4. 是 dense matrix datapath 还是所有 operation 都可使用？
5. 对应哪个 frequency、power mode 与 silicon bin？
6. 单 chip、module、node 还是 rack aggregate？
7. Software release 是否 production-available？

FLOPS 是每秒 floating-point operation 的计数约定，不是 token、sample 或 training step。若 vendor 把 fused multiply-add 计作两个 operation，[Vendor Claim] 比较双方必须使用相同 convention。低 precision peak 上升也可能使 machine balance 上升，让 memory-bound kernel 更难获得同比例 speedup。

### Roofline 快速检查

[
P_{bound}=min(P_{peak}, Bandwidth	imes Arithmetic Intensity)
]

Berkeley Lab 对 Roofline 的说明把 Arithmetic Intensity 定义为 operation 与 data movement bytes 的比例。[Primary Source] 如果 kernel 的 intensity 低于 ridge point (P_{peak}/Bandwidth)，它首先受 bandwidth ceiling 限制。

假设 accelerator 有 4 PFLOP/s peak 与 4 TB/s HBM，[Vendor Claim] ridge point 为 1000 FLOP/byte。[Estimate] 一个只有 200 FLOP/byte 的 kernel，即使完美使用 HBM，其 roofline ceiling 约 0.8 PFLOP/s，[Estimate] 即 peak 的 20%。这不是预测真实 performance，而是证明“4 PFLOP/s”不可能成为该 kernel 的第一约束。

## 4. 看到 HBM capacity 与 bandwidth

Capacity 要拆成 physical capacity、可由软件使用的 capacity、系统保留、ECC/metadata、workspace、fragmentation，以及 multi-tenant SLO 下的安全余量。模型能“放进”memory 不等于有足够空间给 KV cache、activation、optimizer、communication buffer 和 kernel workspace。

Bandwidth 要区分 pin/theoretical、copy benchmark、特定 access pattern 与 application sustained。连续大块读取、bank-friendly mapping 与足够 outstanding request 可接近较高利用率；小而随机、热点、read/write 混合或 capacity conflict 会降低。还要问所有 HBM stack 是否在同一 address domain，NUMA/partition 是否让部分 compute 只能访问局部 bandwidth。

### 反推 bytes/token

若 decode 主要读取 140 GB weight，[Estimate] 且 batch 1 每生成 token 至少读取一次全部 weight，一阶 bandwidth lower bound 为 140 GB/token。8 TB/s HBM 的理想 ceiling 约 57 token/s，[Estimate] 尚未计 KV、activation、协议与未满带宽。提高 Tensor Core peak 对这个极简 bound 没有直接帮助；weight quantization、batch reuse、cache/locality 或更多 memory bandwidth 才会移动 ceiling。

## 5. 看到 TDP / Board Power / Rack Power

TDP 通常是 thermal/design boundary，不自动等于 workload 平均功耗，也不包含 host、NIC、switch、optics、storage、fans/pumps 与 power conversion。比较必须写清：

- chip、board、server、rack 还是 wall；
- average、peak、transient 还是 provisioned；
- DC input 还是 facility AC；
- 是否含 cooling；
- performance 是否在同一 power cap；
- 目标 ambient/coolant condition。

Useful metric 应至少包含 throughput/W、energy/token 或 time-to-train × average wall power。更高功率若显著缩短 job，total energy 可能下降；更高 efficiency 若牺牲太多 throughput，固定 facility/租金成本可能上升。

## 6. 看到 Interconnect bandwidth

Aggregate bandwidth 可能把每方向、所有 links、双向或多 port 相加。必须问：

1. Unidirectional 还是 bidirectional sum？
2. Payload、encoded line rate 还是 protocol effective？
3. Endpoint injection bandwidth 是否同量级？
4. Topology 是否允许每个 pair 同时获得？
5. Collective algorithm 下的 useful bandwidth？
6. Message size 与 latency regime？
7. Oversubscription、failure/degraded mode 如何？
8. Scale-up、scale-out 或 host I/O？

单 link 速度提高不代表 All-Reduce completion time同比下降；ring/tree traffic、hop、contention、straggler、software launch 与 synchronization 都可能主导。

## 7. 看到 SerDes rate

“224G SerDes”通常描述 lane signaling generation，不等于 224 GB/s payload。要核对 symbol modulation、coding/FEC overhead、lane count、reach、BER target、electrical/optical boundary、power/lane 与 package/board assumptions。更高 lane rate 可减少 lane 数，却可能缩短 reach并增加 equalization、retimer或optics。

## 8. Benchmark skepticism：先固定 comparison contract

任何“2× performance”都应填下表：

| Boundary | 必须固定或披露 |
|---|---|
| Workload | model、dataset、operation mix、sequence/context |
| Quality | accuracy、convergence、output quality threshold |
| Shape | batch、dimensions、sparsity、request distribution |
| Software | framework、compiler、kernel、driver、version |
| Hardware | SKU、count、memory、network、power mode |
| Scenario | offline/server、TTFT/TPOT、latency percentile |
| Power | chip/board/system/wall boundary |
| Baseline | tuned程度、generation、availability |
| Statistics | warm-up、duration、run count、variance |
| Status | measured silicon、simulated、preview、shipping |

MLPerf Inference 把 Datacenter 区分 Offline、Server、Interactive 等 scenario，并要求 performance 与 accuracy validation；还区分 Available、Preview 与 RDI 类别。[Primary Source] 这说明“同模型”仍不足以保证可比，arrival model、latency constraint、division 和 availability 都是 benchmark contract。

## 9. 常见 benchmark traps

### 用 microbenchmark 代表 application

GEMM 可证明矩阵 datapath 与 library 的上限，不包含 attention、normalization、KV、communication、data pipeline 与 scheduler。

### 不同 accuracy / precision

低 bit 结果若未达到相同 quality threshold，是不同产品。Training 要比较 target quality 的 time-to-train，而不只 step/s。

### 不公平 baseline

新产品使用最新 fused kernel，baseline 使用旧 framework；测出的“硬件代际提升”混入 software gap。应同时报告同 software stack 与各自最佳 stack。

### 只报平均 latency

Online serving 受 queueing、variable context、prefill interference 与 failures 影响，p95/p99 和 SLO-compliant throughput 比平均值更重要。

### 把 simulated roadmap 当 shipping result

Pre-silicon estimate 可用于 architecture exploration，但必须标 [Estimate]；announced、preview、shipping、deployed 的风险不同。

## 10. Worked waterfall

假设产品宣称 10 PFLOP/s FP8 peak。[Vendor Claim] 目标 workload：

- 只有 80% operation 可用 FP8，[Estimate]
- kernel/shape efficiency 70%，[Estimate]
- memory stall 后 active efficiency 65%，[Estimate]
- communication/scaling efficiency 75%，[Estimate]
- runtime/fleet utilization 85%。[Estimate]

启发式 useful ceiling：

[
10	imes0.8	imes0.7	imes0.65	imes0.75	imes0.85
approx2.3 PFLOP/s
]

结果不是产品预测，而是 sensitivity map。最大的 loss 不一定最值得优化：若 memory 与 kernel efficiency 相互依赖，先 fuse kernel 可能同时改善两项。Diligence 应要求 vendor 用 profiler 把真实时间与 bytes 分解，而不是接受分析者随意给出的效率。

## 11. Product comparison workflow

1. 定义决策：training、prefill、decode、recommendation 或 HPC？
2. 固定 workload、quality、latency 与 availability boundary。
3. 把每个 spec 写成“值 + 条件 + source + date + status”。
4. 计算 ridge point、capacity、traffic、power 等一阶 bound。
5. 找到不可能被 peak spec 解决的瓶颈。
6. 获取 profiler 或 benchmark decomposition。
7. 用 sensitivity 分析判断最关键假设。
8. 加入 rack、facility、software、labor 与 failure cost。
9. 区分 measured、vendor claim、estimate 与 inference。
10. 记录缺失披露，而不是补猜数字。

## 12. Engineers actually say

- “Peak is irrelevant for this kernel.”：该 kernel 受 memory、shape、dependency 或 unsupported operation 限制。
- “We are at 60% of roofline.”：追问使用哪层 bandwidth、如何计算 bytes 与 peak。
- “The benchmark is latency constrained.”：throughput 只能在满足 percentile latency 下解释。
- “It is an optimized baseline.”：要求公开版本、flags 与可复现脚本。
- “System power is lower.”：追问 wall boundary、cooling、duration 与等质量 throughput。
- “We scale nearly linearly.”：追问规模区间、baseline node 数、parallelism、network 与 efficiency definition。

## 13. Engineering → Strategy

| Spec / result | 工程解释 | 商业问题 |
|---|---|---|
| Peak FLOPS 上升 | datapath potential | 有多少可转成 useful workload？ |
| HBM capacity 上升 | 更大 state/model | package、supply、cost 与 concurrency？ |
| Bandwidth 上升 | bytes/s ceiling | workload intensity 与 sustained efficiency？ |
| Link rate 上升 | lane signaling | reach、PHY power、optics 与 topology？ |
| TDP 上升 | higher design envelope | rack density、cooling、facility delivery？ |
| Benchmark leadership | contract 内更快 | contract 是否代表客户 workload？ |
| Better scaling | communication loss 较低 | network/control point 与 cluster TCO？ |

## 14. Diligence questions

1. Claim 的完整 benchmark contract 与 raw result在哪里？
2. Peak、sustained microbenchmark 与 application result分别是多少？
3. Accuracy/quality 与 baseline 是否相同？
4. Profiler 中 compute、HBM、collective、runtime、idle 各占多少？
5. Power 在什么 boundary 测量，是否满足同一 SLO？
6. System size、network topology 与 degraded mode？
7. 哪些 optimization 是客户可获得的 production software？
8. Baseline 是否用同版本重新调优？
9. Result variance、warm-up、duration 与 tail percentile？
10. Missing disclosure 中哪一项最可能反转购买结论？

## 15. Takeaways

1. Spec 是资源上限及其条件，不是 application performance。
2. Waterfall 把 peak 到 useful 的 loss bucket 显式化。
3. Roofline 用 arithmetic intensity 快速排除不可能的 speedup。
4. Benchmark 只有在 workload、quality、scenario、power、software、status 相同时才可比。
5. 战略决策最终比较 useful work / rack / watt / dollar 与风险，而不是单列最大值。

## Primary sources

- [Primary Source] [Berkeley Lab：Roofline Model](https://amcr.lbl.gov/departments/computer-science-department/ppan/roofline-performance-model/)
- [Primary Source] [Roofline original technical report](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2008/Archive/EECS-2008-134.pdf)
- [Primary Source] [MLPerf Inference Submission Guide](https://docs.mlcommons.org/inference/submission/)
- [Primary Source] [MLCommons benchmark methodology overview](https://mlcommons.org/benchmarks/)
- [Independent] [MLPerf Inference Benchmark paper](https://arxiv.org/abs/1911.02549)
