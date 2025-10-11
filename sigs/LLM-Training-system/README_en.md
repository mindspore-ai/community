# LLM Training System SIG Introduction

The LLM Training System SIG (Special Interest Group) is a technical team within the MindSpore open-source community focused on accelerating AI large model training using distributed parallel technologies. The team is dedicated to enhancing the usability and performance of large models (such as language, multimodal, and omnidirectional models) in distributed parallel training scenarios. It provides a parallel programming paradigm that enables efficient development and flexible combination of various parallel strategies, simplifies the complexity of parallel programming, and offers developers an extremely simple and efficient distributed parallel training experience.

The technical areas covered by the MindSpore Parallel SIG mainly include the following aspects:

1. **Parallel Optimization**: Utilizes parallel techniques such as data parallelism, tensor parallelism, and pipeline parallelism to split training tasks across multiple computing devices for collaborative processing, significantly improving large-scale model training efficiency and solving single-machine computing power bottlenecks.

2. **Computing Optimization**: Employs techniques like mixed-precision training, operator fusion, and sparse computing to reduce computational overhead; reduces the number of floating-point operations, merges memory access operations, and optimizes kernel scheduling to increase computational throughput while maintaining accuracy, substantially shortening training time.

3. **Communication Optimization**: Designs strategies like gradient compression, hierarchical AllReduce, and communication hiding to address parameter synchronization needs across multiple devices; aggregates communication operations and overlaps computation with communication to reduce inter-device communication latency and bandwidth usage, solving the problem of communication becoming a performance bottleneck in distributed training.

4. **Memory Optimization**: Uses methods like activation recomputation, Offload, and Zero Redundancy Optimizer (ZeRO) to reduce memory usage; dynamically releases intermediate variables, swaps some data to CPU memory, and shards optimizer states to significantly increase the model size manageable by a single device.

5. **Automatic Parallel Strategy Search**: Users do not need to concern themselves with strategy configuration; the framework automatically builds a cost model to find parallel strategies with shorter training times, reducing the cost of manual tuning.

6. **High Availability Training**: Employs elastic job scheduling and checkpoint resumption mechanisms to handle hardware failures or system exceptions. Combined with monitoring and fast recovery strategies, it ensures the stability of long-term training tasks, reduces training cost losses caused by unexpected interruptions, and improves the overall reliability of large-scale training.

The SIG provides a platform for experts and enthusiasts in the above fields to communicate and collaborate. Our vision is to build world-leading distributed parallel technology rooted in MindSpore. The goals of the MindSpore Parallel SIG are twofold:

1. Continuously improve the usability and performance of MindSpore distributed training through automatic parallelism.

2. Assist MindSpore in building industry-leading large model training capabilities.

## SIG Repository

1. [LLM Training System SIG](https://gitee.com/mindspore/community/tree/master/sigs/LLM-Training-System)

## Maintainers

* Li Cheng (Special Appointment Researcher, University of Science and Technology of China)
* Su Teng @stsuteng (MindSpore Chief Expert, SIG Initiator)
* Yang Zhenzhang @yangzhenzhang (MindSpore Distributed Parallel Training Technology Expert)
* Wang Kaisheng @kisnwang (MindSpore Distributed Parallel Training Technology Expert)
* Yao Yifan @yao_yf (MindSpore Distributed Parallel Training Technology Expert)

## Committers

* Tang Huikang @HulkTang (MindSpore AI Engineering Technology Expert, Head of Heterogeneous Parallelism)
* Liu Yanwei @liu-yanwei6 (MindSpore AI Engineering Technology Expert, Head of MoE Parallelism)
* Wang Haoran @bj-wang (MindSpore AI Engineering Technology Expert, Head of Automatic Strategy Search)
* Miao Yanming @askmiao (MindSpore AI Engineering Technology Expert, Head of Training High Availability)

## Q4 2025 Goals

1. Organization Management: Improve the SIG organization, inviting initial members including Maintainers (5) and Committers (at least 4) to participate in SIG operations.

2. Feature Development: Add at least 2 new features in areas such as declarative programming in automatic parallelism and network training acceleration, and recruit developers for co-development.

3. Activity Execution: Conduct at least 2 live technical sharing sessions and solicit 3+ technical articles in the field of distributed parallelism.

---

## Development Directions

### 1. Key Function and Module Development

* Responsible for the design, development, and optimization of core functional modules in the MindSpore Parallel project.
* Write high-quality, reusable, and extensible code.

### 2. Testing, Verification, and Standardization

* Write and maintain unit tests, integration tests, performance tests, and accuracy verification scripts.
* Establish standards for configuration, output result consistency, and reproducibility.
* Deliver automated CI/CD processes.

### 3. Documentation and Examples

* Write user documentation, developer guides, API references, and quick start tutorials.
* Provide executable examples, Notebooks, and reference configurations.
* Continuously improve FAQs and usage guides.

**Developers interested in the above development directions are welcome to contribute!**

---

## Communication Activities

### 1. Regular Meetings

* Monthly online SIG regular meetings are held at 3:00 PM on the first Friday of each month.
* Report task progress, discuss technical solutions, and share the latest updates.
* SIG organizational management (such as discussions on operational rules, updates on Maintainers & Committers personnel and responsibilities).

### 2. Technical Discussions and Design Reviews

* Organize thematic technical sharing sessions (e.g., design details of specific PRs, model training optimization solutions).
* Conduct RFC (Request for Comments) discussions for community review of major designs or features.

### 3. Issue Tracking and PR Reviews

* Regularly organize and review Issues/Pull Requests.
* Coordinate the Maintainer and Committer teams for PR reviews.
* Publicly disclose review records and decisions to maintain transparency.

### 4. Community Communication and External Sharing

* Maintain discussion channels (e.g., Gitee Issues, mailing lists, WeChat groups, community forums, etc.).
* Periodically host community meetups and sharing sessions to disseminate SIG progress and successful industry and research experiences.

---

## SIG Organization and Management

### Member Role Description

Member roles within the SIG include Members, Contributors, and Maintainers. The descriptions and application criteria for each role are as follows:

#### Maintainer

* Responsibilities and Benefits:
  1. Determine the technical roadmap for projects under the SIG's responsibility: including planning and decision-making for the SIG's technical direction, milestone planning, and architecture evolution.
  2. Develop release plans for projects under the SIG's responsibility: identify key requirements and release plans for the SIG; participate in community PM activities and align SIG plans with community release milestone schedules.
  3. Participate in community coordination activities: represent the SIG in activities and specific meetings organized by the MindSpore Technical Steering Committee or Board.
  4. Convene SIG meetings: regularly organize SIG meetings to resolve disputes escalated within the SIG.
* Requirements to Join:
  1. Served as a Reviewer for at least 3 months.
  2. Participated as the primary reviewer in at least 12 PR reviews.
  3. Reviewed or merged at least 30 substantial PRs into the codebase.
  4. Familiar with the codebase.
  5. Can self-nominate or be nominated by a subproject Maintainer, with no objections from other subproject Maintainers.

#### Committer

* Responsibilities and Benefits:
  1. Review PRs: Complete reviews of PRs submitted by Contributors, following the community's [Programming Recommendations and Secure Coding Standards](https://gitee.com/mindspore/community/blob/master/guidelines/python_programming_specification_zh_cn.md).
  2. Handle assigned issues: Refer to the "[Issue Handling Process](https://gitee.com/mindspore/community/blob/master/guidelines/issue_process_CN.md)".
  3. Track dependency issues: In the development branch, updates from other SIGs may break dependencies of projects within this SIG. Committers will receive alerts and should attempt to resolve these issues. Dependency errors may prevent end-users from updating systems. While packaging teams may intervene and rebuild affected projects, Committers should not rely solely on such rebuilds.
  4. Notify potentially affected SIGs of interface changes: Committers must understand, review, and decide on the impact of changes due to dependencies, and announce/send alert emails for API or ABI changes. Such announcements should be made at least one week before the change and notify all potentially affected SIGs.
* Requirements to Join:
  1. Served as a Contributor for at least 3 months.
  2. Participated as the primary reviewer in at least 6 PR reviews.
  3. Reviewed or merged at least 20 substantial PRs into the codebase.
  4. Familiar with the codebase.
  5. Can self-nominate or be nominated by a Reviewer or Maintainer of the SIG.

#### Contributor

* Responsibilities and Benefits:
  1. Respond to assigned issues and PRs.
  2. Contributed code should meet the following criteria (including but not limited to): well-tested; maintains consistently passing test cases; addresses subsequent errors or issues.
  3. Can be assigned issues or PRs.
  Note: Members who frequently contribute code should actively participate in code reviews and have the opportunity to become SIG Committers (Reviewers).
* Requirements to Join:
  1. Registered member on Gitee.
  2. Made various contributions to the SIG or community, including but not limited to: submitting or reviewing PRs on Gitee; filing or commenting on issues on Gitee; participating in SIG or community discussions.
  3. Have read the Contributor Guide and are familiar with the contribution process.
  4. Active participation in 1 or more SIGs.

## Upcoming Activities and Meeting Announcements

1. Technical Sharing Session

2. SIG Regular Meeting

## Past Activities and Meetings

* [March 16, 2022: Detailed Explanation of MindSpore's Parallel Strategies](https://mp.weixin.qq.com/s/ENi8sbghtIEcQFnGpWVEXg)
