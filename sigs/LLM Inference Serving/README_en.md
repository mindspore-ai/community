## Introduction to SIG

LLMs are moving from theoretical research to large-scale production. Providing high-throughput and low-latency LLM inference services has become one of the key tasks of AI foundational software stacks. In recent years, open-source LLM serving frameworks like vLLM and SGLang have advanced rapidly, supporting many models and features, and are widely used in academia and industry.

LLM Inference Serving SIG is dedicated to construct high-performance and user-friendly MindSpore-based LLM inference serving capabilities by leveraging open-source inference frameworks like vLLM and SGLang. LLM Inference Serving SIG has brewed [vLLM-MindSpore](https://gitee.com/mindspore/vllm_mindspore), an open source plugin enabling the vLLM framework to use MindSpore as the underlying inference computing platform for large model inference services.

The technical areas involved in LLM Inference Serving SIG mainly include the following:
1. **vLLM Compatibility and Adaptation**: Integrating MindSpore LLM inference capabilities to open-source LLM serving frameworks including vLLM and SGLang. Take vLLM as an example, mapping vLLM's PyTorch API calls to MindSpore and adapting to vLLM's plugin interfaces to integrate MindSpore's large model inference components into the vLLM framework.
2. **Large Model Inference Acceleration**: Leveraging MindSpore's graph fusion and communication-computation overlap technologies to achieve high-performance large model inference.

The LLM Inference Serving SIG is an open and collaborative platform for learning and development, welcoming developers to participate in enhancing MindSpore's large model inference capabilities and jointly building a foundation for technological accumulation and industrial success.

## Maintainers

* Zhai Zhiqiang (Leader of MindSpore Inference Architecture Design Team, Huawei Technical Expert)
* Ye Zichun (Ph.D. in Mathematics, Huawei Senior Engineer)
* Pan Shaowu (MindSpore Developer, Huawei Technical Expert)

## Committers

* Zou Liqin (MindSpore Developer, Huawei Senior Engineer, responsible for vLLM V1 architecture adaptation and development)
* Zhang Zhaochuang (MindSpore Developer, Huawei Senior Engineer, responsible for vLLM service component adaptation and development)
* Deng Yepeng (MindSpore Developer, Huawei Senior Engineer, responsible for MoE large model inference acceleration and vLLM adaptation and docking)
* Wang Shaocong (MindSpore Developer, Huawei Senior Engineer, responsible for large model distributed inference acceleration features)
* Zhang Xuetong (MindSpore Developer, Huawei Technical Expert, responsible for MindSpore large model inference acceleration system design)
* Tan Weicheng (MindSpore Developer, Huawei Senior Engineer, responsible for dense large model inference acceleration and vLLM adaptation and docking)

## Goals for 2025

1. Organizational Management: Establish organizational management standards for the SIG and invite initial members of Maintainers and Contributors to participate in SIG operations (3 Maintainers + at least 5 Contributors).
2. Ecosystem Expansion: Develop 30 official members of the LLM Inference Serving SIG, over 200 followers; cultivate 5 senior developers and 10 outstanding developers.
3. Feature Development: Support at least 20 State-of-the-Art LLMs and MMLMs, continuously adapt to the latest stable versions of vLLM, challenge to follow the evolution of the vLLM main branch, and ensure core features are adapted and supported within 2 days.
4. Event Organization: Achieve over 300 participants in vLLM-MindSpore experience activities, conduct 3 live technical sharing events, and collect over 10 technical articles.

## Major Activities

### 1. Online Technical Sharing Sessions

* Event Positioning: Jointly explore topics related to large model inference acceleration.
* Event Format: Regularly invite industry experts, university faculty and students, and senior developers to share topics.
* Event Frequency: Once every 1-2 months, focusing on 2-3 topics around the same theme each time.
* Sharing Scope: Technical topics related to the field of large model inference acceleration, including but not limited to:
  1. Technical architecture and user experience of vLLM, SGLang, and other open source LLM inference serving frameworks
  2. Development direction and improvement points of MindSpore's large model inference acceleration technology
  3. Emerging technologies, development experiences, and application suggestions for large model inference acceleration
  4. Introduction and demonstration of SIG feature development tasks and achievements
* Sharing Guests: Any SIG member, including university faculty and students, industry experts, and developers.
* Organizers: Rotated among Contributors.

### 2. vLLM-MindSpore Feature Development

* Event Positioning: Jointly participate in vLLM-MindSpore feature development to create a comprehensive and agile large model inference framework.
* Event Format: Regularly release large-grained feature development tasks, recruit developers to participate, and offer prizes or internship wages/certificates to those who complete the tasks.
* Event Frequency: Tasks released/refreshed quarterly.
* Event Content: To be discussed and refined.
* Organizers: Contributors in various technical fields.

### 3. Documentation and Product Experience Improvement Activities

* Event Positioning: Conduct product experience activities to collect suggestions and evaluations, and continuously improve the overall experience of documentation and products.
* Event Format: Developers submit issues/PRs to propose suggestions or modifications, accumulate points to win prizes.
* Event Frequency: Irregularly held.
* Event Planning:
  1. Documentation Experience: Phased activities targeting videos, tutorials, and APIs on the official website for crowd-testing experiences.
  2. Product Experience: Conducted with new version releases, focusing on the functional features of the released versions.

### 4. Regular Meetings

* Time: 7 PM on Wednesday or Thursday evenings, held bi-weekly.
* Meeting Content: Open routine exchanges for SIG feature development and organizational management.
* Meeting Topics:
  1. Fixed Topics: Progress and issue exchanges of feature development tasks assigned to SIG members.
  2. Optional Topics: Demonstrations of feature development interim achievements.
  3. Optional Topics: SIG organizational management (such as discussion of operational rules, refresh of Maintainers & Commiters' roles and responsibilities).

## SIG Organizational Management

### Member Identity Description

The SIG membership includes Members, Contributors, and Maintainers. The descriptions and application criteria for each role are as follows:

#### Members (Official Members)

* Rights: Participate in all SIG activities and communications.
* Application Criteria: Fill out the SIG membership application form (distributed when joining the WeChat discussion group).

#### Committers (Core Contributors)

* Responsibilities: Lead the planning, organization, and management of a specific area in technical development, daily operations, publicity, and event organization.
* Rights: Recorded in the SIG Hall of Fame, with priority in applying for MindSpore Evangelist or Senior Evangelist roles.
* Application Criteria: Already a Member, willing to take responsibility for a specific area and develop a work plan, and approved by a majority of other Maintainers and Contributors at the SIG regular meeting.

#### Maintainers (Leaders)

* Responsibilities: Responsible for the overall planning and strategy formulation of the SIG, guiding the development direction of the SIG, and reviewing key work plans.
* Rights: Recorded in the SIG Hall of Fame, with outstanding Maintainers having the opportunity to become members of the MindSpore TSC (Technical Steering Committee).
* Application Criteria: Already a Contributors for over one year, with significant contributions in the area of responsibility, recommended by at least one Maintainer, and approved by a majority of other Maintainers and Contributors at the SIG regular meeting.