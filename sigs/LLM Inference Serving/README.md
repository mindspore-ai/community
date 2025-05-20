## SIG简介

大模型正在由理论研究阶段逐步进入大规模生产应用阶段，高吞吐、低时延的大模型推理服务部署能力，已成为AI基础软件栈的核心功能之一。近年来，vLLM、SGLang等开源推理服务框架迅速发展，覆盖支持了众多模型和特性，并已广泛应用于学术和工业领域。

LLM Inference Serving SIG致力于通过积极拥抱vLLM、SGLang等开源推理服务框架的软件生态，有机整合其技术长板，提供高性能、易用的MindSpore大模型推理部署能力。LLM Inference Serving SIG已孵化了开源插件[vLLM-MindSpore](https://gitee.com/mindspore/vllm_mindspore)，可支持[vLLM](https://github.com/vllm-project/vllm)框架以MindSpore为推理计算底座，实现大模型推理服务化部署。

LLM Inference Serving SIG所涉及的技术领域主要包括以下方面：
1. **开源推理服务框架兼容适配**：将MindSpore大模型推理能力，接入vLLM、SGLang等开源推理服务框架。以vLLM为例，通过将vLLM的PyTorch API调用映射至MindSpore，并适配vLLM的插件接口，将MindSpore大模型推理组件接入vLLM框架。
2. **大模型推理加速**：依托MindSpore的图融合、通信-计算掩盖等技术，实现高性能的大模型推理。

LLM Inference Serving SIG是开放开源的交流学习平台，欢迎开发者参与共同提升MindSpore的大模型推理能力，合作共建实现技术沉淀和产业成功。

## Maintainers

* Zhai Zhiqiang (MindSpore推理架构设计团队Leader，华为技术专家）
* Ye Zichun (数学博士，华为主任工程师）
* Pan Shaowu (MindSpore开发者，华为技术专家)

## Committers

* Zou Liqin (MindSpore开发者，华为主任工程师，负责vLLM V1架构适配开发)
* Zhang Zhaochuang (MindSpore开发者，华为高级工程师，负责vLLM服务组件适配开发)
* Deng Yepeng (MindSpore开发者，华为高级工程师，负责MoE大模型推理加速及vLLM适配对接)
* Wang Shaocong (MindSpore开发者，华为高级工程师，负责大模型分布式推理加速特性)
* Zhang Xuetong (MindSpore开发者，华为技术专家，负责MindSpore大模型推理加速系统设计)
* Tan Weicheng (MindSpore开发者，华为高级工程师，负责稠密大模型推理加速及vLLM适配对接)

## 2025年目标

1. 组织管理：制定SIG组织管理规范，邀请Maintainers与Contributors初始成员参与SIG运作(3名Maintainers + 至少5名Contributors）；
2. 生态拓展：发展30位LLM Inference Serving SIG正式成员、200+关注者；发展5位资深开发者、10位优秀开发者；
3. 特性开发：支持至少20个SOTA LLM和MMLM，持续适配vLLM最新稳定版本，挑战跟随vLLM主干分支演进，核心特性2天内适配支持；
4. 活动开展：vLLM-MindSpore体验活动参与人次300+，开展技术分享活动直播3次，征集技术文章10+。

## 主要活动

### 1. 线上技术分享会

* 活动定位：共同探讨大模型推理加速的相关话题
* 活动形式：定期邀请业界专家、高校师生、资深开发者分享话题
* 活动频率：每1-2个月1次，每次围绕同一个共同主题分享2-3个话题
* 分享范围：与大模型推理加速技术领域相关的技术话题，包括但不限于：
  1. vLLM、SGLang等开源推理服务框架的架构演讲趋势和特性使用体验
  2. MindSpore大模型推理加速技术的发展方向和改进点讨论
  3. 大模型推理加速技术的新兴技术、开发经验、应用建议
  4. SIG特性开发任务介绍与成果展示等
* 分享嘉宾：任何SIG成员，包括高校师生、业界专家、开发者均可
* 组织者：各位Contributors轮流组织

### 2. vLLM-MindSpore特性开发

* 活动定位：共同参与vLLM-MindSpore特性开发，打造功能完善、敏捷演进的大模型推理框架
* 活动形式：定期发布大颗粒特性开发任务，招募开发者共同参与，完成者可获得奖品或者实习工资、实习证明
* 活动频率：每季度发布/刷新任务
* 活动内容：待讨论完善
* 组织者：各技术领域Contributors

### 3. 资料与产品体验改进活动

* 活动定位：开展产品体验活动，收集建议及体验评价，持续提升资料与产品综合体验
* 活动形式：开发者通过提交issue/PR形式提出问题建议或修改，累积积分获得奖品
* 活动频率：不定期举行
* 活动规划：
  1. 资料体验：分期系列活动，针对官网上线的视频、教程及API等内容，开展众测体验活动
  2. 产品体验：随新发布版本进行，针对版本发布的功能特性开展体验活动

### 4. 例会

* 时间：周三或周四晚上19点，每2周开展一次
* 例会内容：面向SIG特性开发和组织管理工作，进行开放式的例行交流
* 例会议题：
  1. 固定议题：SIG成员领取的特性开发任务进展与问题交流
  2. 选报议题：特性开发阶段性成果演示
  3. 选报议题：SIG组织管理(如运作规则讨论、Maintainers&Commiters担任人员及职责刷新）
* 组织者：各位Contributors和核心开发者轮流组织

## SIG组织管理

### 成员身份说明

SIG的成员身份包括Members、Contributors、Maintainers，各角色的描述和申请条件如下：

#### Members(正式成员）

* 权益：参与SIG的各项活动与交流
* 申请条件：填写SIG成员申请表(加入微信交流群时发放）

#### Committers(核心贡献者）

* 职责：牵头负责技术开发、日常运营、宣传推广、活动组织等领域某一特定方向的规划、组织与管理工作
* 权益：事迹录入SIG荣誉殿堂，并在申请MindSpore布道师或资深布道师时具有优先权
* 申请条件：已经成为Members，有意愿负责某一特定方向并制定出工作方案，并在SIG例会上经过其他Maintainers与Contributors多数通过。

#### Maintainers(负责人）

* 职责：负责SIG的总体规划与策略制定，把握SIG发展方向、审核重点工作方案
* 权益：事迹录入SIG荣誉殿堂，优秀Maintainers有机会成为MindSpore TSC(技术委员会）成员
* 申请条件：已经成为Contributors一年以上，在所负责领域有突出贡献，获得至少一位Maintainers推荐，并在SIG例会上经过其他Maintainers与Contributors多数通过。