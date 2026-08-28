---
id: memory_hierarchy
title: Memory Hierarchy：为什么算力必须被多层数据供给系统包围
concepts: [memory_hierarchy, locality, cache, register_file, shared_memory, dram, hbm, bandwidth, latency]
prerequisites: [gpu, cpu, matrix_multiplication, arithmetic_intensity]
level: [2, 3, 4]
status: draft
last_verified: 2026-08-23
source_date: 2026-08-23
---

# Memory Hierarchy：为什么算力必须被多层数据供给系统包围

> 第一次阅读：Sections 1–8  
> 第二次阅读：Sections 9–18  
> 深入阅读：Sections 19–26

## 阅读前后

**I should understand before:** CPU/GPU、GEMM、bandwidth、latency 与算术强度。  
**I should understand after:** 能从 working set、reuse、access pattern 与 scope 推导数据应放在哪一层，区分 cache、scratchpad、register、DRAM/HBM、host memory 与 storage，并用 AMAT、bandwidth 和 Roofline 解释性能。

## 1. 先告诉我为什么需要它

Arithmetic units 可以在极短时间内消费大量 operands，但“大、快、便宜、低功耗、可共享”的存储无法同时实现。若所有数据都来自远端大容量 memory，计算单元会等待；若所有数据都放在最快 SRAM，面积、漏电、线长与成本不可接受。

Memory hierarchy 的本质不是把不同产品排成金字塔，而是利用 workload 的 **temporal locality、spatial locality、parallelism 与 explicit reuse**，把少量当前最有价值的数据逐级靠近计算。

没有 hierarchy，峰值 FLOPS 会成为一座无法被喂饱的工厂。

## 2. 一句话直觉

**越靠近 compute 的 memory 越快但越小、越贵且 scope 越窄；系统通过 cache、tiling、prefetch 和 placement，让数据的大部分访问在更近层命中。**

## 3. 它在整个系统哪里？

~~~mermaid
flowchart LR
    ALU[ALU / Tensor Core] <--> R[Registers]
    R <--> S[L1 / Shared / Local SRAM]
    S <--> L2[L2 / LLC]
    L2 <--> D[Device DRAM / HBM]
    D <--> H[Host DRAM]
    H <--> ST[SSD / Object Storage]
    ST <--> NW[Remote Storage / Network]
~~~

这个图是 logical hierarchy。具体产品可能有 victim cache、distributed L2、cache-coherent fabric、stacked cache、near-memory compute 或 unified address space。地址统一不等于物理距离和访问成本统一。

## 4. 前置知识：四个不能混用的轴

1. **Latency**：单个 dependency 从请求到数据可用所需时间。
2. **Bandwidth**：稳定状态下单位时间可传输 bytes。
3. **Capacity**：能保存多少 state。
4. **Scope / sharing**：哪些 threads、cores、devices 能访问和保持一致性。

低 latency 不保证高 aggregate bandwidth；高 data rate 不保证 random access latency 低；capacity 能装下模型也不代表能足够快地读它。

## 5. 从第一性原理理解

### 5.1 为什么 SRAM 更快却不能做全部 memory

SRAM cell、外围电路与布线占面积；更大的 array 需要更长 wordline/bitline、更复杂 banking 和更多 leakage。Register file 还需多端口以同时供给大量 execution lanes，多端口成本随读写口增长很快。

### 5.2 为什么 DRAM 大却更慢

DRAM 用电容存 bit，cell 密度高，但读取需要激活 row、感测微小电荷、通过 row buffer 选择 column，并周期性 refresh。Off-chip/stacked interface、controller queue 与 bank conflicts 进一步增加访问成本。

### 5.3 为什么 locality 可以弥合差距

- Temporal locality：刚访问的数据很可能再次访问。
- Spatial locality：访问某地址后，邻近地址很可能被访问。
- Structured reuse：GEMM 的 tile 可在 on-chip buffer 中被多次乘加。
- Concurrency：多个 independent misses 可并行，隐藏单次 latency。

Hierarchy 的成功条件不是每次访问都快，而是昂贵层只承担低 miss rate 或可高度并行的 traffic。

## 6. Follow the Data：GEMM tile 的旅程

~~~mermaid
flowchart LR
    H[HBM: A/B matrices] -->|bulk tile| L[L2]
    L -->|coalesced load| S[Shared memory / scratchpad]
    S -->|fragments| R[Registers]
    R --> T[Tensor Core MMA]
    T --> R
    R -->|accumulated tile| S
    S -->|writeback| H
~~~

Tiling 让从 HBM 搬来的 A/B tile 被多次复用。若 tile 太小，reuse 不足；太大则占满 shared memory/register，降低 resident warps 或无法调度。Memory optimization 与 occupancy 不是独立问题。

## 7. Architecture：每层解决什么

| 层级 | 典型技术 | 管理方式 | 主要价值 | 主要限制 |
|---|---|---|---|---|
| Register | multiported SRAM-like file | compiler/hardware | 最低 operand latency | 极小、per-thread、pressure/spill |
| L1 / shared | cache + software scratchpad | hardware / programmer | thread block/core 内 reuse | banking、capacity、scope |
| L2 / LLC | shared cache slices | hardware | 跨 block/core reuse、减少 DRAM | hit latency、contention、coherence |
| Device memory | GDDR/HBM DRAM | controller + software placement | 模型与 active state | bandwidth/capacity/power |
| Host DRAM | DDR DRAM | OS/NUMA/runtime | 大容量 system state | device link、NUMA latency |
| SSD | NAND + controller | filesystem/runtime | checkpoint、dataset、cold weights | latency、write endurance |
| Remote tier | networked storage/memory | distributed software | pool capacity、durability | network、failure、consistency |

GPU 中 **shared memory** 是 programmer-managed scratchpad；CPU cache 通常由 hardware 自动管理。两者都使用 on-chip SRAM，却提供不同 contract。

## 8. 关键 engineering parameters

| 参数 | 含义 | 为什么重要 | 牺牲什么 |
|---|---|---|---|
| Capacity | 层级可保存 bytes | 决定 working set hit | area、cost、power |
| Hit latency | 命中到数据可用 | dependency chain 性能 | 更大 cache 往往更慢 |
| Bandwidth | 每秒可供给 bytes | throughput kernels | pins、banks、power |
| Line / transaction size | 一次传输粒度 | spatial efficiency | overfetch |
| Associativity | 地址可映射位置数 | 减 conflict miss | lookup energy/latency |
| Banking | 独立并发子阵列 | aggregate bandwidth | bank conflicts、routing |
| Ports | 同周期访问数 | execution supply | area、timing、energy |
| MSHR / outstanding requests | 可追踪 misses | latency hiding | state/complexity |
| Coherence scope | 保持一致的 agents | programmability | traffic、directory、latency |
| ECC / protection | 检测/纠错 | reliability | capacity、bandwidth、latency |

## 9. 关键 equations 与 worked example

### 9.1 Average Memory Access Time

简化两层模型：

\[
AMAT=T_{L1}+m_{L1}(T_{L2}+m_{L2}T_{mem})
\]

其中 \(m\) 是 local miss rate。例：\(T_{L1}=1\) ns，L1 miss 5%，\(T_{L2}=5\) ns，L2 local miss 20%，memory penalty 100 ns：

\[
AMAT=1+0.05(5+0.2\times100)=2.25\text{ ns}
\]

虽然 memory 是 100 ns，locality 把平均访问成本压低。这个平均值不适合直接解释 serial pointer chase 的 tail，也未计 queueing、TLB、coherence 与 memory-level parallelism。

### 9.2 Bandwidth demand

\[
BW_{\text{required}}=\text{useful operations per second}\times
\frac{\text{bytes moved}}{\text{operation}}
\]

[Estimate] 若目标是 1 PFLOP/s，而 kernel arithmetic intensity 只有 50 FLOP/byte：

\[
BW=10^{15}/50=20\text{ TB/s}
\]

若 HBM 只能持续提供 3 TB/s，compute roof 再高也不能达到目标。Tiling 的价值就是降低从较远层看到的 bytes/operation。

### 9.3 Cache line utilization

若一次取 64-byte line，但算法只用其中 8 bytes：

\[
\eta_{\text{line}}=8/64=12.5\%
\]

物理 bandwidth 看似忙碌，useful bandwidth 只有八分之一。GPU uncoalesced access、CPU strided access 和过大的 granularity 都会造成类似浪费。

## 10. Bottleneck：如何区分哪一层在限制

- L1/L2 miss 高不一定是问题：若 misses 被 prefetch 和 concurrency 隐藏，execution 仍可满载。
- DRAM bandwidth 未满不代表非 memory-bound：serial latency、bank conflict、TLB miss 或 insufficient concurrency 可能限制。
- Cache hit rate 高也不代表快：shared cache contention、coherence invalidation 与 bandwidth saturation 仍可 stall。
- Register spills 会把本应 on-chip 的 values 放到“local memory”；在 CUDA 语义中 local memory 通常位于 device memory 并被 cache，不等于物理上靠近。
- HBM capacity 不足可能触发 host/offload/page migration，使性能呈 cliff 而非平滑下降。

需要同时看 stall breakdown、transactions、hit/miss、achieved bandwidth、outstanding requests、occupancy 与 end-to-end time。

## 11. Design Space

| 方案 | 优化目标 | 代价 | 适用条件 |
|---|---|---|---|
| Larger cache | 提高 hit rate | area、latency、power | working set 有 locality |
| More HBM bandwidth | 提高 far-memory supply | package、power、cost | streaming / low reuse |
| Software-managed scratchpad | 可预测 reuse | programmer/compiler complexity | regular tiling |
| Hardware cache | 自动适配动态访问 | tag/eviction overhead | irregular/data-dependent |
| Prefetch | 提前隐藏 latency | overfetch、pollution | access 可预测 |
| Compression | 增有效 capacity/BW | encode/decode、variable ratio | data 可压缩 |
| Recompute | 少存 activation | 增 compute | compute 比 memory 便宜 |
| Offload/tiering | 扩 capacity | link latency/BW | cold state、SLO 宽 |
| Near-memory compute | 减移动 | programmability、yield、thermal | 特定操作/高 traffic |

## 12. 为什么最终是 hierarchy，而不是一种万能 memory

Memory cell、array、wire、package 与 protocol 在 physical constraints 上形成 Pareto frontier。更靠近 compute 意味着更短 wire、更高 bandwidth，但占用稀缺 die area；更远层用密度和容量换 latency。

Hierarchy 让不同技术各做自己擅长的部分：SRAM 捕获 reuse，DRAM 保存 active working set，NAND 保存 cold state，software 决定 placement 与 movement。

## 13. 为什么不……？

### 为什么不把 cache 做到能装下整个模型？

大 SRAM 消耗 silicon area 与 leakage，访问延迟随规模和线长上升；同一面积可能更适合 compute 或 memory controllers。模型还会继续增长。

### 为什么不完全依靠 hardware cache？

AI kernels 的 tile 与 lifetime 往往可预测。Explicit shared memory 能避免 replacement uncertainty、控制 layout 并协调 threads。但 irregular workloads 仍更适合 cache；二者通常共存。

### 为什么不只增加 HBM bandwidth？

若 bottleneck 是 capacity、serial dependency、L2 contention、register spill 或 host link，HBM pins 增加无效；还会增加 package routing、power、thermal 和成本。

### 为什么不把所有数据统一成一个地址空间？

统一 virtual address 提高可编程性，却不会消除物理 placement。Page fault、migration、coherence 与 remote access 仍有不同代价；“可访问”不等于“本地”。

## 14. Trade-offs

~~~mermaid
flowchart LR
    C[More on-chip capacity] --> H[Higher hit/reuse]
    H --> A[More area + longer wires]
    A --> P[Power / timing pressure]
    P --> N[Less compute or new hierarchy level]
~~~

另一条链是：更大 transfer granularity → 更高 sequential efficiency → 更多 random overfetch → cache pollution 与 bandwidth 浪费。

## 15. Second-order effects

1. **更大 L2 可改变 network demand。** 跨 kernel 或多 SM reuse 命中后，HBM traffic 下降。
2. **HBM 增长改变 package。** 更多 stacks/channels 牵动 interposer、routing、yield、thermal 与 supply chain。
3. **低 precision 同时作用于 compute 与 hierarchy。** 同样 capacity 可放更多 state，同样 bandwidth 搬更多 elements，但转换与 quality 进入软件。
4. **Memory pooling 把 fabric 变成 memory component。** CXL/scale-up 的 latency、coherence 与 failure semantics 决定哪些 state 能远置。
5. **Compiler 变成 memory architect。** Layout、fusion、tiling、liveness 与 recompute 决定每层真实 traffic。

## 16. Workload mapping

| Workload | Locality / working set | 常见瓶颈 |
|---|---|---|
| Training GEMM | tile reuse 高，activation/state 大 | HBM capacity、collectives、on-chip supply |
| Prefill | weights 跨 tokens 复用 | compute、attention、long-context traffic |
| Decode | batch 小，weights/KV 反复读 | HBM bandwidth、KV capacity/latency |
| Recommendation | embedding 随机且巨大 | capacity、random latency、network |
| Graph analytics | pointer/irregular | latency、cache/TLB miss |
| Database scan | streaming | bandwidth、compression |
| HPC stencil | spatial reuse | cache blocking、bandwidth |

## 17. Real Product / architecture examples

[Primary Source] CUDA Programming Guide 明确区分 per-thread register、per-block shared memory、per-device global memory，以及 SM 内 L1/unified data cache 与全 GPU shared L2。这是 programming contract；实际物理结构随 architecture 改变。

[Primary Source] Intel Optimization Reference Manual 使用 L1、L2、LLC 与 external memory 的层级解释 backend memory stalls，并强调 cache/memory latency 随 locality 与 microarchitecture 变化。具体周期数不能跨代外推。

[Primary Source] NVIDIA CUTLASS 的 efficient GEMM 说明高性能矩阵乘通过 hierarchical tiling 在 global memory、shared memory 与 registers 间复用数据。这展示 software structure 如何把 memory hierarchy 变成 compute utilization。

## 18. Product evolution

~~~mermaid
flowchart LR
    A[Compute rises] --> B[DRAM bandwidth wall]
    B --> C[More cache + wider memory]
    C --> D[Package/power wall]
    D --> E[HBM + advanced packaging]
    E --> F[Capacity / data placement wall]
    F --> G[Compression / tiering / pooling / co-design]
~~~

更快 memory 不是终点。每次提高某层后，bottleneck 可能移到上一层供给、下一层 refill、address translation 或 software reuse。

## 19. Engineers actually say

- “The working set fits in L2.”：要问在哪个 phase、是否与其他 tenants/SM 共享。
- “We hit 90% of peak bandwidth.”：要问 physical 还是 useful bytes、读写比例、是否 SLO-compliant。
- “The kernel is latency-bound.”：要问 dependency、outstanding requests、occupancy 与哪个层级。
- “We use shared memory to stage tiles.”：要问 tile size、bank conflicts、double buffering 与 occupancy cost。
- “Unified memory makes placement automatic.”：要问 migration、prefetch、oversubscription 和 steady-state locality。
- “The model fits.”：要问 weights 之外的 KV、activation、workspace、fragmentation 与 redundancy。

## 20. 听到这些话意味着什么？

“Cache 更大”只有在目标 working set 有 reuse 且 hit 能避免昂贵 traffic 时有价值。“Memory bandwidth 翻倍”必须说明接口宽度、data rate、channels、有效 efficiency 与 workload。“On-chip memory”可能是 cache、scratchpad、register 或 SRAM buffer，management 与 scope 完全不同。

## 21. 我应该追问工程师什么？

1. Working set 在各 phase 的大小和 lifetime？
2. 从 register、L1/shared、L2 到 DRAM 的实际 bytes 分别多少？
3. Hit rate 是 global 还是 per-kernel/per-tenant？
4. Line/transaction utilization 与 coalescing 如何？
5. Achieved bandwidth 与 useful bandwidth 的差距？
6. 是 latency、bandwidth、capacity 还是 scope/coherence 限制？
7. 可同时 outstanding 的 requests 有多少，如何隐藏 latency？
8. Tile、register 与 shared allocation 如何影响 occupancy？
9. Page size、TLB reach 与 migration 是否造成 cliff？
10. ECC、scrub、refresh 与 reliability overhead 是否计入？
11. 多设备访问时 placement、coherence 和 topology 如何？
12. 增加 cache/HBM 后下一个 bottleneck 在哪里？

## 22. Common misconceptions

1. **“越大 cache 一定越快。”** 更大可能增加 latency/power，且无 locality 时无效。
2. **“Bandwidth 高就代表 latency 低。”** 宽并行 streaming 接口可高 bandwidth，同时单次 miss 仍很慢。
3. **“Shared memory 是共享给整个 GPU。”** CUDA shared memory 的基本 scope 是 thread block；命名容易误导。
4. **“Local memory 在芯片本地。”** CUDA local 是 per-thread address space，物理数据可在 device memory。
5. **“地址统一就没有数据移动。”** 物理 placement 与 migration 仍决定性能。

## 23. Engineering → Strategy

| Engineering change | System effect | Product effect | Business effect | Strategic implication |
|---|---|---|---|---|
| 更大 on-chip SRAM | 降外部 traffic | 提高特定 workload 利用率 | 降 energy/op | Area allocation 是差异化 |
| 更高 HBM BW/capacity | 扩 active working set | 支持更大模型/并发 | 提高 ASP 与 BOM | Memory/package supply leverage |
| Better tiling/compiler | 提高 reuse | 同 silicon 更快 | 软件提升毛利/TCO | Compiler/library moat |
| Memory tiering | 扩 capacity pool | 新 deployment flexibility | 降昂贵 memory 比例 | Fabric与orchestration控制权 |
| Compression/low precision | 提升有效 BW/capacity | 更多 workload fit | 推迟硬件扩容 | Numerics/quality data 成为壁垒 |

## 24. 投资 / M&A Technical Diligence

- **Cell/array:** 宣称的 memory 是 SRAM、DRAM、NAND 还是新介质？密度与端口？
- **Architecture:** hierarchy 插入哪一层，谁管理，scope 是什么？
- **Workload:** locality 与 reuse 的证据是否来自真实 trace？
- **Bandwidth:** pin、channel、data rate 与 sustained efficiency 是否自洽？
- **Latency:** empty-system、loaded、average 还是 tail？
- **Capacity:** usable 是否扣除 ECC、metadata、reserve 与 redundancy？
- **Software:** compiler/runtime 是否自动 placement、tiling 与 eviction？
- **Package:** PHY、routing、stack、thermal 与 yield 代价？
- **Manufacturing:** 新 memory 的良率、retention、endurance 与 test？
- **Competition:** incumbent 增 cache、压缩或软件优化能否复制大部分收益？
- **Economics:** 每 saved byte、每 useful GB/s 或每 workload 的系统价值？
- **Moat:** cell IP、controller、compiler、package 还是 ecosystem？

## 25. 五个必须记住的 takeaway

1. Memory hierarchy 来自 capacity、latency、bandwidth、power 与 scope 无法由单一技术同时最优。
2. Locality 与 reuse 决定 hierarchy 是否有效；容量本身不创造性能。
3. Cache 是 hardware-managed，scratchpad 是 software-managed，它们解决相似距离问题但 contract 不同。
4. Memory-bound 必须继续拆成 latency、bandwidth、capacity、transaction efficiency、translation 与 contention。
5. 在 AI 系统中，compiler、HBM、package、fabric 与 runtime 都是 memory architecture 的一部分。

## 26. 三个真正值得继续思考的问题

1. 当 on-chip SRAM 面积继续增加，应该用于更大 cache、更多 shared memory，还是用于更近的 matrix operands？
2. CXL/scale-up memory pooling 能承载哪些 cold state，而不会把 latency 和 failure domain 变成新瓶颈？
3. 如果未来 model architecture 主动压缩 KV、激活或参数，memory vendor 的价值会从 capacity 转向哪种 bandwidth/packaging 能力？

## Sources

- [Primary Source] [NVIDIA CUDA Programming Guide — Programming Model and GPU Memory](https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html)
- [Primary Source] [NVIDIA CUDA C++ Best Practices Guide — Device Memory Spaces](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html)
- [Primary Source] [NVIDIA CUTLASS — Efficient GEMM](https://docs.nvidia.com/cutlass/latest/media/docs/cpp/efficient_gemm.html)
- [Primary Source] [Intel 64 and IA-32 Architectures Optimization Reference Manual](https://www.intel.com/content/www/us/en/developer/articles/technical/intel64-and-ia32-architectures-optimization.html)
- [Primary Source] [CUDA Programming Guide — Unified and System Memory](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/understanding-memory.html)


## 基础概念桥接

先区分容量、延迟、带宽、并发、访问粒度和持久性。memory hierarchy 依赖 locality；命中率必须和 miss penalty、bank conflict、queue 与搬运放大一起看。更多容量不会自动提高速度，更多带宽也不能消除依赖延迟。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。
