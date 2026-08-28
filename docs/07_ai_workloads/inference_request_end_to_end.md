# 一个 Production Inference Request 的完整旅程：从 Arrival 到最后一个 Token

## 1. 请求延迟不等于 GPU kernel时间

生产 LLM inference从 load balancer收到请求开始，经过 authentication、tokenization、routing、queue、prefill、KV allocation、iterative decode、detokenization与 streaming。模型可能跨多个 devices或 hosts，任何 queue、collective、memory pressure与 retry都会进入用户感知延迟。

服务目标通常包含 TTFT、inter-token latency、end-to-end latency、tail percentile、SLO-compliant throughput与 cost/token。只报 tokens/s会把排队、首 token和失败排除。

~~~mermaid
sequenceDiagram
  participant U as Client
  participant F as Frontend/Scheduler
  participant P as Prefill Workers
  participant D as Decode Workers
  participant K as KV Manager
  U->>F: request + prompt
  F->>F: auth/tokenize/admission
  F->>P: scheduled prompt
  P->>K: allocate/write KV
  P-->>U: first token
  loop each next token
    F->>D: iteration batch
    D->>K: read/update KV
    D-->>U: streamed token
  end
~~~

## 2. Frontend 与 admission control

请求首先经历 TLS/API、quota、content policy、tokenization与 model routing。Prompt长度、期望 output、priority与 cache状态决定资源需求。Admission control若只看当前 queue而忽略未来 KV增长，可能在中途耗尽 memory。

Scheduler需要决定接受、等待、拒绝或降级；还要防止长 prompt/长 generation拖累短请求。公平、utilization与 revenue priority之间没有免费答案。生产指标应分离 frontend time、queue time与 engine time。

## 3. Tokenization 与 request shape

Tokenizer把文本变成 token IDs。不同语言和内容具有不同 tokens/character，导致相同字符长度产生不同 compute与 KV需求。Chat template、system prompt、tool schema与 retrieved context也属于真实 input。

Prompt distribution比单一 maximum sequence更重要。Benchmark若全用相同长度，无法代表 fragmentation、batch mixing与 tail。应记录 input/output token的 joint distribution、arrival process与 cancellation。

## 4. Prefill：并行处理 prompt

Prefill一次处理多个 prompt tokens，构建每层 KV cache。大矩阵和 attention提供较高并行度，常更偏 compute-bound；长 context又会增加 attention与 memory。TTFT包括 queue、prefill计算与第一个 decode token，不应把 queue移除后仍称用户 TTFT。

Batching多个 prompts可提高 accelerator利用率，却让早到请求等待 batch形成。Chunked prefill把长 prompt切片，与 decode交错，改善 fairness但增加 scheduler与 KV管理复杂度。

## 5. KV allocation：容量是动态承诺

每个 request的 KV随已处理 tokens增长。Allocator需要 page/block、free list、prefix sharing、eviction或 offload。连续预留 maximum context会造成内部碎片；paged allocation减少浪费，却增加 metadata、indirection与可能的 fragmentation。

[Primary Source] vLLM文档描述 PagedAttention把每个 request的 KV分为 blocks，以更灵活管理非连续 cache。这个机制说明 serving software可以改变可用 capacity，但不能取消每 token KV bytes与 HBM bandwidth。

Prefix cache可复用 system prompt或共同前缀，降低 prefill；cache key必须包含 model、tokenization、adapter、position和 relevant settings，避免错误复用。命中率依赖真实 traffic，不应按演示场景外推。

## 6. Decode：每一步都要重新调度

Decode每次为每个 active request生成一个或少数 tokens，读取 weights与历史 KV，再采样下一个 token。单 request矩阵较小，batch reuse对 weight bandwidth很重要。Continuous batching在每个 iteration加入新请求、移除完成/取消请求，提高利用率。

代价是 batch shape不断变化，长尾请求持有 KV，prefill与 decode争用 compute/memory。Scheduler优化平均 throughput可能伤害 inter-token tail；优先 decode可稳定 streaming，却让新请求 TTFT上升。

## 7. Worked latency waterfall

[Estimate] 某请求 frontend/tokenization 8 ms、queue 22 ms、prefill 70 ms、第一个 decode iteration 10 ms，因此：

<code>TTFT = 8 + 22 + 70 + 10 = 110 ms</code>

之后生成80个 tokens，平均 iteration 12 ms，但每二十个 token有一次25 ms scheduler/collective tail。[Estimate] 额外 tail共100 ms，decode总时间约：

<code>80 × 12 + 100 = 1,060 ms</code>

End-to-end约1.17秒。把 prefill加速一倍只节省35 ms；改善 decode tail或 queue可能更有用户价值。必须按 request length与 percentile做 sensitivity。

## 8. Disaggregated prefill/decode

把 prefill与 decode放到不同 worker pools可分别优化 compute-heavy与 memory/latency-heavy资源，并独立扩容。代价是 KV必须跨 fabric传输或由共享 memory访问，增加 handoff latency、bandwidth、一致性与 failure。

当 prompt长、output短时，prefill pool更忙；chat式短 prompt、长 output则 decode占主导。静态资源比例会在 traffic变化时失衡，scheduler需要 capacity forecasting与 backpressure。

## 9. Model parallel与 communication

模型放不进单 device时使用 tensor/pipeline/expert parallel。每个 decode iteration中的 collective latency可能直接进入 inter-token latency；小 message与同步使 network tail尤其重要。Pipeline可以增加并发，却让单 token跨 stages。

Replica/data parallel提高 request throughput，但每个 replica需要 weights和 cache capacity。选择是在单 replica规模、replica数量、batch reuse与 failure domain之间优化。

## 10. Sampling与输出也在 timed path

Logits processing、temperature/top-k/top-p、grammar约束、speculative verification、detokenization与 streaming serialization都会增加 latency。大 vocabulary与复杂 structured output可能让“非模型”部分显著。

Speculative decoding用较小 draft model提出多个 tokens，再由 target model验证，以额外 compute换更少串行 target iterations。收益依赖 acceptance rate、draft cost、batch与 memory；低 acceptance可能更慢。

## 11. Cancellation、timeout 与 retry

用户断开后，系统应尽快停止 future iterations并回收 KV；否则幽灵请求继续消耗资源。Timeout策略需区分 queue、TTFT、idle stream与 total duration。

Retry可能跨 replica重新做 prefill，扩大 load并形成 retry storm。Engine failure时能否迁移 KV、从 prefix恢复或只能重算，决定可用性成本。Exactly-once streaming很难，API需要定义 partial output与 billing semantics。

## 12. Queueing为何在高利用率时爆炸

接近饱和时，小小的 service-time variation会形成长队。更高 batch可提高 service rate，却延长等待形成批次；优先级可以保护重要请求，却让低优先级饥饿。SLO-compliant throughput是在 tail约束下找到稳定 arrival rate，不是把离线 batch塞满。

[Primary Source] MLPerf Inference规则区分 Server/Interactive与 Offline等 scenario；Server使用随机到达并受 tail latency约束，Offline更接近一次性吞吐。这说明同一硬件的“性能”取决于 arrival与 latency contract。

## 13. 为什么不永远扩大 batch

Batch提高 weight reuse与 compute效率，但占用更多 KV/workspace，增加排队和 iteration跨度。Mixed sequence lengths导致 padding或不同请求完成时间。高 batch还会让一个 slow collective或 long request影响更多用户。

Scheduler应根据 SLO、memory headroom与 traffic动态选择，而不是追求单一最大 throughput点。

## 14. 为什么不把所有 KV offload到 host

Host DRAM容量大、成本较低，但访问需要 PCIe/CXL/fabric，decode每步频繁读取会增加 latency与 bandwidth压力。Selective offload可以保存低优先级或暂停 request，但需要预测 reuse与迁移时间。若在关键 token前 page-in，tail可能恶化。

Compression或低 precision KV减少 capacity和 bytes，却需要 accuracy验证、decode compute与 format支持。任何容量方案都要同时测质量和 inter-token tail。

## 15. Observability 的最小分解

每个 request至少记录：

- arrival、admission、queue start/end；
- tokenize、prefill start/end、first token；
- 每个 decode iteration或聚合 distribution；
- input/output tokens、batch size、KV blocks；
- model/adapter/software/precision版本；
- worker、parallel group与 network path；
- cancellation、preemption、retry与 error；
- power/cost归属。

只记录 end-to-end无法区分是 frontend、scheduler、compute、memory还是 network。只记录 engine则无法解释用户体验。

## 16. Second-order effects

1. 更强 continuous batching提高 throughput，却可能伤害 TTFT或 inter-token tail。
2. Prefix cache减少 prefill，但占用 memory并增加 invalidation/security风险。
3. KV paging提高 capacity利用率，却增加 metadata和 indirection。
4. Prefill/decode分离允许独立扩容，却制造 KV transport。
5. Quantization减少 weight bytes，却可能让 KV或 network成为新瓶颈。
6. Speculative decoding减少串行步数，却增加 draft与 verification work。
7. 更高利用率改善 cost/token，却让 queue对故障和 burst更敏感。

## 17. Engineers actually say

- “We serve one千 tokens/s.”：问 input/output、batch、TTFT、ITL与 percentile。
- “KV cache is paged.”：问 block size、fragmentation、eviction与 metadata。
- “Continuous batching keeps GPU full.”：问 queue与每类 SLO。
- “Prefill is disaggregated.”：问 KV handoff bytes、latency与 failure。
- “Prefix cache hit很高.”：问 traffic mix、tenant isolation与 cache key。
- “We can offload long context.”：问 page-in tail与 fabric contention。
- “The engine is faster.”：问是否包含 tokenization、network与 streaming。

## 18. Engineering → Strategy

| Serving层 | 约束 | 优化 | 价值控制点 |
|---|---|---|---|
| Frontend | auth/tokenization | caching/scale | API platform |
| Scheduler | queue/fairness | continuous batching | serving software |
| Prefill | compute/context | fusion/chunking | accelerator/kernel |
| KV | capacity/bandwidth | paging/quantization | HBM/runtime |
| Decode | serial latency | batching/speculation | memory+software |
| Fabric | collectives/KV handoff | topology | NIC/switch |
| Reliability | retry/recovery | replicas/checkpoint | cloud operations |

## 19. Technical diligence questions

1. Arrival、input/output token与 cancellation distributions是什么？
2. TTFT、inter-token与 end-to-end p50/p95/p99如何分解？
3. SLO-compliant throughput而非 offline peak是多少？
4. KV bytes/request、fragmentation、reserve与 eviction策略？
5. Prefill/decode batch policy和资源比例如何动态调整？
6. Parallelism collective是否进入每个 token critical path？
7. Prefix/speculative/quantization在相同质量下的真实命中或接受率？
8. Cancellation、worker failure与 retry如何回收/恢复 state？
9. Software升级、model adapter与 cache compatibility？
10. Cost/token是否包含 idle headroom、frontend、network和 failures？

## 20. Takeaways

1. Production inference是 arrival、queue、prefill、KV、decode与 streaming的完整路径。
2. TTFT、inter-token、tail与 cost/token必须同时优化。
3. KV cache是动态容量承诺，也是 decode bandwidth负担。
4. 提高 batch/utilization会与 queueing和 tail交换。
5. Serving software决定同一 silicon能否转成 SLO-compliant useful work。

## Primary sources

- [Primary Source] [vLLM Documentation](https://docs.vllm.ai/)
- [Primary Source] [vLLM PagedAttention documentation PDF](https://docs.vllm.ai/_/downloads/en/v0.5.3/pdf/)
- [Primary Source] [MLCommons Inference Policies](https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc)
- [Primary Source] [MLCommons Inference Reference Suite](https://github.com/mlcommons/inference)


## 基础概念桥接

先把训练、prefill、decode、embedding、recommendation 与 multimodal 拆成不同 phase。明确 weights、activations、gradients、optimizer state、KV cache 的生命周期，再写 batch、sequence、precision、arrival distribution 和 SLO。模型名称本身不是硬件需求。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。


## 进阶工程术语桥接

本篇进一步需要掌握：微操作、流水线冒险、并行度、shape、动态批处理、尾延迟、数量级与单位经济性。阅读这些术语时，不只记中英文对应，还要补齐系统位置、正常路径、饱和或失败路径、直接 counter、端到端结果、产品状态和证据等级。若工程会议出现“已解决”“无开销”“已量产”，应立即追问 workload、boundary、configuration、status/date、failure mode 与 falsifier。

延伸阅读：[进阶工程术语手册](../31_glossary/advanced_engineering_terms_handbook.md)。
