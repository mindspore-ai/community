# 代码上库规范

* 规范1：PR标题与commit信息保持一致
* 规范2：一个PR只允许有一个提交记录，多个commit需要rebase合一，防止冗余的commit信息
* 规范3：描述清楚PR解决的问题（What does this PR do / why do we need it）
* 规范4：一个PR只能解决一个问题，禁止将多个问题放在一个PR提交
* 规范5：每个PR必须关联对应的issue（需求/Bug/Task/……），做到issue解决记录可跟踪，PR禁止合入与issue无关代码
* 规范6：禁止开发approve自己的PR
* 规范7：每个代码检视人员的检视意见必须有效闭环，由检视人员勾选“已解决”选项
* 规范8：CI门禁不过，禁止强行合入
* 规范9：每个PR提交前需做本地告警清零，都要有本地新增告警清零
* 规范10：特性或bugfix必须补充用例（增量代码LLT覆盖率>=80%），如无用例，需澄清原因且经过committer认可
* 建议1：每个PR建议不超过200行代码（减掉用例代码）

## 用例上库规范

* ST用例运行方式: MindSpore Python语言的ST用例仅支持pytest方式运行（不支持python直接运行），文件名以 `st_`开头，支持在一个文件中定义多个用例，门禁不支持传递参数，需要在用例中设置运行参数。
* 目录结构: 存放在tests/st目录
* 门禁使能: 在 `test_用例名称`的上面添加以下字段（注意事项：用例不要绑Device ID，直接使用Device ID就可以了）

    * Ascend910 单P用例:

    ```python
    @pytest.mark.level0           # 说明: level0: 门禁构建用例   level1~level2: 版本构建用例
    @pytest.mark.platform_arm_ascend_training
    @pytest.mark.platform_x86_ascend_training
    @pytest.mark.env_onecard      # 说明: env_onecard为单P
    def test_resnet_cifar_1p():
        xxx
        xxx
    ```

    * Ascend910 8P用例:

    ```python
    @pytest.mark.level0           # 说明: level0: 门禁构建用例   level1~level2: 版本构建用例
    @pytest.mark.platform_arm_ascend_training
    @pytest.mark.platform_x86_ascend_training
    @pytest.mark.env_single       # 说明: env_single为8P
    def test_resnet_cifar_8p():
        xxx
        xxx
    ```

    * GPU单P用例:

    ```python
    @pytest.mark.level0           # 说明: level0: 门禁构建用例   level1~level2: 版本构建用例
    @pytest.mark.platform_x86_gpu_training     # training 执行在Tesla V100; inference 执行在Tesla P4 (当前不提供)
    @pytest.mark.env_onecard      # 说明: env_onecard为单P，env_single为8P
    def test_LSTM():
        xxx
        xxx
    ```

    * CPU用例:

    ```python
    @pytest.mark.level0           # 说明: level0: 门禁构建用例   level1~level2: 版本构建用例
    @pytest.mark.platform_x86_cpu
    @pytest.mark.platform_arm_cpu
    @pytest.mark.env_onecard      # 说明: 仅有env_onecard（CPU没有8P用例）
    def test_lenet():
        xxx
        xxx
    ```

    * Ascend310 单P用例:

    ```python
    @pytest.mark.level0           # 说明: level0: 门禁构建用例   level1~level2: 版本构建用例
    @pytest.mark.platform_arm_ascend310_inference
    @pytest.mark.platform_x86_ascend310_inference
    @pytest.mark.env_onecard      # 说明: env_onecard为单P, ascend310暂无多卡场景
    def test_resnet_cifar_1p():
        xxx
        xxx
    ```

* 导包规则

  * 调用 `tests/st/tbe_networks/resnet.py`中的 `resnet50`，则导入包名为：

    ```python
    from test.st.tbe_networks.resnet import resnet50
    ```

  * 调用 `models`目录中的包，导入包名为：

    ```python
    from models.bert.src.xxx
    ```

  * 调用 `example`目录中的包，导入包名为：

    ```python
    from example.xxx.xxx
    ```

* 数据集约定目录

  * 输入数据集目录：`/home/workspace/mindspore_dataset`
    例如: cifar10数据集：`/home/workspace/mindspore_dataset/cifar-10-batches-bin`
  * 配置文件目录: `/home/workspace/mindspore_config`
    例如: `/home/workspace/mindspore_config/hccl/rank_table_8p.json`
  * 注意事项: 数据集不要上库，找CIE存放在运行环境中
