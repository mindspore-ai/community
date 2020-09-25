<!-- TOC -->

[Note](#note)
- [Scope](#scope)
    - [Code Style](#1-code-style)
        - [Naming](#11-naming)
        - [Format](#12-format)
        - [Comment](#13-comment)
        - [Log](#14-log)
    - [General Coding](#2-general-coding)
        - [Interface Declaration](#21-interface-declaration)
        - [Data Verification](#22-data-verification)
        - [Abnormal Behavior](#23-abnormal-behavior)
        - [Serialization and Deserialization](#24-serialization-and-deserialization)

<!-- /TOC -->

## Note

This document is developed based on [PEP 8](https://www.python.org/dev/peps/pep-0008/), Huawei Python Coding Style Guide, Huawei Python Secure Coding Standard, and industry consensus. To participate in the MindSpore community, please comply with this style guide (for contents conflict with the PEP 8 style guide), and then with PEP 8.  
If you disagree with the rules, you are advised to submit an issue and provide reasons. The issue can take effect after being reviewed, accepted, and modified by the MindSpore community operation team.

## Scope

MindSpore open source community  

------------------------


### <a name="psf">1. Code Style</a>

#### <a name="pnm">1.1 Naming</a>

##### Rule 1.1.1 Package names and module names are in lowercase and cannot contain underscores (_). 

##### Rule 1.1.2 Class names are in the CamelCase style. The first letter must be capitalized, and the prefix is a private class underscore (_).  

```python
class _Foo:
    _instance = None
    pass
```

##### Rule 1.1.3 Function names and variable names are in lowercase and separated by underscores (_) when containing multiple words.  

```python
def _func_example(path):
    pass
```

##### Recommendation 1.1.4 Do not use single-character names except for iterators and counters.     

#### <a name="pcs">1.2 Format</a>

##### Rule 1.2.1 Ensure that each line contains a maximum of 120 characters.

If a line contains more than 120 characters, start a new line properly.   

##### Rule 1.2.2 Use spaces to indent, four at a time. Tab indent is forbidden.  

##### Rule 1.2.3 The import sequence is as follows: standard library, third-party, and customization module.   

##### Rule 1.2.4 Do not use parentheses in return statements and conditional statements.   

##### Rule 1.2.5 There are two blank lines between a module-level function and a class, and one blank line between class member functions. Add blank lines between comments and code as needed. In principle, there should be no more than two blank lines.   

##### Rule 1.2.6 Delete invalid or redundant code directly. Do not retain the code in the form of comments or TODO. You are advised to submit an issue record.

#### <a name="pns">1.3 Comment</a>

##### Rule 1.3.1 File header comments must contain copyright statements.

All Python files must contain the following copyright statements:

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

> Notes:  
> Files created in 2020 should contain `Copyright 2020 Huawei Technologies Co., Ltd`.  
> Files created in 2019 and modified in 2020 should contain `Copyright 2019-2020 Huawei Technologies Co., Ltd`.

##### Rule 1.3.2 Comply with the comment formats of external classes, methods, operators, and cells:

- The comment formats of `class` and `def` are the same. Use Python comments which is generally accepted by the industry, and indent the comments under a declaration. All `class` and `def`should be commented. You can write only one introduction for the classes and methods in the module.
- For details about the comment formats, see [MindSpore Comment Specifications](https://gitlab.huawei.com/mindspore/docs/wikis/Python-API%E6%B3%A8%E9%87%8A%E8%A7%84%E8%8C%83). 

##### Rule 1.3.3 Do not use comments to mask Pylint alarms.

#### <a name="pls">1.4 Log</a>

##### Rule 1.4.1 Capitalize the first letter of the exception log text. 

##### Rule 1.4.2 Variable names in log texts must be marked with single quotation marks. 

### <a name="pcc">2. General Coding</a>

#### <a name="pif">2.1 Interface Declaration</a>

##### Rule 2.1.1 User interfaces are described in __all__ of a file, and __all__ is placed between import and code.

##### Rule 2.1.2 Use underscores (_) to prefixe the non-external methods used by the current file. Method names used across modules do not need underscore prefixes. User interfaces are declared in __all__ of a file.   

#### <a name="pdc">2.2 Data Verification</a>

##### Rule 2.2.1 Check the validity of all external data, including but not limited to function input parameters, external input named lines, file formats, file sizes, environment variables, and user data.

##### Recommendation 2.2.2 File paths must be canonicalized before use.

A file path that comes from external data must be canonicalized first. If the file path is not canonicalized, attackers can construct a malicious file path to access the file without authorization.
For example, an attacker can construct ../../../etc/passwd to access any file.
For example, use the realpath() function in Linux and the PathCanonicalize() function in Windows for file path canonicalization.
[Noncompliant Code Example]
The following code obtains the file name from an external system, concatenates the file name into a file path, and directly reads the file content. As a result, the attacker can read the content of any file.
```python
    The following is an example of error code:
```
[Compliant Code Example]
Canonicalize the file path and then check whether the path is valid in the program.
```python
    The following is an example of correct code:
```
[Exceptions]
Command line programs that run on the console, or file paths that are manually entered on the console are exempted from this rule.

##### Rule 2.2.3 Do not invoke the OS command parser to run commands or programs.  

If untrusted input that is not verified is used as a parameter or part of a system command, vulnerability may occur in a command injection. For the command injection vulnerability, the command is executed at the same privilege level as the Python application. It provides a function similar to shells for attackers. In Python, os.system or os.popen is often used to call a new process. If the command to be executed comes from external input, command and parameter injection may occur.
When running the command, pay attention to the following points:  
1. Do not concatenate the input parameters in the character string for command execution. If the input parameters must be concatenated, perform whitelist filtering on the input parameters.
2. Verify the type of the input parameters. For example, integer data can be mandatorily converted into integers.
3. Ensure that the formatted string is correct. For example, use %d instead of %s to concatenate parameters of the int type.

[Noncompliant Code Example 1]  
The attacker can find the value of the environment variable APPHOME and place the attacking program against the constant INITCMD in the corresponding directory 
to execute the attack.

```python
    home = os.getenv('APPHOME')
    cmd = os.path.join(home, INITCMD)
    os.system(cmd)
```

[Noncompliant Code Example 2]  
The value of the backuptype attribute is not verified. The value is entered by the user and may be attacked. For example, the value entered by the user is && del.
c:\\dbms\\*.* "：

```python
    # The value is obtained from the user configuration.
    btype = req.field('backuptype')
    cmd = "cmd.exe /K \"c:\\util\\rmanDB.bat " + btype + "&&c:\\util\\cleanup.bat\""
    os.system(cmd)
```

[Noncompliant Code Example 3]  
The value of the backuptype attribute is not verified. The value is entered by the user, which may be attacked. For example, the value entered by the user is && del.
c:\\dbms\\*.* ":

```python
    import os
    import sys
    try:
        print(os.system("ls " + sys.argv[1]))
    except Exception as ex:
        print('exception:', ex)
```
Attackers can run the following command to exploit this vulnerability:
```python
    python test.py ". && echo bad"
```
Actually, the following two commands are executed:
```python
    ls .
    echo bad
```

[Compliant Code Example]  
Do not use os.system. You can use standard APIs instead of running system commands to complete the tasks.
```python
    import os
    import sys
    try:
        print(os.listdir(sys.argv[1]))
    except Exception as ex:
        print(ex)
```

#### <a name="pex">2.3 Abnormal Behavior</a>

##### Rule 2.3.1 Exceptions must be properly handled. Do not suppress or ignore exceptions found in the check results.

Ensure that the programs in each except block continue to operate only when they are valid. The except block must either recover from an exception or throw another exception suitable for the context of the current catch block to allow the most adjacent outer try-except statement block to recover.
[Compliant Code Example]
The correct method is to avoid using os.system. You can use standard APIs instead of running system commands to complete the tasks.
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
[Exceptions] 
1. If the resource release failure does not affect the subsequent program behavior, the exception that occurs during resource release can be suppressed. Examples of releasing resources include closing files, network sockets, threads, and so on. These resources are usually released in the except or fianlly block and will not be used during subsequent program operation. Therefore, unless the resources are exhausted, these exceptions cannot affect the subsequent behavior of the program. When the resource exhaustion is resolved, you only need to purify the exceptions and record logs (for future improvement). In this case, there is no need to handle other errors.
2. If it is impossible to recover from an exception at a specific abstraction level, the code at that level does not need to handle the exception. Instead, the code at that level should throw an appropriate exception so that higher-level code can catch the exception and attempt to recover it. In this case, the most common implementation method is to omit the catch statement block and allow the exception to be broadcast.

##### Rule 2.3.2 When using try…except… to protect the code, use finally… to ensure that operation objects are released after an exception occurs.  

When using try…except… to protect the code, if an exception occurs during code execution, use finally… to ensure that operation objects can be released.

[Compliant Code Example]
```python
    handle = open(r"/tmp/sample_data.txt") # May raise IOError
    try:
        data = handle.read() # May raise UnicodeDecodeError
    except UnicodeDecodeError as decode_error:
        print(decode_error)
    finally:
        handle.close() # Always run after try:
```

##### Rule 2.3.3 Do not capture all exceptions by executing the "except:" statement.  

Note that Python is tolerant of exceptions. The "except:" statement can capture any errors, including those in Python syntax. Executing the "except:" statement hides potential bugs. Therefore, specify exceptions to be handled when using try…except… to protect the code. The Exception class is the base class of most runtime exceptions and should not be used in the "except:" statement. The "try" statement should contain only exceptions that must be handled at the current location. The "except:" statement should only capture exceptions that must be handled. For example, for the code for opening files, the "try" statement should contain only the "open" statement. The "except:" statement only captures the FileNotFoundError exceptions. Other unexpected exceptions are captured by functions in the upper layer, or are transparently transmitted to external programs for exposure.

[Noncompliant Code Example]  
Two types of exceptions may occur in the following code. When executing the "except:" statement for unified handle, if exceptions occur in the open statement execution, and the "except:" statement handle is invalid, the close method will be called and an error that the reported handle is undefined will be reported.
```python
    try:
        handle = open(r"/tmp/sample_data.txt") # May raise IOError
        data = handle.read() # May raise UnicodeDecodeError
    except:
        handle.close()
```
[Compliant Code Example]  
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

##### Rule 2.3.4 The raise keyword that is not contained in the "except:" statement must have exceptions specified.  

**Note**: The raise keyword can be used only in the "try-except" statement and re-throw exceptions captured by the "except:" statement.

[Noncompliant Code Example]

```python
    a = 1
    if a==1:
        raise
```
[Compliant Code Example 1] Raise an exception or a custom exception.
```python
    a = 1
    if a==1:
        raise Exception
```

[Compliant Code Example 2] Use the raise keyword in the "try-except" statement.
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

#### <a name="psr">2.4 Serialization and Deserialization</a>

##### Rule 2.4.1 When pickle has security risks, do not use the pickle.load, cPickle.load, or shelve module to load untrusted data.

##### Rule 2.4.2 Use secure random numbers.  

Python implements the random number generation function in the random module, and implements various distributed pseudo-random number generators. The generated random numbers can be
evenly distributed, in Gaussian distribution, logarithmic normal distribution, negative exponential distribution, alpha distribution, or beta distribution manners. However, these random numbers are pseudo-random numbers, and 
cannot be used for applications requiring security encryption.
Use /dev/random to generate secure random numbers, or use the secrets module introduced by Python 3.6 to generate secure random numbers.

[Noncompliant Code Example]

```python
    import random
    # Pseudo-random numbers
    func = random.SystemRandom()
    print(func.random())
    print(func.randint(0, 10))
```

[Compliant Code Example]

```python
    import platform
    # For details about the length, see the cryptographic algorithm specifications. The length varies according to the scenario.
    randLength = 16
    if platform.system() == 'Linux':
    with open("/dev/random", 'rb') as file:
    sr = file.read(randLength)
    print(sr)
```

##### Rule 2.4.3 The assert statement is usually used only in test code. Do not include the assert function in released versions.

The assert statement is used only for internal tests during R&D. If AssertionError occurs, it indicates that errors exist in software design or the code.
The software should be modified to resolve this issue. Do not include the assert function in externally released versions for production.