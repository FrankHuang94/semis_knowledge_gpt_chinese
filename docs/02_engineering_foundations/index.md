# Engineering Foundations for Semiconductor Strategists

本模块只补后续 architecture、SerDes、power、timing 与 manufacturing 推理真正依赖的 EE / CE 基础，不按本科教材顺序铺开。

## 学习顺序

1. [数字逻辑、时钟与功耗](digital_logic_clock_power.md)：从 transistor、gate、register、pipeline 到 timing closure 与动态功耗。
2. [电路与 Signal Integrity 直觉](circuit_signal_integrity_intuition.md)：从 R/C/L、impedance、transmission line 到 eye、equalization、retimer 与 optics。
3. 带着上述直觉进入 [CPU Architecture](../05_cpu/cpu_architecture.md)、[SerDes](../11_serdes_signal_integrity/serdes.md)、[Power Delivery](../18_power_delivery/power_delivery.md) 与 [Thermal](../19_thermal_cooling/thermal_cooling.md)。

## 学完以后应该能回答

- 为什么提高 clock 会同时影响 timing、voltage、power 与 thermal？
- Pipeline 为什么提高 throughput，却可能增加 latency 与控制成本？
- 为什么 wire delay、fan-out 与 clock tree 会反过来改变 architecture？
- 什么情况下 PCB trace 必须视为 transmission line？
- Eye、BER、FEC、link flap 与 system reliability 有什么区别？
- Retimer、redriver、equalization 与 optics 分别在重分配哪一段 channel budget？

合格标准不是会背公式，而是看到 “timing cannot close” 或 “signal margin is tight” 时，知道该要求哪些 boundary、corner、metric 与验证证据。


## 深化阅读

- [Clock、Reset 与 Error Containment](clock_reset_error_containment.md)


## 基础教程

- [工程数学、度量与不确定性](engineering_measurement_uncertainty.md)
- [数字逻辑、处理器与加速器基础词汇](digital_compute_accelerator_vocabulary.md)
