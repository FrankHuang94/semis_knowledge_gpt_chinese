# Clock、Reset 与 Error Containment：系统为何会卡在“偶发错误”

数字系统假设信号在规定时序和状态下被采样，但真实芯片包含多个 clock domains、独立电源域、异步外设与复杂启动顺序。平均功能正确并不消除罕见的 metastability、reset sequencing 或错误传播。规模扩大后，低概率事件会成为 fleet 问题。

## 边界机制

~~~mermaid
flowchart LR
  A[Clock domain A] --> S[Synchronizer / FIFO]
  S --> B[Clock domain B]
  P[Power domain] --> I[Isolation]
  I --> B
  R[Reset controller] --> A
  R --> B
  E[Error detect] --> C[Contain / recover]
~~~

跨时钟单 bit control 可用 synchronizer 降低 metastability 传播概率；多 bit data 需要 handshake 或 asynchronous FIFO 保持一致性；reset 必须满足 assert、deassert 与 clock availability 的顺序；掉电域输出要隔离，避免未知状态污染仍工作的逻辑。

## 为什么不使用一个全局 clock 和 reset

单一时钟简化验证，却限制频率、电源管理和物理实现；全局同步 reset 布线大、timing 难，并可能在解除时制造巨大 switching event。多个域提高效率，却增加 CDC、RDC、power-state 与 firmware sequence 的验证空间。

chosen design 会明确 domain boundary、合法状态转换和恢复层级：局部 retry、block reset、device reset 或 system reboot。恢复范围越小，可用性越高，但状态一致性和诊断更复杂。

## Error containment

ECC、parity、timeout 和 watchdog 能发现部分错误，却必须定义谁消费错误、哪些操作可重放、数据是否已对外可见。静默纠错会提高 uptime，但若不保留 telemetry，会掩盖 aging 或制造问题；立即复位最安全，却可能扩大 failure domain。

[Inference] 在大集群中，单芯片极低错误率乘以设备数量和运行时间后仍可能频繁出现。产品 diligence 应要求 error-rate distribution、injection coverage、recovery latency、状态清理和 fleet correlation，而不是只问“有 ECC 吗”。

## 资料

- [AMBA Specifications](https://www.arm.com/architecture/system-architectures/amba-specifications) [Primary Source]
- [Accellera CDC resources](https://www.accellera.org/) [Primary Source]
- [RISC-V Reliability Extensions](https://riscv.org/technical/specifications/) [Primary Source]


## 基础概念桥接

先区分数值表示、组合逻辑、时序状态、时钟、流水线与测量误差。工程上相同功能可有不同 timing、power、area 和 reliability；公式成立也不代表测量边界正确。先做量纲与数量级检查，再进入电路或架构细节。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。
