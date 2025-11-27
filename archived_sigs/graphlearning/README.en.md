## Join Graph Learning SIG to create an efficient and easy-to-use graph learning library

Due to the powerful expressive power of the graph data structure, the use of machine learning to analyze graphs has attracted more and more attention, and has become a research hotspot at major AI conferences. In recent years, graph machine learning has made new breakthroughs in network data analysis, recommendation systems, molecular computing, knowledge graphs, and combinatorial optimization. In the recommendation scenario, graph learning is used to efficiently represent real-time interactive data, leading the development of the real-time streaming recommendation model; in the drug discovery scenario, graph learning has become the basic model for drug molecular representation; in the chip design scenario, Google has proved the application of GNN modeling The chip netlist diagram can realize the optimal layout of the chip unit. These cases all demonstrate the effectiveness and potential value of graph learning methods.

Different from the development of deep learning frameworks and domain libraries in CV and NLP fields, there is no stable and easy-to-use model library or community in the field of graph learning, so that algorithm researchers can quickly experiment with algorithms, and application developers can efficiently train and deploy Model.

Therefore, building an open, easy-to-use, and efficient graph learning library that is analogous to the domain library Huggingface of the transformer method is conducive to promoting the vigorous development of graph learning research and innovative breakthroughs in graph learning methods applied to other fields.

To this end, Shengsi Graph Learning Special Interest Group (Graph Learning SIG for short) was formally established and recruited like-minded partners from the open source community.

## Graph Learning SIG

### 1. Introduction to SIG

Graph Learning SIG focuses on the latest technologies and applications in the direction of graph computing and graph learning, mainly including the following directions:

1. Algorithm evolution: random walk, graph neural network, knowledge graph, hyperbolic graph neural network
2. Graph framework optimization and evolution: large-scale graph distribution, heterogeneous graph learning optimization, and sequence graph learning optimization
3. Graph learning application scenarios: molecular computing, search recommendation

### 2. SIG Code Repository

[MindSpore Graph Learning] https://gitee.com/mindspore/graphlearning

### 3. SIG Results

MindSpore Graph Learning

The graph learning framework jointly constructed by the team of Professor James Cheng of the Chinese University of Hong Kong and the Huawei MindSpore team based on MindSpore tries to seek breakthroughs from the perspective of ease of use and high performance, and innovatively proposes a point-centric programming paradigm and a graph-oriented Learned compiler optimization strategies.

The graph neural network model needs to perform information transfer and aggregation on a given graph structure, and the whole graph calculation cannot express these operations intuitively. MindSpore Graph Learning provides a point-centered programming paradigm, which is more in line with the graph learning algorithm logic and Python language style, and can directly translate formulas to codes, reducing the gap between algorithm design and implementation.

Combining MindSpore's graph-computing fusion and automatic operator compilation technology (AKG) features, MindSpore Graph Learning automatically recognizes the unique execution pattern of the graph neural network task for fusion and kernel level optimization, which can cover existing operators and new combinations in the existing framework The integration and optimization of operators has achieved an average performance improvement of 3 to 4 times compared with existing popular frameworks.

### 4. Graph Learning SIG Composition

#### Lead Member：

##### Lei CHEN

Chief Professor of Computer Science and Engineering Department of Hong Kong University of Science and Technology, Director of Big Data Research Institute, IEEE Fellow, ACM Outstanding Scientist, Chief Scientist of MindSpore, research directions include data-driven machine learning, large-scale graph learning, knowledge graph, etc.

##### Zipeng Liu

Assistant professor of the School of Software, Beihang University, graduated with a Ph.D. from the Department of Computer Science, University of British Columbia, Canada. His main research directions are visualization and visual analysis, human-computer interaction, big data analysis, and interpretable machine learning. He has published many papers in top journals and conferences (TVCG, CHI) in the field of visualization, and has won the PacificVis Best Paper Nomination Award.

#### Team Member

Member:Yujie Yuan，Shengsi MindSpore Evangelist

Member:Yidi Wu，Ph.D.，Department of Computer Science, The Chinese University of Hong Kong

Member:Peiqi Yin，Ph.D.，Department of Computer Science, The Chinese University of Hong Kong

Member:Long Da，Huawei Data System Senior Engineer

Member:Sophie，Senior Engineer of Shengsi MindSpore

Member:Xun Feng，Senior Engineer of Shengsi MindSpore

#### Maintainers

Responsible for the operation of SIG's daily activities, formulating training plans for SIG members, and developing project management.

Xun Feng

Sophie

### 5. 2022 Goal

1. Added support for 10+ graph data processing or graph convolution interfaces
2. Added support for distributed training of graph models
3. Access to CSR data format to further optimize performance
4. Establish GNN SIG

### 6. SIG Main Activities

#### Online technology sharing

SIG internal members, industry experts and professors are invited from time to time to share technology, explain MindSpore-related features or introduce application cases, etc. The average cycle is 1-2 months, and the event notice will be updated on the SIG page and the code warehouse homepage.

#### Technical Research

It is organized once a quarter to publish the latest papers in the industry or research tasks on open source work, and SIG members will receive them, and finally display the research results in the form of blog posts on the SIG Zhihu account or sharing at regular meetings.

#### Development task distribution

1. The open source internship task <https://gitee.com/mindspore/community/issues/I55TNF> is aimed at current students, and the time is flexible. After completing the task and earning points, you can receive the corresponding internship salary.
2. Common tasks in the community are presented in the form of graph learning warehouse issues, and any interested developer can submit the corresponding code PR.

#### Member Development

Membership includes three types: Contributors, Committers, and Maintainers, which are recorded in the SIG member list. The description and application conditions of each identity role are as follows:

 **Contributors:**  Actively participate in SIG's daily activities, project development, etc., responsible for code warehouse PR review, issue submission and technical research paper recommendation, etc. Application conditions: Participate in at least 2 SIG meetings/events, and participate in more than 2 PR code reviews, publish more than 10 effective revision comments, or complete more than 2 technical research tasks.

 **Committers:**  Code warehouse committer, who has the permission to merge code warehouses. Application conditions: as a contributor, at least complete 5 community issue tasks or 3 open source internship tasks.

 **Maintainers:**  Members of the SIG Operations Committee, responsible for the technical direction formulation and event organization of the entire SIG. Application conditions: as committers, at least 2 members of the existing maintainers and more than 65% of the total number of members voted to agree.

 **How to apply:** First fork the Community warehouse; then submit a PR, add your Gitee home page link, name (real name not required), registered Gitee email address, and interest direction to the SIG member list, and list relevant achievements or contributions in the PR description. After the PR is submitted, the Maintainers will review it.

### 7. Graph Learning SIG's mission

Focus on the latest technologies and applications in the direction of graph computing and graph learning, explore more expressive graph learning models, build a graph learning framework that is simple to use and computationally efficient, and apply graph learning methods to actual scenarios to achieve better results.

The focus of the group's work includes the following directions:

#### ● Graph learning model library construction

Realize cutting-edge algorithm models in various directions of graph learning based on MindSpore, including but not limited to random walk, knowledge map, graph neural network, hyperbolic graph neural network, sequential graph neural network, Graphormer, etc.

#### ● Graph computing framework optimization

Different from the calculation of structured data, graph calculation has the characteristics of poor data locality, high transmission calculation ratio, complex data dependence, etc., and has high requirements for computing resources and memory usage. This feature is particularly prominent in large-scale graph distributed computing, heterogeneous graph learning models, and sequence graph learning scenarios. A more efficient solution based on MindSpore is proposed for the data structure, computing implementation, and compilation optimization of these scenarios.

In terms of ease of use, give full play to the logical interpretability of graph data, analyze the entire process of graph model training through visualization tools, and further guide users to debug and optimize graph models or data processing.

#### ● Scene field package

In recent years, graph learning has made a lot of progress in the application of recommendation, molecular computing, knowledge graph, autonomous driving and other scenarios. It is further necessary to build a general data set for each scenario including but not limited to recommendation, molecular computing, knowledge graph, etc., and to refine common module interfaces. , to realize the SOTA model, so that subsequent researchers or applicators can quickly work on this basis and build an open and thriving community.

### 8. Graph Learning SIG work plan

#### ● Early stage

Focus on members' academic exchange activities, regularly share the latest papers or open source work research and analysis reports, and organize online communication activities from time to time, focusing on improving the expressive power of graph algorithms, graph computing optimization, and problems encountered in the application of graph learning. The progress of the research work and discuss the difficulties in the research work.

#### ● Late stage

Carry out cooperative research on issues related to graph learning among domestic universities and enterprises through cooperative development or competition.
