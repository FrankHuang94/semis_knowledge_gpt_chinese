# Rack / Cluster / Datacenter

本模块把 accelerator 放回真实运行环境：compute、memory、network、power、cooling、firmware、facility 与 operations 共同决定 useful work。

## 核心文章

- [AI Rack Power 与 Cooling Capacity Planning](power_cooling_capacity_planning.md)
- [一个现代 AI 数据中心到底是怎么工作的？](modern_ai_datacenter.md)
- [Modern AI Rack：为什么机柜已经成为计算机](modern_ai_rack.md)

## 学习结果

完成后应能：

- 画出 token 从 rack 内 scale-up 到 cluster scale-out 的数据路径；
- 追踪 facility power 到 transistor，再追踪 heat 回到 facility water；
- 识别 busbar、power shelf、cold plate、manifold、CDU 与 control plane；
- 区分 rack、network、cooling 与 software failure domains；
- 用 availability-adjusted compute 而不是 nameplate specs 评价系统；
- 把 installation、commissioning、service 与 spares 纳入 TCO。
