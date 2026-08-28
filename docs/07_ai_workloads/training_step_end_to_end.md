# 一个 Distributed Training Step 的完整旅程：从 Batch 到同步更新

## 1. Training step不是一次矩阵乘法

一个同步 distributed training step从数据准备开始，经过 forward、loss、backward、gradient communication、optimizer update与可能的 checkpoint/metrics。任一 rank迟到，barrier或 collective会把局部抖动放大为全局 step time。

目标不是让每颗 accelerator始终忙，而是在达到相同模型质量的前提下，最小化 time-to-quality、成本与失败风险。更快 step若需要更大 global batch并损害 convergence，不能直接视为更快训练。

~~~mermaid
sequenceDiagram
  participant D as Data Pipeline
  participant G as GPU Rank
  participant N as Fabric
  participant O as Optimizer
  D->>G: batch / tokens
  G->>G: forward + save activations
  G->>G: loss
  G->>G: backward gradients
  G->>N: reduce / shard collectives
  N-->>G: synchronized gradients/state
  G->>O: optimizer update
  O-->>G: new weights
~~~

## 2. Step开始前：数据必须准时到达

Dataset读取、shuffle、tokenization、augmentation、packing与 host-to-device transfer构成 input pipeline。若 accelerator在等待下一批数据，compute优化毫无意义。需要观察 prefetch queue、CPU utilization、storage throughput、network filesystem与 page-locked buffers。

数据随机性和样本顺序也是 correctness的一部分。为提高 packing efficiency改变 sequence组合，可能改变训练分布；丢弃难处理样本或重复 cache数据会让 benchmark失真。

## 3. Forward：产生输出，也产生未来的 memory负担

每一层读取 weights与 input activations，执行 GEMM/attention/normalization等，再生成下一层 activation。Training还要保留 backward所需的中间 state。Activation memory随 microbatch、sequence、hidden size与保存策略变化。

Checkpointing/recomputation可以少存 activations，在 backward时重新计算，以 compute换 capacity。它能让更大模型或 batch放入 memory，却增加 step operations，并可能缩短 communication overlap窗口。是否划算取决于当前是 capacity、compute还是 communication-bound。

## 4. Loss 与 numerical state

Loss reduction、scaling与 mixed precision决定 gradient的数值行为。低 precision加速 datapath并减少 bytes，但 accumulation、master weights、loss scaling与 optimizer state可能使用更高 precision。Overflow/underflow detection有时触发跳过 update，吞吐仍高却没有有效学习。

训练系统必须同时记录 step time与 effective samples/tokens、skipped steps、loss curve、validation quality。只测 kernel不能证明 time-to-quality。

## 5. Backward：反向依赖与 bucket ready order

Autograd从 loss沿 graph反向计算 activation与 weight gradients。后层 gradient先 ready，前层后 ready。Data parallel可以在某个 gradient bucket完成后立刻发起 All-Reduce，与其余 backward overlap。

[Primary Source] PyTorch DDP design note说明 reducer通过 autograd hooks标记 gradients并按 bucket触发 asynchronous all-reduce，最终等待所有 reductions完成。Bucket太大，通信启动晚；太小，launch/latency overhead增加。参数注册顺序、graph break与 unused parameters都可能影响 overlap。

## 6. Parallelism如何改变 traffic

### Data Parallel

每个 rank有模型 replica与不同 batch，gradient需要 reduction。实现简单、compute scaling好，但参数/optimizer state复制占 memory，global batch随 ranks增加。

### Tensor Parallel

矩阵按维度切分，层内需要 All-Reduce、All-Gather或 Reduce-Scatter。它让单模型跨 devices，却在每层引入 latency-sensitive communication。

### Pipeline Parallel

层分 stage，microbatches流过 pipeline。减少单 device memory，但产生 bubble、stage imbalance与 activation point-to-point traffic。

### Expert Parallel

MoE tokens通过 All-to-All路由。平均 expert load相等不代表每 step平衡；hot expert与 network contention影响 tail。

现实系统组合多种 parallelism。选择要最小化 critical-path traffic，而不是最大化某一种理论 efficiency。

## 7. Worked timeline

[Estimate] 一个 step包含 forward 90 ms、backward 150 ms、gradient communication 80 ms、optimizer 30 ms。若 communication中有60 ms可与 backward overlap，exposed communication只有20 ms：

<code>T_step = 90 + 150 + 20 + 30 = 290 ms</code>

若 kernel优化把 backward降到100 ms，但可 overlap窗口也降到40 ms，exposed communication变40 ms：

<code>T_new = 90 + 100 + 40 + 30 = 260 ms</code>

Backward本身快了三分之一，step只快约10%。[Estimate] Bottleneck移向 fabric。下一项投资可能是 gradient sharding、topology或 collective，而不是继续加 compute。

## 8. Optimizer step与 state

Optimizer读取 weights、gradients和一阶/二阶 moments，执行 update并写回。Adam类方法的 state容量可能显著超过 weights本身；sharding把 optimizer state、gradients或 parameters分散到 ranks，减少单 rank memory，但增加 gather/scatter与 failure coordination。

[Primary Source] PyTorch FSDP文档区分 replicated与 sharded parameters/gradients/optimizer state。Sharding stage不是数字越高越好：通信频率、prefetch、CPU offload、checkpoint format与 recovery complexity都会变化。

## 9. Gradient accumulation

多个 microsteps累积 gradient后再同步更新，可以减少 collective频率并增大 effective batch。它也延长一次 update的时间、增加 activation/accumulation state，并改变 optimization semantics。若使用 DDP，通常只在 accumulation周期最后一次 backward做 global reduction。

要区分 microstep throughput与 optimizer-step throughput，更要区分 samples-to-quality。把 accumulation加大可以让 network图变漂亮，却可能需要重新调 learning rate与 schedule。

## 10. Straggler 从哪里来

- 输入样本长度不同，padding/packing不均；
- MoE expert load偏斜；
- GPU clock/thermal或 error recovery；
- network congestion、retransmission或 routing；
- Python/host scheduler抖动；
- memory allocator、page fault或 background job；
- checkpoint、logging与 filesystem；
- 某 rank kernel compilation/cache miss。

同步训练的 step时间接近最慢 rank。平均 device utilization掩盖 tail，必须收集 per-rank timeline与 collective wait。

## 11. Failure与 checkpoint属于 step economics

大集群运行越久，device、link、switch、host与 software failure越不可忽略。Checkpoint过频消耗 I/O与 step时间，过疏则失败后重算更多。Checkpoint还要保存 model、optimizer、scheduler、random state与 data position，才能实现语义正确恢复。

Sharded checkpoint可以并行写入，却需要 metadata与一致性；异步 checkpoint减少暂停，但必须保证 snapshot对应同一 logical step。恢复速度、坏 rank替换与 topology remap都会影响 delivered training throughput。

## 12. 为什么不把 batch无限增大

更大 batch提高 GEMM效率、减少相对通信与增加 data reuse，但可能降低 gradient noise并改变 convergence；最终需要更多 epochs/tokens或精细 learning-rate调整。Memory与 pipeline latency也会上升。

系统 benchmark应在相同 target quality下比较，不应通过扩大 batch把硬件喂满却改变训练任务。

## 13. 为什么不把所有 communication隐藏

Overlap要求 computation与 communication使用不同可并行资源，并且 gradient及时 ready。两者可能竞争 HBM、L2、copy engines、PCIe或 power。过度并发会让各自变慢；短 layer和小 bucket的 launch overhead也可能主导。

“完全 overlap”必须由 timeline证明，且在所有 ranks、真实 network load下成立。隐藏在平均图中的最后一个 bucket仍可能决定 barrier。

## 14. Second-order effects

1. Kernel加速会缩短 overlap窗口，让 network更暴露。
2. Activation checkpoint节省 memory，却增加 compute与能耗。
3. Sharding减少 state复制，却增加 fine-grained collectives。
4. 更大 global batch提高 utilization，却可能损害 convergence。
5. MoE降低每 token compute，却引入 All-to-All与 load imbalance。
6. 更频繁 checkpoint减少重算，却增加 storage与 network traffic。
7. Elastic recovery提高 fleet utilization，却增加 reproducibility与 optimizer语义复杂度。

## 15. Engineers actually say

- “Scaling efficiency is eighty percent.”：问从几个 ranks到几个、固定 global batch还是弱缩放。
- “Communication is hidden.”：问最后 exposed bucket与 resource contention。
- “We are input-bound.”：问 storage、CPU、tokenization还是 H2D。
- “FSDP solves memory.”：问哪种 sharding、gather频率与 checkpoint。
- “The job has high utilization.”：问 skipped steps、stragglers与 time-to-quality。
- “Checkpoint overhead is low.”：问写入、同步、恢复和重算全部成本。

## 16. Engineering → Strategy

| Step阶段 | 约束 | 投资方向 | 价值控制点 |
|---|---|---|---|
| Data | CPU/storage/packing | pipeline与storage | data software |
| Forward/backward | compute/HBM | accelerator/kernel | silicon+compiler |
| Gradient sync | network/topology | NIC/switch/fabric | networking |
| Optimizer | state capacity/bytes | sharding/memory | HBM/runtime |
| Checkpoint | storage/recovery | parallel I/O | storage platform |
| Fleet | failures/queue | scheduler/telemetry | cloud operations |

## 17. Technical diligence questions

1. Step timeline按 rank、kernel、collective如何分解？
2. Global batch、sequence、precision与 target quality是否固定？
3. Activation、gradient、optimizer state与 workspace各多大？
4. Parallelism组合为何选择，traffic matrix是什么？
5. Communication真正 overlap多少，最后哪个 bucket暴露？
6. Straggler p95/p99来自哪些层？
7. Sharding/recomputation节省什么、增加什么？
8. Checkpoint interval、写入、恢复与重算的期望成本？
9. Failure/degraded topology下 step time与 correctness？
10. Peak到 time-to-quality waterfall中最大 loss是什么？

## 18. Takeaways

1. 一个 training step是 data、compute、memory、collective、optimizer与 storage的关键路径。
2. Backward gradient ready order决定 communication overlap。
3. Parallelism是在 memory capacity与 communication之间交换。
4. Step/s只有在相同 global batch、quality和失败边界下才有意义。
5. 优化一个阶段会缩短 overlap或把 bottleneck移到下一层。

## Primary sources

- [Primary Source] [PyTorch DistributedDataParallel](https://docs.pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html)
- [Primary Source] [PyTorch DDP Design Note](https://docs.pytorch.org/docs/stable/notes/ddp)
- [Primary Source] [PyTorch FullyShardedDataParallel](https://docs.pytorch.org/docs/stable/fsdp.html)
- [Primary Source] [NVIDIA NCCL Documentation](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/)


## 基础概念桥接

先把训练、prefill、decode、embedding、recommendation 与 multimodal 拆成不同 phase。明确 weights、activations、gradients、optimizer state、KV cache 的生命周期，再写 batch、sequence、precision、arrival distribution 和 SLO。模型名称本身不是硬件需求。

延伸基础：[工程术语手册](../31_glossary/engineering_terms_handbook.md)；[工程度量与不确定性](../02_engineering_foundations/engineering_measurement_uncertainty.md)；[数字逻辑、处理器与加速器](../02_engineering_foundations/digital_compute_accelerator_vocabulary.md)。


## 进阶工程术语桥接

本篇进一步需要掌握：微操作、流水线冒险、并行度、shape、动态批处理、尾延迟、数量级与单位经济性。阅读这些术语时，不只记中英文对应，还要补齐系统位置、正常路径、饱和或失败路径、直接 counter、端到端结果、产品状态和证据等级。若工程会议出现“已解决”“无开销”“已量产”，应立即追问 workload、boundary、configuration、status/date、failure mode 与 falsifier。

延伸阅读：[进阶工程术语手册](../31_glossary/advanced_engineering_terms_handbook.md)。
