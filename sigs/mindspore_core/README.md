## SIG简介

MindSpore core主要构建Mindpore的底层基础能力和基础表达，提供nn、数学等计算算子，自动微分，设备管理等功能，提供张量、模型等基础表达，以及动态图执行、静态图加速能力。

主要工作内容​​：
​1、​动态图内核开发​​：优化算子调度、内存管理和自动微分机制，提升执行效率。
​2、动静​混合编程支持​​：实现动态图与静态图的无缝切换（@ms.jit），结合两者的优势。
​3、​社区协作​​：响应开发者需求，修复动态图模式下的问题，完善文档与示例。
1. 生态建设: 构建与推广MindSpore基础接口能力与南向芯片生态（CPU/GPU/NPU/FPGA/x86/arm等），繁荣MindSpore社区，提升社区影响力。
2. 功能演进：模型构建能力、模型训推基础能力、模型序列化保存与加载、模型动态图和静态图执行能力、Ascend等异构硬件加速优化与表达、自动微分能力等。
3. 竞争力特性：面向下一代ascend硬件的平滑演讲与针对性优化；供灵活的开放能力，如自定义算子、hook、自定义pass等。

## PyNative相关代码仓

1. [MindSpore 代码仓](https://gitee.com/mindspore/mindspore)
2. [MindSpore Core SIG工作目录](https://gitee.com/mindspore/community/tree/master/sigs/mindspore_core)

## Maintainers

* 鲍翀（MindSpore core架构师，负责MindSpore core整体框架架构设计，特性方案评审等）
* 黎明奇（MindSpore编译后端&运行时架构师，负责异构硬件加速优化、三方硬件注入能力、运行时系统增强等）
* 余坚峰（MindSpore静态图编译架构师，负责静态入图能力、静态图编译、自动微分等）
* 褚金锦（MindSpore PyNative模式架构师，负责PyNative模式特性设计、开发和需求收集等）

## Contributors

* 蔡福璧（MindSpore PyNative模式资深开发者，负责MindSpore PyNative模式设计和特性开发）
* 罗超（MindSpore PyNative模式资深开发者，负责MindSpore PyNative模式设计和特性开发）
* 李振宇（MindSpore 运行时资深开发者，负责南向执行相关接口设计和开发）
* 张银霞（MindSpore 编译后端资深开发者，负责集合通讯相关接口设计和开发）
* 俞超杰（MindSpore 编译后端资深开发者，负责硬件相关图编译优化设计和开发）
* 胡彬（MindSpore 编译后端资深开发者，负责硬件相关图编译优化设计和开发）
* 黄炳坚（MindSpore 编译前端资深开发者，负责硬件无关图编译优化和python接口入图技术）
* 王睿（MindSpore 编译前端资深开发者，负责硬件无关图编译优化和python接口入图技术）
