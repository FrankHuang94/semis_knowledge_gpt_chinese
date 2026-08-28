---
id: fermi_exercises
title: AI Datacenter Fermi Exercises：从数量级到决策边界
concepts: [fermi_estimation, quantitative_reasoning, sensitivity]
prerequisites: [roofline, hbm, collective, optics, advanced_packaging, modern_ai_rack]
level: [2, 3, 4, 5]
status: reviewed
last_verified: 2026-08-24
source_date: 2026-08-24
---

# AI Datacenter Fermi Exercises：从数量级到决策边界

所有输入都是教学用 [Estimate]，不是产品规格。目标不是得到漂亮小数，而是定义 boundary、暴露主导变量、给出 sensitivity，并知道模型在什么条件下失效。可执行版本见 [scripts/fermi_models.py](https://github.com/FrankHuang94/semis_knowledge_gpt_chinese/blob/main/scripts/fermi_models.py)。

## 通用解题模板

1. 写清 Objective：要支持购买、architecture 还是 capacity 决策？
2. 定义 System boundary：chip、board、rack、cluster 还是 facility？
3. 列 Input、unit、source label 与 date。
4. 写最简单的守恒式或 upper/lower bound。
5. 做 base case，不伪造未知精度。
6. 对一至两个主导变量做 sensitivity。
7. 用另一种方法 sanity check。
8. 写出 missing factors 与 falsifier。
9. 把答案连接到 bottleneck 与 value capture。

## 1. HBM feeding 与 Roofline

[Estimate] Accelerator peak 为 1000 TFLOP/s，HBM 为 4 TB/s。

Ridge point：<code>AI* = 1000 / 4 = 250 FLOP/byte</code>。

- Kernel A 的 Arithmetic Intensity 为 50 FLOP/byte，memory ceiling 为 200 TFLOP/s，因此 memory-bound。
- Kernel B 为 500 FLOP/byte，memory ceiling 高于 peak，可能 compute-bound。

“可能”很重要：cache、instruction mix、shape 与 kernel efficiency 还会降低 ceiling。运行：

<code>python scripts/fermi_models.py roofline --peak-tflops 1000 --bandwidth-tb-s 4 --ai-flop-byte 50</code>

## 2. KV cache capacity

[Estimate] 80 layers、16,384 cached tokens、batch 1、8 KV heads、head dimension 128、每元素 2 bytes。

容量：<code>2 × 80 × 16384 × 1 × 8 × 128 × 2 / 1024^3 = 5 GiB</code>。

这只是单 request KV，不含 weight、workspace、allocator page、fragmentation 与 reserve。把 batch 提到 32 时理论 KV 变 160 GiB，[Estimate]，但生产系统还要按 context distribution 与 SLO admission，而不是按所有 request 都在 maximum context。

## 3. Ring All-Reduce

[Estimate] Gradient message 8 GiB、8 ranks、effective link 200 GiB/s。

Ring 每 rank traffic：<code>2 × (8 - 1) / 8 × 8 = 14 GiB</code>。理想时间约 70 ms。[Estimate]

如果 backward 可 overlap 50 ms，[Estimate] exposed communication 约 20 ms。Sensitivity：

- Message 减半不保证时间严格减半，小 message latency/launch 比例会上升；
- Ranks 增加时 traffic factor 接近 2，但 topology、contention 与 straggler 可能恶化；
- Effective bandwidth 不能直接用 raw line rate。

## 4. Pipeline bubble

[Estimate] 四个等时 stage、八个 microbatch。简单 schedule 的 bubble fraction：

<code>(p - 1) / (m + p - 1) = 3 / 11 ≈ 27%</code>。

增加 microbatch 可降低 bubble，但 activation memory、kernel shape 与 optimizer step latency 会变化。若 stages 不平衡，最长 stage 会增加其他 stage 等待；先做 layer-to-stage partition，而不是只增加 microbatch。

## 5. Optical port 与 spare

[Estimate] 100,000 accelerator endpoint，每个需要一个 optical link，module 一 link，spare 5%。

<code>Modules = 100000 × 1 / 1 × 1.05 = 105000</code>。

这是 endpoint-side 数量；若 link 两端都用 module，还需乘二。若 switch-side 使用 CPO 或 breakout，边界又不同。继续估算：

- module power × installed count；
- fiber/connector count；
- ToR/spine port 与 oversubscription；
- spare 的区域分布，而非只算总仓库数量；
- failure rate、replacement time 与 cleaning workflow。

## 6. Package yield

[Estimate] 四颗 chiplet KGD pass 各 0.96，六组关键 bond 各 0.995，其余 assembly 0.97。

<code>Y = 0.96^4 × 0.995^6 × 0.97 ≈ 79.9%</code>。

如果 chiplet pass 提到 0.98，组合 yield 改善；但要比较新增 sort coverage 的 test time/cost。该乘法假设独立，真实 defect clustering、common process excursion 与 systematic design interaction 会破坏独立性。

## 7. Busbar current 与 resistive loss

[Estimate] Rack IT power 120 kW、DC busbar 50 V。

<code>I = P / V = 120000 / 50 = 2400 A</code>。

若等效 resistance 为 100 micro-ohm，[Estimate]：

<code>Loss = I^2 R = 576 W</code>。

把 voltage 翻倍、保持 power 与 resistance 不变，current 减半、resistive loss 降到四分之一；但 conversion stage、connector creepage/clearance、安全、component qualification 与 architecture 都会改变。

## 8. Coolant flow

[Estimate] 液体移除 100 kW，温升 10 °C，水基 coolant 比热按 4.18 kJ/(kg·K)。

<code>Mass flow = 100 / (4.18 × 10) ≈ 2.39 kg/s</code>。

允许更大温升可按 energy balance 降低 flow，却会提高 return temperature，并可能改变 junction temperature、heat exchanger approach、pump curve、material compatibility 与 reliability。

## 9. Delivered performance waterfall

[Estimate] Peak 100 units，precision coverage 0.8、kernel 0.75、memory 0.8、communication 0.9、runtime/fleet 0.95。

<code>Delivered = 100 × 0.8 × 0.75 × 0.8 × 0.9 × 0.95 ≈ 41</code>。

若只把 peak 提高 50%，同时 memory efficiency 因 machine balance 变化降到 0.6，[Estimate] 新 delivered 约 46，远低于 1.5× headline。这个模型用于定位 sensitivity；效率并非独立，最终仍需 profiler。

## 10. Qualified good-system output

[Estimate] Logic 每周支持 20,000 套，HBM 18,000，packaging 15,000，final yield 0.92。

<code>Output = min(20000, 18000, 15000) × 0.92 = 13800/week</code>。

只扩 logic 不改变 output。若 packaging 扩到 19,000，HBM 会成为新 bottleneck，output 约 16,560/week。[Estimate] 继续问 installed capacity、qualified capacity、cycle time 与 mix fungibility。

## 11. DPU offload core savings

[Estimate] Packet rate 16 million/s，host software 每 packet 1200 cycles，每 core 可持续 3 billion useful cycles/s。

<code>Cores = 16e6 × 1200 / 3e9 = 6.4</code>。

若 DPU 多耗 80 W，[Estimate]，不能只比较 watts：还要计算释放 CPU core 的 server consolidation、license、tail latency、isolation、firmware 与 security value。Packet-size distribution 与 offload feature coverage 会改变 cycles/packet。

## 12. TCO break-even

[Estimate] 新 rack capital 高 25%，delivered throughput 高 60%，lifetime power/cooling cost 从旧 rack capital 的 40% 增到 46%。

旧：<code>1.0C + 0.4C = 1.4C</code>。

新：<code>1.25C + 0.46C = 1.71C</code>。

Cost/throughput：旧为 1.4；新为 <code>1.71 / 1.6 ≈ 1.07</code>，低约 24%。[Estimate] 然后测试 software efficiency、availability、deployment delay、financing、residual value 与 power delivery schedule。

## 13. Reverse-engineering exercises

### A. HBM bandwidth 上升但 stack 数不变

推测可能来自更高 per-pin rate、generation、PHY/controller 或更高 sustained utilization。验证：

- 是否同 capacity 与 stack count；
- interface speed 与 channel 数；
- package routing/PDN/thermal 变化；
- memory vendor qualification；
- peak 与 measured workload bandwidth。

### B. Switch capacity 翻倍但 radix 不变

可能是 port rate 翻倍。追踪 SerDes generation、FEC、PCB reach、retimer、optics power 与 front-panel density。若 lane rate更高，系统可能从 pluggable 转向 LPO/CPO。

### C. Accelerator FLOPS 提升 2.5×、HBM bandwidth 仅 1.35× [Vendor Claim]

Machine ridge point 上升约 1.85×，[Inference]；原本接近 memory-bound 的 decode、embedding、small GEMM 或 gather/scatter 更难获得 2.5×。要求按 workload Arithmetic Intensity、bytes 与 profiler 验证。

## 14. 自建模型表

| 项 | 必填内容 |
|---|---|
| Objective | 哪个决策？ |
| Boundary | chip / board / rack / cluster / facility |
| Inputs | value、unit、label、source、date |
| Equation | 最简可审计关系 |
| Base result | 保留合理有效位 |
| Sensitivity | 至少一个主导变量 |
| Missing factors | 哪些现实被省略？ |
| Falsifier | 什么 evidence 会推翻？ |
| Strategy | 谁获得价值，谁承担风险？ |

## 15. 评分标准

- 单位与数量级正确：基础；
- Assumption 与 source label 透明：可审计；
- 找到主导变量：有用；
- 给 range/sensitivity：可决策；
- 指出模型何时失效：成熟；
- 连接 bottleneck、TCO 与 value capture：完成。


## 基础概念桥接

练习的目标不是背答案，而是展示推理链。每道题先写已知、未知、单位、边界和假设，再做数量级计算；最后指出替代方案、最敏感输入、证伪测试和 bottleneck 迁移。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。


## 进阶工程术语桥接

本篇进一步需要掌握：微操作、流水线冒险、并行度、shape、动态批处理、尾延迟、数量级与单位经济性。阅读这些术语时，不只记中英文对应，还要补齐系统位置、正常路径、饱和或失败路径、直接 counter、端到端结果、产品状态和证据等级。若工程会议出现“已解决”“无开销”“已量产”，应立即追问 workload、boundary、configuration、status/date、failure mode 与 falsifier。

延伸阅读：[进阶工程术语手册](../31_glossary/advanced_engineering_terms_handbook.md)。
