# Network 与 Optics Port-Count Model：从 Endpoint 到 Fiber、Spare 与 Power

## 1. 为什么 port count经常差一倍或一个数量级

“十万 accelerator需要十万 modules”通常缺少 topology和 boundary。一个 link有两个端点；一个 optical module可能承载一个或多个 links；breakout、AEC、CPO与 on-board optics改变 module边界；leaf-spine有多层 ports；spares和 failure isolation又增加数量。

正确顺序：

<code>Endpoints → Ports/endpoint → Links → Topology stages → Media choice → Modules/engines → Fibers/connectors → Spares</code>

~~~mermaid
flowchart LR
  E[Accelerator endpoints] --> P[Endpoint ports]
  P --> L[Leaf links]
  L --> S[Spine links]
  S --> M[Optical modules / CPO engines]
  M --> F[Fiber pairs / connectors]
  F --> R[Spares + maintenance]
~~~

## 2. 定义 counting boundary

至少说明：

- 数 endpoint-side、switch-side还是两端；
- physical ports、logical links或 lanes；
- duplex fiber pair还是单 fiber；
- pluggable module、AOC/AEC或 CPO engine；
- breakout后每端口多少 links；
- active、installed、warehouse spare；
- primary network、management还是 storage；
- normal还是 degraded topology。

很多“一倍错误”来自只数一端；“四倍错误”来自 breakout/parallel lanes；更大错误来自忽略 spine层。

## 3. Endpoint links

[Estimate] 100,000 accelerators，每个两个 scale-out ports，每个 module承载一个 link，链路两端都有 pluggable，基础 modules：

<code>100,000 × 2 × 2 = 400,000 modules</code>

若一个 module通过 breakout承载四个 endpoint links，switch端 modules可减少，但 endpoint端形态不一定相同。不能直接把总数除四，必须分别算两端。

## 4. Leaf-spine模型

设每个 leaf有 <code>D</code>个 downlinks和 <code>U</code>个 uplinks。Endpoint数 <code>N</code>：

<code>Leaf count = ceil(N / D)</code>

<code>Leaf uplinks = Leaf count × U</code>

若 spine每台提供 <code>S</code>个相关 ports：

<code>Spine count = ceil(Leaf uplinks / S)</code>

[Estimate] N=6,400，D=32，U=32，S=64，则200个 leaf、6,400条 leaf-spine links、100个 spine。端点层6,400 links加 spine层6,400 links，总 physical links为12,800；若两端 pluggable，则25,600 modules，再加 spare。

## 5. Oversubscription

Leaf下行/上行 payload比定义 oversubscription。1:1可支持特定 worst-case traffic，但不保证 arbitrary pair同时 line rate，因为 routing和 fabric仍有限。2:1减少 spine ports与 optics，却在 collective all-to-all下可能直接限制 completion。

应该用 workload traffic matrix模拟：data parallel ring、expert All-to-All、storage checkpoint、background flow。Average traffic低不代表 incast/collective peak可 oversubscribe。

## 6. Scale-up与 scale-out分开

Package/board/rack内 scale-up可能使用 copper、backplane或 proprietary links；rack外 scale-out使用 Ethernet/InfiniBand optics。若 rack-scale domain变大，scale-out endpoint数可能按 rack而非 GPU，但 rack出口 bandwidth需增加。

Generation比较时，“GPU数量相同”不能直接沿用 optics count。Topology从每 GPU NIC到 shared SuperNIC/rail或更大 scale-up domain会改变 ports、failure与 traffic。

## 7. Reach决定 media

短 reach可用 DAC；更长/更高速可能用 AEC或 optics。选择依赖 channel loss、cable diameter、bend、power、latency与 service。Optics还分 SR/DR/FR/LR等 reach与 fiber type；标准名称不能替代实际 path loss和 patch-panel数量。

[Primary Source] IEEE 802.3定义不同 Ethernet rates与 physical-layer objectives。标准合规说明 interface，不说明数据中心布线路径已满足 loss、cleanliness与 service。

## 8. Fiber与 connector数量

Duplex architecture通常每 link有发送/接收 fiber，parallel optics可能有更多 fibers，WDM可在单 fiber上传多 wavelengths。Module count与 fiber count不是固定比例。

需要数：

- trunk fibers；
- MPO/LC或其他 connectors；
- patch panels；
- cross-connect；
- slack/service loops；
- polarity；
- cleaning caps；
- spare fibers；
- test points。

Connector insertion loss和 contamination会进入 optical budget。更多 patch方便运维，却减少 margin。

## 9. Power与 thermal

[Estimate] 400,000 modules，平均每个15 W，则仅 modules为6 MW。[Estimate] 还不含 switch ASIC、NIC、fans和 cooling。即使每 module节省3 W，总计也节省1.2 MW，足以影响 facility；这解释 LPO/CPO的吸引力。

但 module平均 power应按 reach、rate、temperature和 traffic；CPO把部分 power移到 package/laser，不应从系统 boundary消失。

## 10. Spare模型

简单 spare fraction：

<code>Installed × (1 + spare_fraction)</code>

[Estimate] 25,600 installed modules、5% spare，需要26,880。现实 spare应按 failure rate、replacement lead time、site分布与 common-mode批次计算。总仓库有 spare不代表远端 site在 SLA内可获得。

Spare还包括 cable、laser、fan、switch line card与 cleaning/test equipment。CPO field replacement unit更大时，spare economics变化。

## 11. Reliability与 expected replacements

若 installed base为 <code>I</code>，annual failure rate <code>f</code>，平均 replacement cycle <code>t</code>年：

<code>Expected replacements = I × f × t</code>

再加 safety stock与 growth。Failure不是独立时，firmware、laser lot、connector contamination或 thermal设计会形成 correlated event。应保留 batch traceability。

## 12. Port utilization与 stranded capacity

部署中常有 reserved、cabled但 inactive、failed、maintenance与 topology stranded ports。Switch有足够总 ports，但某一 rail或 rack缺少可用端口，仍无法调度完整 parallel group。

需要按 location/rail而不是 aggregate统计。Spare port可提高恢复，却占用 ASIC/optics/power。调度器若能重映 topology，stranded比例下降，但 application performance可能降级。

## 13. Cost model

总成本包括：

- switch/NIC ports；
- modules/AEC/DAC；
- fiber/trunk/patch；
- installation与 testing；
- cleaning与 field labor；
- spares；
- module power/cooling；
- failure与 downtime；
- monitoring；
- technology transition inventory。

便宜 module若 failure高、功耗高或 vendor qualification慢，lifetime cost可能更高。CPO降低 pluggable数量，也可能提高 line-card replacement cost。

## 14. Why-not

### 为什么不只按 switch radix数

Radix不说明 down/up分配、breakout、spines、failure和 endpoint NIC。

### 为什么不把所有 link做 optics

短 copper更低成本/功耗且易维护；optics用于 electrical reach/density不经济的位置。

### 为什么不统一买最大 reach

Longer-reach optics可能更贵、更耗电；过度规格化也增加库存成本。标准化SKU与按需优化需平衡。

## 15. Engineering → Strategy

| Model输出 | 工程含义 | 商业含义 |
|---|---|---|
| Ports/endpoints | NIC与topology | attach rate |
| Leaf/spine links | radix/oversub | switch TAM |
| Module count | media/breakout | optics demand |
| Fiber/connector | physical plant | installation |
| Power | rack/facility | Opex/CPO价值 |
| Spares | reliability | recurring demand |
| Transition | compatibility | inventory risk |

## 16. Technical diligence questions

1. Counting boundary与 topology图？
2. Ports/endpoint、link两端与 breakout？
3. Leaf/spine radix和 oversubscription？
4. Normal/degraded traffic matrix？
5. Reach与 media selection？
6. Module、fiber、connector和 patch数量？
7. Power按完整系统 boundary？
8. Failure、replacement lead time和 site spares？
9. Rail/location stranded ports？
10. 新一代 scale-up如何改变 scale-out count？

## 17. Takeaways

1. Port count必须从 endpoint和 topology逐层推导。
2. Link两端、breakout和 spine是最常见误差源。
3. Optics需求同时由 reach、topology、power和 failure决定。
4. Spare应按 site、lead time与 correlated risk，而非统一百分比。
5. Port-count model连接 network architecture、optics TAM、facility power和 service成本。

## Primary sources

- [Primary Source] [IEEE 802.3 Ethernet Working Group](https://www.ieee802.org/3/index.html)
- [Primary Source] [IEEE P802.3df public materials](https://www.ieee802.org/3/df/public/22_07/index.html)
- [Primary Source] [OIF Implementation Agreements](https://www.oiforum.com/technical-work/implementation-agreements-ias/)
