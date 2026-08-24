# Switch / NIC / DPU

本模块追踪 packet 从 fiber/electrical link 穿过 switch pipeline、NIC queues 与 PCIe DMA，最终进入 host 或 GPU memory。

## 核心文章

- [Switch、NIC 与 DPU：Packet、DMA、Offload 与 Infrastructure Isolation](switch_nic_dpu.md)

## 学习结果

完成后应能区分 switch、NIC、SmartNIC 与 DPU；画出 fast/slow path；解释 DMA、RDMA、offload、queue 与 trust boundary；并用 CPU savings、tail、power、software lifecycle 与 failure domain评价产品。
