# Joint Research on Future AI Topics

## Table of Contents
<!-- toc -->
- [Summary](#summary)
- [Motivation](#motivation)
- [Goals](#goals)
- [Method](#method)
- [How to join](#how-to-join)
<!-- /toc -->

## Summary

MindSpore cooperates with universities to research on future AI topics and jointly cultivate future AI talents.There are 10 topics in total:

- Low-bit Neural Networks Training

- Memory Optimization

- Model Innovation

- AI for Scientific Computing

- Verifiable/certifiable Trustworthy AI

- Confidential AI Computing

- Tensor Differentiable Computing Framework

- Distributed And Parallel AI Computing Framework

- XAI in line with human cognitive

- Automatic model optimization recommendation

## Motivation

- Low-bit Neural Networks Training

    ​At present, mixed precision can automatically adjust the accuracy of fp16 and fp32 for the network to improve training performance and memory optimization. Because operators have different costs on different AI chips, all optimization strategies for different AI chips are different. The network configuration of different hardware is different, so how to automatically generate the precision adjustment strategy that adapts to various hardware, especially the low bit strategy has become a difficult problem.

- Memory Optimization

    ​There are many strategies for memory optimization, such as recalculation and host-device memory switching. These strategies further break through the memory bottleneck by increasing the amount of calculation and increase the batchsize. Increasing batchsize can often improve the utilization of GPU and NPU to improve throughput performance.

- Model Innovation

    (1) Model innovation combining traditional models and neural networks is a research hotspot.

    (2) Deep probability model innovation: through the combination of neural network and probability model, the model can better help decision-making.

    (3) Graph neural network: The neural network is combined with the traditional graph structure, oriented to cognitive reasoning and future trends.

- AI for Scientific Computing

    (1) AI modeling: AI automatic modeling can effectively improve modeling efficiency of scientific calculations, and convergence analysis can improve model reliability and ensure simple and safe use by users.

    (2) AI solution: The calculation amount of high-order differential increases exponentially with the parameter and the order. We can design neural network models to solve such classic problems.

- Verifiable/certifiable Trustworthy AI

    (1) Many aspects of trustworthy AI (or responsible AI), such as adversarial robustness, backdoor, fairness, privacy protection capabilities, and accountability, have gradually attracted the attention of the industry and academia.

    (2) Current study on trustworthy AI are mostly empirical, and there are few theoretical studies. The verifiable and certifiable trustworthy AI, especially its training, evaluation and test methods, and its underlying insight related with explainable AI, requires theoretical guidance.

- Confidential AI Computing

    (1) In the training and deployment process of AI services, several vital resources such as data, models, and computing resources may belong to different parties. A large amount of data will move across trust domains. The problems of data privacy protection and model confidentiality protection are prominent.

    (2) Confidential computing is an important direction to protect the confidentiality of key data. At present, confidential computing based on trusted execution environment has performance advantages, but its trust model is limited; confidential computing based on cryptography has simple trust model, but there is still a gap between performance and practicality.

    (3) A series of specialized optimizations may improve the performance of confidential computing in AI scenarios, including but not limited to: cryptography suitable for AI, specialized intermediate representation and compiling strategy, and hardware-based acceleration.

- Tensor Differentiable Computing Framework

    (1) The new network model poses challenges to the IR expression, optimization and execution of the deep learning framework, including the introduction of a new op abstraction level, and the dynamics of the model.

    (2) The acceleration of third-party high-performance computing languages ​​or frameworks urgently requires a more versatile and open tensor computing framework and API design.

    (3) The technical challenges of unified optimization of the model layer and the operator layer, including hierarchical IR design, optimization of infrastructure, automatic tuning, loop optimization, etc.

    (4) Differential equations are solved with a large number of differentials, which have high requirements for the differential expression of the framework, interface design, algorithm analysis efficiency and reliability.

- Distributed And Parallel AI Computing Framework

    (1) The scale and complexity of models are getting higher and higher, such as GPT-3 with 175 billion parameters, millions of face recognition, and tens of billions of feature recommendations.

    (2) It is difficult to split the model manually. For example, developers need to combine information such as calculation amount, cluster size, communication bandwidth, and network topology to construct a parallel mode.

    (3) The expression of the parallel mode lacks adaptability, and the simple graph-level model segmentation cannot obtain high-efficiency speedup. It requires the decoupling of algorithm logic and parallel logic.

- XAI in line with human cognitive

    (1) The current deep learning model is essentially black box due to its technical complexity , which leads to the opacity and inexplicability of AI services and further restricts the commercial application and promotion of AI services. Existing explainable AI technology mainly focuses on how to provide limited engineering auxiliary information to the model, but ignores the understanding of AI models from the perspective of human cognition.

    (2) Humans usually understand things through analogies, metaphors, induction and other cognitive methods, and have a certain process of mental cognition construction. Thus, in this project, we expect to be able to explore more systematic and explainable AI methods that conform to human cognition, including interactive interfaces, explainable methods, measurement methods, and so on.

- Automatic model optimization recommendation

    (1) Nowadays, training a high accuracy and high performance model often requires rich expert knowledge and repeated iterative attempts. AutoML makes it easier to apply and reduce the demand for experienced human experts, however, there are still some difficulties in setting search space which lead to large search spaces and long training time. If we can combine the iterative history of user training and analyze historical training data, a lite hyper-parameter recommendation method can be realized, which can greatly improve the developer experience.

    (2) Meanwhile, there are similar problems for model performance tuning, In different heterogeneous hardware, models, and data processing scenarios, expert knowledge is also required. Therefore, we aim to reduce the performance tuning threshold by automatically identifying system performance bottlenecks and recommending the best code path.
​

## Goals

- Low-bit Neural Networks Training

    ​Self-adaptively provides a low-bit precision training mechanism for various networks.

    ![target](./target.png)

- Memory Optimization

    Adaptive search memory optimization strategy to find the best balance between recalculation overhead and memory optimization benefits, so as to optimize the overall network performance.

    ![memory_opt](./memory_opt.png)

- Model Innovation

    (1) Complete probability sampling library and probability inference (learning the probability distribution of the overall sample through known samples) algorithm library.

    (2) Design new algorithms for dynamically changing heterogeneous graphs (different feature dimensions and different information aggregation methods)

    (3) Trillion distributed graph data storage, segmentation and sampling

- AI for Scientific Computing

    (1) AI modeling：Construct a neural network, training data and loss function for scientific computing problems.

    (2) AI solution：AI model solves differential equations, solves optimization problems,  achieve the goal that the amount of high-order automatic differential calculation increases linearly with the order.

- Verifiable/certifiable Trustworthy AI

    ​Propose research on mechanism and evaluation system of verifiable or certifiable trustworthy AI.

- Confidential AI Computing

    Realize an Confidential AI Computing framework, or its key technologies,  with feasible, flexible and efficient performance in actual AI application scenarios.

- Tensor Differentiable Computing Framework

    ​Driven by cutting-edge applications, from the perspectives of new models, dynamic models, high-performance computing languages, etc., study the evolution direction and key technology paths of future computing frameworks. For example, it supports differentiable programming of high-order differentiation.

- Distributed And Parallel AI Computing Framework

    ​Driven by super-large models, research key technologies for accelerating distributed training, including but not limited to automatic parallelism, hybrid parallelism, memory optimization, and elastic scaling. Such as achieving heterogeneous automatic parallel efficiency and linear speedup.

- XAI in line with human cognitive

    A complete set of explainable AI methods and strategies in line with human cognition, providing necessary interactive cognitive interface design solutions for different scenarios and different cognitions, and a case study for typical scenarios.

- Automatic model optimization recommendation

    This feature automatically recommends optimized hyper-parameter configurations and performance optimization paths, reducing the threshold for model development and use and improving the model debugging and optimization efficiency.


## Method:

​We expect the applicant can conduct the above research based on MindSpore, and hope to get your valuable suggestions to MindSpore in the process. We will do our best to improve the capabilities of the MindSpore framework and  provide you with the most powerful technical support.


## How To Join：
* Submit an issue/PR based on community discussion for consultation or claim on related topics

* Submit your proposal to us by email <wang1@huawei.com>
