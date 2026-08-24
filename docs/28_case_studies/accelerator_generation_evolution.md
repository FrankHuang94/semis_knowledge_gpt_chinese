# Case：Accelerator Generation Evolution——Hopper→Blackwell 与 MI300→MI350 怎么读

## 1. 代际比较不是把 spec列相减

Accelerator generation的真正变化通常同时发生在 compute precision、memory、die partition、scale-up fabric、rack topology、power/cooling、software与 deployment form factor。单颗 GPU更快不代表相同 datacenter能部署更多 useful compute；rack系统更密不代表客户能按期获得 power与 cooling。

本案例不评选赢家，而是训练一种方法：把 NVIDIA Hopper→Blackwell与 AMD MI300/MI325→MI350各自还原为“旧 bottleneck、新 architecture、新 bottleneck”，并区分 shipping事实、vendor claim与 inference。

截至 2026-08-24，本文只把官方产品/开发文档中明确描述的 H100/H200、B200/GB200和 MI300/MI325/MI350系列纳入；未来 roadmap不作为 production evidence。

## 2. Status snapshot

- NVIDIA Hopper H100/H200：Production/Shipping，并已在公开系统与云环境 Deployed。[Primary Source]
- NVIDIA Blackwell B200/GB200：Production/Shipping；CUDA已提供 Blackwell tuning与 compatibility资料，公开 MLPerf/系统材料表明已进入部署。[Primary Source]
- AMD MI300/MI325系列：Production/Shipping，并有官方客户 acceptance与软件文档。[Primary Source]
- AMD MI350X/MI355X：Production/Shipping；AMD在2025年发布，提供产品页、CDNA4白皮书、ROCm架构与 system acceptance文档。[Primary Source]

Status按具体 SKU、地区与 provider仍会不同；“系列已 Shipping”不表示所有 configuration都可即时交付。

## 3. Hopper建立了哪些 architecture方向

Hopper把 Transformer Engine与 FP8、第四代 Tensor Core、更强 NVLink、HBM3和 thread-block cluster/asynchronous data movement组合起来。它解决的是 Transformer compute效率、数据搬运和多 GPU scaling，而不是单纯增加 CUDA cores。

[Vendor Claim] NVIDIA Hopper技术资料列出 H100 SXM的80 GB HBM3与超过3 TB/s memory bandwidth，并描述 FP8 Transformer Engine。数字必须连同 SKU、precision、software与 workload解释。H200又通过更高 HBM capacity/bandwidth延长 Hopper平台，说明 memory wall可以通过中代更新缓解。

Hopper的系统边界主要仍以多 GPU server和 scale-out cluster理解。随着模型和 MoE扩大，rack内更大的低延迟 coherent/scale-up domain成为下一约束。

## 4. Blackwell改变了什么

Blackwell不是只换 GPU die。官方 tuning guide描述更大 memory/L2、第五代 NVLink与延续的 CUDA模型；GB200 NVL72类系统把 rack-scale NVLink domain与 Grace CPU、switch trays、power/cooling共同设计。

[Vendor Claim] NVIDIA Blackwell tuning guide给出 B200 up to 180 GB HBM3/HBM3e；NVIDIA技术资料给出第五代 NVLink的更高 per-GPU bandwidth。更大的 scale-up domain意在减少大模型跨较慢 scale-out边界的 traffic，尤其支持 tensor/expert parallel与 inference。

新瓶颈随之出现：

- 两颗大 dies统一成单 GPU的 package/yield与 D2D；
- HBM3e supply；
- rack busbar、liquid cooling与 service；
- NVLink switch trays和 cable；
- software要用 FP4/FP8、larger domain与 topology；
- 单 rack failure/maintenance blast radius。

Blackwell的竞争单位更接近“rack-scale platform”，采购和价值捕获从 GPU ASP扩展到 CPU、NVLink switch、networking、software与服务。

## 5. MI300建立了哪些方向

MI300系列采用多 chiplet、3D package、XCD/IOD与 HBM的高度集成，并以 Infinity Fabric连接。它体现“不同 die用适合工艺、在 package内组合”的平台路线。大 HBM capacity是其重要定位，适合模型和 HPC state。

Architecture价值取决于 software能否把多 dies、cache与 memory呈现为可用 GPU，以及 ROCm/kernel/library在目标 workload的成熟度。Chiplet降低某些 die与产品复用风险，也把 package、yield、test与 software locality放到核心。

MI325作为同平台 memory-heavy演进，说明代际并非每次都重做 compute；通过 HBM容量/带宽更新可以针对 memory bottleneck延长 baseboard与系统投资。

## 6. MI350/CDNA4改变了什么

AMD CDNA4延续 multi-chip/advanced 3D packaging，增加低精度 formats、compute与 memory能力，并强调与既有 UBB平台兼容。[Vendor Claim] AMD产品页列出 MI350系列 up to 288 GB HBM3E与8 TB/s peak theoretical bandwidth；这些是 SKU-level vendor specs，不是 application sustained。

MI350X与更高功率/液冷取向的 MI355X展示同一 architecture按 power/cooling envelope分 SKU。官方白皮书把 MI350X描述为适配既有 baseboard生态，并把 MI355X放入更高密度直接液冷系统。[Vendor Claim]

这条路线的关键问题：

- drop-in compatibility在 BIOS、power、thermal与 network上有多完整；
- ROCm新版本与低 precision能否达到相同质量；
- scale-up domain、NIC和 rack设计是否跟上 per-GPU compute；
- chiplet/package yield与供应；
- OEM/CSP availability和 acceptance。

## 7. 两条代际路线的共同规律

### Compute不再独立扩展

低 precision提高 matrix peak后，memory、KV、collective和 software coverage成为限制。Both platforms都增加 HBM和 interconnect，说明 datapath、memory与 fabric必须共同升级。

### Package成为 architecture

Blackwell用多 die unified GPU与 HBM；MI300/MI350延续 XCD/IOD/3D integration。Monolithic不再足以承载产品目标，good-package yield、D2D、power与 thermal成为竞争力。

### Rack成为采购单位

高功率 module需要 baseboard、busbar、liquid cooling、NIC/switch与 orchestration。客户不能只换 accelerator而忽略 facility。Generation cadence越快，datacenter construction与 qualification越可能拖慢部署。

### Software决定代际兑现

FP8/FP4/MX formats、new collectives、kernel tiling与 serving runtime必须达到 quality和 stability。早期 silicon benchmark容易混入新 software与旧 baseline差异；真正代际收益应在同版本重测并给各自最佳栈。

## 8. Worked performance waterfall

[Estimate] 某新一代 headline matrix peak为旧代2.5倍，HBM bandwidth为1.4倍，scale-up effective bandwidth为2倍。目标 workload时间分布：compute 45%、HBM 30%、communication 15%、runtime/other 10%。

理想分项加速后的归一化时间：

<code>T = 0.45/2.5 + 0.30/1.4 + 0.15/2 + 0.10 = 0.569</code>

理论端到端 speedup约1.76倍，而不是2.5倍。若低 precision只有70% operations适用、communication不能完全利用新 topology，结果更低。这个模型同时适用于两条产品线的 diligence，不是对具体 SKU的预测。

## 9. 为什么不按 FLOPS/美元排名

不同产品的 precision计数、sparsity、power、form factor、memory capacity和 software不同。采购还受：

- 模型能否 fit；
- tokens/quality/SLO；
- cluster规模与 network；
- rack power/cooling；
- availability与 delivery；
- migration与 engineering；
- reliability与 support；
- residual value和 cadence。

一个更贵但更快部署、软件成熟的系统可能 NPV更高；一个大 memory产品可能减少 sharding和 network；一个高 peak产品若受 power限制，facility内可装数量下降。

## 10. Baseboard compatibility的真实价值

保持 UBB/HGX类机械/电气平台可以复用 chassis、OEM设计、firmware与 qualification，缩短 time-to-market。但功率、cooling、cable和 BIOS变化可能让“drop-in”只在部分层成立。

要求列出 unchanged、compatible-with-update与 must-redesign：

| 层 | 检查 |
|---|---|
| Mechanical | module/board/chassis |
| Electrical | power rail/transient/connector |
| Thermal | air/liquid/cold plate |
| Firmware | BIOS/BMC/driver |
| Fabric | scale-up/NIC/cable |
| Software | compiler/library/framework |
| Operations | telemetry/spares/training |

兼容性是 deployment moat，也可能让旧边界限制新 architecture。

## 11. Product reality：benchmark contract

厂商 generation claims通常选择最受新 feature帮助的 model、precision与 software。正确比较至少有三组：

1. 同 software stack重测旧/新 hardware；
2. 各自最佳 production stack；
3. 客户真实 model/SLO/power与 cluster。

还要区分 MLPerf Available/Preview、vendor benchmark、internal estimate与 customer production。本文所有带倍数的厂商陈述都应保留 [Vendor Claim]，直到 comparison contract和独立复现明确。

## 12. Supply与 deployment

Hopper→Blackwell与 MI300→MI350都提高 HBM、package和 rack复杂度。即使 accelerator wafer充足，HBM3e、CoWoS类 packaging、substrate、liquid cooling、high-current power、NIC/switch与 datacenter energization可能限制 installed base。

产品 status的经济意义按这条链递减：

<code>Announced → Sampling → Production → Shipping → Customer accepted → Deployed → Utilized</code>

Revenue可能在 Shipping确认，客户价值要到 Utilized才发生。投资和竞争分析必须分别追踪。

## 13. Second-order effects

1. 更低 precision提高 compute，却把质量验证与 compiler变成 bottleneck。
2. 更大 HBM减少 model sharding，也可能鼓励更长 context扩大 KV。
3. 更大 scale-up domain减少 scale-out traffic，却集中 switch/power failure。
4. 多 die提高集成规模，却增加 package yield与 thermal。
5. 年度 cadence提高创新，也增加客户折旧和 qualification压力。
6. Rack platform整合提高 time-to-solution，也加深 vendor control。
7. Open software降低 lock-in的目标，需要用 migration labor与 production coverage验证。

## 14. Engineering → Strategy

| 代际方向 | 工程目的 | 新控制点 | 战略问题 |
|---|---|---|---|
| Lower precision | 更多 useful matrix work | compiler/quality | 谁控制格式与 recipes |
| More HBM | fit/reuse/bandwidth | memory/package | allocation与成本 |
| Multi-die | scale beyond reticle | D2D/yield | integration moat |
| Larger scale-up | 少慢速通信 | switch/cable | rack lock-in |
| Baseboard reuse | 快部署 | platform boundary | OEM ecosystem |
| Higher power | more throughput | facility/cooling | installed capacity |
| Faster cadence | workload跟进 | qualification | residual value |

## 15. Technical diligence questions

1. 旧 bottleneck是什么，新 feature对应哪一项？
2. Peak、sustained与 end-to-end waterfall？
3. Precision/quality和 software版本是否可比？
4. HBM capacity/bandwidth如何改变 sharding？
5. Scale-up domain对目标 parallelism的 exposed traffic影响？
6. Multi-die package的 yield、D2D与 thermal？
7. Baseboard compatibility在哪些层真实成立？
8. Rack power/cooling与 datacenter delivery？
9. Production/Shipping/Deployed分别有哪些证据？
10. Customer独立 benchmark与 migration labor？
11. Supply chain的最小 qualified capacity？
12. 下一代 cadence是否在当前代回收前到来？

## 16. Takeaways

1. 代际升级是 compute、memory、fabric、package、rack与 software的共同变化。
2. Hopper→Blackwell把 scale-up和 rack platform推到更大边界。
3. MI300→MI350延续 chiplet/3D与大 HBM，并扩展低精度和平台兼容。
4. Headline peak必须经过 workload waterfall与 deployment chain。
5. 最终竞争单位是 deployed、utilized、可维护的系统，而不是 datasheet GPU。

## Primary sources

- [Primary Source] [NVIDIA Hopper Architecture In-Depth](https://developer.nvidia.com/blog/?p=45555)
- [Primary Source] [NVIDIA Blackwell Tuning Guide](https://docs.nvidia.com/cuda/blackwell-tuning-guide/)
- [Primary Source] [NVIDIA CUDA Documentation](https://docs.nvidia.com/cuda/index.html)
- [Primary Source] [AMD CDNA Architecture](https://www.amd.com/en/technologies/cdna.html)
- [Primary Source] [AMD MI350 Series Product Page](https://www.amd.com/en/products/accelerators/instinct/mi350.html)
- [Primary Source] [AMD CDNA4 Architecture Whitepaper](https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/white-papers/amd-cdna-4-architecture-whitepaper.pdf)
- [Primary Source] [AMD Instinct Architecture Documentation](https://instinct.docs.amd.com/latest/gpu-arch/gpu-arch.html)
