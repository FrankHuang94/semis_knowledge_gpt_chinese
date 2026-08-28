# Performance Regression Operations：性能为什么会在没有改模型时消失

AI 平台由 framework、compiler、kernel library、runtime、driver、firmware 和 silicon 共同组成。任何一层升级都可能改变 graph partition、fusion、memory layout、collective algorithm 或 power behavior。功能测试全通过并不代表性能保持；性能因此需要像 correctness 一样持续运营。

## Regression 路径

~~~mermaid
flowchart LR
  C[Code / model change] --> B[Build matrix]
  B --> K[Kernel microbench]
  B --> G[Graph benchmark]
  B --> S[System workload]
  K --> A[Attribution]
  G --> A
  S --> A
  A --> R[Bisect / rollback]
  R --> D[Release decision]
~~~

单一 end-to-end 数字能发现问题，却难定位；只测 kernels 容易漏掉 graph、memory、launch 和 communication。chosen design 是分层 benchmark：microbench 监控原子机制，representative graphs 监控 compiler，完整 workload 监控 SLO 与系统交互。三层共享版本和 trace metadata。

## Baseline 不是一个固定数字

硬件 stepping、firmware、温度、background load、model shape 与 cache state 都会造成 variation。基线应包含分布、允许噪声和重复次数，并区分 cold start、warm steady state 与故障恢复。阈值太窄会产生告警疲劳，太宽会让小幅回归长期累积。

[Estimate] 多个看似可接受的小回归会相乘：compiler、kernel、network 和 runtime 各损失一点，端到端可能形成显著成本。版本治理要记录累计 waterfall，而不是每个团队只守自己的局部预算。

## 为什么不总是升级最新版本

新版本修复 correctness 和 security，也可能改变 autotuning、workspace、precision 或 supported shapes；固定旧版本稳定，却错过优化并扩大维护风险。合理策略是 canary、代表性 workload matrix、自动 bisect 和明确 rollback window，而不是永久冻结或 fleet-wide 直接升级。

## Attribution

发现回归后先确认 workload、input、SLO 和硬件是否相同，再用 profiler 区分 compile、launch、compute、memory、collective、I/O 与 idle。若某个 unsupported op 回退到 CPU，局部日志可能仍显示 GPU kernels 很快；必须追完整 critical path。

软件 moat 也可从 regression operations 观察。能快速检测、归因、修复并安全发布的团队，才可持续兑现 silicon feature。一次精心调优的 benchmark 不能证明这种能力。

## Diligence

- 支持哪些 framework、compiler、driver 和 firmware 组合？
- 每个 release 的性能 matrix 覆盖真实客户 shape 吗？
- regression 由谁拥有，修复时限和 rollback 如何？
- profiler 能否追踪 fallback 与跨设备等待？
- 客户自定义模型如何加入回归集并保护隐私？
- 性能数据是否与功耗、温度、correctness 和 quality 同时保存？

## 资料

- [OpenXLA GPU Architecture](https://openxla.org/xla/gpu_architecture) [Primary Source]
- [MLIR Documentation](https://mlir.llvm.org/docs/) [Primary Source]
- [PyTorch Benchmark Utilities](https://pytorch.org/docs/stable/benchmark_utils.html) [Primary Source]


## 基础概念桥接

先区分 framework graph、IR、lowering、fusion、kernel、runtime、driver 与 firmware。硬件 feature 只有被正确导入、覆盖、调试和部署才产生价值。首次编译、warm cache、dynamic shape、fallback 与版本回归需要分别测量。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。
