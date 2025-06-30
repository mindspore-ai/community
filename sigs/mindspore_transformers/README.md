## SIG 简介

MindSpore Transformers SIG（Special Interest Group）是 MindSpore 开源社区下聚焦 Transformer 类大模型全流程开发与优化的技术团队，涵盖大模型的预训练、微调、推理与部署等关键环节。SIG 团队致力于提升 Transformer类大模型在性能与易用性方面的表现，推动其在实际场景中的高效应用与落地。

MindSpore Transformers SIG 积极拥抱 Hugging Face、Megatron-LM、vLLM 等开源模型系统及训练推理框架生态，为用户提供高性能且易于使用的 MindSpore 大模型训练与推理能力。目前 MindSpore Transformers SIG 已孵化了开源大模型套件[MindSpore Transformers](https://gitee.com/mindspore/mindformers)，支持大模型预训练、微调、推理、部署全流程使能。

MindSpore Transformers SIG 所涉及的技术领域主要包括以下方面：

1. **大模型开发迁移**：基于 MindSpore AI 框架和 MindSpore Transformers 大模型套件开发大模型，或迁移适配其他框架的优秀开源大模型至 MindSpore Transformers。
2. **高效大模型训练**：依托 MindSpore 的图融合、通信-计算掩盖、多维混合并行等技术，实现高性能的大模型训练；支持主流数据集格式，提供完备数据集特性；大集群训练高可用，故障自动检测、自动恢复。
3. **高效大模型推理**：依托 MindSpore 的图融合、通信-计算掩盖、多维混合并行等技术，实现高性能的大模型推理；对接 MindSpore 金箍棒套件和 vLLM-MindSpore 插件，实现高效易用的大模型量化与服务化部署。
4. **大模型全流程易用性提升**：优化大模型全流程开发的易用性，提供清晰易用的生态资料；拥抱业界主流开源生态，无缝对接主流大模型训推框架、套件，提升大模型全流程开发迁移效率。

MindSpore Transformers SIG 欢迎开发者参与共同推动 Transformer 大模型在 MindSpore 框架下的标准化、高效化与工程化，实现大模型全流程端到端能力的创新与落地，助力 AI 研发者与产业用户轻松构建与应用大模型。

## Maintainers

* He Qinglin @Lin-Bert (MindSpore Transformers SIG 负责人)
* Su Haibo @suhaibo (MindSpore Transformers 架构师)

## Committers

* Huang Shengshuai @hss-shuai (MindSpore Transformers 训练负责人)
* Ren Yujin @renyujin (MindSpore Transformers 推理负责人)
* Chen Xinrui @chenrayray (MindSpore Transformers 生态&资料负责人)
* Zhang Youwen @zyw-hw (MindSpore Transformers 安全负责人)

## 目标

1. **聚焦大模型技术方向，推动关键技术演进**

   聚焦大模型全流程领域（包括大模型训推流程优化、精度性能调优、高可用、易用性等），持续跟踪前沿技术并组织实现落地。

   形成高质量的技术方案、设计文档与可复用模块。

2. **建设可持续的开源生态**

   积极孵化与引入优秀开源成果（如模型、工具、数据），与社区上下游生态对接，提升可用性与兼容性。

   通过标准化接口与组件，支持多场景适配和二次开发。

3. **推动贡献者协作与社区成长**

   制定并维护开发、测试、评审、发布等贡献流程。

   定期组织开发活动（如Code Review、Feature Hackathon、线上讨论会）。

   帮助新贡献者快速上手，培养活跃的贡献群体和核心维护者。

4. **保障贡献代码质量与可用性**

   输出稳定的里程碑版本和关键能力（如工程特性、并行算法等）。

   制定持续集成、精度验证、性能验证等标准，保证贡献代码质量可靠。

5. **推动成果落地与场景化应用**

   将 SIG 成果应用到实际业务、行业或科研任务中，形成示范案例。

   汇集反馈，持续改进 SIG 的方案和工具。

---

## 开发方向

### 1. 关键功能与模块开发

* 负责 MindSpore Transformers 项目核心功能模块的设计、开发与优化。
* 编写高质量、可复用、可扩展的组件。

### 2. 模型开发与生态集成

* 孵化或迁移优秀开源的模型或算法到 MindSpore Transformers。
* 对接主流大模型生态社区与框架（如 Hugging Face、vLLM、Megatron-LM），维护对上下游库（数据集、推理服务等）的兼容与集成。

### 3. 测试、验证与标准化

* 编写并维护单元测试、集成测试、性能测试、精度验证脚本。
* 制定配置、输出结果的一致性和可复现性标准。
* 输出可自动化的 CI/CD 流程。

### 4. 文档与示例

* 编写用户文档、开发者手册、API 参考和快速上手教程。
* 提供可执行示例、Notebook、参考配置。
* 持续完善 FAQ 和使用指南。

**上述开发方向欢迎感兴趣的开发者参与贡献！**

---

## 交流活动

### 1. 定期例会

* 每月第一个周四下午4点举办线上 SIG 定期例会。
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

## SIG 组织管理

### 成员身份说明

SIG的成员身份包括 Contributor、Committer、Maintainer，各角色的描述如下：

#### Contributor (贡献者）

* 职责范围：SIG 组及 MindSpore Transformers 项目的重要贡献者，代码仓库问题的主要修复者和代码开发者。

#### Committer (审核者）

* 职责范围：SIG 组部分仓库的看护者，是这部分仓库的第一责任人，审核其他成员的贡献。
* 要求：经验丰富，富有责任心、出色的技术能力和管理能力。从 Contributors 中选拔，有持续稳定的代码贡献。

#### Maintainer (维护者）

* 职责范围：SIG 组组长、牵引者、规划者，需做好SIG组的发展和演进，同时也是 MindSpore Transformers 项目 Owner，清楚项目的 Roadmap 版本规划、开发计划，对项目进行管理。
* 要求：经验丰富，富有责任心、出色的技术能力和管理能力。从 Committers 中选拔。