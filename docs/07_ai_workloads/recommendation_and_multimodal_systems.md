# Recommendation 与 Multimodal Systems：为什么“也是 AI”却不是同一台机器

LLM 让矩阵乘法与 KV cache 成为主叙事，但推荐系统和多模态流水线会把随机 embedding 访问、特征处理、解码、数据搬运与在线排序重新带回中心。用同一个 accelerator utilization 指标评价所有 AI workload，容易把系统结构看错。

## 推荐请求的数据路径

传统深度推荐把 dense features 送入 MLP，把 categorical IDs 送入大规模 embedding tables，再做 feature interaction 与 ranking。它同时含有两种相反的访问模式：MLP 规则、计算密集；embedding lookup 稀疏、随机且对容量敏感。

~~~mermaid
flowchart LR
  R[Request] --> F[Feature service]
  F --> I[ID / sparse features]
  F --> D[Dense features]
  I --> E[Embedding lookup]
  D --> M[Bottom MLP]
  E --> X[Feature interaction]
  M --> X
  X --> T[Top MLP / Ranking]
  T --> P[Policy / Auction]
~~~

[Primary Source] Meta 的 DLRM 实现明确区分 dense 向量与 sparse indices，并把 embedding vectors 与 MLP 结果送入交互算子。这意味着容量规划不能只问模型参数量，还要问热行比例、reuse distribution、table sharding、cache 命中、特征新鲜度和跨节点 all-to-all。

## 为什么不把 embedding 全放进加速器

全放 HBM 可获得较低延迟，但大表可能挤占计算模型与 activation 空间；把冷表放 DRAM 或 SSD 可扩容量，却增加访问层级和尾延迟。复制热门表降低远程访问，代价是更新广播与一致性；按表切分容易实现，却可能形成热点；按行切分更均衡，却增加请求 fan-out。

一个可用的容量模型是：

\[
C_{\text{effective}}=\frac{C_{\text{raw}}-C_{\text{runtime}}-C_{\text{activations}}}{1+\rho_{\text{replica}}+\rho_{\text{fragment}}}
\]

[Estimate] 分母中的复制与碎片并非小数点后的细节；当 table placement 不均衡时，最满设备而非平均设备决定扩容时间。

## 多模态不是一个 kernel

图文、视频或语音请求通常经历 CPU 解码、resize/tokenize、encoder、cross-modal projection、LLM prefill、decode 与后处理。不同阶段需要不同资源，且通过 queue 串联。若图像 decoder 在 CPU 上形成排队，即使 GPU kernel 很快，用户仍看不到改善。

~~~mermaid
flowchart LR
  B[Bytes] --> C[Decode / preprocess]
  C --> V[Vision or audio encoder]
  V --> Q[Projection / fusion]
  Q --> L[Language model]
  L --> O[Postprocess]
  subgraph 共享瓶颈
    N[Network] --- S[Storage]
    S --- H[Host memory]
  end
~~~

多模态还改变 batching。相同 token 数的请求可能有不同图像分辨率、帧数或音频长度；padding 浪费、动态 shape 编译和 encoder/decoder 资源争用都会扩大 tail latency。最优 batch 不再是单变量，而是 modality、shape、SLO 与 cache locality 的组合。

## Alternatives 与 chosen design

- **统一大型 accelerator pool**：调度简单、软件一致，但预处理和 embedding 可能浪费昂贵 HBM 与矩阵单元。
- **CPU + accelerator 分层**：让 CPU 处理控制密集与容量型工作，让 accelerator 处理规则张量；边界清楚，但 PCIe 和 host-device copy 可能成为瓶颈。
- **异构服务拆分**：各阶段独立扩缩容，故障隔离更好；代价是网络 hop、版本协调和 backpressure。
- **近内存或专用推荐芯片**：可提高 embedding 效率，但生态、模型演进与利用率风险更高。

常见 chosen design 是按阶段解耦、共享特征缓存，并让调度器依据 shape 和 SLO 路由；选择理由是可独立扩容，而不是某个芯片在单一 benchmark 上最快。

## 新瓶颈与战略含义

当 embedding cache 提高后，特征服务的新鲜度和网络 fan-out 会浮现；当 encoder 加速后，LLM decode 或内容安全过滤成为关键路径；当模型吞吐上升后，线上实验、日志与 feature pipeline 的成本跟着增长。推荐系统还受业务反馈环影响：延迟改变候选数量，候选数量改变质量，质量又改变请求和数据分布。

产品 diligence 因此要按完整 request trace 比较：召回、排序、后处理的资源占比；P50 与 P99；特征缺失和 cold-start；模型质量约束；每千次有效决策成本。只报告 accelerator QPS 会遗漏最贵的系统边界。

## 资料

- [Meta DLRM reference implementation](https://github.com/facebookresearch/dlrm) [Primary Source]
- [TorchRec documentation](https://pytorch.org/torchrec/) [Primary Source]
- [MLPerf Inference repository](https://github.com/mlcommons/inference) [Independent]
