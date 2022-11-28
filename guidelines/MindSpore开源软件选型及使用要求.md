# MindSpore开源软件选型及使用要求


## 选型规则

### 规则1：开源软件变更的对象应该是开源软件

开源软件的定义参考[https://opensource.org/osd.html](https://opensource.org/osd.html) 。MindSpore目前的三方软件承载在<https://gitee.com/mindspore/community/blob/master/security/config/Third_Party_Open_Source_Software_List.yaml>中。

### 规则2：禁止选择GPL或LGPL开源软件

MindSpore引入的开源软件，要求禁止使用GPL，LGPL的开源软件。

### 规则3：开源软件变更需要通过Technical Committee评审

MindSpore开源软件变更时，包括新引入、变更版本等，通过Technical Committee评审，Technical Committee对软件引入原则的一致性负责。

### 规则4：开源软件变更通过MindSpore社区ISSUE管理

Technical Committee评审通过后，对于开源三方件变更，MindSpore通过MindSpore社区ISSUE的方式管理选型评估信息。

### 规则5：开源软件引入前，需要确保可以被正确构建

当软件有尚未被引入的依赖关系，或者软件的运行或者构建依赖一个绝不可能引入MindSpore的组件，此等例外，经由Technical Committ讨论后决定。



