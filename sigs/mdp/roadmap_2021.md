Technical Roadmap for 2021
====

Probabilistic Programming Layer
----

Distribution:

- [D1] add support to multivariate continous distributions
- [D1.1] MultivariateNormal
- [D1.2] GumbelSoftmax
- [D1.3] Dirichlet

Expected time: Q3

Modeling Language:

- [M1] Based on the new support of MindSpore, extend the BayesianNet modeling capacity to general
- [M1.1] Implement with dictionaies
- [M1.2] Integrate StochasticTensor with Distribution

Expected time: Q1

- [M2] Hybrid BayesianNet + Bijector modeling language
- [M2.1] Implement a bijector API, and integrate it with the existing bijector in distributions
- [M2.2] Implement affine coupling layer
- [M2.3] Reimplement the existing Glow / VFlow in the test folder with the new API

Depends on: M1
Expected time: Q4

Inference algorithm:

- [I1] Support common black-box algorithms
- [I1.1] Importance sampling
- [I1.2] SGLD
- [I1.3] Reinforce
- [I1.4] HMC

Depends on: M1
Expected time: [I1.1]:Q1, [I1.2]:Q2, [I1.3]:Q3, [I1.4]:Q4

Model and Toolbox Layer
----

- [T1] Reimplement existing model and toolbox with the probabilistic programming layer
- [T1.1] Reimplement VAE
- [T1.2] Reimplement BNN
- [T1.3] Reimplement Uncertainty Estimation
- [T1.4] Reimplement Anormaly Detection

Depends on: M1
Expected time: Q2

- [T2] Implement more SOTA algorithms of toolbox
- [T2.1] BNN with SGLD for uncertainty estimation
  Depends on: M1, I1.2
  Expected time: Q2
- [T2.2] SWAG for uncertainty estimation
  Depends on: D1.1, M1
  Expected time: Q3

(Optional) Test uncertainty estimation on language modeling

Appliation
----

- [A1] Apply our tools to representative applications

Depends on: T2
Expected time: Q4

Miscellanous
----

Keep interacting with MindSpore to improve the coding style.

Expected Goal
----

Q1:

- A general BayesianNet framework, that supports modeling of arbitary Bayesian networks

Q2:

- Support representative inference algorithms in the general format
- Rewrite applications and examples with the new interface

Q3:

- Implement more distributions, inference algorithms
- Implement some SOTA algorithms for uncertainty estimation
- Should have a comparable version of TF ZhuSuan now

Q4:

- Modeling tools for flow bases
- Tentative applications of uncertainty estimation

