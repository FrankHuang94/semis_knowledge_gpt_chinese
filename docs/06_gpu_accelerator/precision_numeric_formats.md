# Precision：FP32、BF16、FP8、FP4 与 INT 为什么共存

> 第一次阅读：1–7 节。第二次阅读：8–13 节。深入阅读：14 节以后。

## 1. 先告诉我为什么需要它

厂商常把更低 precision 与更高 TOPS/FLOPS 放在同一张表里，让人产生“bit 数减半，性能就按比例上升”的直觉。真实 workload 必须先把 tensor 转换到目标格式，选择 scale，执行支持该格式的 kernel，再以足够高 precision 累加或完成 sensitive operation；如果 shape、software、accuracy 或 memory movement 不匹配，峰值吞吐不会变成 application performance。

Precision 不是单纯存储格式，而是 hardware datapath、memory footprint、bandwidth、collective traffic、numeric recipe 与 model quality 的共同契约。

## 2. 一句话直觉

更少 bit 让相同 memory、wire 和 multiplier 面积承载更多元素，通常降低 energy per operation；代价是能表达的数值范围或相邻可表示值的细度下降。Exponent 主要决定 dynamic range，mantissa/significand 主要决定相对精度，scale 又决定实际 tensor 如何落入有限编码范围。

## 3. 系统位置

~~~mermaid
flowchart LR
  T[High-precision tensor] --> S[Choose scale / block scale]
  S --> Q[Quantize + round / clip]
  Q --> L[Low-precision load]
  L --> M[Tensor Core / matrix datapath]
  M --> A[Higher-precision accumulate]
  A --> O[Activation / normalization]
  O --> C[Checkpoint / communication]
  C -. accuracy feedback .-> S
~~~

只有矩阵乘法使用低 precision 并不意味着整个 model 都使用低 precision。LayerNorm、Softmax、loss accumulation、optimizer state、master weights、reductions 或异常敏感层可能保留更高 precision。NVIDIA Transformer Engine 的公开说明也明确：并非所有 operation 都适合低 precision；常见 recipe 让 linear operation 使用低 precision，而部分 normalization、Softmax 或 division 保留高 precision。[Primary Source]

## 4. Floating point 如何编码

典型 floating-point 数近似表示为：

[
x = (-1)^s 	imes significand 	imes 2^{exponent}
]

Sign 决定正负，exponent 覆盖很大数量级，mantissa/significand 保存有效数字。增加 exponent bit 通常扩大 range，却在总 bit 固定时挤压 significand precision；增加 mantissa bit 则改善相邻值分辨率，但可覆盖 range 变小。

FP32 适合需要较高 range 与 precision 的累加、控制与 reference computation，但 storage、bandwidth 和 arithmetic energy 较高。FP16 有较多 mantissa、较小 exponent；BF16 保留与 FP32 相近的 exponent 宽度、减少 mantissa，训练时更不容易因 range 不足 overflow/underflow。两者都不是“哪个永远更准”，而是 range 与 resolution 的不同分配。

FP8 常见 E4M3 与 E5M2。NVIDIA 文档给出的 E4M3 具有更高 significand precision、较小 range；E5M2 用更多 exponent 换更大 range、较低 precision。[Primary Source] Forward activation/weight 与 backward gradient 的分布不同，因此 hybrid recipe 可能在不同方向使用不同格式。

INT8/INT4 用定点整数加 scale 表达 real value。它们的 datapath 高效，但 range 分配高度依赖 scale，outlier 容易迫使大多数普通值使用很粗的 step。Floating point 自带 exponent，在 tensor 内跨数量级时更灵活；integer 在 distribution 可校准时可能更简单高效。

## 5. Quantization 真正做了什么

最简单对称量化可写成：

[
q = clamp(round(x/s), q_{min}, q_{max})
]

(s) 是 scale，round 产生离散误差，clamp 产生 saturation。Scale 太大，普通值被映射到少数 code，quantization noise 增加；scale 太小，outlier 被 clip。目标不是让每个值无误差，而是让累积误差不显著损害目标 model metric。

Scale granularity 是关键 design choice：

| Granularity | 优点 | 代价 |
|---|---|---|
| per-tensor | metadata 少、实现简单 | 一个 outlier 影响整个 tensor |
| per-channel | 适应 channel 分布 | 更多 scale 与 kernel constraint |
| per-block | 更贴近局部分布 | layout、metadata、reduction direction 复杂 |
| per-token/dynamic | 适应运行时变化 | 在线统计与 conversion overhead |

OCP Microscaling（MX）规范定义 block scaling 相关的低 bit format；NVIDIA 的 MXFP8 文档举例说明 block of 32 consecutive values 使用各自 scale，[Primary Source] 从而减少整个 tensor 共享一个 scale 的压力。数字 32 属于特定 recipe，不应泛化为所有 block quantization。[Primary Source]

## 6. Accumulation precision 为什么重要

即使乘数是 FP8 或 FP4，大量 partial product 的 sum 也可能需要 FP16、BF16 或 FP32 accumulate。Reduction 长度越长，小误差与 cancellation 越可能累积；如果 accumulator range 或 precision 不足，结果可能逐步漂移。

因此 spec sheet 上的“FP8 compute”必须拆成 input format、multiply format、accumulator format、output format 与 rounding mode。若使用 sparsity、structured metadata 或特定 accumulate mode 才能达到 peak，也要把条件写进比较。

Training 还会产生 gradient、optimizer state 和 weight update。某一 GEMM 支持低 precision，不代表 optimizer 与 checkpoint memory 按同比例缩小。Mixed precision 的价值来自选择性：把吞吐密集且数值鲁棒的部分降 precision，把 sensitive state 留在较高 precision。

## 7. Training 与 inference 不同

Training 必须保持 forward、backward 与 update 的稳定性。Gradient distribution 可能跨较大 range，scale 需要跟踪 amax 或局部统计；loss scaling、master weights、stochastic rounding 与 accumulation policy 都可能影响 convergence。仅在短训练或小模型上匹配 accuracy，不足以证明大规模长训练稳定。

Inference 没有 backward 和 optimizer，可以进行 calibration 或 quantization-aware training，常更适合 INT8/INT4/FP4。但生成模型的 token distribution、context length、KV cache、MoE routing 和 rare outlier 会让静态 calibration 失效。还要分别看 prefill 与 decode：prefill 大 GEMM 更容易利用低 precision compute；decode 可能由 weight/KV movement 主导，低 bit 的主要价值变成减少 bytes，而不只是增加 FLOPS。

## 8. Precision 如何移动瓶颈

降低 precision 会同时改变：

~~~mermaid
flowchart TD
  P[Precision down] --> C[More peak compute]
  P --> B[Fewer bytes / element]
  P --> E[Lower arithmetic + movement energy]
  P --> Q[Quantization / scale overhead]
  C --> M[Memory wall becomes more visible]
  B --> K[More model / KV fits in memory]
  B --> N[Less collective traffic]
  Q --> A[Accuracy / convergence risk]
  Q --> L[Layout and kernel constraints]
~~~

如果 compute throughput 增长快于 HBM bandwidth，机器 balance（peak FLOPS / bandwidth）上升，更多 kernel 反而变成 memory-bound。低 precision 只有在数据确实以更少 bytes 存储和传输时才能改善 bandwidth；若每次从高 precision 临时 cast、重复保存 transpose 或产生 scale metadata，节省会被部分抵消。

## 9. 为什么不……？

### 为什么不把所有 operation 都用最低 precision？

Softmax、normalization、reduction、optimizer 或极端 activation 可能对 range/rounding 更敏感。错误还可能逐层放大，导致 convergence 或 rare-input quality 下降。

### 为什么不只保留一个通用 low-bit format？

Weight、activation、gradient、KV cache 与 optimizer 的 distribution 不同；training 和 inference 的容错也不同。单一 format 会在 range、precision 或 implementation efficiency 上妥协。

### 为什么不使用一个 tensor-wide scale？

Outlier 会决定 scale，使多数值的有效 code 变少。更细 granularity 可改善表示，却增加 metadata、layout、hardware 和 software complexity。

### 为什么不相信 vendor 的“accuracy 无损”？

必须问 model、dataset、task metric、baseline、sequence length、training duration、seed、recipe 与 excluded layer。平均 benchmark 相同不等于 tail behavior、rare language、long context 或 downstream fine-tuning 相同。

## 10. Worked example：memory 与 compute 的不同收益

一个含 70B parameters 的模型，若只计算 weight storage：

- 16-bit weight 约 140 GB，[Estimate]
- 8-bit weight 约 70 GB，[Estimate]
- 4-bit weight 约 35 GB。[Estimate]

实际 serving 还需 KV cache、activation、workspace、scale/zero-point metadata、runtime 与可能的 high-precision copy，所以不能把这些数字直接当作 GPU memory requirement。

假设某 accelerator 的 FP8 peak 是 BF16 的 2 倍，[Vendor Claim] 但 HBM bandwidth 不变。若 kernel 原先已 memory-bound，单纯切 FP8 compute 不会获得 2 倍；只有实际 bytes/element 同时下降、kernel 支持目标 format、conversion overhead 可隐藏，才可能提高 roofline 的 memory-bound ceiling。

## 11. Product / software reality

Hardware support 要拆成 native datapath 与 emulation。Native 也不等于所有 shape 都高效：matrix dimension alignment、tile size、transpose direction、batch、sequence、fusion 和 memory layout 会决定 Tensor Core utilization。

Transformer Engine 文档说明 FP8 autocast 会维护 amax history 与 scale，并指出部分 tensor shape 需要满足 alignment 条件。[Primary Source] MXFP8 还可能为了不同 reduction direction 从 high-precision input 生成 regular 与 transposed quantized copy，避免 double quantization，但增加 storage 与 conversion work。[Primary Source]

因此 product comparison 应同时记录：

1. 支持哪些 input/accumulate/output format；
2. Peak 是否含 structured sparsity；
3. 哪些 library/kernel 已 production-ready；
4. 转换、scale、transpose 和 metadata overhead；
5. Accuracy recipe 是否公开且可复现；
6. 分布式训练中 scale/amax 如何同步；
7. fallback operation 占总时间多少。

## 12. Engineers actually say

- “We are range-limited.”：overflow/underflow 或 clipping 主导；追问 exponent、scale 与 outlier。
- “We are precision-limited.”：quantization step 或 accumulate error 主导，不一定靠扩大 range 解决。
- “That layer stays in FP32.”：局部敏感 operation 保留高 precision；追问占比和 data-conversion boundary。
- “The recipe is per-block.”：scale granularity 更细；追问 block orientation、metadata 和 transpose。
- “Accuracy is recovered with QAT.”：需要重新训练或 fine-tune，部署成本不只是推理 kernel。
- “The hardware supports FP4.”：仍要问 software coverage、accumulation、shape 与实际 model quality。

## 13. Second-order effects

更低 precision 提高 compute density后，operand delivery、HBM、register file、NoC 和 collective 更可能主导；减少 bytes 后，更大的 batch 或 context 又增加 scheduling 与 tail latency；block scaling 改善 accuracy 后，scale metadata、layout 与 transpose 成为 overhead；模型能放入更少 GPU 后，scale-out traffic 降低，但单 GPU power density 与 local memory access 可能上升。

更高 peak 也会改变商业比较：如果 competitor 的 low-precision number 对应不同 sparsity、accumulator、power 与 accuracy recipe，直接相除没有意义。应比较目标 workload 的 sustained useful tokens/s、training time、joule、rack 和 dollar。

## 14. Engineering → Strategy

| Precision change | System effect | Product effect | Strategic implication |
|---|---|---|---|
| BF16/FP16 → FP8 | compute/byte efficiency 上升 | library 与 scaling 重要 | software recipe 成为 adoption moat |
| per-tensor → per-block | outlier 影响下降 | metadata/layout 复杂 | hardware-software co-design 价值提高 |
| weight-only INT4/FP4 | model footprint 下降 | quality/calibration 风险 | 可减少 accelerator count 与网络需求 |
| high-precision accumulate | numeric stability 提高 | accumulator area/energy | peak spec 需解释 accumulate mode |
| mixed precision | workload balance 更好 | graph partition/cast 增加 | compiler/runtime coverage 决定价值 |

## 15. Technical diligence questions

1. Peak 数字的 input、accumulator、output precision 各是什么？
2. 是否包含 sparsity？稀疏 pattern 是否由目标模型自然满足？
3. 哪些 operation fallback 到 BF16/FP32，占 runtime 多少？
4. Scale 是 per-tensor、per-channel、per-block 还是 dynamic？
5. Calibration/QAT 需要多少 data、compute 与 customer work？
6. Accuracy 用什么任务、baseline、context、seed 与统计显著性验证？
7. Weight、activation、KV、gradient、optimizer 分别采用什么格式？
8. Conversion、transpose、amax、metadata 与 distributed sync overhead 多大？
9. 不满足 tile/alignment 的 shape 性能如何？
10. 发生 overflow、NaN 或 convergence drift 时如何观测和 fallback？
11. 低 precision 是否真实减少 HBM/collective bytes？
12. 生产软件版本与 roadmap feature 如何区分？

## 16. Takeaways

1. Precision 是 range、resolution、scale、accumulate 与 workload quality 的组合。
2. 更低 bit 可同时改善 compute density 与 data movement，但不会自动兑现 peak speedup。
3. Mixed precision 是有选择地把数值风险留在 sensitive operation。
4. Scale granularity 改善表示时，会增加 metadata、layout 与 software complexity。
5. 比较产品必须回到 sustained application performance、accuracy、power 与 system boundary。

## Primary sources

- [Primary Source] [FP8 Formats for Deep Learning](https://arxiv.org/abs/2209.05433)
- [Primary Source] [NVIDIA Transformer Engine：FP8 primer](https://docs.nvidia.com/deeplearning/transformer-engine-releases/release-2.6/user-guide/examples/fp8_primer.html)
- [Primary Source] [NVIDIA Transformer Engine：low-precision training](https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/features/low_precision_training/introduction/introduction.html)
- [Primary Source] [NVIDIA Transformer Engine：FP8 与 FP4 / MXFP8](https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/examples/fp8_primer.html)
- [Primary Source] [OCP Microscaling Formats (MX) Specification](https://www.opencompute.org/documents/ocp-microscaling-formats-mx-v1-0-spec-final-pdf)
