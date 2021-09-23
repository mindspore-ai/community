# DX SIG Governance Charter

The Charter follows the convention described in MindSpore Open Governance [governance.md](https://gitee.com/mindspore/community/blob/master/governance.md). This article will be updated as needed to meet the requirements of MindSpore Open Governance.

In order to standardize the community seats and allow community participants to better integrate into the community, each SIG members should check the following guidelines to obtain a community seat:

## SIG maintainers

At the beginning of the establishment of DX SIG, the role of SIG Lead was set as the initial maintainer. The list is as follows:

  - CaoJian @JianCao81
  - Li Zi (a.k.a Clement Li) @clement_li

In order to better serve the community developers, three additional maintainers was elected in the August SIG meeting. The list is as follows:

  - Zhao Boxuan @BoxuanZhao 
  - Xia Wenzong @WenzongXia 
  - Zhu Naipan @zhunaipan （The original elected Wang Yehui applied for no longer serving as the maintainer）

The maintainers of the SIG group come from different regions, universities, and companies, and have different responsibilities according to different backgrounds, but all the maintainers have in common:

  - The maintainers have a shared responsibility for the success of the project.
  - The maintainers have made long-term and regular time investment to improve the project.
  - The maintainers spend time doing whatever needs to be done but not necessarily the most interesting thing.

Maintainers are often underestimated because the work they do is not obvious. It is often very simple to identify excellent and technologically advanced features,
However, it is often difficult to appreciate the absence of bugs, slow but stable improvements, or the reliability of the release process, and these are the fundamental differences between a great project and a good project.

## Maintainers election

The maintainer is a contributor who has been active in the community for a long time. Contributors are eligible for maintainer nomination through **not less than 3 months** of code contribution, code review, and issue discussion classification.

But contributions alone cannot make a contributor become a maintainer. It also needs to win the trust of the current maintainer and other project contributors, and its decisions and actions need to be in the best interests of the project.

The existing maintainer regularly organizes a list of contributors who have shown regular activities on the project in the past few months. From this list, select the maintainer candidate and nominate on the maintainer mailing list.

After nominating candidates on SIG Slack and Issue, the existing maintainers will discuss the candidates, provide feedback and vote in the next **5 working days**. Newly nominated maintainers need at least **more than half (>50%)** of the current maintainers to vote in favor.

If the candidate is approved, the maintainer will contact the candidate, inviting them to add the contributor to this document and submit a PR. When the PR is merged, the candidate will become the maintainer.

## Maintainers withdrawal

Maintainer can withdraw from the seat based on his voluntary abandonment request or his inability to effectively perform maintainer duties in the project.

### Giving up the seats

Due to changes in situations such as interest and enthusiasm, if the current maintainer is consciously unable/unwilling to continue to perform the duties of the maintainer, he can inform other maintainers to voluntarily give up the maintainer seat.

Abandoners should help the community find successors as much as possible, and at least they need to ensure that the work of the community will not be interrupted by their departure.

### Inability to effectively perform maintainer duties

Maintainer representatives will regularly review the community activities of all maintainers in the past three months. If the existing maintainer has not shown important activities in the project for a long time, consider removing it.
The maintainer represents the rotation of all maintainers, and the rotation period is three months.

If the maintainer shows insufficient activity during this period, the representative of the maintainer will contact the relevant parties and ask if they want to continue to serve as the maintainer. If it decides to withdraw from the maintainer team, the maintainer representative will create a PR and delete it from the OWNERS file.

If the maintainer wants to continue to assume this role, but is unable to perform the required responsibilities, it can be removed by at least **more than half (>50%)** of the current maintainer’s votes, and the maintainer in discussion will not be removed Allow voting.

Voting can invite the maintainers of the SIG group to participate through the maintainer mailing list. The voting period is five working days.
Issues related to the performance of the maintainer under discussion should be discussed with other maintainers during the voting process. All discussions should be handled objectively and no personal attacks are allowed.

## Community decision

Both MindSpore core projects and SIGs are open source projects with open design concepts. This means that the code warehouse is the true source of all aspects of the project and the SIG group's concept, design, and development planning.

Therefore, each decision can be expressed as a change in the code bin.

All decisions that affect DX SIG, no matter how big or small, follow the same steps:

  - **Step 1**: Create PR. Anyone can do this.

  - **Step 2**: Discuss PR. Anyone can do this.

  - **Step 3**: MindSpore Community Owners merge, close or reject PR.

PR is reviewed by the current maintainer of DX SIG.