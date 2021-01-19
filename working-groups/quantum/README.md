# MindSpore AI for Quantum Machine Learning Working Group (WG)

<!-- TOC -->

- [MindSpore AI for Quantum Machine Learning Working Group (WG)](#mindspore-ai-for-quantum-working-group-wg)
    - [Summary](#summary)
    - [WG Leads](#wg-leads)
    - [Motivation](#motivation)
    - [Goals](#goals)
    - [Method](#method)
    - [How to Join](#how-to-join)

<!-- /TOC -->

## Summary

Quantum computing is an important approach to improve the ability of information processing on Post-Moore era, and the quantum supremacy has been demonstrated in recent works[1, 2]. Quantum machine learning is a research areas that combine both quantum computing and classical machine learning, which demonstrates significant influence on healthcare, energy, new material, financial, logistics and transportation. The Quantum WG aims to develop a community collaboration for solving both classic and quantum problems with hybrid quantum-classical machine learning framework.

## WG Leads

YUNG MANHONG (SUSTech)

## Motivation

Thanks to quantum coherence, quantum superposition principle and quantum parallelism, quantum computers can exponentially accelerate the calculation for some specific problems. Commonly used quantum machine learning algorithms include HHL algorithm for solving linear equations [3], quantum principal component analysis (Q-PCA) [4], quantum support vector machine (Q-SVM) [5], quantum neural network (QNN) [6], etc. However, at the stage of NISQ ( Noisy Intermediate-Scale Quantum ) [7], the number of bits and operation accuracy of quantum computers are not enough to implement these algorithms. Through the variational quantum algorithm [8], QNN shows robustness to noise, which are expected to achieve quantum superiority in the NISQ stage. MindSpore is a powerful deep learning framework which can provides user-friendly API, operator fusion and auto-paralleling capabilities, supporting CPU, Ascend and GPU backend. We can combine classical machine learning with quantum algorithms to build a quantum-classical hybrid architecture, allowing users to build their own QNNs conveniently. In addition, we can also use MindSpore to solve quantum problems with classic machine learning algorithms such as quantum control.

## Goals

The goals of the AI for Quantum Machine Learning WG are as follows:

- To design a user-friendly programming model and API for the implementation of quantum neural network.

- To develop a high-performance system with large qubit quantum simulator operator to simulate the quantum circuit.

- To build a reinforcement learning framework to do quantum control.

## Method

​We expect the applicant can conduct AI for Quantum Machine Learning research based on MindSpore, and hope to get your valuable suggestions to MindSpore in the process. We will do our best to improve the capabilities of the MindSpore framework and provide you with the most powerful technical support.

## How to Join

- Submit an issue/PR based on community discussion for consultation or claim on related topics.

- Submit your proposal to us by email yangkang22@huawei.com.

## References

[1] Arute F, Arya K, Babbush R, et al. Quantum supremacy using a programmable superconducting processor[J]. Nature, 2019, 574(7779): 505-510.

[2] Zhong H S, Wang H, Deng Y H, et al. Quantum computational advantage using photons[J]. Science, 2020, 370(6523): 1460-1463.

[3] Harrow A W, Hassidim A, Lloyd S. Quantum algorithm for linear systems of equations[J]. Physical review letters, 2009, 103(15): 150502.

[4] Lloyd S, Mohseni M, Rebentrost P. Quantum principal component analysis[J]. Nature Physics, 2014, 10(9): 631-633.

[5] Rebentrost P, Mohseni M, Lloyd S. Quantum support vector machine for big data classification[J]. Physical review letters, 2014, 113(13): 130503.

[6] Kak S C. Quantum neural computing[M]//Advances in imaging and electron physics. Elsevier, 1995, 94: 259-313.

[7] Preskill J. Quantum Computing in the NISQ era and beyond[J]. Quantum, 2018, 2: 79.

[8] Peruzzo A, McClean J, Shadbolt P, et al. A variational eigenvalue solver on a photonic quantum processor[J]. Nature communications, 2014, 5: 4213.
