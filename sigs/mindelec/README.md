## SIG简介

电磁场看不见、摸不着，却在日常生活中无处不在。电磁场的产生主要源于自然和人工两类。自然产生的电磁场有地磁场、太阳光以及一切物体热辐射产生的电磁波等等。自然电磁场催生并推动了人类的文明：由于太阳光的存在，人类可以在温度适宜的地球居住，可以通过植物的光合作用获取充足的食物；利用地磁场人类可以进行导航，进而迎来了大航海和全球化时代。随着科技的发展，人类已经不满足于自然产生的电磁场，开始主动向环境中发射电磁场，并充分挖掘电磁场的应用潜力。如通信领域中利用无线电波收听广播、利用高频微波进行手机通话等；又如地质勘探中利用电磁波的回波探明煤炭存储等。

电磁场的应用不胜枚举，为了能够更好的利用电磁场，人们通过实验、理论以及计算等手段研究电磁场的机理。实验方面，1820年奥斯特在一次讲座上偶然发现通电的导线让小磁针发生偏转，从而发现了电能生磁的现象。1831年，法拉第在实验中发现变化的磁场可以产生电场，即磁也能够生电。麦克斯韦总结前人的工作，提出了位移电流假说（变化的电场能够产生磁场），完善了电生磁的理论。最终，麦克斯韦将电磁场理论用给简洁、对称和完美的数学形式表示出来，即麦克斯韦方程组。随着计算机技术的发展，人们采用数值计算的方式去求解麦克斯韦方程组,模拟电磁场在空间中的分布。这样即可以节省实验的成本，也可以通过仿真设计出更加符合需求的电子设备。传统的电磁计算方法包括精确的全波方法和高频近似方法。全波方法如时域有限差分（Finite-Difference Time-Domain method，FDTD），有限元（Finite-Element-Method，FEM）、矩量法（Method of MoMents，MoM）等；高频近似方法如几何光学法（Geometrical Optics，GO）、物理光学法(physical optics，PO)等。

数值计算较好地辅助了电子产品的设计，但传统的数值方法仍存在许多缺陷，如需要进行复杂的网格剖分、迭代计算，计算过程复杂、计算周期长。神经网络具有万能逼近和高效推理能力，这使得神经网络在求解微分方程时具有潜在的优势。为此，昇思MindSpore Elec AI 专项兴趣小组（简称：智能电磁AI SIG）正式成立，并面向开源社区招募志同道合的伙伴。

## MindSpore Elec AI SIG的使命

围绕实际生产中的各类电磁应用场景，在昇思MindSpore框架下探索和研究基于AI的电磁正问题以及反问题。例如开发高效精确的AI电磁模型，构建高效的MindSpore Elec基础工具包，提升电子产品的设计效率等。

### MindSpore Elec 代码仓

1. [Mindspore Elec 代码仓](https://gitee.com/mindspore/mindscience/tree/master/MindElec)
2. [Mindspore Elec SIG 工作目录]( https://gitee.com/mindspore/community/tree/master/sigs/mindelec)

### SIG小组重点工作方向

#### MindSpore Elec基础工具包构建

基于MindSpore构建MindSpore Elec基础工具包。基础工具包内置有数据构建及转换、仿真计算以及结果可视化等。

  1. 数据构建及转换：支持CSG （Constructive Solid Geometry，CSG） 模式的几何构建，以及cst和stp数据（CST等商业软件支持的数据格式）的高效张量转换。

  2. 仿真计算：
     a) AI电磁基础模型库：提供物理和数据驱动的AI电磁模型，物理驱动无需额外的标签数据，只需方程和初边界条件即可；数据驱动是指训练需使用仿真或实验等产生的数据。
     b) 优化策略：数据压缩可以有效地减少神经网络的存储和计算量；多尺度滤波、动态自适应加权可以提升模型的精度，克服点源奇异性等问题；小样本学习主要是为了减少训练的数据量，节省训练的成本。

  3. 结果可视化：仿真的结果如S参数或电磁场等可保存在CSV、VTK文件中。MindInsight可以显示训练过程中的损失函数变化，并以图片的形式在网页上展示结果；Paraview是第三方开源软件，具有动态展示切片、翻转等高级功能。

#### AI电磁仿真模型和方法构建

  1. 端到端可微的传统电磁仿真方法研究：基于MindSpore构筑传统的电磁仿真方法如FDTD/有限元/矩量法等，形成端到端可微的AI融合方法。这样可以利用MindSpore加速传统的数值方法，生成模型训练的数据，也可以基于自动微分机制，实现数据同化、电磁反演等应用。

  2. AI电磁仿真融合算法研究: 物理驱动（如PINNs方法）和数据驱动的AI方法，以及物理和数据融合的算法创新等。

#### AI电磁仿真模型应用

  1. 正问题：基站天线、雷达天线、射频电路与系统等电磁仿真。

  2. 反问题：电磁超材料设计、雷达勘探、电磁成像等。

## MindSpore Elec AI SIG工作计划

  1. 前期：以成员学术交流活动为主，每月组织线上交流活动，围绕AI电磁中涉及的问题，介绍研究工作进展，讨论研究工作中的难点。

  2. 后期：通过合作开发等模式，在国内高校及企业间开展电磁AI问题的合作研究。

## MindSpore Elec AI SIG构成

### 领衔成员：

* 陆卫兵 东南大学科研院 院长/教授
* 杨武 东南大学信息科学与工程学院 副研究员
* 徐勇 江苏浩云连德信息技术有限公司 高级工程师
* 李家奇 东南大学物理学院 副教授
* 陈新蕾 南京航空航天大学电子信息工程学院 副教授

### 小组成员：

* 成员：苑玉杰 华为昇思MindSpore布道师
* 成员：Kyang 华为昇思MindSpore高级工程师

* 成员：翁瑞 东南大学信息科学与工程学院 博士生
* 成员：Adrian Lee 华为昇思MindSpore高级工程师
* 成员：Lulu Zhang 华为昇思MindSpore高级工程师
* 成员：秦洁 东南大学信息科学与工程学院 硕士生
* 成员：张哲 东南大学信息科学与工程学院 硕士生
* 成员：孙丁一 东南大学信息科学与工程学院 硕士生