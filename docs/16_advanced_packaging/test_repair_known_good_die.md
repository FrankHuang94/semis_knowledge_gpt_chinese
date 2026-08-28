# Test、Repair 与 Known-Good Die：先进封装的隐藏架构

多颗高价值 die 被组装进同一 package 后，缺陷的经济损失不再等于一颗小 die。先进封装 test strategy 的任务是在最便宜、最可访问的阶段尽早发现缺陷，同时避免测试本身损伤器件或把良品误判为坏品。test、repair 和 redundancy 因而是产品架构，不只是制造收尾。

## Yield waterfall

\[
Y_{\text{package}}=\prod_i Y_{\text{component},i}\times Y_{\text{assembly}}\times Y_{\text{final test}}
\]

[Estimate] 独立相乘只是第一阶模型；实际缺陷可能相关，测试覆盖也不完美。随着 die 数增加，即使单颗良率很高，package good rate 仍会下降。

~~~mermaid
flowchart LR
  W[Wafer probe] --> K[Known-good die]
  K --> A[Assembly]
  A --> I[In-process test]
  I --> F[Final test]
  F --> S[System test / burn-in]
  I -.repair.-> A
  F -.binning.-> P[Product SKUs]
~~~

## 测试边界

wafer probe 能在组装前筛选 logic 和 memory，却受到 pad 可访问、probe pitch、温度和 test time 限制；in-process test 可定位 bonding 或 interconnect 问题，但临时访问结构增加设计复杂度；final test 覆盖完整 package，却在失败时已经投入大部分价值；system test 最接近真实 workload，但诊断分辨率低且昂贵。

为什么不在每一步做完整测试？测试时间会直接占用设备并扩大 cycle time，重复高温应力也可能影响寿命。chosen design 根据 defect escape cost、测试可访问性和工序价值增长安排 coverage。

## Repair 与 redundancy

HBM、chiplet link、cache 或 compute array 可预留 spare rows、lanes 或 units，通过 fuse、firmware 或 binning 绕过局部缺陷。这提高 usable yield，却增加面积、验证状态和库存分层。若 repair 只能在封装前执行，assembly-induced defect 无法挽回；若现场可重配置，可靠性提高，但安全、诊断和软件支持更复杂。

Known-good die 也不是绝对“good”。它只表示通过既定 coverage 和条件；latent defect、不同封装应力与高速接口组合问题仍可能在后续出现。因此 supplier agreement 必须定义测试条件、guardband、责任边界和 escape 处理。

## Economics 与 new bottleneck

提升前段筛选后，assembly tool 或 final tester 可能成为瓶颈；增加 burn-in 降低 field return，却提高资本和能耗；更细 binning 提高回收率，却增加 SKU、库存和客户 qualification。应优化每月 good qualified systems 和 lifetime cost，而非单站 test yield。

## Diligence checklist

- test vehicle 与目标产品在尺寸、材料和接口上有多接近？
- 每一阶段能看到哪些 nets、die 和 failure mode？
- false fail、escape、retest 与 correlation 数据如何？
- repair 覆盖多少缺陷，何时执行，是否影响性能？
- tester、probe card、socket 与 burn-in capacity 是否匹配 ramp？
- field return 能否追溯到 wafer、assembly lot 与 test history？

## 资料

- [IEEE 1838 Standard for 3D Stacked IC Test Access](https://standards.ieee.org/ieee/1838/6846/) [Primary Source]
- [JEDEC Standards and Documents](https://www.jedec.org/standards-documents) [Primary Source]
- [imec Advanced Packaging](https://www.imec-int.com/en/what-we-offer/research-portfolio/advanced-packaging) [Independent]


## 基础概念桥接

先区分 substrate、interposer、RDL、bump、hybrid bond、die attach、underfill、warpage 和 test。封装不是被动外壳，而是电源、信号、热、机械和良率架构。known-good die 也只表示通过既定测试覆盖。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。
