# DX SIG治理章程

该Charter内容遵循MindSpore Open Governance [governance.md](https://gitee.com/mindspore/community/blob/master/governance.md) 描述的约定，本文会根据需要进行更新，以满足MindSpore Open Governance的需求。  

为了使社区席位设置规范化和标准化，让社区参与者更好的融入社区，DX SIG 社区席位设置应该遵循以下准则：  

## SIG maintainers

DX SIG成立之初，为引导社区发展，设置SIG Lead角色，作为初始maintainer，名单如下：  

  - 曹健 @JianCao81
  - 李自 @clement_li

为了更好服务社区开发者，DX SIG在8月例会中增选3位maintainer，名单如下：  

  - 赵博宣 @BoxuanZhao 
  - 夏文宗 @WenzongXia 
  - 朱乃盘 @zhunaipan （因原当选人王晔晖申请不再担任maintainer，由朱乃盘增补）

SIG组的maintainer来自不同的地区、高校、公司，根据背景不同也有着不同的职责，但所有的maintainer都有着共同点：  

  - 他们对项目的成功负有共同的责任。
  - 他们花费大量的时间来改进项目。
  - 他们花费时间做任何需要做但不一定是最有趣的事情。

Maintainer经常因为他们所做的工作不太明显而被低估。往往作为技术专家识别技术点是很简单的（例如改进代码），但维护文档、以整体角度评估系统可靠性往往是比较难的（做架构设计、开发者指导），而这些却是一个伟大的项目和一个好项目的根本区别。  

## 增加 maintainers

Maintainer首先是长期活跃在社区的贡献者。贡献者通过不少于三个月的代码贡献、代码审查、issue讨论分类来获得maintainer提名资格。  

但仅靠贡献并不能使贡献者成为maintainer。其还需要赢得当前maintainer和其他项目贡献者的信任，其决定和行动需要符合项目的最大利益。  

现有的maintainer会定期整理一份贡献者名单，这些贡献者在过去几个月中在项目上表现出定期活动。 从这个列表中，选择maintainer候选人并在maintainer邮件列表中提名。  

在SIG Slack、社区Issue上提名候选人后，现有maintainer将在接下来的 **5个工作日内** 讨论候选人，提供反馈并投票。新提名maintainer至少需要获得 **超过半数(>50%)** 的当前维护者的赞成票。  

如果候选人获得批准，maintainer会联系候选人，邀请他们建立将贡献者添加到该文档中并提交PR。 当PR被合并后，候选人将成为maintainer。  

## 移除 maintainers

Maintainer可以根据本人的自愿放弃请求或者在项目中无法有效履行maintainer职责而被移除权限。  

### 自愿放弃

由于兴趣和热情等因素的改变，当前maintainer自觉无法/无意愿继续行使maintainer职责的可告知其他maintainer其自愿放弃maintainer席位。  
放弃者应尽可能帮助社区寻找接任者，其至少需要确保社区的工作不至于因其离开而中断。

### 无法有效履行maintainer职责
  
Maintainer代表会定期审查所有maintainer在过去三个月中的社区活动。如果现有maintainer在项目中长期没有表现出重要的活动，则可以考虑将其移除。  

Maintainer代表由所有maintainer轮值，轮值期三个月。  

如果maintainer在此期间表现出的活动不足，maintainer代表将联系相关者，询问他们是否想继续担任maintainer。 如果其决定退出maintainer队伍，maintainer代表将建立PR将其从 OWNERS 文件中删除。  

如果该maintainer想继续担任此角色，但无法履行所需职责，则可以通过至少 **超过半数(>50%)** 的当前maintainer的赞成票来将其移出，讨论中的维护者将不被允许投票。  

投票可通过maintainer邮件列表来邀请SIG组的maintainer参与，投票期为五个工作日。  

与讨论中的maintainer的表现相关的问题应该在投票过程中与其他maintainer讨论，所有的讨论应该客观地处理，不准人身攻击。  

## 社区决策

MindSpore核心项目和SIGs都是具有开放设计理念的开源项目。这意味着代码仓是项目和SIG组理念、设计、发展规划等各个方面的真实来源。  

因此，每个决定都可以表示为代码仓的更改。  

所有影响DX SIG的决策，无论大小，都遵循相同的步骤：  

  - **第 1 步**：建立PR。 任何人都可以做到这一点。  

  - **第 2 步**：讨论PR。 任何人都可以做到这一点。  

  - **第 3 步**：MindSpore Community Owners合并、关闭或拒绝PR。  

PR由DX SIG的当前maintainer审查。  