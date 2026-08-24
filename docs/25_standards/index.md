# Standards & Interface Database

Standards定义可互操作边界；interfaces记录真实系统中data、memory、optical或power如何跨boundary。两者不能混为“兼容”。

## Standards

| Standard | Organization | Version | Status | Scope |
|---|---|---|---|---|
| PCI Express | PCI-SIG | 7.0 | Released | open board/system I/O |
| PCI Express | PCI-SIG | 6.4 | Released | deployed-generation base spec |
| CXL | CXL Consortium | 3.2 | Released | coherent cache/memory/I/O fabric |
| UCIe | UCIe Consortium | 3.0 | Released | package die-to-die |
| 800ZR IA | OIF | 01.0 | Released | coherent DCI interoperability |
| Open Rack V3 | OCP | 1.1 | Adopted | rack mechanical/power/service |

## Interfaces

当前记录PCIe、CXL、UCIe、NVLink、RoCEv2、OIF 800ZR、HBM3E与Open Rack V3 power。每条记录分scope、layers、protocol、topology、alternatives、status、last_verified与sources。

完整数据：

- [data/standards.yaml](https://github.com/FrankHuang94/semis_knowledge_gpt_chinese/blob/main/data/standards.yaml)
- [data/interfaces.yaml](https://github.com/FrankHuang94/semis_knowledge_gpt_chinese/blob/main/data/interfaces.yaml)

## 判断纪律

“符合标准”只支持被测试层的互操作，不自动证明performance、package、firmware、coherence、management或production qualification。Diligence必须问compliance matrix与failed cases。
