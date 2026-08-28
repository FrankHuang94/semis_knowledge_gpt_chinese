# 进阶工程术语手册

> 本手册新增一百二十个在芯片架构、AI 系统、制造、运维和技术尽调中高频出现的术语。每个条目都从直觉、系统位置、机制、量化、证据、误区和追问七个角度展开，目标是让读者能够进入真实工程对话，而不是只会识别缩写。

## 计算与工作负载：architecture

该组术语连接数值表示、流水线、并行执行与模型 shape。判断性能时要区分峰值执行能力、可发射工作、数据供给和有效输出；同一个硬件在短序列、小 batch、分支密集或不规则访问下可能表现完全不同。

### 微操作（Micro-operation）

**基础直觉：**复杂指令在微架构内部拆成的更小执行动作。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语连接数值表示、流水线、并行执行与模型 shape。判断性能时要区分峰值执行能力、可发射工作、数据供给和有效输出；同一个硬件在短序列、小 batch、分支密集或不规则访问下可能表现完全不同。把“微操作”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“微操作”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更多 core、更高频率或更低精度直接换算成应用加速，也不要用一个 shape 代表生产分布。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“微操作 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**执行单元为何会空闲？shape、依赖、局部性、编译器和质量约束分别贡献多少？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“微操作”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../04_computer_architecture/cpu_gpu_npu.md)。

### 重排序缓冲区（Reorder Buffer）

**基础直觉：**保存未退休操作并维持精确异常和程序可见顺序。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语连接数值表示、流水线、并行执行与模型 shape。判断性能时要区分峰值执行能力、可发射工作、数据供给和有效输出；同一个硬件在短序列、小 batch、分支密集或不规则访问下可能表现完全不同。把“重排序缓冲区”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“重排序缓冲区”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更多 core、更高频率或更低精度直接换算成应用加速，也不要用一个 shape 代表生产分布。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“重排序缓冲区 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**执行单元为何会空闲？shape、依赖、局部性、编译器和质量约束分别贡献多少？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“重排序缓冲区”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../04_computer_architecture/cpu_gpu_npu.md)。

### 分支目标缓冲区（Branch Target Buffer）

**基础直觉：**缓存分支目标以缩短取指控制转移。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语连接数值表示、流水线、并行执行与模型 shape。判断性能时要区分峰值执行能力、可发射工作、数据供给和有效输出；同一个硬件在短序列、小 batch、分支密集或不规则访问下可能表现完全不同。把“分支目标缓冲区”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“分支目标缓冲区”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更多 core、更高频率或更低精度直接换算成应用加速，也不要用一个 shape 代表生产分布。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“分支目标缓冲区 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**执行单元为何会空闲？shape、依赖、局部性、编译器和质量约束分别贡献多少？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“分支目标缓冲区”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../04_computer_architecture/cpu_gpu_npu.md)。

### 加载存储队列（Load Store Queue）

**基础直觉：**跟踪未完成内存操作并处理地址依赖。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语连接数值表示、流水线、并行执行与模型 shape。判断性能时要区分峰值执行能力、可发射工作、数据供给和有效输出；同一个硬件在短序列、小 batch、分支密集或不规则访问下可能表现完全不同。把“加载存储队列”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“加载存储队列”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更多 core、更高频率或更低精度直接换算成应用加速，也不要用一个 shape 代表生产分布。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“加载存储队列 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**执行单元为何会空闲？shape、依赖、局部性、编译器和质量约束分别贡献多少？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“加载存储队列”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../04_computer_architecture/cpu_gpu_npu.md)。

### 存储缓冲区（Store Buffer）

**基础直觉：**暂存尚未写入缓存或内存的 store。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语连接数值表示、流水线、并行执行与模型 shape。判断性能时要区分峰值执行能力、可发射工作、数据供给和有效输出；同一个硬件在短序列、小 batch、分支密集或不规则访问下可能表现完全不同。把“存储缓冲区”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“存储缓冲区”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更多 core、更高频率或更低精度直接换算成应用加速，也不要用一个 shape 代表生产分布。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“存储缓冲区 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**执行单元为何会空闲？shape、依赖、局部性、编译器和质量约束分别贡献多少？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“存储缓冲区”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../04_computer_architecture/cpu_gpu_npu.md)。

### 指令级并行（Instruction-level Parallelism）

**基础直觉：**同一线程中可同时执行的独立操作数量。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语连接数值表示、流水线、并行执行与模型 shape。判断性能时要区分峰值执行能力、可发射工作、数据供给和有效输出；同一个硬件在短序列、小 batch、分支密集或不规则访问下可能表现完全不同。把“指令级并行”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“指令级并行”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更多 core、更高频率或更低精度直接换算成应用加速，也不要用一个 shape 代表生产分布。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“指令级并行 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**执行单元为何会空闲？shape、依赖、局部性、编译器和质量约束分别贡献多少？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“指令级并行”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../04_computer_architecture/cpu_gpu_npu.md)。

### 线程级并行（Thread-level Parallelism）

**基础直觉：**通过多个线程隐藏等待并扩大执行供给。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语连接数值表示、流水线、并行执行与模型 shape。判断性能时要区分峰值执行能力、可发射工作、数据供给和有效输出；同一个硬件在短序列、小 batch、分支密集或不规则访问下可能表现完全不同。把“线程级并行”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“线程级并行”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更多 core、更高频率或更低精度直接换算成应用加速，也不要用一个 shape 代表生产分布。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“线程级并行 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**执行单元为何会空闲？shape、依赖、局部性、编译器和质量约束分别贡献多少？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“线程级并行”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../04_computer_architecture/cpu_gpu_npu.md)。

### 控制冒险（Control Hazard）

**基础直觉：**未知控制流对流水线供给和回滚造成的风险。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语连接数值表示、流水线、并行执行与模型 shape。判断性能时要区分峰值执行能力、可发射工作、数据供给和有效输出；同一个硬件在短序列、小 batch、分支密集或不规则访问下可能表现完全不同。把“控制冒险”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“控制冒险”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更多 core、更高频率或更低精度直接换算成应用加速，也不要用一个 shape 代表生产分布。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“控制冒险 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**执行单元为何会空闲？shape、依赖、局部性、编译器和质量约束分别贡献多少？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“控制冒险”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../04_computer_architecture/cpu_gpu_npu.md)。

### 数据冒险（Data Hazard）

**基础直觉：**操作之间的读写依赖限制调度和重排。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语连接数值表示、流水线、并行执行与模型 shape。判断性能时要区分峰值执行能力、可发射工作、数据供给和有效输出；同一个硬件在短序列、小 batch、分支密集或不规则访问下可能表现完全不同。把“数据冒险”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“数据冒险”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更多 core、更高频率或更低精度直接换算成应用加速，也不要用一个 shape 代表生产分布。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“数据冒险 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**执行单元为何会空闲？shape、依赖、局部性、编译器和质量约束分别贡献多少？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“数据冒险”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../04_computer_architecture/cpu_gpu_npu.md)。

### 结构冒险（Structural Hazard）

**基础直觉：**多个操作竞争同一硬件资源产生的冲突。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语连接数值表示、流水线、并行执行与模型 shape。判断性能时要区分峰值执行能力、可发射工作、数据供给和有效输出；同一个硬件在短序列、小 batch、分支密集或不规则访问下可能表现完全不同。把“结构冒险”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“结构冒险”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更多 core、更高频率或更低精度直接换算成应用加速，也不要用一个 shape 代表生产分布。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“结构冒险 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**执行单元为何会空闲？shape、依赖、局部性、编译器和质量约束分别贡献多少？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“结构冒险”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../04_computer_architecture/cpu_gpu_npu.md)。

## 计算与工作负载：gpu_architecture

该组术语连接数值表示、流水线、并行执行与模型 shape。判断性能时要区分峰值执行能力、可发射工作、数据供给和有效输出；同一个硬件在短序列、小 batch、分支密集或不规则访问下可能表现完全不同。

### Warp 分歧（Warp Divergence）

**基础直觉：**同组线程选择不同控制路径导致执行串行化。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语连接数值表示、流水线、并行执行与模型 shape。判断性能时要区分峰值执行能力、可发射工作、数据供给和有效输出；同一个硬件在短序列、小 batch、分支密集或不规则访问下可能表现完全不同。把“Warp 分歧”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“Warp 分歧”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更多 core、更高频率或更低精度直接换算成应用加速，也不要用一个 shape 代表生产分布。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“Warp 分歧 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**执行单元为何会空闲？shape、依赖、局部性、编译器和质量约束分别贡献多少？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“Warp 分歧”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../06_gpu_accelerator/gpu_execution_kernel_performance.md)。

### 访存合并（Memory Coalescing）

**基础直觉：**把相邻线程请求合并成较少内存事务。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语连接数值表示、流水线、并行执行与模型 shape。判断性能时要区分峰值执行能力、可发射工作、数据供给和有效输出；同一个硬件在短序列、小 batch、分支密集或不规则访问下可能表现完全不同。把“访存合并”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“访存合并”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更多 core、更高频率或更低精度直接换算成应用加速，也不要用一个 shape 代表生产分布。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“访存合并 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**执行单元为何会空闲？shape、依赖、局部性、编译器和质量约束分别贡献多少？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“访存合并”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../06_gpu_accelerator/gpu_execution_kernel_performance.md)。

### Kernel 启动开销（Kernel Launch Overhead）

**基础直觉：**提交和调度短 kernel 的固定时间成本。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语连接数值表示、流水线、并行执行与模型 shape。判断性能时要区分峰值执行能力、可发射工作、数据供给和有效输出；同一个硬件在短序列、小 batch、分支密集或不规则访问下可能表现完全不同。把“Kernel 启动开销”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“Kernel 启动开销”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更多 core、更高频率或更低精度直接换算成应用加速，也不要用一个 shape 代表生产分布。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“Kernel 启动开销 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**执行单元为何会空闲？shape、依赖、局部性、编译器和质量约束分别贡献多少？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“Kernel 启动开销”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../06_gpu_accelerator/gpu_execution_kernel_performance.md)。

### 寄存器溢出（Register Spill）

**基础直觉：**活跃值超过分配后被写到更慢存储。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语连接数值表示、流水线、并行执行与模型 shape。判断性能时要区分峰值执行能力、可发射工作、数据供给和有效输出；同一个硬件在短序列、小 batch、分支密集或不规则访问下可能表现完全不同。把“寄存器溢出”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“寄存器溢出”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更多 core、更高频率或更低精度直接换算成应用加速，也不要用一个 shape 代表生产分布。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“寄存器溢出 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**执行单元为何会空闲？shape、依赖、局部性、编译器和质量约束分别贡献多少？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“寄存器溢出”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../06_gpu_accelerator/gpu_execution_kernel_performance.md)。

### 共享存储 Bank 冲突（Shared-memory Bank Conflict）

**基础直觉：**多个线程同周期访问冲突 bank 造成串行。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语连接数值表示、流水线、并行执行与模型 shape。判断性能时要区分峰值执行能力、可发射工作、数据供给和有效输出；同一个硬件在短序列、小 batch、分支密集或不规则访问下可能表现完全不同。把“共享存储 Bank 冲突”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“共享存储 Bank 冲突”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更多 core、更高频率或更低精度直接换算成应用加速，也不要用一个 shape 代表生产分布。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“共享存储 Bank 冲突 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**执行单元为何会空闲？shape、依赖、局部性、编译器和质量约束分别贡献多少？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“共享存储 Bank 冲突”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../06_gpu_accelerator/gpu_execution_kernel_performance.md)。

### 常驻 Kernel（Persistent Kernel）

**基础直觉：**长时间驻留设备并自行取得任务的执行模式。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语连接数值表示、流水线、并行执行与模型 shape。判断性能时要区分峰值执行能力、可发射工作、数据供给和有效输出；同一个硬件在短序列、小 batch、分支密集或不规则访问下可能表现完全不同。把“常驻 Kernel”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“常驻 Kernel”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更多 core、更高频率或更低精度直接换算成应用加速，也不要用一个 shape 代表生产分布。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“常驻 Kernel 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**执行单元为何会空闲？shape、依赖、局部性、编译器和质量约束分别贡献多少？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“常驻 Kernel”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../06_gpu_accelerator/gpu_execution_kernel_performance.md)。

### 序列并行（Sequence Parallelism）

**基础直觉：**沿 sequence 维度切分状态和计算。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语连接数值表示、流水线、并行执行与模型 shape。判断性能时要区分峰值执行能力、可发射工作、数据供给和有效输出；同一个硬件在短序列、小 batch、分支密集或不规则访问下可能表现完全不同。把“序列并行”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“序列并行”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更多 core、更高频率或更低精度直接换算成应用加速，也不要用一个 shape 代表生产分布。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“序列并行 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**执行单元为何会空闲？shape、依赖、局部性、编译器和质量约束分别贡献多少？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“序列并行”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../06_gpu_accelerator/gpu_execution_kernel_performance.md)。

### 专家并行（Expert Parallelism）

**基础直觉：**把 MoE experts 分布到不同设备并交换 token。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语连接数值表示、流水线、并行执行与模型 shape。判断性能时要区分峰值执行能力、可发射工作、数据供给和有效输出；同一个硬件在短序列、小 batch、分支密集或不规则访问下可能表现完全不同。把“专家并行”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“专家并行”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更多 core、更高频率或更低精度直接换算成应用加速，也不要用一个 shape 代表生产分布。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“专家并行 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**执行单元为何会空闲？shape、依赖、局部性、编译器和质量约束分别贡献多少？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“专家并行”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../06_gpu_accelerator/gpu_execution_kernel_performance.md)。

### 激活重计算（Activation Recomputation）

**基础直觉：**少存中间激活并在反向阶段重新计算。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语连接数值表示、流水线、并行执行与模型 shape。判断性能时要区分峰值执行能力、可发射工作、数据供给和有效输出；同一个硬件在短序列、小 batch、分支密集或不规则访问下可能表现完全不同。把“激活重计算”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“激活重计算”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更多 core、更高频率或更低精度直接换算成应用加速，也不要用一个 shape 代表生产分布。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“激活重计算 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**执行单元为何会空闲？shape、依赖、局部性、编译器和质量约束分别贡献多少？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“激活重计算”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../06_gpu_accelerator/gpu_execution_kernel_performance.md)。

### 动态批处理（Dynamic Batching）

**基础直觉：**运行时按到达和形状组合请求以提高利用率。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语连接数值表示、流水线、并行执行与模型 shape。判断性能时要区分峰值执行能力、可发射工作、数据供给和有效输出；同一个硬件在短序列、小 batch、分支密集或不规则访问下可能表现完全不同。把“动态批处理”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“动态批处理”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更多 core、更高频率或更低精度直接换算成应用加速，也不要用一个 shape 代表生产分布。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“动态批处理 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**执行单元为何会空闲？shape、依赖、局部性、编译器和质量约束分别贡献多少？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“动态批处理”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../06_gpu_accelerator/gpu_execution_kernel_performance.md)。

## 存储与 I/O：dram

该组术语描述数据如何驻留、寻址、迁移和保持一致。容量、延迟、带宽、并发与故障语义不能互相替代；任何 tiering 或 pooling 都会增加 placement、translation、migration 和 recovery 责任。

### 行缓冲区（Row Buffer）

**基础直觉：**保存已激活 DRAM row 并影响命中与延迟。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述数据如何驻留、寻址、迁移和保持一致。容量、延迟、带宽、并发与故障语义不能互相替代；任何 tiering 或 pooling 都会增加 placement、translation、migration 和 recovery 责任。把“行缓冲区”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“行缓冲区”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更大容量当成更低延迟，或把 peak bandwidth 当成随机访问和迁移后的有效能力。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“行缓冲区 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**数据在哪一层、以多大粒度访问？translation、queue、migration 和 coherence 的成本在哪里测量？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“行缓冲区”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../08_memory/dram.md)。

### 行命中（Row Hit）

**基础直觉：**请求访问当前已打开 row 从而避免重新激活。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述数据如何驻留、寻址、迁移和保持一致。容量、延迟、带宽、并发与故障语义不能互相替代；任何 tiering 或 pooling 都会增加 placement、translation、migration 和 recovery 责任。把“行命中”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“行命中”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更大容量当成更低延迟，或把 peak bandwidth 当成随机访问和迁移后的有效能力。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“行命中 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**数据在哪一层、以多大粒度访问？translation、queue、migration 和 coherence 的成本在哪里测量？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“行命中”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../08_memory/dram.md)。

### Bank Group（一组共享部分时序或数据路径的 DRAM banks）

**基础直觉：**undefined。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述数据如何驻留、寻址、迁移和保持一致。容量、延迟、带宽、并发与故障语义不能互相替代；任何 tiering 或 pooling 都会增加 placement、translation、migration 和 recovery 责任。把“Bank Group”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“Bank Group”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更大容量当成更低延迟，或把 peak bandwidth 当成随机访问和迁移后的有效能力。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“Bank Group 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**数据在哪一层、以多大粒度访问？translation、queue、migration 和 coherence 的成本在哪里测量？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“Bank Group”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../08_memory/dram.md)。

### 突发长度（Burst Length）

**基础直觉：**一次命令连续传输的数据拍数。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述数据如何驻留、寻址、迁移和保持一致。容量、延迟、带宽、并发与故障语义不能互相替代；任何 tiering 或 pooling 都会增加 placement、translation、migration 和 recovery 责任。把“突发长度”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“突发长度”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更大容量当成更低延迟，或把 peak bandwidth 当成随机访问和迁移后的有效能力。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“突发长度 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**数据在哪一层、以多大粒度访问？translation、queue、migration 和 coherence 的成本在哪里测量？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“突发长度”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../08_memory/dram.md)。

### 刷新间隔（Refresh Interval）

**基础直觉：**为维持电荷而重新写回 DRAM cell 的时间节奏。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述数据如何驻留、寻址、迁移和保持一致。容量、延迟、带宽、并发与故障语义不能互相替代；任何 tiering 或 pooling 都会增加 placement、translation、migration 和 recovery 责任。把“刷新间隔”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“刷新间隔”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更大容量当成更低延迟，或把 peak bandwidth 当成随机访问和迁移后的有效能力。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“刷新间隔 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**数据在哪一层、以多大粒度访问？translation、queue、migration 和 coherence 的成本在哪里测量？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“刷新间隔”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../08_memory/dram.md)。

### 内存控制器（Memory Controller）

**基础直觉：**调度命令并管理 timing refresh ECC 和地址映射。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述数据如何驻留、寻址、迁移和保持一致。容量、延迟、带宽、并发与故障语义不能互相替代；任何 tiering 或 pooling 都会增加 placement、translation、migration 和 recovery 责任。把“内存控制器”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“内存控制器”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更大容量当成更低延迟，或把 peak bandwidth 当成随机访问和迁移后的有效能力。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“内存控制器 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**数据在哪一层、以多大粒度访问？translation、queue、migration 和 coherence 的成本在哪里测量？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“内存控制器”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../08_memory/dram.md)。

### 地址交织（Address Interleaving）

**基础直觉：**把连续地址分散到 channel bank 或 rank。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述数据如何驻留、寻址、迁移和保持一致。容量、延迟、带宽、并发与故障语义不能互相替代；任何 tiering 或 pooling 都会增加 placement、translation、migration 和 recovery 责任。把“地址交织”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“地址交织”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更大容量当成更低延迟，或把 peak bandwidth 当成随机访问和迁移后的有效能力。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“地址交织 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**数据在哪一层、以多大粒度访问？translation、queue、migration 和 coherence 的成本在哪里测量？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“地址交织”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../08_memory/dram.md)。

### 写恢复时间（Write Recovery Time）

**基础直觉：**写入后允许 precharge 前需要等待的时序。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述数据如何驻留、寻址、迁移和保持一致。容量、延迟、带宽、并发与故障语义不能互相替代；任何 tiering 或 pooling 都会增加 placement、translation、migration 和 recovery 责任。把“写恢复时间”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“写恢复时间”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更大容量当成更低延迟，或把 peak bandwidth 当成随机访问和迁移后的有效能力。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“写恢复时间 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**数据在哪一层、以多大粒度访问？translation、queue、migration 和 coherence 的成本在哪里测量？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“写恢复时间”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../08_memory/dram.md)。

### 内存巡检（Memory Scrubbing）

**基础直觉：**后台读取纠错并回写以减少潜伏错误累积。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述数据如何驻留、寻址、迁移和保持一致。容量、延迟、带宽、并发与故障语义不能互相替代；任何 tiering 或 pooling 都会增加 placement、translation、migration 和 recovery 责任。把“内存巡检”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“内存巡检”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更大容量当成更低延迟，或把 peak bandwidth 当成随机访问和迁移后的有效能力。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“内存巡检 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**数据在哪一层、以多大粒度访问？translation、queue、migration 和 coherence 的成本在哪里测量？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“内存巡检”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../08_memory/dram.md)。

### 毒化数据（Poisoned Data）

**基础直觉：**携带不可纠正错误标记并阻止静默使用的数据。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述数据如何驻留、寻址、迁移和保持一致。容量、延迟、带宽、并发与故障语义不能互相替代；任何 tiering 或 pooling 都会增加 placement、translation、migration 和 recovery 责任。把“毒化数据”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“毒化数据”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更大容量当成更低延迟，或把 peak bandwidth 当成随机访问和迁移后的有效能力。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“毒化数据 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**数据在哪一层、以多大粒度访问？translation、queue、migration 和 coherence 的成本在哪里测量？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“毒化数据”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../08_memory/dram.md)。

## 存储与 I/O：io

该组术语描述数据如何驻留、寻址、迁移和保持一致。容量、延迟、带宽、并发与故障语义不能互相替代；任何 tiering 或 pooling 都会增加 placement、translation、migration 和 recovery 责任。

### 直接内存访问（Direct Memory Access）

**基础直觉：**设备无需 CPU 搬运每个 byte 即可访问内存。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述数据如何驻留、寻址、迁移和保持一致。容量、延迟、带宽、并发与故障语义不能互相替代；任何 tiering 或 pooling 都会增加 placement、translation、migration 和 recovery 责任。把“直接内存访问”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“直接内存访问”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更大容量当成更低延迟，或把 peak bandwidth 当成随机访问和迁移后的有效能力。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“直接内存访问 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**数据在哪一层、以多大粒度访问？translation、queue、migration 和 coherence 的成本在哪里测量？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“直接内存访问”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../10_pcie_cxl_io/cxl_tiered_memory.md)。

### 输入输出内存管理单元（IOMMU）

**基础直觉：**转换和保护设备发起的内存地址。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述数据如何驻留、寻址、迁移和保持一致。容量、延迟、带宽、并发与故障语义不能互相替代；任何 tiering 或 pooling 都会增加 placement、translation、migration 和 recovery 责任。把“输入输出内存管理单元”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“输入输出内存管理单元”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更大容量当成更低延迟，或把 peak bandwidth 当成随机访问和迁移后的有效能力。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“输入输出内存管理单元 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**数据在哪一层、以多大粒度访问？translation、queue、migration 和 coherence 的成本在哪里测量？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“输入输出内存管理单元”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../10_pcie_cxl_io/cxl_tiered_memory.md)。

### 地址转换服务（Address Translation Service）

**基础直觉：**让设备请求并缓存主机地址转换。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述数据如何驻留、寻址、迁移和保持一致。容量、延迟、带宽、并发与故障语义不能互相替代；任何 tiering 或 pooling 都会增加 placement、translation、migration 和 recovery 责任。把“地址转换服务”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“地址转换服务”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更大容量当成更低延迟，或把 peak bandwidth 当成随机访问和迁移后的有效能力。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“地址转换服务 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**数据在哪一层、以多大粒度访问？translation、queue、migration 和 coherence 的成本在哪里测量？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“地址转换服务”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../10_pcie_cxl_io/cxl_tiered_memory.md)。

### 缺页异常（Page Fault）

**基础直觉：**访问页尚未映射或驻留时触发的软件处理。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述数据如何驻留、寻址、迁移和保持一致。容量、延迟、带宽、并发与故障语义不能互相替代；任何 tiering 或 pooling 都会增加 placement、translation、migration 和 recovery 责任。把“缺页异常”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“缺页异常”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更大容量当成更低延迟，或把 peak bandwidth 当成随机访问和迁移后的有效能力。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“缺页异常 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**数据在哪一层、以多大粒度访问？translation、queue、migration 和 coherence 的成本在哪里测量？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“缺页异常”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../10_pcie_cxl_io/cxl_tiered_memory.md)。

### 固定页内存（Pinned Memory）

**基础直觉：**禁止换出的主机页以提供可预测 DMA。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述数据如何驻留、寻址、迁移和保持一致。容量、延迟、带宽、并发与故障语义不能互相替代；任何 tiering 或 pooling 都会增加 placement、translation、migration 和 recovery 责任。把“固定页内存”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“固定页内存”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更大容量当成更低延迟，或把 peak bandwidth 当成随机访问和迁移后的有效能力。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“固定页内存 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**数据在哪一层、以多大粒度访问？translation、queue、migration 和 coherence 的成本在哪里测量？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“固定页内存”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../10_pcie_cxl_io/cxl_tiered_memory.md)。

### 页面迁移（Page Migration）

**基础直觉：**在不同 memory tiers 或 NUMA nodes 间移动页。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述数据如何驻留、寻址、迁移和保持一致。容量、延迟、带宽、并发与故障语义不能互相替代；任何 tiering 或 pooling 都会增加 placement、translation、migration 和 recovery 责任。把“页面迁移”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“页面迁移”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更大容量当成更低延迟，或把 peak bandwidth 当成随机访问和迁移后的有效能力。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“页面迁移 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**数据在哪一层、以多大粒度访问？translation、queue、migration 和 coherence 的成本在哪里测量？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“页面迁移”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../10_pcie_cxl_io/cxl_tiered_memory.md)。

### 内存池化（Memory Pooling）

**基础直觉：**多个 host 或 device 按策略共享容量资源。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述数据如何驻留、寻址、迁移和保持一致。容量、延迟、带宽、并发与故障语义不能互相替代；任何 tiering 或 pooling 都会增加 placement、translation、migration 和 recovery 责任。把“内存池化”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“内存池化”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更大容量当成更低延迟，或把 peak bandwidth 当成随机访问和迁移后的有效能力。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“内存池化 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**数据在哪一层、以多大粒度访问？translation、queue、migration 和 coherence 的成本在哪里测量？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“内存池化”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../10_pcie_cxl_io/cxl_tiered_memory.md)。

### 缓存一致性（Cache Coherence）

**基础直觉：**维护多个缓存副本对共享地址的可见关系。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述数据如何驻留、寻址、迁移和保持一致。容量、延迟、带宽、并发与故障语义不能互相替代；任何 tiering 或 pooling 都会增加 placement、translation、migration 和 recovery 责任。把“缓存一致性”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“缓存一致性”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更大容量当成更低延迟，或把 peak bandwidth 当成随机访问和迁移后的有效能力。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“缓存一致性 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**数据在哪一层、以多大粒度访问？translation、queue、migration 和 coherence 的成本在哪里测量？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“缓存一致性”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../10_pcie_cxl_io/cxl_tiered_memory.md)。

### 内存顺序（Memory Ordering）

**基础直觉：**规定操作对不同观察者可见的先后约束。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述数据如何驻留、寻址、迁移和保持一致。容量、延迟、带宽、并发与故障语义不能互相替代；任何 tiering 或 pooling 都会增加 placement、translation、migration 和 recovery 责任。把“内存顺序”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“内存顺序”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更大容量当成更低延迟，或把 peak bandwidth 当成随机访问和迁移后的有效能力。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“内存顺序 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**数据在哪一层、以多大粒度访问？translation、queue、migration 和 coherence 的成本在哪里测量？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“内存顺序”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../10_pcie_cxl_io/cxl_tiered_memory.md)。

### 热插拔（Hot Plug）

**基础直觉：**系统运行时增加或移除设备并处理状态变化。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述数据如何驻留、寻址、迁移和保持一致。容量、延迟、带宽、并发与故障语义不能互相替代；任何 tiering 或 pooling 都会增加 placement、translation、migration 和 recovery 责任。把“热插拔”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“热插拔”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把更大容量当成更低延迟，或把 peak bandwidth 当成随机访问和迁移后的有效能力。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“热插拔 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**数据在哪一层、以多大粒度访问？translation、queue、migration 和 coherence 的成本在哪里测量？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“热插拔”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../10_pcie_cxl_io/cxl_tiered_memory.md)。

## 高速互连与光学：serdes

该组术语从 electrical channel 延伸到 packet fabric 和 optical link。必须分清序列化、传播、排队、协议、重传和纠错；线速、symbol rate、payload throughput 与 collective completion 不是同一个指标。

### 序列化延迟（Serialization Latency）

**基础直觉：**把并行数据按链路速率发送所需时间。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语从 electrical channel 延伸到 packet fabric 和 optical link。必须分清序列化、传播、排队、协议、重传和纠错；线速、symbol rate、payload throughput 与 collective completion 不是同一个指标。把“序列化延迟”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“序列化延迟”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把单链路 headline 当作多 hop、拥塞、故障和 FEC 条件下的应用性能。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“序列化延迟 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**从应用 bytes 到物理符号经过哪些开销？拥塞、错误和失效后还有多少有效吞吐？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“序列化延迟”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../11_serdes_signal_integrity/serdes.md)。

### 传播延迟（Propagation Delay）

**基础直觉：**信号穿过介质和物理距离所需时间。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语从 electrical channel 延伸到 packet fabric 和 optical link。必须分清序列化、传播、排队、协议、重传和纠错；线速、symbol rate、payload throughput 与 collective completion 不是同一个指标。把“传播延迟”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“传播延迟”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把单链路 headline 当作多 hop、拥塞、故障和 FEC 条件下的应用性能。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“传播延迟 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**从应用 bytes 到物理符号经过哪些开销？拥塞、错误和失效后还有多少有效吞吐？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“传播延迟”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../11_serdes_signal_integrity/serdes.md)。

### 插入损耗（Insertion Loss）

**基础直觉：**channel 对前向信号幅度造成的衰减。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语从 electrical channel 延伸到 packet fabric 和 optical link。必须分清序列化、传播、排队、协议、重传和纠错；线速、symbol rate、payload throughput 与 collective completion 不是同一个指标。把“插入损耗”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“插入损耗”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把单链路 headline 当作多 hop、拥塞、故障和 FEC 条件下的应用性能。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“插入损耗 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**从应用 bytes 到物理符号经过哪些开销？拥塞、错误和失效后还有多少有效吞吐？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“插入损耗”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../11_serdes_signal_integrity/serdes.md)。

### 回波损耗（Return Loss）

**基础直觉：**阻抗不连续产生反射的量化指标。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语从 electrical channel 延伸到 packet fabric 和 optical link。必须分清序列化、传播、排队、协议、重传和纠错；线速、symbol rate、payload throughput 与 collective completion 不是同一个指标。把“回波损耗”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“回波损耗”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把单链路 headline 当作多 hop、拥塞、故障和 FEC 条件下的应用性能。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“回波损耗 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**从应用 bytes 到物理符号经过哪些开销？拥塞、错误和失效后还有多少有效吞吐？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“回波损耗”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../11_serdes_signal_integrity/serdes.md)。

### 串扰（Crosstalk）

**基础直觉：**相邻 aggressor 对 victim channel 注入干扰。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语从 electrical channel 延伸到 packet fabric 和 optical link。必须分清序列化、传播、排队、协议、重传和纠错；线速、symbol rate、payload throughput 与 collective completion 不是同一个指标。把“串扰”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“串扰”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把单链路 headline 当作多 hop、拥塞、故障和 FEC 条件下的应用性能。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“串扰 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**从应用 bytes 到物理符号经过哪些开销？拥塞、错误和失效后还有多少有效吞吐？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“串扰”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../11_serdes_signal_integrity/serdes.md)。

### 眼图开口（Eye Opening）

**基础直觉：**采样点附近电压和时间余量的可视化。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语从 electrical channel 延伸到 packet fabric 和 optical link。必须分清序列化、传播、排队、协议、重传和纠错；线速、symbol rate、payload throughput 与 collective completion 不是同一个指标。把“眼图开口”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“眼图开口”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把单链路 headline 当作多 hop、拥塞、故障和 FEC 条件下的应用性能。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“眼图开口 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**从应用 bytes 到物理符号经过哪些开销？拥塞、错误和失效后还有多少有效吞吐？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“眼图开口”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../11_serdes_signal_integrity/serdes.md)。

### 均衡（Equalization）

**基础直觉：**补偿 channel 频率相关损耗和符号间干扰。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语从 electrical channel 延伸到 packet fabric 和 optical link。必须分清序列化、传播、排队、协议、重传和纠错；线速、symbol rate、payload throughput 与 collective completion 不是同一个指标。把“均衡”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“均衡”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把单链路 headline 当作多 hop、拥塞、故障和 FEC 条件下的应用性能。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“均衡 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**从应用 bytes 到物理符号经过哪些开销？拥塞、错误和失效后还有多少有效吞吐？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“均衡”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../11_serdes_signal_integrity/serdes.md)。

### 时钟数据恢复（Clock and Data Recovery）

**基础直觉：**从接收数据中恢复采样时钟和相位。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语从 electrical channel 延伸到 packet fabric 和 optical link。必须分清序列化、传播、排队、协议、重传和纠错；线速、symbol rate、payload throughput 与 collective completion 不是同一个指标。把“时钟数据恢复”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“时钟数据恢复”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把单链路 headline 当作多 hop、拥塞、故障和 FEC 条件下的应用性能。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“时钟数据恢复 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**从应用 bytes 到物理符号经过哪些开销？拥塞、错误和失效后还有多少有效吞吐？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“时钟数据恢复”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../11_serdes_signal_integrity/serdes.md)。

### 前向纠错（Forward Error Correction）

**基础直觉：**用冗余编码在不重传时纠正部分错误。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语从 electrical channel 延伸到 packet fabric 和 optical link。必须分清序列化、传播、排队、协议、重传和纠错；线速、symbol rate、payload throughput 与 collective completion 不是同一个指标。把“前向纠错”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“前向纠错”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把单链路 headline 当作多 hop、拥塞、故障和 FEC 条件下的应用性能。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“前向纠错 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**从应用 bytes 到物理符号经过哪些开销？拥塞、错误和失效后还有多少有效吞吐？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“前向纠错”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../11_serdes_signal_integrity/serdes.md)。

### 误码率（Bit Error Rate）

**基础直觉：**错误 bit 相对传输 bit 的比例。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语从 electrical channel 延伸到 packet fabric 和 optical link。必须分清序列化、传播、排队、协议、重传和纠错；线速、symbol rate、payload throughput 与 collective completion 不是同一个指标。把“误码率”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“误码率”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把单链路 headline 当作多 hop、拥塞、故障和 FEC 条件下的应用性能。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“误码率 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**从应用 bytes 到物理符号经过哪些开销？拥塞、错误和失效后还有多少有效吞吐？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“误码率”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../11_serdes_signal_integrity/serdes.md)。

## 高速互连与光学：networking

该组术语从 electrical channel 延伸到 packet fabric 和 optical link。必须分清序列化、传播、排队、协议、重传和纠错；线速、symbol rate、payload throughput 与 collective completion 不是同一个指标。

### 队头阻塞（Head-of-line Blocking）

**基础直觉：**前方受阻工作阻止后续可服务工作前进。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语从 electrical channel 延伸到 packet fabric 和 optical link。必须分清序列化、传播、排队、协议、重传和纠错；线速、symbol rate、payload throughput 与 collective completion 不是同一个指标。把“队头阻塞”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“队头阻塞”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把单链路 headline 当作多 hop、拥塞、故障和 FEC 条件下的应用性能。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“队头阻塞 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**从应用 bytes 到物理符号经过哪些开销？拥塞、错误和失效后还有多少有效吞吐？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“队头阻塞”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../13_scale_out_networking/ai_ethernet_rdma.md)。

### 直通交换（Cut-through Switching）

**基础直觉：**收到部分 frame 后即开始转发以降低延迟。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语从 electrical channel 延伸到 packet fabric 和 optical link。必须分清序列化、传播、排队、协议、重传和纠错；线速、symbol rate、payload throughput 与 collective completion 不是同一个指标。把“直通交换”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“直通交换”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把单链路 headline 当作多 hop、拥塞、故障和 FEC 条件下的应用性能。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“直通交换 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**从应用 bytes 到物理符号经过哪些开销？拥塞、错误和失效后还有多少有效吞吐？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“直通交换”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../13_scale_out_networking/ai_ethernet_rdma.md)。

### 存储转发（Store-and-forward）

**基础直觉：**完整接收并校验 frame 后再转发。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语从 electrical channel 延伸到 packet fabric 和 optical link。必须分清序列化、传播、排队、协议、重传和纠错；线速、symbol rate、payload throughput 与 collective completion 不是同一个指标。把“存储转发”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“存储转发”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把单链路 headline 当作多 hop、拥塞、故障和 FEC 条件下的应用性能。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“存储转发 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**从应用 bytes 到物理符号经过哪些开销？拥塞、错误和失效后还有多少有效吞吐？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“存储转发”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../13_scale_out_networking/ai_ethernet_rdma.md)。

### 显式拥塞标记（ECN Marking）

**基础直觉：**在丢包前标记 queue pressure 通知发送端减速。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语从 electrical channel 延伸到 packet fabric 和 optical link。必须分清序列化、传播、排队、协议、重传和纠错；线速、symbol rate、payload throughput 与 collective completion 不是同一个指标。把“显式拥塞标记”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“显式拥塞标记”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把单链路 headline 当作多 hop、拥塞、故障和 FEC 条件下的应用性能。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“显式拥塞标记 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**从应用 bytes 到物理符号经过哪些开销？拥塞、错误和失效后还有多少有效吞吐？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“显式拥塞标记”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../13_scale_out_networking/ai_ethernet_rdma.md)。

### 优先级流控暂停（Priority Flow Control Pause）

**基础直觉：**按 priority 暂停上游发送以避免 buffer 溢出。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语从 electrical channel 延伸到 packet fabric 和 optical link。必须分清序列化、传播、排队、协议、重传和纠错；线速、symbol rate、payload throughput 与 collective completion 不是同一个指标。把“优先级流控暂停”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“优先级流控暂停”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把单链路 headline 当作多 hop、拥塞、故障和 FEC 条件下的应用性能。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“优先级流控暂停 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**从应用 bytes 到物理符号经过哪些开销？拥塞、错误和失效后还有多少有效吞吐？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“优先级流控暂停”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../13_scale_out_networking/ai_ethernet_rdma.md)。

### 数据包乱序（Packet Reordering）

**基础直觉：**不同路径或恢复导致 packet 到达顺序改变。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语从 electrical channel 延伸到 packet fabric 和 optical link。必须分清序列化、传播、排队、协议、重传和纠错；线速、symbol rate、payload throughput 与 collective completion 不是同一个指标。把“数据包乱序”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“数据包乱序”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把单链路 headline 当作多 hop、拥塞、故障和 FEC 条件下的应用性能。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“数据包乱序 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**从应用 bytes 到物理符号经过哪些开销？拥塞、错误和失效后还有多少有效吞吐？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“数据包乱序”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../13_scale_out_networking/ai_ethernet_rdma.md)。

### 重传（Retransmission）

**基础直觉：**检测丢失或错误后再次发送数据。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语从 electrical channel 延伸到 packet fabric 和 optical link。必须分清序列化、传播、排队、协议、重传和纠错；线速、symbol rate、payload throughput 与 collective completion 不是同一个指标。把“重传”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“重传”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把单链路 headline 当作多 hop、拥塞、故障和 FEC 条件下的应用性能。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“重传 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**从应用 bytes 到物理符号经过哪些开销？拥塞、错误和失效后还有多少有效吞吐？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“重传”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../13_scale_out_networking/ai_ethernet_rdma.md)。

### 汇聚拥塞（Incast）

**基础直觉：**多个 sender 同时向少数 receiver 发送形成突发。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语从 electrical channel 延伸到 packet fabric 和 optical link。必须分清序列化、传播、排队、协议、重传和纠错；线速、symbol rate、payload throughput 与 collective completion 不是同一个指标。把“汇聚拥塞”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“汇聚拥塞”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把单链路 headline 当作多 hop、拥塞、故障和 FEC 条件下的应用性能。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“汇聚拥塞 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**从应用 bytes 到物理符号经过哪些开销？拥塞、错误和失效后还有多少有效吞吐？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“汇聚拥塞”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../13_scale_out_networking/ai_ethernet_rdma.md)。

### 光链路预算（Optical Link Budget）

**基础直觉：**发射功率扣除路径损耗和接收要求后的余量。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语从 electrical channel 延伸到 packet fabric 和 optical link。必须分清序列化、传播、排队、协议、重传和纠错；线速、symbol rate、payload throughput 与 collective completion 不是同一个指标。把“光链路预算”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“光链路预算”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把单链路 headline 当作多 hop、拥塞、故障和 FEC 条件下的应用性能。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“光链路预算 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**从应用 bytes 到物理符号经过哪些开销？拥塞、错误和失效后还有多少有效吞吐？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“光链路预算”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../13_scale_out_networking/ai_ethernet_rdma.md)。

### FEC 余量（FEC Margin）

**基础直觉：**相对纠错能力边界仍保留的错误裕量。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语从 electrical channel 延伸到 packet fabric 和 optical link。必须分清序列化、传播、排队、协议、重传和纠错；线速、symbol rate、payload throughput 与 collective completion 不是同一个指标。把“FEC 余量”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“FEC 余量”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把单链路 headline 当作多 hop、拥塞、故障和 FEC 条件下的应用性能。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“FEC 余量 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**从应用 bytes 到物理符号经过哪些开销？拥塞、错误和失效后还有多少有效吞吐？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“FEC 余量”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../13_scale_out_networking/ai_ethernet_rdma.md)。

## 物理系统与制造：power

该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。

### 电阻压降（IR Drop）

**基础直觉：**电流经过有限电阻产生的稳态电压损失。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“电阻压降”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“电阻压降”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“电阻压降 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“电阻压降”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../18_power_delivery/power_delivery.md)。

### 电感性压降（Inductive Droop）

**基础直觉：**电流快速变化通过寄生电感产生的瞬态压降。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“电感性压降”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“电感性压降”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“电感性压降 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“电感性压降”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../18_power_delivery/power_delivery.md)。

### 目标阻抗（Target Impedance）

**基础直觉：**为限制电压波动而设定的 PDN 阻抗上限。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“目标阻抗”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“目标阻抗”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“目标阻抗 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“目标阻抗”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../18_power_delivery/power_delivery.md)。

### 去耦电容（Decoupling Capacitor）

**基础直觉：**在负载附近暂时供能并抑制电压变化。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“去耦电容”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“去耦电容”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“去耦电容 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“去耦电容”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../18_power_delivery/power_delivery.md)。

### 负载线（Load Line）

**基础直觉：**输出电压随负载电流变化的设计关系。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“负载线”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“负载线”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“负载线 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“负载线”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../18_power_delivery/power_delivery.md)。

### 相位关闭（Phase Shedding）

**基础直觉：**低负载时关闭部分 VRM phases 提高效率。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“相位关闭”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“相位关闭”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“相位关闭 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“相位关闭”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../18_power_delivery/power_delivery.md)。

### 功率上限（Power Cap）

**基础直觉：**限制设备允许消耗功率的控制约束。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“功率上限”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“功率上限”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“功率上限 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“功率上限”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../18_power_delivery/power_delivery.md)。

### 动态电压频率调整（Dynamic Voltage and Frequency Scaling）

**基础直觉：**按负载和 margin 联合改变电压与频率。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“动态电压频率调整”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“动态电压频率调整”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“动态电压频率调整 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“动态电压频率调整”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../18_power_delivery/power_delivery.md)。

### 欠压事件（Brownout）

**基础直觉：**供电低于安全范围但未完全断电的状态。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“欠压事件”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“欠压事件”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“欠压事件 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“欠压事件”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../18_power_delivery/power_delivery.md)。

### 电源正常信号（Power Good）

**基础直觉：**表示 rail 已进入可接受范围的控制信号。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“电源正常信号”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“电源正常信号”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“电源正常信号 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“电源正常信号”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../18_power_delivery/power_delivery.md)。

## 物理系统与制造：thermal

该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。

### 热阻（Thermal Resistance）

**基础直觉：**单位热流引起的稳态温差。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“热阻”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“热阻”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“热阻 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“热阻”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../19_thermal_cooling/thermal_cooling.md)。

### 热容（Thermal Capacitance）

**基础直觉：**系统储存热量并延缓温度变化的能力。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“热容”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“热容”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“热容 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“热容”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../19_thermal_cooling/thermal_cooling.md)。

### 结温（Junction Temperature）

**基础直觉：**半导体有源区的工作温度。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“结温”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“结温”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“结温 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“结温”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../19_thermal_cooling/thermal_cooling.md)。

### 热界面材料（Thermal Interface Material）

**基础直觉：**填充接触微空隙以降低界面热阻。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“热界面材料”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“热界面材料”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“热界面材料 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“热界面材料”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../19_thermal_cooling/thermal_cooling.md)。

### 冷却液流量（Coolant Flow Rate）

**基础直觉：**单位时间通过冷却回路的流体量。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“冷却液流量”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“冷却液流量”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“冷却液流量 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“冷却液流量”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../19_thermal_cooling/thermal_cooling.md)。

### 压降（Pressure Drop）

**基础直觉：**流体经过管路和冷板时损失的压力。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“压降”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“压降”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“压降 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“压降”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../19_thermal_cooling/thermal_cooling.md)。

### 露点（Dew Point）

**基础直觉：**空气水汽开始凝结的温度边界。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“露点”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“露点”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“露点 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“露点”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../19_thermal_cooling/thermal_cooling.md)。

### 流量不均（Flow Imbalance）

**基础直觉：**并联支路因阻抗差获得不同流量。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“流量不均”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“流量不均”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“流量不均 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“流量不均”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../19_thermal_cooling/thermal_cooling.md)。

### 热降频（Thermal Throttling）

**基础直觉：**温度或热 margin 不足时降低性能。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“热降频”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“热降频”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“热降频 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“热降频”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../19_thermal_cooling/thermal_cooling.md)。

### 排热（Heat Rejection）

**基础直觉：**把设施吸收的热最终释放到外部环境。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“排热”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“排热”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“排热 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“排热”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../19_thermal_cooling/thermal_cooling.md)。

## 物理系统与制造：packaging

该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。

### 热膨胀系数（Coefficient of Thermal Expansion）

**基础直觉：**材料温度变化时尺寸变化的比例。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“热膨胀系数”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“热膨胀系数”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“热膨胀系数 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“热膨胀系数”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../16_advanced_packaging/advanced_packaging.md)。

### 翘曲（Warpage）

**基础直觉：**封装或基板因应力产生的非平面变形。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“翘曲”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“翘曲”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“翘曲 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“翘曲”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../16_advanced_packaging/advanced_packaging.md)。

### 底部填充材料（Underfill）

**基础直觉：**填充 die 与基板间隙以分散机械应力。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“底部填充材料”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“底部填充材料”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“底部填充材料 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“底部填充材料”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../16_advanced_packaging/advanced_packaging.md)。

### 凸点间距（Bump Pitch）

**基础直觉：**相邻互连 bumps 中心间距离。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“凸点间距”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“凸点间距”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“凸点间距 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“凸点间距”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../16_advanced_packaging/advanced_packaging.md)。

### 混合键合（Hybrid Bonding）

**基础直觉：**介质与金属同时直接连接的高密度 bonding。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“混合键合”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“混合键合”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“混合键合 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“混合键合”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../16_advanced_packaging/advanced_packaging.md)。

### 已知良品裸片（Known-good Die）

**基础直觉：**在组装前通过既定测试覆盖的 die。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“已知良品裸片”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“已知良品裸片”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“已知良品裸片 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“已知良品裸片”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../16_advanced_packaging/advanced_packaging.md)。

### 晶圆分选（Wafer Sort）

**基础直觉：**封装前在 wafer 上测试并分类 dies。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“晶圆分选”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“晶圆分选”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“晶圆分选 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“晶圆分选”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../16_advanced_packaging/advanced_packaging.md)。

### 老化筛选（Burn-in）

**基础直觉：**施加应力以暴露早期失效的测试过程。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“老化筛选”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“老化筛选”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“老化筛选 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“老化筛选”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../16_advanced_packaging/advanced_packaging.md)。

### 缺陷密度（Defect Density）

**基础直觉：**单位制造面积中可能导致失效的缺陷水平。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“缺陷密度”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“缺陷密度”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“缺陷密度 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“缺陷密度”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../16_advanced_packaging/advanced_packaging.md)。

### 工艺窗口（Process Window）

**基础直觉：**仍能满足质量要求的参数组合范围。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语把供电、热、材料、装配和良率放入同一物理系统。局部电气或热优化会改变机械应力和制造窗口；实验室样片通过也不代表目标产品完成可靠性、测试、资格认证和规模爬坡。把“工艺窗口”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“工艺窗口”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 TDP、冷板额定值、设备安装数或技术样片当成可交付 good systems。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“工艺窗口 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**最坏温压和冗余故障下还有多少 margin？逐站 yield、cycle time、test 和 qualification 状态是什么？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“工艺窗口”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../16_advanced_packaging/advanced_packaging.md)。

## 软件、可靠性与运维：compiler

该组术语描述硬件能力如何经 compiler、runtime、driver 和 fleet operations 兑现。功能正确只是起点；版本兼容、性能回归、遥测、故障隔离、回滚和恢复决定长期可用产出。

### 计算图捕获（Graph Capture）

**基础直觉：**记录运行操作和依赖以便整体优化或重放。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述硬件能力如何经 compiler、runtime、driver 和 fleet operations 兑现。功能正确只是起点；版本兼容、性能回归、遥测、故障隔离、回滚和恢复决定长期可用产出。把“计算图捕获”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“计算图捕获”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把一个手工优化 demo 当成平台覆盖，也不要只用平均 uptime 隐藏 tail failure 和恢复成本。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“计算图捕获 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**哪些版本和路径原生支持？fallback、回归、故障检测、blast radius 和恢复时间如何观测？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“计算图捕获”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../21_software_hardware_codesign/software_hardware_codesign.md)。

### 算子降级（Operator Lowering）

**基础直觉：**把高层语义逐步转换为低层实现。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述硬件能力如何经 compiler、runtime、driver 和 fleet operations 兑现。功能正确只是起点；版本兼容、性能回归、遥测、故障隔离、回滚和恢复决定长期可用产出。把“算子降级”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“算子降级”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把一个手工优化 demo 当成平台覆盖，也不要只用平均 uptime 隐藏 tail failure 和恢复成本。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“算子降级 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**哪些版本和路径原生支持？fallback、回归、故障检测、blast radius 和恢复时间如何观测？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“算子降级”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../21_software_hardware_codesign/software_hardware_codesign.md)。

### 中间表示方言（IR Dialect）

**基础直觉：**为特定抽象层定义操作和类型的 IR 集合。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述硬件能力如何经 compiler、runtime、driver 和 fleet operations 兑现。功能正确只是起点；版本兼容、性能回归、遥测、故障隔离、回滚和恢复决定长期可用产出。把“中间表示方言”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“中间表示方言”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把一个手工优化 demo 当成平台覆盖，也不要只用平均 uptime 隐藏 tail failure 和恢复成本。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“中间表示方言 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**哪些版本和路径原生支持？fallback、回归、故障检测、blast radius 和恢复时间如何观测？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“中间表示方言”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../21_software_hardware_codesign/software_hardware_codesign.md)。

### 形状特化（Shape Specialization）

**基础直觉：**针对特定 tensor shape 生成优化代码。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述硬件能力如何经 compiler、runtime、driver 和 fleet operations 兑现。功能正确只是起点；版本兼容、性能回归、遥测、故障隔离、回滚和恢复决定长期可用产出。把“形状特化”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“形状特化”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把一个手工优化 demo 当成平台覆盖，也不要只用平均 uptime 隐藏 tail failure 和恢复成本。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“形状特化 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**哪些版本和路径原生支持？fallback、回归、故障检测、blast radius 和恢复时间如何观测？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“形状特化”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../21_software_hardware_codesign/software_hardware_codesign.md)。

### 自动调优（Autotuning）

**基础直觉：**搜索 tile algorithm 和参数以选择较快实现。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述硬件能力如何经 compiler、runtime、driver 和 fleet operations 兑现。功能正确只是起点；版本兼容、性能回归、遥测、故障隔离、回滚和恢复决定长期可用产出。把“自动调优”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“自动调优”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把一个手工优化 demo 当成平台覆盖，也不要只用平均 uptime 隐藏 tail failure 和恢复成本。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“自动调优 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**哪些版本和路径原生支持？fallback、回归、故障检测、blast radius 和恢复时间如何观测？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“自动调优”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../21_software_hardware_codesign/software_hardware_codesign.md)。

### Kernel 缓存（Kernel Cache）

**基础直觉：**保存已编译或已调优 kernel 避免重复成本。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述硬件能力如何经 compiler、runtime、driver 和 fleet operations 兑现。功能正确只是起点；版本兼容、性能回归、遥测、故障隔离、回滚和恢复决定长期可用产出。把“Kernel 缓存”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“Kernel 缓存”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把一个手工优化 demo 当成平台覆盖，也不要只用平均 uptime 隐藏 tail failure 和恢复成本。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“Kernel 缓存 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**哪些版本和路径原生支持？fallback、回归、故障检测、blast radius 和恢复时间如何观测？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“Kernel 缓存”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../21_software_hardware_codesign/software_hardware_codesign.md)。

### 运行时调度器（Runtime Scheduler）

**基础直觉：**在设备 stream 和资源间安排工作。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述硬件能力如何经 compiler、runtime、driver 和 fleet operations 兑现。功能正确只是起点；版本兼容、性能回归、遥测、故障隔离、回滚和恢复决定长期可用产出。把“运行时调度器”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“运行时调度器”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把一个手工优化 demo 当成平台覆盖，也不要只用平均 uptime 隐藏 tail failure 和恢复成本。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“运行时调度器 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**哪些版本和路径原生支持？fallback、回归、故障检测、blast radius 和恢复时间如何观测？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“运行时调度器”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../21_software_hardware_codesign/software_hardware_codesign.md)。

### 应用二进制接口（Application Binary Interface）

**基础直觉：**约定调用、数据布局和二进制兼容。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述硬件能力如何经 compiler、runtime、driver 和 fleet operations 兑现。功能正确只是起点；版本兼容、性能回归、遥测、故障隔离、回滚和恢复决定长期可用产出。把“应用二进制接口”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“应用二进制接口”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把一个手工优化 demo 当成平台覆盖，也不要只用平均 uptime 隐藏 tail failure 和恢复成本。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“应用二进制接口 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**哪些版本和路径原生支持？fallback、回归、故障检测、blast radius 和恢复时间如何观测？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“应用二进制接口”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../21_software_hardware_codesign/software_hardware_codesign.md)。

### 设备驱动（Device Driver）

**基础直觉：**在操作系统和硬件之间管理命令与资源。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述硬件能力如何经 compiler、runtime、driver 和 fleet operations 兑现。功能正确只是起点；版本兼容、性能回归、遥测、故障隔离、回滚和恢复决定长期可用产出。把“设备驱动”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“设备驱动”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把一个手工优化 demo 当成平台覆盖，也不要只用平均 uptime 隐藏 tail failure 和恢复成本。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“设备驱动 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**哪些版本和路径原生支持？fallback、回归、故障检测、blast radius 和恢复时间如何观测？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“设备驱动”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../21_software_hardware_codesign/software_hardware_codesign.md)。

### 固件（Firmware）

**基础直觉：**在设备控制处理器上运行的低层软件。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述硬件能力如何经 compiler、runtime、driver 和 fleet operations 兑现。功能正确只是起点；版本兼容、性能回归、遥测、故障隔离、回滚和恢复决定长期可用产出。把“固件”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“固件”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把一个手工优化 demo 当成平台覆盖，也不要只用平均 uptime 隐藏 tail failure 和恢复成本。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“固件 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**哪些版本和路径原生支持？fallback、回归、故障检测、blast radius 和恢复时间如何观测？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“固件”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../21_software_hardware_codesign/software_hardware_codesign.md)。

## 软件、可靠性与运维：operations

该组术语描述硬件能力如何经 compiler、runtime、driver 和 fleet operations 兑现。功能正确只是起点；版本兼容、性能回归、遥测、故障隔离、回滚和恢复决定长期可用产出。

### 可观测性（Observability）

**基础直觉：**由外部信号推断系统内部状态的能力。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述硬件能力如何经 compiler、runtime、driver 和 fleet operations 兑现。功能正确只是起点；版本兼容、性能回归、遥测、故障隔离、回滚和恢复决定长期可用产出。把“可观测性”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“可观测性”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把一个手工优化 demo 当成平台覆盖，也不要只用平均 uptime 隐藏 tail failure 和恢复成本。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“可观测性 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**哪些版本和路径原生支持？fallback、回归、故障检测、blast radius 和恢复时间如何观测？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“可观测性”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../20_rack_cluster_datacenter/reliability_availability_serviceability.md)。

### 分布式追踪（Distributed Tracing）

**基础直觉：**关联跨服务和设备的请求时间线。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述硬件能力如何经 compiler、runtime、driver 和 fleet operations 兑现。功能正确只是起点；版本兼容、性能回归、遥测、故障隔离、回滚和恢复决定长期可用产出。把“分布式追踪”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“分布式追踪”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把一个手工优化 demo 当成平台覆盖，也不要只用平均 uptime 隐藏 tail failure 和恢复成本。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“分布式追踪 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**哪些版本和路径原生支持？fallback、回归、故障检测、blast radius 和恢复时间如何观测？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“分布式追踪”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../20_rack_cluster_datacenter/reliability_availability_serviceability.md)。

### 金丝雀发布（Canary Release）

**基础直觉：**先在小范围部署变更以限制风险。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述硬件能力如何经 compiler、runtime、driver 和 fleet operations 兑现。功能正确只是起点；版本兼容、性能回归、遥测、故障隔离、回滚和恢复决定长期可用产出。把“金丝雀发布”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“金丝雀发布”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把一个手工优化 demo 当成平台覆盖，也不要只用平均 uptime 隐藏 tail failure 和恢复成本。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“金丝雀发布 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**哪些版本和路径原生支持？fallback、回归、故障检测、blast radius 和恢复时间如何观测？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“金丝雀发布”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../20_rack_cluster_datacenter/reliability_availability_serviceability.md)。

### 回滚（Rollback）

**基础直觉：**把软件或配置恢复到已知稳定版本。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述硬件能力如何经 compiler、runtime、driver 和 fleet operations 兑现。功能正确只是起点；版本兼容、性能回归、遥测、故障隔离、回滚和恢复决定长期可用产出。把“回滚”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“回滚”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把一个手工优化 demo 当成平台覆盖，也不要只用平均 uptime 隐藏 tail failure 和恢复成本。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“回滚 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**哪些版本和路径原生支持？fallback、回归、故障检测、blast radius 和恢复时间如何观测？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“回滚”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../20_rack_cluster_datacenter/reliability_availability_serviceability.md)。

### 故障注入（Fault Injection）

**基础直觉：**主动制造受控错误验证检测和恢复。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述硬件能力如何经 compiler、runtime、driver 和 fleet operations 兑现。功能正确只是起点；版本兼容、性能回归、遥测、故障隔离、回滚和恢复决定长期可用产出。把“故障注入”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“故障注入”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把一个手工优化 demo 当成平台覆盖，也不要只用平均 uptime 隐藏 tail failure 和恢复成本。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“故障注入 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**哪些版本和路径原生支持？fallback、回归、故障检测、blast radius 和恢复时间如何观测？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“故障注入”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../20_rack_cluster_datacenter/reliability_availability_serviceability.md)。

### 检查点（Checkpoint）

**基础直觉：**保存可恢复状态以避免从头重做。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述硬件能力如何经 compiler、runtime、driver 和 fleet operations 兑现。功能正确只是起点；版本兼容、性能回归、遥测、故障隔离、回滚和恢复决定长期可用产出。把“检查点”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“检查点”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把一个手工优化 demo 当成平台覆盖，也不要只用平均 uptime 隐藏 tail failure 和恢复成本。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“检查点 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**哪些版本和路径原生支持？fallback、回归、故障检测、blast radius 和恢复时间如何观测？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“检查点”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../20_rack_cluster_datacenter/reliability_availability_serviceability.md)。

### 优雅降级（Graceful Degradation）

**基础直觉：**故障时保留部分功能而非完全中断。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述硬件能力如何经 compiler、runtime、driver 和 fleet operations 兑现。功能正确只是起点；版本兼容、性能回归、遥测、故障隔离、回滚和恢复决定长期可用产出。把“优雅降级”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“优雅降级”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把一个手工优化 demo 当成平台覆盖，也不要只用平均 uptime 隐藏 tail failure 和恢复成本。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“优雅降级 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**哪些版本和路径原生支持？fallback、回归、故障检测、blast radius 和恢复时间如何观测？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“优雅降级”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../20_rack_cluster_datacenter/reliability_availability_serviceability.md)。

### 故障影响范围（Blast Radius）

**基础直觉：**单一事件能够影响的系统和用户边界。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述硬件能力如何经 compiler、runtime、driver 和 fleet operations 兑现。功能正确只是起点；版本兼容、性能回归、遥测、故障隔离、回滚和恢复决定长期可用产出。把“故障影响范围”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“故障影响范围”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把一个手工优化 demo 当成平台覆盖，也不要只用平均 uptime 隐藏 tail failure 和恢复成本。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“故障影响范围 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**哪些版本和路径原生支持？fallback、回归、故障检测、blast radius 和恢复时间如何观测？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“故障影响范围”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../20_rack_cluster_datacenter/reliability_availability_serviceability.md)。

### 平均修复时间（Mean Time to Repair）

**基础直觉：**从故障到恢复服务的平均时长。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述硬件能力如何经 compiler、runtime、driver 和 fleet operations 兑现。功能正确只是起点；版本兼容、性能回归、遥测、故障隔离、回滚和恢复决定长期可用产出。把“平均修复时间”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“平均修复时间”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把一个手工优化 demo 当成平台覆盖，也不要只用平均 uptime 隐藏 tail failure 和恢复成本。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“平均修复时间 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**哪些版本和路径原生支持？fallback、回归、故障检测、blast radius 和恢复时间如何观测？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“平均修复时间”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../20_rack_cluster_datacenter/reliability_availability_serviceability.md)。

### 错误预算消耗（Error Budget Burn）

**基础直觉：**实际失败相对允许预算的消耗速度。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语描述硬件能力如何经 compiler、runtime、driver 和 fleet operations 兑现。功能正确只是起点；版本兼容、性能回归、遥测、故障隔离、回滚和恢复决定长期可用产出。把“错误预算消耗”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“错误预算消耗”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把一个手工优化 demo 当成平台覆盖，也不要只用平均 uptime 隐藏 tail failure 和恢复成本。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“错误预算消耗 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**哪些版本和路径原生支持？fallback、回归、故障检测、blast radius 和恢复时间如何观测？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“错误预算消耗”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../20_rack_cluster_datacenter/reliability_availability_serviceability.md)。

## 标准、产品与战略：standard

该组术语用于区分接口承诺、产品成熟度和商业价值。标准支持、送样、量产、出货、部署和收入是不同阶段；技术优势还要通过制造、生态、客户迁移、单位经济性和竞争反应才能形成价值。

### 标准配置档（Standard Profile）

**基础直觉：**从标准选取一组必选和可选功能的组合。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语用于区分接口承诺、产品成熟度和商业价值。标准支持、送样、量产、出货、部署和收入是不同阶段；技术优势还要通过制造、生态、客户迁移、单位经济性和竞争反应才能形成价值。把“标准配置档”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“标准配置档”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 announcement、logo、design win 或 roadmap 当成 shipping 和 deployed evidence。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“标准配置档 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**证据对应哪个状态和日期？若关键依赖延期，价值、成本与竞争位置如何变化？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“标准配置档”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../25_standards/standards_to_interoperability.md)。

### 可选功能（Optional Feature）

**基础直觉：**规范允许实现选择是否支持的能力。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语用于区分接口承诺、产品成熟度和商业价值。标准支持、送样、量产、出货、部署和收入是不同阶段；技术优势还要通过制造、生态、客户迁移、单位经济性和竞争反应才能形成价值。把“可选功能”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“可选功能”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 announcement、logo、design win 或 roadmap 当成 shipping 和 deployed evidence。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“可选功能 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**证据对应哪个状态和日期？若关键依赖延期，价值、成本与竞争位置如何变化？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“可选功能”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../25_standards/standards_to_interoperability.md)。

### 符合性测试（Compliance Test）

**基础直觉：**检查实现是否满足规定要求的测试。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语用于区分接口承诺、产品成熟度和商业价值。标准支持、送样、量产、出货、部署和收入是不同阶段；技术优势还要通过制造、生态、客户迁移、单位经济性和竞争反应才能形成价值。把“符合性测试”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“符合性测试”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 announcement、logo、design win 或 roadmap 当成 shipping 和 deployed evidence。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“符合性测试 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**证据对应哪个状态和日期？若关键依赖延期，价值、成本与竞争位置如何变化？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“符合性测试”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../25_standards/standards_to_interoperability.md)。

### 认证（Certification）

**基础直觉：**由指定流程确认产品达到一组条件。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语用于区分接口承诺、产品成熟度和商业价值。标准支持、送样、量产、出货、部署和收入是不同阶段；技术优势还要通过制造、生态、客户迁移、单位经济性和竞争反应才能形成价值。把“认证”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“认证”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 announcement、logo、design win 或 roadmap 当成 shipping 和 deployed evidence。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“认证 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**证据对应哪个状态和日期？若关键依赖延期，价值、成本与竞争位置如何变化？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“认证”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../25_standards/standards_to_interoperability.md)。

### 互操作活动（Plugfest）

**基础直觉：**多家实现集中互连以发现组合问题。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语用于区分接口承诺、产品成熟度和商业价值。标准支持、送样、量产、出货、部署和收入是不同阶段；技术优势还要通过制造、生态、客户迁移、单位经济性和竞争反应才能形成价值。把“互操作活动”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“互操作活动”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 announcement、logo、design win 或 roadmap 当成 shipping 和 deployed evidence。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“互操作活动 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**证据对应哪个状态和日期？若关键依赖延期，价值、成本与竞争位置如何变化？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“互操作活动”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../25_standards/standards_to_interoperability.md)。

### 勘误（Errata）

**基础直觉：**发布后确认的规范或实现错误与修正。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语用于区分接口承诺、产品成熟度和商业价值。标准支持、送样、量产、出货、部署和收入是不同阶段；技术优势还要通过制造、生态、客户迁移、单位经济性和竞争反应才能形成价值。把“勘误”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“勘误”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 announcement、logo、design win 或 roadmap 当成 shipping 和 deployed evidence。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“勘误 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**证据对应哪个状态和日期？若关键依赖延期，价值、成本与竞争位置如何变化？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“勘误”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../25_standards/standards_to_interoperability.md)。

### 送样状态（Sampling Status）

**基础直觉：**产品已向有限客户提供评估样品。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语用于区分接口承诺、产品成熟度和商业价值。标准支持、送样、量产、出货、部署和收入是不同阶段；技术优势还要通过制造、生态、客户迁移、单位经济性和竞争反应才能形成价值。把“送样状态”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“送样状态”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 announcement、logo、design win 或 roadmap 当成 shipping 和 deployed evidence。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“送样状态 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**证据对应哪个状态和日期？若关键依赖延期，价值、成本与竞争位置如何变化？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“送样状态”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../25_standards/standards_to_interoperability.md)。

### 量产状态（Production Status）

**基础直觉：**制造流程已进入正式规模生产阶段。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语用于区分接口承诺、产品成熟度和商业价值。标准支持、送样、量产、出货、部署和收入是不同阶段；技术优势还要通过制造、生态、客户迁移、单位经济性和竞争反应才能形成价值。把“量产状态”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“量产状态”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 announcement、logo、design win 或 roadmap 当成 shipping 和 deployed evidence。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“量产状态 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**证据对应哪个状态和日期？若关键依赖延期，价值、成本与竞争位置如何变化？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“量产状态”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../25_standards/standards_to_interoperability.md)。

### 出货状态（Shipping Status）

**基础直觉：**产品已向客户实际交付。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语用于区分接口承诺、产品成熟度和商业价值。标准支持、送样、量产、出货、部署和收入是不同阶段；技术优势还要通过制造、生态、客户迁移、单位经济性和竞争反应才能形成价值。把“出货状态”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“出货状态”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 announcement、logo、design win 或 roadmap 当成 shipping 和 deployed evidence。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“出货状态 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**证据对应哪个状态和日期？若关键依赖延期，价值、成本与竞争位置如何变化？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“出货状态”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../25_standards/standards_to_interoperability.md)。

### 部署状态（Deployed Status）

**基础直觉：**产品已在真实目标环境持续运行。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语用于区分接口承诺、产品成熟度和商业价值。标准支持、送样、量产、出货、部署和收入是不同阶段；技术优势还要通过制造、生态、客户迁移、单位经济性和竞争反应才能形成价值。把“部署状态”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“部署状态”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 announcement、logo、design win 或 roadmap 当成 shipping 和 deployed evidence。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“部署状态 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**证据对应哪个状态和日期？若关键依赖延期，价值、成本与竞争位置如何变化？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“部署状态”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../25_standards/standards_to_interoperability.md)。

## 标准、产品与战略：strategy

该组术语用于区分接口承诺、产品成熟度和商业价值。标准支持、送样、量产、出货、部署和收入是不同阶段；技术优势还要通过制造、生态、客户迁移、单位经济性和竞争反应才能形成价值。

### 设计导入（Design Win）

**基础直觉：**客户选择方案进入产品设计但未必形成出货。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语用于区分接口承诺、产品成熟度和商业价值。标准支持、送样、量产、出货、部署和收入是不同阶段；技术优势还要通过制造、生态、客户迁移、单位经济性和竞争反应才能形成价值。把“设计导入”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“设计导入”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 announcement、logo、design win 或 roadmap 当成 shipping 和 deployed evidence。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“设计导入 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**证据对应哪个状态和日期？若关键依赖延期，价值、成本与竞争位置如何变化？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“设计导入”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../26_engineering_to_strategy/engineering_to_strategy.md)。

### 搭载率（Attach Rate）

**基础直觉：**某组件随目标系统销售或部署的比例。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语用于区分接口承诺、产品成熟度和商业价值。标准支持、送样、量产、出货、部署和收入是不同阶段；技术优势还要通过制造、生态、客户迁移、单位经济性和竞争反应才能形成价值。把“搭载率”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“搭载率”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 announcement、logo、design win 或 roadmap 当成 shipping 和 deployed evidence。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“搭载率 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**证据对应哪个状态和日期？若关键依赖延期，价值、成本与竞争位置如何变化？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“搭载率”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../26_engineering_to_strategy/engineering_to_strategy.md)。

### 单系统价值量（Content per System）

**基础直觉：**每个系统包含的某类组件数量或金额。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语用于区分接口承诺、产品成熟度和商业价值。标准支持、送样、量产、出货、部署和收入是不同阶段；技术优势还要通过制造、生态、客户迁移、单位经济性和竞争反应才能形成价值。把“单系统价值量”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“单系统价值量”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 announcement、logo、design win 或 roadmap 当成 shipping 和 deployed evidence。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“单系统价值量 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**证据对应哪个状态和日期？若关键依赖延期，价值、成本与竞争位置如何变化？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“单系统价值量”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../26_engineering_to_strategy/engineering_to_strategy.md)。

### 总体可服务市场上限（Total Addressable Market）

**基础直觉：**在最宽假设下的总潜在需求。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语用于区分接口承诺、产品成熟度和商业价值。标准支持、送样、量产、出货、部署和收入是不同阶段；技术优势还要通过制造、生态、客户迁移、单位经济性和竞争反应才能形成价值。把“总体可服务市场上限”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“总体可服务市场上限”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 announcement、logo、design win 或 roadmap 当成 shipping 和 deployed evidence。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“总体可服务市场上限 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**证据对应哪个状态和日期？若关键依赖延期，价值、成本与竞争位置如何变化？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“总体可服务市场上限”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../26_engineering_to_strategy/engineering_to_strategy.md)。

### 可服务可获得市场范围（Serviceable Available Market）

**基础直觉：**受产品和渠道约束后可服务的市场。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语用于区分接口承诺、产品成熟度和商业价值。标准支持、送样、量产、出货、部署和收入是不同阶段；技术优势还要通过制造、生态、客户迁移、单位经济性和竞争反应才能形成价值。把“可服务可获得市场范围”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“可服务可获得市场范围”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 announcement、logo、design win 或 roadmap 当成 shipping 和 deployed evidence。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“可服务可获得市场范围 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**证据对应哪个状态和日期？若关键依赖延期，价值、成本与竞争位置如何变化？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“可服务可获得市场范围”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../26_engineering_to_strategy/engineering_to_strategy.md)。

### 近期可获取市场（Serviceable Obtainable Market）

**基础直觉：**在竞争和执行约束下可能获得的份额。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语用于区分接口承诺、产品成熟度和商业价值。标准支持、送样、量产、出货、部署和收入是不同阶段；技术优势还要通过制造、生态、客户迁移、单位经济性和竞争反应才能形成价值。把“近期可获取市场”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“近期可获取市场”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 announcement、logo、design win 或 roadmap 当成 shipping 和 deployed evidence。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“近期可获取市场 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**证据对应哪个状态和日期？若关键依赖延期，价值、成本与竞争位置如何变化？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“近期可获取市场”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../26_engineering_to_strategy/engineering_to_strategy.md)。

### 学习曲线（Learning Curve）

**基础直觉：**累积产出增加时单位成本或缺陷下降的经验关系。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语用于区分接口承诺、产品成熟度和商业价值。标准支持、送样、量产、出货、部署和收入是不同阶段；技术优势还要通过制造、生态、客户迁移、单位经济性和竞争反应才能形成价值。把“学习曲线”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“学习曲线”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 announcement、logo、design win 或 roadmap 当成 shipping 和 deployed evidence。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“学习曲线 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**证据对应哪个状态和日期？若关键依赖延期，价值、成本与竞争位置如何变化？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“学习曲线”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../26_engineering_to_strategy/engineering_to_strategy.md)。

### 资本密集度（Capital Intensity）

**基础直觉：**扩大收入或产能需要投入资本的程度。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语用于区分接口承诺、产品成熟度和商业价值。标准支持、送样、量产、出货、部署和收入是不同阶段；技术优势还要通过制造、生态、客户迁移、单位经济性和竞争反应才能形成价值。把“资本密集度”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“资本密集度”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 announcement、logo、design win 或 roadmap 当成 shipping 和 deployed evidence。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“资本密集度 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**证据对应哪个状态和日期？若关键依赖延期，价值、成本与竞争位置如何变化？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“资本密集度”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../26_engineering_to_strategy/engineering_to_strategy.md)。

### 切换成本（Switching Cost）

**基础直觉：**客户更换供应商或平台承担的迁移和风险。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语用于区分接口承诺、产品成熟度和商业价值。标准支持、送样、量产、出货、部署和收入是不同阶段；技术优势还要通过制造、生态、客户迁移、单位经济性和竞争反应才能形成价值。把“切换成本”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“切换成本”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 announcement、logo、design win 或 roadmap 当成 shipping 和 deployed evidence。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“切换成本 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**证据对应哪个状态和日期？若关键依赖延期，价值、成本与竞争位置如何变化？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“切换成本”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../26_engineering_to_strategy/engineering_to_strategy.md)。

### 价值迁移（Value Migration）

**基础直觉：**约束变化使利润和控制点在产业链间移动。它描述的是一个具体机制、状态或商业阶段；离开 workload、system boundary、configuration 和 as-of date 后，不能单独用于比较产品。

**系统位置：**该组术语用于区分接口承诺、产品成熟度和商业价值。标准支持、送样、量产、出货、部署和收入是不同阶段；技术优势还要通过制造、生态、客户迁移、单位经济性和竞争反应才能形成价值。把“价值迁移”放进完整路径时，应写明上游生产者、下游消费者、共享资源和 failure boundary，并区分由硬件、firmware、driver、runtime、operator 还是运维团队负责。

**机制拆解：**先画正常路径，再画 saturation、error 和 recovery 路径。列出状态在哪里保存、由什么事件推进、什么时候发生排队或重试、哪些动作能够并行、哪些必须同步。若一个术语无法连接到可观察状态或因果路径，它还只是标签。

**量化方法：**为“价值迁移”选择至少一个直接 counter 和一个端到端结果。记录测量点、单位、样本、分布、温度、版本、配置与误差；同时建立理论上限、保守保证和实测值，解释差额来自空闲、协议、搬运、竞争、降频、良率还是软件覆盖。

**证据与状态：**规格、标准和产品事实分别标为 [Primary Source]、[Independent]、[Vendor Claim]、[Estimate] 或 [Inference]。单次 demo 只证明特定条件下可行；资格认证、出货与生产部署需要额外的重复性、规模、时间和客户证据。

**常见误区：**不要把 announcement、logo、design win 或 roadmap 当成 shipping 和 deployed evidence。还要避免把局部平均值当 fleet 分布，把功能支持当性能支持，把 nominal capacity 当 qualified good output。

**工程口语翻译：**当听到“价值迁移 已解决”“没有开销”“已经量产”时，把原话改写为：在何种对象、边界、条件、时间和证据下，哪个指标达到什么状态。随后要求一个失败案例、一个 why-not 和一个能推翻主张的测试。

**工程追问：**证据对应哪个状态和日期？若关键依赖延期，价值、成本与竞争位置如何变化？当前设计与两个替代方案相比牺牲了什么？优化后 bottleneck 移到哪一层，谁获得或失去价值？

**练习：**从相关产品或公开材料中找一条包含“价值迁移”的主张，补齐 metric、boundary、status/date 和 evidence；再设计正常、压力和故障三组测试，并说明哪一项结果会改变采购、架构或投资判断。

**深入阅读：**[canonical article](../26_engineering_to_strategy/engineering_to_strategy.md)。

## 使用与维护

进阶术语必须与原有 glossary ID、canonical article 和 source freshness 保持一致。新增概念先判断是否属于现有机制的别名；若只是 marketing rename，保留 lineage 而不新建重复事实。每次标准版本、产品状态或实现边界变化，都要同时更新结构化数据、正文和 open questions。
