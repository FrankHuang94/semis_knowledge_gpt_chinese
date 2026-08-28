# Case：Liquid Cooling Datacenter Retrofit——机房改造不是换服务器

## 决策情境

现有数据中心希望部署高密度 AI racks。服务器供应商提供 direct-to-chip 液冷，但建筑最初按较低热密度与风冷设计。决策不是“液冷效率更高吗”，而是现有配电、结构、管路、facility water、消防、控制和维护流程能否一起跨越新的 operating envelope。

## 先做边界审计

~~~mermaid
flowchart TB
  U[Utility / UPS] --> R[Rack power]
  R --> I[IT heat]
  I --> C[Cold plates]
  C --> D[CDU]
  D --> F[Facility water]
  F --> H[Heat rejection]
  B[Building structure] --> R
  O[Operations] --> D
~~~

容量由最小约束决定：

\[
Capacity_{\text{deployable}}=\min(P_{\text{electrical}},Q_{\text{cooling}},L_{\text{floor}},C_{\text{network}},C_{\text{operations}})
\]

[Estimate] 单独升级 cooling 不会突破配电或地板荷载，且每项都要在冗余故障和最高环境温度下 derate。

## Alternatives

**行级 CDU 改造**：施工范围相对局部，可逐区上线；缺点是占空间、管路多、维护点增加。

**集中 secondary loop**：长期效率和管理较好；缺点是初期工程大，切换风险高，failure domain 更广。

**rear-door heat exchanger 过渡**：对服务器改动少，可提高部分密度；但仍依赖空气路径，难覆盖最高热流密度。

**新建专用 hall**：可从头设计供电和液冷；资本和交付周期最大，却可能比在受限建筑内反复改造更经济。

chosen design 要看资产剩余寿命、目标 rack rollout、停机窗口和可复制性。若改造只支持少量孤立 racks，运维复杂度可能超过收益。

## 实施 gate

1. **Survey**：实测电力、供回水、压差、结构载荷、管线空间与 network ingress。
2. **Design validation**：联合验证 P&ID、材料、dew point、leak zoning、controls 和 fail-safe position。
3. **Pilot**：用真实热负载测试泵切换、失电、阀门故障、泄漏报警与自动降载。
4. **Commissioning**：对每条支路平衡流量，记录基线，验证 BMS/DCIM 告警。
5. **Ramp**：按 failure-free hours 和服务能力放量，保留回退容量。

## 为什么不一次性切换

大爆炸式上线减少重复施工，却把 design error 扩散到整区；并行保留风冷提高安全性，却占用容量并延长双系统运维。最稳妥的方案通常是 cell-based rollout，每个单元具有隔离阀、监控和明确回滚条件。

## 经济与二阶效应

液冷可能降低风扇功耗和 chiller 需求，但会增加 CDU、泵、管路、水处理、检漏和技术人员成本。更高 rack density 减少白区面积，却集中网络、配电和故障影响。温水运行可提高 free cooling 机会，却压缩 junction margin。

投资模型应比较“每单位可用算力的改造资本”，并计入停机、延迟收入、保险、spares 和 stranded capacity。验收不能只看入口温度；还应看 hottest device、支路流量、泵冗余切换、残余 air-cooled components 与长时间 workload soak。

## 资料

- [OCP Cold Plate Cooling Loop Requirements](https://www.opencompute.org/documents/cold-plate-cooling-loop-requirements-rev-2-pdf) [Primary Source]
- [ASHRAE Thermal Guidelines](https://www.ashrae.org/technical-resources/bookstore/thermal-guidelines-for-data-processing-environments-5th-ed) [Independent]
- [OCP Advanced Cooling Solutions](https://www.opencompute.org/projects/advanced-cooling-solutions) [Primary Source]


## 基础概念桥接

案例中的数字必须进入统一 waterfall：理论峰值到 kernel、application、system、availability-adjusted output，再到单位经济性。为 base、upside、downside 分别写依赖和触发器，避免把最好条件的演示直接当财务预测。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。
