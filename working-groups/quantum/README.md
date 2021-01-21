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

Quantum computing is a disruptive approach to go beyond the capability of classical computers in the Post-Moore era. In 2019, quantum computational supremacy was experimentally demonstrated[1], meaning that the existing quantum chips can be used to perform certern tasks much faster than all classical computers. The next step is to find practical applications for these quantum chips, where machine learning is a natural choice. In fact, quantum machine learning is a fast-growing research area combining both quantum computation and classical machine learning, which can potentially achieve breakthroughs for both fields of research. The Quantum WG aims to foster a community for solving both classical and quantum problems by a collaboration in building a software framework for quantum machine learning.

## WG Leads

YUNG MANHONG (SUSTech)

## Motivation

Based on a variety of quantum properties, including coherence, superposition parallelism etc., quantum computers can achieve exponential speedups for many computational problems. In recent years, lots of important quantum-machine-learning algorithms have been invented, for example, HHL algorithm for solving linear equations [2], quantum principal component analysis (Q-PCA) [3], quantum support vector machine (Q-SVM) [4], quantum neural network (QNN) [5], etc. However, we are currently in the era of NISQ ( Noisy Intermediate-Scale Quantum ) [6], where the number of qubits and the accuracy of quantum gates are not good enough for implementing these quanutm algorithms. To overcome such challenge, we may consider the approach of variational quantum algorithm [7], which are expected to be capable of achieving quantum superiority in the NISQ stage.

MindSpore is a powerful deep learning framework which can provides user-friendly APIs, operator fusion and auto-paralleling capabilities, supporting CPU, Ascend and GPU backends. We can combine classical machine learning with quantum algorithms to build a quantum-classical hybrid architecture, allowing users to build their own QNNs conveniently. In addition, we can also use MindSpore to solve quantum problems with classic machine learning algorithms for the purpose of quantum control.

## Goals

The goals of this AI for Quantum Machine Learning WG are as follows:

- To design a user-friendly programming and API for the implementation of quantum neural network (QNN).

- To develop a high-performance quantum simulator that can support the simulation of quantum circuit wwith 50 or more qubits.

- To build a reinforcement learning framework for optimizing quantum control.

## Method

​We expect the applicant can conduct AI for Quantum Machine Learning research based on MindSpore, and hope to get your valuable suggestions to MindSpore in the process. We will do our best to improve the capabilities of the MindSpore framework and provide you with the most powerful technical support.

## How to Join

- Submit an issue/PR based on community discussion for consultation or claim on related topics.

- Submit your proposal to us by email yangkang22@huawei.com.

## References

[1] Arute F, Arya K, Babbush R, et al. Quantum supremacy using a programmable superconducting processor[J]. Nature, 2019, 574(7779): 505-510.

[2] Harrow A W, Hassidim A, Lloyd S. Quantum algorithm for linear systems of equations[J]. Physical review letters, 2009, 103(15): 150502.

[3] Lloyd S, Mohseni M, Rebentrost P. Quantum principal component analysis[J]. Nature Physics, 2014, 10(9): 631-633.

[4] Rebentrost P, Mohseni M, Lloyd S. Quantum support vector machine for big data classification[J]. Physical review letters, 2014, 113(13): 130503.

[5] Kak S C. Quantum neural computing[M]//Advances in imaging and electron physics. Elsevier, 1995, 94: 259-313.

[6] Preskill J. Quantum Computing in the NISQ era and beyond[J]. Quantum, 2018, 2: 79.

[7] Peruzzo A, McClean J, Shadbolt P, et al. A variational eigenvalue solver on a photonic quantum processor[J]. Nature communications, 2014, 5: 4213.
