---
id: switch_nic_dpu
title: Switch、NIC 与 DPU：Packet、DMA、Offload 与 Infrastructure Isolation
concepts: [switch, nic, dpu, dma, packet_pipeline, offload, infrastructure_isolation]
prerequisites: [pcie, serdes, rdma, ethernet, scale_out]
level: [2, 3, 4]
status: draft
last_verified: 2026-08-24
source_date: 2026-08-24
---

# Switch、NIC 与 DPU：Packet、DMA、Offload 与 Infrastructure Isolation

> 第一次阅读：Sections 1–8  
> 第二次阅读：Sections 9–18  
> 深入阅读：Sections 19–26

## 阅读前后

读前需理解 [PCIe/CXL](../10_pcie_cxl_io/pcie_vs_cxl.md)、[SerDes](../11_serdes_signal_integrity/serdes.md) 与 [AI Ethernet/RDMA](../13_scale_out_networking/ai_ethernet_rdma.md)。读后应能区分 switch、NIC、SmartNIC 与 DPU，画出 packet 与 DMA dataflow，并判断 offload 何时节省 host resources、何时只是把复杂度搬到另一颗 silicon。

## 1. 先告诉我为什么需要它

AI cluster 不只需要“连上网”。Packets 要被解析、分类、转发、排队；host memory 与 GPU memory 要被 DMA；virtualization、security、storage、telemetry 与 congestion policy 要在不抢占 application CPU 的情况下执行。

Switch 解决 many-to-many forwarding；NIC 终止 link 并连接 host memory；DPU/SmartNIC 把更多 infrastructure control 与 data plane 放到独立 compute domain。它们共同决定 data 是否及时到达 accelerator，以及 tenant/workload 是否能被隔离。

## 2. 一句话直觉

**Switch 决定 packet 往哪里走，NIC 决定 packet 如何进入主机内存，DPU 决定多少 infrastructure work 在 host 之外执行；offload 节省的 CPU cycles 必须大于新增 data movement、software 和 failure cost。**

## 3. 系统位置

~~~mermaid
flowchart LR
  GPU[GPU / HBM] <--> PCIE[PCIe / DMA]
  CPU[Host CPU / memory] <--> PCIE
  PCIE <--> NIC[NIC / DPU]
  NIC <--> TOR[Leaf switch]
  TOR <--> SPINE[Spine switch]
  DPUCPU[Embedded cores / accelerators] -. policy .-> NIC
  CTRL[SDN / orchestration] -. rules .-> TOR
  CTRL -. lifecycle .-> DPUCPU
~~~

## 4. 前置知识

Packet、frame、header/payload、MAC/IP/transport、queue、buffer、SerDes、PCIe、DMA/IOMMU、interrupt、RDMA、virtual function、P4、TCAM 与 control plane/data plane。

## 5. 第一性原理：为什么需要专用 data plane

General-purpose CPU 擅长复杂控制流，却不适合以确定速率逐 packet 执行相同 parse/match/action。Switch ASIC 与 NIC pipeline 用并行 fixed-function/programmable blocks 处理 headers，并用 queues、schedulers、DMA engines 维持 line-rate movement。

但专用 pipeline 的 on-chip memory 有限。复杂 state、large tables 或 slow-path exception 仍要交给 embedded/host CPU。设计核心是 fast path 与 slow path 的边界。

## 6. Follow the Packet

1. PHY/SerDes 恢复 bits，MAC/PCS 检查 framing/FEC。
2. Parser 提取 headers 与 metadata。
3. Match tables 查找 route、ACL、tunnel、QoS 或 virtual port。
4. Action engine 改写 header、计数或选择 egress。
5. Buffer/queue 吸收 contention，scheduler 选择发送顺序。
6. NIC 端执行 transport、DMA 与 completion。
7. Exception、miss 或 management packet 进入 slow path。

Packet 在每个 queue 等待的时间比 pure wire latency 更易形成 tail。

## 7. Switch architecture

| Block | 职责 | 主要限制 |
|---|---|---|
| SerDes / MAC | physical link termination | power、reach、BER |
| Parser | 识别 protocol fields | header depth、flexibility |
| Match memory | exact/LPM/ternary lookup | SRAM/TCAM area、update rate |
| Action | rewrite、meter、encap | operation set、pipeline stages |
| Buffer | absorb burst/contention | capacity、power、headroom |
| Scheduler | QoS 与 egress arbitration | fairness、latency、complexity |
| Control CPU | routes、firmware、management | convergence、security |

## 8. NIC architecture

NIC 把 network packets 映射为 host-visible queues、DMA descriptors 和 completions。RSS/flow steering 把 flows 分配到 cores；checksum、segmentation、encryption 或 RDMA engines减少 host work；IOMMU 与 memory registration控制可访问地址。

Zero-copy 是减少 copy，不是取消 data movement。Payload 仍穿过 link、NIC buffers、PCIe 与 memory hierarchy。

## 9. SmartNIC 与 DPU 的边界

行业用词并不统一。可操作定义：

- NIC：主要终止 network，并提供有限 fixed-function offloads。
- SmartNIC：在 NIC datapath 上加入更强 programmable packet processing。
- DPU：除 packet path 外，还包含可独立运行 infrastructure software 的 cores、memory、accelerators、security/management root，并能在 host 不可信或重启时继续工作。

不要按品牌判断，应问谁拥有 control plane、能运行什么 code、访问哪些 memory、如何隔离 host。

## 10. Infrastructure isolation

若 host OS 同时拥有 application 与 network/security/storage policy，host compromise 可能绕过 controls，infrastructure tasks 也与 workload争 CPU。DPU 可成为 provider-managed trust domain：管理 virtual switch、encryption、storage path 与 telemetry。

Isolation 的代价是第二个 operating system、firmware supply chain、remote management、secure boot、patching 与 incident response。

## 11. RDMA 与 GPU Direct path

NIC/DPU 可把 registered GPU memory作为 DMA target，减少 CPU copy。有效路径仍受 PCIe topology、IOMMU、BAR/aperture、ordering、NIC cache、GPU synchronization 与 transport congestion限制。把 NIC 放得“更近”只有在完整 topology 和 software stack 支持时才有意义。

## 12. Offload categories

- Stateless：checksum、segmentation、encapsulation。
- Stateful networking：NAT、firewall、connection tracking、load balancing。
- Security：IPsec/TLS、key storage、attestation。
- Storage：NVMe-oF、compression、erasure coding。
- Virtualization：vSwitch、virtio、SR-IOV、rate policing。
- AI communication：RDMA、collectives assist、telemetry。

每项 offload 都要评估 state ownership、fallback、versioning 与 observability。

## 13. 为什么不让 CPU 做所有工作？

CPU 最灵活，但 high packet rate 会消耗 cores、memory bandwidth 与 cache，并增加 jitter。Offload 可释放 host resources；若 workload traffic低、policy快速变化或 offload API不成熟，CPU path 可能更简单、更可观察。

## 14. 为什么不把所有功能硬化？

Fixed-function silicon 的 throughput/energy 最好，却难以适应新 protocols、security bugs 和 cloud policies。Programmable pipeline/cores 提供 agility，但性能、verification 与 isolation更难。实际 DPU 是硬件加速器、packet pipeline 与 general cores 的组合。

## 15. 为什么不把 Switch 与 DPU 合成一颗芯片？

Switch 优化 aggregate radix、buffer 与 many ports；DPU 优化 host-facing PCIe、DMA、tenant isolation 与 infrastructure compute。合并会让 process、package、power 与 lifecycle 更复杂，也扩大 failure domain。某些 rack appliance可共封装，但职责边界仍不同。

## 16. 为什么不把 DPU 当作小型 Server？

DPU 的 cores 能运行 software，却受 memory capacity、thermal、debug、ecosystem 与 upgrade约束。把任意 microservice 搬上 DPU 可能挤占 data plane、增加 tail latency并破坏 isolation。它首先是 infrastructure endpoint，而不是廉价通用 compute。

## 17. 量化例：CPU cores 被 packet work 吞掉多少

[Estimate] 假设 software path 每个 packet 消耗 (1{,}500) CPU cycles，平均 packet rate 为 (20) million packets/s，则总需求为 (30) billion cycles/s。若每个 core 可持续提供 (3) billion useful cycles/s，忽略 cache/NUMA/OS overhead 也约需十个 cores。

[
Coresapproxrac{20	imes10^6	imes1500}{3	imes10^9}=10
]

这不是产品 benchmark；它说明 packet size、cycles/packet 与 burst distribution 比 nominal link rate更能解释 offload value。

## 18. Queue、Buffer 与 Backpressure

NIC receive queues、PCIe credits、host rings、switch egress buffers 与 application consumption rate形成串联 queueing system。某处 slow consumer 会向上游形成 backpressure或drop。DPU增加新的 queues与schedulers，可能改善 isolation，也可能制造隐藏 latency。

## 19. Control plane 与 lifecycle

Rules 需要从 orchestration/SDN 下发到 switch、NIC/DPU，并与 host identity、tenant、job topology一致。Rolling upgrade、rule atomicity、counter consistency、rollback 与 firmware compatibility常比 packet ALU 更难。硬件支持但 control plane未集成，功能等于不存在。

## 20. Reliability 与 security

DPU 成为 trust boundary 后，secure boot、signed firmware、key management、DMA protection、tenant reset 和 crash recovery 都是产品核心。Switch/NIC firmware bug 可影响整个 rack/cluster；可观测性应区分 optical errors、congestion、PCIe stall、DMA fault、rule miss 与 embedded CPU overload。

## 21. Workload mapping 与 second-order effects

Dense training重视 RDMA、collective completion与低 jitter；inference重视 multi-tenancy、security、tail与cost；storage-heavy pipelines重视 compression/encryption/NVMe-oF。Offload解决 CPU bottleneck 后，瓶颈可能迁移到 PCIe、NIC memory、embedded cores、control plane或 network fabric。

## 22. Engineer language decoder

| 说法 | 应翻译成 | 追问 |
|---|---|---|
| “line rate” | 对哪些 packet sizes/functions | table miss与exception呢？ |
| “zero-copy” | 少了哪次copy | DMA与synchronization仍在哪？ |
| “fully programmable” | parser/action/cores可改哪些 | throughput与verification边界？ |
| “hardware offload” | 哪个fast path被硬化 | unsupported flows如何fallback？ |
| “isolated” | trust、DMA、reset与management边界 | DPU compromise影响什么？ |

## 23. 常见误解

1. **DPU 等于更快 NIC。** 关键差异是 infrastructure control 与 trust domain。
2. **Offload 一定降低 latency。** 新 hop、queue、serialization 与 firmware可能反增。
3. **Switch buffer越大越好。** 可掩盖拥塞并增加 tail；控制闭环更重要。
4. **P4/programmability等于任意软件。** Pipeline resource 与 timing严格受限。
5. **CPU freed 等于 TCO saved。** 还要计 DPU power、license、operations和spares。

## 24. Product 与标准 grounding

- [Primary Source] [NVIDIA DOCA Documentation](https://docs.nvidia.com/doca-documentation-3-1-0.pdf) 区分 NIC 与 DPU mode，并描述 embedded control 与 host-facing traffic ownership。
- [Primary Source] [AMD Pensando SSDK Architecture](https://docs.amd.com/r/en-US/ug1669-amd-pensando-ssdk-hello-world-user-guide/Architecture) 展示 P4-programmable data plane 的 parse/match/action使用方式。
- [Primary Source] PCI-SIG、IEEE Ethernet 与 DMTF/virtio等规范分别约束 host I/O、link 与 management/virtualization边界。
- [Vendor Claim] Vendor 的“CPU savings”必须用同 workload、packet distribution、security/storage features与host baseline验证。

## 25. Engineering → Strategy 与 Diligence

Switch/NIC/DPU价值来自 silicon、firmware、SDK、orchestration与fleet telemetry的组合。Platform control可能形成高 switching cost；开放 APIs有助生态，却不能自动保证可移植 performance。

尽调应问：

1. Fast/slow paths分别处理哪些flows？
2. Advertised throughput对应什么 packet size和feature set？
3. Offload前后CPU、PCIe、power与tail如何变化？
4. State由host、DPU还是controller拥有？
5. Embedded cores overload时如何degrade？
6. Firmware/API版本如何rolling upgrade和rollback？
7. DMA与tenant isolation如何验证？
8. Rule/table capacity、update rate与miss behavior？
9. Telemetry能否关联switch、NIC、PCIe与GPU？
10. Savings是否扣除device、license、power与operations？

## 26. 小结与延伸

Switch、NIC 与 DPU 是一条连续 packet-to-memory machine。评价它们时，必须同时看 forwarding、DMA、queue、control、trust、software与failure，而不是只看 port speed。

下一步阅读 [Chiplet & 3D](../17_chiplet_3d_integration/chiplet_3d.md)、[Modern AI Rack](../20_rack_cluster_datacenter/modern_ai_rack.md) 与未来的 distributed training/collectives专题。

## Sources

- [NVIDIA — DOCA Documentation](https://docs.nvidia.com/doca-documentation-3-1-0.pdf)
- [AMD — Pensando SSDK Architecture](https://docs.amd.com/r/en-US/ug1669-amd-pensando-ssdk-hello-world-user-guide/Architecture)
- [IEEE 802.3 Ethernet Working Group](https://www.ieee802.org/3/)
