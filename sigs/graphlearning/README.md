## 加入Graph Learning SIG，共同打造高效易用的图学习库

由于图数据结构的强大表现力，用机器学习分析图越来越受到重视，成为各大AI顶会的研究热点。近年来，图机器学习应用于网络数据分析、推荐系统、分子计算、知识图谱和组合优化都取得了新的突破。在推荐场景，图学习被用于高效表征实时交互数据，引领了实时流推荐模式发展；在药物发现场景，图学习成为药物分子表征的基础模型；在芯片设计场景，Google已证明应用GNN建模芯片网表图可实现晶片单元的优化布置。这些案例都证明了图学习方法的有效性和潜在价值。

不同于CV和NLP领域深度学习框架和领域库发展趋于成熟，图学习领域尚未有一个稳定易用的模型库或社区，使算法研究者能快速实验算法，使应用开发者能高效训练和部署模型。

因此，类比transfomer方法的领域库Huggingface，构建开放，易用，高效的图学习库有利于促进图学习研究的蓬勃发展和图学习方法应用于其他领域的创新突破。
为此，昇思Graph Learning专项兴趣小组(简称：Graph Learning SIG)正式成立，并面向开源社区招募志同道合的伙伴。

## Graph Learning SIG

### 1. SIG简介

Graph Learning SIG 聚焦于图计算、图学习方向最新技术和应用，主要包括以下几个方向：

1. 算法演进：随机游走、图神经网络、知识图谱、双曲图神经网络
2. 图框架优化及演进：大规模图分布式、异构图学习优化、时序图学习优化
3. 图学习应用场景：分子计算、搜索推荐

### 2. SIG 代码仓

[MindSpore Graph Learning] http://gitee.com/mindspore/graphlearning

### 3. SIG 成果

MindSpore Graph Learning

由香港中文大学的James Cheng教授团队和华为MindSpore团队基于MindSpore共同构建的图学习框架，尝试从易用性，高性能的角度寻求突破，创新性的提出了以点为中心的编程范式和针对图学习的编译优化策略。

图神经网络模型需要在给定的图结构上做信息的传递和聚合，整图计算无法直观表达这些操作。MindSpore Graph Learning提供以点为中心的编程范式，更符合图学习算法逻辑和Python语言风格，可以直接进行公式到代码的翻译，减少算法设计和实现间的差距。

结合MindSpore的图算融合和自动算子编译技术（AKG）特性，MindSpore Graph Learning自动识别图神经网络任务特有执行pattern进行融合和kernel level优化，能够覆盖现有框架中已有的算子和新组合算子的融合优化，获得相比现有流行框架平均3到4倍的性能提升。

### 4. Graph Learning SIG构成

#### 领衔成员：

##### Lei CHEN

香港科技大学计算机科学与工程系首席教授、大数据研究所主任、IEEE fellow、ACM突出科学家，MindSpore首席科学家，研究方向包含数据驱动机器学习，大规模图学习，知识图谱等。

##### 刘子鹏

北京航空航天大学软件学院助理教授，博士毕业于加拿大不列颠哥伦比亚大学计算机系，主要研究方向为可视化与可视分析，人机交互，大数据分析，可解释机器学习。在可视化领域顶级期刊及会议（TVCG, CHI）发表论文多篇，曾获得 PacificVis 最佳论文提名奖。

#### 小组成员：

成员：苑玉杰，昇思MindSpore布道师

成员：吴一迪， 香港中文大学计算机系博士

成员：尹沛骐，香港中文大学计算机系博士

成员：大龙，华为数据系统高级工程师

成员：sophie，昇思MindSpore高级工程师

成员：fengxun，昇思MindSpore高级工程师

#### Maintainers

负责SIG日常活动的运作、制定SIG成员的培养计划以及开发项目管理。

Fengxun

Sophie

### 5. 2022目标

1. 新增支持10+图数据处理或图卷积接口
2. 新增支持图模型分布式训练
3. 接入CSR数据格式进一步优化性能
4. 建立GNN SIG

### 6. SIG 主要活动

#### 线上技术分享

不定期邀请SIG内部成员、业界专家教授等进行技术分享、MindSpore相关特性讲解或应用案例介绍等，平均周期为1-2月，活动预告会在SIG页面和代码仓主页更新。

#### 技术调研

每季度组织一次，发布业界最新论文或开源工作调研任务，SIG成员领取，最终以在SIG知乎账号发表博文或进行例会分享等形式展示调研成果。

#### 开发任务发放

1. 开源实习任务< https://gitee.com/mindspore/community/issues/I55TNF>，面向在校学生，时间灵活，完成任务获取积分后可领取相应实习工资。
2. 社区普通任务, 以graph learning仓issue的方式呈现，任何感兴趣的开发者可以提交相应的代码PR。

#### 成员发展

成员身份包含Contributors、Committers、Maintainers三种，记录在SIG成员名单中，各身份角色的描述和申请条件如下：

 **Contributors：** 积极参与SIG的日常活动，项目开发等，负责代码仓PR的review，提issue以及技术调研论文推荐等。申请条件：至少参加2次SIG会议/活动，并且参与2个以上PR代码review发表有效修改评论10个以上，或完成2次以上技术调研任务。

 **Committers：** 代码仓committer，拥有代码仓合入权限。申请条件：身份为contributor，至少完成5个社区issue任务或3个开源实习任务。

 **Maintainers：** SIG运作委员会成员，负责整个SIG的技术方向制定和活动组织。申请条件：身份为committers，通过现有maintainers中至少2名成员并且超过65%以上的总成员数投票同意。

 **申请方法:** 首先fork Community仓库；然后提交PR，把自己的Gitee主页链接、名字（不要求真名）、注册Gitee的邮箱以及兴趣方向加到SIG成员列表中，PR的描述中列举相关成果或贡献列表。提交PR之后，Maintainers会进行审核。

### 7. Graph Learning SIG的使命

聚焦于图计算、图学习方向的最新技术和应用，探索表达力更强的图学习模型，构建使用简单、计算高效的图学习框架，将图学习方法应用于实际场景取得更好的效果。

小组的重点工作包括以下几个方向：

#### ● 图学习模型库构建

基于MindSpore实现图学习各方向前沿算法模型，包含但不限于随机游走、 知识图谱、图神经网络、双曲图神经网络、时序图神经网络、Graphormer等。

#### ● 图计算框架优化

不同于结构数据的计算，图计算具有数据局部性差，高传输计算比，数据依赖复杂等特点，对计算资源和内存占用需求高。这一特点在大规模图分布式计算、异构图学习模型和时序图学习场景尤为突出，针对这些场景的数据结构，计算实现，编译优化基于MindSpore提出更高效的解决方案。
易用性方面，充分发挥图数据的逻辑可解释性，通过可视化工具分析图模型训练全流程，进一步指导用户调试调优图模型或数据处理。

#### ● 场景领域包

近年来，图学习在推荐、分子计算、知识图谱、自动驾驶等场景应用取得不少进展，进一步需要针对各场景包含但不限于推荐、分子计算、知识图谱等构建通用数据集，提炼常用模块接口，实现SOTA模型， 使后继研究者或应用者能在此基础上快速开展工作，构建一个开放，蓬勃发展的社区。

### 8. Graph Learning SIG工作计划

#### ● 前期：

以成员学术交流活动为主，定期分享最新论文或开源工作调研分析报告，不定期组织线上交流活动，围绕着图算法表达力提升，图计算优化，图学习在应用中遇到的问题，介绍研究工作进展，讨论研究工作中的难点。

#### ● 后期：

通过合作开发或竞赛等模式，在国内高校及企业间开展图学习相关问题的合作研究。
