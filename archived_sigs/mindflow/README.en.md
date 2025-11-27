# Join MindSpore MindFlow SIG to help AI fluid simulation development

🔥🔥🔥 [Open Source Internship Tasks](https://gitee.com/mindspore/community/issues/I55B5A?from=project-issue)

🔥🔥🔥 [MindSpore Flow Repo](https://gitee.com/mindspore/mindscience/tree/master/MindFlow)

## 1.Establishment background

Computational fluid dynamics is closely related to the research and development of aerospace, marine equipment, energy, and power.    However, it still faces challenges and bottlenecks from mesh generation complexity.   Automatic mesh generation sometimes can not cope with complex boundary geometry.    Manual processing is necessary.  The simulation of fluid mechanics relies on complex iterative computation, which is limited by parallel efficiency.  Moreover, it is difficult to solve high-dimensional equations. Accuracy and performance need to be balanced.

These challenges also bring new opportunities for AI scientific computation.    With its parallel training and inferring ability, AI does not rely on grids.    It can quickly obtain results without iterative calculation.      AI has the ability to learn intrinsic laws from the physical world and to obtain results with high accuracy and performance.      In recent years, Google, Nvidia, and other major institutions have begun to apply AI to fluid mechanics research.   These works have received widespread attention.

Different from the mature deep learning kits of CV and NLP, there is still not a stable and easy-to-use model library or community in the field of AI fluid mechanics, which enables researchers to examine algorithms conveniently and develop models efficiently.

Therefore, building an open, easy-to-use, and efficient AI+ fluid mechanics library and community is conducive to the prosperity of fluid mechanics research and the wide application and innovation of AI.

In these circumstances, the MindFlow Special Interest Group ("MindFlow SIG") of Shengsi was formally established. SIG welcomes all like-minded partners from open-source communities.

## 2.Brief introduction

Focused on Shengsi MindFlow, in order to make full use of the advantages of MindSpore, improve the capabilities of kits and expand the community ecology, SIG provides an efficient and easy-to-use AI computational fluid simulation kit for scientific researchers, teachers, and students.  Furthermore, it offers a platform for those who have strong influence and interest in this field to communicate and cooperate.

## 3.Mission

Focusing on the application of AI in fluid mechanics. Exploring multiple AI fluid simulation modes such as physics-driven, data-driven and data-mechanism-fusion. Building AI+fluid computation framework with simple use and efficient operation. Supporting AI fluid research in aerospace, ship hydrodynamics, energy and power industries.

The key work of the group includes the following directions:

### Physics-driven AI fluid simulation

Physics-driven AI fluid simulation, i.e., introducing the physics equation into the loss function of the neural network.    Physics equations participate in network training to learn results that meet physical laws.  This module is mainly used for the forward and inverse solution of PDE equations and data assimilation.  At present, MindFlow provides APIs of common boundary, initial condition setting methods, sampling methods, loss function construction, etc., which meet the requirements for solving and optimizing relevant classical flow fields.

### Data-driven AI fluid simulation

The data-driven AI fluid simulation relies on a large amount of fluid simulation data.   The physical laws between data samples are learned by designing suitable neural networks that take the advantage of efficient parallelism and fast inference. Neural operators like FNO and DeepONet have certain parameter generalization capabilities.   These modules are mainly used for fast inference with a large amount of labeled data, parameter space design optimization, and other applications.   MindFlow now has network models such as ViT and FNO, which can solve classical flow (Burgers' equation, etc.) and flow problems faced in engineering practice.

### data-mechanism-fusion AI fluid simulation

AI fluid simulation based on data and mechanism fusion can learn partial differential equations from data and predict the dynamical properties of complex systems with high accuracy and uncover potential PDE models.  PDE-Net is one of the typical examples.  This model is mainly in small scientific data samples and known control equations.   It reduces the demand for data and improves the generalization of the network through built-in flow equations.  In addition, by coupling with a differentiable CFD solver and neural network, new applications such as AI correction, AI interpolation, and AI supersession of fluid simulation can be realized.  The basic API of PDE-Net is currently available to solve convection-diffusion equations.

### Differentiable CFD solver

Fluid simulation software solves the fluid control equations by numerical methods to analyze, predict and control fluid motion. It has a wide range of applications in aerospace, shipbuilding, and energy. Based on the AI framework, Shengsi MindFlow CFD differentiable solver has the advantages of jit(just-in-time compilation), vmap automatic vectorization, autograd end-to-end automatic differentiation, and support of different hardware.

## 4.Framework architecture/code repository

![输入图片说明](https://gitee.com/mindspore/community/raw/master/sigs/mindflow/images/mindflow_archi.png)

MindFlow is a fluid simulation kit based on Shengsi MindSpore, which supports AI flow simulation in aerospace, ship hydrodynamics, and energy and power industries.  It is aimed to provide efficient and easy-to-use AI computational fluid simulation software for industrial research engineers, teachers, and students from universities.  MindFlow provides a variety of common features such as physics-driven, data-driven, and data-mechanism-fusion AI fluid simulation.

## 5.Work plan

The main focus is on members' academic exchange activities to provide a reference for MindFlow evolution and function improvement.  SIG will organize one large event and several small events every year.  We will organize campus tours every quarter.  SIG will hold a large summer school event every year.  We will invite core experts in the group and prepare multiple topics for several-day lectures.  The group teachers will lead members to conduct technology research, function expansion, and bug fixing.  Members are also free to use MindFlow software for their own research and development.  The group will post open-source internship tasks in the community for students and teachers to claim. Through cooperative development and other forms of cooperation, we will conduct collaborative research in the community and carry out more applications.

## 6.SIG construction

### Leading member

![输入图片说明](https://gitee.com/mindspore/community/raw/master/sigs/mindflow/images/%E5%BC%A0%E4%BC%9F%E4%BC%9F.jpeg)

Zhang Weiwei, Distinguished Professor of Changjiang Scholars at Northwestern Polytechnical University, Vice President of the School of Aeronautics, and Chinese director of the International Joint Research Institute of Fluid Mechanics and Intelligence. He is mainly engaged in the research of intelligent hydrodynamics, aeroelasticity and aircraft design. He has won the National Natural Science Fund for Distinguished Young Scholars, the Youth Science and Technology Award of the Aviation Society, the first Youth Science and Technology Award of the Aerodynamic Society and other honors. He is currently the Vice President of the China Aerodynamic Society, the Director of the Intelligent Fluid Mechanics Professional Group, the Deputy Director of the Aeroelastic Mechanics Professional Committee, the Deputy Director of the Fluid-Solid Coupling Mechanics Professional Committee of the Chinese Society of Mechanics, the Vice President and Secretary-General of the Intelligent Fluid Mechanics Industry Consortium, and the Editorial Board of AST, TAML, AAMM, AIA and other international journals.

![输入图片说明](https://gitee.com/mindspore/community/raw/master/sigs/mindflow/images/%E8%91%A3%E5%BD%AC.jpeg)

Dong Bin, Peking University, professor of the Beijing International Mathematics Research Center, deputy director of the International Machine Learning Research Center, researcher of the National Engineering Laboratory for Big Data Analysis and Application, researcher of the National Biomedical Imaging Science Center, and vice president of the Institute of Computing and Digital Economics of Peking University.   He graduated from the School of Mathematical Sciences of Peking University in 2003, obtained a master's degree in the Department of Mathematics of the National University of Singapore in 2005, and obtained a doctor's degree in the Department of Mathematics of the University of California, Los Angeles, in 2009.   After graduation, he served as a visiting assistant professor in the Department of Mathematics at the University of California, San Diego, USA, and an assistant professor in the Department of Mathematics at the University of Arizona, USA, from 2011 to 2014. He joined Peking University at the end of 2014. The main research fields are scientific computing, machine learning, and their applications in computational imaging and data analysis. He is currently the editorial board member of the journal Inverse Problems and Imaging, and the deputy chief editor of CSIAM Transactions on Applied Mathematics, Journal of Computational Mathematics, and Journal of Machine Learning. In 2014, he won the Outstanding Young Scholar Award of Qiushi.   In 2015, he was selected for the "Thousand Talents Program" youth program of the Central Organization Department. In 2019, he was selected for the innovative talent promotion program of the Ministry of Science and Technology.   In 2020, he was selected as the leading talent of the "Ten Thousand Talents Program" of the Central Organization Department.   In 2022, he was invited to give a 45-minute report at the World Conference of Mathematicians (ICM).

![输入图片说明](https://gitee.com/mindspore/community/raw/master/sigs/mindflow/images/%E5%AD%99%E6%B5%A9.jpeg)

Sun Hao, "Associate Professor and Doctoral Tutor of the High-level School of Artificial Intelligence, at the Renmin University of China ", is a young expert in national high-level talents. In 2014, he obtained a doctorate in engineering mechanics from Columbia University in the United States and then engaged in post-doctoral research at the Massachusetts Institute of Technology. He served as an assistant professor and doctoral advisor of lifelong sequence at the University of Pittsburgh and Northeastern University in the United States. He mainly focused on scientific intelligence, artificial intelligence, mathematical foundation, and cross-cutting frontier research, including interpretable in-depth learning, physical-inspired in-depth learning, symbolic reinforcement learning and Reasoning, data-driven complex power system modeling and identification, infrastructure health monitoring, and intelligent management. More than 60 papers have been published in international first-class SCI journals (such as Nature Communications) and computer summit conferences (such as ICLR, NeuroIPS) and other important journals; Presided over ten vertical/horizontal research projects (about 29 million yuan in total), including the National High-level Talent Program, the National Natural Science Foundation of China (major research projects, general projects), the National Science Foundation of the United States (ECI, SCC, DRRG), and Huawei Technologies Co., Ltd; The research results have been widely reported by dozens of international well-known media (such as Fox News, Science Daily, MIT Technology Review, etc.). In 2018, he was selected into Forbes North America's "30 elites under the age of 30 (science)", and in 2019, he was selected as the "Top Ten Outstanding Chinese Youth in the United States".

### Team members

#### Name Unit Post Email

Maintainer: hsliu_ustc, Manager of Shengsi MindSpore

Maintainer: zedeng, Post-doctor of Shengsi MindSpore

Maintainer: Yi_zhang95, Engineer of Shengsi MindSpore

Team member: hong-ye-zhou, Engineer of Shengsi MindSpore

Team member: Bokai Li, Engineer of Shengsi MindSpore

Team member: liulei277, Engineer of Shengsi MindSpore

Team member: yangge_nihilism,Engineer of Shengsi MindSpore

Team member: Li Zhengyi, PhD student of Peking University lizhengyi@pku.edu.cn

Team member: Li Zhuoyuan, PhD. student of Peking University zy.li@stu.pku.edu.cn

Team member: Ye Zhanhong, PhD student of Peking University 2101110053@pku.edu.cn

Team member: Wang Qi, PhD student of Renmin University of China qi_wang@ruc.edu.cn

Team member: Hao Jiwei, Master of Beijing University of Aeronautics and Astronautics jiweihao@buaa.edu.cn

Team member: Lei Yixiang, undergraduate student of Wuhan University 2020301051197@whu.edu.cn

Team member: Zhang Yanglin, MPhil of the Chinese University of Hong Kong 119010446@qq.com

Team member: Liang JiaMing, Master of Xidian University me@puqing.work

Team member: Chen Lunhao, Undergraduate student of Guangdong Polytechnic Normal University 2085127827@qq.com

Team member: Ye Zhenghao, Undergraduate student of Wuhan University yezhenghao@isrc.isca.ac.cn

### About MindSpore SIG

The MindSpore community welcomes industry experts and academic partners to set up Special Interest Groups (SIGs) in the community, as the community's technical spokesperson in the field, to build a technical reputation in the field, and to build the MindSpore open source ecology.

The full name of MindSpore SIG is MindSpore Special Interest Groups. The MindSpore SIG is established to provide an open communication platform for experts, professors, and students in the field, to promote technical exchange and win-win cooperation through conference sharing and project development activities, and to enhance the influence and technical ability of SIG members.
