## SIG简介

AI Security SIG 聚焦于AI模型开发项目中从数据处理到模型训练再到部署推理过程中的安全问题。具体包括以下几点：

1. **模型鲁棒性和可靠性**：AI模型对于对抗样本、自然扰动样本的推理鲁棒性、数据概念漂移检测、模型故障注入评估。
2. **隐私保护**：差分隐私、联邦学习等隐私保护训练算法。
3. **模型部署安全**：模型加密、模型混淆等技术。

## SIG代码仓

1. [MindAarmour](https://gitee.com/mindspore/mindarmour)
2. [联邦学习云侧](https://gitee.com/mindspore/mindspore/tree/master/mindspore/ccsrc/fl) 、[联邦学习端侧](https://gitee.com/mindspore/mindspore/tree/master/mindspore/lite/java/java/fl_client/src/main/java/com/mindspore/flclient)

## SIG负责人

* Wang Ze (Huawei)
* Xiulang (Huawei)

## 成员说明

AI Security SIG的成员身份包含Members、Reviewers、Committers、Maintainers，并且记录在[SIG名单](./sig_members.yaml)中，各角色的描述和申请条件如下：

### Members

* SIG正式成员，可参与SIG的日常讨论和活动。
* 申请条件：至少参加过2次SIG会议/活动。

### Reviewers

* SIG代码仓的代码reviewer，负责代码仓PR(pull requests)的review工作。
* 申请条件：身份为Members，且至少review过[MindSpore主仓](https://gitee.com/mindspore/mindspore/pulls) 或者[MindArmour仓](https://gitee.com/mindspore/mindarmour/pulls) 的2个PR，在PR中发表的修改评论总数为10个以上。

### Committers

* SIG代码仓的Committer，拥有代码仓PR的合入权限。
* 申请条件：身份为Reviewers，且至少往**SIG代码仓**中合入5个PR。

### Maintainers

* SIG运作的负责人，负责整个SIG的技术研究方向和活动组织。
* 申请条件：身份为Committers，通过Maintainers资格评审。

### 申请方式

1. Fork [Community仓库](https://gitee.com/mindspore/community) 。
2. 提交PR，把自己的Gitee主页链接、名字（不要求真名）、注册Gitee的邮箱加到[sig_members](./sig_members.yaml)中，PR的描述中需要附加申请的证明，例如评论过的PR、提交合入过的PR等等。提交PR之后，Maintainers会进行审核。

## 近期活动预告

## 往期会议

* [会议录屏](https://www.bilibili.com/video/BV14g411V7nZ?spm_id_from=333.999.0.0)
* [2022-3-15会议预告](https://mp.weixin.qq.com/s/NCw-kdQiTGXhH1BNrPiFkQ)
* [Thursday June 04, 2020](./meetings/001-20200604.md)
* [Friday July 03, 2020](./meetings/002-20200703.md)
* [Saturday August 08, 2020](./meetings/003-20200808.md)
* [Friday September 04, 2020](./meetings/004-20200904.md)
