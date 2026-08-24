# Company Architecture Database

这里不按市值或新闻热度描述公司，而是记录它控制哪些architecture layers、依赖哪些manufacturing steps、软件生态与客户switching cost在哪里。

## 当前覆盖

| Company | Control points | 关键依赖 | 主要追问 |
|---|---|---|---|
| NVIDIA | GPU、NVLink/NVSwitch、NIC/DPU、CUDA、rack | foundry、HBM、packaging、systems | proprietary scale-up 与 portable software 各贡献多少？ |
| AMD | CPU、Instinct、Infinity、Pensando、ROCm | foundry、HBM、packaging | software coverage 与 rack integration 能否同步？ |
| Intel | x86、Ethernet、foundry、EMIB/Foveros | fabs、external foundry、memory | process/package 如何转成 delivered systems？ |
| TSMC | process/yield、CoWoS/SoIC、allocation | equipment、materials、utilities | 哪个qualified step限制good packages？ |
| AWS | Trainium、Neuron、Nitro、EFA、cloud | silicon、memory、network、facility | vertical integration是否降低customer TCO？ |
| Google | TPU、XLA、framework、cloud | silicon、memory、network、facility | internal workload优势能否外溢？ |
| Broadcom | switch ASIC、SerDes、custom ASIC | foundry、package、optics | merchant与custom value如何分配？ |
| Marvell | custom compute、Ethernet、DPU、optics | foundry、OSAT、optics | design wins到production的转换率？ |
| SK hynix | DRAM/HBM process、stack、test | equipment、materials、stacking | bottleneck在wafer、stack、test还是qualification？ |
| Micron | DRAM/HBM、test、qualification | fabs、equipment、packaging | qualified good-output如何增长？ |

完整字段与sources见 [data/companies.yaml](https://github.com/FrankHuang94/semis_knowledge_gpt_chinese/blob/main/data/companies.yaml)。

## Freshness policy

每条记录必须有last_verified与sources。Moat只记录为hypothesis；公司战略变化、产品状态或supplier dependency发生变化时必须重新核验。
