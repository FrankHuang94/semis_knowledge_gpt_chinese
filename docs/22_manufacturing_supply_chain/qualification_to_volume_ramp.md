# 从 Qualification 到 Volume Ramp：为什么“量产准备”仍离出货很远

## 1. Status必须拆成 evidence gate

新 silicon/package从 first silicon到客户部署经历 bring-up、characterization、qualification、yield ramp、system acceptance、capacity ramp和 shipment。厂商说“production-ready”可能只表示设计/line准备，不代表所有客户已 qualified。

建议 gate：

<code>Tape-out → First silicon → Engineering samples → Internal qualification → Customer sampling → Customer qualification → Production → Shipping → Deployed</code>

每一步有不同 evidence和风险，不能只用日期预测收入。

~~~mermaid
flowchart LR
  S[Samples] --> B[Bring-up]
  B --> Q[Qualification]
  Q --> Y[Yield ramp]
  Y --> C[Customer acceptance]
  C --> V[Volume shipment]
  V --> F[Field learning]
~~~

## 2. Bring-up

Bring-up验证 boot、clock、power、memory、I/O、firmware和 basic tests。能跑 demo不代表 corner、yield或 long workload。Engineering samples可能有 fuse、workaround、低 frequency或功能禁用。

记录 silicon revision、known errata、workaround的 performance/security影响与下一 stepping计划。

## 3. Characterization

跨 voltage、temperature、frequency、process corner测 power/performance、timing、SerDes、memory和 reliability。Datasheet limit应来自 distribution与 guardband，不是少数 golden units。

Characterization会发现 systematic margin，导致 bin调整、firmware cap、board修改或 respin。每项都会影响 schedule和 economics。

## 4. Qualification

Qualification覆盖 package、temperature cycling、humidity、mechanical、burn-in、ESD/latch-up与 application-specific tests。Datacenter还需要 server/baseboard、BIOS、driver、NIC/network、cooling和 manageability。

“JEDEC/PCIe compliant”只是相应标准层；customer qualification往往更严格且包含供应、software和 field service。

## 5. Yield ramp

Yield随 defect Pareto关闭、tool matching、test改善和 supplier learning上升。Ramp速度取决于问题是否 random process还是 systematic design。后者可能需要 mask spin。

要看多 lot、多个 tools/sites、first-pass与 final yield、bin mix、cycle time和 rework。一次高 yield lot不能支持 volume forecast。

## 6. Customer acceptance

客户会用自己的 workload、rack、cooling、network和 software验证。Hyperscaler可能有独立 security、RAS、fleet telemetry与 failure injection。不同客户完成时间不同，不能把首位客户 acceptance外推全部 TAM。

Acceptance criteria应书面化：性能、power、quality、availability、service和 software support。

## 7. Capacity ramp

Process qualified后还要有 tools、materials、operators、testers和 upstream/downstream匹配。Logic、HBM、package、substrate与 board任一不足都会限制 shipment。Installed capacity需要经过 qualification和 yield。

[Estimate] Line nameplate每月20,000，但 uptime85%、cycle mix90%、yield75%、customer-qualified mix80%，effective output：

<code>20,000 × 0.85 × 0.90 × 0.75 × 0.80 = 9,180</code>

用 nameplate预测会高估一倍以上。

## 8. Software readiness

Driver能识别设备只是起点。需要 compiler、libraries、framework、orchestrator、telemetry、firmware update、debug和 support。Early benchmark可能依赖内部 branch，客户无法获得。

Day-0支持应证明 public/released version能重现性能，installation与 rollback有 runbook，known issues有 owner/date。

## 9. Field learning

Shipping后才出现真实 workload、长期 thermal、operator error与规模效应。RMA、correctable error、firmware incident与 customer support会反馈 design/process。Production不是风险终点。

Early field failures可能需要 containment、screen、firmware或 recall。Warranty reserve和 spare supply进入 gross margin。

## 10. Why-not

- 为什么不把 sample当 production：corner、yield、capacity和客户未验证。
- 为什么不把标准认证当客户 acceptance：system boundary更大。
- 为什么不按 tool install直接算 output：uptime、mix、yield、qualification。
- 为什么不等完美再 ship：市场窗口与 learning；但要控制 blast radius。
- 为什么不同时所有客户 ramp：support和供应会过载。

## 11. Evidence dashboard

| Gate | Evidence | 常见风险 |
|---|---|---|
| First silicon | boot/basic test | errata |
| Internal qual | reports/corners | margin |
| Sampling | customer units | limited bin |
| Customer qual | acceptance | workload gap |
| Production | line/release | low yield |
| Shipping | invoice/units | mix |
| Deployed | field telemetry | utilization |
| Mature | stable yield/RMA | price/cycle |

## 12. Diligence questions

1. 当前 gate与明确 evidence？
2. Silicon stepping、errata与 workaround？
3. PVT distribution和 guardband？
4. Qualification scope和 remaining tests？
5. 多 lot yield、bin、cycle和 top defects？
6. 每客户 acceptance status？
7. Effective capacity bridge？
8. Public software能否复现？
9. Supply chain最小 qualified环节？
10. Field RMA、containment和 feedback？

## 13. Takeaways

1. Production-ready、Production、Shipping和 Deployed是不同 gate。
2. Qualification从 component扩展到完整 customer system。
3. Effective output是 nameplate、uptime、mix、yield和 qualification的乘积。
4. Software与 field learning决定 silicon能否变 revenue和客户价值。
5. Status数据库必须附 evidence与 date，不能靠发布语言推断。

## Primary sources

- [Primary Source] [TSMC 2025 Annual Report](https://investor.tsmc.com/static/annualReports/2025/english/index.html)
- [Primary Source] [PCI-SIG Integrators List and Compliance](https://pcisig.com/developers/integrators-list)
- [Primary Source] [AMD Instinct Customer Acceptance Guide](https://instinct.docs.amd.com/projects/system-acceptance/en/latest/)


## 基础概念桥接

先区分 wafer starts、WIP、throughput、cycle time、die yield、assembly yield、qualified capacity 与 good shipments。设备已安装不代表产品可出货；材料、HBM、substrate、test、客户认证和地理风险都会迁移约束。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。
