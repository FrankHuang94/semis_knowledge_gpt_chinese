# Case：Software–Accelerator Platform Diligence——硅功能如何变成客户价值

## 决策情境

一家 accelerator startup 展示出优异的 kernel benchmark，并称 compiler 可自动支持主流模型。芯片可能真实领先，但平台价值取决于模型从 framework graph 到稳定生产的整条路径。技术尽调要回答：性能来自普遍架构优势、少数手写 kernel，还是 benchmark 特化；客户升级模型后优势能否保留。

## 价值兑现链

~~~mermaid
flowchart LR
  F[Framework graph] --> I[Import / IR]
  I --> O[Optimization]
  O --> K[Kernel selection]
  K --> R[Runtime]
  R --> D[Driver / firmware]
  D --> S[Silicon]
  S --> M[Metrics]
  X[Unsupported op] -.fallback.-> C[CPU / competitor]
~~~

平台兑现率可表示为：

\[
V=P_{\text{silicon}}\times C_{\text{operator}}\times E_{\text{compiler}}\times A_{\text{runtime}}\times Q_{\text{quality}}
\]

[Estimate] 这是乘法而不是加法：operator coverage、编译效率、运行稳定性或模型质量中任何一项偏低，峰值 silicon advantage 都会被吞掉。

## 尽调实验

选择供应商从未优化过、但代表目标客户的新模型，在干净环境完成：

1. 安装与版本锁定；
2. graph import 和 correctness；
3. dynamic shape、custom op 与 fallback；
4. compile time、cache 和首次请求；
5. steady-state throughput、P99 latency 与 memory footprint；
6. 多卡 placement、collective 和故障恢复；
7. profiler 是否能把问题定位到 graph、kernel 或 hardware；
8. 升级 framework 与 driver 后重复测试。

测试团队应保留原始日志和脚本。供应商工程师可以解释，但不能在计时期间进行一次性手工改写，否则测到的是服务项目，不是可复制产品。

## Alternatives

**全栈专有平台**可深度协同，性能上限高，客户却承担迁移和锁定；**兼容主流框架的后端**采用容易，但要追赶不断变化的 operator；**开放 compiler stack**透明且可借生态扩展，差异化 IP 暴露更多；**library-first**可快速覆盖热点，却在新模型和长尾算子上脆弱。

chosen design 不必支持所有 operator，但必须对目标 segment 有清晰边界、可观察 fallback 和可预测 roadmap。少而深的 coverage 可以成为产品；“任何模型自动加速”则需要极强证据。

## 证据分层

- [Vendor Claim] 官方 benchmark、路线图与已优化模型；
- [Primary Source] compiler repository、release notes、supported-op matrix 和 issue tracker；
- [Independent] 客户在无驻场支持下的部署记录；
- [Inference] 根据新增模型支持时间、bug closure 和工程人数判断维护成本。

检查组织结构同样重要：compiler、kernel、runtime、driver 与 application team 是否共享性能回归系统；硬件勘误如何传入 compiler；客户 issue 是否反哺 architecture。

## 二阶效应与商业判断

更多 fusion 可减少 memory traffic，却拉长编译时间并增加 shape specialization；快速支持新模型会扩大代码路径，回归矩阵随之膨胀；提供 CPU fallback 提高兼容性，却可能隐藏昂贵的数据搬运。平台成熟后，客户 switching cost 增加，但维护旧版本也消耗研发资源。

估值不应按理论峰值折价后直接计算。更可靠的 leading indicators 是：目标模型首跑时间、无需手改的 coverage、版本升级成功率、性能回归率、客户自助问题解决率和单位软件工程投入带来的部署收入。

## 资料

- [OpenXLA GPU Architecture](https://openxla.org/xla/gpu_architecture) [Primary Source]
- [MLIR Documentation](https://mlir.llvm.org/docs/) [Primary Source]
- [PyTorch Custom Operators](https://pytorch.org/tutorials/advanced/custom_ops_landing_page.html) [Primary Source]
