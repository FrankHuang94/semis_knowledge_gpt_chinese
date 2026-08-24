# 如何使用这套知识库

这不是按目录从头读到尾的教材。推荐采用 spiral learning：第一次建立 intuition；第二次补 architecture；第三次补 quantitative analysis；第四次补 real product；第五次把工程结论翻译为 strategy。

## 每次阅读的四步

1. 先画 system boundary：研究的是 die、package、board、rack 还是 cluster？
2. Follow the Data：输入、state、intermediate result 和 control 分别怎么走？
3. 找 limiting resource：compute、capacity、bandwidth、latency、power、thermal、routing、yield 还是 software？
4. 做反事实：为什么不能用更简单的办法？解决后下一个 bottleneck 在哪里？

## 不需要一次补完所有基础

遇到 setup/hold、impedance、row buffer 等陌生概念时，只补到能够解释当前 architecture choice 的程度。后续再次遇到时逐层加深。

## 建议起点

- 建立全栈地图：[现代 AI 数据中心](../20_rack_cluster_datacenter/modern_ai_datacenter.md)
- 建立数据移动直觉：[Follow the Data](follow_the_data.md)
- 建立约束思维：[Bottleneck Map](follow_the_bottleneck.md)
- 为会议做准备：[如何读架构演讲](../29_hot_chips/how_to_read_architecture_presentation.md)
