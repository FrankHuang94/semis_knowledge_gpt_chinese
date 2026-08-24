---
id: fermi_exercises
title: AI Datacenter Fermi Exercises：从数量级到决策边界
concepts: [fermi_estimation, quantitative_reasoning, sensitivity]
prerequisites: [roofline, hbm, collective, optics, advanced_packaging, modern_ai_rack]
level: [2, 3, 4, 5]
status: draft
last_verified: 2026-08-24
source_date: 2026-08-24
---

# AI Datacenter Fermi Exercises：从数量级到决策边界

每题先独立完成，再看参考解。所有输入均为教学用 [Estimate]，不是产品规格。目标是暴露主导变量，而不是得到小数点后的“正确答案”。

## 通用模板

1. 定义system boundary与目标。
2. 写已知/未知及units。
3. 建立最简单方程。
4. 算base case。
5. 做至少一个sensitivity。
6. Sanity check并指出模型遗漏。

## 1. HBM Feeding

[Estimate] Accelerator peak为 (1 	ext{PFLOP/s})，HBM bandwidth为 (4 	ext{TB/s})。Ridge point：

[
AI^*=rac{1000 	ext{TFLOP/s}}{4 	ext{TB/s}}=250 	ext{FLOP/byte}
]

**问：** Arithmetic intensity为 (50) 与 (500) 的kernels分别是哪侧？  
**解：** 前者memory ceiling约 (200 	ext{TFLOP/s})，后者可能compute-bound。实际还看cache、precision与efficiency。

## 2. KV Cache Capacity

[Estimate] 每token、每request跨所有layers的KV state为 (0.5 	ext{MB})，平均active context为 (8{,}000) tokens，可用于KV的HBM为 (800 	ext{GB})。

[
Requestsapproxrac{800 	ext{GB}}{0.5 	ext{MB}	imes8000}approx200
]

**Sensitivity：** KV quantization减半bytes可近似翻倍capacity，但metadata、fragmentation与quality会降低收益。

## 3. Ring All-Reduce

[Estimate] Gradient为 (8 	ext{GB})，八个ranks，effective link bandwidth (200 	ext{GB/s})。Ring per-rank traffic近似 (2(N-1)/N) 倍message：

[
Tapproxrac{2	imes7/8	imes8}{200}=0.07 	ext{s}
]

忽略latency与contention约 (70 	ext{ms})。若backward可overlap (50 	ext{ms})，暴露约 (20 	ext{ms})。

## 4. Pipeline Bubble

[Estimate] 四个equal stages，使用八个microbatches。简单schedule的bubble fraction近似：

[
Bubbleapproxrac{p-1}{m+p-1}=rac{3}{11}approx27%
]

增加microbatches降bubble，但会改变activation memory与kernel efficiency。

## 5. Optical Port Count

[Estimate] Switch aggregate capacity为 (51.2 	ext{Tb/s})，每port (800 	ext{Gb/s})：

[
Ports=51.2/0.8=64
]

若每port total optical subsystem节省 (4 	ext{W})，满配节省约 (256 	ext{W})。需核验host SerDes、laser、cooling与FEC boundary。

## 6. Package Yield

[Estimate] Package含四颗chiplets，每颗KGD pass probability (0.96)，六个关键bond groups各 (0.995)，其余assembly (0.97)：

[
Yapprox0.96^4	imes0.995^6	imes0.97approx80%
]

若chiplet pass提高到 (0.98)，重新计算并比较增加KGD test成本是否值得。

## 7. Busbar Current

[Estimate] Rack IT power (120 	ext{kW})，DC busbar (50 	ext{V})：

[
I=P/V=2{,}400 	ext{A}
]

等效resistance若 (100 muOmega)，loss约 (576 	ext{W})。把voltage翻倍、保持power/resistance不变，loss降为四分之一；conversion/safety不在模型内。

## 8. Coolant Flow

[Estimate] Liquid移除 (100 	ext{kW})，允许rise (10^circ	ext{C})，比热 (4.18 	ext{kJ/(kg·K)})：

[
dot mapproxrac{100}{4.18	imes10}=2.39 	ext{kg/s}
]

若允许rise翻倍，energy-balance flow减半，但junction/return temperature与heat exchanger会改变。

## 9. Delivered Compute Waterfall

[Estimate] Peak (100) units，kernel efficiency (75%)，memory/fabric joint efficiency (80%)，availability (95%)：

[
Delivered=100	imes0.75	imes0.8	imes0.95=57
]

若只把peak提高 (50%) 而memory/fabric efficiency降到 (60%)，delivered约 (64)；远小于peak headline。

## 10. Good-system Output

[Estimate] Logic支持每周 (20{,}000) packages，HBM支持 (18{,}000)，packaging (15{,}000)，final yield (92%)：

[
Output=min(20{,}000,18{,}000,15{,}000)	imes0.92=13{,}800/week
]

只扩logic不增加output；先找minimum constraint。

## 11. Offload Core Savings

[Estimate] Packet rate (16) million/s，software cost (1{,}200) cycles/packet，每core可持续 (3) billion useful cycles/s：

[
Cores=rac{16	imes10^6	imes1200}{3	imes10^9}=6.4
]

若DPU多耗 (80 	ext{W})，比较释放cores的server power、license与capacity value，不能只报cores。

## 12. TCO Break-even

[Estimate] 新rack价格高 (25%)，delivered throughput高 (60%)，annual power/cooling cost高 (15%)。令旧rack capital为 (C)、lifetime energy为 (0.4C)：

[
Old=1.4C,quad New=1.25C+0.46C=1.71C
]

Cost/throughput比：旧 (1.4)，新 (1.71/1.6=1.07)，约低 (24%)。再测试availability、software efficiency与deployment delay。

## 13. 开放题：建立你自己的模型

任选一个真实claim，保留来源标签与日期，填写：

| 项 | 内容 |
|---|---|
| Objective | |
| Boundary | |
| Inputs / labels | |
| Equation | |
| Base result | |
| Sensitivity | |
| Missing factors | |
| Falsifier | |
| Strategy implication | |

## 评分标准

- Equation正确且units一致：基础。
- Assumptions透明：可审计。
- 找到主导变量：有用。
- 给range/sensitivity：可决策。
- 指出模型何时失效：成熟。
- 把结果连接到bottleneck与value capture：完成。
