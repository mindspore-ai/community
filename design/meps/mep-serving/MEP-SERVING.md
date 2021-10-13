<!--
**Note:** When your MEP is complete, all of these comment blocks should be removed.

**Note:** Any PRs to move a MEP to `implementable` or significant changes once
it is marked `implementable` must be approved by each of the MEP approvers.
If any of those approvers is no longer appropriate than changes to that list
should be approved by the remaining approvers and/or the owning SIG.
-->
| title | authors | owning-sig | participating-sigs | status | creation-date | reviewers | approvers | stage | milestone |
| ----- | ------- | ---------- | ------------------ | ------ | ------------- |---------- | --------- | ----- | --------- |
| MindSpore Serving | xuyongfei | serving | serving | provisional/implementable/implemented/deferred/rejected/withdrawn/replaced | 2020-11-16 | xuyongfei/zhangyinxia | xuyongfei/zhangyinxia | beta | beta: "v0.6" |

# MEP-SERVING: Serving

## Table of Contents

<!-- TOC -->

- [MEP-SERVING: Serving](#mep-serving-serving)
    - [Table of Contents](#table-of-contents)
    - [Summary](#summary)
    - [Motivation](#motivation)
        - [Goals](#goals)
        - [Non-Goals](#non-goals)
    - [Proposal](#proposal)
        - [User Stories (optional)](#user-stories-optional)
            - [Story 1](#story-1)
            - [Story 2](#story-2)
        - [Notes/Constraints/Caveats (optional)](#notesconstraintscaveats-optional)
        - [Risks and Mitigations](#risks-and-mitigations)
    - [Design Details](#design-details)
        - [Test Plan](#test-plan)
        - [Graduation Criteria](#graduation-criteria)
            - [Alpha -> Beta Graduation](#alpha---beta-graduation)
            - [Beta -> Stable Graduation](#beta---stable-graduation)
        - [Upgrade / Downgrade Strategy](#upgrade--downgrade-strategy)
    - [Implementation History](#implementation-history)
    - [Drawbacks](#drawbacks)
    - [Alternatives](#alternatives)
    - [Infrastructure Needed (optional)](#infrastructure-needed-optional)
    - [References (optional)](#references-optional)

<!-- /TOC -->

## Summary

<!--
This section is incredibly important for producing high quality user-focused
documentation such as release notes or a development roadmap.  It should be
possible to collect this information before implementation begins in order to
avoid requiring implementors to split their attention between writing release
notes and implementing the feature itself.  MEP editors, SIG Docs, and SIG PM
should help to ensure that the tone and content of the `Summary` section is
useful for a wide audience.

A good summary is probably at least a paragraph in length.

Both in this section and below, follow the guidelines of the [documentation
style guide]. In particular, wrap lines to a reasonable length, to make it
easier for reviewers to cite specific portions, and to minimize diff churn on
updates.

[documentation style guide]: https://gitee.com/mindspore/docs/blob/master/CONTRIBUTING_DOC.md
-->

MindSpore Serving is a lightweight and high-performance service module that helps MindSpore developers efficiently deploy online inference services in the production environment. After completing model training using MindSpore, you can export the MindSpore model and use MindSpore Serving to create an inference service for the model. Currently, only Ascend 910 is supported.

## Motivation

<!--
This section is for explicitly listing the motivation, goals and non-goals of
this MEP. Describe why the change is important and the benefits to users.
-->

1. MindSpore and Serving header files are interdependent.
2. ACL related code is managed in Serving.
3. Enabling different port services requires recompilation.

### Goals

<!--
List the specific goals of the MEP. What is it trying to achieve? How will we
know that this has succeeded?
-->

1. Decoupling of MindSpore and Serving.
2. Serving no longer distinguishes the backend.
3. Serving can provide more flexible interface calls.

### Non-Goals

<!--
What is out of scope for this MEP? Listing non-goals helps to focus discussion
and make progress.
-->

NA

## Proposal

<!--
This is where we get down to the specifics of what the proposal actually is.
This should have enough detail that reviewers can understand exactly what
you're proposing, but should not include things like API designs or
implementation. The "Design Details" section below is for the real
nitty-gritty.
-->

1. Adjust and enhance the external interface: grpc + restful.
2. Single model concurrent, give full play to chip capability.
3. The model implements two forms of batch.
4. Support data pre-processing and post-processing sink to the service back-end.
5. Support multiple models.

### User Stories (optional)

<!--
Detail the things that people will be able to do if this MEP is implemented.
Include as much detail as possible so that people can understand the "how" of
the system. The goal here is to make this feel real for users without getting
bogged down.
-->

NA

#### Story 1

NA

#### Story 2

NA

### Notes/Constraints/Caveats (optional)

<!--
What are the caveats to the proposal?
What are some important details that didn't come across above.
Go in to as much detail as necessary here.
This might be a good place to talk about core concepts and how they relate.
-->

NA

### Risks and Mitigations

<!--
What are the risks of this proposal and how do we mitigate. Think broadly.
For example, consider both security and how this will impact the larger
MindSpore ecosystem.
How will security be reviewed and by whom?
How will UX be reviewed and by whom?
Consider including folks that also work outside the SIG or subproject.
-->

NA

## Design Details

<!--
This section should contain enough information that the specifics of your
change are understandable. This may include API specs (though not always
required) or even code snippets. If there's any ambiguity about HOW your
proposal will be implemented, this is the place to discuss them.
-->

1. RESTful

    ```bash
    POST http://${HOST_IP}:${PORT_NUM}/model/${MODEL_NAME}[/version/${VERSION}]:${METHOD_NAME}
    ```

2. instances format

    ```json
    {
      "instances":[
          {
            "tagx": "foo",
            "signalx": [1,2,3,4,5],
            "sensorx": [[1,2], [3,4]]
          },
          {
            "tagx": {"b64": "bytes_data_base64_code"},
            "signalx": 3,
            "sensorx": [[4,5], [6,8], [4,5], [6,8]]
          }
      ]
    }
    ```

3. replay

    ```json
    {
      "instances":[
          {
            "label": "new"
          },
          {
            "tagx": {"b64": "bytes_data_base64_code"},
            "signalx": 3,
            "sensorx": [[4,5], [6,8], [4,5], [6,8]]
          }
      ]
    }
    ```

### Test Plan

<!--
**Note:** *Not required until targeted at a release.*

Consider the following in developing a test plan for this enhancement:

- Will there be e2e and integration tests, in addition to unit tests?
- How will it be tested in isolation vs with other components?

No need to outline all of the test cases, just the general strategy. Anything
that would count as tricky in the implementation and anything particularly
challenging to test should be called out.

All code is expected to have adequate tests (eventually with coverage
expectations). Please adhere to the [MindSpore contributing guidelines][contributing-guidelines]
when drafting this test plan.

[contributing-guidelines]: https://gitee.com/mindspore/mindspore/blob/master/CONTRIBUTING.md
-->

1.ut

2.st

### Graduation Criteria

<!--
**Note:** *Not required until targeted at a release.*

Define graduation milestones.

These may be defined in terms of API maturity, or as something else. The MEP
should keep this high-level with a focus on what signals will be looked at to
determine graduation.

Consider the following in developing the graduation criteria for this enhancement:

- Maturity levels (`alpha`, `beta`, `stable`)
- Deprecation policy (TBD)

Clearly define what graduation means by either linking to the [API doc definition](https://www.mindspore.cn/docs/api/en/master/index.html), or by redefining what graduation means.

In general, we try to use the same stages (alpha, beta, stable), regardless how the
functionality is accessed.

Below are some examples to consider, in addition to the aforementioned maturity levels.

#### Alpha -> Beta Graduation

- Gather feedback from developers and surveys
- Complete features A, B, C
- Tests are in Testgrid and linked in MEP

#### Beta -> Stable Graduation

- N examples of real world usage
- N installs
- More rigorous forms of testing e.g., downgrade tests and scalability tests
- Allowing time for feedback

**Note:** Generally we also wait at least 2 releases between beta and
GA/stable, since there's no opportunity for user feedback, or even bug reports,
in back-to-back releases.
-->

NA

### Upgrade / Downgrade Strategy

<!--
If applicable, how will the component be upgraded and downgraded? Make sure
this is in the test plan.

Consider the following in developing an upgrade/downgrade strategy for this
enhancement:

- What changes (in invocations, configurations, API use, etc.) is an existing
  cluster required to make on upgrade in order to keep previous behavior?
- What changes (in invocations, configurations, API use, etc.) is an existing
  cluster required to make on upgrade in order to make use of the enhancement?
-->

NA

## Implementation History

<!--
Major milestones in the life cycle of a MEP should be tracked in this section.
Major milestones might include

- the `Summary` and `Motivation` sections being merged signaling SIG acceptance
- the `Proposal` section being merged signaling agreement on a proposed design
- the date implementation started
- the first MindSpore release where an initial version of the MEP was available
- the version of MindSpore where the MEP graduated to general availability
- when the MEP was retired or superseded

-->

NA

## Drawbacks

<!--
Why should this MEP _not_ be implemented?
-->

NA

## Alternatives

<!--
What other approaches did you consider and why did you rule them out? These do
not need to be as detailed as the proposal, but should include enough
information to express the idea and why it was not acceptable.
-->

NA

## Infrastructure Needed (optional)

<!--
Use this section if you need things from the project/SIG. Examples include a
new subproject, repos requested, github details. Listing these here allows a
SIG to get the process for these resources started right away.
-->

NA

## References (optional)

<!--
Listing some dependencies of `project` and `website` links mentioned in the
sections above if required.
-->

NA
