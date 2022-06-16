# 代码检视Checklist运作机制（试运行）

## 目标

代码检视 Checklist 诣在辅助 Committer 进行高质量代码检视，同时为开发者提供代码自检的参考指南。

## Checklist 说明

代码检视 Checklist 分为 **必选** 与 **可选** 两节，其中：

### 必检项：

必选检查项位于**Code review checklist**下，为 Committer 代码Review的常规检查项，Committer 确认无问题后请在 CheckBox 勾选以表明完成对应检查（若当前 Pull request
不涉及某项，无须勾选）；若当前 Pull request 涉及 **【性能分析】**中某子项、**【是否涉及模块/特性间交互】**，请开发者概述设计思想或实现方案。

- **Typical problems of security
  coding [[historical security coding cases reference]](https://gitee.com/mindspore/community/blob/master/security/security_coding_violation_cases.md)**
    - [ ] whether to verify the pointer is null/nullptr
    - [ ] whether to verify the function's return value
    - [ ] whether new/malloc memory is released correctly
- **Performance analysis (if a sub-item is involved, please outline the implementation idea or modification content)**
    - [ ] whether to modify hotspot ***function / algorithm / operation***
    - [ ] whether to consider concurrent scenarios
    - [ ] whether to consider communication scenario

- - [ ] **Whether to comply with coding
      specifications [[coding specification reference]](https://gitee.com/mindspore/community/blob/master/security/coding_guild_cpp_zh_cn.md)**
- - [ ] **Whether to comply with ***SOLID principle / Demeter's law*****
- - [ ] **Whether the ***interaction between modules / features*** is involved (if yes, please outline the
      implementation ideas)**
- - [ ] **Whether there is UT test case && the test case is a valid (if there is no test case, please explain the
      reason)**
- - [ ] **whether the secret key is loaded/released correctly**

- **Error handling and recording**
    - [ ] whether the interface exception scenarios are fully considered
    - [ ] whether the error is recorded appropriately

### 可选检查项：

若当前Pull request涉及 **【是否导致无法前向兼容】**、**【是否为对外接口变更】**、**【是否涉及依赖的三方库变更】**
  中某项，请将对应可选项的注释去掉，并增加对应的评审结论，如：”已于YYYY/MM/dd在SEG通过评审“；若涉及对外文档变更，请将**【是否涉及文档（安装、教程、设计、参考、API、迁移指南、FAQ等）修改】**
  的注释打开，并附上文档变更的Pull request。

- [ ] **Whether document (installation, tutorial, design, reference, API, migration guide, FAQ, etc.) modification
      is involved**
- - [ ] **Whether it causes forward compatibility failure**
- - [ ] **Whether the API change is involved**
- - [ ] **Whether the dependent third-party library change is involved**

## 代码检视 Checklist 中英文参照表

| 检视项                                                              | checklist                                                                                                              |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| 是否进行空指针校验                                            | whether to verify the pointer is null/nullptr                                                                          |
| 是否进行返回值校验                                            | whether to verify the function's return value                                                                          |
| 是否正确释放new/malloc内存                                     | whether new/malloc memory is released correctly                                                                        |
| 是否修改热点函数/算法/算子                                 | whether to modify hotspot function / algorithm / operation                                                             |
| 是否考虑并发场景                                               | whether to consider concurrent scenarios                                                                               |
| 是否考虑通信场景                                               | whether to consider communication scenario                                                                             |
| 是否符合编码规范 【编码规范】                            | Whether to comply with coding specifications [coding specification reference]                                          |
| 是否遵守SOLID原则/迪米特法则                                | Whether to comply with SOLID principle / Demeter's law                                                                 |
| 是否涉及模块/特性间交互【若涉及请概述实现思路】 | Whether the interaction between modules / features is involved (if yes, please outline the implementation ideas)       |
| 是否具备UT测试用例看护 && 测试用例为有效用例【若无测试用例请说明原因】 | Whether there is UT test case && the test case is a valid (if there is no test case, please explain the reason)        |
| 秘钥是否被正确加载、释放                                   | whether the secret key is loaded/released correctly                                                                    |
| 是否充分考虑接口的异常场景                                | whether the interface exception scenarios are fully considered                                                         |
| 是否正确记录错误信息                                         | whether the error is recorded appropriately                                                                            |
| 是否涉及文档（安装、教程、设计、参考、API、迁移指南、FAQ等）修改 | Whether document (installation, tutorial, design, reference, API, migration guide, FAQ, etc.) modification is involved |
| 是否导致无法前向兼容                                         | Whether it causes forward compatibility failure                                                                        |
| 是否为对外接口变更                                            | Whether the API change is involved                                                                                     |
| 是否涉及依赖的三方库变更                                   | Whether the dependent third-party library change is involved                                                           |
