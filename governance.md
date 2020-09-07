# MindSpore Open Governance

## Overview

MindSpore is embracing open governance to build a truly open source ecosystem
and developer friendly atmosphere. The governance model adopted here is heavily
influenced by the [onnx governance](https://github.com/onnx/onnx/blob/master/community/readme.md)
which drew reference from the [kubernetes governance](https://github.com/kubernetes/community/blob/master/governance.md).
*For similar structures some of the same wordings from onnx governance are
borrowed to adhere to the originally construed meaning.*

MindSpore open governance adopts three types of governance structures: Technical
Steering Committee, Special Interest Groups (SIGs) and Working Groups (WG).
MindSpore also defines two roles for development: *Contributor* and *Approver*.
*Contributors* are the developers who have contributed code which got merged and
*Approvers* are those who have the right to merge code. *Contributors* can vote
and run for the *Approver* role. The Technical Steering Committee charters
SIGs/WGs and appoints SIG/WG chairs. Every piece of MindSpore belongs to some
SIG. Contributors and Approvers participate in one or more SIGs.

The effort is bootstrapped with an initial Technical Steering Committee and set
of SIGs with the first elections to occur after 1 year.

## Principles

The MindSpore community adheres to the following principles:

* __Open__: MindSpore is open source. See repository guidelines and CLA, below.
* __Welcoming and respectful__: See Code of Conduct, below.
* __Transparent and accessible__: Work and collaboration should be done in
public. See SIG governance, below.
* __Merit__: Ideas and contributions are accepted according to their technical
merit and alignment with project objectives, scope and design principles.
* __Speed__: Contributing the time and effort to ensure fast decision-making is
key to ensuring that the specifications produced is aligned to the fast
iteration of machine learning technologies.

## Community Roles

### Contributors
Contributors are the developers who have contributed code and got merged. They
can have issues and PRs assigned to them. They also have voting privileges.
Contributors can be active in many ways including but not limited to:

* Authoring or reviewing PRs, but do not have right to merge
* Filing or commenting on issues
* Contributing to SIG, WG, or community discussions (e.g. IRC, meetings,
  email discussion forums, Stack Overflow, etc)
* Creator of content, promoting and advocating the MindSpore community.

The first group of Contributors will be appointed and more Contributors will be
added accordingly.

### Approvers
Approvers are *Contributors* who have the right to merge code. Approvers are
responsible for reviewing contributions for acceptance by considering not just
code quality but also holistic impact of the contribution including
compatibility, performance, and interactions with other areas.

Approvers need to be active *Contributors* for at least 3 months and will be
selected in a voting process within a SIG/WG by all the related *Contributors*.
The first group of Approvers will be appointed for an one-year term.
After the first year all the Approvers need to be qualified through open
elections.

### Community Partners
Community Partners are organizations (include but not limited to companies,
  universities, research institutes, industrial associations, open source
  foundations/communities/projects, etc.) that support MindSpore in one or more
  of the following ways:
* Having employees participate in SIGs, Working Groups, or the Technical
Steering Committee
* Hosting a workshop or meetup for MindSpore
* Providing resources for building or hosting MindSpore assets
* Doing media or PR activities to promote MindSpore
* Shipping a product that supports MindSpore
* Collaborating in open source development with MindSpore

Community Partners do not have any voting rights, except via their employees
who are *Contributors*. Affiliates and subsidiaries are considered as separate
organizations. Being a Community Partner does not by itself confer any
compliance or certification to the Community Partner's products.

### Community Manager
Community manager is the people who help run day to day MindSpore governance
operations. The role is appointed by the Technical Steering Committee and does
not have any code or voting related privileges by its own right. The role does
not have a term limit and its duration depends only upon the governance charter
approved by the Technical Steering Committee.

## Organizational Structure

The MindSpore community is organized in the following manner, with all
governance and execution being planned and coordinated as follows:

* **Technical Steering Committee** is made up of a set number of people whose
charter it is to define and iterate on the vision, goals, and governance process
of the MindSpore community.
* **Special  Interest Groups (SIGs)** are persistent groups that are responsible
for specific parts of the project. SIGs must have open and transparent
proceedings. Anyone is welcomed to participate and contribute provided they
follow the [Code of Conduct](code-of-conduct_en.md). The purpose of a SIG is to
develop a set of goals to be achieved over a set period of time, and then to
gather input, drive consensus and closure, implement code contributions, and
other related activities to achieve the goal. SIGs are also responsible for
ongoing maintenance of the code in their areas.
* **Working Groups** are groups that are formed to address issues that cross SIG
boundaries. Working groups do not own any feature code ownership or other long
term artifacts. Working groups can report back and act through involved SIGs.

## Language

The working language in MindSpore community is English, this applies to things
like code notation, documentation, ISSUE, PR and so forth. International
language support for documentation translation and localized presentations are
highly encouraged. An i18n WG could be formed to address multi-lang support.

### Technical Steering Committee

#### Role

The Technical Steering Committee has a set of rights and responsibilities
including the following:

* Define, evolve, and defend the vision, values, mission, and scope of the
community.
* Define, evolve, and defend a [Code of Conduct](code-of-conduct_en.md),  which
must include a neutral and unbiased process for resolving conflicts.
* Define and evolve project governance structures and policies,
including how members become Contributors, approvers, SIG chairs, etc.
* Charter and refine policy for defining new community groups (Special Interest
Groups, Working Groups, and any future possible defined structure), and
establish transparency and accountability policies for such groups.
* Decide, for the purpose of elections, who is a  member of standing of the
MindSpore community, and what privileges that entails.
* Decide which functional areas and scope are part of the MindSpore community,
including accepting new or pruning old SIGs and Working Groups.
* Decide how and when official releases of MindSpore artifacts are made and what
they include.
* Declare releases when quality/feature/other requirements are met.
* Control access to, establish processes regarding, and provide a final
escalation path for any MindSpore repository, which currently includes all
repositories under the MindSpore organizations
* Control and delegate access to and establish processes regarding other project
resources/assets, including artifact repositories, build and test infrastructure,
web sites and their domains, blogs, social-media accounts, etc.
* Define any certification process.
* Manage the MindSpore brand and any outbound marketing.
* Make decisions by majority vote if consensus cannot be reached.

#### Structure

The Technical Steering Committee (TSC) consists of representatives from the
community. The first group of TSC members will consist of representatives from
the founding members. The chairperson of the TSC will be appointed for the first
term. No single member entity may have more than 1 representative. TSC chair and
members all serve 1 year terms.

TSC Chair is the chairperson of the Technical Steering Committee that fulfills
the duties include hosting TSC meetings, organizing elections and participating
promotion related publicities. TSC Chair is a member of the sitting TSC and has
the same voting right as any other TSC member.

After the initial term, TSC members will elect the new TSC Chair for the next
term. The TSC member seat itself will constitute representative from the same
founding member entity, unless alterations occurs to that membership which
leads to either new TSC member appointed by the newly TSC-approved member entity,
or the vacancy of the seat if the TSC votes to shrink the size of the committee.

Additionally, TSC might create new Contributor representative seats which could be
open for any *Contributor* in the community to be elected into the seat via a
community vote. Only Contributors may vote, but would be restricted to no more
than one representative elected per member entity.

If a representative of the Technical Steering Committee changes affiliations,
by default the original member entity should appoint a new TSC representative.
If the employment change results in a single member entity having more than one
representative, then one of them must resign. If the
founding member entity fails to appoint a new TSC representative, the TSC will
decide the new seat. Elections will be held for the seat which is elected.

A Technical Steering Committee representative can be removed due to
[Code of Conduct](code-of-conduct_en.md) violations by a super majority vote in
the TSC.

#### Decision

The Technical Steering Committee (TSC) requires quorum of the member to be
present for any type of decision making process. An official TSC decision will
be carried through by a majority vote (i.e more than half of the TSC vote yes).

During the first year of the TSC term, in order to ensure the smooth progress
of the community, if TSC meeting does not get quorum in live attendance, then
an email quorum voting procedure will be initiated. If email voting does not get
quorum in a week, then the motion will be treated as approved if there is no
outstanding objection from any of the TSC member.

### SIG - Special Interest Groups

#### Role

The MindSpore project is organized primarily into Special Interest Groups, or
SIGs. Each SIG is comprised of individuals from multiple companies and
organizations, with a common purpose of advancing the project with respect to a
specific topic.

Our goal is to enable a distributed decision structure and code ownership,
as well as providing focused forums for getting work done, making decisions,
and on-boarding new Contributors. Every identifiable part of the project
(e.g., repository, subdirectory, API, test, issue, PR, IRC) is intended to be
owned by some SIG. At the time of inception of this organizational structure,
the following SIGs will be present:

| SIG name | Responsibilities |
| :------- | :--------------- |
| FrontEnd | This SIG is responsible for the development of MindSpore front-end expression. |
| Compiler | This SIG is responsible for the development of MindSpore high level graph compilation. |
| Executor | This SIG is responsible for the development of MindSpore back-end support for pipeline. |
| ModelZoo | This SIG is responsible for the development of MindSpore modelzoo and additional ops. |
| Data | This SIG is responsible for the development of MindSpore data processing and data format transformation. |
| GraphEngine | This SIG is responsible for the development of MindSpore graph engine for Ascend AI processor. |
| Visualization | This SIG is responsible for the development of MindSpore visualization tools. |
| Security | This SIG is responsible for the development of MindSpore security related tools. |
| AKG | This SIG is responsible for the development of MindSpore auto kernel generator. |

#### Structure

SIGs must have at least one, and may have up to two SIG chairs at any given
time. SIG chairs are intended to be organizers and facilitators, responsible for
the operation of the SIG and for communication and coordination with the other
SIGs, the Technical Steering Committee, and the broader community. All SIG
chairs are appointed by the Technical Steering Committee. If there are more
than two *Contributors* being considered for a particular SIG, the Technical
Steering Committee will vote on and resolve who the chairs would be. Candidates
need to be *Approvers*.

Each SIG must have a charter that specifies its scope (topics, sub-systems,
code repos and directories), responsibilities, and areas of authority. Charters
are submitted to the MindSpore community via PR for review and approval by the
Technical Steering Committee who will be looking to ensure the scope of the SIG
as represented in the charter is reasonable. All SIGs are expected to follow
the standards established by the Technical Steering Committee for how
*Contributors* are roles of authority/leadership are selected/granted, how
decisions are made, and how conflicts are resolved.

A primary reason that SIGs exist is as forums for collaboration. Much work in a
SIG should stay local within that SIG. However, SIGs must communicate in the
open, ensure other SIGs and community members can find meeting notes,
discussions, designs, and decisions, and periodically communicate a high-level
summary of the SIG's work to the community. SIGs are also responsible to:

* Meet regularly, at least monthly
* Keep up-to-date meeting notes, linked from the SIG's page in the community
repo
* Announce meeting agenda and minutes after each meeting, on the
`mindspore-discuss` mailing list and/or IRC or slack or other channel.
* Ensure the SIG's decision making is archived (i.e on IRC meeting log)
* Report activity in overall MindSpore community meetings
* Participate in release planning meetings, retrospective, etc (if relevant)
* Actively triage issues, PRs, test failures, etc. related to code and tests
owned by the SIG
* Use the above forums as the primary means of working, communicating, and
collaborating, as opposed to private emails and meetings

#### Decision making

When it is time to formalize the work-product from a SIG, votes are taken from
every *Contributor* who participates in the SIG. The list of active
*Contributors* is determined by the one (or two) SIG leads to ensure that only
those who have actively participated in the SIG can vote. At this time there is
no restrictions on how many *Contributors* from any one member entity can
participate (and hence vote). The Technical Steering Committee will monitor how
the community behaves and apply constraints if needed in the future.

While most work shouldn’t require expensive coordination with other SIGs, there
will be efforts (features, refactoring, etc.) that cross SIG boundaries. In this
case, it is expected that the SIGs coordinate with each other and come to
mutually agreed solutions. In some cases, it may make sense to form a Working
Group for joint work. Cross-SIG coordination will naturally require more time
and implies a certain amount of overhead. This is intentional to encourage
changes to be well encapsulated whenever possible.

### WG - Working Groups

Working Groups (WGs) are primarily used to facilitate topics of discussion that
cross SIG lines, or are topics which are short-lived and require a limited set
of decisions to be agreed upon. Working groups:

* do not own feature code that will be included in a certain release (document
  not applied here)
* have a clear goal measured through specific deliverables
* could choose to be retired after most of the goals are achieved

Working Groups can create glue code, specifications, recommendations, or
implementations for submission to the relevant SIGs for approval and acceptance.
At time of inception of this organizational structure, the following WGs will be
present initially:

   * Doc
   * Infra

Working Groups are formed by submitting a proposal via PR to the Technical
Steering Committee. The proposal should cover:

* what is the exact problem being worked on
* what is the exit criteria
* who are the chairs (up to 2)
* what are the meeting and discussion mechanics

## Repository Guidelines

All repositories under the MindSpore org:

* Must adopt the MindSpore [Code of Conduct](code-of-conduct_en.md).
* All code projects use the Apache 2.0 license. Documentation repositories must
use the Creative Commons License version 4.0.
* Must adopt the MindSpore CI bot
* Repository must be approved by the Technical Steering Committee

Repositories can be removed when they are inactive by archiving them.

## CLA

All Contributors must either sign the [MindSpore ICLA](https://www.mindspore.cn/icla),
or download and sign the [MindSpore CCLA](CCLA.pdf) and sent a scan
copy to <contact@mindspore.cn>. The Technical Steering Committee will update the
CLA to reflect the MindSpore organization/ownership as needed.
