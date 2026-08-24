# Changelog

本项目采用面向知识库的变更记录：记录新增的 mental model、重大事实更新、结构迁移与来源修订。

## Unreleased

### Added

- 完成 Semiconductor Manufacturing / Supply Chain 与 Software / Hardware Co-design 两篇 Core Curriculum drafts。
- 扩展 good-system flow、yield/cycle time/capacity、compiler IR、fusion/layout、autotuning、runtime 与 performance portability 知识节点。

- 完成 GPU Execution / Kernel Performance 与 Distributed Training / Collectives 两篇 Core Curriculum drafts。
- 扩展 warp scheduling、coalescing、fusion/stall、DP/TP/PP/EP、collective semantics、topology mapping 与 communication overlap 知识节点。

- 完成 Power Delivery 与 Thermal / Cooling 两篇 Core Curriculum drafts。
- 扩展 utility-to-transistor power chain、VRM/PDN/droop、junction-to-facility heat path、cold plate/manifold/CDU 与 flow sizing 知识节点。

- 完成 Switch / NIC / DPU 与 Chiplet / 3D Integration 两篇 Core Curriculum drafts。
- 扩展 packet pipeline、DMA/offload、infrastructure isolation、D2D layer stack、UCIe 与 active base die 知识节点。

- 完成 Modern AI Rack cornerstone draft，Phase 1 Core Cornerstones 全部闭环。
- 扩展 rack-scale system、busbar、liquid loop、CDU、availability-adjusted compute 与 commissioning 知识节点。

- 完成 Datacenter Optics 与 Advanced Packaging 两篇 cornerstone drafts。
- 扩展 pluggable/LPO/CPO、optical transceiver、interposer/RDL、microbump/hybrid bonding、KGD 与 package yield 知识节点。

- 完成 Scale-up vs Scale-out 与 AI Ethernet / RDMA 两篇 cornerstone drafts。
- 扩展 collective traffic、topology、bisection、RDMA、ECN、PFC 与 congestion control 知识节点。

- 完成 PCIe vs CXL 与 SerDes / Signal Integrity 两篇 cornerstone drafts。
- 增加 protocol layering、coherence、memory tiering、PAM4、equalization、FEC 与 retimer 的知识节点。

- 完成 HBM 与 Roofline Model 两篇 cornerstone drafts，并补齐 memory/package economics 与 quantitative bound 的交叉链接。

- 完成 Training vs Inference、Prefill vs Decode、Memory Hierarchy 与 DRAM 四篇 cornerstone drafts。
- 扩展 serving SLO、KV cache、locality、cache/DRAM organization、bank、row buffer 与 refresh 的知识图谱和 glossary。

- 完成 CPU Architecture、GPU Architecture、Matrix Multiplication 与 Tensor Core 四篇 cornerstone drafts。
- 扩展 CPU/GPU execution、GEMM dataflow、MMA、precision 与 software pipeline 的知识图谱和 glossary。

- 初始化 Learning Command Center、taxonomy、MkDocs 与 Mermaid。
- 建立 Follow the Data / Power / Heat / Bottleneck 四个 master frameworks。
- 建立 knowledge graph、glossary、citation 与 product freshness 框架。
- 启动首批四篇 cornerstone articles。

### Quality

- 所有产品事实需带 status、last_verified 与 source_date。
- 关键数字必须区分 Primary Source、Vendor Claim、Estimate 与 Inference。
