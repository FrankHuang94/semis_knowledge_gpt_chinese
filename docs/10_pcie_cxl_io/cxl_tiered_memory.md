# CXL 与 Tiered Memory：容量池不会自动变成本地 HBM

## 1. 问题是 stranded capacity 与 placement

服务器常同时出现两种浪费：某些节点 memory闲置，另一些节点因 capacity不足而无法调度；accelerator又拥有昂贵但有限的 device memory。CXL提供 cache-coherent I/O与 memory语义，并通过 switching/pooling让 capacity更灵活，但任何远端层都具有不同 latency、bandwidth、failure与 ownership。

[Primary Source] CXL Consortium把 memory expansion/pooling列为规范用例；Linux CXL文档则展示 firmware、OS、decoder、NUMA、DAX、hotplug与 user policy的复杂交接。协议可建立可访问性，性能仍由 topology和 placement决定。

~~~mermaid
flowchart LR
  C[CPU/GPU] --> L[Local DRAM/HBM]
  C --> X[CXL Root/Switch]
  X --> M1[Memory Device A]
  X --> M2[Memory Device B]
  P[OS/Runtime Policy] -.placement.-> L
  P -.placement.-> M1
  P -.placement.-> M2
~~~

## 2. 三种价值主张要分开

- Expansion：一台 host获得更多 capacity；
- Pooling：capacity可在多个 hosts/devices之间分配，提高利用率；
- Tiering：hot data留在快层，cold data迁到慢/便宜层。

Expansion最容易理解；pooling增加 fabric manager、security和 failure domain；tiering依赖 workload locality和迁移策略。产品若只展示 capacity，不代表三者都 production-ready。

## 3. Whole-path performance

CXL memory latency包含 CPU/root、link、switch、device controller和 media。Bandwidth还受 shared upstream link、interleave、NUMA与并发 hosts。Linux文档使用 CDAT/HMAT等描述 latency/bandwidth属性，并计算 whole-path coordinates。[Primary Source]

因此不能写“CXL memory latency为某固定值”。必须在目标 topology下测 local/remote read/write、random/stream、queue load与 tail。

## 4. Placement粒度

OS可把 CXL capacity加入 page allocator、暴露 DAX供应用显式管理，或由 runtime做对象/tensor placement。自动 page migration兼容性高，但可能在 critical path触发 fault；显式 placement可预测，却需要应用知道 lifetime和reuse。

[Estimate] 若 hot set占20%、贡献80% accesses，把 hot pages留 local、cold pages放 CXL，平均 latency可能接近本地；若访问均匀，远端 tier会直接进入大部分请求。Page classification准确率比总 capacity更重要。

## 5. 为什么不把所有 memory pooled

共享 pool扩大 blast radius与 security边界；switch/fabric manager故障可能影响多个 hosts。Bandwidth也会被 noisy neighbor争用。对于 latency-critical state，本地 memory的可预测性更有价值。

Pooling还需要 allocation、scrub、ownership transfer与 isolation。释放给新 tenant前必须清除数据；device firmware、attestation与 key lifecycle进入 memory管理。

## 6. 为什么不把 HBM overflow直接放 CXL

GPU decode/attention频繁访问的 KV或 weights若跨较慢 fabric，会增加 token latency。CXL更适合 cold state、capacity spill、checkpoint staging或 CPU-centric workload，除非 accelerator与 system提供足够 coherent path且软件能分层。

应测每 byte被访问频率：一次性冷数据可以远置，反复 streaming的大 weight即使“只读”也可能压满 link。

## 7. Hotplug与 failure

Memory不是普通 peripheral。Linux CXL hotplug文档警告，未正确 teardown就硬拔 memory device可能导致 machine check或 SIGBUS。[Primary Source] Production系统必须先迁移/停止访问、拆 region、更新 allocator，再物理操作。

Failure语义包括 poison、media error、link reset、switch isolation和 partial capacity。Application是否 crash、retry或降级必须定义。

## 8. Worked economics

[Estimate] 集群一百台 hosts，每台本地 memory利用率平均55%，但因 peak需求按100配置。若共享 pool让本地配置降到75、另配总量1,500的 pooled capacity，总 installed从10,000降到9,000，节省10%。若 pool只达到50%有效利用或需20% spare，收益会缩小。

还要加 CXL switch/device、power、software、failure headroom与 performance loss。Capacity utilization提升不自动等于 TCO下降。

## 9. Second-order effects

1. Pooling提高利用率，却让 fabric成为 memory availability的一部分。
2. Tiering增加 capacity，也增加 page migration和 observability。
3. 更慢 memory可能让 CPU/GPU stalls扩大，节省硬件却增加运行时间。
4. Coherency简化共享，增加 protocol/state和 verification。
5. Hotplug提高 serviceability，但需要预留 address space和 orchestration。
6. Memory disaggregation扩大供应选择，也可能把 lock-in移到 fabric manager。

## 10. Diligence questions

1. Expansion、pooling还是 tiering的哪一项已交付？
2. Topology下 whole-path latency/bandwidth与 tail？
3. Placement由 OS、runtime还是 application，粒度多大？
4. Hot/cold识别错误代价？
5. Shared link oversubscription与 noisy neighbor？
6. Failure、poison、hot-remove和 recovery语义？
7. Security、scrub、attestation与 tenant ownership？
8. 节省的 local memory是否超过 switch/device/软件成本？
9. Target workload的远端 bytes比例？
10. Product status、OS/BIOS与 interoperability matrix？

## 11. Takeaways

1. CXL解决可访问性与资源组合，不取消 locality。
2. Expansion、pooling和 tiering是不同产品能力。
3. Whole-path topology与 placement决定性能。
4. Memory hotplug和 failure比普通 I/O更危险。
5. 价值来自可验证的 stranded-capacity减少，而不是池化容量本身。

## Primary sources

- [Primary Source] [CXL 2.0 Memory Pooling Overview](https://computeexpresslink.org/blog/compute-express-link-2-0-specification-now-available-2374/)
- [Primary Source] [Linux Kernel CXL Documentation](https://docs.kernel.org/driver-api/cxl/index.html)
- [Primary Source] [Linux CXL Hotplug](https://docs.kernel.org/driver-api/cxl/platform/device-hotplug.html)
- [Primary Source] [Linux CXL CDAT](https://docs.kernel.org/driver-api/cxl/platform/cdat.html)


## 基础概念桥接

先区分 PHY、link、transaction、I/O、cache coherence 和 memory semantics。协议支持不等于性能；lane width、payload efficiency、round-trip、switch、HDM placement、OS 与 driver 都会影响结果。pool、tier 和 local memory 也不是同义词。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。


## 进阶工程术语桥接

本篇进一步需要掌握：row buffer、refresh、controller、DMA、IOMMU、ATS、page migration、pooling 与 coherence。阅读这些术语时，不只记中英文对应，还要补齐系统位置、正常路径、饱和或失败路径、直接 counter、端到端结果、产品状态和证据等级。若工程会议出现“已解决”“无开销”“已量产”，应立即追问 workload、boundary、configuration、status/date、failure mode 与 falsifier。

延伸阅读：[进阶工程术语手册](../31_glossary/advanced_engineering_terms_handbook.md)。
