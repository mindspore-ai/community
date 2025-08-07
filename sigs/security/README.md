## SIG简介

MindSpore Security & Trusted AI SIG包含以下两个方向：

1. **MindSpore Security**：MindSpore Security负责接受和响应MindSpore相关的安全问题报告、提供社区安全编码以及规范的指导、进行社区安全编码的评审，制定和决策，开展社区安全治理。

2. **Trusted AI**：聚焦于人工智能领域的模型、数据可信技术，致力于打造安全可靠的AI计算框架。

## MindSpore Security & Trusted AI SIG职责

### MindSpore Security

* 协助漏洞修复：及时响应修复已知漏洞。帮助用户系统在成为攻击受害者之前进行漏洞修复，包括提供相关漏洞检测和修复工具。
* 响应安全问题：响应上报的安全问题。用户通过[MindSpore安全中心](https://www.mindspore.cn/security)中的安全流程上报安全问题，SIG积极响应上报的安全问题，跟踪安全问题的处理进展，并遵循安全问题披露策略对安全问题在社区内进行披露和公告。
* 安全编码规则：普及安全编码知识是安全团队的目标。安全团队会努力创建文档（[c++编码规范](https://gitee.com/mindspore/community/blob/master/security/coding_guild_cpp_zh_cn.md)和[python编码规范](https://gitee.com/mindspore/community/blob/master/security/coding_guild_python_zh_cn.md)）或开发工具来帮助开发团队避免软件开发过程中的常见陷阱。安全团队还会尝试回答在开发和使用过程中遇到的任何问题。
* 参与代码审核：安全团队希望能够通过代码审核帮助团队提前发现代码中的漏洞。

### Trusted AI

Trusted AI 聚焦于人工智能领域的模型、数据可信技术，致力于打造安全可靠的AI计算框架，主要包括以下几个方向：

1. **模型鲁棒性和可靠性**：对抗样本、对抗训练、AI可解释、数据概念漂移检测、模型故障注入评估。
2. **隐私保护**：差分隐私训练、联邦学习、数据脱敏、隐私泄露评估。
3. **模型部署安全**：模型加密、模型混淆等技术。

## 代码仓

1. [MindArmour](https://gitee.com/mindspore/mindarmour)
2. [MindSpore社区](https://gitee.com/mindspore)

## SIG成员

### Maintainer

* 杨渊[@yyuse](https://gitee.com/yyuse), *yangyuan24@huawei.com*，Trusted AI & MindSpore Security

### Committer

* 鲍翀[@baochong](https://gitee.com/baochong), *zjbc123@sina.com*，MindSpore Security
* 陈一杰[@chenyijie6](https://gitee.com/chenyijie6), *chenyijie6@huawei.com*，MindSpore Security
* 郭琦[@guoqi1024](https://gitee.com/guoqi1024), *guoqi5@huawei.com*，MindSpore Security
* 韩志斌[@ZhibinHan](https://gitee.com/ZhibinHan), *hanzhibin1@huawei.com*，MindSpore Security
* Kewei[@qmckw](https://gitee.com/qmckw), *2512235663@qq.com*，Trusted AI
* 刘崇鸣[@liuchongming74](https://gitee.com/liuchongming74), *liuchongming1@huawei.com*，MindSpore Security
* Mr. Hu[@Mr_GerhardtHu_Fox](https://gitee.com/Mr_GerhardtHu_Fox), *780308144@qq.com*，Trusted AI
* Mr. Li[@limingjun1](https://gitee.com/limingjun1), *NA*，Trusted AI
* Rice Zhang[@hu2175](https://gitee.com/hu2175), *8623924@qq.com*，Trusted AI
* 张兆创[@tronzhang](https://gitee.com/tronzhang), *zhangzhaochuang@huawei.com*，MindSpore Security

### Contributor

* 胡思航[@siriushsh](https://gitee.com/siriushsh), *siriushsh@foxmail.com*，MindSpore Security
* Mr. Zhang[@shazi4399](https://gitee.com/shazi4399), *NA*，Trusted AI

## SIG的主要活动

### １，线上技术讨论

主要内容：MindSpore安全流程讨论，AI安全技术分享讨论等

负责人：Maintainers、Committers轮流组织

### 2，会议时间(双周例会)

时间：每双周二上午9:30~10:30，通过视频会议召开。

例会内容：议题收集后根据议题进行讨论，如安全编码评审、论文分享、技术调研等

例会记录：https://etherpad.mindspore.cn/p/meetings-Trusted_AI

负责人：Maintainers、Committers轮流组织

### 3，开发任务发放

[开源实习任务](https://gitee.com/mindspore/community/issues/I557F6)

时间：每季度一次

负责人：Maintainers、Committers

### 4，晋升选拔

时间：半年一次

内容：选拔Committers、Maintainers

负责人：Maintainers

## 往期会议

* [会议录屏](https://www.bilibili.com/video/BV14g411V7nZ?spm_id_from=333.999.0.0)
* [2022-3-15会议预告](https://mp.weixin.qq.com/s/NCw-kdQiTGXhH1BNrPiFkQ)
* [Thursday June 04, 2020](./meetings/001-20200604.md)
* [Friday July 03, 2020](./meetings/002-20200703.md)
* [Saturday August 08, 2020](./meetings/003-20200808.md)
* [Friday September 04, 2020](./meetings/004-20200904.md)

## 成员说明

MindSpore Security & Trusted AI SIG的成员身份包含Contributors、Committers、Maintainers，并且记录在[SIG名单](./sig_info.yaml)中，各角色的描述和申请条件如下（详细可以查阅官网[角色说明](https://www.mindspore.cn/sig/role-description)）：

### Contributors

* 职责：响应被分配的问题和PR，可以分配问题或PR。
* 申请条件：Gitee上的注册会员，为SIG或社区做出多方面贡献，熟悉贡献流程，积极参与1个或多个SIG。

### Committers

* 职责：评审PR，分发处理问题，跟踪依赖性问题。
* 申请条件：作为Contributor至少3个月，作为主要审阅者至少参与了6次PR的审阅，审阅或者合并至少20个基本PR到代码库，熟悉代码库。可以自我提名，或由该SIG的审核者或维护者提名。

### Maintainers

* 职责：负责SIG的总体规划与策略制定，把握SIG发展方向、审核重点工作方案
* 申请条件：作为Committer至少3个月，作为主要审阅者至少参与了12次PR的审阅，审阅或合并至少30个基本PR到代码库，熟悉代码库。可以自我提名，也可以由子项目Maintainer提名，并且没有其他子项目Maintainer的反对。

### 申请方式

1. Fork [Community仓库](https://gitee.com/mindspore/community) 。
2. 提交PR，把自己的Gitee主页链接、名字（不要求真名）、注册Gitee的邮箱以及兴趣方向加到[SIG名单](./sig_info.yaml)中，PR的描述中需要附加申请的证明，例如评论过的PR、提交合入过的PR等等。提交PR之后，Maintainers会进行审核。
