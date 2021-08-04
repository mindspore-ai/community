# 关于CI机器人规划

## 背景

随着MindSpore社区的迅速发展，社区成员、用户的互动和协作越来越频繁，社区需要投入大量的人力去开展社区治理工作（包含入门辅导、问题分发与解答、代码检视与合入、文化和活动宣传等）。

本文档旨在通过社区CI机器人的规划与建设，帮助社区成员、用户更高效的开展活动，减少人工重复性的工作投入，高效协作，促进社区快速发展。

## 整体规划

本章节会针对ISSUE和PR类的具体场景展开说明。

### ISSUE类

#### ISSUE: 提供帮助

- 给予ISSUE内容填写规范指导
- 给予ISSUE标签机制辅导

#### ISSUE: 协助解决

- 给予ISSUE标签建议
- 推荐ISSUE负责人、协作者、外部志愿者。
- 推荐问题的相似问题参考
- 提供一些入门ISSUE（good-first-issue）
- 推荐一些成员参与SIG活动、会议等

#### ISSUE: 提供福利

- 推荐一些大赛
- 推荐一些工作机会

### PR类

#### PR: 提供帮助

- CLA签署指南
- GIT操作指南
- 常见编码规范或指南（Python/C++/JAVA）

#### PR: 协助解决

- 提升代码质量
    - 门禁流水线（静态检查工具）
        - Markdown文档检查：markdownlint
        - 英文单词拼写检查：codespell
        - Python类检查：pylint
        - C++类检查：cpplint, cppcheck
        - 构建类检查：cmakelint
        - 脚本检查：shellcheck
        - 代码质量（代码圈复杂度、代码行）检查：lizard
- 帮助指派reviewer和approver

#### PR: 给予激励

- 推荐成为reviewer和committer
- 给予社区贡献证书。
