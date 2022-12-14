# MindSpore 开发流程

![image.png](https://images.gitee.com/uploads/images/2022/0713/145040_8bd805cc_7501862.png)

## 落地一致性自验

* [ ] 特性需求是否发生变化？如果是：
  - [ ] 需求是否经过需求评审会评审？
  - [ ] 相关人力、交付时间是否进行调整？
  - [ ] 特性交付规格是否与测试进行对齐？

* [ ] 特性设计是否发生变化？如果是：
  - [ ] 是否需要进行技术委员会评审？
  - [ ] 是否调整特性设计文档、并与测试串讲对齐？
  - [ ] 如果有其他模块的依赖关系，是否需要重新梳理交互点？

## 特性内容自验

### 特性等级自验

* [ ] STABLE：需求有具体的落地应用场景，而且特性支持是平台无关、或全平台通用的。无较大应用场景约束。
* [ ] BETA：需求有落地场景，但特性支持的平台有限，或有偏向性的应用场景约束。
* [ ] DEMO：需求不一定有落地场景，属于阶段性设计的特性，无交付计划场景。

### 特性代码自验

* [ ] 特性功能完整性自检
* [ ] 特性错误日志规范自检（[日志与错误信息规范 V1.3](https://e.gitee.com/mind_spore/docs/984545/file/2690919?sub_id=5661904)）
* [ ] C++/Python 安全规范、编程规范自检（[C++ 编程规范](https://gitee.com/mindspore/community/blob/master/security/coding_guild_cpp_zh_cn.md)、[Python 编程规范](https://gitee.com/mindspore/community/blob/master/security/coding_guild_python_zh_cn.md)）
* [ ] C++/Python 典型代码问题自检（[C++ 典型代码问题检视指导书](https://e.gitee.com/mind_spore/docs/983619/file/2685819)、[Python 典型代码问题检视指导书](https://e.gitee.com/mind_spore/docs/983620/file/2685821)）

### 开发者测试自验

* [ ] UT/ST测试用例开发指导书（[UT 测试用例开发指导书](https://e.gitee.com/mind_spore/docs/983555/file/2685526?sub_id=5654688)）
* [ ] 是否对API进行调用测试？参数类型校验测试、参数范围校验测试、参数冲突校验测试、输入校验
* [ ] 是否对特性所有**正常分支**场景进行覆盖？
* [ ] 是否对特性所有**异常分支**场景进行覆盖？
* [ ] 是否对于其他特性有影响的场景进行覆盖？

### 交付场景自验

* [ ] 是否与测试对齐交付测试场景？

  * [ ] 明确验收场景、用例、验收标准
* [ ] 特性是否与硬件平台相关？

  * [ ] 如果否：CPU侧基本功能验证
  * [ ] 如果是：
    * [ ] Ascend
      * [ ] 特性模块单点测试
      * [ ] 端到端交付场景测试
    * [ ] GPU
      * [ ] 特性模块单点测试
      * [ ] 端到端交付场景测试
* [ ] 特性是否影响到modelzoo模型？

  * [ ] 是否通过触发每日CI提前验证？
  * [ ] 是否通过触发每周CI提前验证？

### 特性资料自验

* [ ] 是否需要新增/更新 API 文档，包括中英文？（[资料标准协作规范](https://e.gitee.com/mind_spore/docs/983610/file/2685802)）
* [ ] 是否需要新增/更新教程、指导文档？
* [ ] 是否有变更需要呈现在Release Note？

## 特性交付件自验

* [ ] 特性代码是否已上库？
* [ ] 新增或修改 API 的中/英文文档，或教程文档，是否同步上线？
* [ ] 特性转测文档是否准备完成？
* [ ] 特性报错白名单文档是否准备完成？

## 其他代码规范自验

#### 安全规范（重点）

1. 禁止使用危险函数，包括memcpy()、memmove()、memset()、strcpy()、strcat()等，替换为相应安全函数等。
2. 防止空指针引用，对未知指针操作前需要先判空。
3. 变量使用前未初始化，建议定义时就进行初始化操作。
4. 未检查函数返回值，安全函数、状态函数的返回值需要先进行校验，再执行后续操作。
5. 除0问题，外部传入的参数作为除数前需要先判0。
6. 越界读写，未校验的值作为索引直接访问指针或数组，可能导致内存和数组越界访问。
7. 整数溢出、反转，整数加减乘除后的值可能超出预期时，需要提前进行校验。
8. 文件路径遍历前，需要先转换成对应Realpath，防止外部构造指向系统关键文件的链接文件，或跨越目录限制访问文件。
9. 捕获异常时及时关闭读写句柄。

#### 编程规范

1. 是否存在冗余头文件，未使用的应删除，.h中已经引用过的头文件，也无需在.cc文件里再引用。
2. 是否存在冗余代码，即定义了却从未使用的变量和函数。
3. **是否存在被注释的代码，无用的代码需要删除。**
4. 头文件是否按照标准库、第三方库、本代码库的顺序分块？每个块内是否按照**字母序**进行排列？只有.cc文件对应的.h文件允许放在头部进行引用。
5. explicit用于屏蔽隐式调用，除带有默认值的参数外，仍有多个参数的构造方法无需explicit关键字修饰。
6. 函数与函数间需要空行，删除不必要的空行。
7. **代码注释不允许使用中文**。
8. 常量值使用constexpr修饰，变量名以k开头。
9. 对于常用的参数校验方法，如正值校验、非负校验，**请定义或使用现有宏函数**，避免重复代码。
10. 对于难以理解的字面值，请将其定义为常量或添加注释进行说明。
11. 重复性的代码需要考虑合并，或定义为工具函数。
12. C++接口注释规范：

    ```cpp
    /// \brief Apply example on the input audio.
    class MS_API Example final : public TensorTransform {
    public:
    /// \brief Constructor.
    /// \param[in] a Xxxxxxxx (Default: 0).
    /// \param[in] b Xxxxxxxx.
    /// \param[in] c Xxxxxxxx.
    /// \param[in] d Xxxxxxxx.
    explicit Example(int32_t a=0, float b, std::string c, std::vector<float> d);
    ```
13. Python接口注释规范：

    ```python
    class Example(AudioTensorOperation):
        """
        Apply example on input audio.

        Args:
            a (int): Xxxxxx.
            b (float, optional): Xxxxxx (default=None).
            c (str, optional): Xxxxxx (default=None).
            d (Union[float, sequence], optional): Xxxxxx (default=None).

        Examples:
            >>> import numpy as np
            >>>
            >>> transforms_list = [audio.Example(a=0, b=1.0)]
            >>> dataset = dataset.map(operations=transforms_list,
            ...                       input_columns=["audio"])
        """
    ```
14. Python接口文档示例中，未完结的代码换行使用...而不是>>>。
15. 报错信息应该准确清晰，需要包括但不限于算子名、参数名、预期结果和实际结果。
16. **新增文件的版权日期应为2022，修改文件的版权日期应为xxxx-2022。**
17. **不要漏掉参数校验用例，需要比较返回错误信息是否符合预期。**
18. **PR中的测试数据不宜过大、过多，尽量自行构造或使用库上已有数据，避免存在版权问题。**
19. 循环语句和条件语句应用大括号包围。
20. 测试用例注释要求：
    Feature: 算子名称
    Description: 描述用例测试的内容
    Expectation: 描述用例运行时预期的现象

    C++

    ```
    /// Feature: Example
    /// Description: test Example in pipeline mode
    /// Expectation: the data is processed successfully
    TEST_F(MindDataTestPipeline, TestExamplePipeline) {
    ```
    Python

    ```
    def test_example_param_check():
        """
        Feature: Example
        Description: test param check of Example 
        Expectation: throw correct error and message
        """
    ```
21. C++接口需要添加MS_API修饰符。

    ```
    class MS_API Example { ... }
    ```