## SIG简介

三方芯片SIG目标：
生态建设：与三方芯片厂商共同构筑MindSpore南向芯片生态（CPU/GPU/NPU/FPGA/x86/arm等），繁荣MindSpore社区，提升社区影响力
标准化：芯片厂商共同参与接口/IR的标准化建设。
商业合作：与芯片厂商形成合作关系，培养合作伙伴/ISV等，面向AI计算中心，共同构建创新应用。
竞争力特性：三方芯片厂商软件基础较弱，接入MindSpore之后，可快速使用MindSpore的关键核心特性，如自动并行、Pynative、动静统一等，通过SIG可让芯片厂商快速了解MindSpore的特性。

## SIG代码仓

1.待创建

## Maintainers

- 王珏（中科院计算机网络中心，副研究员）
- 郭琦 （华为MindSpore架构师，SIG发起人）

## Contributors

- 翟智强（华为MindSpore架构师，负责推理芯片对接接口设计及训练推理接口统一）
- 周峰（华为MindSpore资深开发者，负责南向整图执行接口的设计开发）
- 赖勇强（华为MindSpore资深开发者，负责南向算子执行接口的设计开发）
- 田野（燧原编译器团队软件总监，负责DSA架构类芯片接口标准，以及标准在燧原芯片的应用）（已沟通，待答复）
- 王黎阳（天数智芯市场部负责人，负责GPGPU架构类芯片接口标准，以及标准在天数智芯芯片上的应用）（已沟通，待答复）

## 2022年目标

1. 组织管理：制定SIG组织管理规范，邀请Maintainers与Contributors初始成员参与SIG运作（2名Maintainers + 至少8名Contributors）；
2. 生态拓展：发展5+芯片企业或高校成为MindSpore的企业贡献者，共同参与MindSpore南向生态构建。
3. 特性开发：MindSpore开发团队与SIG组共同完成南向统一接口定义，支持5+训练芯片和10+推理芯片的对接工作；
4. 活动开展：以南向统一接口标准为主要技术方向，由各参与企业/高效轮值主持，全年开展8+次技术主题研讨；

## 主要活动

### 1. 线上技术研讨

- 活动定位：共同探讨南向统一接口标准的相关话题
- 活动形式：定期邀请业界专家、高校师生、资深开发者分享话题
- 活动频率：每1个月1次，每次围绕同一个共同主题进行研讨
- 分享范围：与南向统一接口标准技术领域相关的技术话题，包括但不限于：

  标准化：
      南向接口的标准化讨论
      CPU/GPU/NPU等硬件抽象建模
      IR的标准与对接流程的规范化
  异构融合：
      跨芯片异构支持形态/运行时讨论
      前端芯片选择的用户接口讨论
  芯片架构：
      AI硬件发展方向讨论
      面向不同芯片的编程规范
- 分享嘉宾：任何SIG成员，包括高校师生、业界专家、开发者均可
- 组织者：由各参与企业/高效轮值主持

### 2. 特性开发

- 活动定位：共同参与第三方芯片适配特性开发，打造多芯一生态的AI框架
- 活动形式：定期发布大颗粒特性开发任务，招募开发者共同参与，完成者可获得奖品或者实习工资、实习证明
- 活动频率：每季度发布/刷新任务
   算子编译流程对接、自定义算子对接、AOT算子库对接
- 组织者：各技术领域Contributors

### 3. 周例会

- 时间：周六或周日晚上7点，每1-2周开展一次
- 例会内容：面向SIG特性开发和组织管理工作，进行开放式的例行交流
- 例会议题：
  1. 固定议题：SIG成员领取的特性开发任务进展与问题交流
  2. 固定议题：南向标准讨论与接口规范定义
  3. 选报议题：特性开发阶段性成果演示
  4. 选报议题：SIG组织管理（如运作规则讨论、Maintainers&Contributors担任人员及职责刷新）
- 组织者：各位Contributors和核心开发者轮流组织

## SIG组织管理

### 成员身份说明

SIG的成员身份包括Members、Contributors、Maintainers，各角色的描述和申请条件如下：

#### Members（正式成员）

- 权益：参与SIG的各项活动与交流
- 申请条件：填写SIG成员申请表（加入微信交流群时发放）

#### Contributors（核心贡献者）

- 职责：牵头负责技术开发、日常运营、宣传推广、活动组织等领域某一特定方向的规划、组织与管理工作
- 权益：事迹录入SIG荣誉殿堂，并在申请MindSpore布道师或资深布道师时具有优先权
- 申请条件：已经成为Members，有意愿负责某一特定方向并制定出工作方案，并在SIG例会上经过其他Maintainers与Contributors多数通过。

#### Maintainers（负责人）

- 职责：负责SIG的总体规划与策略制定，把握SIG发展方向、审核重点工作方案
- 权益：事迹录入SIG荣誉殿堂，优秀Maintainers有机会成为MindSpore TSC（技术委员会）成员
- 申请条件：已经成为Contributors一年以上，在所负责领域有突出贡献，获得至少一位Maintainers推荐，并在SIG例会上经过其他Maintainers与Contributors多数通过。

## 近期活动与例会预告

1. 技术分享会
2. SIG例会

## 往期活动与例会
