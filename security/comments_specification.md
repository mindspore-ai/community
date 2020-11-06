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
            - [公式](#公式)
            - [链接](#链接)
    - [C++ API注释规范](#c-api注释规范)

<!-- /TOC -->

## 总体说明

- MindSpore Python代码注释遵循[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)，由Sphinx工具自动生成API文档，注释样例和支持情况可参考[Example Google Style Python Docstrings](https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html)和[Support for NumPy and Google style docstrings](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html)。
- MindSpore C++代码需按照命名空间的设计，分别编写Markdown文件。

## Python API注释规范

### 注释格式

类和方法的注释都采用如下格式：

```rst
Summary.

More elaborate description.

Note:
    Description.

Args:
    Arg1 (Type): Description. Default: xxx.
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

- `Summary`：简单描述该接口的功能。
- `More elaborate description`：详细描述该接口的功能和如何使用等信息。
- `Note`：描述使用该接口时需要注意的事项。特别注意不能写成`Notes`。
- `Args`：接口参数信息，包含参数名、参数类型、取值范围、默认值等。
- `Returns`：返回值信息，包含返回值类型等。
- `Raises`：异常信息，包含异常类型、含义等。
- `Examples`：样例代码。

针对算子和Cell的注释，需要在`Examples`前添加`Inputs`和`Outputs`两项内容，用于描述实例化后，算子的输入和输出的类型和shape，输入名可以和样例相同。建议在注释中给出对应的数学公式。

```rst
Inputs:
    - **input_name1** (Type) - Description.
    - **input_name2** (Type) - Description.

Outputs:
    Type and shape, description.
```

### 注意事项

- 整体要求
    - 类或方法必须书写的注释项有：`Summary`、`Args`、`Returns`和`Raises`。如果函数中没有相关信息（如`Args`、`Returns`和`Raises`等），不需要写None（如`Raises：None`），直接省略注释项即可。
    - 以目录为粒度生成API时，__init__文件头部的注释内容会呈现在网页开头；以文件为粒度生成API时，该文件头部的注释内容会呈现在网页开头。这些注释内容需包含相应模块的整体说明。
    - 注释中包含反斜杠时，需要将头部的`"""`改成`r"""`。
    - 冒号要求：关键字（如`Args`、`Returns`等）后面有冒号":"；参数名（如`Arg1`、`Arg2`等）后面有冒号":"，冒号后需有空格。`Summary`和`Returns`的内容中不能包含冒号。
    - 空行要求：不同类型（如`Args`、`Returns`等）的内容之间需有空行，同种类型（如`Arg1`、`Arg2`等）的内容之间不需要空行。采用无序或有序列表描述内容时，整个列表内容与上方内容之间需增加一个空行。
    - 空格要求：`Args`和`Raises`内容的换行需要缩进4个空格，`Args`的子参数或取值、`Inputs`、`Outputs`和`Returns`等无序或有序列表内容的换行不需要缩进，与上一行的正文起始位置对齐。`Args`中参数名和类型的`(`之间需要有空格。
- `Args`注释说明
    - 常见参数类型有：
        - 基本数据类型：`int`、`float`、`bool`、`str`、`list`、`dict`、`set`、`tuple`、`numpy.ndarray`。
        - dtype：如果是mindspore.dtype里的值，写成`mindspore.dtype`，如果是numpy类型，写成`numpy.dtype`。其他按实际情况写。
        - 一个参数有多个可选类型：Union[类型1, 类型2]，如`Union[Tensor, Number]`。
        - list类型：list[具体类型]，如`list[str]`。
        - 可选类型统一格式：(类型, optional)。
        - 其他类型：Tensor或其他具体类型或方法名。
- `Returns`注释说明
    - 如果返回值类型或维度发生变化，需要说明返回值与输入的关系。
    - 多个返回值时，分行写，网页显示时不分行，无序列表的方式可支持分行。
- `Examples`注释说明
    - `Examples`中的内容需在每行代码开头加上```>>>```，多行代码（含类或函数定义、人为换行等）或空行的开头需加上```...```，输出结果行开头不需要加任何符号。
    - `Examples`中需提供实际的代码，如果需提示参考其他Examples，请使用Note。
    - ops算子注释采用PyNative模式写作，可运行的需给出运行结果。
    - 业界共识的情况可省略import，如np、nn等。
    - 导入路径较长和必须自定义别名的导入需要加`from xxx import xxx as something`或`import xxx`，导入路径短的尽量放到代码中。
- `Inputs`和`Outputs`注释说明

    - 类型是Tensor时，需描述shape，并按:math:`(N, C, X)`格式写作。
- 公式
    - 行公式（单独占一行，居中）

      ```rst
      .. math::

         formula
      ```

    - 行内嵌公式（与其他同行文字显示在一起，不居中）

      ```rst
      xxx :math:`formula` xxx
      ```

    - 公式中带有含下划线的变量，且下划线后存在多个字母（如xxx_yyy），请根据实际需要选择以下其中一种方式。
        1. 多个字母用{}括起来（如xxx_{yyy}），可将下划线后的内容作为下标，显示为$xxx_{yyy}$。
        2. 在下划线前增加反斜杠（如xxx\\_yyy），可将完整显示变量名称，显示为xxx_yyy。
- 父类方法的显示
    - 默认不显示父类方法。
    - 可通过在Sphinx工程rst文件的模块下添加`:inherited-members:`，指定需要显示父类方法，详细可参考<https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html>。
- 链接
    - 只显示标题（如例子中的name），不显示详细地址。

        引用的地方需这样写：

        ```rst
        `name`_
        ```

        提供链接的地方需这样写：

        ```rst
        .. _`name`: https://xxx
        ```

        注意：
        - 如有换行请注意缩进，参考下方具体示例。
        - https前需有空格。

        或者可以采用以下简化写法，只在引用的地方写即可。

        ```rst
        `name <https://xxx>`_
        ```

    - 直接显示详细地址。

        ```rst
        https://xxx
        ```

- 表格（详细可参考<https://sublime-and-sphinx-guide.readthedocs.io/en/latest/tables.html#list-table-directive>）

    ```rst
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

    ![image](./resource/list_table.png)

- 详细说明默认不换行，如需换行，需以列表或code-block的方式写作。
    - 列表方式：

        ```rst
        - Content1
        - Content2
        - Content3
        ```

    - code-block方式：

        ```rst
        .. code-block::

        Content1
        Content2
        Content3
        ```

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
            The argument is used to define the data type of the output tensor. If it is None, the data type of the
            output tensor will be as same as the `input_data`. Default: None.

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

显示效果可访问[这里](https://www.mindspore.cn/doc/api_python/zh-CN/master/mindspore/mindspore.html#mindspore.Tensor)。

#### 方法

```python
def ms_function(fn=None, obj=None, input_signature=None):
    """
    Create a callable MindSpore graph from a python function.

    This allows the MindSpore runtime to apply optimizations based on graph.

    Args:
        fn (Function): The Python function that will be run as a graph. Default: None.
        obj (Object): The Python Object that provides the information for identifying the compiled function. Default:
            None.
        input_signature (MetaTensor): The MetaTensor which describes the input arguments. The MetaTensor specifies
            the shape and dtype of the Tensor and they will be supplied to this function. If input_signature
            is specified, each input to `fn` must be a `Tensor`. And the input parameters of `fn` cannot accept
            `**kwargs`. The shape and dtype of actual inputs should keep the same as input_signature. Otherwise,
            TypeError will be raised. Default: None.

    Returns:
        Function, if `fn` is not None, returns a callable function that will execute the compiled function; If `fn` is
        None, returns a decorator and when this decorator invokes with a single `fn` argument, the callable function is
        equal to the case when `fn` is not None.

    Examples:
        >>> def tensor_add(x, y):
        ...     z = F.tensor_add(x, y)
        ...     return z
        ...
        >>> @ms_function
        >>> def tensor_add_with_dec(x, y):
        ...     z = F.tensor_add(x, y)
        ...     return z
        ...
        >>> @ms_function(input_signature=(MetaTensor(mindspore.float32, (1, 1, 3, 3)),
        ...                               MetaTensor(mindspore.float32, (1, 1, 3, 3))))
        >>> def tensor_add_with_sig(x, y):
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

显示效果可访问[这里](https://www.mindspore.cn/doc/api_python/zh-CN/master/mindspore/mindspore.html#mindspore.ms_function)。

#### 公式

```python
class Conv2d(_Conv):
    r"""
    2D convolution layer.

    Applies a 2D convolution over an input tensor which is typically of shape :math:`(N, C_{in}, H_{in}, W_{in})`,
    where :math:`N` is batch size, :math:`C_{in}` is channel number, and :math:`H_{in}, W_{in})` are height and width.
    For each batch of shape :math:`(C_{in}, H_{in}, W_{in})`, the formula is defined as:

    .. math::

        out_j = \sum_{i=0}^{C_{in} - 1} ccor(W_{ij}, X_i) + b_j,

    ...
    """
```

显示效果可访问[这里](https://www.mindspore.cn/doc/api_python/zh-CN/master/mindspore/mindspore.nn.html#mindspore.nn.Conv2d)。

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

显示效果可访问[这里](https://www.mindspore.cn/doc/api_python/zh-CN/master/mindspore/mindspore.ops.html#mindspore.ops.BatchNorm)。

## C++ API注释规范

- Markdown文件命名需与命名空间相同。
- Markdown文件内部格式如下，可参考[样例](https://www.mindspore.cn/doc/api_cpp/zh-CN/master/lite.html)。

  ```markdown
  # The name of namespace
  
  The link of header file.

  ## The name of class

  The description of class.

  The name of attribute or function.

  The description of attribute or function.
  
  ```
