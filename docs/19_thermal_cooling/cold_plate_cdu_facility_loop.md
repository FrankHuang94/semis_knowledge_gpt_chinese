# Cold Plate、CDU 与 Facility Loop：液冷不是一根水管

液冷把热量更高效地从芯片带走，但没有消灭热量，也没有消灭风冷。完整系统至少包含芯片热界面、cold plate、technology cooling system、CDU 换热与泵、facility water system、heat rejection，以及对内存、电源和光模块的残余空气冷却。任何边界设计错误都会在另一侧表现为温度、压差、泄漏或能耗问题。

## 热如何离开晶体管

\[
Q=\dot m c_p \Delta T
\]

[Estimate] 该能量守恒式说明，在热负载既定时，可以提高流量或允许更大温升；但流量提高会增加压降和泵功，温升扩大又受器件 junction、材料和设施供水温度约束。

~~~mermaid
flowchart LR
  J[Die / TIM] --> P[Cold plate]
  P --> M[Manifold]
  M --> C[CDU secondary loop]
  C --> H[Heat exchanger]
  H --> F[Facility water]
  F --> R[Chiller / cooling tower]
  C --> Q[Pump + control]
  L[Leak detection] -.-> M
  A[Residual air cooling] -.-> DIMM[DIMM / PSU / Optics]
~~~

热阻链也必须端到端看：

\[
T_j=T_{\text{facility}}+Q(R_{\text{facility}}+R_{\text{HX}}+R_{\text{plate}}+R_{\text{TIM}})
\]

[Estimate] 芯片温度不是 cold plate 单一指标；接触压力、流量分配、冷却液老化与换热器 fouling 都会改变长期 margin。

## 为什么不把所有东西直接接 facility water

直接连接可减少换热温差和设备，但把设施水质、压力波动与维护故障带到 IT 设备。CDU 通过热交换器隔离一次侧和二次侧，可控制温度、流量、压力和化学性质；代价是额外温差、泵功、控制系统与维护点。

每排或每柜 CDU 缩短二次管路、故障域较小，却占用 white space；集中 CDU 可提高设备利用率，单点影响范围和管路复杂度更大。没有普适拓扑，选择取决于热密度、建筑改造、冗余、泄漏策略和服务流程。

## 工程约束

1. **流量平衡**：并联 cold plates 的阻抗不同，最小流量支路决定 hottest device。仅看总流量会隐藏局部 starvation。
2. **水质与材料兼容**：铜、铝、焊料、密封件与添加剂可能导致腐蚀、沉积或颗粒。采购 BOM 必须与 coolant specification 联合评审。
3. **压力与瞬态**：阀门动作、泵切换和快速断接会造成 water hammer；软管和接头要覆盖寿命内的压力循环。
4. **露点控制**：供液过冷会产生凝露。控制器必须根据环境湿度保留 margin，而不是只追求最低入口温度。
5. **服务性**：更换 accelerator 时如何隔离、排液、捕获残液、复压和检漏，决定实际停机时间。
6. **残余风冷**：DIMM、VRM、NIC、光模块和 PSU 仍产生热；液冷比例提高后，风道和风扇控制不能被省略。

## Capacity planning

名义 CDU capacity 不等于可部署 IT load。应依次扣除设计裕量、N+1 冗余、最高设施水温下的 derating、泵故障模式、换热器 fouling 和不均匀流量。然后检查 facility side 是否有足够水量、压差和 heat-rejection capacity。

[Estimate] 一个安全模型可写为：

\[
Q_{\text{IT,usable}}=\min(Q_{\text{CDU,derated}},Q_{\text{FWS}},Q_{\text{heat rejection}})-Q_{\text{reserve}}
\]

若只扩 CDU 而不扩 facility loop，新增设备不会增加可用容量；若提高供水温度减少 chiller 能耗，芯片温度 margin 又会缩小。这就是能效、可靠性和资本效率之间的 tradeoff。

## 新瓶颈与运营现实

液冷解决芯片 thermal resistance 后，配电、光模块温度或设施水资源可能成为下一约束。高密度还会缩小故障容忍：一次泵停机造成的温升更快，监控、阀门 fail position 和自动降载必须共同验证。

diligence 应查看 P&ID、材料兼容矩阵、压力/流量 envelope、控制状态机、泄漏检测覆盖、维护演练、spares、commissioning 数据和真实负载热测试。产品状态也要区分“实验室样机”“已通过 qualification”“已在目标设施规模运行”，不能把单机演示当作 fleet readiness。

## 资料

- [OCP Cold Plate Cooling Loop Requirements](https://www.opencompute.org/documents/cold-plate-cooling-loop-requirements-rev-2-pdf) [Primary Source]
- [OCP Cold Plate Development and Qualification](https://www.opencompute.org/documents/ocp-cold-plate-development-and-qualification-with-integrated-comments-pdf) [Primary Source]
- [ASHRAE Thermal Guidelines for Data Processing Environments](https://www.ashrae.org/technical-resources/bookstore/thermal-guidelines-for-data-processing-environments-5th-ed) [Independent]
