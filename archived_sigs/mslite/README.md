## SIG简介

MindSpore Lite是MindSpore推出的端云协同的、轻量化、高性能AI推理框架，用于满足越来越多的端测AI应用需求。MindSpore Lite聚焦AI技术在端侧设备上的部署和运行，已经在华为HMS和智能终端的图像分类、目标识别、人脸识别、文字识别等应用中广泛使用，未来MindSpore Lite将与MindSpore AI社区一起，致力于丰富AI软硬件应用生态。MindSpore Lite的优势：

1. **极致性能**

    高效的内核算法和汇编级优化，支持CPU、GPU、NPU异构调度，最大化发挥硬件算力，最小化推理时延和功耗。

2. **轻量化**

    提供超轻量的解决方案，支持模型量化压缩，模型更小跑得更快，使能AI模型极限环境下的部署执行。

3. **全场景支持**

    支持iOS、Android等手机操作系统以及LiteOS嵌入式操作系统，支持手机、大屏、平板、IoT等各种智能设备上的AI应用。

4. **高效部署**

    支持MindSpore/TensorFlow Lite/Caffe/Onnx模型，提供模型压缩、数据处理等能力，统一训练和推理IR，方便用户快速部署。

MindSpore Lite分为离线模块和在线模块两个部分，其框架的总体架构如下所示：

![architecture](https://www.mindspore.cn/lite/docs/zh-CN/master/_images/MindSpore-Lite-architecture.png)

- 离线模块：
    - **3rd Model Parsers:** 将第三方模型转换为统一的MindIR，其中第三方模型包括TensorFlow、TensorFlow Lite、Caffe 1.0和ONNX模型。
    - **MindIR:** MindSpore端云统一的IR。
    - **Optimizer:** 基于IR进行图优化，如算子融合、常量折叠等。
    - **Quantizer:** 训练后量化模块，支持权重量化、激活值量化等训练后量化手段。
    - **benchmark:** 测试性能以及调试精度的工具集。
    - **Micro CodeGen:** 针对IoT场景，将模型直接编译为可执行文件的工具。
- 在线模块：
    - **Training/Inference APIs:** 端云统一的C++/Java训练推理接口。
    - **MindRT Lite:** 轻量化的在线运行时，支持异步执行。
    - **MindData Lite:** 用于端侧数据处理。
    - **Delegate:** 用于对接专业AI硬件引擎的代理。
    - **Kernels:** 内置的高性能算子库，提供CPU、GPU和NPU算子。
    - **Learning Strategies:** 端侧学习策略，如迁移学习。

## SIG代码仓

[MindSpore Lite](https://gitee.com/mindspore/mindspore/tree/master/mindspore/lite)

## Maintainers

- Zhai Zhiqiang(MindSpore Lite首席架构师，负责MindSpore Lite技术领域总体规划)
- Li Zheng(MindSpore Lite 专家工程师，负责MindSpore Lite 技术领域创新，SIG 发起人)

## Contributors

- Yunpeng(华为资深工程师，负责SIG规划、组织、运营与管理工作)

## 2022年目标

1. 硬件接入：基于南向接口对接等3款新硬件以及基于Micro新增对Cortex-M系列的接入
2. 组织管理：制定SIG组织管理规范，邀请Maintainers与Contributors初始成员参与SIG运作；
3. 生态拓展：发展50+位Lite SIG正式成员、1000+关注者；发展20位优秀开发者, 共同进行特性和案例开发建设；
4. 特性开发：在Lite技术领域中增加至少5个新特性并招募开发者共建；
5. 活动开展：开展技术分享活动直播6次，征集30篇技术文章、开发案例、趣味Demo；

## 主要活动

### 1. MindSpore Lite特性开发

- 活动定位：共同参与MindSpore Lite特性开发，打造端云协同的、轻量化、高性能AI推理框架
- 活动形式：定期发布大颗粒特性开发任务，招募开发者共同参与，完成者可获得奖品或者实习工资、实习证明
- 活动频率：每季度发布/刷新任务
- 任务范围：
    1. 通过南向自定义、Delegate机制对接新三方硬件
    2. 量化、剪枝、蒸馏等模型小型化新特性开发
    3. 端侧训练、联邦学习等新特性开发
    4. 转化工具新增Pytorch模型算子转换、图算融合等新特性开发
    5. Micro增加对Cortex-M系列的接入以及IAR等IDE的支持
    6. 补充及优化CPU、GPU算子
- MindSpore Lite现有相关任务：
    - [开源实习任务](https://gitee.com/mindspore/community/issues/I55WCW)
- 组织者：Lite技术领域Maintainers及Contributors

### 2. 线上技术分享会

- 活动定位：共同探讨MindSpore Lite推理框架相关话题
- 活动形式：定期邀请业界专家、高校师生、资深开发者分享话题
- 活动频率：每1-2个月1次，每次围绕同一个共同主题分享3-4个话题
- 分享范围：分享Lite技术领域相关的技术话题，包括但不限于：
    1. MindSpore Lite最新特性介绍与演示
    2. 量化、剪枝、蒸馏等模型小型化前沿论文和工程落地分享
    3. 端侧训练、联邦学习前沿论文和工程落地分享
    4. CPU、GPU等高性能算子库优化方法
    5. 学习心得、开发经验、部署建议
    6. SIG特性开发任务介绍与成果展示等
- 分享嘉宾：任何SIG成员，包括高校师生、业界专家、开发者均可
- 组织者：Lite技术领域Maintainers及Contributors

### 3. 资料改进活动

- 活动定位：持续提升Lite资料与产品综合体验
- 活动形式：开发者通过提交issue/PR形式提出问题建议或修改，累积积分获得奖品
- 活动频率：不定期举行
- 活动规划：
    - 开发案例：针对官网上线的特性，通过视频/案例的形式丰富教程
    - 趣味小应用Demo：采用Lite进行推理，实现趣味小应用Demo

### 4. 周例会

- 时间：周四晚上7点，每1-2周开展一次
- 例会内容：面向SIG特性开发和组织管理工作，进行开放式的例行交流
- 例会议题：
    1. 固定议题：SIG成员领取的特性开发任务进展与问题交流
    2. 选报议题：特性开发阶段性成果演示
    3. 选报议题：SIG组织管理（如运作规则讨论、Maintainers&Contributors担任人员及职责刷新）
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

## 近期活动预告

1. MindSpore Lite端侧训练

## 往期会议

- [2022昇思MindSpore TechDay](https://www.bilibili.com/video/BV1o34y147zE?p=6)

- [第三届MindCon极客周](https://www.bilibili.com/video/BV1kU4y1T7PH?p=7)

- [1024全场景AI论坛](https://www.bilibili.com/video/BV1dQ4y1U739?p=2)

- [MindSpore 第六期集训营](https://www.bilibili.com/video/BV1f34y1o7mR?spm_id_from=333.337.search-card.all.click)

- [MindSpore 第五期集训营](https://www.bilibili.com/video/BV14V411q7C2?spm_id_from=333.337.search-card.all.click)

- [MindSpore Lite SIG Meeting](https://www.bilibili.com/video/BV1ef4y1H7p2/?spm_id_from=333.788.recommend_more_video.-1)

- [MindSpore Lite南向接入](https://www.bilibili.com/video/BV1pv411H7x3?spm_id_from=333.337.search-card.all.click)