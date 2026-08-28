# SRAM vs DRAM vs HBM：Memory 选择其实是 Cell、距离与并行接口的联合设计

## 1. 先纠正一个常见分类错误

SRAM 与 DRAM 是不同的存储 cell 与 array 组织；HBM 不是第三种基础 cell，而是把 DRAM die 堆叠、通过 TSV 与宽接口连接到封装内 compute 的系统方案。把三者放在一起比较有用，但必须明确比较层级：

- SRAM 主要回答“怎样在芯片上以低延迟、高局部带宽保存有限 working set”；
- 普通 DRAM 主要回答“怎样以较低 bit cost 提供大容量系统 memory”；
- HBM 回答“怎样让大量 DRAM bandwidth 在有限 package perimeter 与 energy/bit 下靠近 accelerator”。

因此选择不是三选一。现代 accelerator 同时使用 register、SRAM cache/scratchpad、HBM，以及 host DRAM；性能取决于数据能否在正确层被复用。

~~~mermaid
flowchart LR
  ALU[Compute Array] <--> RF[Register]
  RF <--> S[On-die SRAM<br/>cache / scratchpad]
  S <--> H[HBM<br/>stacked DRAM]
  H <--> D[Host DRAM]
  D <--> ST[Storage]
  C[Compiler / Runtime] -.placement.-> S
  C -.placement.-> H
  C -.placement.-> D
~~~

## 2. SRAM：用面积换速度与控制

典型 SRAM cell 通过交叉耦合结构保持状态，不需要像 DRAM 那样周期刷新。读取通常不破坏存储值，适合 cache、register file、queue、metadata table 与软件管理 scratchpad。它可以靠近执行单元，提供很高的局部并行访问。

代价是每 bit 占用更多 transistor 与面积，leakage 和 wire 也会随容量增长。大 SRAM 不只是“多放一些 cell”：更长 wordline/bitline 增加 RC，bank、decoder、tag、ECC 与 routing 占据面积，访问时间可能要求更深 pipeline。离 compute 越远、阵列越大，它越不像理想的单周期 memory。

SRAM 的价值来自避免更昂贵的数据移动。若一个 tile 从 HBM 读一次后在 SRAM 复用许多次，SRAM 面积可能节省大量外部 bandwidth；若数据只访问一次，搬入 scratchpad 反而增加指令与延迟。

## 3. DRAM：用电容与刷新换 bit density

DRAM cell 把 bit 表示为微小电荷。电荷会泄漏，读取涉及 sense amplifier，并且 row activation、precharge、refresh、bank timing 与 scheduling 共同决定观察到的 latency 和 bandwidth。DRAM 芯片内部不是平坦字节数组，而是 channel、rank、bank、row、column 的层次结构。

连续、row-buffer-friendly access 能摊薄 activate 开销；随机访问、bank conflict、read/write turnaround 与 refresh 会降低有效带宽。Memory controller 通过 reordering、interleaving 与 queue management 提高吞吐，但可能牺牲单请求公平性或 tail latency。

DRAM 的关键优势是容量经济性。模型 weights、KV cache、大型 embedding 与 host working set 很难全部驻留在 SRAM。代价是访问距离、I/O energy、时序约束和低于 compute demand 的供给速度。

## 4. HBM：改变的是接口与封装距离

HBM 仍然遵循 DRAM 的 cell、refresh、bank 与可靠性约束，但通过堆叠 die、TSV、base die/logic interface 与非常宽的封装级连接，提高 aggregate bandwidth并降低相对狭窄的高频板级接口压力。它把 memory controller、PHY、interposer/bridge、package routing、power 和 thermal 变成一体化设计。

HBM 并没有“消灭 memory wall”。更高 compute peak、低 precision 与更大模型会继续提高 bytes demand；stack capacity、package area、yield、thermal 与 supply 可能成为新墙。HBM 的 expensive bandwidth 还必须通过 tiling、coalescing、prefetch 与 batching 转为 useful bandwidth。

## 5. 三者的根本 trade-off

| 维度 | SRAM | 普通 DRAM | HBM |
|---|---|---|---|
| 基础 cell | 多晶体管静态 cell | 电容式动态 cell | 堆叠 DRAM cell |
| 典型位置 | on-die | DIMM/board/package 外 | accelerator package 内或近封装 |
| 优势 | 低延迟、局部带宽、可控 | 高容量、低 bit cost、成熟生态 | 高 aggregate bandwidth、较短 I/O |
| 主要成本 | die area、leakage、wire | latency、I/O、refresh | package、yield、thermal、supply |
| 软件角色 | cache 或 scratchpad | system working set | device global memory |
| 常见瓶颈 | capacity/ports/banks | row/bank/queue | sustained utilization/capacity |

表格描述方向，不应被当成跨产品的固定排序。不同工艺、array compiler、controller、package 与 workload 会改变结果。

## 6. 计算：一个 tile 应该复用多少次

[Estimate] 某 tile 大小为 8 MiB，从外部 memory 搬入一次的相对成本记为 100；从片上 SRAM 读取一次的相对成本记为 5；直接从外部 memory 每次重读的成本仍为 100。

若复用次数为 <code>R</code>：

- 不放入 SRAM：<code>Cost_direct = 100R</code>
- 放入 SRAM：<code>Cost_stage = 100 + 5R</code>

当 <code>100 + 5R &lt; 100R</code>，也就是 <code>R &gt; 1.05</code> 时，第二次使用就开始受益。现实还要计入写入、同步、bank conflict、occupancy 与 SRAM capacity。这个模型说明 compiler 为什么积极做 tiling，但也说明一次性 streaming data 不一定值得 staging。

## 7. 为什么不把芯片全部做成 SRAM

第一，容量会迅速吞噬 die area，减少 compute 与 I/O。第二，大阵列的 wire delay、banking 与 leakage 使“SRAM 都很快”不再成立。第三，更大的 die 增加 defect exposure 与 cost。第四，working set 经常远大于片上容量，即使加倍 SRAM 也只是改变 miss point。第五，更多 SRAM 可能降低可驻留 thread block 数，因为每个 kernel 占用的 scratchpad 变大。

合理问题不是“能不能多加 SRAM”，而是每增加一单位 SRAM 能减少多少 HBM bytes、提高多少 utilization、付出多少 die 与 yield cost。

## 8. 为什么不在所有系统中使用 HBM

HBM 需要先进封装、宽 PHY、复杂 power/thermal 与专用 supply chain。许多 CPU、storage、control-plane 与容量型 workload 更看重可扩展 DIMM capacity、可维护性、成本和标准化。若 workload 的访问率不高、locality 不好或 compute 本身较慢，HBM bandwidth 可能闲置。

此外，HBM stack 通常不可像 DIMM 那样现场更换；容量升级与故障隔离更依赖 module/platform design。HBM 应用于 bandwidth value 足以覆盖 package 与 supply premium 的位置，而不是成为身份标签。

## 9. 为什么不做一个完全统一、自动的 memory pool

统一 address space 改善可编程性，但一致地址不代表一致距离。Page placement、migration、coherency、fault handling 与 fabric congestion仍然存在。若 runtime 在关键路径上迁移大页，tail latency 可能突然上升；若多个 accelerator 远程访问同一 pool，fabric 和 directory 可能取代 HBM 成为瓶颈。

[Primary Source] CUDA 文档明确区分 host DRAM、device global memory 与 on-chip register/shared memory，并说明 Unified Memory 可以自动处理可见性或迁移，但最佳性能仍依赖把数据放在访问它的 processor 附近。抽象减少程序员负担，却不能违反 locality。

## 10. Cache 与 scratchpad：谁决定 placement

Cache 由 hardware 自动判断复用，兼容性好，适合动态 access；scratchpad 由 software/compiler 显式分配和搬运，可提供更确定的容量与时序，但需要知道 tile 和 lifetime。

GPU/NPU 常把两者结合：部分 SRAM 做 hardware cache，部分做 shared memory/LDS/local buffer。这个 carveout 本身就是 trade-off。Cache 太大可能保留无用 line；scratchpad 太大可能因单个 block 占用过多而降低并发。应看 hit rate、bytes saved、bank conflict 与 occupancy，而不只看片上容量。

## 11. Reliability 与可制造性

Memory 设计还必须处理 soft error、retention variation、row disturbance、ECC、repair、redundancy、temperature 与 aging。SRAM 需要 bitcell margin 与 array test；DRAM/HBM 需要 refresh、training、channel repair 与 stack-level test。堆叠使单 die defect、bond defect 和 thermal gradient共同影响 final good stack。

Known-good-die 能降低把明显坏 die 带入昂贵封装的概率，却不能发现所有 assembly 后 interaction。更多 stack 提供 capacity/bandwidth，也扩大 package yield、routing 与 power validation 的联合问题。

## 12. Product reality 应怎样读

产品页写“cache、shared memory、HBM capacity、peak bandwidth”时，至少追问：

1. SRAM 是 private、shared、cache 还是 programmable？
2. 容量按 SM、chip、partition 还是 system aggregate？
3. HBM bandwidth 是 pin peak、copy benchmark 还是 application sustained？
4. ECC、metadata 与 system reserve 后可用容量多少？
5. NUMA/partition 是否限制每个 compute tile 可见的带宽？
6. Remote/peer memory 的 latency、coherency 与 failure semantics？
7. Stack、base die、interposer 与 packaging capacity 的来源？
8. Thermal throttling 会不会同时降低 compute 与 memory rate？

[Primary Source] AMD HIP 文档把 registers、LDS 与 HBM 分成不同 scope 的 memory resources；NVIDIA CUDA 文档也把 per-thread、per-block 与 device-wide memory 区分开。不同品牌术语不同，但核心都是 scope、lifetime、placement 与 physical distance。

## 13. Second-order effects

1. 增加 compute peak 会提高 ridge point，使同一 HBM 更容易成为瓶颈。
2. 增加 SRAM 可减少 HBM traffic，却可能降低 compute area 与 occupancy。
3. HBM bandwidth提高后，address generation、crossbar、L2 或 bank conflict 可能成为新限制。
4. 更大 HBM capacity 支持更长 context，也会扩大 KV bandwidth 与 scheduling 难题。
5. Memory pooling提高平均利用率，却把可靠性和隔离扩展到 fabric。
6. 更激进的数据压缩减少 bytes，但增加 decode compute、metadata 与误差管理。
7. 先进封装让 memory 更近，也使 memory supply 与 package qualification成为平台节奏的一部分。

## 14. Engineers actually say

- “It fits in memory.”：问是否包括 weight、KV、activation、workspace、fragmentation 与 reserve。
- “We have enough bandwidth.”：问哪一层、什么 access pattern、多少 useful bytes。
- “The cache should handle it.”：问 working set、reuse distance、associativity 与 conflict。
- “Put it in shared memory.”：问 tile lifetime、bank mapping、同步与 occupancy。
- “Unified memory makes placement irrelevant.”：问 migration、fault、NUMA 与 p99。
- “HBM is faster.”：问 workload 是 bandwidth、latency、capacity 还是 transaction-limited。

## 15. Engineering → Strategy

| 技术变化 | 工程价值 | 新约束 | 商业含义 |
|---|---|---|---|
| 更多 SRAM | 复用、低延迟 | die area、yield | 设计 IP 与工艺价值上升 |
| 更多 DRAM capacity | 更大 working set | latency、power | 容量供应与平台扩展 |
| 更多 HBM stacks | bandwidth/capacity | package、thermal | HBM 与先进封装控制点 |
| 更强 compiler tiling | 减少外部 bytes | 软件复杂度 | software moat |
| Memory pooling | 资源共享 | fabric/coherency | switch、CXL、control plane |
| 压缩/量化 | 减少 bytes | quality/compute | algorithm-hardware co-design |

## 16. Technical diligence questions

1. Workload 的 working set、reuse distance 与读写比例是什么？
2. 每层 memory 的 capacity、scope、latency 与 sustained bandwidth 如何测量？
3. Profiler 中 HBM bytes、cache hit、stall 与 bank conflict各占多少？
4. SRAM 增量能减少多少 external traffic，是否降低 occupancy？
5. HBM capacity 是否受 stack、package 或 allocation reserve限制？
6. Unified/tiered memory 在 p95/p99 下的 migration 行为如何？
7. ECC、repair、degraded mode 与 field failure如何处理？
8. Memory vendor、stack qualification 与 packaging capacity 是否多源？
9. 下一代 compute 提升后，machine balance 如何变化？
10. 成本比较按 chip、module、rack 还是 delivered workload？

## 17. Takeaways

1. SRAM 与 DRAM是 cell/array选择，HBM是堆叠 DRAM 与封装接口的系统选择。
2. Memory hierarchy 的目标是让复用发生在最便宜、最近的层。
3. 更多 SRAM、更多 HBM 或统一地址都不会自动消灭 locality。
4. Software placement 与 tiling决定昂贵 bandwidth能否转成 useful work。
5. Memory 竞争最终连接 die area、package yield、thermal、supply 与 software moat。

## Primary sources

- [Primary Source] [NVIDIA CUDA Programming Guide：GPU Memory](https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html)
- [Primary Source] [NVIDIA CUDA Programming Guide：Device Memory Spaces](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html)
- [Primary Source] [NVIDIA CUDA Best Practices Guide：Device Memory Spaces](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html)
- [Primary Source] [AMD HIP Programming Model：Memory Hierarchy](https://rocm.docs.amd.com/projects/HIP/en/latest/understand/programming_model.html)


## 基础概念桥接

先区分容量、延迟、带宽、并发、访问粒度和持久性。memory hierarchy 依赖 locality；命中率必须和 miss penalty、bank conflict、queue 与搬运放大一起看。更多容量不会自动提高速度，更多带宽也不能消除依赖延迟。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。
