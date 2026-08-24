# Learning Command Center

欢迎进入 AI Datacenter & Semiconductor Engineering Knowledge Base。

这里的学习单位不是“术语”，而是**一条能够解释真实产品的因果链**。先从 [AI Datacenter Engineering Core](01_learning_paths/ai_datacenter_core.md) 开始；如果马上要参加技术会议，则先读 [Architecture Presentation Decoder](29_hot_chips/how_to_read_architecture_presentation.md)。

## 四个入口

<div class="grid cards" markdown>

- :material-database-arrow-right: **Follow the Data**

    数据在哪里产生、移动、复用、排队和等待？

    [开始追踪一个 Token](00_start_here/follow_the_data.md)

- :material-flash: **Follow the Power**

    设施功率如何变成 transistor switching，又如何限制 rack density？

    [进入 Power Delivery](18_power_delivery/index.md)

- :material-thermometer: **Follow the Heat**

    为什么 cooling 已经成为 chip、package 与 rack 的 architecture input？

    [进入 Thermal](19_thermal_cooling/index.md)

- :material-wall: **Follow the Bottleneck**

    峰值 compute 增加后，为什么 application performance 经常不同比例增加？

    [打开 Bottleneck Map](00_start_here/follow_the_bottleneck.md)

</div>

## 当前 cornerstone

1. [一个现代 AI 数据中心到底是怎么工作的？](20_rack_cluster_datacenter/modern_ai_datacenter.md)
2. [Follow the Data：一个 Token 的完整旅程](00_start_here/follow_the_data.md)
3. [AI 芯片 Bottleneck Map](00_start_here/follow_the_bottleneck.md)
4. [如何读懂一场 Hot Chips 芯片架构演讲](29_hot_chips/how_to_read_architecture_presentation.md)
5. [CPU Architecture：一条 Instruction 如何穿过现代处理器](05_cpu/cpu_architecture.md)
6. [GPU Architecture：为什么大量并行适合 AI](06_gpu_accelerator/gpu_architecture.md)
7. [为什么 Matrix Multiplication 主导 AI](06_gpu_accelerator/why_matrix_multiplication.md)
8. [Tensor Core：小矩阵单元如何成为 AI Engine](06_gpu_accelerator/tensor_core.md)
9. [Training vs Inference：同一个模型，为什么需要两套系统思维](07_ai_workloads/training_vs_inference.md)
10. [Prefill vs Decode：一次 LLM 请求为什么像两种不同 workload](07_ai_workloads/prefill_vs_decode.md)
11. [Memory Hierarchy：为什么算力必须被多层数据供给系统包围](08_memory/memory_hierarchy.md)
12. [DRAM：从一个电容到 AI 系统的容量与带宽墙](08_memory/dram.md)
13. [HBM：为什么 AI 加速器必须把 DRAM 堆到封装旁边](09_hbm/hbm.md)
14. [Roofline Model：把算力、带宽与 workload 放到同一张图](08_memory/roofline_model.md)
15. [PCIe vs CXL：I/O、Coherence 与 Memory Semantics](10_pcie_cxl_io/pcie_vs_cxl.md)
16. [SerDes 与 Signal Integrity：速率、Margin、Power 与 Reach](11_serdes_signal_integrity/serdes.md)
17. [Scale-up vs Scale-out：为什么 AI 集群需要两张网络](12_scale_up/scale_up_vs_scale_out.md)
18. [AI Ethernet 与 RDMA：Congestion、Loss 与 Tail Latency](13_scale_out_networking/ai_ethernet_rdma.md)
19. [Datacenter Optics：为什么高速 SerDes 最终必须把比特变成光](15_optics/datacenter_optics.md)
20. [Advanced Packaging：为什么 AI 芯片的边界已经超出单颗 Die](16_advanced_packaging/advanced_packaging.md)
21. [Modern AI Rack：为什么机柜已经成为计算机](20_rack_cluster_datacenter/modern_ai_rack.md)
22. [Switch、NIC 与 DPU：Packet、DMA、Offload 与 Infrastructure Isolation](14_switch_nic_dpu/switch_nic_dpu.md)
23. [Chiplet 与 3D Integration：Die Partition、D2D Protocol、Coherence 与 Thermal](17_chiplet_3d_integration/chiplet_3d.md)
24. [Power Delivery：从 Utility 到 Transistor 的 Voltage、Current、Loss 与 Transient](18_power_delivery/power_delivery.md)
25. [Thermal 与 Cooling：从 Junction 到 Facility 的 Heat、Flow 与 Reliability](19_thermal_cooling/thermal_cooling.md)
26. [GPU Execution 与 Kernel Performance：Warp、Occupancy、Tiling、Coalescing 与 Stall](06_gpu_accelerator/gpu_execution_kernel_performance.md)
27. [Distributed Training 与 Collectives：DP、TP、PP、EP 如何变成 Network Traffic](07_ai_workloads/distributed_training_collectives.md)
28. [Semiconductor Manufacturing 与 Supply Chain：从 Wafer Start 到 Good AI System](22_manufacturing_supply_chain/manufacturing_supply_chain.md)
29. [Software / Hardware Co-design：Graph、Compiler、Kernel、Runtime 与 Silicon 如何闭环](21_software_hardware_codesign/software_hardware_codesign.md)
30. [Engineering → Strategy：从 Bottleneck、Design Choice 到 Value Capture](26_engineering_to_strategy/engineering_to_strategy.md)
31. [Technical Diligence Playbook：如何拆 Claim、验证 Evidence、识别 Scale-up Risk](27_technical_diligence/technical_diligence_playbook.md)
32. [Engineer Language Decoder：把口语主张变成 Metric、Boundary 与追问](30_engineer_language/engineer_language_decoder.md)
33. [End-to-End Case：如何审计一套“更快、更省电、可量产”的 AI Rack](28_case_studies/end_to_end_ai_system_case.md)

## 阅读纪律

看到任何性能主张，先问 workload、precision、batch、sequence length、software、power、system size、network 与 baseline。看到任何 architecture block，先问它保存什么 state、数据从哪里来、控制从哪里来、带宽和 latency 在哪里，以及删掉它会发生什么。

## Practice & Quantitative Toolkit

- [AI Datacenter Engineering Core 五级测验](32_quizzes/core_quiz.md)
- [AI Datacenter Fermi Exercises](32_quizzes/fermi_exercises.md)
- [Technical Diligence Playbook](27_technical_diligence/technical_diligence_playbook.md)

测验按 Terminology → Mechanism → Architecture → Trade-off → Strategy 递进；数量题要求公开 assumptions、units、sensitivity 与 model failure boundary。
