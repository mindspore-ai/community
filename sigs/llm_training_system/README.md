# LLM Training System SIG简介

LLM Training System SIG（Special Interest Group）是 MindSpore 开源社区下聚焦于利用分布式并行技术加速AI大模型训练的技术团队，团队致力于提升语言、多模态、全模态等大模型在分布式并行训练场景下的易用性与性能等方面的表现，提供可高效开发、灵活组合多种并行策略的并行编程范式，简化并行编程的复杂度，为开发者带来极简高效的分布式并行训练体验。

MindSpore Parallel SIG 所涉及的技术领域主要包括以下方面：

1. **并行优化**：通过数据并行、张量并行和流水线并行等并行技术，将训练任务拆分到多个计算设备上协同处理，显著提升大规模模型训练效率，解决单机算力瓶颈问题。
2. **计算优化**：采用混合精度训练、算子融合、稀疏计算等技术降低计算开销；通过减少浮点运算次数、合并内存访问操作、优化kernel调度，在保证精度的同时提升计算吞吐量，大幅缩短训练时间。
3. **通信优化**：针对多设备间参数同步需求，设计梯度压缩、分层AllReduce、通信隐藏等策略，通过聚合通信操作、计算通信掩盖，减少设备间通信延迟和带宽占用，解决分布式训练中通信成为性能瓶颈的问题。
4. **内存优化**：使用激活重计算、Offload、Zero Redundancy Optimizer等方法降低显存占用，通过动态释放中间变量、将部分数据交换到CPU内存、分片存储优化器状态，显著提升单卡可承载的模型规模。
5. **自动并行策略搜索**：用户无需关心策略配置，框架自动建立代价模型，找到训练时间较短的并行策略，减少人工调优成本。
6. **高可用训练**：采用弹性任务调度和断点续训机制，应对硬件故障或系统异常。结合监控和快速恢复策略，保障长周期训练任务的稳定性，减少因意外中断导致的训练成本损失，提升大规模训练的整体可靠性。

SIG为上述领域的专家、爱好者提供了一个交流、合作的平台。我们的愿景是打造根植于MindSpore的世界领先的分布式并行技术。MindSpore Parallel SIG的目标有两个：

1. 通过自动并行持续提升MindSpore分布式训练易用性及性能。
2. 助力MindSpore构建业界领先的大模型训练能力。

## SIG代码仓

1. [LLM Training System SIG](https://gitee.com/mindspore/community/tree/master/sigs/LLM-Training-System)

## Maintainers

* Li Cheng （中国科学技术大学特任研究员）
* Su Teng @stsuteng （MindSpore首席专家，SIG发起人）
* Yang Zhenzhang @yangzhenzhang (MindSpore分布式并行训练技术专家)
* Wang Kaisheng @kisnwang (MindSpore分布式并行训练技术专家)
* Yao Yifan @yao_yf (MindSpore分布式并行训练技术专家)

## Committers

* Tang Huikang @HulkTang (MindSpore AI工程技术专家，异构并行负责人)
* Liu Yanwei @liu-yanwei6 (MindSpore AI工程技术专家，MoE并行负责人)
* Wang Haoran @bj-wang (MindSpore AI工程技术专家，自动策略搜索负责人)
* Miao Yanming @askmiao (MindSpore AI工程技术专家，训练高可用负责人)

## 2025年Q4目标

1. 组织管理：完善SIG组织，邀请Maintainers（5名）与Commiters（至少4名）初始成员参与SIG运作；

2. 特性开发：在自动并行领域声明式编程和网络训练加速等方向中增加至少2个新特性并招募开发者共建；

3. 活动开展：开展至少2场技术分享活动直播, 征集分布式并行领域技术文章3+；

---

## 开发方向

### 1. 关键功能与模块开发

* 负责 MindSpore Parallel 项目核心功能模块的设计、开发与优化。
* 编写高质量、可复用、可扩展的代码。

### 2. 测试、验证与标准化

* 编写并维护单元测试、集成测试、性能测试、精度验证脚本。
* 制定配置、输出结果的一致性和可复现性标准。
* 输出可自动化的 CI/CD 流程。

### 3. 文档与示例

* 编写用户文档、开发者手册、API 参考和快速上手教程。
* 提供可执行示例、Notebook、参考配置。
* 持续完善 FAQ 和使用指南。

**上述开发方向欢迎感兴趣的开发者参与贡献！**

---

## 交流活动

### 1. 定期例会

* 每月第一个周五下午3点举办线上 SIG 定期例会。
* 汇报任务进展、讨论技术方案、共享最新动态。
* SIG 组织管理（如运作规则讨论、Maintainers & Committers 担任人员及职责刷新）。

### 2. 技术研讨与设计评审

* 组织专题技术分享（如某个 PR 的设计细节、模型训练优化方案）。
* 开展 RFC（Request for Comments）讨论，对重大设计或功能进行社区评审。

### 3. Issue 跟进与 PR 评审

* 定期梳理 Issue / Pull Request。
* 组织 Maintainer 和 Committer 团队进行 PR Review。
* 对外公开 Review 记录和决议，保持透明。

### 4. 社区沟通与对外分享

* 维护讨论渠道（如 Gitee Issue、邮件列表、微信群、社区论坛等）。
* 不定期举办社区 Meetup、分享会，分享 SIG 进展与行业、科研成功经验。

---

## SIG组织管理

### 成员身份说明

SIG的成员身份包括Maintainer、Committer、Contributor，各角色的描述和申请条件如下：

#### Maintainer

* 责任与权益：
  1. 确定 SIG 所负责项目的技术路线：包括规划和决策 SIG 技术方向、路标规划、架构演进。
  2. 制定 SIG 所负责项目的发布计划：确定 SIG 的关键需求和发布计划；参与社区的 PM 活动，并协调 SIG 计划和社区版本的里程碑时间表匹配。
  3. 参与社区协调活动：作为 SIG 的代表参与 MindSpore 技术委员会或理事会组织的活动和特定会议等。
  4. 召集 SIG 组会议：定期召集 SIG 会议，决策 SIG 内上升的争议
* 加入要求：
  1. 作为审核者至少 3 个月
  2. 作为主要审阅者至少参与了 12 次 PR 的审阅
  3. 审阅或合并至少 30 个基本 PR 到代码库
  4. 熟悉代码库
  5. 可以自我提名，也可以由子项目 Maintainer 提名，并且没有其他子项目 Maintainer 的反对

#### Committer

* 责任与权益：
  1. 评审 PR：对 Contributor 提交的 PR 完成评审，评审可以参考社区的[编程建议和安全编程规范](https://gitee.com/mindspore/community/blob/master/guidelines/python_programming_specification_zh_cn.md)。
  2. 分发处理问题:请参考“[问题处理流程](https://gitee.com/mindspore/community/blob/master/guidelines/issue_process_CN.md)”。
  3. 跟踪依赖性问题：在开发分支中，其他 SIG 组的软跟踪依赖性问题：在开发分支中，其他 SIG 组的更新可能会到导致破坏本 SIG 内项目的依赖关系。此时 Committer 会收到告警提示，Committer 应尽力重建处理。依赖关系出错可能会使最终用户无法更新系统，打包团队也会介入并重建存在依赖性问题的项目，但 Committer 不应依赖这些重建。
  4. 如有接口变更，需要通知可能会影响到的 SIG。Committer 应了解并评审&决策变更造成的依赖影响，并公告和发送 API 或 ABI 变更的告警邮件。这类公告应在变更发生至少一周前完成，并应通知到所有可能受影响的 SIG。

* 加入要求：
  1. 作为贡献者至少 3 个月
  2. 作为主要审阅者至少参与了 6 次 PR 的审阅
  3. 审阅或合并至少 20 个基本 PR 到代码库
  4. 熟悉代码库
  5. 可以自我提名，或由该 SIG 的审核者或维护者提名

#### Contributor

* 责任与权益：
  1. 响应被分配的问题和 PR
  2. 贡献的代码应该包括但不限于：经过良好的测试；能够让测试用例始终通过；解决后继发生的错误或问题
  3. 可以分配问题或 PR
  注意：经常贡献代码的成员应积极的参与代码审查，有机会成为 SIG 的审核者 Committer

* 加入要求：
  1. Gitee 上的注册会员
  2. 为 SIG 或社区做出多方面贡献，包括不限于：在 Gitee 上提交或审核 PR；在 Gitee 上对问题进行归档或评论；参与 SIG 或社区讨论
  3. 已阅读 贡献者指南，熟知贡献流程
  4. 积极参与 1 个或多个 SIG

## 近期活动与例会预告

1. 技术分享会
2. SIG例会

## 往期活动与例会

* [2022年3月16日：MindSpore的并行策略详解](https://mp.weixin.qq.com/s/ENi8sbghtIEcQFnGpWVEXg)