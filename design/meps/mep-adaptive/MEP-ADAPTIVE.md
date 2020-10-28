| title        | authors              | owning-sig | participating-sigs | status      | creation-date | reviewers | approvers | stage | milestone     |
| ------------ | -------------------- | ---------- | ------------------ | ----------- | ------------- | --------- | --------- | ----- | ------------- |
| MEP-ADAPTIVE | @SunnyBeike | adaptivetraining   |        adaptivetraining            | provisional | 2020-10-27    |           | TBD       | beta  | beta : "v1.0" |

# MEP-ADAPTIVE: Adaptive Distributed Training System

## Table of Contents

<!-- toc -->

- [MEP-ADAPTIVE: Adaptive Distributed Training](#mep-adaptive)
  - [Table of Contents](#table-of-contents)
  - [Summary](#summary)
  - [Motivation](#motivation)
    - [Goals](#goals)
    - [Non-Goals](#non-goals)

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


Adaptive Distributed Training System aims to train the neural networks with elastic resources.

## Motivation

<!--
This section is for explicitly listing the motivation, goals and non-goals of
this MEP. Describe why the change is important and the benefits to users.
-->

Improving the resource utilization of a deep learning cluster is of paramount concern for many AI practioners. A promising approach is to use elastic deep learning systems. These systems allow users to dynamically change the number of training resources allocated to training jobs. Hence, practitioners can pack a large number of training jobs into a cluster, significantly improving cluster utilization.

Though promising, elastic deep learning systems are difficult to be deployed in practice. State of the art data-parallel elastic ddp learning systems couple the number of training resources with a critical learning hyper-parameter: the batch size of the SGD. Any scaling decisions made by the cluster scheduler therefore must alter the SGD batch size, which affects training results and can even make the training fail to converge.

### Goals

<!--
List the specific goals of the MEP. What is it trying to achieve? How will we
know that this has succeeded?
-->

In this project, we will enable the cluster scheduler to dynamically scale a training job without affecting its SGD batch size. To achieve this, we want to explore a novel method to decouple the SGD batch size and the number of training resources, so that the change of training resources does not affect the convergence.

### Non-Goals

<!--
What is out of scope for this MEP? Listing non-goals helps to focus discussion
and make progress.
-->
- None

