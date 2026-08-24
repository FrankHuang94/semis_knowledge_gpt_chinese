# GPU & Accelerator

> 状态：框架已建立，内容将按 [Roadmap](https://github.com/FrankHuang94/semis_knowledge_gpt_chinese/blob/main/ROADMAP.md) 的依赖顺序深化。

本模块不以术语数量为目标。每个主题将从 problem、constraint 与 dataflow 出发，比较 architecture alternatives，解释 trade-off、second-order effects，并连接到真实 workload、产品、制造与 Strategy Lens。

## 本模块默认问题

1. 没有这项技术时，系统在哪里失败？
2. 限制来自 physics、architecture、software 还是 manufacturing？
3. 有哪些替代方案，为什么它们共存？
4. 优化一个指标会牺牲什么？
5. bottleneck 解决后移到哪里？
6. 哪些 metric 能证伪产品主张？
7. 谁控制关键 IP、capacity、validation 与 ecosystem？

具体内容将优先链接到 cornerstone articles，避免重复建立短定义页面。


## Cornerstone sequence

1. [GPU Architecture：Thread、Warp、SM 与 Memory Hierarchy](gpu_architecture.md)
2. [为什么 Matrix Multiplication 主导 AI](why_matrix_multiplication.md)
3. [Tensor Core：小矩阵乘法单元如何变成 AI Compute Engine](tensor_core.md)
4. [GPU Execution 与 Kernel Performance：Warp、Occupancy、Tiling、Coalescing 与 Stall](gpu_execution_kernel_performance.md)
5. [Sparsity 与 Compression：减少工作，不等于自动加速](sparsity_and_compression.md)

四篇共同回答：workload为何产生规则matrix operations；GPU如何组织parallel threads与data；专用MMA datapath为什么仍依赖register、shared memory、HBM、compiler和kernel library。


## Precision 与数值格式

[Precision：FP32、BF16、FP8、FP4 与 INT 为什么共存](precision_numeric_formats.md) 从 sign/exponent/mantissa、quantization scale、accumulation 与 mixed precision 出发，解释低 bit 如何同时改变 compute、memory、collective 与 model quality。阅读任何 TOPS/FLOPS 比较前，先核对 input、accumulator、sparsity、software recipe 与实际 bytes。
