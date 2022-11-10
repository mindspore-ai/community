# Summary

Explainable AI (also termed transparent AI) is a form of artificial intelligence whose behavior is easily understood by humans. Unlike a "black box" in machine learning, in which the creators of an AI cannot explain how a specific decision was made, it implies the "explainability" of the algorithm's operation. The MindSpore XAI SIG is an initiative designed to build a collaborative environment for innovative research and industrial applications in XAI.

## Motivation

Theoretical flaws in machine learning decision-making mechanisms
Due to data samples' general limitations and biases, this association learning will inevitably learn a spurious relationship. A model based on this as a decision-making basis may perform well on most test data, but in fact, the reasoning and decision-making ability based on correct causality has not been learned, and its performance will be greatly reduced when faced with new data with distribution shift from the training samples.

## Application pitfalls of machine learning

First, due to the limitations and biases of data sample collection, data-driven AI systems are also biased, tantamount to bias in human society. Entrusting the future and destiny of individuals to such a biased artificial intelligence system damages social justice and causes contradictions among social groups.
Secondly, the "black box" deep neural network often makes low-level mistakes humans do not make, leading to potential security risks.
Lastly, and most importantly, from the point of view of the decision-making mechanism, the current analysis of deep learning algorithms is still in an opaque exploratory stage. Especially for super-large-scale pre-trained neural networks with hundreds of millions of parameters, such as BERT[1], GPT3[2], etc., the decision-making process is still not clearly explained academically. Such "black box" deep neural networks cannot be fully understood and trusted by humans for the time being, and the potential risks of large-scale application of such pre-trained models cannot be ignored.
Traditional AI systems fail to meet regulatory requirements in major fields such as finance, medical care, and law, legislation on the prevention and supervision of the application risks of artificial intelligence systems has been gradually strengthened and implemented.

## Goals

The goals of this SIG are as follows:

1. To develop novel solutions to basic scientific problems such as poor robustness, poor interpretability, and strong dependence on data of artificial intelligence methods represented by deep learning;

2. To improve the state-of-the-art XAI solutions, such as perturbation, counterfactual, and explainable GNN;

3. To explore the basic principles of machine learning, develop explainable and general-purpose next-generation artificial intelligence methods;

4. To promote the innovative application of explainable artificial intelligence methods in the scientific/industrial fields;

5. To promote academic activities, including academic workshops, conferences, and contests;

6. To contribute to open-source software for XAI based on MindSpore

## SIG members

PolyU:

Prof. LI Qing qing-prof.li@polyu.edu.hk lead

Dr. ZHANG Chen jason-c.zhang@polyu.edu.hk  co-lead

Dr. LIN Wanyu wan-yu.lin@polyu.edu.hk approver

Dr. FAN Wenqi wenqi.fan@polyu.edu.hk approver

Dr. ZHOU Kai kai.zhou@polyu.edu.hk approver

Huawei:

Dr. CAO Chen caleb.cao@huawei.com approver

Dr. WANG Lunning wangluning2@huawei.com approver

Dr. Yang Yujie yuanyujie@huawei.com approver

Dr. Huang Yongxiang huang.yongxiang2@huawei.com coordinator and contactor

HKUST:

Prof. CHEN Lei leichen@cse.ust.hk co-lead
