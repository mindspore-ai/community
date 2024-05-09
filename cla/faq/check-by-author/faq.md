---
title: "Sign CLA"
weight: 6
description: |
  An overview about CLA.
---

## 机器人是怎么检查PR是否签署了CLA的

机器人是通过检查PullRequest中**所有commit**作者的邮箱是否都签署了CLA来判定PR是否完成了CLA签署

## 怎么查看PR所有commit的作者的邮箱

请访问这个[网页](https://gitee.com/api/v5/swagger#/getV5ReposOwnerRepoPullsNumberCommits)，输入pr信息进行查看

PR中某个commit的作者的邮箱见下图。

![commit-author-email](commit_author_email.png)

## 当某个commit作者的邮箱未签署CLA怎么处理

   1. 使用该邮箱签署CLA

   2. 如果该邮箱签署的是员工CLA，请确保该邮箱已经被所属企业的CLA管理员激活

   3. 如果该commit的邮箱设置错误，请参考[下一节](#amend_email)的方法处理

## 怎么修改commit作者的邮箱<a id="amend_email"/>

   step1: 运行如下命令进入交互式界面，需要替换参数 **n** 。在界面中选择需要修改的commit，将pick 改为 edit，之后按界面提示保存设置并退出

   ```sh
   git rebase -i HEAD~n # n 是需要修改的commit的编号，最新提交的commit的编号是1，以此类推

   ```

   step2: 运行如下命令修改commit的作者和其邮箱, **--author** 参数指定作者(Gitee ID)和邮箱

   ```sh
   git commit --amend --author="Jessica Smith <email@address.com>" --no-edit

   git rebase --continue

   ```

   step3: 请重新提交commit，以便更新PR的commit信息

   step4: 到PR的页面评论 */check-cla* ，以便重新检查CLA

## 开发建议

### 怎么设置本地开发环境

在开发前请按如下方式配置git。这里的邮箱必须是已经签署过CLA

```sh
git config user.name [gitee id]

git config user.email example@xx.com
```
