# 门禁告警检查规范（试运行）

## 目标

门禁告警规范旨在统一编码风格，使得合入代码符合MindSpore编码风格，同时让开发者做好代码上库前的各项自检，遵循基础代码质量规范。

## 门禁工具及遵循规范

新增代码英文拼写需满足Codespell单词拼写检查，规则详见：[Codespell规则](https://github.com/codespell-project/codespell)

新增C&C++代码需满足ClangFormat代码格式检查，配置请查阅mindspore目录下的 .clang-format文件，规则详见：[ClangFormat文档](https://clang.llvm.org/docs/ClangFormat.html)

新增C&C++代码需满足CppCheck&Cpplint 静态检查，规则详见：[CppCheck文档](https://cppcheck.sourceforge.io/) 与 [Cpplint文档](https://github.com/cpplint/cpplint)

新增C&C++代码需符合C&C++编码规范，规则详见：[C++编码规范](https://e.gitee.com/mind_spore/docs/1015619/file/2796407?sub_id=5766886)

新增Python代码需符合Pylint静态检查，规则详见：[Pylint文档](https://pylint.pycqa.org/en/latest/)

新增Python代码符合Python编码规范，规则详见：[Python编码规范](https://e.gitee.com/mind_spore/docs/1015695/file/2796633?sub_id=5767134)

C&C++&Python函数长度与圈复杂度需满足Lizard检查，规则详见：[Lizard文档](https://github.com/terryyin/lizard)

新增Cmake代码需满足Cmakelint代码静态检查，规则详见：[Cmakelint规则](https://cmake-format.readthedocs.io/en/latest/cmake-lint.html)

新增Shell代码需满足Shellcheck静态检查，规则详见：[Shellcheck文档](https://www.shellcheck.net/)

API注释格式需满足Darglint检查，规则详见：[Darglint文档](https://github.com/terrencepreilly/darglint)

Markdown文件需满足Markdownlint检查，规则详见：[Markdownlint文档](https://github.com/DavidAnson/markdownlint)

新增rst文档需满足Rstlint静态检查，规则详见：[Rstlint文档](https://pypi.org/project/restructuredtext-lint/)

链接有效性需满足Linklint检查，规则详见：[LinkLint文档](http://www.linklint.org/)

### 上库自检：

需要认真审视代码检视checklist符合情况，规则详见：[代码检视checklist](https://gitee.com/mindspore/community/blob/master/security/code_review_checklist_mechanism.md)
