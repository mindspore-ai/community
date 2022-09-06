## SIG简介

编译器SIG（Usability SIG）以“易用语法表达，丰富接口支持，极致编译性能，最佳编程体验”为愿景，助力开发者更高效的使用MindSpore。

## 总目标

持续提升MindSpore编译器前端框架的易用性，实现动静统一，提高编译性能。

1. 持续提升MindSpore前端框架的易用性，实现动静统一分析并解决MindSpore框架静态图的语法限制，实现MindSpore框架的动静态语法的统一。 使用户可以以更灵活，更自由的方式构建网络。
2. 控制流：支持度+性能
3. 持续优化编译性能不断提升编译器前端的编译性能，提高框架的竞争力。

## 年度目标

1. 优化MindSpore编译器前端框架：

   A. 静态图语法支持度从63%提升至70%以上

   B. 控制流完善和性能提升。执行、编译性能的提升

   C. 典型网络编译性能提高15%

2. 组织管理：制定SIG组织管理规范，邀请Maintainers与Contributors初始成员参与SIG运作。

3. 生态拓展：发展30+位SIG正式成员，发展5位优秀开发者, 共同进行特性和案例开发建设；

4. 活动开展：开展技术分享活动直播4次，征集15篇技术文章、开发案例；

## 关键落地技术

1. 动静统一，通过JIT Fallback等方式，完善静态图语法支持度。
2. 控制流IR表达重构，完善控制流使用场景，提升控制流性能。

## Maintainers

* Zhang Qinghua (华为资深前端架构师)

## Contributors

* zibo (@liangzhibo), SIG Contributor, MindSpore Compiler前端工程师，负责：自动微分，语法解析
* YGrey (@huanghui), SIG Contributor, MindSpore Compiler前端工程师，负责：DFX， 语法解析
* RayWang (@wangrui), SIG Contributor, MindSpore Compiler前端工程师，负责：副作用，Jit Fallback。
* ME 打杂店小二（@lianliguang）SIG Contributor, MindSpore Compiler前端工程师，负责: MindIR导入导出，语法支持
* Joker（@huangbingjian）SIG Contributor, MindSpore Compiler前端工程师，负责: 图优化，动静统一
* KinFung（@yujianfeng）SIG Contributor, MindSpore Compiler前端工程师，负责自动微分
* Felix (@chenfei): Contributor, MindSpore Compiler前端工程师，负责控制流。

## 主要活动

### 1. 例会

* 时间：周一晚上7点，每月开展一次
* 例会内容：面向SIG特性开发和组织管理工作，进行开放式的例行交流
* 例会议题：
  1. 固定议题：SIG成员领取的特性开发任务进展与问题交流
  2. 选报议题：特性开发阶段性成果演示
  3. 选报议题：SIG组织管理（如运作规则讨论、Maintainers&Contributors担任人员及职责刷新）
* 组织者：各位Contributors和核心开发者轮流组织

### 2. 技术分享

* 活动定位：共同探讨MindSpore编译器前端相关话题
* 活动形式：定期邀请业界专家、高校师生、资深开发者分享话题
* 活动频率：每季度一次，每次围绕同一个共同主题分享3-4个话题
* 分享嘉宾：任何SIG成员，包括高校师生、业界专家、开发者均可
* 组织者：SIG Compiler的Maintainers及Contributors

### 3. 不定期会议

当出现问题需要及时解决，问题责任人发起issue/召集会议。

## SIG组织管理

### 成员身份说明

SIG的成员身份包括Members、Reviewers、Committers、Maintainers，各角色的描述和申请条件如下：

#### Members（正式成员）

* 职责：参与SIG的各项活动与交流
* 申请条件：至少参加过1次SIG会议/活动

#### Reviewers（核心贡献者）

* 职责：牵头负责技术开发、日常运营、宣传推广、活动组织等领域某一特定方向的规划、组织与管理工作
* 申请条件：身份为Members，且至少review过[MindSpore主仓](https://gitee.com/mindspore/mindspore/pulls)编译器前端相关的两个PR，或者在编译器相关PR中发表的修改评论总数为10个以上。

#### Committer （代码提交者）

* 职责：SIG代码仓的Committer，拥有代码仓PR的合入权限。
* 申请条件：身份为Reviewers，通过committer资格审核。

#### Maintainers（负责人）

* 职责：SIG运作的负责人，负责整个SIG的技术研究方向和活动组织。
* 申请条件：身份为Committer，通过Maintainer资格审核。

