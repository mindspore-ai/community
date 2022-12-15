# MindSpore开源软件选型及使用要求


## 选型规则

### 规则1：开源软件变更的对象应该是开源软件

开源软件的定义参考[https://opensource.org/osd.html](https://opensource.org/osd.html) 。MindSpore目前的三方软件承载在<https://gitee.com/mindspore/community/blob/master/security/config/Third_Party_Open_Source_Software_List.yaml>中。

### 规则2：不建议选择GPL或LGPL开源软件；禁止选用无许可证、许可证要求无法履行、有知识产权问题的开源软件

MindSpore引入的开源软件，不建议使用GPL，LGPL的开源软件。GPL是Copyleft类型的许可协议，有传导性，这意味着基于GPL组件编写的任何软件以及依赖GPL的任何软件的都必须以开源的方式进行发布。

若MindSpore包含GPL协议的依赖软件，则对于依赖MindSpore的产品也需要进行开源发布，可能造成商业风险。对于协议是LGPL的软件，如果使用方式是动态链接，则不需要公开源码或履行开源职责。

### 规则3：开源软件变更需要通过Technical Committee评审

开源软件的变更，包括在MindSpore社区中引入其他开源软件（项目）、升级或者降级已引入的开源软件、删除已引入的开软软件等动作。

其中引入、升级、降级开源软件必须满足开源软件选型原则。升级、降级开源软件必须考虑MindSpore社区所提供功能的稳定性与兼容性。

整个变更的过程都必须可被追踪。 TSC通过对变更申请(Pull Request)的评审，管理软件变更。MindSpore开源软件变更时，

包括新引入、变更版本等，通过Technical Committee评审，Technical Committee对软件引入原则的一致性负责。

### 规则4：开源软件变更通过MindSpore社区ISSUE管理

Technical Committee评审通过后，对于开源三方件变更，MindSpore通过MindSpore社区ISSUE的方式管理选型评估信息。可参照https://gitee.com/mindspore/mindspore/issues/I4NAY6?from=project-issue。

### 规则5：开源软件引入前，需要确保满足技术生态要求

1. 开源软件引入前，需要确保能正确构建；当软件有尚未被引入的依赖关系，或者软件的运行或者构建依赖一个绝不可能引入MindSpore的组件，此等例外，经由Technical Committee讨论后决定。

2. 选用版本必须是正式发布的版本。未正式发布的版本（如：Beta版本，rc（Released candidate）版本）禁止引入。

3. 优先选择主流的供应商/社区或社区项目。

4. 优先选择版本稳定性高的软件，无已知的未解决的致命Bug。

5. 优先选择代码质量高的软件。如代码结构规范、代码调试功能可关闭、有自动化构建能力、自动化测试充分等。

### 规则6：开源软件引入前，需要确保满足网络安全要求

1. 禁止选用含非误报病毒告警的软件。

2. 选用的开源软件必须有问题反馈与修复跟踪管理机制，优先选择有漏洞披露源的开源软件。

3. 优先选择漏洞较少的版本。

### 规则7：选用成熟期或成长期的软件，禁止选用处于衰退期的软件

成长期软件：发布频繁。成熟期软件：定期发布版本。衰退期软件：社区更新少，已经不再发布新版本。
