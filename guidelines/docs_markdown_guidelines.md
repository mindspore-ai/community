# MindSpore Markdown文档写作要求

<!-- TOC -->

- [MindSpore Markdown文档写作要求](#mindspore-markdown文档写作要求)
    - [文档命名](#文档命名)
    - [标题](#标题)
    - [gitee链接](#gitee链接)
    - [概述](#概述)
    - [注意事项](#注意事项)
    - [有序/无序列表](#有序无序列表)
    - [代码样例](#代码样例)
    - [图片](#图片)
    - [表格](#表格)
    - [术语](#术语)
    - [参考文献](#参考文献)
    - [格式](#格式)
    - [英文](#英文)

<!-- /TOC -->

## 文档命名

Markdown文件名和图片名使用全小写，单词间可使用_分隔。

## 标题

- 标题仅支持Atx风格，标题与上下文需用空行隔开。
- 标题最多不超过4级（####）。

示例：

```text
# 一级标题

## 二级标题

### 三级标题
```

## gitee链接

每个Markdown文件添加链到自身的gitee链接，方便在网页上直接跳转到gitee页面。

- 文中使用gitee链接时，目录应为`https://gitee.com/mindspore/docs/tree/xxx`，文件应为`https://gitee.com/mindspore/docs/blob/xxx`。

示例：

```markdown
<a href="https://gitee.com/mindspore/docs/blob/master/tutorials/source_zh_cn/beginner/quick_start.ipynb" target="_blank"><img src="https://gitee.com/mindspore/docs/raw/master/resource/_static/logo_source.png"></a>
```

## 概述

要求描述以下内容：

- 主题内容相关技术的背景、介绍以及给用户带来的好处。
- MindSpore在各平台的支持情况。
- 完整样例代码的链接。

## 注意事项

注意事项使用“>”标识。

示例：

```text
> 注意事项内容。
```

多条示例：

```text
> - 注意事项内容。
> - 注意事项内容。
```

受Sphinx工具解析限制，注意事项中只能列举单行代码。

```text
> 注意事项内容，`code`。
```

## 有序/无序列表

- 有序/无序列表下的详细内容需缩进4格写作。
- 标题和内容间需增加一个空行，否则可能无法实现换行。

示例：

````text
1. 内容1。

    详细说明。

    ```
    code
    ```

2. 内容2。

    详细说明。

    ```
    code
    ```

````

````text
- 内容1。

    详细说明。

    ```
    code
    ```

- 内容2。

    详细说明。

    ```
    code
    ```

````

## 代码样例

- 教程和文档中不可出现下划线开头的内部接口。
- 注释要求使用英文写作。
- Python函数、方法、类的注释使用```"""```。
- Python其他代码注释使用```#```。
- C++代码注释使用```//```。

示例：

```text
"""
Python函数、方法、类的注释
"""

# Python代码注释

// C++代码注释

```

## 图片

- 教程和文档的图片中不出现个人信息。
- 采用Markdown格式写，不要采用html格式写。
- 图和上下文需增加一个空行，否则会导致排版异常。
- 图片放置在临近的images目录下。

示例：

```text
![xxx](./xxx.png)
```

## 表格

- 表格前后需增加一个空行，否则会导致排版异常。
- 采用Markdown格式写，不要采用html格式写。
- 有序或无序列表内不支持表格。

示例：

```text
## 文章标题

| 表头1   | 表头2
| -----   | ----
| 内容I1  | 内容I2
| 内容II1 | 内容II2

下文内容。
```

## 术语

统一术语大小写：MindSpore、CIFAR-10、Python等。详见[术语表](https://www.mindspore.cn/docs/zh-CN/master/design/glossary.html)。

## 参考文献

- 参考文献需列举在文末，并在文中标注。
- 引用文字或图片说明后，增加标注[编号]。

示例：

```text
## 参考文献

[1] 作者. [有链接的文献名](http://xxx).

[2] 作者. 没有链接的文献名.
```

## 格式

- 教程、文档中引用接口、路径名、文件名等使用“\` \`”标注，如果是函数或方法，最后不加括号。

    引用方法示例：

    ```text
    使用映射 `map` 方法。
    ```

    引用代码示例：

    ```text
    `batch_size`：每组包含的数据个数。
    ```

    引用路径示例：

    ```text
    将数据集解压存放到工作区`./MNIST_Data`路径下。
    ```

    引用文件名示例：

    ```text
    其他依赖项在`requirements.txt`中有详细描述。
    ```

- 教程、文档中待用户替换的内容需要额外标注，在正文中，使用“*”包围需要替换内容，在代码片段中，使用“{}”包围替换内容。

    正文中示例：

    ```text
    需要替换你的本地路径*your_path*。
    ```

    代码片段中示例：

    ```text
    conda activate {your_env_name}
    ```

## 英文

- 中英文内容需同步修改。
- 英文文档需链英文链接。如将`zh-CN`改成`en`。
