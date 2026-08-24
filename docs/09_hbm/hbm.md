---
id: hbm
title: HBM：为什么 AI 加速器必须把 DRAM 堆到封装旁边
concepts: [hbm, dram, tsv, memory_controller, advanced_packaging, memory_bandwidth]
prerequisites: [dram, memory_hierarchy, gpu, signal_integrity]
level: [2, 3, 4]
status: draft
last_verified: 2026-08-24
source_date: 2026-08-24
---

# HBM：为什么 AI 加速器必须把 DRAM 堆到封装旁边

> 第一次阅读：Sections 1–8  
> 第二次阅读：Sections 9–18  
> 深入阅读：Sections 19–26

## 阅读前后

**I should understand before:** [DRAM](../08_memory/dram.md)、[Memory Hierarchy](../08_memory/memory_hierarchy.md)、GPU 与基本 packaging。  
**I should understand after:** 能从 wide I/O、TSV、stack、PHY、controller、interposer 与 workload 推导 HBM 的带宽、容量、功耗和制造代价。

## 1. 先告诉我为什么需要它

AI accelerator 的 matrix units 能极快消费 operands。传统板级 memory 若主要依靠提高每 pin data rate，会遇到 channel loss、PHY power、pin 与 board routing；计算单元等数据时，更多 FLOPS 只是更多 idle silicon。

HBM 把多片 DRAM 竖直堆叠，用 TSV 穿过 dies，以极宽、短距离 interface 放到 accelerator package 旁。它优化 aggregate bandwidth 与 energy/bit，同时增加容量；代价转移到 stacking、known-good-die、2.5D routing、package area、thermal、yield、test 与供应协同。

## 2. 一句话直觉

HBM 不靠一条线无限快，而靠上千条短连接并行搬数据；wide I/O 降低 per-bit 传输压力，却把 memory 与 advanced packaging 绑成一个共同产品。

## 3. 系统位置与 cross-section

~~~mermaid
flowchart TB
  GPU[Accelerator die] <-->|wide interface| INT[Interposer / RDL]
  INT <--> BASE[HBM base / interface die]
  BASE <--> D1[DRAM die 1]
  D1 <--> D2[DRAM die 2]
  D2 <--> DN[DRAM die N]
  TSV[TSVs + bonds] --- D1
  TSV --- D2
  TSV --- DN
~~~

## 4. 前置知识

DRAM bank/row buffer/refresh；bandwidth = data rate × width；die、TSV、bond、interposer；controller、PHY、channel；[Roofline](../08_memory/roofline_model.md) 与 Arithmetic Intensity。

## 5. 从第一性原理理解

宽、短 package interface 不必像长 PCB SerDes 那样依靠强 equalization 与高 swing，就能用并行 width 获得总带宽。Stacking 沿 z-axis 增加容量，TSV 让信号穿过 dies；但 thinning、via、bond alignment、warpage、thermal 与堆叠良率变难。

HBM 仍是 DRAM：仍有 ACTIVATE、row buffer、bank、refresh。它改变 organization、interface 与 integration，不取消 cell physics。

## 6. Follow the Data

~~~mermaid
flowchart LR
  SM[SM / Tensor Core] --> L1[L1 / Shared]
  L1 --> L2[L2]
  L2 --> MC[Controller]
  MC --> PHY[HBM PHY]
  PHY --> PKG[Package wires]
  PKG --> CH[Channel]
  CH --> BK[Bank + row buffer]
  BK --> CELL[DRAM array]
~~~

高总带宽来自许多 channels/banks 同时工作，不表示一个 dependent load 的 latency 同比例下降。

## 7. Architecture blocks

| Block | 职责 | 关键限制 |
|---|---|---|
| DRAM dies | cells、banks、row buffers | density、refresh、yield |
| TSV/bond | 垂直 data/control/power | area、alignment、defect |
| Base/interface die | stack I/O、控制、RAS | process、power、test |
| PHY/controller | timing、mapping、queue | area、training、efficiency |
| Interposer/RDL | accelerator 到 stacks | routing、area、yield |
| Substrate | power 与外部 I/O | warpage、cost |

## 8. 关键 parameters

Pin data rate、interface width、stack height、channels、capacity/placement、bandwidth/placement、energy/bit、temperature、KGD yield 与 final package yield必须一起看。

## 9. Equations 与 worked example

\[
BW_{\text{stack}}=\frac{N_{\text{IO}}\times R_{\text{pin}}}{8}
\]

[Primary Source] Micron HBM3E brief给出 1024 I/O、超过 9.2 Gb/s pin rate 与超过 1.2 TB/s bandwidth；\(1024\times9.2/8\approx1.18\) TB/s，和标称量级一致。

[Estimate] 六个 placement 的 raw aggregation约 \(6\times1.2=7.2\) TB/s；application sustained bandwidth还要扣 protocol、refresh、bank conflict、controller、ECC 与访问效率。

\[
C_{\text{total}}=N_{\text{placements}}\times C_{\text{stack}}
\]

能装下与能及时读完分别对应 capacity 与 bandwidth。

## 10. 何时 HBM 是 bottleneck

Decode反复读 weights/KV；training state放不下；access不能分散 banks；L2 reuse差；compute/low precision增速超过 HBM；on-die NoC 喂不满 controller；thermal限制 rate；package无法容纳更多 stacks。

## 11. Design Space

| 方案 | 优点 | 代价 | 场景 |
|---|---|---|---|
| DDR | capacity/cost/module | bandwidth/pin | CPU/system |
| GDDR | 高 per-pin、板级 | PHY power/reach | graphics |
| HBM | 高 BW/W、容量密度 | package/supply | AI/HPC |
| Larger SRAM | 减 DRAM traffic | die area/leakage | 高 reuse |
| Compression | 增有效 BW | quality/codec | AI data |
| CXL tiering | 扩容量池 | latency/link | cold state |

## 12. 为什么采用 2.5D + stacked DRAM

Logic 与 DRAM 可分别选择合适 process；stack 提供 footprint capacity，interposer/RDL 提供宽横向连接。相比单片集成更现实，相比板级高速 interface更节能。

## 13. 为什么不……？

- 不无限增加 stack：package、routing、controller、power、cooling、yield 与 supply增长。
- 不直接堆在 GPU 上：高功率 logic 与 memory thermal coupling、bond/yield/power更难。
- 不用 SRAM：density 与 leakage 无法经济保存数百 GB。
- 不无限加宽 interface：bumps、TSV、PHY、controller、routing 与 die area有限。

## 14. Trade-off

~~~mermaid
flowchart LR
  B[More stacks / higher rate] --> U[More BW + capacity]
  U --> A[Larger package]
  A --> P[More power + thermal]
  P --> Y[Yield / supply risk]
  Y --> C[Higher cost]
~~~

## 15. Second-order effects

HBM 解决 memory wall 后，bottleneck迁移到 L2/NoC、scale-up、package power、cooling或 software tiling。更多 placements提高 BOM，并把出货绑定 memory qualification与 advanced packaging capacity。

## 16. Workload mapping

Training需要 state/activation capacity；prefill需要大块供给；decode更看 weight/KV bandwidth与capacity；recommendation看随机访问；HPC看streaming、ECC与持续带宽。

## 17. Real products

[Primary Source] Micron HBM3E brief列出24/36 GB、8H/12H、超过1.2 TB/s；性能/功耗比较属于 [Vendor Claim]，必须按footnotes验证。  
[Primary Source] SK hynix HBM3E技术文章说明TSV signals占 peripheral area，interface design本身是关键IP。

## 18. Evolution

\[
\text{more compute}\rightarrow\text{faster/wider HBM}\rightarrow
\text{package/power}\rightarrow\text{bonding/base die}\rightarrow
\text{thermal/yield/supply wall}
\]

## 19. Engineers actually say

“We are HBM-bound”“supports eight HBM sites”“known-good-die is critical”“routing is congested”“top die is thermally limited”。

## 20. 听到这些话意味着什么

TB/s要问raw/sustained、读写、precision、stack数；GB要问usable、ECC、KV/activation；lower power要问energy/bit boundary与workload。

## 21. 追问工程师

1. 每stack width/rate与持续效率？
2. L2/NoC是否先限速？
3. Bank conflict与读写比例？
4. Stack height、bond与TSV？
5. Die/stack/package yield？
6. Test/repair覆盖？
7. Thermal gradient/throttle？
8. PHY/controller area/power？
9. Interposer routing/warpage？
10. 多供应商qualification周期？
11. Offload路径？
12. 新瓶颈在哪里？

## 22. Common misconceptions

HBM不只是快DRAM；peak不等于kernel；更多HBM不必然增性能；主要优势不是同比降latency；stack yield不能仅用单die yield粗暴相乘。

## 23. Engineering → Strategy

| Engineering | System | Business | Strategy |
|---|---|---|---|
| 更宽/快HBM | compute utilization | ASP/BOM | memory leverage |
| More stacks | BW/capacity | package cost | packaging control |
| Better bond/test | yield | supply | know-how moat |
| Lower energy/bit | rack headroom | TCO | efficiency pricing |
| Base-die logic | RAS/interface | customization | value migration |

## 24. Technical Diligence

验证DRAM process、TSV/bond、KGD/test、controller/PHY、routing、thermal、yield、qualification与 cost/GB、cost/GB/s。Moat可能在process、stack integration、interface、test data或长期客户qualification。

## 25. 五个 takeaway

1. HBM用wide short I/O提供AI bandwidth。
2. TSV stacking把yield、test与thermal变成产品问题。
3. Peak BW、usable capacity、application performance不同。
4. More HBM牵动package、power、cooling与supply。
5. 战略价值来自memory + packaging + qualification共同稀缺。

## 26. 三个开放问题

Base die逻辑增加后价值向谁迁移？Hybrid bonding何时成为主流限制？KV compression会把HBM需求转向哪个指标？

## Sources

- [Primary Source] [Micron HBM3E Product Brief](https://www.micron.com/content/dam/micron/global/public/documents/products/product-flyer/hbm3e-product-brief.pdf)
- [Primary Source] [Micron HBM3E](https://www.micron.com/products/memory/hbm/hbm3e)
- [Primary Source] [SK hynix — HBM3E TSV Scaling](https://news.skhynix.com/en/rulebreakers-revolutions-design-scheme-elevates-hbm3e/)
