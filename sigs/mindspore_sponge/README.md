## SIG 简介

MindSPONGE是基于昇思MindSpore面向计算生物领域的套件，涵盖药物研发全流程。MindSPONGE中包含白质结构预测工具MEGA-Protein，分子动力学模拟等多种常用功能。

### MEGA-Protein

MEGA-Protein包含MSA生成(MEGA-EvoGen)、蛋白质折叠训练推理流程(MEGA-Fold)、蛋白质结构打分(MEGA-Assessment)、蛋白质结构预测数据集PSP等关键技术，该工具提供了高精度高性能蛋白质结构和功能预测。

#### MEGA-EvoGen

MEGA-EvoGen能够在MSA较少(few shot)甚至没有MSA(zero-shot，即单序列)的情况下，帮助MEGA-Fold/AlphaFold2等模型维持甚至提高推理精度，突破了在“孤儿序列”、高异变序列和人造蛋白等MSA匮乏场景下无法做出准确预测的限制，该方法获得了CAMEO-3D蛋白质结构预测赛道月榜第一。

#### MEGA-Fold

MEGA-Fold网络模型部分与AlphaFold2相同，在数据预处理的多序列对比环节采用了MMseqs2进行序列检索，相比于原版端到端速度提升2-3倍；同时借助内存复用大幅提升内存利用效率，同硬件条件下支持更长序列的推理。其中在Ascend 910 32G硬件下支持3072推理长度。

#### MEGA-Assessment

MEGA-Assessment可以评价蛋白质结构每个残基的准确性以及残基-残基之间的距离误差，从而达到跨模型挑选蛋白质结构，并且在CAMEO-QE结构质量评估赛道取得月榜第一， 同时可以基于评价结果对蛋白结构作出进一步的优化。

### 基于AI框架昇思MindSpore的MD模拟软件

分子动力学模拟软件是一种根据分子力场所描述的势能函数模拟分子的微观运动，从而计算分子体系的物理和化学性质的科学计算工具，在化学、生物、物理、制药、材料、环境等领域有着广泛的应用。基于AI框架昇思MindSpore的MD模拟软件具备自动微分，支持不同硬件，端到端可微等优点。

#### 自动微分

昇思MindSpore的“自动微分”功能，可以直接计算函数的导数，因此基于MindSpore编写分子力场只需编写势能函数的代码即可，原子受力即原子坐标对势能函数的负梯度可以直接通过“自动微分”计算，在很大程度上简化了MD模拟程序结构的复杂度。

#### 支持不同硬件

昇思MindSpore能在CPU、GPU和华为自主研发的“昇腾”(Ascend)AI加速芯片上运行，程序只需修改一行代码便可移植到不同的硬件设备上。此外，华为昇思MindSpore还具备“自动并行”的能力，只需简单修改代码就能自动实现程序的并行化计算。

#### 端到端可微

昇思MindSpore具备“高阶自动微分”的能力，可以自动求解函数的高阶导数。因此可以像运行AI优化算法那样，直接对MD模拟过程本身进行优化，从而获得理想的结果。这即是一种“元优化”(meta-optimization)过程。

## SIG 代码仓

1. [MindSPONGE 代码仓](https://gitee.com/mindspore/mindscience/tree/master/MindSPONGE)
2. [MindSpore SPONGE SIG工作目录](https://gitee.com/mindspore/community/tree/master/sigs/mindspore_sponge)

## CO-CHAIRS

* 杨奕 （深圳湾实验室副研究员，MindSPONGE社区核心贡献者）
* 张骏 （昌平实验室研究员，MindSPONGE社区核心贡献者）
* 刘思睿 （昌平实验室研究员，MindSPONGE社区核心贡献者）

## Maintainers

* Yahao Ding （MindSPONGE社区资深开发者，负责MindSPONGE生态推广、特性开发和需求收集等）
* Mengyun Chen （MindSPONGE社区资深开发者，负责MindSPONGE生态推广、特性开发和需求收集等）
* Ningxi Ni （MindSPONGE社区资深开发者，负责MindSPONGE生态推广、特性开发和需求收集等）
* 夏义杰 （MindSPONGE社区核心贡献者）
* 陈迪青 （MindSPONGE社区核心贡献者）
* 黄渝鹏 （MindSPONGE社区核心贡献者）
* Haotian Chu  （MindSPONGE社区资深开发者，负责MindSPONGE生态推广、特性开发和需求收集等）
* Junbin Li （MindSPONGE社区资深开发者，负责MindSPONGE生态推广、特性开发和需求收集等）
* Chenghao Wang （MindSPONGE社区资深开发者，负责MindSPONGE生态推广、特性开发和需求收集等）
* Min Wang （MindSPONGE社区资深开发者，负责MindSPONGE生态推广、特性开发和需求收集等）
* Jialiang Yu （MindSPONGE社区资深开发者，负责MindSPONGE生态推广、特性开发和需求收集等）

## 成果积累

* 蛋白质结构预测工具MEGA-Fold获得CAMEO-3D蛋白质结构预测赛道2022年4月月榜第一。

* MSA生成工具MEGA-EvoGen获得CAMEO-3D蛋白质结构预测赛道2022年7月月榜第一。

* 蛋白质结构评分工具MEGA-Assessment获得了CAMEO-QE结构质量评估赛道2022年7月月榜第一。

* 2022.8.11—2022.8.15举办了MindSPONGE SIG暑期学校活动，邀请到13位专家老师进行一场为期五天的授课，授课主题主要包括MindSpore基础，分子动力学以及AI × Science进阶课程三大主题

## 主要活动

### 1, 暑期学校活动

时间：每年暑假

主要内容：大型授课活动，MindSpore使用教学， MindSPONGE案例讲解，论文分享，前沿技术讲解

主讲人：SIG组内核心专家老师，业界专家教授

组织者：Maintainers

### 2, 校园行活动

时间：不定期，一季度一次

主要内容：MindSPONGE介绍，MindSPONGE案例讲解

分享人：SIG成员、业界专家教授

参与者：Members，高校学生等

组织者：Maintainers

### 3，开发任务发放

① [开源实习任务](https://gitee.com/mindspore/community/issues/I561LI?from=project-issue)

② [社区普通任务]()（暂无）

时间：每季度一次

负责人：Maintainers、Committers

### 4，内部分享会

时间：每月一次

主要内容：Members交流已调研论文或正在开发内容

负责人：Maintainers、Committers轮流组织,或Members主动提出申请。

### 5，晋升选拔

时间：每半年一次

内容：选拔Committers、Maintainers。

负责人：Maintainers

## 近期活动与例会预告

1. 即将公布12月初校园行活动预告
2. SIG组例会

## 往期活动

1. 2022.8.11—2022.8.15， MindSPONGE SIG[暑期学校活动](https://www.bilibili.com/video/BV1pB4y167yS/?spm_id_from=333.999.0.0&vd_source=94e532d8ff646603295d235e65ef1453)。
