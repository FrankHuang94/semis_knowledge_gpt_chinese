# AI Datacenter Engineering Core

目标：用 60–80 小时建立可以与工程师进行有技术含量对话的全栈 mental model。

## 第一圈：全栈直觉（4–6 小时）

1. 现代 AI 数据中心
2. Follow the Data
3. Bottleneck Map
4. [Training vs Inference](../07_ai_workloads/training_vs_inference.md)
5. [Prefill vs Decode](../07_ai_workloads/prefill_vs_decode.md)

完成后应能说清：token 为什么会在 compute、memory 与 network 之间移动；peak FLOPS 为什么不是 application performance。

## 第二圈：芯片内（15–20 小时）

Computer Architecture → GPU → GEMM/Tensor Core → Precision → [Memory Hierarchy](../08_memory/memory_hierarchy.md) → [DRAM](../08_memory/dram.md) → HBM → Roofline。

完成后应能判断一个 kernel 何时 compute-bound、memory-bound 或 latency-bound，并解释 HBM 增加为何会牵动 package、power、thermal 与 yield。

## 第三圈：芯片间（15–20 小时）

PCIe/CXL → SerDes → Scale-up → Parallelism → Collectives → RDMA/RoCE → Switch/NIC/DPU → Scale-out topology。

完成后应能从 DP/TP/PP/EP 推导 collective pattern，再推导 bandwidth、latency、topology 与 congestion requirement。

## 第四圈：物理系统（12–16 小时）

Optics → Advanced Packaging → Chiplet/3D → Power Delivery → Thermal/Cooling → Modern AI Rack。

完成后应能解释 electrical reach、package routing、rack power density 与 liquid cooling 如何反向决定 silicon roadmap。

## 第五圈：Strategy（10–15 小时）

System Performance Waterfall → Spec Sheet Translator → Value Capture → Supply Chain → Product Evolution → Technical Diligence。

完成后应能把 engineering delta 翻译成 BOM、TCO、supplier leverage、switching cost、moat 与 roadmap risk。

## 自测标准

给出一个陌生 accelerator spec，能够：

- 画出可能的 dataflow 和 system position；
- 用 Roofline 做第一轮 bound 判断；
- 找出缺失的 memory/network/power/software 信息；
- 提出至少三个替代 architecture；
- 指出解决旧瓶颈后最可能出现的新瓶颈；
- 提出十个工程师愿意回答的 diligence questions。
