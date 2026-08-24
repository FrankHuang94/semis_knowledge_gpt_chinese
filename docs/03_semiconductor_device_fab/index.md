# Semiconductor Device, Fab & Yield

本模块把 architecture 连接到可制造性。重点不是背工艺步骤，而是判断一个设计如何变成 qualified good output。

## 核心文章

- [从 Transistor 到 Good Package：Fab、Yield 与量产爬坡](from_transistor_to_good_package.md)：FEOL/MOL/BEOL、lithography、process interaction、yield chain、cycle time、known-good-die、chiplet economics 与 capacity qualification。
- [数字逻辑、时钟与功耗](../02_engineering_foundations/digital_logic_clock_power.md)：device 与 wire 如何限制 timing 和 power。
- [Advanced Packaging](../16_advanced_packaging/advanced_packaging.md)：interposer、RDL、substrate、assembly 与 test。
- [Manufacturing & Supply Chain](../22_manufacturing_supply_chain/manufacturing_supply_chain.md)：把 fab/package/test 约束翻译成供应风险。

## 学完以后应该能回答

- 为什么 node 名称不能直接预测 product PPA、cost 或 yield？
- Die yield、binning yield、assembly yield、final-test yield 有什么区别？
- Chiplet 为什么可能改善可筛选性，却增加 package/test 风险？
- Installed capacity、qualified capacity 与 good output 为什么不能互换？
- 制造 learning rate 为什么可能比某个时点的 nominal yield 更重要？


## 深化阅读

- [Process Control、Cycle Time 与 Learning Rate](process_control_cycle_time_learning.md)
