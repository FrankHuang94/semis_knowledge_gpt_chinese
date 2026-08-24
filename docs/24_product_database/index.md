# Product Database

产品记录以status和last_verified为核心，严格区分Announced、Sampling、Production、Shipping、Deployed、Roadmap与Rumored。

## 当前 seed records

| Product / Platform | Company | Category | Status | 主要architecture response |
|---|---|---|---|---|
| GB200 NVL72 | NVIDIA | rack-scale system | Shipping | rack-scale NVLink domain |
| Instinct MI355X | AMD | datacenter GPU | Production | chiplet compute + HBM |
| EC2 Trn2 | AWS | cloud accelerator instance | Deployed | custom silicon + Neuron/EFA |
| Cloud TPU Ironwood | Google | cloud accelerator | Deployed | workload/compiler codesign |
| BlueField-3 | NVIDIA | DPU | Deployed | infrastructure offload/isolation |
| ConnectX-8 | NVIDIA | SuperNIC | Deployed | RDMA endpoint and offload |
| CoWoS Platform | TSMC | packaging service | Production | heterogeneous HBM integration |
| Gaudi 3 | Intel | AI accelerator | Shipping | accelerator + Ethernet scale-out |

完整architecture、old/new bottleneck、missing disclosures与sources见 [data/products.yaml](https://github.com/FrankHuang94/semis_knowledge_gpt_chinese/blob/main/data/products.yaml)。

## 使用纪律

Status不是质量评分；Shipping不等于large-scale Deployed。任何性能比较回到workload、software、power、system boundary与date。数据库优先保存缺失披露，而不是补齐未经证实的规格。
