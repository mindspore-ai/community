| title | authors | owning-sig | participating-sigs | status | creation-date | reviewers | approvers | stage | milestone |
| ----- | ------- | ---------- | ------------------ | ------ | ------------- |---------- | --------- | ----- | --------- |
| MEP-QUANTUM | @donghufeng, @kangyangzc  | wg-quantum | sig-parallel | provisional | 2021-01-19 | TBD | TBD | NA | "v1.0" |

# MEP-QUANTUM: MindSpore QUANTUM

## Table of Contents

<!-- toc -->

- [Summary](#summary)
- [Motivation](#motivation)
    - [Goals](#goals)
    - [Non-Goals](#non-goals)
- [Proposal](#proposal)
    - [User Stories](#user-stories)
- [References](#references)

<!-- /toc -->

## Summary

Quantum computing is an important approach to improve the ability of information processing on Post-Moore era, and the quantum supremacy has been demonstrated in recent works[1, 2]. Quantum machine learning is a research areas that combine both quantum computing and classical machine learning, which demonstrates significant influence on healthcare, energy, new material, financial, logistics and transportation. The Quantum WG aims to develop a community collaboration for solving both classic and quantum problems with hybrid quantum-classical machine learning framework.

## Motivation

Thanks to quantum coherence, quantum superposition principle and quantum parallelism, quantum computers can exponentially accelerate the calculation for some specific problems. Commonly used quantum machine learning algorithms include HHL algorithm for solving linear equations [3], quantum principal component analysis (Q-PCA) [4], quantum support vector machine (Q-SVM) [5], quantum neural network (QNN) [6], etc. However, at the stage of NISQ ( Noisy Intermediate-Scale Quantum ) [7], the number of bits and operation accuracy of quantum computers are not enough to implement these algorithms. Through the variational quantum algorithm [8], QNN shows robustness to noise, which are expected to achieve quantum superiority in the NISQ stage. MindSpore is a powerful deep learning framework which can provides user-friendly API, operator fusion and auto-paralleling capabilities, supporting CPU, Ascend and GPU backend. We can combine classical machine learning with quantum algorithms to build a quantum-classical hybrid architecture, allowing users to build their own QNNs conveniently. In addition, we can also use MindSpore to solve quantum problems with classic machine learning algorithms such as quantum control.

### Goals

The goals of this project are as follows:

- To design a user-friendly programming and API for the implementation of QNN.

- To develop a high-performance system with large qubit quantum simulator operator to simulate the quantum circuit.

- To build a reinforcement learning framework to do quantum control.

### Non-Goals

- None.

## Proposal

To address the limitations of existing quantum machine learning framework, proposals and contributions on the following aspects are welcomed.

- **Friendly programming API.** The MindSpore quantum is supposed to compatible with MindSpore deep learning framework. The developers can naturally use the existing operators and optimizers in MindSpore to train hybrid quantum-classical neural network.

- **Rich library of quantum models.** Based on the current quantum neural network framework, more quantum models are welcomed to developed, such as quantum convolutional neural network and quantum graph neural network.

- **High performance simulation backend.** With the increase of quantum qubits, the quantum state we need to handle increase exponentially, as well as the simulation process. To increase our simulation performance, more backends should be implemented, such as Ascend and GPU. Moreover, tensor network is also an approach to simulate quantum circuit with less time consuming.

### User Stories

Quantum neural network can be described by quantum circuit model. A quantum circuit is composed of quantum qubits, quantum gates and measurements. The quantum qubits are implemented by different quantum systems, such as Josephson junction, trapped ion, NV center, etc. For a $n$ qubits quantum system, the quantum state lives in a $2^n$ dimension Hilbert space. The quantum gate is quantum operator that acts on quantum qubits. Basically, there are two different kinds of quantum gates, non-parameterized gate and parameterized gate. The Pauli gate $X, Y, Z$, hadamard gate $H$ and CNot gate are commonly used non-parameterized gate. The parameterized gates are trainable gate in quantum circuit. Rotation-X gate $\text{Rx}(\theta)$ is one of them, for example, and we can adjust the rotation angle $\theta$ by the expectation value of measurements. The measurements applied on the end of quantum circuit will return the probability of the quantum state collapsed on certain bit strings.

Figure 1[9] shows a basic structure of parameterized quantum circuit operator in MindSpore. Here we have 8 quantum qubits, and the measurement is applied on the first qubit. The whole quantum circuit is construct by a encoding circuit $U(\rho_{\text{in}})$, which will prepare the quantum system in certain initial state, and a ansatz circuit combined by CNOT gate and Rotation gate, with rotation angle can be trained by MindSpore.

<img src="./TT_QNN.png" style="zoom:30%" div align=center/>

By specially designing the QNN, one can feed data into this layer with the encoding circuit and train the ansatz with optimizers, or connect the QNN layer with a classic neural network, as shown in figure 2. The forward and backward propagation of QNN are automatically implement in the MindSpore pipelines. Since the quantum gates can be represented by unitary matrices, the QNN will naturally be an invertible neural network, which dramatically reduced the calculation time of gradient.

<img src="./MindQuantum-architecture.png" style="zoom:30%" div align=center/>

### References

[1] Arute F, Arya K, Babbush R, et al. Quantum supremacy using a programmable superconducting processor[J]. Nature, 2019, 574(7779): 505-510.

[2] Zhong H S, Wang H, Deng Y H, et al. Quantum computational advantage using photons[J]. Science, 2020, 370(6523): 1460-1463.

[3] Harrow A W, Hassidim A, Lloyd S. Quantum algorithm for linear systems of equations[J]. Physical review letters, 2009, 103(15): 150502.

[4] Lloyd S, Mohseni M, Rebentrost P. Quantum principal component analysis[J]. Nature Physics, 2014, 10(9): 631-633.

[5] Rebentrost P, Mohseni M, Lloyd S. Quantum support vector machine for big data classification[J]. Physical review letters, 2014, 113(13): 130503.

[6] Kak S C. Quantum neural computing[M]//Advances in imaging and electron physics. Elsevier, 1995, 94: 259-313.

[7] Preskill J. Quantum Computing in the NISQ era and beyond[J]. Quantum, 2018, 2: 79.

[8] Peruzzo A, McClean J, Shadbolt P, et al. A variational eigenvalue solver on a photonic quantum processor[J]. Nature communications, 2014, 5: 4213.

[9] Zhang K, Hsieh M H, Liu L, et al. Toward trainability of quantum neural networks[J]. arXiv preprint arXiv:2011.06258, 2020.
