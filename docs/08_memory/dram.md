---
id: dram
title: DRAM：从一个电容到 AI 系统的容量与带宽墙
concepts: [dram, sdram, row_buffer, bank, channel, refresh, memory_controller, ddr, gddr, hbm]
prerequisites: [memory_hierarchy, bandwidth, latency, capacitor, signal_integrity]
level: [2, 3, 4]
status: draft
last_verified: 2026-08-23
source_date: 2026-08-23
---

# DRAM：从一个电容到 AI 系统的容量与带宽墙

> 第一次阅读：Sections 1–8  
> 第二次阅读：Sections 9–18  
> 深入阅读：Sections 19–26

## 阅读前后

**I should understand before:** Memory hierarchy、bandwidth/latency、基本电容与数字接口。  
**I should understand after:** 能从 DRAM cell 推导 refresh、ACTIVATE、row buffer、bank/channel parallelism 与 timing constraints，解释 advertised MT/s 为什么不等于 application bandwidth，并比较 DDR、GDDR 与 HBM 的 design direction。

## 1. 先告诉我为什么需要 DRAM

Compute 需要保存远超 on-chip SRAM 容量的 weights、activations、KV cache、dataset pages 与 system state。NAND 足够密但访问太慢且写入机制不适合主存；SRAM 足够快却面积和功耗过高。

DRAM 以一个小电容的电荷代表 bit，用高密度换取有限 retention、破坏性读取、复杂时序和外部 controller。它成为主存，不是因为在每个维度最好，而是因为它位于 capacity、cost、latency、bandwidth、endurance 的可用折中点。

## 2. 一句话直觉

**DRAM 把大量 bit 密集地存进 cell array，但访问不是“给地址立即返回”：必须选择 bank、打开 row 到 sense amplifier，再读写 column，并按时 refresh。**

## 3. 它在整个系统哪里？

~~~mermaid
flowchart LR
    C[CPU / GPU] <--> MC[Memory Controller]
    MC <--> PHY[PHY + Channel]
    PHY <--> R[Rank / Stack]
    R --> BG[Bank Groups]
    BG --> B[Bank]
    B <--> RB[Row Buffer / Sense Amplifiers]
    RB <--> A[DRAM Cell Array]
~~~

HBM、GDDR 与 DDR 都是 DRAM family，但在 channel width、data rate、package distance、bank organization、power 与 target workload 上做不同选择。

## 4. 前置知识：一个 cell 为什么需要 sense amplifier

简化的 1T1C cell 用 transistor 连接 storage capacitor 与 bitline。电容极小，stored charge 会泄漏。读取时，wordline 打开，cell 与预充电 bitline share charge，产生微小电压偏移；sense amplifier 放大为 0 或 1，并把数据恢复写回 cell。

因此：

- data retention 有限 → 需要 refresh；
- read 会扰动 stored charge → sense/restore 是访问的一部分；
- 一整条 wordline 的 cells 共同被激活 → row buffer 天然存在；
- cell 密度高，但外围 sense amplifiers、decoders 与 wiring 仍占面积。

## 5. 从第一性原理理解一次访问

### 5.1 PRECHARGE

在打开新 row 前，bitlines 被准备到参考状态。关闭当前 open row 并准备下一次 ACTIVATE 受 \(t_{RP}\) 等 timing 限制。

### 5.2 ACTIVATE

Controller 发 ACTIVATE，选择 bank 与 row。Wordline 打开，整行数据进入 row buffer/sense amplifiers。ACT 到可发 READ/WRITE 的间隔由 \(t_{RCD}\) 等约束。

### 5.3 READ / WRITE

READ/WRITE 选择 open row 中的 columns；数据不是一个 bit 一个 bit过接口，而以 burst 传输。CAS latency、burst length、bus turnaround 与 bank-group timing 共同影响 schedule。

### 5.4 RESTORE / REFRESH

Sense amplifier 恢复被读取的 cell。即使软件不访问，controller 也必须按规则 refresh rows；refresh 会占用部分 bank/command resources，其代价随 density、temperature 与标准机制变化。

## 6. Follow the Data

~~~mermaid
sequenceDiagram
    participant C as Memory Controller
    participant B as DRAM Bank
    participant R as Row Buffer
    C->>B: PRECHARGE old row (if needed)
    C->>B: ACTIVATE row X
    B->>R: sense + restore whole row
    C->>R: READ column Y
    R-->>C: burst data
    C->>R: READ column Z (row hit)
    R-->>C: burst data
    C->>B: PRECHARGE
~~~

若下一请求访问同一 open row，是 **row hit**；若 bank 已关闭，是 row miss；若另一 row 已打开，需要 precharge + activate，形成 row conflict。Controller 会在 latency、fairness、row locality 与 QoS 之间重排 requests。

## 7. Architecture：组织层级

| 层级 | 作用 | 并行/限制 |
|---|---|---|
| Cell | 保存单 bit 电荷 | retention 与 sensing |
| Row | wordline 激活单位 | 一次激活大量 bits |
| Row buffer | 当前 open row | 同 row column access 快 |
| Bank | 独立 cell array/row buffer | 不同 banks 可重叠操作 |
| Bank group | 组织 banks 与 timing | same/different group timing 不同 |
| Rank | 一组 devices 共同提供数据宽度 | rank switching、shared channel |
| Channel / subchannel | controller 到 memory 的接口 | 独立 channel 提升并行 |
| Module / stack | DIMM、package 或 3D stack | capacity、signal、thermal、repair |

不同 generation 和 form factor 的精确组织必须看 datasheet；不能把某个 DDR5 device 的 bank 数、burst 或 timing 当作所有 DRAM 固有属性。

## 8. 关键 engineering parameters

| 参数 | 含义 | 为什么重要 | 不是 |
|---|---|---|---|
| Data rate (MT/s) | 每 pin 每秒 transfers | raw interface speed | application GB/s |
| Bus width | 并行 DQ bits | channel raw BW | chip 总容量 |
| \(t_{RCD}\) | ACT 到 column command 的约束 | row miss latency | 完整 load-to-use |
| CL / RL | READ command 到 data 的时序 | open-row read component | CPU/GPU observed latency |
| \(t_{RP}\) | precharge 时间 | row conflict cost | refresh interval |
| \(t_{RAS}\) | row active 最小时间等约束 | ACT/PRE schedule | bandwidth |
| \(t_{RFC}\) | refresh cycle 占用 | refresh interference | refresh 间隔 |
| \(t_{REFI}\) | 平均 refresh interval | retention requirement | refresh duration |
| Burst length | command 后传输粒度 | bus efficiency/cache-line mapping | row size |
| Banks/channels | 独立并行资源 | hide latency / bandwidth | 无冲突保证 |

Timing 参数通常以 cycles 或 time 表达，controller 还必须同时满足多项约束，如 \(t_{RRD}\)、\(t_{FAW}\)、write recovery、read/write turnaround。不能把 CL 相加当成完整系统 latency。

## 9. 关键 equations 与 worked example

### 9.1 理论 channel bandwidth

\[
BW_{\text{raw}}=
\text{transfer rate}\times\frac{\text{bus width}}{8}
\]

例：一个 64-bit 数据通路工作在 6400 MT/s：

\[
6.4\times10^9\times64/8=51.2\text{ GB/s}
\]

这是 raw peak，未扣 command、refresh、turnaround、idle、ECC organization、conflict、protocol 与 workload inefficiency。DDR5 module 的 subchannel 组织应按具体 module/controller 计算，不能只看“64-bit”标签。

### 9.2 有效 bandwidth

\[
BW_{\text{useful}}=
BW_{\text{raw}}\times \eta_{\text{protocol}}\times
\eta_{\text{schedule}}\times\eta_{\text{access}}
\]

三个效率分别代表 protocol/refresh、controller scheduling 与 useful-byte utilization。它们不是标准固定常数，必须测量。

### 9.3 Row conflict latency 的直觉

极简近似：

\[
T_{\text{conflict}}\gtrsim t_{RP}+t_{RCD}+CL+\text{queue/PHY}
\]

Row hit 可避开 precharge/activate components，但仍有 CAS、queue 与 burst。真实 controller 会 overlap banks，单请求 latency 与 aggregate throughput 因此不可直接互换。

## 10. Bottleneck：DRAM 为什么“没跑满也很慢”

- **Bank-level parallelism 不足**：pointer chasing 每次依赖上一次地址，无法发足够 outstanding requests。
- **Row conflicts**：访问在同 bank 不同 rows 之间跳转，反复 PRE/ACT。
- **Hot bank**：地址映射或 stride 让 traffic 集中到少数 banks/channels。
- **Small/random access**：burst 搬回的数据多数无用。
- **Read/write turnaround**：方向切换需要 timing margin。
- **Refresh interference**：refresh 暂时阻塞相应 resources。
- **Controller queue/QoS**：多 agents 竞争导致 tail latency。
- **PHY/power/thermal limit**：高 data rate 需要 signal integrity、training 与功耗预算。

因此“只达到峰值带宽 30%”可能是 access pattern 的自然上限，不一定是 memory vendor defect。

## 11. Design Space

| 方案 | 优化目标 | 代价 | 适用条件 |
|---|---|---|---|
| 更多 channels | 提升 aggregate BW | pins、PHY、package、power | 多并发 streaming |
| 更高 data rate | 每 pin BW | SI、equalization、power | 板级/短距接口可支持 |
| 更多 banks | bank parallelism | die/periphery、timing complexity | requests 可分散 |
| Larger row | locality/burst efficiency | activation energy、overfetch | spatial locality 高 |
| Closed-page policy | 降未来 conflict 风险 | 放弃 row reuse | random traffic |
| Open-page policy | 利用 row hits | conflicts/fairness | stable locality |
| Prefetch/burst 增大 | 提高 interface efficiency | overfetch、latency granularity | sequential access |
| Wider interface / HBM | 低 data-rate/pin 获高总 BW | package/stack/cost | accelerator near-package |
| Compression/low precision | 增 effective BW/capacity | logic、quality | data 可压缩 |
| Near-memory compute | 少过 I/O 搬数据 | programmability/thermal/yield | 特定 data-intensive ops |

## 12. 为什么 DDR、GDDR、HBM 会分化

- **DDR** 面向 CPU/system memory：module capacity、可扩展通道、成本与通用性重要，走较长 board channel。
- **GDDR** 通过较高 per-pin data rate 和较宽 device interface 服务 graphics/accelerator bandwidth，付出功耗与 signal complexity。
- **HBM** 通过 3D-stacked DRAM、TSV 与非常宽的 near-package interface 获得高 aggregate bandwidth，降低每 pin 速率压力，却增加 advanced packaging、stack yield、thermal 与供应复杂度。

它们没有“绝对更好”的排序。问题是目标 capacity、bandwidth、distance、power、cost 与 package 是否匹配。

## 13. 为什么不……？

### 为什么不用 SRAM 取代 DRAM？

SRAM cell 面积与 leakage 更高，同等 die cost 无法提供相同容量。大 array/多端口还增加 wire 与 access cost。SRAM 适合 hierarchy 上层而非 bulk memory。

### 为什么不把 DRAM row 永远保持打开？

每 bank 同时只能利用有限 open-row state；下一请求可能访问不同 row，导致 conflict。长期 open 还涉及 policy、fairness、power 和 refresh。Controller 需根据 workload 选择。

### 为什么不无限提高 clock/data rate？

Channel loss、crosstalk、jitter、timing margin、training、equalization 与 I/O power 变得更难。HBM 选择更宽、更短的接口，就是另一条 scaling path。

### 为什么增加容量不会自动增加 bandwidth？

Density 增加的是 cells；bandwidth 由 channels、DQ width、data rate、banks 与 schedule 决定。更高 density 甚至可能增加 refresh/repair 复杂度。

### 为什么 on-die ECC 不等于系统 ECC？

On-die ECC 主要帮助 DRAM die 内部 cell reliability，外部 interface、controller path 与多 bit/system-level faults 仍可能需要 end-to-end ECC/RAS。保护范围必须看具体 contract。

## 14. Trade-offs

~~~mermaid
flowchart LR
    D[Higher density] --> C[More capacity]
    C --> R[Refresh / repair / sensing pressure]
    R --> E[More ECC + timing complexity]
    E --> P[Power / latency / usable-capacity cost]
~~~

另一条 trade-off：更高 data rate → 更高 raw BW → 更难 SI/PHY → 更多 training/equalization/power。

## 15. Second-order effects

1. **DRAM bandwidth 推动 package。** 宽接口需要更多 bumps、routing 和 controller area，HBM 把 memory roadmap 与 packaging capacity 绑定。
2. **Capacity 推动 software policy。** KV paging、activation checkpointing、optimizer sharding 都是在管理昂贵 DRAM state。
3. **更快 compute 增大 memory power 占比。** Data movement energy 与 refresh/PHY 进入 rack power budget。
4. **更多 banks 需要更聪明 controller。** 地址映射、QoS、request reordering 与 security isolation 决定实际收益。
5. **Reliability 随规模放大。** 更多 bits、更多 devices、长时间运行使 ECC、scrub、repair、checkpoint 与 fault containment 更重要。

## 16. Workload mapping

| Workload | DRAM access shape | 关注点 |
|---|---|---|
| Training GEMM | 大块 streaming + reuse | HBM BW、capacity、overlap |
| LLM decode | weights/KV repeated reads | useful BW、capacity、batch |
| Recommendation embeddings | random gathers | bank parallelism、latency、capacity |
| CPU databases | cache-line random/scan 混合 | channels、NUMA、tail latency |
| HPC | stencil/streaming/irregular | BW、row locality、ECC |
| Checkpoint | sequential writes | host/network/storage path，而非只看 DRAM |

## 17. Real Product / standard examples

[Primary Source] Micron DDR5 white paper说明 DDR5 通过更高 data rates、16n prefetch、更多 bank organization、长 burst 与 module subchannels 等手段提高 interface efficiency；这些是 generation-specific 设计，不是 DRAM cell 原理本身。

[Primary Source] Micron DDR5 new-features paper讨论 same-bank refresh：只 refresh 选定 banks 可允许其他 banks 继续部分活动，但引入新的 schedule constraints。这显示 refresh 不是简单固定税率，标准和 controller policy 可改变 interference。

[Primary Source] Micron HBM2E technical brief用 ACTIVATE、READ/WRITE、PRECHARGE 的命令序列说明 stacked DRAM 仍遵循 DRAM row/bank 机制；HBM 的差异主要来自 organization、interface 与 package，而不是取消 DRAM 基本物理。

## 18. Product evolution

~~~mermaid
flowchart LR
    A[More compute / cores] --> B[Bandwidth per core falls]
    B --> C[Higher MT/s + more channels/banks]
    C --> D[SI and I/O power wall]
    D --> E[Wider near-package HBM]
    E --> F[Packaging / capacity / yield wall]
    F --> G[More stacks, compression, tiering, new integration]
~~~

Old bottleneck 被解决后，价值会迁移：从 DRAM cell density 到 PHY/controller，再到 TSV、stacking、interposer、thermal 与 software placement。

## 19. Engineers actually say

- “It is a row-buffer hit.”：目标 row 已在 sense amplifiers，避开部分 ACT/PRE。
- “We are not getting bank-level parallelism.”：outstanding requests 或地址分布不足以让多个 banks overlap。
- [Inference] “DDR5-6400 gives 51.2 GB/s per 64-bit path.”：这是基于 data rate 与 bus width 的 raw arithmetic，需问 module organization 与 sustained efficiency。
- “Refresh is eating bandwidth.”：要问 density、temperature、refresh mode 与测量方法。
- “HBM has lower energy per bit.”：需给 generation、traffic、PHY/package boundary 与测量。
- “On-die ECC fixes reliability.”：需问 coverage、visibility 与 end-to-end protection。

## 20. 听到这些话意味着什么？

“带宽翻倍”可能来自 data rate、width、channels、compression 或 workload efficiency，工程含义不同。“Latency 是 14 ns”可能只是某 timing parameter，不能代表 CPU load-to-use 或 GPU global-memory latency。“有 32 banks”不代表 workload 能并行使用 32 banks。

## 21. 我应该追问工程师什么？

1. 具体 memory generation、device organization、channels、ranks、banks 与 bus width？
2. 报告的是 MT/s、raw GB/s、measured GB/s 还是 useful GB/s？
3. Read/write mix、burst、stride、row hit/conflict 比例？
4. Outstanding requests 与 bank-level parallelism？
5. Controller 的 address mapping、page policy 与 QoS？
6. Timing 是 datasheet minimum、controller setting 还是 observed latency？
7. Refresh mode、temperature 与 interference 如何？
8. ECC/CRC/repair 的 coverage 与 capacity/latency overhead？
9. PHY、training、equalization 与 signal margin？
10. HBM stack/package 的 thermal、yield 与 known-good-die flow？
11. Capacity 增加后是否仍有足够 bandwidth per byte？
12. Bottleneck 是 cell array、row buffer、bank schedule、channel、controller、cache 还是 software access pattern？

## 22. Common misconceptions

1. **“DRAM 可以按任意 byte 立即访问。”** 软件地址最终被组织成 channel/rank/bank/row/column，物理传输以 burst 为单位。
2. **“CAS latency 就是 memory latency。”** 完整路径还包括 cache/TLB、queue、ACT/PRE、PHY、fabric 与 controller。
3. **“频率翻倍，应用带宽必然翻倍。”** 需要足够并行、有效 burst、无严重 conflict，并扣除 overhead。
4. **“HBM 不是 DRAM。”** HBM 是 3D-stacked synchronous DRAM family，仍有 banks、rows、refresh 与 controller。
5. **“更多容量总是更好。”** 若 bandwidth 不随 capacity 扩展，访问全部 state 的时间可能更长。

## 23. Engineering → Strategy

| Engineering change | System effect | Product effect | Business effect | Strategic implication |
|---|---|---|---|---|
| Higher density | 更多 capacity/package | 更大模型/state | 降每 bit 成本 | Process/yield/repair 能力关键 |
| More channels/wider interface | 更高 BW | 提高 accelerator utilization | 提高 system ASP/BOM | Controller/package IP 增值 |
| HBM stacking | 高近封装 BW | AI/HPC differentiation | Supply 与 packaging 成约束 | Memory vendor+foundry+OSAT 联动 |
| Better refresh/bank scheduling | 提高有效 BW/tail | 同 DRAM 更好性能 | 软件/控制器杠杆 | Controller know-how 可形成 moat |
| Low precision/compression | 降 bytes | 延展既有 memory | 降 TCO | 数值/codec ecosystem 影响需求 |

## 24. 投资 / M&A Technical Diligence

- **Physics:** cell capacitance、retention、sensing margin 如何随 node scaling？
- **Process:** DRAM-specific process、EUV使用、layer/step、yield 与 cycle time？
- **Architecture:** bank、row buffer、prefetch、I/O organization 的差异？
- **Controller/PHY:** 谁拥有 training、equalization、scheduler 与 RAS IP？
- **Package:** TSV、micro-bump/bonding、base die/interposer、thermal path？
- **Reliability:** ECC、repair、refresh、retention binning 与 field failure？
- **Performance:** raw、sustained、useful bandwidth 和 loaded tail latency？
- **Customer:** target workload 是否真有足够 locality/parallelism？
- **Supply:** wafer、stacking、test、substrate 与 capacity qualification？
- **Economics:** cost/GB、cost/GB/s、power/GB/s 与 package yield？
- **Competition:** 更宽 DDR/GDDR、更多 cache、compression 能否替代？
- **Moat:** cell/process、stack integration、controller/PHY 还是 customer qualification？

## 25. 五个必须记住的 takeaway

1. DRAM 的高密度来自 1T1C-like cell，而 refresh、sense/restore 与时序复杂性是相应代价。
2. 一次访问围绕 bank 与 open row 展开：PRECHARGE、ACTIVATE、READ/WRITE、burst 和 restore。
3. MT/s × bus width 给 raw peak，不给 useful application bandwidth。
4. Banks/channels 提供并行，但只有 access pattern、controller 与 outstanding requests 能利用它。
5. DDR、GDDR、HBM 是同一基本 memory 物理在 distance、width、rate、power、capacity 与 packaging 上的不同答案。

## 26. 三个真正值得继续思考的问题

1. DRAM scaling 越来越依赖 on-die ECC、repair 与复杂 sensing 时，usable density 的经济性应如何衡量？
2. HBM interface 继续变宽后，controller area、package routing、thermal 和 stack yield 哪个会先限制？
3. 若 model architecture 大幅降低 KV 与 parameter bytes，HBM 的战略价值会从 capacity/BW 转向哪些 reliability 或 integration 特性？

## Sources

- [Primary Source] [Micron — Introducing DDR5 SDRAM: More Than a Generational Update](https://www.micron.com/content/dam/micron/global/public/products/white-paper/ddr5-more-than-a-generational-update-wp.pdf)
- [Primary Source] [Micron — DDR5 SDRAM: New Features](https://www.micron.com/content/dam/micron/global/public/products/white-paper/ddr5-new-features-white-paper.pdf)
- [Primary Source] [Micron — DDR5 SDRAM Product and Technical Resources](https://www.micron.com/products/memory/dram-components/ddr5-sdram)
- [Primary Source] [Micron — HBM2E Technical Brief](https://tw.micron.com/content/dam/micron/global/public/products/technical-marketing-brief/micron-hbm2e-memory-wp.pdf)
- [Primary Source] [JEDEC — Memory Standards](https://www.jedec.org/standards-documents/focus/memory-configuration)
- [Primary Source] [Intel 64 and IA-32 Architectures Optimization Reference Manual](https://www.intel.com/content/www/us/en/developer/articles/technical/intel64-and-ia32-architectures-optimization.html)
