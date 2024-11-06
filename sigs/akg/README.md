# 昇思MindSpore AKG SIG

MindSpore社区成立SIG的初衷是为该领域的专家、教授和学生提供一个开放交流的平台，通过会议分享、项目开发等活动促进技术交流、合作共赢，并使得SIG成员的影响力和技术能力得到提升。
昇思MindSpore社区欢迎业界专家、学术伙伴在社区成立特别兴趣小组（SIG），作为社区领域技术代言人，打造领域技术品牌，共建昇思MindSpore开源生态。

## 简介

MindSpore AKG SIG专注于利用MindSpore AKG在图计算融合编译领域的技术积累，持续完善软件功能，拓展社区生态，为科研人员、教师、学生以及对此领域有深厚兴趣和强大影响力的人们提供一个高效易用的图计算融合编译器，同时提供一个共同交流合作的平台。

## 使命

持续引入业界先进的算子编译技术，帮助MindSpore AKG进行功能迭代，打造业界领先的算子编译器。

## 工作计划

主要围绕成员学术交流活动，为MindSpore AKG的演进和功能完善提供参考。

### 活动组织

每年小组都会组织一场大型活动和数场小型活动，包括每个季度固定的校园行活动和每年固定的大型暑期学校活动，邀请组内的核心专家老师准备多个主题进行多天的授课。小组老师将带领成员进行科技调研以及代码仓功能扩展、bug修复等工作。成员也可以自由使用MindSpore AKG软件进行自己的课题研究和开发。

### 开源实习

小组将在社区内发布开源实习任务和众智任务，供学生和老师认领。当前我们安排的任务包括：

1. **MindSpore AKG算子支持**  
   对于新算子提供基于循环和数学表达式的表达，对于融合算子提供以已有算子拼接的展开表达。

2. **MindSpore AKG后端支持迭代**  
   随着包括MLIR社区版本的迭代和硬件的更新，我们计划对后端代码生成能力进行持续更新，并随着更多AI芯片的涌现，添加更多后端的代码生成能力。

## 构成

### 小组领衔成员

- 赵捷，湖南大学信息科学与工程学院教授,华为MindSpore社区技术专家委员会委员。

### 小组成员

- Renwei Zhang（@anyrenwei），SIG发起人，昇思MindSpore技术专家
- Zichun Ye （@zichun_ye），SIG Lead与组织者，昇思MindSpore高级工程师
- 赵捷（@yaozhujia），SIG组织者与运营顾问，AI编译器资深专家
- Leo（@zhanghanLeo），昇思MindSpore工程师
- Xinkai（@di-xinkai），昇思MindSpore工程师
- gent1e（@gent1ezzz），昇思MindSpore工程师
- pudding，香港科技大学，AI编译器专家
- 蛋、，华南理工大学，AI编译器开发者

## 会议记录

会议记录和提案将定期在此仓库中记录和更新。

## 代码仓库

- 主AKG代码仓：https://gitee.com/mindspore/akg
- SIG仓库：https://gitee.com/mindspore/community/tree/master/sigs/akg

ms.set_context(enable_graph_kernel=True, graph_kernel_flags="--kernel_generator=AKG_V2 --disable_cluster_ops=Cast --enable_expand_ops_ops= BiasAdd ,iasAddGrad, FillV2,FastGelu,FastGeluGrad,FastGeLU,FastGeLUGrad ,SiLU,SiLUGrad, RsqrtGrad,Sigmoid,igmoidGrad,SigmoidCrossEntropyWithLogits,SigmoidCrossEntropyWithLogitsGrad,SquaredDifference,TanhGrad,OnesLike,ZerosLike,ReduceMean,LogSoftmaxGrad,ReLU,ReluGrad, AdamApplyOneWithDecay")
