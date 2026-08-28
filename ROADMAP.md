# Roadmap

本路线图把项目拆成可验证的 learning outcomes，而不是按页面数量衡量进度。

> 当前状态：Phase 0–5 首轮全部完成；正文规模、链接、来源、结构化情报、知识图谱、MkDocs build 与定量模型均由 CI 验证。

## Phase 0 — Repository Foundation（完成）

- [x] 中文 Learning Command Center
- [x] MkDocs Material、Mermaid、中文搜索配置
- [x] 完整 taxonomy 与目录入口
- [x] knowledge graph、product、company、standard、interface schema
- [x] major article、citation、glossary 模板
- [x] validation 与 index-generation 脚本骨架
- [x] 首批四篇 cornerstone articles 达到质量门槛
- [x] CI 执行 build、link、metadata validation

完成定义：新内容有明确归属、可导航、可引用、可进入图谱，且 MkDocs strict build 通过。

## Phase 1 — Core Cornerstones（完成）

按依赖顺序完成：

- [x] 现代 AI 数据中心
- [x] Follow the Data：一个 Token 的旅程
- [x] Bottleneck Map
- [x] 如何读 Hot Chips 架构演讲
- [x] CPU Architecture
- [x] GPU Architecture
- [x] 为什么 Matrix Multiplication 主导 AI
- [x] Tensor Core
- [x] Training vs Inference
- [x] Prefill vs Decode
- [x] Memory Hierarchy
- [x] DRAM
- [x] HBM
- [x] Roofline Model
- [x] PCIe vs CXL
- [x] SerDes
- [x] Scale-up vs Scale-out
- [x] AI Ethernet / RDMA
- [x] Datacenter Optics
- [x] Advanced Packaging
- [x] Modern AI Rack

质量门槛：每篇能够支撑 30–60 分钟工程对话；包含 mechanism、design space、why-not、quantitative example、second-order effects、strategy lens、diligence questions 与 primary sources。

## Phase 2 — Core Curriculum（60–80 topics，首轮完成）

目标为 100–150 小时 accelerated curriculum。深化 GPU execution、distributed training、collectives、switch/NIC/DPU、optics、chiplet、power/thermal、manufacturing、software/hardware co-design，并建立五级 quizzes 与 Fermi exercises。

当前进度：

- [x] Switch / NIC / DPU
- [x] Chiplet & 3D Integration
- [x] Power Delivery
- [x] Thermal & Cooling
- [x] Distributed Training & Collectives
- [x] GPU Execution & Kernel Performance
- [x] Manufacturing & Supply Chain
- [x] Software / Hardware Co-design
- [x] 五级 quizzes 与 Fermi exercises

## Phase 3 — Product and Company Intelligence（完成首轮）

建立有 freshness metadata 的 product/company database；所有状态明确标记 Announced、Sampling、Production、Shipping、Deployed、Roadmap 或 Rumored。

当前进度：

- [x] Company / Product / Standard / Interface schemas
- [x] 16 家公司 architecture-control records
- [x] 14 个已核验产品/平台 records
- [x] 9 个 standards 与 12 个 interfaces
- [x] Arm、Samsung、switch/retimer/AEC、HBM 与 power/cooling ecosystem
- [x] Product-generation milestone time series
- [x] Source freshness policy 与 high-volatility review queue
- [x] CI required-fields、status、date、source、reference、lineage 与 queue validation

## Phase 4 — Conference Learning Loop（完成首轮）

- [x] 建立 conference inbox 与标准 note template
- [x] 建立概念提取、prerequisite 与 backlink 工作流
- [x] 建立 architecture claim evidence matrix
- [x] 连接 product case、strategy implication 与 open questions
- [x] 区分 provisional note 与 authoritative record

## Phase 5 — Quantitative Strategy Toolkit（完成首轮）

- [x] Spec-sheet translator 与 system performance waterfall
- [x] Cluster / rack sizing
- [x] Yield economics 与 good-output model
- [x] Network / optics port-count model
- [x] Power / cooling capacity planning
- [x] Technical Diligence playbooks 与多类 end-to-end cases

## Phase 6 — Foundations & Engineering Vocabulary Expansion（完成）

- [x] 将 114 个 glossary terms 扩展为可用于工程交流与尽调的深度手册
- [x] 新增工程数学、单位、统计、排队、数量级与不确定性教程
- [x] 新增数字逻辑、时钟、流水线、CPU/GPU、片上存储与并行执行教程
- [x] 为原有 92 篇正文加入模块专属“基础概念桥接”与统一学习入口
- [x] 正文达到 95 篇、209,868 个 Han characters，并由 CI 强制 200,000 下限

## Phase 7 — Advanced Vocabulary & 300K Expansion（完成）

- [x] 结构化 glossary 从 114 个扩展到 233 个工程术语
- [x] 新增进阶工程术语手册，覆盖计算、存储、互连、物理系统、软件运维、标准与战略
- [x] 为扩写前的 95 篇正文加入模块化进阶术语入口
- [x] 正文达到 96 篇、306,410 个 Han characters，全部 docs 达到 311,729
- [x] CI body-only content floor 提升到 300,000

## 持续质量指标

- 中文为主的解释性正文：96 篇、306,410 个 Han characters（排除 index 与模板），CI 下限为 300,000
- 关键 specification citation coverage = 100%
- major article 至少 3 个 why-not、5 个追问、1 个计算例
- 无 broken internal links
- metadata schema validation 通过
- 不重复建立平铺式 glossary 页面
- 每次扩展先 gap analysis，再写内容
