# HBM Scaling：Capacity、Bandwidth、Thermal 与 Yield 为什么不能同时最大化

HBM 的系统价值来自宽接口、堆叠容量与靠近 accelerator 的封装位置，但每次增加 stack height、速率或堆叠数量，都会同时改变信号、电源、散热、封装面积、良率和供应约束。把 HBM 当作“更快的 DRAM”会漏掉它与 logic die、interposer 和 package 的共同设计。

## 从带宽公式开始，再离开公式

\[
BW_{\text{peak}}=N_{\text{stacks}}\times W_{\text{interface}}\times R_{\text{pin}}
\]

[Estimate] 峰值带宽只是接口上限。持续有效带宽还要乘以 controller efficiency、bank parallelism、访问局部性和软件调度效率；容量则由 stack 数、每层 density 与 stack height 决定。提高其中一项可能降低其他项的 margin。

~~~mermaid
flowchart TB
  M[Model state] --> C[Memory capacity]
  M --> B[Bandwidth demand]
  C --> S[Stack count / height]
  B --> R[Pin rate / channels]
  S --> P[Package area]
  S --> T[Thermal path]
  R --> I[Signal + power integrity]
  P --> Y[Assembly yield]
  T --> Y
~~~

## 四组耦合约束

**容量与热**：更高堆叠减少单位容量占地，却延长顶层 die 的热路径并改变温度分布。刷新、retention 与功耗又随温度变化，因此 thermal margin 会反馈到有效性能。

**速率与功耗**：提高 pin rate 增加带宽，也收紧时序、训练和电源完整性。controller、PHY 与 termination 的功耗会进入同一 package thermal budget。

**stack 数与 routing**：增加堆叠可并行扩带宽，却消耗 interposer 面积、microbump、routing channels 和 package edge；logic die 周围并非无限空间。

**良率与可修复性**：最终 good package 依赖 logic、每颗 HBM、interposer、assembly 与 test。已知良品降低风险，但 assembly 后缺陷仍可能报废高价值组件。repair、redundancy 和 binning 能改善经济性，却增加设计和测试复杂度。

## 为什么不只加更多 HBM

首先，workload 可能受 compute、collective 或 latency 限制，多余带宽无法兑现。其次，大 package 降低 wafer utilization、提高 warpage 和 substrate 难度。再次，供应 allocation、qualification 和代际转换可能比 silicon 设计更慢。最后，软件若不能提高 locality 或并行发出请求，峰值通道闲置。

chosen design 应先由模型 state、batch、sequence 和并行方式算出 capacity 与 bandwidth envelope，再比较更多 stack、更高 density、低精度、compression、recomputation、CXL tiering 与 sharding。最佳方案通常是跨层组合，而非把所有压力交给 HBM。

## 二阶效应与 diligence

容量增加后可以提高 batch 或 context，随即扩大 activation、KV cache 或通信；带宽提高后，tensor units、network 或 power delivery 成为新墙。采购时应要求目标 workload 的 controller counters、温度分布、降频条件、stack/bin 配置、package yield 与供应状态。[Inference] 若性能只在冷机、理想 locality 或稀有最高 bin 下成立，商业可用量会显著低于 headline。

## 资料

- [JEDEC Standards and Documents](https://www.jedec.org/standards-documents) [Primary Source]
- [AMD Instinct documentation](https://instinct.docs.amd.com/) [Vendor Claim]
- [NVIDIA HBM3E technology overview](https://www.nvidia.com/en-us/data-center/technologies/hbm3e/) [Vendor Claim]


## 基础概念桥接

先区分 stack、channel、pseudo-channel、bank、pin rate、controller efficiency 与有效带宽。HBM 是逻辑 die、memory stack、interposer、封装、热和供应共同系统。容量、带宽、温度、良率和 package area 无法同时独立最大化。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。


## 进阶工程术语桥接

本篇进一步需要掌握：row buffer、refresh、controller、DMA、IOMMU、ATS、page migration、pooling 与 coherence。阅读这些术语时，不只记中英文对应，还要补齐系统位置、正常路径、饱和或失败路径、直接 counter、端到端结果、产品状态和证据等级。若工程会议出现“已解决”“无开销”“已量产”，应立即追问 workload、boundary、configuration、status/date、failure mode 与 falsifier。

延伸阅读：[进阶工程术语手册](../31_glossary/advanced_engineering_terms_handbook.md)。
