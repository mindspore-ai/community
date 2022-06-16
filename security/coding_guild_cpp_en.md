<!-- TOC -->

- [Note](#note)
- [Scope](#scope)
    - [Code Style](#1-code-style)
        - [Naming](#11-naming)
        - [Format](#12-format)
        - [Comment](#13-comment)
    - [General Coding](#2-general-coding)
        - [Code Design](#21-code-design)
        - [Header File and Preprocessing](#22-header-file-and-preprocessing)
        - [Data Type](#23-data-type)
        - [Constant](#24-constant)
        - [Variable](#25-variable)
        - [Expression](#26-expression)
        - [Conversion](#27-conversion)
        - [Control Statement](#28-control-statement)
        - [Declaration and Initialization](#29-declaration-and-initialization)
        - [Pointer and Array](#210-pointer-and-array)
        - [String](#211-string)
        - [Assert](#212-assert)
        - [Class and Object](#213-class-and-object)
        - [Function Design](#214-function-design)
        - [Function Usage](#215-function-usage)
        - [Memory](#216-memory)
        - [File](#217-file)
        - [Secure Function](#218-secure-function)

<!-- /TOC -->

## Note

This document is developed based on [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html), Huawei C++ Coding Style Guide, Huawei secure coding standards, and industry consensus. To participate in the MindSpore community, please comply with this style guide, and then the Google C++ Style Guide.
If you disagree with the rules, you are advised to submit an issue and provide reasons. The issue can take effect after being reviewed, accepted, and modified by the MindSpore community operation team.

## Scope

MindSpore open source community

------------------

### <a name="csf">1. Code Style</a>

#### <a name="nm">1.1 Naming</a>

##### Rule 1.1.1 File Naming  

C++ files are named in the format of lowercase letters + underscores (_). The file name extension is `.cc`. The header file name extension is `.h`. The unit test file name ends with `_test.cc`.

> a_b_c.h
> a_b_c.cc
> a_b_c_test.cc

##### Rule 1.1.2 Use lowercase letters and underscores (_) to name local variables and parameters

```cpp
void FooBar(int func_param) {
  int local_var;
}
```

##### Rule 1.1.3 Use lowercase letters and underscores (_) to name member variables, with an underscore (_) as the suffix

```cpp
class FooBar {
  public:
    int mamber_var_;
};
```

##### Rule 1.1.4 Use uppercase letters and underscores (_) in macro names

```cpp
#define MS_LOG(...)
```

##### Rule 1.1.5 Name constants and enumerations in the CamelCase style starting with letterr "k."

```cpp
const int kDaysInAWeek = 7;

enum UrlTableErrors {
  kOk = 0,
  kErrorOutOfMemory,
  kErrorMalformedInput,
};
```

##### Rule 1.1.6 Naming of function

1. Class member variable accessor：naming of accessor should comply with naming rule of variables and parameters, such as:

```c++
int count() {return this->count_;}
```

2. Class member variable modifier：naming of modifier should be started with `set_` and followed by variables or parameters name, such as:

```c++
void set_count(int count) {this->count_ = count;}
```

3. Other class member functions/common functions: named based on the large hump rules, such as:

```c++
void FindPattern(...);
```

#### <a name="fmt">1.2 Format</a>

##### Recommendation 1.2.1 Each line contains a maximum of 120 characters

If a line contains more than 120 characters, start a new line properly.

##### Rule 1.2.2 Use spaces to indent, two at a time

##### Rule 1.2.3 When declaring a pointer or referencing variables or parameters, follow variable names with `&` and `*` and place a space on the other side

```cpp
  char *c;
  const std::string &str;
```

##### Rule 1.2.4 Use braces to include an if statement

```cpp
// Even if the if branch code is within one line, braces are required.
if (cond) {
  single line code;
}
```

##### Rule 1.2.5 Use braces for loop statements such as for and while statements, even if the loop body is empty or there is only one loop statement

##### Rule 1.2.6 Keep a consistent line break style for expressions and ensure that operators are placed at the end of a line

```cpp
int a = a_very_long_expression +
        a_very_very_long_expression +
        a_very_very_very_long_expression;
```

##### Rule 1.2.7 Each variable definition or assignment statement occupies one line

```cpp
a = 1;
b = 2;
c = 3;
```

#### <a name="nts">1.3 Comment</a>

##### Rule 1.3.1 File header comments contain copyright statements

All .h and .cc files must contain the following copyright statements:

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

> Notes:
> Files created in 2020 should contain `Copyright 2020 Huawei Technologies Co., Ltd`.
> Files created in 2019 and modified in 2020 should contain `Copyright 2019-2020 Huawei Technologies Co., Ltd`.

##### Rule 1.3.2 A comment is placed above or to the right of the code. There must be a space between the comment character and the comment content, and at least one space between the code and its comment on the right. Use `//`, not `/**/`

```cpp
// this is multi-
// line comment
int foo; // this single-line comment
```  

##### Rule 1.3.3 Do not use comments such as TODO, TBD, and FIXME in code. You are advised to submit an issue for tracking

##### Recommendation 1.3.4 Function header comments with no content are forbidden

Not all functions require header comments. You are advised to use the name of the function as its comment and write header comments if there is the need. For the information that cannot be expressed by the function prototype but is expected to be known by readers, function header comments are required.
Do not write useless or redundant function headers. The function header comments are optional, including but not limited to function description, return values, performance constraints, usage, memory conventions, algorithm implementation, and reentrant requirements.

### <a name="cc">2. General Coding</a>

#### <a name="cdes">2.1 Code Design</a>

##### Rule 2.1.1 Check the validity of all external data, including but not limited to function input parameters, external input named lines, files, environment variables, and user data

##### Rule 2.1.2 When transferring function execution results, preferentially use return values and avoid output parameters

```cpp
  FooBar *Func(const std::string &in);
```

##### Rule 2.1.3 Delete invalid, redundant, or never-executed code

Although most modern compilers in many cases can alert you to invalid or never executed code, responding alarms should be identified and cleared.
Identify and delete invalid statements or expressions from the code.

##### Rule 2.1.4 Follow additional specifications to the C++ exception mechanism

###### Rule 2.1.4.1 Specify the types of exceptions to be captured. Do not capture all exceptions

```cpp
// Incorrect
try {
  // do something;
} catch (...) {
  // do something;
}
// Correct
try {
  // do something;
} catch (const std::bad_alloc &e) {
  // do something;
}
```

#### <a name="inc">2.2 Header File and Preprocessing</a>

##### Rule 2.2.1 Use the new standard C++ header file

```cpp
// Correct
#include <cstdlib>
// Incorrect
#include <stdlib.h>
```

##### Rule 2.2.2 Header file cyclic dependency is forbidden

An example of cyclic dependency (also known as circular dependency) is: a.h contains b.h, b.h contains c.h, and c.h contains a.h. If any of these header files is modified, all code containing a.h, b.h, and c.h needs to be recompiled.
The cyclic dependency of header files reflects an obviously unreasonable architecture design, which can be avoided through optimization.

##### Rule 2.2.3 Do not include unnecessary header files

##### Rule 2.2.4 It is prohibited to reference external function interfaces and variables in extern declaration mode

##### Rule 2.2.5 Do not include header files in extern "C"

##### Rule 2.2.6 Do not use "using" to import namespace in a header file or before #include statements

#### <a name="dtype">2.3 Data Type</a>

##### Recommendation 2.3.1 Do not abuse typedef or #define to alias basic types

##### Rule 2.3.2 Use “using” instead of typedef to define the alias of a type to avoid shot-bomb modification caused by type changes

```cpp
// Correct
using FooBarPtr = std::shared_ptr<FooBar>;
// Incorrect
typedef std::shared_ptr<FooBar> FooBarPtr;
```

#### <a name="cons">2.4 Constant</a>

##### Rule 2.4.1 Do not use macros to replace constants

##### Rule 2.4.2 Do not use magic numbers or character strings

##### Recommendation 2.4.3 Ensure that a constant has only one responsibility

#### <a name="var">2.5 Variable</a>

##### Recommendation 2.5.1 Use namespaces to manage global constants. If the global constants are closely tied to a class, you can use static member constants to manage them

```cpp
namespace foo {
  int kGlobalVar;

  class Bar {
    private:
      static int static_member_var_;
  };
}
```

##### Rule 2.5.2 Do not use global variables. Use the singleton pattern cautiously to avoid abuse

##### Rule 2.5.3 A variable cannot be referenced again if it is contained in an increment or decrement operation in an expression

##### Rule 2.5.4 After the resource is released, immediately assign a new value to the pointer variable that points to a resource handle or descriptor, or set the value to NULL

##### Rule 2.5.5 Do not use uninitialized variables

#### <a name="exp">2.6 Expression</a>

##### Recommendation 2.6.1 When comparing expressions, follow the principle that the left side tends to change and the right side tends to remain unchanged

```cpp
// Correct
if (ret != SUCCESS) {
  ...
}

// Incorrect
if (SUCCESS != ret) {
  ...
}
```

##### Rule 2.6.2 Use parentheses to specify the operator precedence to avoid rookie errors

```cpp
// Correct
if (cond1 || (cond2 && cond3)) {
  ...
}

// Incorrect
if (cond1 || cond2 && cond3) {
  ...
}
```

#### <a name="exc">2.7 Conversion</a>

##### Rule 2.7.1 Use the type casting provided by the C++ instead of the C style. Do not use const_cast and reinterpret_cast

#### <a name="ctrl">2.8 Control Statement</a>

##### Rule 2.8.1 A switch statement must have a default branch

#### <a name="init">2.9 Declaration and Initialization</a>

##### Rule 2.9.1 Do not use `memcpy_s` or `memset_s` to initialize non-POD objects

#### <a name="ptr">2.10 Pointer and Array</a>

##### Rule 2.10.1 Do not use the pointer returned by c_str () of std::string

```cpp
// Incorrect
const char * a = std::to_string(12345).c_str();
```

##### Rule 2.10.2 Prefer `unique_ptr` to `shared_ptr`

##### Rule 2.10.3 Create `shared_ptr` by using `std::make_shared` instead of `new`

```cpp
// Correct
std::shared_ptr<FooBar> foo = std::make_shared<FooBar>();
// Incorrect
std::shared_ptr<FooBar> foo(new FooBar());
```

##### Rule 2.10.4 Use a smart pointer to manage objects. Do not use new or delete

##### Rule 2.10.5 Do not use auto_ptr

##### Rule 2.10.6 For formal parameters of pointer and reference types, if the parameters do not need to be modified, use const

##### Rule 2.10.7 Use the array length as a function parameter when the array is a function parameter

```cpp
int ParseMsg(BYTE *msg, size_t msgLen) {
  ...
}
```

#### <a name="str">2.11 String</a>

##### Rule 2.11.1 When saving a string, ensure that it has '\0' at the end

#### <a name="ast">2.12 Assert</a>

##### Rule 2.12.1 Assert cannot be used to verify errors that may occur when the program is running. To handle possible running errors, use error processing code

#### <a name="cls">2.13 Class and Object</a>

##### Rule 2.13.1 When a single object is released, delete is used. When an array object is released, delete [] is used

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

##### Rule 2.13.2 Do not use std::move to operate the const object

##### Rule 2.13.3 Strictly use virtual/override/final to modify virtual functions

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

#### <a name="fdes">2.14 Function Design</a>

##### Rule 2.14.1 Use the RAII feature to help track dynamic allocation

```cpp
// Correct
{
  std::lock_guard<std::mutex> lock(mutex_);
  ...
}
```

##### Rule 2.14.2 Avoid capturing by reference in lambdas that will not be used locally

```cpp
{
  int local_var = 1;
  auto func = [&]() { ...; std::cout << local_var << std::endl; };
  thread_pool.commit(func);
}
```

##### Rule 2.14.3 Do not use default parameter values for virtual functions

##### Recommendation 2.14.4 Use strongly typed parameters or member variables. Do not use void*

#### <a name="fuse">2.15 Function Usage</a>

##### Rule 2.15.1 The input parameter must be transferred before the output parameter

```cpp
  bool Func(const std::string &in, FooBar *out1, FooBar *out2);
```

##### Rule 2.15.2 Use `const T &` as the input parameter and `T *` as the output parameter for function transfer

```cpp
  bool Func(const std::string &in, FooBar *out1, FooBar *out2);
```

##### Rule 2.15.3 In the scenario where ownership is not involved, use T * or const T & instead of the smart pointer as the transfer parameter

```cpp
  // Correct
  bool Func(const FooBar &in);
  // Incorrect
  bool Func(std::shared_ptr<FooBar> in);
```

##### Rule 2.15.4 To transfer the ownership, you are advised to use shared_ptr + move to transfer parameters

```cpp
class Foo {
  public:
    explicit Foo(shared_ptr<T> x):x_(std::move(x)){}
  private:
    shared_ptr<T> x_;
};
```

##### Rule 2.15.5 Use explicit to modify single-parameter constructors and do not use explicit to modify multi-parameter constructors

```cpp
  explicit Foo(int x);          //good :white_check_mark:
  explicit Foo(int x, int y=0); //good :white_check_mark:
  Foo(int x, int y=0);          //bad  :x:
  explicit Foo(int x, int y);   //bad  :x:
```

##### Rule 2.15.6 Copy constructors and copy assignment operators should be implemented or hidden together

```cpp
class Foo {
  private:
    Foo(const Foo&) = default;
    Foo& operator=(const Foo&) = default;
    Foo(Foo&&) = delete;
    Foo& operator=(Foo&&) = delete;
};
```

##### Rule 2.15.7 [Question] Do not save or delete pointer parameters

##### Rule 2.15.8 [Question] Do not use insecure functions as listed

##### Rule 2.15.9 [Question] Do not use insecure exit functions as listed

```cpp
{
  Kill(...);            // If you invoke kill to forcibly terminate other processes (such as kill -9), the resources of other processes cannot be cleared.
  TerminateProcess();   // If you call the erminateProcess function to forcibly terminate other processes, the resources of other processes cannot be cleared.
  pthread_exit();       // Do not terminate a thread. The thread functions will exit automatically and safely after the execution is complete.
  ExitThread();         // Do not terminate a thread. The thread functions will exit automatically and safely after the execution is complete.
  exit();               // Do not call any function except the main function. The program must exit safely.
  ExitProcess();        // Do not call any function except the main function. The program must exit safely.
  abort();              //Forbidden. If abort is used, the program exits immediately and resources cannot be cleared.
}
```

##### Rule 2.15.10 Do not use the rand function to generate pseudo-random numbers for security purposes

The rand() function in the C standard library generates pseudo-random numbers. To generate random numbers, use /dev/random.

##### Rule 2.15.11 Do not use the string class to store sensitive information

The string class is a character string management class defined in C++. If sensitive information such as passwords is operated through the string class, the sensitive information can be
scattered in various places of the memory and cannot be cleared.

In the following code, the Foo function obtains the password, saves it to the string variable password, and then transfers it to the VerifyPassword function. In this process,
two copies of the password exist in the memory.

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

Sensitive information must be stored using char or unsigned char. For example:  

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

##### Rule 2.15.12 Clear sensitive information in the memory immediately after use

Sensitive information, such as passwords and keys, must be cleared immediately after being used to prevent attackers from obtaining the information.

#### <a name="mem">2.16 Memory</a>

##### Rule 2.16.1 Check whether memory allocation is successful

If the memory allocation fails, the subsequent operations may have undefined behavior risks. For example, if malloc fails to be applied for and a null pointer is returned, dereference of the null pointer is an undefined behavior.

##### Rule 2.16.2 Do not reference uninitialized memory

The memory allocated by malloc and new is not initialized to 0. Ensure that the memory is initialized before being referenced.

##### Rule 2.16.3 Do not use the realloc() function

The behavior of the realloc function varies with parameters. This is not a well-designed function. Although it provides some convenience in coding, it can easily cause various bugs.

##### Rule 2.16.4 Do not use the alloca() function to apply for stack memory

Neither POSIX nor C99 deﬁnes the alloca() behavior. Some platforms do not support this function. Using alloca() reduces program compatibility and portability. This function requests memory in the stack frame. The requested size may exceed the stack boundary, aﬀecting code execution.

#### <a name="file">2.17 File</a>

##### Rule 2.17.1 File paths must be canonicalized before use

A file path that comes from external data must be canonicalized first. If the file path is not canonicalized, attackers can construct a malicious file path to access the file without authorization.
For example, an attacker can construct “../../../etc/passwd” to access any file.
Use the realpath() function in Linux and the PathCanonicalize() function in Windows for file path canonicalization.
[Noncompliant Code Example]
The following code obtains the file name from an external system, concatenates the file name into a file path, and directly reads the file content. As a result, the attacker can read the content of any file.

```cpp
char *fileName = GetMsgFromRemote();
...
sprintf_s(untrustPath, sizeof(untrustPath), "/tmp/%s", fileName);
char *text = ReadFileContent(untrustPath);   // Bad: Did not check whether the untrustPath can be accessed before the data is read.
```

[Compliant Code Example]
Canonicalize the file path and then check whether the path is valid in the program.

```cpp
char *fileName = GetMsgFromRemote();
...
sprintf_s(untrustPath, sizeof(untrustPath), "/tmp/%s", fileName);
char path[PATH_MAX] = {0};
if (realpath(untrustPath, path) == NULL) {
    //error
    ...
}
if (!IsValidPath(path)) {    // Good: Check whether the file location is correct.
    //error
    ...
}
char *text = ReadFileContent(untrustPath);
```

Exceptions:
Command line programs that run on the console, or file paths that are manually entered on the console are exempted from this rule.

##### Rule 2.17.2 Do not create temporary files in the shared directory

Temporary ﬁles of a program must be exclusively used by itself. Otherwise, other users of the shared directory may obtain additional information about the program, resulting in information leakage. Therefore, do not create temporary files that should be used only by the program itself in any shared directory.
For example, the /tmp directory in Linux is a shared directory that all users can access. Do not create temporary files that should be used only by the program itself in this directory.

#### <a name="sf">2.18 Secure Function</a>

<table>
    <thead>
      <tr>
          <th style="width: 100px; ">Secure Function Type</th>
          <th style="width: 150px; ">Description</th>
          <th>Remarks</th>
      </tr>
    </thead>
    <tr>
      <td rowspan="1">xxx_s</td>
      <td>Secure function API of Huawei Secure C library</td>
      <td> It can be used when the Huawei Secure C library is integrated.</td>
    </tr>
    <tr>
      <td rowspan="1">xxx_sp</td>
      <td> API of Huawei Secure C library with optimized secure function performance (macro implementation)</td>
      <td>
      If count, destMax, and strSrc are constants, the performance-optimized macro interface displays its effect. If they are variables, the performance optimization effect is not obvious. The macro interface usage policy is as follows: The _s interface is used by default. The _sp interface is restricted in performance-sensitive call sites. The restriction scenarios are as follows:
      a)  memset_sp and memcpy_sp: destMax and count are constants.
      b)  strcpy_sp or strcat_sp: destMax is a constant and strSrc is a literal.
      c)  strncpy_sp or strncat_sp: destMax and count are constants and strSrc is a literal.</td>
    </tr>
</table>

##### Rule 2.15.18 Use secure functions provided by the community in the secure function library. Do not use dangerous functions related to memory operations

<table>
    <thead>
      <tr>
          <th style="width: 100px; ">Function Type</th>
          <th style="width: 150px; ">Dangerous Function</th>
          <th>Secure Surrogate Function</th>
      </tr>
    </thead>
    <tr>
      <td rowspan="4">Memory copy</td>
      <td>memcpy or bcopy</td>
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
      <td rowspan="4">String copy</td>
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
      <td rowspan="4">Character string concatenation</td>
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
      <td rowspan="6">Format output</td>
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
      <td>snprintf_s or snprintf_truncated_s</td>
    </tr>
    <tr>
      <td>vsnprintf</td>
      <td>vsnprintf_s or vsnprintf_truncated_s</td>
    </tr>
    <tr>
      <td rowspan="12">Format input</td>
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
      <td rowspan="1">Standard input stream input</td>
      <td>gets</td>
      <td>gets_s</td>
    </tr>
    <tr>
      <td rowspan="1">Memory initialization</td>
      <td>memset</td>
      <td>memset_s</td>
    </tr>
</table>

##### Rule 2.18.2 Correctly set the destMax parameter in secure functions

##### Rule 2.18.3 Do not encapsulate secure functions

##### Rule 2.18.4 Do not rename secure functions using macros

```cpp
#define XXX_memcpy_s memcpy_s
#define SEC_MEM_CPY memcpy_s
#define XX_memset_s(dst, dstMax, val, n) memset_s((dst), (dstMax), (val), (n))
```

##### Rule 2.18.5 Do not customize secure functions

Using macros to rename secure functions does not help static code scanning tools (non-compiled) customize rules for the misuse of secure functions. In addition, there are various naming styles.
In addition, it is not conducive to reminding the code developer of the real usage of functions, and may easily cause misunderstanding of the code and misuse of the renamed secure functions. Renaming secure functions will not
affect the checking capability of the secure functions.

```cpp
void MemcpySafe(void *dest, unsigned int destMax, const void *src, unsigned int count) {
  ...
}
```

##### Rule 2.18.6 Check the return values of secure functions and correctly process them

In principle, if a secure function is used, its return value must be checked. If the return value is ! = EOK, this function should be returned immediately,
and cannot be continued.
A secure function may have multiple erroneous return values. If a secure function returns a failure, perform the following operations (one or more) based on specific product scenario before it is returned
:
(1) Record logs.
(2) Return an error.
(3) Call abort to exit the program immediately.

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

##### Rule 2.18.7 Do not use external controllable data as function parameters for starting processes, such as system, popen, WinExec, ShellExecute, execl, xeclp, execle, execv, execvp and CreateProcess

##### Rule 2.18.8 Do not use external controllable data as parameters for module loading functions such as dlopen/LoadLibrary

##### Rule 2.18.9 Do not call non-asynchronous secure functions in signal processing routines

Signal processing routines should be as simple as possible. If a non-asynchronous secure function is called in a signal processing routine, the execution of the function may not generate expected results.
The signal handler in the following code writes logs by calling fprintf(), but the function is not asynchronous secure function.

```cpp
void Handler(int sigNum) {
  ...
  fprintf(stderr, "%s\n", info);
}
```

------------------
