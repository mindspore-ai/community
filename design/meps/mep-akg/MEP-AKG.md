| title   | authors                          | owning-sig | participating-sigs | status      | creation-date | reviewers | approvers | stage | milestone     |
| ------- | -------------------------------- | ---------- | ------------------ | ----------- | ------------- | --------- | --------- | ----- | ------------- |
| MEP-AKG | @anyrenwei  @ckey_dou @dylangeng | akg        |                    | provisional | 2020-06-16    |           | TBD       | beta  | beta : "v0.5" |

# MEP-AKG: Auto Kernel Generator

## Table of Contents

<!-- toc -->

- [MEP-AKG: Auto kernel Generator](#mep-akg-auto-kernel-generator)
  - [Table of Contents](#table-of-contents)
  - [Summary](#summary)
  - [Motivation](#motivation)
    - [Goals](#goals)
    - [Non-Goals](#non-goals)
  - [Proposal](#proposal)
    - [User Stories](#user-stories)
      - [Deep Graph Optimization](#deep-graph-optimization)
      - [Optimize Dynamic Neural Network](#optimize-dynamic-neural-network)
  - [Design Details](#design-details)
    - [Test Plan](#test-plan)
  - [Implementation History](#implementation-history)
  - [Drawbacks](#drawbacks)
  - [Alternatives](#alternatives)
  - [References](#references-optional)

  <!-- /toc -->

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

AKG is an optimizer for operators in Deep Learning Networks. It provides the ability to automatically fuse ops with specific patterns. AKG works with MindSpore-GraphKernel to improve the performance of networks running on different hardware backends

## Motivation

<!--
This section is for explicitly listing the motivation, goals and non-goals of
this MEP. Describe why the change is important and the benefits to users.
-->

Fusion can improve the performance of Deep Learning networks significantly. The fusion pattern varies in different networks, it may also change even in the same network when the hyperparameters change. So it's hard to ahead-of-time cover all the fused operators manually. GraphKernel analyzes the graph and find out the opportunities to fuse according to pre-designed patterns. AKG generates high-performance target code for these patterns on different hardware backends.

### Goals

<!--
List the specific goals of the MEP. What is it trying to achieve? How will we
know that this has succeeded?
-->

- Provide ability to fuse operators with specific patterns in resnet50 and bert.
- Provide ability to generate high-performance target code for these patterns automatically on different hardware backends.

### Non-Goals

<!--
What is out of scope for this MEP? Listing non-goals helps to focus discussion
and make progress.
-->
- None

## Proposal

<!--
This is where we get down to the specifics of what the proposal actually is.
This should have enough detail that reviewers can understand exactly what
you're proposing, but should not include things like API designs or
implementation. The "Design Details" section below is for the real
nitty-gritty.
-->

AKG aims to generate high-performance target code for fusing operators with specific patterns on different hardware backends. So three basic processes should be contained in akg as follows.
- **Operator Expression.**
  AKG defines several basic operators which can be used to compose a complicated fused operator. These basic operators have the same granularity with MindSpore's IR. We introduce json to expressed the relation of the basic operators in one fused operator which brings weak dependency between MindSpore and AKG.

- **Schedule initialize based on polyhedral.**

  When akg obtained the dsl of operators which would be fused, it would transform the operator dsl into formularIR(now we use HalidIR as tvm) and then into isl schedule tree. Next the polyhedral schedule process begin. With the help of pluto algorithm and other optimizations the schedule tree will do some transformations including vectorization, loop tiling, mem promotion and loop distribution, which can help us to improve the parallel capability and data locality.

- **Emit instructions on different hardware from IR.**

  In order to generate correctness and high-performance codes for different hardware, The IR should be optimized respectively, which consists of double buffer optimization, storage rewrite optimization and inject sync optimization.


### User Stories

<!--
Detail the things that people will be able to do if this MEP is implemented.
Include as much detail as possible so that people can understand the "how" of
the system. The goal here is to make this feel real for users without getting
bogged down.
-->

#### Deep Graph Optimization

Since the network is becoming more deeper and larger, there are more opportunity to fused different operation into one to optimize network performance.
AKG tools has the ability to auto-generate target code based on composited dsl, without scheduling procedure.
After automatic operator fusion and operator re-composition in graph level, AKG tools can generates high-performance target code for these composited pattern.

#### Optimize Dynamic Neural Network

Networks are exhibiting more and more dynamism, especially in the fields of deep graph analysis and NLP.
Tensors in a model may have dynamic shapes such as batch size, image size, sequence length, etc.
Models are expressed with control-flow, such as recursion, conditionals and loops.
Within these different dynamic requirement, AKG can generate one general target code on davinci hardware(different hardware) using for different shape of one common operator.

## Design Details

<!--
This section should contain enough information that the specifics of your
change are understandable. This may include API specs (though not always
required) or even code snippets. If there's any ambiguity about HOW your
proposal will be implemented, this is the place to discuss them.
-->

<!--![Image text](akg-design.png) {:height="75%" width="75%"} -->

AKG composes with four basic optimization module, normalization, auto schedule, instruction emit and backend optimization.
- **normalization.** The mainly optimization of normalization includes three address transform, common subexpression elimination, copy propagation and so on.
- **auto schedule.** The auto schedule module mainly have vectorization, loop tiling, mem promotion and loop distribution.
- **instruction emit.** The instruction emitting module has the optimization about loop normalization, auto pragma and emit instruction.
- **backend optimization.** The backend optimization module consists of double buffer optimization, storage rewrite optimization and inject sync optimization.

  <img src="akg-design.png" style="zoom:80%" div align=center/>

When GraphKernel is enabled, ops are reconstructed in the graph level. The new ops described in the format of json will be translated into DSL in AKG and then compiled to the target binary.

  <img src="https://images.gitee.com/uploads/images/2020/0618/093458_8e3a1221_6569326.png" style="zoom:80%" div align=center />


<!-- ![输入图片说明](https://images.gitee.com/uploads/images/2020/0618/093458_8e3a1221_6569326.png "屏幕截图.png") -->


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

AKG employed pytests and nosetest to launch the testing process, and there are three types of testing strategies in AKG:

- **Unit Test.** Every optimization or pass in AKG has its own unitest.

- **System test**. The akg module has its own component testing. Basically we classify the testing into compilation verification, function verification and performance testing.

- **Integration test or API test**. Akg provides certain number of APIs to MindSpore-GraphKernel. So in the integration test process we have to make sure the fusion of patterns meets the requirements from both correctness and performance.

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

- Support auto scheduling and auto tuning
- Support auto pragma optimization and alignment optimization and auto emitinsn
- Support auto tiling optimization
- Support To ThreeAddr and CSE optimization for auto-diff
- Support dynamic shape for resnet inference
- Enhance fused operator performance for Deep Graph Optimization

## Drawbacks

<!--
Why should this MEP _not_ be implemented?
-->
- The schedule generated directly by pluto algorithm during the polyhedral process would exist some issues on both correctness and performance in some scenarios. So some extra passes have to added before emitting instructions.

## Alternatives

<!--
What other approaches did you consider and why did you rule them out? These do
not need to be as detailed as the proposal, but should include enough
information to express the idea and why it was not acceptable.
-->
- Both TVM[1] and TC[2] are outstanding tools which can automatically synthesize high-performance machine learning kernel. However, neither of them could generate codes for Davinci cores(cce codes) as davinci cores have more complicated multi-level memory design(L0-A/B/C, L1 and UB) as well as specific dataflow constraint. Besides, TVM adopted schedule space model and had to write the schedule all by ourselves while akg used polyhedral techniques to initialize the schedule automatically, which referenced from the designing of TC.

## References
- [1] https://github.com/apache/incubator-tvm
- [2] https://github.com/facebookresearch/TensorComprehensions
