# Standards & Interface Database

Standards 定义可互操作边界；interfaces 记录真实系统中 data、memory、optical、power 或 coolant 如何跨 boundary。两者不能混为“兼容”。

## Standards

| Domain | Standards | 当前意义 |
|---|---|---|
| Board / coherent I/O | PCIe 6.4 / 7.0、CXL 3.2 | I/O、coherence、memory expansion / pooling |
| Package die-to-die | UCIe 3.0 | chiplet physical、adapter、protocol mapping |
| Accelerator scale-up | UALink 1.0 | open memory-semantic accelerator fabric |
| AI scale-out | Ultra Ethernet 1.0 | Ethernet transport、congestion、security、management |
| Optical DCI | OIF 800ZR | coherent optical interoperability |
| Rack / cooling | Open Rack V3、OCP Project Deschutes | mechanical/power boundary 与 liquid-cooling facility boundary |

以上版本号与 release 状态来自相应 consortium 或 OCP primary sources；它们不证明商业产品已经大规模部署。[Primary Source]

## Interfaces

当前记录 PCIe、CXL、UCIe、NVLink、RoCEv2、OIF 800ZR、HBM3E、Open Rack V3 power、UALink、Ultra Ethernet transport、CXL memory pooling，以及 Project Deschutes facility-to-IT liquid loop。

完整数据：

- [data/standards.yaml](https://github.com/FrankHuang94/semis_knowledge_gpt_chinese/blob/main/data/standards.yaml)
- [data/interfaces.yaml](https://github.com/FrankHuang94/semis_knowledge_gpt_chinese/blob/main/data/interfaces.yaml)

## 判断纪律

“符合标准”只支持被测试层的互操作，不自动证明 performance、package、firmware、coherence、management 或 production qualification。Diligence 必须要求 compliance matrix、版本组合、failed cases、firmware rollback 与 degraded-mode 行为。


## 深化阅读

- [从 Standard Compliance 到 Interoperability](standards_to_interoperability.md)
