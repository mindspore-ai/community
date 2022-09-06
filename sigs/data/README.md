## SIG简介

数据SIG（DATA SIG） 聚焦于MindSpore框架中的数据处理模块，致力于为MindSpore提供更丰富、灵活、易用的数据操作能力，方便用户随心所欲“把玩”手中的数据，并接入到MindSpore中进行训练。

数据处理模块：支持更多业界基准数据集一键读取，支持业界常用的、最新的数据预处理操作。主要负责将用户的数据高效读取到MindSpore框架，然后执行相关的数据增强操作（调整大小、旋转、混洗、批处理...），最终将数据集提供给训练过程。
数据格式模块：支持聚合存储、高效读取的数据格式MindRecord，实现数据统一存储、访问，使得训练时数据读取更加快速。同时MindRecord支持灵活控制数据切分和高效索引，可以支持超大规模的分布式训练场景。

## SIG代码仓

1. [代码仓](https://gitee.com/mindspore/mindspore)
2. [Data SIG工作目录](https://gitee.com/mindspore/community/tree/master/sigs/data)

## Maintainers

* Luoyang   （华为MindSpore开发者体验专家，SIG Lead，负责数据处理模块技术领域总体规划、发展布道师）
* Xiaotianci（华为MindSpore数据专家，负责MindSpore数据模块关键问题的识别与改进）

## Contributors

* Jony 2015 （华为资深架构师，MindSpore AI数据处理技术专家，负责数据模块的技术能力规划与构建）

## 2022年目标

1. 组织管理：制定SIG组织管理规范，邀请高校成员、招募开发者参与SIG运作（2名Maintainers + 至少8名Contributors）；
2. 生态拓展：发展50+位DATA SIG成员，其中重点发展5位资深开发者、10位优秀开发者；
3. 特性开发：在数据处理模块中规划2+个新特性，并发布任务，招募开发者共同设计开发；
4. 活动开展：组织DATA模块教程体验活动、文档检视和改进活动、特性体验与反馈活动，收集改进建议200+，征集技术文章50+；

## 主要活动

### 1. 线上技术/特性分享会

* 活动定位：分享MindSpore数据处理模块的技术和特性，促进开发者深入使用MindData。
* 活动形式：邀请内部开发专家、社区开发者、高校师生分享话题
* 活动频率：每1-2个月1次，每次围绕同一个共同主题分享3-4个话题
* 分享范围：相关的技术话题，包括但不限于：
 1. MindData常用特性/新特性介绍与演示；
 2. MindData特性改进建议、特性需求收集、使用体验反馈；
 3. MindData学习心得、开发经验、使用建议
 5. MindData开发任务分发、设计评议、开发讨论、验收颁奖等。
* 分享嘉宾：任何SIG成员，包括高校师生、业界专家、开发者均可

### 2. MindData特性/基础架构开发

* 活动定位：共同参与MindData架构开发，丰富数据处理能力，提升数据处理模块的易用性。
* 活动形式：定期发布大颗粒特性开发任务，招募开发者共同参与，完成者可获得奖品或者实习工资、实习证明
* 活动频率：每季度发布/刷新任务
* 现有相关任务：
  1. [DATA SIG开源实习任务](https://gitee.com/mindspore/community/issues/I55ET9)

### 3.资料改进活动

* 活动定位：降低MindData入门门槛，令开发者能够快速上手，由浅到深了解到数据处理模块提供的能力。
* 活动形式：组织教程体验活动、文档检视和改进活动、特性体验与反馈活动，开发者通过在技术分享会，或提交issue/PR形式提出问题建议或修改，累积积分获得奖品
* 活动频率：不定期举行

### 4. 周例会

* 时间：周六或周日晚上7点，每1-2周开展一次
* 例会内容：面向SIG特性开发和组织管理工作，进行开放式的例行交流
* 例会议题：
  1. 固定议题：SIG成员领取的特性开发任务进展与问题交流
  2. 选报议题：特性开发阶段性成果演示
  3. 选报议题：SIG组织管理（如运作规则讨论、Maintainers&Contributors担任人员及职责刷新）
* 组织者：各位Contributors和核心开发者轮流组织
* 轮值表：SIG核心成员轮值组织

## SIG组织管理

SIG的成员身份包括Members、Contributors、Maintainers，各角色的描述和申请条件如下：

## #Members（正式成员）

* 权益：参与SIG的各项活动与交流
* 申请条件：填写SIG成员申请表（加入微信交流群时发放）

### Contributors（核心贡献者）

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

[2021 MindSpore Data SIG Meeting](https://www.bilibili.com/video/BV1m64y12741)

[2021 MindSpore | MindData Overview](https://www.bilibili.com/video/BV1YK411c7dM)

[2020 MindInsight MindData联合例会](https://www.bilibili.com/video/BV1U54y1i717)

[2020 五一两日集训营 MindSpore数据处理详解](https://www.bilibili.com/video/BV1RZ4y1W7FL)

[2020 MindSpore Data SIG Meeting](https://www.bilibili.com/video/BV1dt4y1m7tX)
