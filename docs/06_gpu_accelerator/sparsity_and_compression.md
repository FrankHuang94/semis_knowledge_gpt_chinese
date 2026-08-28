# Sparsity 与 Compression：减少工作，不等于自动加速

稀疏、量化与压缩常被写成同一类“效率技术”，但它们删除的对象不同：稀疏删除零值计算，量化缩短每个数，压缩则减少传输或存储字节。工程判断不能从“压缩率”直接跳到“吞吐翻倍”，而要追踪表示如何在模型、编译器、kernel、memory hierarchy 与硬件执行单元之间兑现。

## 问题：理论上省下了什么

设稠密权重矩阵有 \(N\) 个元素，每个元素 \(b\) bit，非零比例为 \(d\)。最理想的权重流量是 \(Ndb\)，但稀疏表示还要携带索引、位图或结构元数据。真实压缩率应写成：

\[
R=\frac{Nb}{Ndb+M_{\text{metadata}}}
\]

[Estimate] 若一个模型采用规则的二比四结构，数值负载约减半，但实际端到端收益还取决于元数据、激活流量、反量化、kernel 覆盖和剩余算子的占比。这个公式首先是边界，不是产品承诺。

~~~mermaid
flowchart LR
  M[模型训练] --> P[Prune / Quantize]
  P --> F[稀疏格式]
  F --> C[Compiler pattern match]
  C --> K[Sparse kernel]
  K --> H[Hardware datapath]
  H --> E[端到端收益]
  C -.不支持.-> D[Dense fallback]
~~~

## 瓶颈：零值也可能很昂贵

非结构化稀疏允许任意位置为零，模型自由度高，却需要索引、间接寻址与负载均衡。一个线程束若读取分散地址，memory coalescing 变差；各行非零数不同，又会形成 tail effect。结果可能是数学乘法减少，地址生成、元数据访问和调度开销上升。

结构化稀疏把规则限制在固定小组内，牺牲模型自由度，换取规则编码和可预测 datapath。其优势不是“更稀”，而是编译器容易证明模式合法，硬件容易在固定节拍取数。代价是训练必须维持约束，checkpoint 转换必须正确，某些层的精度损失不能接受。

## 为什么不把所有层都稀疏化

第一，attention、normalization、embedding lookup 与小矩阵未必由相同计算单元主导。第二，batch、shape 与 sequence length 会改变 kernel 选择；支持的矩阵维度之外可能回退到 dense path。第三，剪枝后的再训练成本和验证周期会吞掉部署收益。第四，动态激活稀疏需要运行时发现零值，若检测成本接近省下的计算，收益消失。

Amdahl 定律提供最重要的 sanity check。若可加速部分占总时延 \(p\)，其加速倍数为 \(s\)，总加速只有：

\[
S=\frac{1}{(1-p)+p/s}
\]

[Estimate] 即使核心矩阵部分加速两倍，只要它只占请求时延六成，端到端也只有约一点四三倍；预处理、通信和采样成为新的墙。

## 工程选择树

- **目标是容量**：先比较低精度、weight-only quantization、分层存储和模型蒸馏；它们通常比非结构化稀疏更容易部署。
- **目标是矩阵吞吐**：确认 silicon、compiler 与 library 对特定结构模式和 shape 的共同支持。
- **目标是带宽**：确认数据在 HBM、片上缓存、互连和主机内存中是否始终保持压缩；中途展开会把收益变成局部优化。
- **目标是成本**：把精度恢复训练、转换、验证、fallback 监控与多代兼容纳入总拥有成本。

## 二阶效应与产品现实

压缩减少 HBM 读流量后，瓶颈可能迁移到 activation、collective 或 CPU feeding；稀疏 kernel 降低平均时延后，少数 fallback shape 会主导尾延迟。供应商展示的峰值 sparse throughput 通常隐含支持格式、对齐和可用 kernel 条件。[Vendor Claim] 采购验证应要求逐层 profiler、真实 shape 分布、精度差异、编译缓存命中率和 dense fallback 计数，而不是只看峰值倍数。

战略上，稀疏价值由“模型可压缩性 × 软件兑现率 × 硬件覆盖率 × 运行规模”相乘。任何一项接近零，silicon feature 都难成为商业 moat。真正可防守的能力往往是训练工具、格式、编译器、kernel 与监控共同形成的闭环。

## Diligence 问题

1. 稀疏规则由训练产生、离线转换，还是运行时动态产生？
2. 哪些 dtype、shape、batch 和算子被原生支持？unsupported path 如何观测？
3. 收益来自计算减少还是 HBM 流量减少？roofline 位置是否真的移动？
4. 精度恢复需要多少训练资源，模型每次更新是否重复支付？
5. 指标是 kernel speedup、tokens per second、tail latency，还是每个有效请求的成本？

## 资料

- [NVIDIA TensorRT Developer Guide：Structured Sparsity](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/advanced.html#sparsity) [Vendor Claim]
- [PyTorch Semi-Structured Sparsity](https://pytorch.org/docs/stable/sparse.html#sparse-semi-structured-tensor-operations) [Primary Source]
- [MLCommons Inference Policies](https://github.com/mlcommons/inference_policies) [Independent]


## 基础概念桥接

先区分 thread、warp、block、SM、occupancy、utilization、register、shared memory 和 HBM。线程很多不等于计算单元忙碌；shape、tiling、coalescing、fusion 与 kernel coverage 决定峰值能否兑现。低精度或稀疏还必须通过质量约束。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。
