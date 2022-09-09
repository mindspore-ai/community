## SIG简介

Parallel SIG 聚焦于利用分布式并行技术加速AI大模型训练和推理。具体包括以下几点：

1. **数据并行（Data Parallel）**：对数据进行切分的并行模式，一般按照batch维度切分，将数据分配到各个计算单元（worker）中，进行模型计算。
2. **模型并行（Model Parallel）**：对模型进行切分的并行模式。模型并行可分为：算子级模型并行、流水线模型并行、优化器模型并行等。
3. **混合并行（Hybrid Parallel）**：指涵盖数据并行和模型并行的并行模式。如何自动地找到最佳的并行方式来加速模型的训练和推理，是所有并行策略的终极目标。

SIG为上述领域的专家、爱好者提供了一个交流、合作的平台。我们的愿景是打造根植于MindSpore的世界领先的分布式并行技术。Parallel SIG的目标有两个：

1. 通过自动并行持续提升MindSpore分布式训练易用性及性能。
2. 助力MindSpore构建业界领先的大模型训练推理能力。

## SIG代码仓

1. [Parallel SIG](https://gitee.com/mindspore/community/tree/master/sigs/parallel)

## Maintainers

* Li Cheng （中国科学技术大学特任研究员）
* Su Teng （华为MindSpore副首席专家，SIG发起人）

## Contributors

* jiahongQian（@jiahongQian，SIG Lead与组织者，负责：活动组织，共享参数预训练特性开发）
* Xiaoda（@zhangxiaoda，SIG Contributor，MindSpore资深算法工程师，负责：MoE路由策略特性开发）
* wangshengnan123（@wangshengnan123，SIG Contributor，MindSpore AI工程技术专家，负责：负责近似计算特性开发）
* youhui（@Bert0108，MindSpore AI工程技术专家）

## 2022年目标

1. 组织管理：完善SIG组织，邀请Maintainers （2名）与Contributors（至少5名）初始成员参与SIG运作；
2. 特性开发：在自动并行领域路由策略和网络训练加速等方向中增加至少3个新特性并招募开发者共建；
3. 活动开展：开展技术分享活动直播4次, 征集分布式并行领域技术文章10+；

## 主要活动

### 1, 线上技术分享

* 活动定位：交流自动并行领域的最新进展
* 活动形式：定期邀请业界专家、高校师生、资深开发者分享话题
* 活动频率：每2-3个月1次，每次围绕同一个共同主题分享3-4个话题
* 分享范围：与自动并行领域相关的技术话题，包括但不限于：
  1. MindSpore在自动并行领域上的最新进展
  2. 学术界在自动并行领域上的最新进展
  3. 自动并行在大模型上的应用案例
  4. 开发者学习心得、开发经验、使用建议
  5. SIG特性开发任务介绍与成果展示等
* 分享嘉宾：任何SIG成员，包括高校师生、业界专家、开发者均可
* 组织者：各位Contributors轮流组织

### 2，特性开发任务

* 活动定位：共同参与易用性特性开发，打造易学易用、灵活高效的AI框架

① [开源实习任务](https://gitee.com/mindspore/community/issues/I55XXN?from=project-issue)

时间：每季度一次

负责人：Maintainers、Committers

### 3，月例会（双月例会）

时间：下午3点

例会内容：①对齐SIG成员领取的开发任务进度；②SIG成员论文分享；③赋能

任务认领情况：

|SIG/特性组| 题目 | 分值 | 预期完成时间 |开发语言| 详情链接 | 任务状态 |任务认领人|
|-----| -------- | ---------------- | -------- | --- | --- |---|---|
|Parallel SIG| 共享参数预训练初始化|50| 2022-8-31 |C++、Python| [详情](https://gitee.com/mindspore/community/issues/I55XVX)|未认领|-|
|Parallel SIG| 通过FFN近似计算实现Transformer网络训练加速|50| 2022-8-31 |Python|[详情](https://gitee.com/mindspore/community/issues/I55XVP)|未认领|-|
|Parallel SIG| 通过attention近似计算实现Transformer网络训练加速|50| 2022-8-31 |Python| [详情](https://gitee.com/mindspore/community/issues/I55XVN) |未认领|-|
|Parallel SIG| MoE（混合专家）中路由策略(optimal_transport路由策略)实现|50| 2022-8-31 |Python| [详情](https://gitee.com/mindspore/community/issues/I55XVN) |未认领|-|
|Parallel SIG| MoE（混合专家）中路由策略(hashing路由策略)实现|50| 2022-8-31 |Python| [详情](https://gitee.com/mindspore/community/issues/I55XUW) |未认领|-|
|Parallel SIG| MoE（混合专家）中路由策略(ntlb路由策略)实现|50| 2022-8-31 |Python| [详情](https://gitee.com/mindspore/community/issues/I55XUD) |未认领|-|

负责人：Maintainers、Committers轮流组织。

轮值表：jiahongQian、Xiaoda、wangshengnan123、youhui

## SIG组织管理

### 成员身份说明

SIG的成员身份包括Members、Contributors、Maintainers，各角色的描述和申请条件如下：

#### Members（正式成员）

* 权益：参与SIG的各项活动与交流
* 申请条件：填写SIG成员申请表（加入微信交流群时发放）

#### Contributors（核心贡献者）

* 职责：牵头负责技术开发、日常运营、宣传推广、活动组织等领域某一特定方向的规划、组织与管理工作
* 权益：事迹录入SIG荣誉殿堂，并在申请MindSpore布道师或资深布道师时具有优先权
* 申请条件：已经成为Members，有意愿负责某一特定方向并制定出工作方案，并在SIG例会上经过其他Maintainers与Contributors多数通过。

#### Maintainers（负责人）

* 职责：负责SIG的总体规划与策略制定，把握SIG发展方向、审核重点工作方案
* 权益：事迹录入SIG荣誉殿堂，优秀Maintainers有机会成为MindSpore TSC（技术委员会）成员
* 申请条件：已经成为Contributors一年以上，在所负责领域有突出贡献，获得至少一位Maintainers推荐，并在SIG例会上经过其他Maintainers与Contributors多数通过。

## 近期活动与例会预告

1. 技术分享会
2. SIG例会

## 往期活动与例会

* [2022年3月16日：MindSpore的并行策略详解](https://mp.weixin.qq.com/s/ENi8sbghtIEcQFnGpWVEXg)