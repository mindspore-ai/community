# MindSpore 开源社区 Python 编程规范（初稿）

<!-- TOC -->

- [说明](#说明)
- [适用范围](#适用范围)
    - [1. 代码风格](#1-代码风格)
        - [1.1 命名](#11-命名)
        - [1.2 格式](#12-格式)
        - [1.3 注释](#13-注释)
        - [1.4 日志](#14-日志)
    - [2. 通用编码](#2-通用编码)
        - [2.1 接口声明](#21-接口声明)
        - [2.2 数据校验](#22-数据校验)
        - [2.3 异常行为](#23-异常行为)
        - [2.4 序列化和反序列化](#24-序列化和反序列化)
    - [3. 安全编码](#3-安全编码)
        - [3.1 运算符与表达式](#31-运算符与表达式)
        - [3.2 函数与方法](#32-函数与方法)
        - [3.3 类与面向对象](#33-类与面向对象)
        - [3.4 异常处理](#34-异常处理)
        - [3.5 标准库](#35-标准库)
        - [3.6 文件](#36-文件)
        - [3.7 序列化](#37-序列化)

<!-- /TOC -->

## 说明

本规范以[PEP8](https://www.python.org/dev/peps/pep-0008/)为基础，参考华为Python通用编码规范、安全编程规范，并结合业界共识整理而成，参与MindSpore社区开发需要首先遵循本规范内容（与PEP8冲突部分），其余遵循PEP8规范;
如果对规则异议，建议提交issue并说明理由，经MindSpore社区运营团队评审接纳后可修改生效；

## 适用范围

MindSpore开源社区

---

### 1. 代码风格

#### 1.1 命名

**规则 1.1.1 包名，模块名：小写+下划线（公有：lower_case_with_underscores，私有：_lower_case_with_underscores）。**

模块应该有短的、全小写的名称。如果可以提高可读性，则可以在模块名称中使用下划线。Python包也应该有短的、全小写的名称，尽管不鼓励使用下划线。

当使用C或C++编写的扩展模块向Python提供更高级别（例如更面向对象）的接口时，C/C++模块命名应该有一个前导下划线（例如_socket）。

**规则 1.1.2 类名：使用驼峰格式，首字母大写，私有类下划线前缀。**

```python
class _Foo:
    _instance = None
    pass
```

**规则 1.1.3 函数名、变量名：小写，多个单词下划线分割。**

```python
def _func_example(path):
    pass
```

**建议 1.1.4 除迭代器与计数器除外，禁止使用单字符命名。**

#### 1.2 格式

**规则 1.2.1 每行字符数不要超过 120 个。**

如果超过120个字符，请选择合理的方式进行换行。

**规则 1.2.2 使用空格进行缩进，每次缩进4个空格，禁止tab缩进。**

**规则 1.2.3 import顺序：标准库、第三方、自定义模块。**

**规则 1.2.4 返回语句和条件语句中不使用括号。**

**规则 1.2.5 模块级函数和类之间双空行，类成员函数之间一空行，注释与代码间按需添加空行，原则上不超过两空行。**

**规则 1.2.6 无效或冗余代码直接删除，不要以注释、TODO等方式保留在代码中，建议提issue记录。**

#### 1.3 注释

**规则 1.3.1  文件头注释必须包含版权声明。**

所有python文件，均需包含如下版权声明：

```python
# Copyright 2019 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""
Add notes.
"""
import xxx
```

> 关于版权说明，应注意：
> 2020年新建的文件，应该是 `Copyright 2020 Huawei Technologies Co., Ltd`
> 2019年创建年份，2020年修改年份，应该是 `Copyright 2019-2020 Huawei Technologies Co., Ltd`

**规则 1.3.2 对外的类、方法、算子、Cell注释格式。**

- `class` 和 `def` 的注释格式相同，采用业界通用的python注释语法，写在声明下方并缩进，所有的 `class` 和 `def` 都需要写注释，模块内部的类和方法可以只写一条简介。
- 注释格式详见[MindSpore注释规范](https://gitee.com/mindspore/community/blob/master/guidelines/docs_comments_guidelines_zh_cn.md)。

**规则 1.3.3 不允许通过注释屏蔽pylint告警。**

#### 1.4 日志

**规则 1.4.1 异常日志文本首字母大写。**

**规则 1.4.2 日志文本中变量名必须使用单引号注明。**

### 2. 通用编码

#### 2.1 接口声明

**规则 2.1.1 用户接口在文件的__all__中说明，__all__摆放在import与代码之间。**

**规则 2.1.2 当前文件使用的非对外方法命名采用下划线前缀，内部跨模块使用的方法无需下划线前缀，用户接口在__all__中声明。**

#### 2.2 数据校验

**规则 2.2.1 对所有外部数据进行合法性检查，包括但不限于：函数入参、外部输入命名行、文件格式，文件大小、环境变量、用户数据等。**

**建议 2.2.2 必须对文件路径进行规范化后再使用。**

当文件路径来自外部数据时，需要先将文件路径规范化，如果没有作规范化处理，攻击者就有机会通过恶意构造文件路径进行文件的越权访问：
例如，攻击者可以构造“../../../etc/passwd”的方式进行任意文件访问。
在Linux下，使用realpath函数，在Windows下，使用PathCanonicalize函数进行文件路径的规范化。

【例外】
运行于控制台的命令行程序，通过控制台手工输入文件路径，可以作为本建议例外。

#### 2.3 异常行为

**规则 2.3.1 异常必须被妥当处理，禁止抑制或者忽略已检查异常。**

每一个except 块都应该确保程序只会在继续有效的情况下才会继续运行下去。except 块必须要么从异常情况中恢复，要么重新抛出适合当前catch块上下文的另一个异常以允许最邻近的外层try-except 语句块来进行恢复工作。
【正确代码示例】
正确的做法是，避免使用 os.system，可以使用标准的 API 替代运行系统命令来完成任务：

```python
validFlag = False
    while not validFlag:
    try:
        # If requested file does not exist, throws FileNotFoundError
        # If requested file exists, sets validFlag to true
        validFlag = True
    except FileNotFoundError:
        import traceback
        traceback.print_exc()
```

【例外情况】：

1. 在资源释放失败不会影响程序后续行为的情况下，释放资源时发生的异常可以被抑制。释放资源的例子包括关闭文件、网络套接字、线程等等。这些资源通常是在except或者fianlly块中被释放，并且在后续的程序运行中都不会再被使用。因此，除非资源被耗尽，否则不会有其他途径使得这些异常会影响程序后续的行为。在充分处理了资源耗尽问题的情况下，只需对异常进行净化和记录日志（以备日后改进）就足够了；在这种情况下没必要做其他额外的错误处理。
2. 如果在特定的抽象层次上不可能从异常情况中恢复过来，则在那个层级的代码就不用处理这个异常，而是应该抛出一个合适的异常，让更高层次的代码去捕获处理，并尝试恢复。对于这种情况，最通常的实现方法是省略掉catch语句块，允许异常被广播出去。

**规则 2.3.2 使用try…except…结构对代码作保护时，需要在异常后使用finally…结构保证操作对象的释放。**

使用try…except…结构对代码作保护时，如果代码执行出现了异常，为了能够可靠地关闭操作对象，需要使用finally…结构确保释放操作对象。

【正确代码示例】

```python
handle = open(r"/tmp/sample_data.txt") # May raise IOError
    try:
        data = handle.read() # May raise UnicodeDecodeError
    except UnicodeDecodeError as decode_error:
        print(decode_error)
    finally:
        handle.close() # Always run after try:
```

**规则 2.3.3 不要使用“except:”语句来捕获所有异常。**

在异常这方面, Python非常宽容,“except:”语句真的会捕获包括Python语法错误在内的任何错误。使用“except:”很容易隐藏真正的bug，我们在使用try…except…结构对代码作保护时，应该明确期望处理的异常。Exception类是大多数运行时异常的基类，一般也应当避免在except语句中使用。通常，try只应当包含必须要在当前位置处理异常的语句，except只捕获必须处理的异常。比如对于打开文件的代码，try应当只包含open语句，except只捕获FileNotFoundError异常。对于其他预料外的异常，则让上层函数捕获，或者透传到程序外部来充分暴露问题。

【错误代码示例】
如下代码可能抛出两种异常，使用“except:”语句进行统一处理时，如果是open执行异常，将在“except:”语句之后handle无效的情况下调用close，报错handle未定义。

```python
try:
        handle = open(r"/tmp/sample_data.txt") # May raise IOError
        data = handle.read() # May raise UnicodeDecodeError
    except:
        handle.close()
```

【正确代码示例】

```python
try:
        handle = open(r"/tmp/sample_data.txt") # May raise IOError
        try:
            data = handle.read() # May raise UnicodeDecodeError
        except UnicodeDecodeError as decode_error:
            print(decode_error)
        finally:
            handle.close()
    except(FileNotFoundError, IOError) as file_open_except:
        print(file_open_except)
```

**规则 2.3.4 不在except分支里面的raise都必须带异常。**

raise关键字单独使用只能出现在try-except语句中，重新抛出except抓住的异常。

【错误代码示例】

```python
a = 1
    if a==1:
        raise
```

【正确代码示例1】raise一个Exception或自定义的Exception

```python
a = 1
    if a==1:
        raise Exception
```

【正确代码示例2】在try-except语句中使用

```python
try:
        f = open('myfile.txt')
        s = f.readline()
        i = int(s.strip())
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    except ValueError:
        print("Could not convert data to an integer.")
    except Exception:
        print("Unexpected error:", sys.exc_info()[0])
    raise
```

#### 2.4 序列化和反序列化

**规则 2.4.1 assert语句通常只在测试代码中使用，禁止在Release版本中包含assert功能。**

assert只应在研发过程中内部测试时使用，出现了AssertionError异常说明存在软件设计或者编码上的错误，应
当修改软件予以解决。在对外发布的生产版本中禁止包含assert功能。

### 3. 安全编码

#### 3.1 运算符与表达式

##### 3.1.1 对除法运算和模运算中的除数为0的情况做相应保护

##### 3.1.2 同一个函数所有分支的返回值类型和个数保持一致

##### 3.1.3 禁止使用is或is not运算符在内置类型之间作比较

#### 3.2 函数与方法

##### 3.2.1 禁止使用可变对象作为参数默认值

##### 3.2.2 使用return代替StopIteration来结束生成器

#### 3.3 类与面向对象

##### 3.3.1 未实现的数值运算类型魔法函数必须返回NotImplemented而不是抛出 NotImplementedError

#### 3.4 异常处理

##### 3.4.1 禁止通过异常泄露敏感数据

#### 3.5 标准库

##### 3.5.1 注意根据场景选用copy或deepcopy来完成浅拷贝或深拷贝

##### 3.5.2 在datetime的使用过程中注意时区的影响，时区敏感的场景建议显式指定时区

#### 3.6 文件

##### 3.6.1 在多用户系统中创建文件时应根据需要指定合适的权限

##### 3.6.2 校验文件路径之前应该先对其进行规范化处理

##### 3.6.3 禁止使用tempfile.mktemp创建临时文件

##### 3.6.4 临时文件使用完毕应及时删除

##### 3.6.5 解压文件必须进行安全检查

攻击者有可能上传一个很小的zip文件，但是完全解压缩之后达到几百万GB甚至更多，消耗完磁盘空间导致系统或程序无法正常运行。因此在解压缩文件时需要限制所使用的磁盘空间。因此，禁止直接一次性递归解压压缩包全部内容。

#### 3.7 序列化

##### 3.7.1 禁止使用pickle.load、_pickle.load和shelve模块加载外部数据

##### 3.7.2 禁止序列化未加密的敏感数据

##### 3.7.3 禁止使用yaml模块的load函数

##### 3.7.4 禁止使用jsonpickle模块的encode/decode或dumps/loads函数

#### 3.8 外部数据校验

##### 3.8.1 禁止使用eval和exec函数执行不可信代码

##### 3.8.2 禁止使用OS命令解析器或“危险函数”调用系统命令

使用未经校验的不可信输入作为系统命令的参数或命令的一部分，可能导致命令注入漏洞。对于命令注入漏洞，命令将会以与Python应用程序相同的特权级别执行，它向攻击者提供了类似系统shell的功能。在Python中，os.system 或 os.popen 经常被用来调用一个新的进程，如果被执行的命令来自于外部输入，则可能会产生命令和参数注入。
执行命令的时候，请注意以下几点：

1. 命令执行的字符串不要去拼接输入的参数，如果必须拼接时，要对输入参数进行白名单过滤。
2. 对传入的参数要做类型校验，例如：整数数据，可以对数据进行整数强制转换。
3. 保证格式化字符串的正确性，例如：int类型参数的拼接，对于参数要用%d，不能用%s。

【错误代码示例1】
攻击者可以通过找到环境变量APPHOME对应的值，并且在相应目录下放置常量INITCMD对应的攻击程序，达到执
行的效果：

```python
home = os.getenv('APPHOME')
    cmd = os.path.join(home, INITCMD)
    os.system(cmd)
```

【错误代码示例2】
没有校验属性 backuptype 的值，这个是用户输入的，攻击者可能进行攻击，例如：用户输入的是：" && del
c:\\dbms\\*.* "：

```python
# 值来自用户配置
    btype = req.field('backuptype')
    cmd = "cmd.exe /K \"c:\\util\\rmanDB.bat " + btype + "&&c:\\util\\cleanup.bat\""
    os.system(cmd)
```

【错误代码示例3】
没有校验属性 backuptype 的值，这个是用户输入的，攻击者可能进行攻击，例如：用户输入的是：" && del
c:\\dbms\\*.* "：

```python
import os
    import sys
    try:
        print(os.system("ls " + sys.argv[1]))
    except Exception as ex:
        print('exception:', ex)
```

攻击者可以通过以下命令来利用这个漏洞程序：

```python
python test.py ". && echo bad"
```

实际将会执行两个命令：

```python
ls .
    echo bad
```

【正确代码示例】
避免使用 os.system，可以使用标准的 API 替代运行系统命令来完成任务：

```python
import os
    import sys
    try:
        print(os.listdir(sys.argv[1]))
    except Exception as ex:
        print(ex)
```

##### 3.8.3 避免在命令解析器中使用通配符

##### 3.8.4 禁止使用subprocess模块中的shell=True选项

##### 3.8.5 不受信任的外部数据禁止使用.format()进行格式化

##### 3.8.6 防止正则表达式引起的ReDos攻击

##### 3.8.7 禁止直接使用外部数据来拼接XML

##### 3.8.8 禁止在处理XML数据时解析不可信的实体

#### 3.9 日志

##### 3.9.1 禁止直接使用外部数据记录日志

##### 3.9.2 禁止在日志中记录口令、密钥等敏感数据

---
