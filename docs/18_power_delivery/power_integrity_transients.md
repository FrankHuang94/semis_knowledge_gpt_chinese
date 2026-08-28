# Power Integrity 与 Transients：平均功率为什么保护不了系统

AI 系统的电源问题不是把 facility 容量除以服务器数量。芯片负载会在微秒至毫秒尺度变化，电源路径却由不同时间常数的 VRM、电容、busbar、power shelf、UPS 与电网组成。平均功率可能合规，瞬态 droop 仍会触发降频、计算错误或整机复位。

## 从负载阶跃追踪能量

芯片电流突增时，近端去耦电容先供能，封装与板级 PDN 随后响应，VRM 控制环再提高输出，机柜和设施系统处理更慢的变化。每一级既有电阻压降，也有电感引起的瞬态：

\[
\Delta V \approx I\cdot R + L\frac{dI}{dt}+\frac{1}{C}\int \Delta I\,dt
\]

[Estimate] 该式用于识别主导项，不是替代仿真；封装、PCB、连接器和控制环的频率相关阻抗必须结合目标阻抗曲线评估。

~~~mermaid
flowchart RL
  D[Die load step] --> P[Package PDN]
  P --> B[Board capacitors]
  B --> V[VRM]
  V --> S[Power shelf]
  S --> U[UPS / Facility]
  C[Control telemetry] -.-> V
  C -.-> S
~~~

## 瓶颈与约束

更大电容可降低 droop，却占面积、增加成本并可能改变谐振；提高供电电压可减少同功率电流，却增加转换级或芯片损耗；把 VRM 放近负载可缩短路径，却恶化热密度和可维护性。提高 power shelf 额定值也不能自动解决连接器温升、busbar 压降和相位不平衡。

真正约束通常是一组 envelope：稳态功率、短时峰值、允许电压偏移、温度、故障清除时间和冗余策略。采购文件若只有“最大功率”，工程团队无法判断峰值持续多久，也无法配置保护曲线。

## 为什么不简单 overprovision

按所有设备峰值相加建设设施最保守，却会占用昂贵的配电和冷却容量；依赖统计多样性可以提高利用率，但相关负载会同时跃迁。训练 job 的 barrier、checkpoint 或 kernel phase 可能让多台设备同步变化，因此独立随机假设会失效。

可选方案包括：

1. **静态 power cap**：可预测、容易审计，但牺牲性能。
2. **动态功率整形**：利用遥测削峰，效率高，但控制延迟和软件故障必须进入 safety case。
3. **局部储能**：缓冲短时峰值，代价是寿命、空间与维护。
4. **调度错峰**：从集群层打散相关负载，代价是作业完成时间和复杂度。
5. **设施冗余**：提升 fault tolerance，但不能代替芯片级 PI 设计。

chosen design 往往是分层组合：芯片 DVFS 和板级电容处理快速事件，power cap 与机柜控制处理较慢事件，调度器避免大规模同步。层间必须定义谁先动作，否则多个控制环可能振荡。

## 二阶效应

修复 droop 后，VRM 与连接器损耗会增加冷却负担；提高功率上限后，热容量和泵速成为限制；动态降频稳定系统后，训练 straggler 会放大 collective idle time。单节点只损失少量性能，在同步集群中却可能拖慢整个 step。

商业上应把“可交付功率”与“可用计算”连接起来。需要收集 rail telemetry、throttle reason、复位日志、负载同步性、冗余切换测试和最坏温度下的 margin。若供应商只展示 TDP 和峰值算力，尚未证明 rack 级稳定性。

## Diligence 清单

- 负载阶跃的幅度、上升时间与持续时间如何定义？
- 从 die 到 facility 的阻抗和控制责任如何分层？
- 单个 PSU、feed 或 VRM 故障时，剩余路径是否越过瞬态 envelope？
- power cap 对吞吐、尾延迟和 collective imbalance 的影响多大？
- commissioning 是否用真实 workload replay，而非只用恒阻负载？

## 资料

- [OCP Open Rack power shelf specification](https://www.opencompute.org/documents/ocp-v2-power-shelf-specification-rev01-pdf) [Primary Source]
- [NVIDIA GPU Power Management documentation](https://docs.nvidia.com/deploy/nvidia-smi/index.html#power-management) [Vendor Claim]
- [PCI-SIG Engineering Change Notices](https://pcisig.com/specifications) [Primary Source]


## 基础概念桥接

先区分 voltage、current、power、energy、efficiency、droop、transient、PDN 与 VRM。额定功率不是实测功耗，平均功率也不能保护瞬态。沿 utility、UPS、PDU、shelf、busbar、VRM、package 到 transistor 建立损耗账本。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。


## 进阶工程术语桥接

本篇进一步需要掌握：IR drop、thermal resistance、warpage、hybrid bonding、wafer sort、process window 与 qualification。阅读这些术语时，不只记中英文对应，还要补齐系统位置、正常路径、饱和或失败路径、直接 counter、端到端结果、产品状态和证据等级。若工程会议出现“已解决”“无开销”“已量产”，应立即追问 workload、boundary、configuration、status/date、failure mode 与 falsifier。

延伸阅读：[进阶工程术语手册](../31_glossary/advanced_engineering_terms_handbook.md)。
