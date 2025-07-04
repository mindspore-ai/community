# MindSpore API注释规范

<!-- TOC -->

- [MindSpore API注释规范](#mindspore-api注释规范)
    - [总体说明](#总体说明)
    - [Python API注释规范](#python-api注释规范)
        - [注释格式](#注释格式)
        - [注意事项](#注意事项)
        - [Python示例](#python示例)
            - [类](#类)
            - [方法](#方法)
            - [基于yaml生成的Tensor方法](#基于yaml文件生成的mindsporetensor方法)
            - [公式](#公式)
            - [链接](#链接)
    - [C++ API注释规范](#c-api注释规范)
        - [注释格式](#注释格式)
        - [注意事项](#注意事项)
        - [完整示例](#完整示例)

<!-- /TOC -->

## 总体说明

- MindSpore Python代码注释遵循[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)，由Sphinx工具自动生成API文档，注释样例和支持情况可参考[Example Google Style Python Docstrings](https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html)和[Support for NumPy and Google style docstrings](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html)。
- MindSpore C++代码需按照命名空间的设计，分别编写Markdown文件。

## Python API注释规范

### 注释格式

类和方法的注释都采用如下格式：

```text
Summary.

More elaborate description.

.. warning::
    Warning description.

Note:
    Note description.

Args:
    Arg1 (Type): Description. Default: ``xxx`` .
    Arg2 (Type): Description.

        - Sub-argument1 or Value1 of Arg2: Description.
        - Sub-argument2 or Value2 of Arg2: Description.

Returns:
    Type, description.

Raises:
    Type: Description.

Examples:
    >>> Sample Code
```

其中，

- `Summary`：简单描述该接口的功能。若该描述为动词开头，模块内需统一用第一人称（即动词原形）或第三人称（即动词后加s），推荐用第一人称。
- `More elaborate description`：详细描述该接口的功能和如何使用等信息。
- `warning`：描述使用该接口时需要警告的事项，以免造成负面影响。
- `Note`：描述使用该接口时需要注意的事项。特别注意不能写成`Notes`。
- `Args`：接口参数信息，包含参数名、参数类型、取值范围、默认值等。
- `Returns`：返回值信息，包含返回值类型等。
- `Raises`：异常信息，包含异常类型、含义等。
- `Examples`：样例代码。

针对算子和Cell的注释，需要在`Examples`前添加`Inputs`、`Outputs`和`Supported Platforms`三项内容。

- `Inputs`和`Outputs`：用于描述实例化后，算子的输入和输出的类型和shape，输入名可以和样例相同。建议在注释中给出对应的数学公式。
- `Supported Platforms`：用于描述算子支持的硬件平台，名称前后需添加``，存在多个时使用空格隔开。

```text
Inputs:
    - **input_name1** (Type) - Description.
    - **input_name2** (Type) - Description.

Outputs:
    Type and shape, description.

Supported Platforms:
    ``Ascend`` ``GPU`` ``CPU``
```

### 注意事项

- 整体要求
    - 类或方法必须书写的注释项有：`Summary`、`Args`、`Returns`和`Raises`。如果函数中没有相关信息（如`Args`、`Returns`和`Raises`等），不需要写None（如`Raises：None`），直接省略注释项即可。
    - 以目录为粒度生成API时，__init__文件头部的注释内容会呈现在网页开头；以文件为粒度生成API时，该文件头部的注释内容会呈现在网页开头。这些注释内容需包含相应模块的整体说明。
    - 注释中包含反斜杠时，需要将头部的`"""`改成`r"""`。
    - 注释内容若为动词开头，模块内需统一用第一人称（即动词原形）或第三人称（即动词后加s），推荐用第一人称。
    - 冒号要求：关键字（如`Args`、`Returns`等）后面有冒号":"；参数名（如`Arg1`、`Arg2`等）后面有冒号":"，冒号后需有空格。`Summary`和`Returns`的内容中不能包含冒号。
    - 空行要求：

        不同类型（如`Args`、`Returns`等）的内容之间需有空行，同种类型（如`Arg1`、`Arg2`等）的内容之间不需要空行。

        ```text
        High-Level API for Training or Testing.

        Args:
            network (Cell): A training or testing network.
            loss_fn (Cell): Objective function, if `loss_fn` is ``None``, the
                network should contain the logic of loss and grads calculation, and the logic
                of parallel if needed. Default: ``None``.

        Returns:
            function, original function.
        ```

        采用无序或有序列表描述内容时，整个列表内容与上方内容之间需增加一个空行。

        ```text
        Args:
            amp_level (str): Option for argument `level` in :func:`mindspore.amp.build_train_network`, level for mixed
                precision training. Supports ``"O0"``, ``"O2"``, ``"O3"``, ``"auto"``. Default: ``"O0"``.

                - ``O0``: Do not change.
                - ``O2``: Cast network to float16, keep batchnorm run in float32, using dynamic loss scale.
                - ``O3``: Cast network to float16, with additional property 'keep_batchnorm_fp32=False'.
                - ``auto``: Set to level to recommended level in different devices. Set level to ``"O2"`` on GPU, set
                  level to ``"O3"`` Ascend. The recommended level is choose by the export experience, cannot
                  always generalize. User should specify the level for special network.

                ``"O2"`` is recommended on GPU, ``"O3"`` is recommended on Ascend.
        ```

    - 空格要求：

        `Args`和`Raises`内容的换行需要缩进4个空格。

        ```text
        Args:
            lr_power (float): Learning rate power controls how the learning rate decreases during training,
                must be less than or equal to zero. Use fixed learning rate if `lr_power` is zero.
            use_locking (bool): If ``True``, the var and accumulation tensors will be protected from being updated.
                Default: ``False``.

        Raises:
            TypeError: If `lr`, `l1`, `l2`, `lr_power` or `use_locking` is not a float.
                If `use_locking` is not a bool.
                If dtype of `var`, `accum`, `linear` or `grad` is neither float16 nor float32.
                If dtype of `indices` is not int32.
        ```

        以下内容的换行不需要缩进，与上一行的正文起始位置对齐。

        1. `Args`的子参数或取值

            ```text
            Args:
                parallel_mode (str): There are five kinds of parallel modes, ``"stand_alone"``, ``"data_parallel"``,
                    ``"hybrid_parallel"``, ``"semi_auto_parallel"`` and ``"auto_parallel"``. Default: ``"stand_alone"``.

                    - ``stand_alone``: Only one processor is working.
                    - ``data_parallel``: Distributes the data across different processors.
                    - ``hybrid_parallel``: Achieves data parallelism and model parallelism
                      manually.
                    - ``semi_auto_parallel``: Achieves data parallelism and model parallelism by
                      setting parallel strategies.
            ```

        2. `Inputs`、`Outputs`和`Returns`等无序或有序列表内容

            ```text
            Inputs:
                - **var** (Parameter) - The variable to be updated. The data type must be float16 or float32.
                - **accum** (Parameter) - The accumulation to be updated, must be same data type and shape as `var`.
                - **linear** (Parameter) - the linear coefficient to be updated, must be same data type and shape
                  as `var`.
                - **grad** (Tensor) - A tensor of the same type as `var`, for the gradient.
                - **indices** (Tensor) - A vector of indices in the first dimension of `var` and `accum`.
                  The shape of `indices` must be the same as `grad` in the first dimension. The type must be int32.

            Outputs:
                Tuple of 3 Tensor, the updated parameters.

                - **var** (Tensor) - Tensor, has the same shape
                  and data type as `var`.
                - **accum** (Tensor) - Tensor, has the same shape
                  and data type as `accum`.
                - **linear** (Tensor) - Tensor, has the same shape
                  and data type as `linear`.
            ```

        3. `Note`和`warning`

            ```text
            .. warning::
                This is warning text. Use a warning for information the user must
                understand to avoid negative consequences.

                If warning text runs over a line, make sure the lines wrap and are indented to
                the same level as the warning tag.
            ```

        `Args`中参数名和类型的`(`之间需要有空格。

        ```text
        Args:
            lr (float): The learning rate value, must be positive.
        ```

- `Args`注释说明
    - 常见参数类型有：
        - 基本数据类型：`int`、`float`、`bool`、`str`、`list`、`dict`、`set`、`tuple`、`numpy.ndarray`。

            ```text
            Args:
                arg1 (int): Some description.
                arg2 (float): Some description.
                arg3 (bool): Some description.
                arg4 (str): Some description.
                arg5 (list): Some description.
                arg6 (dict): Some description.
                arg7 (set): Some description.
                arg8 (tuple): Some description.
                arg9 (numpy.ndarray): Some description.
            ```

        - dtype：如果是mindspore.dtype里的值，写成`mindspore.dtype`，如果是numpy类型，写成`numpy.dtype`。其他按实际情况写。

            ```text
            Args:
                arg1 (mindspore.dtype): Some description.
            ```

        - 一个参数有多个可选类型：Union[类型1, 类型2]，如`Union[Tensor, Number]`。

            ```text
            Args:
                arg1 (Union[Tensor, Number]): Some description.
            ```

        - list类型：list[具体类型]，如`list[str]`。

            ```text
            Args:
                arg1 (list[str]): Some description.
            ```

        - 可选类型统一格式：(类型, optional)。

            ```text
            Args:
                arg1 (bool, optional): Some description.
            ```

        - 其他类型：Tensor或其他具体类型或方法名。

            ```text
            Args:
                arg1 (Tensor): Some description.
            ```

- `Returns`注释说明
    - 如果返回值类型或维度发生变化，需要说明返回值与输入的关系。
    - 多个返回值时，分行写，网页显示时不分行，无序列表的方式可支持分行。

        ```text
        Returns:
            - DatasetNode, the root node of the IR tree.
            - Dataset, the root dataset of the IR tree.
        ```

- `Examples`注释说明
    - `Examples`中的内容需在每行代码开头加上```>>>```，多行代码（含类或函数定义、人为换行等）或空行的开头需加上```...```，输出结果行开头不需要加任何符号。

        ```text
        Examples:
            >>> import mindspore as ms
            >>> import mindspore.nn as nn
            >>> class Net(nn.Cell):
            ...     def __init__(self, dense_shape):
            ...         super(Net, self).__init__()
            ...         self.dense_shape = dense_shape
            ...     def construct(self, indices, values):
            ...         x = SparseTensor(indices, values, self.dense_shape)
            ...         return x.values, x.indices, x.dense_shape
            ...
            >>> indices = Tensor([[0, 1], [1, 2]])
            >>> values = Tensor([1, 2], dtype=ms.float32)
            >>> out = Net((3, 4))(indices, values)
            >>> print(out[0])
            [1. 2.]
            >>> print(out[1])
            [[0 1]
             [1 2]]
            >>> print(out[2])
            (3, 4)
        ```

    - `Examples`中需提供实际的代码，如果需提示参考其他Examples，请使用Note。
    - ops算子注释采用PyNative模式写作，可运行的需给出运行结果。
    - 业界共识的情况可省略import，如np、nn等。
    - 导入路径较长和必须自定义别名的导入需要加`from xxx import xxx as something`或`import xxx`，导入路径短的尽量放到代码中。
- `Inputs`和`Outputs`注释说明

    - 类型是Tensor时，需描述shape，并按:math:\`(N, C, X)\`格式写作。
- 公式
    - 行公式（单独占一行，居中）

      ```text
      .. math::

         formula
      ```

    - 行内嵌公式（与其他同行文字显示在一起，不居中）

      ```text
      xxx :math:`formula` xxx
      ```

    - 公式中带有含下划线的变量，且下划线后存在多个字母（如xxx_yyy），请根据实际需要选择以下其中一种方式。
        1. 多个字母用{}括起来（如xxx_{yyy}），可将下划线后的内容作为下标，显示为$xxx_{yyy}$。
        2. 在下划线前增加反斜杠（如xxx\\_yyy），可将完整显示变量名称，显示为xxx_yyy。

    - 公式中正斜体规范
        - 以下情况用斜体
            1. 变量（直接书写，无需加特殊符号）

                ```text
                x, p, a, h, ...
                ```

            2. 小写希腊字母

                ```text
                \alpha, \beta, \gamma, \sigma, \theta, \pi, ...
                ```

        - 以下情况用正体
            1. 有固定含义的数学函数，如：exp, log, sin, cos, tanh

                ```text
                \exp, \log, \sin, \cos, \tanh, ...
                ```

            2. 有特殊数学意义的缩写字母，如：max, min, lim, sum, ...

                ```text
                \max, \min, \lim, \sum, ...
                ```

            3. 其他专有名词（用\text包裹）

                ```text
                \text{sigmoid}, \test{Tanh} ...
                ```

- 父类方法的显示
    - 默认不显示父类方法。
    - 可通过在Sphinx工程rst文件的模块下添加`:inherited-members:`，指定需要显示父类方法，详细可参考<https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html>。
- 链接
    - 只显示标题（如例子中的name），不显示详细地址。

        引用的地方需这样写：

        ```text
        `name`_
        ```

        提供链接的地方需这样写：

        ```text
        .. _`name`: https://xxx
        ```

        注意：
        - 如有换行请注意缩进，参考下方具体示例。
        - https前需有空格。

        或者可以采用以下简化写法，只在引用的地方写即可。

        ```text
        `name <https://xxx>`_
        ```

    - 直接显示详细地址。

        ```text
        https://xxx
        ```

- 表格（详细可参考<https://sublime-and-sphinx-guide.readthedocs.io/en/latest/tables.html#list-table-directive>）

    ```text
    .. list-table:: Title            # 表格标题
    :widths: 25 25 25               # 表格列宽
    :header-rows: 1

    * - Heading row 1, column 1     # 表头
        - Heading row 1, column 2
        - Heading row 1, column 3
    * - Row 1, column 1
        -                             # 表格内容为空
        - Row 1, column 3
    * - Row 2, column 1
        - Row 2, column 2
        - Row 2,
                                    # 表格内容如需换行，在中间增加一个空行
        column 3
    ```

    显示效果：

    ![image](./images/list_table.png)

- 详细说明默认不换行，如需换行，需以列表或code-block的方式写作。
    - 列表方式：

        ```text
        - Content1
        - Content2
        - Content3
        ```

    - code-block方式：

        ```text
        .. code-block::

        Content1
        Content2
        Content3
        ```

- 在注释中引用其他接口。

    - 引用class。

      只写接口名：

      ```text
      :class:`AdamNoUpdateParam`
      ```

      若存在重复接口名，则需引用完整模块名和类名：

      ```text
      :class:`mindspore.ops.LARS`
      ```

    - 引用function，必须写上完整模块名和函数名。

      ```text
      :func:`mindspore.compression.quant.create_quant_config`
      ```

- 接口描述中，变量名或接口名使用符号\`包裹，变量值使用符号\`\`包裹。

    - 变量名或接口名。

      ```text
      This part is a more detailed overview of `Mul` operation. For more details about Quantization,
      please refer to the implementation of subclass of `Observer`.

      Other losses derived from this should implement their own `construct` and use method `self.get_loss`
      to apply reduction to loss values.
      ```

    - 变量值。

      ```text
      If `reduction` is not one of ``'none'``, ``'mean'``, ``'sum'``.
      ```

- 废弃算子需要写明建议使用的接口，以及需要在支持平台中写上Deprecated。

    ```python
    class BasicLSTMCell(PrimitiveWithInfer):
        """
        It's similar to operator :class:`DynamicRNN`. BasicLSTMCell will be deprecated in the future.
        Please use :class:`DynamicRNN` instead.

        Supported Platforms:
            Deprecated
        """
    ```

- 添加图片。

    格式：`.. image:: {name.png}`。

    其中`{name.png}`为图片名称，并将图片提交到<https://gitee.com/mindspore/mindspore/tree/master/docs/api/api_python>中对应模块的目录下。

    如在`mindspore.dataset.audio.transforms.FrequencyMasking`接口注释中添加图片`frequency_masking.png`：

    ```python
    class FrequencyMasking(AudioTensorOperation):
    """
    Some description.

    .. image:: frequency_masking.png
    """
    ```

    并将图片提交至：<https://gitee.com/mindspore/mindspore/blob/master/docs/api/api_python/dataset_audio/frequency_masking.png>。

### Python示例

#### 类

```python
class Tensor(Tensor_):
    """
    Tensor is used for data storage.

    Tensor inherits tensor object in C++.
    Some functions are implemented in C++ and some functions are implemented in Python.

    Args:
        input_data (Tensor, float, int, bool, tuple, list, numpy.ndarray): Input data of the tensor.
        dtype (:class:`mindspore.dtype`): Input data should be None, bool or numeric type defined in `mindspore.dtype`.
            The argument is used to define the data type of the output tensor. If it is ``None``, the data type of the
            output tensor will be as same as the `input_data`. Default: ``None``.

    Outputs:
        Tensor, with the same shape as `input_data`.

    Examples:
        >>> # initialize a tensor with input data
        >>> t1 = Tensor(np.zeros([1, 2, 3]), mindspore.float32)
        >>> assert isinstance(t1, Tensor)
        >>> assert t1.shape == (1, 2, 3)
        >>> assert t1.dtype == mindspore.float32
        ...
        >>> # initialize a tensor with a float scalar
        >>> t2 = Tensor(0.1)
        >>> assert isinstance(t2, Tensor)
        >>> assert t2.dtype == mindspore.float64
    """

    def __init__(self, input_data, dtype=None):
        ...
```

显示效果可访问[这里](https://www.mindspore.cn/docs/en/master/api_python/mindspore/mindspore.Tensor.html)。

#### 方法

```python
def ms_function(fn=None, obj=None, input_signature=None):
    """
    Create a callable MindSpore graph from a python function.

    This allows the MindSpore runtime to apply optimizations based on graph.

    Args:
        fn (Function): The Python function that will be run as a graph. Default: ``None``.
        obj (Object): The Python Object that provides the information for identifying the compiled function. Default:
            ``None``.
        input_signature (MetaTensor): The MetaTensor which describes the input arguments. The MetaTensor specifies
            the shape and dtype of the Tensor and they will be supplied to this function. If `input_signature`
            is specified, each input to `fn` must be a `Tensor`. And the input parameters of `fn` cannot accept
            `**kwargs`. The shape and dtype of actual inputs should keep the same as `input_signature`. Otherwise,
            TypeError will be raised. Default: ``None``.

    Returns:
        Function, if `fn` is not ``None``, returns a callable function that will execute the compiled function; If `fn` is
        ``None``, returns a decorator and when this decorator invokes with a single `fn` argument, the callable function is
        equal to the case when `fn` is not ``None``.

    Examples:
        >>> def tensor_add(x, y):
        ...     z = F.tensor_add(x, y)
        ...     return z
        ...
        >>> @ms_function
        ... def tensor_add_with_dec(x, y):
        ...     z = F.tensor_add(x, y)
        ...     return z
        ...
        >>> @ms_function(input_signature=(MetaTensor(mindspore.float32, (1, 1, 3, 3)),
        ...                               MetaTensor(mindspore.float32, (1, 1, 3, 3))))
        ... def tensor_add_with_sig(x, y):
        ...     z = F.tensor_add(x, y)
        ...     return z
        ...
        >>> x = Tensor(np.ones([1, 1, 3, 3]).astype(np.float32))
        >>> y = Tensor(np.ones([1, 1, 3, 3]).astype(np.float32))
        ...
        >>> tensor_add_graph = ms_function(fn=tensor_add)
        >>> out = tensor_add_graph(x, y)
        >>> out = tensor_add_with_dec(x, y)
        >>> out = tensor_add_with_sig(x, y)
    """
    ...
```

显示效果可访问[这里](https://www.mindspore.cn/docs/en/master/api_python/mindspore/mindspore.ms_function.html)。

#### 基于yaml文件生成的mindspore.Tensor方法

```text
gather:
  description: |
    gather(dim, index) -> Tensor

    Gather data from a tensor by indices.

    .. math::
        output[(i_0, i_1, ..., i_{dim}, i_{dim+1}, ..., i_n)] =
        input[(i_0, i_1, ..., index[(i_0, i_1, ..., i_{dim}, i_{dim+1}, ..., i_n)], i_{dim+1}, ..., i_n)]

    .. warning::
        On Ascend, the behavior is unpredictable in the following cases:

        - the value of `index` is not in the range `[-self.shape[dim], self.shape[dim])` in forward;
        - the value of `index` is not in the range `[0, self.shape[dim])` in backward.

    Args:
        dim (int): the axis to index along, must be in range `[-self.rank, self.rank)`.
        index (Tensor): The index tensor, with int32 or int64 data type. An valid `index` should be:

            - `index.rank == self.rank`;
            - for `axis != dim`, `index.shape[axis] <= self.shape[axis]`;
            - the value of `index` is in range `[-self.shape[dim], self.shape[dim])`.

    Returns:
        Tensor, has the same type as `self` and the same shape as `index`.

    Raises:
        ValueError: If the shape of `index` is illegal.
        ValueError: If `dim` is not in `[-self.rank, self.rank)`.
        ValueError: If the value of `index` is out of the valid range.
        TypeError: If the type of `index` is illegal.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> import mindspore
        >>> import numpy as np
        >>> from mindspore import Tensor
        >>> input = Tensor(np.array([[-0.1, 0.3, 3.6], [0.4, 0.5, -3.2]]), mindspore.float32)
        >>> index = Tensor(np.array([[0, 0], [1, 1]]), mindspore.int32)
        >>> output = input.gather(1, index)
        >>> print(output)
        [[-0.1 -0.1]
         [0.5   0.5]]

    .. method:: Tensor.gather(input_indices, axis, batch_dims=0) -> Tensor
        :noindex:

    Returns the slice of the input tensor corresponding to the elements of `input_indices` on the specified `axis`.

    The following figure shows the calculation process of Gather commonly:

    .. image:: ../../images/Gather.png

    where params represents the input `input_params`, and indices represents the index to be sliced `input_indices`.

    .. note::
        1. The value of input_indices must be in the range of `[0, input_param.shape[axis])`.
           On CPU and GPU, an error is raised if an out of bound indice is found. On Ascend, the results may be
           undefined.
        2. The data type of self cannot be
           `bool_ <https://www.mindspore.cn/docs/en/master/api_python/mindspore/mindspore.dtype.html>`_ on Ascend
           platform currently.

    Args:
        input_indices (Tensor): Index tensor to be sliced, the shape of tensor is :math:`(y_1, y_2, ..., y_S)`.
            Specifies the indices of elements of the original Tensor. The data type can be int32 or int64.
        axis (Union(int, Tensor[int])): Specifies the dimension index to gather indices.
            It must be greater than or equal to `batch_dims`.
            When `axis` is a Tensor, the size must be 1.
        batch_dims (int): Specifies the number of batch dimensions. It must be less than or euqal to the rank
            of `input_indices`. Default: ``0`` .

    Returns:
        Tensor, the shape of tensor is
        :math:`input\_params.shape[:axis] + input\_indices.shape[batch\_dims:] + input\_params.shape[axis + 1:]`.

    Raises:
        TypeError:  If `axis` is not an int or Tensor.
        ValueError: If `axis` is a Tensor and its size is not 1.
        TypeError:  If `self` is not a tensor.
        TypeError:  If `input_indices` is not a tensor of type int.
        RuntimeError: If `input_indices` is out of range `[0, input_param.shape[axis])` on CPU or GPU.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> import mindspore
        >>> import numpy as np
        >>> from mindspore import Tensor
        >>> # case1: input_indices is a Tensor with shape (5, ).
        >>> input_params = Tensor(np.array([1, 2, 3, 4, 5, 6, 7]), mindspore.float32)
        >>> input_indices = Tensor(np.array([0, 2, 4, 2, 6]), mindspore.int32)
        >>> axis = 0
        >>> output = input_params.gather(input_indices=input_indices, axis=axis)
        >>> print(output)
        [1. 3. 5. 3. 7.]
        >>> # case2: input_indices is a Tensor with shape (2, 2). When the input_params has one dimension,
        >>> # the output shape is equal to the input_indices shape.
        >>> input_indices = Tensor(np.array([[0, 2], [2, 6]]), mindspore.int32)
        >>> axis = 0
        >>> output = input_params.gather(input_indices=input_indices, axis=axis)
        >>> print(output)
        [[1. 3.]
         [3. 7.]]
        >>> # case3: input_indices is a Tensor with shape (2, ) and
        >>> # input_params is a Tensor with shape (3, 4) and axis is 0.
        >>> input_params = Tensor(np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]), mindspore.float32)
        >>> input_indices = Tensor(np.array([0, 2]), mindspore.int32)
        >>> axis = 0
        >>> output = input_params.gather(input_indices=input_indices, axis=axis)
        >>> print(output)
        [[ 1.  2.  3.  4.]
         [ 9. 10. 11. 12.]]
        >>> # case4: input_indices is a Tensor with shape (2, ) and
        >>> # input_params is a Tensor with shape (3, 4) and axis is 1, batch_dims is 1.
        >>> input_params = Tensor(np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]), mindspore.float32)
        >>> input_indices = Tensor(np.array([0, 2, 1]), mindspore.int32)
        >>> axis = 1
        >>> batch_dims = 1
        >>> output = input_params.gather(input_indices, axis, batch_dims)
        >>> print(output)
        [ 1.  7. 10.]
```

- 首行注释为接口定义， 格式为 `xxx(param1, param2)`，不需要加类名前缀Tensor，直接写接口名即可。
- 有重载函数时，不需要顶格书写，与正文缩进一样，使用 `.. method:: Tensor.xxx` ，并换行再缩进4格添加标签 `:noindex:` ，注意不要用 `mindspore.Tensor.xxx` 作为定义。
- 使用 `.. image:: ../xxx.png` 引用图片时，以中文文档与图片的相对位置为准，英文注释写法与中文文档保持一致。
- 如果需要引用 `mindspore.Tensor.xxx` 相关接口的内容，推荐写成 :func:`Tensor.xxx` 。

显示效果可访问[这里](https://www.mindspore.cn/docs/en/master/api_python/mindspore/Tensor/mindspore.Tensor.gather.html)。

#### 公式

```python
class Conv2d(_Conv):
    r"""
    2D convolution layer.

    Apply a 2D convolution over an input tensor which is typically of shape :math:`(N, C_{in}, H_{in}, W_{in})`,
    where :math:`N` is batch size, :math:`C_{in}` is channel number, and :math:`H_{in}, W_{in})` are height and width.
    For each batch of shape :math:`(C_{in}, H_{in}, W_{in})`, the formula is defined as:

    .. math::

        out_j = \sum_{i=0}^{C_{in} - 1} ccor(W_{ij}, X_i) + b_j,

    ...
    """
```

显示效果可访问[这里](https://www.mindspore.cn/docs/en/master/api_python/nn/mindspore.nn.Conv2d.html)。

#### 链接

```python
class BatchNorm(PrimitiveWithInfer):
    r"""
    Batch Normalization for input data and updated parameters.

    Batch Normalization is widely used in convolutional neural networks. This operation
    applies Batch Normalization over input to avoid internal covariate shift as described
    in the paper `Batch Normalization: Accelerating Deep Network Training by Reducing Internal
    Covariate Shift <https://arxiv.org/abs/1502.03167>`_. It rescales and recenters the
    features using a mini-batch of data and the learned parameters which can be described
    in the following formula,

    ...
    """
```

显示效果可访问[这里](https://www.mindspore.cn/docs/en/master/api_python/ops/mindspore.ops.BatchNorm.html)。

## C++ API注释规范

### 注释格式

所有接口注释都采用如下格式：

```cpp
/// \brief Short description
///
/// Detailed description.
///
/// \note
/// Describe what to be aware of when using this interface.
///
/// \f[
/// math formula
/// \f]
/// XXX \f$ formulas in the line \f$ XXX
///
/// \param[in] Parameter_name meaning, range of values, other instructions.
///
/// \return Returns a description of the value, the cause of the error,
///     and the corresponding solution.
///
/// \par Example
/// \code
/// Example code
/// \endcode
```

其中：

- `\brief`：简要描述。

    ```cpp
    /// \brief Function to create a CocoDataset.
    ```

- `Detailed description`：详细描述。

    ```cpp
    ///  Base class for all recognizable patterns.
    ///  We implement an Expression Template approach using static polymorphism based on
    ///  the Curiously Recurring Template Pattern (CRTP) which "achieves a similar effect
    ///  to the use of virtual functions without the costs..." as described in:
    ///  https://en.wikipedia.org/wiki/Expression_templates and
    ///  https://en.wikipedia.org/wiki/Curiously_recurring_template_pattern
    ///  The TryCapture function tries to capture the pattern with the given node.
    ///  The GetNode function builds a new node using the captured values.
    ```

- `\note`：使用该接口的注意事项。

    ```cpp
    /// \note
    /// The generated dataset has multi-columns
    ```

- 公式写法。

    多行公式写法：

    ```cpp
    /// \f[
    /// x>=y
    /// \f]
    ```

    行内公式写法，公式位于两个`\f$`之间：

    ```cpp
    /// \brief Computes the boolean value of \f$x>=y\f$ element-wise.
    ```

- `\param[in]`：传入参数描述。

    ```cpp
    /// \param[in] weight Defines the width of memory to request
    /// \param[in] height Defines the height of memory to request
    /// \param[in] type Defines the data type of memory to request
    ```

- `\return`：返回值描述。

    ```cpp
    /// \return Reference count of a certain memory currently.
    ```

- 示例代码，格式如下，`\par Example`作为前缀，示例代码位于`\code`和`\endcode`之间：

    ```cpp
    /// \par Example
    /// \code
    /// /* Set number of workers(threads) to process the dataset in parallel */
    /// std::shared_ptr<Dataset> ds = ImageFolder(folder_path, true);
    /// ds = ds->SetNumWorkers(16);
    /// \endcode
    ```

### 注意事项

1. 需要生成文档的接口注释内容统一使用`///`引导而不是使用`//`引导；
2. 不要间断注释，空行使用`///`；
3. 引用在C++ API中具有同名的外部名称时，避免生成错误链接，需要在前面添加`@ref`标识：

    ```cpp
    /// \brief Referring to @ref mindspore.nn.Cell for detail.
    ```

### 完整示例

```cpp
/// \brief Function to create a MnistDataset.
/// \note The generated dataset has two columns ["image", "label"].
/// \param[in] dataset_dir Path to the root directory that contains the dataset.
/// \param[in] usage Part of dataset of MNIST, can be "train", "test" or "all" (default = "all").
/// \param[in] sampler Shared pointer to a sampler object used to choose samples from the dataset. If sampler is not
///     given, a `RandomSampler` will be used to randomly iterate the entire dataset (default = RandomSampler()).
/// \param[in] cache Tensor cache to use (default=nullptr which means no cache is used).
/// \return Shared pointer to the MnistDataset.
/// \par Example
/// \code
///      /* Define dataset path and MindData object */
///      std::string folder_path = "/path/to/mnist_dataset_directory";
///      std::shared_ptr<Dataset> ds = Mnist(folder_path, "all", std::make_shared<RandomSampler>(false, 20));
///
///      /* Create iterator to read dataset */
///      std::shared_ptr<Iterator> iter = ds->CreateIterator();
///      std::unordered_map<std::string, mindspore::MSTensor> row;
///      iter->GetNextRow(&row);
///
///      /* Note: In MNIST dataset, each dictionary has keys "image" and "label" */
///      auto image = row["image"];
/// \endcode
inline std::shared_ptr<MnistDataset> MS_API
Mnist(const std::string &dataset_dir, const std::string &usage = "all",
      const std::shared_ptr<Sampler> &sampler = std::make_shared<RandomSampler>(),
      const std::shared_ptr<DatasetCache> &cache = nullptr) {
  return std::make_shared<MnistDataset>(StringToChar(dataset_dir), StringToChar(usage), sampler, cache);
}
```

根据以上注释内容输出的API文档页面为[Function mindspore::dataset::Coco](https://www.mindspore.cn/lite/api/en/master/generate/function_mindspore_dataset_Mnist-1.html)。
