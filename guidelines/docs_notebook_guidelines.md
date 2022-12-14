# MindSpore Notebook文档写作要求

<!-- TOC -->

- [MindSpore Notebook文档写作要求](#mindspore-notebook文档写作要求)
    - [文档命名](#文档命名)
    - [单元格组成](#单元格组成)
    - [内容大纲](#内容大纲)
    - [文档相关文件存放](#文档相关文件存放)
    - [图片](#图片)
    - [表格](#表格)
    - [其他](#其他)

<!-- /TOC -->

## 文档命名

ipynb文件名和图片名使用全小写，单词间可使用_分隔。

## 单元格组成

Notebook文档使用Markdown和运行代码两种单元格组合的形式。

- Markdown单元格格式要求参考[MindSpore Markdown文档写作要求](./docs_markdown_guidelines.md)。
- 运行代码单元格格式要求参考编码规范。

## 内容大纲

1. 标题（与当前主题相关）：`# xxxx`。
2. 作者：名字加Gitee或Github个人链接。
3. 资源链接标签：使用“图片+链接”的格式，`&emsp;`表示分隔符。

    如：

    ```text
    [![在线运行](https://gitee.com/mindspore/docs/raw/master/resource/_static/logo_modelarts.png)](https://authoring-modelarts-cnnorth4.huaweicloud.com/console/lab?share-url-b64=aHR0cHM6Ly9taW5kc3BvcmUtd2Vic2l0ZS5vYnMuY24tbm9ydGgtNC5teWh1YXdlaWNsb3VkLmNvbS9ub3RlYm9vay9tb2RlbGFydHMvbWluZHNwb3JlX3F1aWNrX3N0YXJ0LmlweW5i&imageid=65f636a0-56cf-49df-b941-7d2a07ba8c8c)&emsp;[![下载Notebook](https://gitee.com/mindspore/docs/raw/master/resource/_static/logo_notebook.png)](https://obs.dualstack.cn-north-4.myhuaweicloud.com/mindspore-website/notebook/master/tutorials/zh_cn/beginner/mindspore_quick_start.ipynb)&emsp;[![下载样例代码](https://gitee.com/mindspore/docs/raw/master/resource/_static/logo_download_code.png)](https://obs.dualstack.cn-north-4.myhuaweicloud.com/mindspore-website/notebook/master/tutorials/zh_cn/beginner/mindspore_quick_start.py)&emsp;[![查看源文件](https://gitee.com/mindspore/docs/raw/master/resource/_static/logo_source.png)](https://gitee.com/mindspore/docs/blob/master/tutorials/source_zh_cn/beginner/quick_start.ipynb)
    ```

    每个链接构成的方法如下：

    - 在线运行：

        ```text
        authoring-modelarts-cnnorth4.huaweicloud.com/console/lab?share-url-bs64={Notebook存储地址的base64编码}&image_id={镜像id}
        ```

    - 下载Notebook：

        ```text
        obs.dualstack.cn-north-4.myhuaweicloud.com/mindspore-website/notebook/{Gitee中docs仓的分支}/{中文zh_cn/英文en}/{Gitee仓库中该Notebook的地址}
        ```

    - 下载样例代码：

        ```text
        obs.dualstack.cn-north-4.myhuaweicloud.com/mindspore-website/notebook/{Gitee中docs仓的分支}/{中文zh_cn/英文en}/{Gitee仓库中该Notebook对应的py文件地址}
        ```

        后缀由.ipynb改为.py。

    - 查看源文件：Gitee仓库中该Notebook文件的地址。

4. 概述。
5. 整体流程。
6. 说明（完整样例代码地址、硬件/系统/平台支持情况）。
7. 准备环节：包括环境配置信息等。
8. 数据集加载、导入公共模块（非必要的话尽量和使用到的代码放在一起）。
9. 数据预处理。
10. 文档主要内容：进行训练、验证精度等。
11. 总结（与当前主题相关）。

补充说明：

- 整体结构可以参考[快速入门](https://gitee.com/mindspore/docs/blob/master/tutorials/source_zh_cn/beginner/quick_start.ipynb)。
- 内容中不要含有个人信息（可以在文件开头附加作者和个人链接）。
- 每个代码单元格建议有输出结果展示，帮助用户加深理解。
- 要求可全文档一键重复多次运行（注意：需编写相关代码在重复运行时删除过期或无效的相关文件）。

## 文档相关文件存放

1. 文中使用到的数据集需要提供可下载的链接地址。

2. 代码中相关文件存放的路径（供参考，可根据实际情况调整）：

    - 训练的模型路径设置为：`./model/{模型文件类型}/{ipynb的文件名}/{模型文件}`。

        常用的模型文件类型有：

        - `ckpt`：CheckPoint格式文件。
        - `mindir`：MindIR格式文件。
        - `onnx`：ONNX格式文件。
        - `air`：AIR格式文件。
    - 数据集放置位置设置为：

        - 常用数据集：

            - 常用数据集路径写为：`./datasets/{数据集名称}/{数据文件}`。
            - 训练数据集路径写为：`./datasets/{ipynb的文件名}/{数据集名称}/train/{数据文件}`。
            - 测试数据集路径写为：`./datasets/{ipynb的文件名}/{数据集名称}/test/{数据文件}`。
        - 自定义数据集：

            - 单张图片的存放

                例如 `test.jpg`文件，放置路径：`./datasets/{ipynb的文件名}/images/test.jpg`。
            - 单个文件的存放

                例如 `test.csv`文件，放置路径：`./datasets/{ipynb的文件名}/docs/test.csv`。
            - MindRecord数据放置

                原始MindRecord数据放置在：`./datasets/{ipynb的文件名}/mindrecord/{数据文件}`。

                其他数据转换为MindRecord的，放置在：`./datasets/{ipynb的文件名}/ds_to_mindrecord/{数据文件}`。

                MindRecord转换成其他数据，放置在：`./datasets/{ipynb的文件名}/mindrecord_to_ds/{数据文件}`。

## 图片

1. 文中所引用的所有图片或其他资源文件需使用**绝对路径**，不使用相对链接，**图片名称不能包含下划线**。
2. 所引用的图片、链接、文档、代码、数据集无版权问题。

## 表格

文中的表格使用Markdown写法，需要确保每行上下的格式符号“|”对齐，且符号“：---------”的长度超过表中该列的最长部分。

## 其他

display_name设置为MindSpore，name设置为mindspore，便于直接对接在线体验环境。
