<!-- TOC -->

- [说明](#说明)
- [适用范围](#适用范围)
    - [代码风格](#1-代码风格)
        - [命名](#11-命名)
        - [格式](#12-格式)
        - [注释](#13-注释)
    - [通用编码](#2-通用编码)
        - [代码设计](#21-代码设计)
        - [头文件和预处理](#22-头文件和预处理)
        - [数据类型](#23-数据类型)
        - [常量](#24-常量)
        - [变量](#25-变量)
        - [表达式](#26-表达式)
        - [转换](#27-转换)
        - [控制语句](#28-控制语句)
        - [声明与初始化](#29-声明与初始化)
        - [指针与数组](#210-指针与数组)
        - [字符串](#211-字符串)
        - [断言](#212-断言)
        - [类和对象](#213-类和对象)
        - [函数设计](#214-函数设计)
        - [函数使用](#215-函数使用)
        - [内存](#216-内存)
        - [文件](#217-文件)
        - [安全函数](#218-安全函数)


<!-- /TOC -->


## 说明

本规范以[Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)为基础，参考华为通用编码规范、安全编程规范，并结合业界共识整理而成，参与MindSpore社区的开发者首先需要遵循本规范内容，其余遵循Google C++ Style Guide规范;
如果对规则异议，建议提交issue并说明理由，经MindSpore社区运营团队评审后可接纳并修改生效；

## 适用范围

MindSpore开源社区

------------------

### 1. 代码风格

#### 1.1 命名

##### 规则 1.1.1 文件命名。
C++文件使用小写+下划线的方式命名，以`.cc`作为后缀，头文件以`.h`作为后缀，单元测试文件以`_test.cc`结尾.

> a_b_c.h
> a_b_c.cc
> a_b_c_test.cc

##### 规则 1.1.2 局部变量、参数命名采用小写加下划线方式。

```cpp
void FooBar(int func_param) {
  int local_var;
}
```

##### 规则 1.1.3 成员变量命名采用小写加下划线，并以下划线作为后缀。

```cpp
class FooBar {
  public:
    int mamber_var_;
};
```

##### 规则 1.1.4 宏命名采用大写加下划线。

```cpp
#define MS_LOG(...)
```

##### 规则 1.1.5 常量、枚举命名采用k驼峰。

```cpp
const int kDaysInAWeek = 7;

enum UrlTableErrors {
  kOk = 0,
  kErrorOutOfMemory,
  kErrorMalformedInput,
};
```


#### 1.2 格式

##### 建议 1.2.1 每行字符数不要超过 120 个。
如果超过120个字符，请选择合理的方式进行换行。

##### 规则 1.2.2 使用空格进行缩进，每次缩进2格。

##### 规则 1.2.3 在声明指针、引用变量或参数时, `&`、`*`跟随变量名，另外一边留空格。

```cpp
  char *c;
  const std::string &str;
```

##### 规则 1.2.4 if语句必须要使用大括号。

```cpp
// 即使if分支代码只有一行，也必须使用大括号
if (cond) {
  single line code;
}
```

##### 规则 1.2.5 for/while等循环语句必须使用大括号，即使循环体是空的，或者循环语句只有一条。

##### 规则 1.2.6 表达式换行要保持换行的一致性，运算符放行末。

```cpp
int a = a_very_long_expression +
        a_very_very_long_expression +
        a_very_very_very_long_expression;
```

##### 规则 1.2.7 每个变量定义和赋值语句单独一行。

```cpp
a = 1;
b = 2;
c = 3;
```


#### 1.3 注释

##### 规则 1.3.1 文件头注释包含版权声明

所有h文件、cc文件，均需包含如下版权声明：
```cpp

/**
 * Copyright 2019 Huawei Technologies Co., Ltd
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

```

> 关于版权说明，应注意：
> 2020年新建的文件，应该是`Copyright 2020 Huawei Technologies Co., Ltd`
> 2019年创建年份，2020年修改年份，应该是`Copyright 2019-2020 Huawei Technologies Co., Ltd`


##### 规则 1.3.2 代码注释置于对应代码的上方或右边，注释符与注释内容之间要有1个空格，右置注释与前面代码至少1空格，使用`//`，而不是`/**/`。
```cpp
// this is multi-
// line comment
int foo; // this single-line comment
```
##### 规则 1.3.3 代码中禁止使用 TODO/TBD/FIXME 等注释，建议提issue跟踪。

##### 建议 1.3.4 不要写空有格式的函数头注释。
并不是所有的函数都需要函数头注释，函数尽量通过函数名自注释，按需写函数头注释；函数原型无法表达的，却又希望读者知道的信息，才需要加函数头注释辅助说明。
不要写无用、信息冗余的函数头，函数头注释内容可选，但不限于：功能说明、返回值，性能约束、用法、内存约定、算法实现、可重入的要求等。


### 2. 通用编码

#### 2.1 代码设计

##### 规则 2.1.1 对所有外部数据进行合法性检查，包括但不限于：函数入参、外部输入命名行、文件、环境变量、用户数据等。

##### 规则 2.1.2 函数执行结果传递，优先使用返回值，尽量避免使用出参。

```cpp
  FooBar *Func(const std::string &in);
```

##### 规则 2.1.3 删除无效、冗余或永不执行的代码。

虽然大多数现代编译器在许多情况下可以对无效或从不执行的代码告警，响应告警应识别并清除告警；
应该主动识别无效的语句或表达式，并将其从代码中删除。

##### 规则 2.1.4 补充C++异常机制的规范。

###### 规则 2.1.4.1 需要指定捕获异常种类，禁止捕获所有异常
```cpp
// 错误示范
try {
  // do something;
} catch (...) {
  // do something;
}
// 正确示范
try {
  // do something;
} catch (const std::bad_alloc &e) {
  // do something;
}
```

#### 2.2 头文件和预处理

##### 规则 2.2.1 使用新的标准C++头文件。

```cpp
// 正确示范
#include <cstdlib>
// 错误示范
#include <stdlib.h>
```

##### 规则 2.2.2 禁止头文件循环依赖。

头文件循环依赖，指a.h包含b.h，b.h包含c.h，c.h包含a.h之类导致任何一个头文件修改，都导致所有包含了a.h/b.h/c.h的代码全部重新编译一遍。
头文件循环依赖直接体现了架构设计上的不合理，可通过优化架构去避免。

##### 规则 2.2.3 禁止包含用不到的头文件。

##### 规则 2.2.4 禁止通过 extern 声明的方式引用外部函数接口、变量。

##### 规则 2.2.5 禁止在extern "C"中包含头文件。

##### 规则 2.2.6 禁止在头文件中或者#include之前使用using导入命名空间。


#### 2.3 数据类型

##### 建议 2.3.1 避免滥用 typedef或者#define 对基本类型起别名。

##### 规则 2.3.2 使用using 而非typedef定义类型的别名，避免类型变化带来的散弹式修改。

```cpp
// 正确示范
using FooBarPtr = std::shared_ptr<FooBar>;
// 错误示范
typedef std::shared_ptr<FooBar> FooBarPtr;
```

#### 2.4 常量

##### 规则 2.4.1 禁止使用宏表示常量。

##### 规则 2.4.2 禁止使用魔鬼数字\字符串。

##### 建议 2.4.3 建议每个常量保证单一职责。

#### 2.5 变量

##### 规则 2.5.1 优先使用命名空间来管理全局常量，如果和某个class有直接关系的，可以使用静态成员常量。

```cpp
namespace foo {
  int kGlobalVar;

  class Bar {
    private:
      static int static_member_var_;
  };
}
```

##### 规则 2.5.2 尽量避免使用全局变量，谨慎使用单例模式，避免滥用。

##### 规则 2.5.3 禁止在变量自增或自减运算的表达式中再次引用该变量。

##### 规则 2.5.4 指向资源句柄或描述符的指针变量在资源释放后立即赋予新值或置为NULL。

##### 规则 2.5.5 禁止使用未经初始化的变量。

#### 2.6 表达式

##### 建议 2.6.1 表达式的比较遵循左侧倾向于变化、右侧倾向于不变的原则。

```cpp
// 正确示范
if (ret != SUCCESS) {
  ...
}

// 错误示范
if (SUCCESS != ret) {
  ...
}
```

##### 规则 2.6.2 通过使用括号明确操作符的优先级，避免出现低级错误。

```cpp
// 正确示范
if (cond1 || (cond2 && cond3)) {
  ...
}

// 错误示范
if (cond1 || cond2 && cond3) {
  ...
}
```

#### 2.7 转换

##### 规则 2.7.1 使用有C++提供的类型转换，而不是C风格的类型转换，避免使用const_cast和reinterpret_cast。


#### 2.8 控制语句

##### 规则 2.8.1 switch语句要有default分支。


#### 2.9 声明与初始化

##### 规则 2.9.1 禁止用`memcpy_s`、`memset_s`初始化非POD对象。


#### 2.10 指针和数组

##### 规则 2.10.1 禁止持有std::string的c_str()返回的指针。

```cpp
// 错误示范
const char * a = std::to_string(12345).c_str();
```

##### 规则 2.10.2 优先使用unique_ptr 而不是shared_ptr。

##### 规则 2.10.3 使用std::make_shared 而不是new 创建shared_ptr。

```cpp
// 正确示范
std::shared_ptr<FooBar> foo = std::make_shared<FooBar>();
// 错误示范
std::shared_ptr<FooBar> foo(new FooBar());
```

##### 规则 2.10.4 使用智能指针管理对象，避免使用new/delete。

##### 规则 2.10.5 禁止使用auto_ptr。

##### 规则 2.10.6 对于指针和引用类型的形参，如果是不需要修改的，要求使用const。

##### 规则 2.10.7 数组作为函数参数时，必须同时将其长度作为函数的参数。

```cpp
int ParseMsg(BYTE *msg, size_t msgLen) {
  ...
}
```

#### 2.11 字符串

##### 规则 2.11.1 对字符串进行存储操作，确保字符串有’\0’结束符。

#### 2.12 断言

##### 规则 2.12.1 断言不能用于校验程序在运行期间可能导致的错误，可能发生的运行错误要用错误处理代码来处理。

#### 2.13 类和对象

##### 规则 2.13.1 单个对象释放使用delete，数组对象释放使用delete []。

```cpp
const int kSize = 5;
int *number_array = new int[kSize];
int *number = new int();
...
delete[] number_array;
number_array = nullptr;
delete number;
number = nullptr;
```
##### 规则 2.13.2 禁止使用std::move操作const对象。

##### 规则 2.13.3 严格使用virtual/override/final修饰虚函数。

```cpp
class Base {
  public:
    virtual void Func();
};

class Derived : public Base {
  public:
    void Func() override;
};

class FinalDerived : public Derived {
  public:
    void Func() final;
};
```

#### 2.14 函数设计

##### 规则 2.14.1 使用 RAII 特性来帮助追踪动态分配

```cpp
// 正确示范
{
  std::lock_guard<std::mutex> lock(mutex_);
  ...
}
```

##### 规则 2.14.2 非局部范围使用lambdas时，避免按引用捕获。

```cpp
{
  int local_var = 1;
  auto func = [&]() { ...; std::cout << local_var << std::endl; };
  thread_pool.commit(func);
}
```

##### 规则 2.14.3 禁止虚函数使用缺省参数值.

##### 建议 2.14.4 使用强类型参数\成员变量，避免使用void*.

#### 2.15 函数使用

##### 规则 2.15.1 函数传参传递，要求入参在前，出参在后。

```cpp
  bool Func(const std::string &in, FooBar *out1, FooBar *out2);
```

##### 规则 2.15.2 函数传参传递，要求入参用`const T &`，出参用 `T *`。

```cpp
  bool Func(const std::string &in, FooBar *out1, FooBar *out2);
```

##### 规则 2.15.3 函数传参传递，不涉及所有权的场景，使用T * 或const T & 作为参数，而不是智能指针。

```cpp
  // 正确示范
  bool Func(const FooBar &in);
  // 错误示范
  bool Func(std::shared_ptr<FooBar> in);
```

##### 规则 2.15.4 函数传参传递，如需传递所有权，建议使用shared_ptr + move传参。

```cpp
class Foo {
  public:
    explicit Foo(shared_ptr<T> x):x_(std::move(x)){}
  private:
    shared_ptr<T> x_;
};
```

##### 规则 2.15.5 单参数构造函数必须用explicit修饰，多参数构造函数禁止使用explicit修饰.

```cpp
  explicit Foo(int x);          //good :white_check_mark:
  explicit Foo(int x, int y=0); //good :white_check_mark:
  Foo(int x, int y=0);          //bad  :x:
  explicit Foo(int x, int y);   //bad  :x:
```

##### 规则 2.15.6 拷贝构造和拷贝赋值操作符应该是成对出现或者禁止。

```cpp
class Foo {
  private:
    Foo(const Foo&) = default;
    Foo& operator=(const Foo&) = default;
    Foo(Foo&&) = delete;
    Foo& operator=(Foo&&) = delete;
};
```

##### 规则 2.15.7 禁止保存、delete指针参数。

##### 规则 2.15.8 禁止使用非安全函数，需要给出清单。

##### 规则 2.15.9 禁止使用非安全退出函数，需要给出清单。

```cpp
{
  kill(...);            // 调用kill强行终止其他进程(如kill -9)，会导致其他进程的资源得不到清理。
  TerminateProcess();   // 调用erminateProcess函数强行终止其他进程，会导致其他进程的资源得不到清理。
  pthread_exit();       // 严禁在线程内主动终止自身线程，线程函数在执行完毕后会自动、安全地退出;
  ExitThread();         // 严禁在线程内主动终止自身线程，线程函数在执行完毕后会自动、安全地退出;
  exit();               // main函数以外，禁止任何地方调用，程序应该安全退出；
  ExitProcess();        // main函数以外，禁止任何地方调用，程序应该安全退出；
  abort();              // 禁用，abort会导致程序立即退出，资源得不到清；
}
```

##### 规则 2.15.10 禁用rand函数产生用于安全用途的伪随机数。

C标准库rand()函数生成的是伪随机数，请使用/dev/random生成随机数。

##### 规则 2.15.11 严禁使用string类存储敏感信息。

string类是C++内部定义的字符串管理类，如果口令等敏感信息通过string进行操作，在程序运行过程中，敏感信息可
能会散落到内存的各个地方，并且无法清0。

以下代码，Foo函数中获取密码，保存到string变量password中，随后传递给VerifyPassword函数，在这个过程中，
password实际上在内存中出现了2份。

```cpp
int VerifyPassword(string password) {
  //...
}
int Foo() {
  string password = GetPassword();
  VerifyPassword(password);
  ...
}
```
应该使用char或unsigned char保存敏感信息，如下代码：
```cpp
int VerifyPassword(const char *password) {
  //...
}
int Foo() {
  char password[MAX_PASSWORD] = {0};
  GetPassword(password, sizeof(password));
  VerifyPassword(password);
  ...
}
```

##### 规则 2.15.12 内存中的敏感信息使用完毕后立即清0。

口令、密钥等敏感信息使用完毕后立即清0，避免被攻击者获取。


#### 2.16 内存
##### 规则 2.16.1 内存分配后必须判断是否成功。

内存分配失败后，那么后续的操作存在未定义的行为风险。比如malloc申请失败返回了空指针，对空指针的解引用是一种未定义行为。

##### 规则 2.16.2 禁止引用未初始化的内存。

malloc、new分配出来的内存没有被初始化为0，要确保内存被引用前是被初始化的。

##### 规则 2.16.3 避免使用realloc()函数。

随着参数的不同，realloc函数行为也不同，这不是一个设计良好的函数。虽然在编码中提供了一些便利性，但是却极易引发各种bug。

##### 规则 2.16.4 不要使用alloca()函数申请栈上内存。

POSIX和C99均未定义alloca()的行为，在有些平台下不支持该函数，使用alloca会降低程序的兼容性和可移植性，该函数在栈帧里申请内存，申请的大小很可能超过栈的边界，影响后续的代码执行。

#### 2.17 文件

##### 规则 2.17.1 必须对文件路径进行规范化后再使用。
当文件路径来自外部数据时，需要先将文件路径规范化，如果没有作规范化处理，攻击者就有机会通过恶意构造文件路径进行文件的越权访问：
例如，攻击者可以构造“../../../etc/passwd”的方式进行任意文件访问。
在linux下，使用realpath函数，在windows下，使用PathCanonicalize函数进行文件路径的规范化。
【错误代码示例】
以下代码从外部获取到文件名称，拼接成文件路径后，直接对文件内容进行读取，导致攻击者可以读取到任意文件的内容：

```cpp
char *fileName = GetMsgFromRemote();
...
sprintf_s(untrustPath, sizeof(untrustPath), "/tmp/%s", fileName);
char *text = ReadFileContent(untrustPath);   // Bad，读取前未检查untrustPath是否允许访问
```
【正确代码示例】
正确的做法是，对路径进行规范化后，再判断路径是否是本程序所认为的合法的路径：
```cpp
char *fileName = GetMsgFromRemote();
...
sprintf_s(untrustPath, sizeof(untrustPath), "/tmp/%s", fileName);
char path[PATH_MAX] = {0};
if (realpath(untrustPath, path) == NULL) {
    //error
    ...
}
if (!IsValidPath(path)) {    // Good，检查文件位置是否正确
    //error
    ...
}
char *text = ReadFileContent(untrustPath);
```
【例外】
运行于控制台的命令行程序，通过控制台手工输入文件路径，可以作为本建议例外。


##### 规则 2.17.2 不要在共享目录中创建临时文件。
程序的临时文件应当是程序自身独享的，任何将自身临时文件置于共享目录的做法，将导致其他共享用户获得该程序的额外信息，产生信息泄露。因此，不要在任何共享目录创建仅由程序自身使用的临时文件。
如Linux下的/tmp目录是一个所有用户都可以访问的共享目录，不应在该目录下创建仅由程序自身使用的临时文件。

#### 2.18 安全函数

<table>
    <thead>
      <tr>
          <th style="width: 100px;">安全函数类型</th>
          <th style="width: 150px;">说明</th>
          <th>备注</th>
      </tr>
    </thead>
    <tr>
      <td rowspan="1">xxx_s</td>
      <td>Huawei Secure C库的安全函数API</td>
      <td>集成Huawei Secure C库即可使用</td>
    </tr>
    <tr>
      <td rowspan="1">xxx_sp</td>
      <td>Huawei Secure C库的安全函数性能优化API（宏实现）</td>
      <td>
      性能优化宏接口对count、destMax、strSrc为常量时有优化效果，如果是变量则优化效果不明显.宏接口使用策略：默认使用_s接口，在性能敏感的调用点受限使用_sp接口，受限场景如下：
      a)  memset_sp/memcpy_sp使用场景:destMax和count为常量
      b)  strcpy_sp/strcat_sp使用场景:destMax为常量且strSrc为字面量
      c)  strncpy_sp/strncat_sp使用场景:destMax和count为常量且strSrc为字面量</td>
    </tr>
</table>

##### 规则 2.18.1 请使用社区提供的安全函数库的安全函数，禁止使用内存操作类危险函数。

<table>
    <thead>
      <tr>
          <th style="width: 100px;">函数类别</th>
          <th style="width: 150px;">危险函数</th>
          <th>安全替代函数</th>
      </tr>
    </thead>
    <tr>
      <td rowspan="4">内存拷贝</td>
      <td>memcpy或bcopy</td>
      <td>memcpy_s</td>
    </tr>
    <tr>
      <td>wmemcpy</td>
      <td>wmemcpy_s</td>
    </tr>
    <tr>
      <td>memmove</td>
      <td>memmove_s</td>
    </tr>
    <tr>
      <td>wmemmove</td>
      <td>wmemmove_s</td>
    </tr>
    <tr>
      <td rowspan="4">字符串拷贝</td>
      <td>strcpy</td>
      <td>strcpy_s</td>
    </tr>
    <tr>
      <td>wcscpy</td>
      <td>wcscpy_s</td>
    </tr>
    <tr>
      <td>strncpy</td>
      <td>strncpy_s</td>
    </tr>
    <tr>
      <td>wcsncpy</td>
      <td>wcsncpy_s</td>
    </tr>
    <tr>
      <td rowspan="4">字符串串接</td>
      <td>strcat</td>
      <td>strcat_s</td>
    </tr>
    <tr>
      <td>wcscat</td>
      <td>wcscat_s</td>
    </tr>
    <tr>
      <td>strncat</td>
      <td>strncat_s</td>
    </tr>
    <tr>
      <td>wcsncat</td>
      <td>wcsncat_s</td>
    </tr>
    <tr>
      <td rowspan="6">格式化输出</td>
      <td>sprintf</td>
      <td>sprintf_s</td>
    </tr>
    <tr>
      <td>swprintf</td>
      <td>swprintf_s</td>
    </tr>
    <tr>
      <td>vsprintf</td>
      <td>vsprintf_s</td>
    </tr>
    <tr>
      <td>vswprintf</td>
      <td>vswprintf_s</td>
    </tr>
    <tr>
      <td>snprintf</td>
      <td>snprintf_s 或 snprintf_truncated_s</td>
    </tr>
    <tr>
      <td>vsnprintf</td>
      <td>vsnprintf_s 或 vsnprintf_truncated_s</td>
    </tr>
    <tr>
      <td rowspan="12">格式化输入</td>
      <td>scanf</td>
      <td>scanf_s</td>
    </tr>
    <tr>
      <td>wscanf</td>
      <td>wscanf_s</td>
    </tr>
    <tr>
      <td>vscanf</td>
      <td>vscanf_s</td>
    </tr>
    <tr>
      <td>vwscanf</td>
      <td>vwscanf_s</td>
    </tr>
    <tr>
      <td>fscanf</td>
      <td>fscanf_s</td>
    </tr>
    <tr>
      <td>fwscanf</td>
      <td>fwscanf_s</td>
    </tr>
    <tr>
      <td>vfscanf</td>
      <td>vfscanf_s</td>
    </tr>
    <tr>
      <td>vfwscanf</td>
      <td>vfwscanf_s</td>
    </tr>
    <tr>
      <td>sscanf</td>
      <td>sscanf_s</td>
    </tr>
    <tr>
      <td>swscanf</td>
      <td>swscanf_s</td>
    </tr>
    <tr>
      <td>vsscanf</td>
      <td>vsscanf_s</td>
    </tr>
    <tr>
      <td>vswscanf</td>
      <td>vswscanf_s</td>
    </tr>
    <tr>
      <td rowspan="1">标准输入流输入</td>
      <td>gets</td>
      <td>gets_s</td>
    </tr>
    <tr>
      <td rowspan="1">内存初始化</td>
      <td>memset</td>
      <td>memset_s</td>
    </tr>
</table>


##### 规则 2.18.2 正确设置安全函数中的destMax参数。

##### 规则 2.18.3 禁止封装安全函数。

##### 规则 2.18.4 禁止用宏重命名安全函数。

```cpp
#define XXX_memcpy_s memcpy_s
#define SEC_MEM_CPY memcpy_s
#define XX_memset_s(dst, dstMax, val, n) memset_s((dst), (dstMax), (val), (n))
```

##### 规则 2.18.5 禁止自定义安全函数。

使用宏重命名安全函数不利于静态代码扫描工具（非编译型）定制针对安全函数误用的规则，同时，由于命名风格多
样，也不利于提示代码开发者函数的真实用途，容易造成对代码的误解及重命名安全函数的误用。重命名安全函数不
会改变安全函数本身的检查能力。

```cpp
void MemcpySafe(void *dest, unsigned int destMax, const void *src, unsigned int count) {
  ...
}
```

##### 规则 2.18.6 必须检查安全函数返回值，并进行正确的处理。

原则上，如果使用了安全函数，需要进行返回值检查。如果返回值!=EOK, 那么本函数一般情况下应该立即返回，不
能继续执行。
安全函数有多个错误返回值，如果安全函数返回失败，在本函数返回前，根据产品具体场景，可以做如下操作(执行
其中一个或多个措施)：
（1）记录日志
（2）返回错误
（3）调用abort立即退出程序

```cpp
{
  ...
  err = memcpy_s(destBuff, destMax, src, srcLen);
  if (err != EOK) {
    MS_LOG("memcpy_s failed, err = %d\n", err);
    return FALSE;
  }
  ...
}
```

##### 规则 2.18.7 禁止外部可控数据作为system、popen、WinExec、ShellExecute、execl, xeclp, execle, execv, execvp、CreateProcess等进程启动函数的参数。

##### 规则 2.18.8 禁止外部可控数据作为dlopen/LoadLibrary等模块加载函数的参数。

##### 规则 2.18.9 禁止在信号处理例程中调用非异步安全函数。

信号处理例程应尽可能简化。在信号处理例程中如果调用非异步安全函数，可能会导致函数的执行不符合预期的结
果。 下列代码中的信号处理程序通过调用fprintf()写日志，但该函数不是异步安全函数。
```cpp
void Handler(int sigNum) {
  ...
  fprintf(stderr, "%s\n", info);
}
```
------------------------