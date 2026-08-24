# AI Rack Power 与 Cooling Capacity Planning：从 Transient 到 Facility

## 1. 平均功耗无法设计基础设施

AI rack的供电和散热必须处理 steady workload、短时 transient、component derating、冗余、maintenance与故障。平均 wall power适合 energy bill，不足以选择 busbar、PSU、breaker、UPS、CDU、pump与 heat exchanger。

Power chain：

<code>Utility → Transformer/Switchgear → UPS/Battery → PDU/Busway → Rack PSU → DC Busbar → VRM → Package</code>

Heat chain：

<code>Junction → Die/TIM → Cold plate/Heatsink → Coolant/Air → CDU → Facility loop → Heat rejection</code>

两条链由 efficiency相连：每次 conversion loss最终也变成热。

~~~mermaid
flowchart LR
  U[Utility] --> P[Power train]
  P --> R[Rack electronics]
  R --> H[Heat]
  H --> C[Cold plate / air]
  C --> D[CDU]
  D --> F[Facility heat rejection]
  T[Telemetry/control] -.-> P
  T -.-> D
~~~

## 2. Boundary与术语

- TDP：设计/thermal参考，不一定等于 workload average；
- Board power：module输入；
- Rack IT power：所有 compute、CPU、NIC、switch、storage、fans/pumps；
- Facility power：IT加 cooling、conversion、lighting等；
- Provisioned power：为安全与 code保留的 capacity；
- Transient：短时间峰值，可能触发 droop或 protection。

比较必须写 chip/board/rack/wall和 average/peak/provisioned。一个“更省电”GPU若需要更多数量或更强 cooling，facility energy未必下降。

## 3. Power waterfall

[Estimate] Rack IT负载120 kW，rack PSU效率96%、上游 PDU/UPS组合效率94%、facility cooling与辅助功率相当于 IT的15%。

AC输入近似：

<code>120 / (0.96 × 0.94) × 1.15 ≈ 153 kW</code>

若只用120 kW做 utility sizing，少算约28%。[Estimate] 不同 load point下效率会变化，冗余设备低负载也可能降低效率。

## 4. Current与 voltage

<code>I = P / V</code>，resistive loss <code>P_loss = I²R</code>。相同 power下提高 distribution voltage降低 current和 I²R，但改变 conversion、connector、clearance、安全与 service。

[Estimate] 120 kW rack在50 V DC约2,400 A；若等效 resistance为100 micro-ohm，loss约576 W。数字旁有 [Estimate]，但真实设计必须分段计算 conductor、connector与 temperature。

高 current还带来 busbar尺寸、接触电阻、hot spot和 fault energy。Connector插拔与 maintenance规则会影响架构。

## 5. Transient与 power capping

AI kernel phase可让 load快速变化。PSU/VRM capacitor、control loop和 facility equipment在不同时间尺度响应。若所有 accelerators同步进入高功率 phase，rack transient比随机负载更难。

Power capping可以限制峰值、提高可部署密度，但可能降低 performance或产生 straggler。需要测 performance/W和 job completion，不只测 cap。Scheduler可错开 jobs或 collective phase，但增加 orchestration。

## 6. Cooling energy balance

Liquid cooling一阶公式：

<code>Q = mass_flow × Cp × delta-T</code>

[Estimate] 移除100 kW热、coolant比热按4.18 kJ/(kg·K)、温升10°C，质量流量约2.39 kg/s。增大 delta-T可降低 flow，却提高 return temperature和 component temperature；pump curve、heat exchanger approach与 reliability都会变化。

Flow不是唯一指标。Cold plate thermal resistance、contact、manifold balance与 coolant properties决定 junction。最远 branch若流量不足，会在平均 supply正常时形成 hotspot。

## 7. Air、direct liquid与 immersion

Air cooling成熟、service简单，但高 density下风量、fan power、acoustics与 heat exchanger受限。Direct-to-chip liquid把主要热从 cold plate带走，仍需空气处理其他 components。Immersion可覆盖更多元件，但 fluid、materials、service与 ecosystem不同。

[Primary Source] ASHRAE data center资料和 OCP Advanced Cooling Solutions把 air、cold plate、rear-door、immersion等作为不同设计空间。选择应按 heat capture、temperature、facility loop、maintainability与 supplier qualification。

## 8. CDU边界

CDU隔离 technology loop和 facility water，包含 pumps、heat exchanger、filter、control与 leak detection。它有容量、redundancy、flow/pressure与 approach temperature。一个 CDU nameplate可服务多少 racks取决于真实 delta-T和 derating。

CDU failure可能影响多个 racks，是 correlated failure domain。N+1 pump不等于 N+1 heat exchanger/control/power。Maintenance期间的 bypass和水质处理必须进入 runbook。

## 9. Water chemistry与 materials

Coolant与 copper、aluminum、nickel、polymer、seal相容性影响 corrosion、biofouling、particles和 conductivity。不同 OEM cold plates混在同 loop可能有材料冲突。水质不仅是 facility问题，也是 IT warranty边界。

要求定义 fluid、additives、filter、sampling、flush、leak detection和 end-of-life disposal。早期 demo使用实验室纯水不代表多年 field可靠性。

## 10. Thermal transient

Silicon温度对短 burst可由 thermal mass缓冲，coolant/facility响应更慢。控制系统要避免 pump/valve oscillation和 condensation。Inlet温度、dew point、flow变化与 workload telemetry可联合控制，但增加 cyber和 software风险。

高 return temperature有利于 free cooling/heat reuse，却减少 silicon thermal margin。最优 facility efficiency可能与最高 accelerator frequency冲突。

## 11. Redundancy与 derating

Power和cooling equipment常按 N、N+1、2N等设计，但冗余必须落到完整 path。两个 utility feeds若共享 substation不独立；两个 CDU若共享控制器或 header仍有共同点。

Derating考虑 ambient、altitude、temperature、aging与 safety code。Nameplate总和减去冗余、maintenance和最坏 component failure才是 usable capacity。

## 12. Commissioning

纸面设计需要 integrated systems test：

- step load与 transient；
- PSU/UPS transfer；
- breaker/overcurrent；
- pump/valve/CDU failover；
- leak与 sensor failure；
- loss of facility water；
- control network outage；
- hot rack/blocked flow；
- restart sequencing；
- thermal soak。

测试应在真实 IT emulator或受控 workload下做，并确认 telemetry time alignment。未经故障演练的冗余只是 topology图。

## 13. Why-not

### 为什么不只提高 rack功率

Utility、busway、floor、cooling、service和 fire code可能不支持；更高 density还扩大单 rack failure。

### 为什么不把所有热都液冷

NIC、memory、VRM、optics和 storage仍可能靠空气；全液冷增加连接与漏液点。Heat-capture比例要测。

### 为什么不追求最低 inlet温度

更冷需要更多 chiller energy并增加 condensation风险；设备只需在可靠 envelope内运行。

## 14. Engineering → Strategy

| Constraint | Capex | Opex/风险 | 价值捕获 |
|---|---|---|---|
| Utility | substation | demand charge | energy/site |
| Rack distribution | busbar/PSU | loss/service | power equipment |
| Transient | storage/control | complexity | power electronics |
| Cold plate | liquid loop | leaks/materials | thermal supplier |
| CDU | pumps/HX | maintenance | cooling platform |
| Facility rejection | chiller/tower | water/energy | facility operator |
| Telemetry | sensors/software | cyber | DCIM/control |

## 15. Technical diligence questions

1. Power boundary、average、peak、transient与 provisioned？
2. Full power waterfall和 load-point efficiency？
3. Busbar current、connector与 fault protection？
4. Workload power trace与 cap performance？
5. Heat capture、flow、delta-T与 junction margin？
6. CDU/facility derating和 correlated failure？
7. Coolant/material compatibility与 warranty？
8. Air-cooled residual components？
9. Integrated commissioning fault tests？
10. Facility energized date和 expansion option？

## 16. Takeaways

1. Facility按 transient、derating和 failure设计，不按平均 chip power。
2. Power conversion loss全部变热，必须用统一 boundary。
3. Liquid flow由热平衡给出，但 junction取决于完整 thermal resistance。
4. CDU、water和 control形成新的系统与故障域。
5. 可部署 compute由供电、散热和 commissioning共同决定。

## Primary sources

- [Primary Source] [ASHRAE Datacom Series](https://www.ashrae.org/technical-resources/bookstore/datacom-series)
- [Primary Source] [ASHRAE：Emergence and Expansion of Liquid Cooling](https://www.ashrae.org/file%20library/technical%20resources/bookstore/emergence-and-expansion-of-liquid-cooling-in-mainstream-data-centers_wp.pdf)
- [Primary Source] [Open Compute Project Advanced Cooling Solutions](https://www.opencompute.org/wiki/Cooling_Environments_Advanced_Cooling_Solutions)
