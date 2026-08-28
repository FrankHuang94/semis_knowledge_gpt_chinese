---
id: pcie_vs_cxl
title: PCIe vs CXL：同一条 PHY 上，I/O、Cache Coherence 与 Memory Semantics 如何分工
concepts: [pcie, cxl, cxl_io, cxl_cache, cxl_mem, coherence, memory_expansion]
prerequisites: [serdes, memory_hierarchy, cache_coherence, latency, bandwidth]
level: [2, 3, 4]
status: draft
last_verified: 2026-08-24
source_date: 2026-08-24
---

# PCIe vs CXL：同一条 PHY 上，I/O、Cache Coherence 与 Memory Semantics 如何分工

> 第一次阅读：Sections 1–8  
> 第二次阅读：Sections 9–18  
> 深入阅读：Sections 19–26

## 阅读前后

**I should understand before:** [Memory Hierarchy](../08_memory/memory_hierarchy.md)、DMA、cache 与 [SerDes](../11_serdes_signal_integrity/serdes.md)。  
**I should understand after:** 能画出 PCIe 的 transaction/data-link/physical layers，区分 CXL.io、CXL.cache、CXL.mem，解释 device type、coherence、memory expansion/pooling 与为什么 CXL 不会替代所有 PCIe。

## 1. 先告诉我为什么需要它

CPU、GPU、NIC、SSD 与 accelerator 不能靠数千根共享 parallel wires连接：pin、routing、skew、distance 与 interoperability不可扩展。PCIe提供标准化 point-to-point serial I/O，让不同厂商设备发现、配置、DMA、传输与报告错误。

但传统 I/O model 对 fine-grained shared data 有软件成本。Device若频繁读 host memory、host若想把 device-attached memory当作 tier，手工copy、driver ownership与cache flush会增加latency和复杂度。CXL复用PCIe electrical/physical ecosystem，在上层加入cache-coherent与memory semantics。

## 2. 一句话直觉

**PCIe擅长“设备通过packets做I/O”；CXL在兼容I/O之外，加入“谁可以缓存谁的数据、哪段device memory可被host load/store”的一致性contract。**

## 3. 系统位置

~~~mermaid
flowchart LR
  CPU[CPU + Root Complex] <-->|PCIe/CXL Link| SW[Switch]
  SW <--> SSD[PCIe SSD]
  SW <--> NIC[PCIe NIC]
  SW <--> A1[CXL Type 1<br/>cache-capable device]
  SW <--> A2[CXL Type 2<br/>accelerator + memory]
  SW <--> M3[CXL Type 3<br/>memory device]
~~~

CXL不是某一颗memory chip，而是host、device、switch、firmware、OS与security共同遵守的fabric contract。

## 4. 前置知识

Transaction是语义请求；packet是编码后的传输单位；lane是一对差分TX/RX；link由多条lanes组成；coherence保证多个cache看到可定义的一致结果；ordering定义请求可观察顺序。

## 5. 从第一性原理理解 PCIe layering

~~~mermaid
flowchart TB
  SW[Software / Driver] --> TL[Transaction Layer<br/>TLP: read/write/config/message]
  TL --> DL[Data Link Layer<br/>reliability, sequence, flow control]
  DL --> PL[Physical Layer<br/>encoding, training, SerDes]
  PL --> CH[Electrical channel]
~~~

Transaction layer决定“要做什么”；data link保证相邻端可靠搬运并管理credit；physical layer完成link training、lane alignment与signals。分层让protocol功能与SerDes代际可分别演进，但新generation仍需完整validation。

## 6. Follow the Data：一次 device DMA read

1. Driver配置queue与buffers。
2. Device产生memory read request TLP。
3. Data-link/PHY把packet跨link送到root/switch。
4. IOMMU/host fabric检查地址与权限。
5. Host memory返回completion data。
6. Device消费data并写completion/interrupt。

Request与completion共享有限credits和link，small transactions会被headers、round trip与ordering放大。Peak GB/s不能描述single-request latency。

CXL.mem路径则让host以memory load/store语义访问Host-managed Device Memory；coherence与home agent决定cache/state动作。它仍跨有限link，不会变成本地DRAM。

## 7. CXL protocols 与 device types

| Protocol | 主要语义 | 典型用途 |
|---|---|---|
| CXL.io | PCIe-compatible discovery/config/I/O | 所有CXL devices基础管理 |
| CXL.cache | device coherently cache host memory | accelerator访问共享host data |
| CXL.mem | host访问device-attached memory | memory expansion/tiering |
| Type 1 | CXL.io + CXL.cache，无device memory | compute accelerator |
| Type 2 | io + cache + mem | accelerator带local memory |
| Type 3 | io + mem | memory expander |

具体版本能力、switching、fabric与HDM模式要以目标CXL revision和公开规范为准，不能把某一代feature外推到全部设备。

## 8. 关键 engineering parameters

| 参数 | 含义 | 为什么重要 | 代价 |
|---|---|---|---|
| GT/s per lane | symbol/transfer rate | raw link rate | SI/FEC/power |
| Lane width x1–x16 | aggregate rate | bandwidth | pins/routing |
| Payload efficiency | useful bytes/line bytes | application BW | packet size依赖 |
| Round-trip latency | request到completion | fine-grained access | switches/retimers |
| Credits | outstanding traffic state | throughput/避免overflow | buffers |
| Max payload/read request | transaction granularity | header效率/latency | compatibility |
| Coherence scope | participating agents | programmability | snoop/state traffic |
| HDM capacity | host-managed device memory | tier size | link/NUMA |
| RAS/security | poison、IDE等 | production部署 | latency/logic/management |

## 9. Worked example：lane rate不是payload rate

[Primary Source] PCI-SIG说明PCIe 6.0在64 GT/s采用PAM4、256-byte FLIT与FEC。  
[Estimate] x16 raw symbol-based gross quantity为 \(64\times16=1024\) GT/s；不能直接称128 GB/s application payload，因为PAM4/FLIT/FEC、headers、flow control、idle与traffic direction定义都要计入。

对任何PCIe/CXL带宽主张，正确公式是：

\[
BW_{\text{useful}}=R_{\text{lane}}\times N_{\text{lanes}}\times
\eta_{\text{encoding}}\times\eta_{\text{protocol}}\times\eta_{\text{workload}}
\]

Latency还需加controller、switch、retimer、IOMMU、queue、target memory与coherence路径，不能由GT/s推导。

## 10. Bottleneck

- Small dependent reads：round-trip latency/credits；
- Bulk DMA：link payload bandwidth；
- CXL memory：link + media latency、cache miss与NUMA placement；
- 多devices：switch uplink oversubscription/contention；
- Coherence-heavy sharing：invalidations、home-agent与false sharing；
- Device reset/error：fabric RAS与software recovery；
- Retimer多跳：reach改善但latency/power上升。

## 11. Design Space

| 方案 | 优点 | 代价 | 适用 |
|---|---|---|---|
| PCIe DMA | 成熟、开放、streaming高效 | copy/ownership/software | SSD/NIC/accelerator |
| CXL.cache | shared host data更自然 | coherence复杂/latency | fine-grained accelerator |
| CXL.mem | capacity tiering | 远端latency/BW | Type 2/3 memory |
| Proprietary scale-up | 更低latency/高BW | lock-in | tightly coupled GPUs |
| Ethernet/RDMA | 跨rack/大规模 | software/network latency | scale-out |
| Local DRAM/HBM | 最低locality成本 | capacity/BOM | hot working set |

## 12. 为什么两者共存

CXL利用PCIe PHY与CXL.io保持enumeration、management与生态兼容；只在需要时使用cache/mem语义。传统SSD/NIC的大块producer-consumer traffic不需要承担coherence复杂度，PCIe仍更直接。

## 13. 为什么不……？

### 为什么不让所有设备cache coherent？

Directory/home-agent state、ordering、snoop traffic、security与verification随agents扩大；false sharing会使性能不可预测。

### 为什么不把全部DRAM做成CXL pooled memory？

Hot data跨link会增加latency并受uplink BW/oversubscription限制；failure domain与OS tiering也更复杂。本地DRAM仍服务hot working set。

### 为什么不使用proprietary fabric取代PCIe/CXL？

专有fabric可优化，但失去multi-vendor interoperability、OS/firmware生态与volume economics。

### 为什么不只提高GT/s？

更高速率恶化signal margin，需要PAM4、FEC、retimer与更严格channel，power/latency增加；也不解决transaction/coherence bottleneck。

## 14. Trade-off

~~~mermaid
flowchart LR
  C[More coherence / sharing] --> P[Easier programming]
  P --> S[More protocol state]
  S --> L[Latency + verification]
  L --> T[Need locality / tiering policy]
~~~

## 15. Second-order effects

CXL扩capacity后，bottleneck转向OS page placement、telemetry、switch uplink与memory QoS；pooling降低stranded capacity，却扩大fault/security domain。PCIe PHY速度提升后，retimer、connector、PCB material与test价值上升。

## 16. Workload mapping

Training可把cold optimizer/checkpoint staging放远层，但collective不用CXL自动解决；inference可扩weights/KV capacity，但decode对latency/BW敏感；database/in-memory analytics适合tiering；storage/NIC streaming通常PCIe DMA足够。

## 17. Real standards与产品形态

[Primary Source] PCI-SIG Base Specification定义electrical、protocol、platform与programming interface。  
[Primary Source] CXL Consortium公开材料把CXL.io与cache/mem分开，并在CXL 3.2公告中强化memory-device management、monitoring与security。  
产品必须标明支持的revision、device type、link width/rate、switch/OS状态；“CXL-ready”不是可验证性能规格。

## 18. Evolution

Parallel bus → PCIe serial packets → faster PHY/FLIT/FEC → CXL coherent memory semantics → switching/pooling → software placement、QoS与security成为新瓶颈。

## 19. Engineers actually say

“x16 link trained down to x8”“we are completion-latency bound”“credits are limiting”“CXL memory is another NUMA tier”“coherence traffic is pathological”“the switch is oversubscribed”。

## 20. 听到这些话意味着什么

Negotiated width/rate低于设计；带宽未满但依赖read慢；outstanding state不足；远端memory不能当local；sharing pattern制造snoop；下行总量高于uplink。

## 21. 追问工程师

1. Negotiated generation/width？
2. Payload size/read-write mix？
3. Peak、measured、useful BW？
4. Empty/loaded/p99 latency？
5. Retimers/switch hops？
6. Credit/buffer限制？
7. CXL protocol/device type/revision？
8. HDM placement与OS policy？
9. Coherence home agent与scope？
10. NUMA-aware software是否必需？
11. Error/poison/reset recovery？
12. IDE/security与performance overhead？
13. Oversubscription/fairness？
14. 客户平台qualification多久？

## 22. Common misconceptions

1. PCIe generation翻倍等于application翻倍。
2. CXL是“更快PCIe”——主要差异是semantics。
3. Coherence等于zero-copy零成本。
4. CXL memory等于local DRAM。
5. Switch支持总端口带宽就代表non-blocking。

## 23. Engineering → Strategy

| Engineering | System | Business | Strategy |
|---|---|---|---|
| Faster PCIe PHY | more I/O BW | retimer/PCB成本 | PHY生态价值 |
| CXL memory tier | capacity utilization | memory pool产品 | controller/software控制 |
| Coherence | less copy | integration价值 | platform switching cost |
| Switching | composability | pooled infrastructure | management/security moat |
| Open standard | interoperability | 多供应商 | proprietary differentiation受限 |

## 24. Technical Diligence

验证protocol IP、PHY来源、compliance、latency breakdown、coherence correctness、OS/firmware、switch scale、RAS/security、customer qualification与full-system economics。真正moat常在controller/switch silicon、verification、telemetry/tiering software与部署经验，而非“支持CXL”字样。

## 25. 五个 takeaway

1. PCIe分transaction/data-link/physical layers。
2. CXL复用PCIe生态但增加cache/memory semantics。
3. GT/s、GB/s payload与latency不同。
4. Coherence与pooling提高可编程性/利用率，也增加state、tail与failure domain。
5. PCIe、CXL、proprietary scale-up与Ethernet按workload共存。

## 26. 三个开放问题

CXL pooling的真实TCO是否能覆盖switch/software成本？AI KV/optimizer哪些state适合远置？大fabric coherence如何控制tail与security domain？

## Sources

- [Primary Source] [PCI-SIG — PCI Express Architecture](https://pcisig.com/what-pci-express-pcie-architecture)
- [Primary Source] [PCI-SIG — PCIe Base Specifications](https://pcisig.com/specification-overview/pci-express-base)
- [Primary Source] [PCI-SIG — PCIe 6.0 FLIT Mode](https://pcisig.com/what-flit-mode-and-why-did-pci-sig-move-unit-data-exchange)
- [Primary Source] [CXL Consortium — CXL 3.2 Announcement](https://computeexpresslink.org/wp-content/uploads/2024/12/CXL_3.2-Spec-Announcement_FINAL-1.pdf)
- [Primary Source] [CXL Consortium — CXL.io and CXL.cache/mem Paths](https://computeexpresslink.org/blog/integrity-and-data-encryption-ide-trends-and-verification-challenges-in-cxl-compute-express-link-2797/)


## 基础概念桥接

先区分 PHY、link、transaction、I/O、cache coherence 和 memory semantics。协议支持不等于性能；lane width、payload efficiency、round-trip、switch、HDM placement、OS 与 driver 都会影响结果。pool、tier 和 local memory 也不是同义词。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。


## 进阶工程术语桥接

本篇进一步需要掌握：row buffer、refresh、controller、DMA、IOMMU、ATS、page migration、pooling 与 coherence。阅读这些术语时，不只记中英文对应，还要补齐系统位置、正常路径、饱和或失败路径、直接 counter、端到端结果、产品状态和证据等级。若工程会议出现“已解决”“无开销”“已量产”，应立即追问 workload、boundary、configuration、status/date、failure mode 与 falsifier。

延伸阅读：[进阶工程术语手册](../31_glossary/advanced_engineering_terms_handbook.md)。
