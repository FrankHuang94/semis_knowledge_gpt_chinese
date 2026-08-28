# Topology-Aware Collectives：Algorithm 必须映射到真实 Links

## 1. Collective名称不决定流量路径

All-Reduce、All-Gather、Reduce-Scatter与 All-to-All定义通信语义，不定义 ring、tree、hierarchical、rail或 switch offload。相同 ranks与 message在不同 topology mapping下，会经过不同 links、hop和 contention。

目标是让 algorithm的 traffic pattern匹配 scale-up island、NIC rails与 leaf-spine结构，并把跨最慢边界的 bytes放到可 overlap位置。

~~~mermaid
flowchart LR
  G0[GPU0] --- G1[GPU1]
  G1 --- G2[GPU2]
  G2 --- G3[GPU3]
  G0 --> N0[NIC rail A]
  G2 --> N1[NIC rail B]
  N0 --> S[Scale-out fabric]
  N1 --> S
~~~

## 2. Ring 与 tree

Ring把 data分块，沿环 reduce-scatter再 all-gather。大 message时每 rank traffic接近两倍 message，能较均匀使用 links；steps随 ranks增加，小 message latency累积。

Tree用分层 reduce/broadcast，steps增长较慢，适合 latency-sensitive message，但根/上层 links可能热点。Double-tree或 split tree可平衡。没有永久赢家，library应按 size、ranks与 topology选择。

## 3. Hierarchical collective

节点内高带宽 scale-up、节点间较慢 scale-out时，先在 node内 reduce，再跨 nodes，再 node内广播，可减少跨 NIC participants。代价是本地阶段串行化和 aggregation buffer。

[Primary Source] NCCL提供 collective primitives并根据 topology建立 rings/trees；PyTorch DDP通过 gradient buckets触发 reduction。Application应验证实际 path，而不是假设 library总能找到最优。

## 4. Worked traffic

[Estimate] 八个 nodes、每 node八 GPUs，每 rank message为8 GiB。Flat ring有64 ranks，每 rank理想 traffic约：

<code>2 × 63/64 × 8 = 15.75 GiB</code>

若 hierarchical先 node内 reduce、再由每 node代表跨八节点通信，跨 scale-out阶段每 node代表 traffic约14 GiB，但还需 node内两阶段。它可能减少 NIC并发和 route复杂度，却不减少所有 bytes。是否更快取决于 scale-up/scale-out ratio与 overlap。

## 5. Rail mapping

每个 GPU/NIC到不同 switch plane形成 rails。正确 rank mapping能让 traffic留在对应 rail并平衡 uplinks；错误 mapping可能让本地 GPU先跨内部 fabric到远端 NIC，增加 contention。

Scheduler需要 topology labels：host、NUMA、PCIe root、NVLink island、NIC、leaf、rail与 failure group。只按空闲 GPU数量调度会产生性能碎片。

## 6. All-to-All 的不同难题

MoE All-to-All每 rank向多个 peers发不同 token，traffic受 expert load和 routing分布影响。Ring的规则大流直觉不够；incast、small messages、hot expert与 variable size主导。需要 capacity factor、token drop/redistribution与 topology-aware expert placement。

平均 bytes平衡不代表瞬时 queue平衡。最慢 expert或 link决定 layer tail。

## 7. Overlap与 ordering

Gradient bucket ready后才能通信；bucket顺序要在 ranks一致，否则可能 hang。Bucket太大启动晚，太小增加 latency。Compiler graph capture若把整个 backward合并，可能推迟 autograd hook，破坏 overlap。[Primary Source] PyTorch DDP design note明确讨论 bucket与 asynchronous all-reduce。

Overlap还会争 HBM、copy engine和 power。必须看 exposed communication，不是 network utilization。

## 8. Failure与 degraded topology

一条 link或 switch失败后，adaptive routing可能保持连通，却降低 bisection并改变 hop。Collective library是否重新建 communicator、job是否 checkpoint/restart、性能是否降级都要测试。

Topology-aware optimization过度依赖特定 path时，failure可能反而更脆弱。应有 nominal和 degraded plans。

## 9. Why-not

- 为什么不总用 ring：小 message和大 rank latency。
- 为什么不总用 tree：大 message link利用和热点。
- 为什么不让 library自动处理一切：scheduler mapping、multi-tenant congestion和 failure信息可能不完整。
- 为什么不最大化 message bucket：会延迟启动和 overlap。
- 为什么不把所有 ranks放同一巨大 domain：power、cost、switch与 failure blast radius。

## 10. Diligence questions

1. Collective语义、message distribution和频率？
2. Physical topology与 rank mapping？
3. Library实际选择 ring/tree/channels？
4. Scale-up与 scale-out bytes分别多少？
5. Exposed而非 total communication？
6. Rails、oversubscription和 contention？
7. MoE load imbalance和 variable messages？
8. Failure后 communicator与 performance？
9. Scheduler能否避免 topology fragmentation？
10. 新硬件 bandwidth是否被 algorithm使用？

## 11. Takeaways

1. Collective语义必须映射到 ring/tree/hierarchical与 physical topology。
2. 大 message和小 message的最优 algorithm不同。
3. Rank/rail mapping是系统性能的一部分。
4. Overlap受 gradient ready order和 shared resources限制。
5. Degraded topology下的表现决定 production scaling。

## Primary sources

- [Primary Source] [NVIDIA NCCL Documentation](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/)
- [Primary Source] [PyTorch DDP Design Note](https://docs.pytorch.org/docs/stable/notes/ddp)


## 基础概念桥接

先区分 packet、frame、flow、queue、buffer、routing、congestion、loss 与 collective。线速不是应用吞吐，平均利用率也看不到 microburst。消息尺寸、incast、ECN、PFC、retransmission、topology 和 job placement 必须联合测试。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。
