
| title   | authors                          | owning-sig | participating-sigs | status      | creation-date | reviewers | approvers | stage | milestone     |
| ------- | -------------------------------- | ---------- | ------------------ | ----------- | ------------- | --------- | --------- | ----- | ------------- |
| MEP-mslite | @zhengli  @zhiqiangzhai @chaijun | mslite |  | provisional | 2020-08-18    |  | TBD       | beta  | beta : "v0.7" |

# MEP-mslite: MindSpore Lite

## Table of Contents

<!-- toc -->

- [MEP-mslite: MindSpore Lite](#mep-mindspore-lite)
  - [Table of Contents](#table-of-contents)
  - [Summary](#summary)
  - [Motivation](#motivation)
    - [Goals](#goals)
    - [Non-Goals](#non-goals)
  - [Proposal](#proposal)
    - [User Stories](#user-stories-optional)
      - [Generate a compact target model and low latency and low consumption runtime](#generate-a-compact-target-model-and-low-latency-and-low-consumption-runtime)
  - [Design Details](#design-details)
    - [Test Plan](#test-plan)
  - [Implementation History](#implementation-history)
  - [Drawbacks](#drawbacks)
  - [Alternatives](#alternatives)
  - [References](#references-optional)
  
  <!-- /toc -->
## Summary
MindSpore(MS) lite is an extremely light-weight deep learning inference framework, 
and designed for smart-phones and embedded devices, such as watches, headsets, and various IoT devices. 
It supports Android and iOS, as well as Harmony os, and has industry leading performance. 
                                
## Motivation
Since increased computing power and sensor data, intelligence is moving towards edge devices. 
Improved AI algorithms are driving the trend towards machine learning be run on 
the end device, such as smart-phones or automobiles, rather than in the cloud.
On-device AI can dramatically reduce latency, conserve bandwidth, 
improve privacy and enable smarter applications. 

### Goals
- Compatibility: supports MindSpore model, as well as mainstream third-party models, such as TensorFlow lite, Caffe 1.0 and ONNX.
- High-performance: 
generates small, low power consumption and fast inference target model for various hardware backends.

- Versatility: supports Harmony, Android and iOS os.
- Light-weight: small shared library size, should be less than 1 MB, and could be easily deployed on 
resource limited devices. 

### Non-Goals
- None

## Proposal

MS lite consists of converter and a runtime library.
The converter is an offline tool can handle most of the model translation work. 
The runtime library deploys to device and executes online, 
it has Lite RT and Lite Micro two modes.
Lite RT is for slightly resource limited devices, such as smart-phones, 
while Lite Micro is for extremely resource limited devices, such as watches, headsets. 

- Compatibility

    provides an abundant of operator parsers for MindSpore, Tensorflow Lite, Caffe, ONNX, 
    and supports common neural networks in CV and NLP, 208+ CPU operators, and 60+ GPU operators.
   
- High performance

    Many optimization methods, including graph optimizations, post training quantization,
    are applied to model in offline converter, and generated target model is more compact.
    Graph optimizations, such as operator fusion and constant folding, make model more compact.
    Post training quantization transfers fp32 model into fix-point int8 model. 
    It brings nearly 4x smaller model size, low latency and low consumption for inference process. 
        
    MS lite also applies a variety of optimization schemes to NN operations, including using Winograd 
algorithm in convolution and deconvolution, Strassen algorithm in matrix multiplication.
Operations support fp64, fp32, fp16 and int8, and are highly optimized with acceleration by 
neon instructions, hand-written assemble, multi-thread, memory reuse, heterogeneous computing, etc.

- Versatility   

    Supports Harmony, iOS and Android os, supports smart-phones, watches, headsets, and various IoT devices.
   
- Light weight

    MS lite is highly Optimized under GHLO and GLLO. It has small foot-print, 
    MS lite runtime is about 800 kB, and MS Micro is less than 200 KB. 
    It is flexible and can easily deploy to mobile and a variety of embedded devices.     
### User Stories

#### Generate a compact target model and low latency and low consumption runtime

Since devices has limited resource with few ROM, RAM, and power, how to deploy AI model to 
device is very challenge. MS lite aims to solve the challenge for users, and provides user-friendly, 
flexible tool to help users to make their own models more slim and more efficiency.
 
## Design Details

MS lite consists of converter and runtime. 
The converter is an offline tool has three parts, frontend, IR, and backend.
Runtime deploys to device and executes online.

- **Frontend.** Frontend aims to parse model from MindSpore, Tensorflow Lite, Caffe and ONNX in protobuf. 
- **IR.** IR is to define ANF, including tensor, operations, and graph.
- **Backend.** Backend is an optimizer based ANF graph, including GHLO, GLLO, and quantization.
               GHLO is short for "graph high level optimization", common optimization methods, 
               such as operators fusion, operator substitution, and constant folding, are included. 
               GLLO is short for "graph low level optimization", low level optimization methods 
               are related to hardware, such as layout adjustment, mixed-precision, etc.
                
- **Runtime.** Runtime has Lite RT and Lite Micro two modes.
  
  <img src="./ms-lite-arch.jpg" style="zoom:80%" div align=center/>


### Test Plan

MS lite employed pytests and nosetest to launch the testing process, 
and there are two types of testing strategies in MS lite:

- **Unit Test.** Every operation, optimization or pass in MS has its own unitest. 

- **System test**. The ms lite module has its own component testing. 
Basically we classify the testing into compilation verification, 
function verification and performance testing.

## Implementation History
- Support high and low level graph optimization.
- Support post training quantization.
- Support Arm CPU and Mali GPU. 
- Support fp64, fp32, fp16, int8 operations.

## Drawbacks
- MS lite does not support on-device training yet, it is coming soon...

## Alternatives
- MNN[1], TF lite[2] and TNN[3] are outstanding on-device AI frameworks. 
MS lite is for on-device AI, and MS cloud is for on-cloud AI, 
both of them are in scope of Huawei's MindSpore AI framework. 
They share same IR, and optimization passes. MS lite is more flexible. 

## References
- [1] https://github.com/alibaba/MNN 
- [2] https://www.tensorflow.org/lite
- [3] https://github.com/Tencent/TNN 
