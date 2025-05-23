## SIG简介

MindSpore Lite小组（MindSpore Lite Sig）专注于端侧AI的部署优化，该小组由华为MindSpore核心开发团队、学术专家及社区开发者共同组成，致力于构建极速、极智、极简的端侧AI引擎，使能全场景智能应用，帮助用户使能AI能力。
MindSpore Lite聚焦AI技术在端侧设备上的部署和运行，已经在华为HMS和智能终端的图像分类、目标识别、人脸识别、文字识别等应用中广泛使用，未来MindSpore Lite将与MindSpore AI社区一起，致力于丰富AI软硬件应用生态。MindSpore Lite的优势：

1. **极致性能**

    高效的内核算法和汇编级优化，支持CPU、GPU、NPU推理后端，最大化发挥硬件算力，最小化推理时延和功耗。

2. **轻量化**

    提供超轻量的解决方案，支持模型量化压缩，模型更小跑得更快，使能AI模型极限环境下的部署执行。

3. **全场景支持**

    支持OpenHarmony、iOS、Android等手机操作系统以及LiteOS嵌入式操作系统，支持手机、平板、PC、座舱、IoT等各种智能设备上的AI应用。

4. **高效部署**

    支持MindSpore/Onnx/TensorFlow/TensorFlow Lite/Caffe模型，提供模型压缩、数据处理等能力，统一训练和推理IR，方便用户快速部署。

MindSpore Lite分为离线模块和在线模块两个部分，其框架的总体架构如下所示：

![architecture](https://www.mindspore.cn/lite/docs/zh-CN/master/_images/MindSpore-Lite-architecture.png)

- 离线模块：
    - **3rd Model Parsers:** 将第三方模型转换为统一的MindIR，其中第三方模型包括ONNX、TensorFlow、TensorFlow Lite等。
    - **MindIR:** MindSpore端云统一的IR。
    - **Optimizer:** 基于IR进行图优化，如算子融合、常量折叠等。
    - **Quantizer:** 训练后量化模块，支持权重量化、激活值量化等训练后量化手段。
    - **benchmark:** 测试性能以及调试精度的工具集。
    - **Micro CodeGen:** 针对IoT场景，将模型直接生成为可执行代码。
- 在线模块：
    - **Inference APIs:** 端云统一的C/C++/Java训练推理接口。
    - **MindRT Lite:** 轻量化的在线运行时，支持异步执行。
    - **Delegate:** 用于对接专业AI硬件引擎的代理。
    - **Kernels:** 内置的高性能算子库，提供CPU、GPU和NPU算子。
    - **On-device Learning:** 端侧学习，提供模型微调能力，支持模型个人化体验。

## MindSpore Lite相关代码仓

1. [MindSpore Lite代码仓](https://gitee.com/mindspore/mindspore/tree/master/mindspore/lite)
2. [MindSpore Lite SIG工作目录](https://gitee.com/mindspore/community/tree/master/sigs/mindspore_lite)

## Maintainers

- 卢家乐（MindSpore Lite社区责任人，负责社区运营、宣传推广、优秀开发者和布道师发展等）
- 朱国栋（MindSpore Lite资深工程师，社区运营接口人，负责社区运营，、宣传推广、优秀开发者和布道师发展等）
- 张琦（MindSpore Lite资深工程师，负责MindSpore Lite框架特性设计、开发和需求收集等）
- 蒋辉（MindSpore Lite资深工程师，负责MindSpore Lite框架特性设计、开发和需求收集等）

## Committers

- 姜建飞（MindSpore Lite资深工程师，负责MindSpore Lite框架需求讨论、特性设计、代码评审等）
- 朱国栋（MindSpore Lite资深工程师，负责MindSpore Lite框架需求讨论、特性设计、代码评审等）
- 叶锋（MindSpore Lite资深工程师，负责MindSpore Lite框架需求讨论、特性设计、代码评审等）
- 徐安越（MindSpore Lite资深工程师，负责MindSpore Lite框架需求讨论、特性设计、代码评审等）
- 陈建平（MindSpore Lite资深工程师，负责MindSpore Lite框架需求讨论、特性设计、代码评审等）

## Contributors

- 杨迎春（MindSpore Lite资深开发者，负责MindSpore Lite模式生态推广、特性开发和需求收集等）
- 张栋宇（MindSpore Lite资深开发者，负责MindSpore Lite模式生态推广、特性开发和需求收集等）
- 顾鹏程（MindSpore Lite资深开发者，负责MindSpore Lite模式生态推广、特性开发和需求收集等）
- 程枫 （MindSpore Lite资深开发者，负责MindSpore Lite模式生态推广、特性开发和需求收集等）
