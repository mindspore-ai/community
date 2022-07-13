# AlphaFold2-Chinese
中文版AlphaFold2开源模型复现-基于DeepMind&ColabFold&Mindspore：
* https://github.com/sokrypton/ColabFold
* https://github.com/deepmind/alphafold
* https://gitee.com/mindspore/mindscience/tree/master/MindSPONGE/mindsponge/fold

<div align=center>
<img src="https://gitee.com/turings-cat/community/raw/master/reproduce/AlphaFold2-Chinese/docs/seq_64.gif" alt="T1079" width="400"/>
</div>

# 目录

<!-- TOC -->

- [目录](#目录)
    - [模型描述](#模型描述)
    - [环境要求](#环境要求)
        - [硬件环境与框架](#硬件环境与框架)
        - [MMseqs2安装](#mmseqs2安装)
        - [MindSpore Serving安装](#mindspore_serving安装)
    - [数据准备](#数据准备)
        - [MSA所需数据库](#msa所需数据库)
        - [Template所需工具和数据](#template所需工具和数据)
            - [数据](#数据)
            - [工具](#工具)
    - [脚本说明](#脚本说明)
        - [脚本及样例代码](#脚本及样例代码)
        - [推理示例](#推理示例)
        - [推理过程](#推理过程)
            - [推理结果](#推理结果)
    - [推理性能](#推理性能)
        - [TMscore对比图](#tmscore对比图)
        - [预测结果对比图](#预测结果对比图)
    - [引用](#引用)

<!-- /TOC -->

## 模型描述

Alphafold2提出了一个新的结构去同时嵌入MSA和残基-残基对的特征（pairwise features），新的输出表示去确保准确的端到端训练，以及新的辅助loss。此外，在finetune训练之前，AlphaFold2首先预训练了一把，在MSA上使用BERT任务遮盖住一些氨基酸再还原回来，此外还使用自蒸馏，自估计的loss去自监督学习——先用训好的模型在只有氨基酸序列的数据上生成预测结果，然后只保留高确信度的，然后使用这个数据预训练，在训练时把输入加上更强的drop out和mask，来增大学习难度，去预测完整信息时高确信度的结果。

结构由两部分组成，Evoformer和结构模块（Structure Module）。Evoformer输入MSA，模板，自己的氨基酸序列，输出MSA信息和残基-残基对关系（刚刚提到的pairwise features）建模。结构模块中，丢掉MSA中的其他氨基酸序列，只保留目标的那一条，然后再加上pairwise features，去计算更新backbone frames，预测所有氨基酸的方位和距离，肽键的长度和角度，氨基酸内部的扭转角度等。Evoformer即进化版Transformer，用来计算MSA和pairwise features。输入MSA和pairwise features，通过很多注意力层，最终输出MSA和pairwise faetures。

基于2021年谷歌DeepMind团队的[AlphaFold2](https://www.nature.com/articles/s41586-021-03819-2)在多序列比对阶段，采用了[MMseqs2](https://www.biorxiv.org/content/10.1101/2021.08.15.456425v1.full.pdf)进行序列检索，相比于原版算法端到端运算速度有2-3倍提升。




## 环境要求

### 硬件环境与框架

本代码运行基于Nvidia GPU/Tesla V100/Ascend处理器（三种都可以，参考华为之前的是Ascend系列为主）与[MindSpore](https://www.mindspore.cn/) AI框架，当前版本需基于最新库上master代码（2021-11-08之后的代码）[编译](https://www.mindspore.cn/install/detail?path=install/r1.5/mindspore_ascend_install_source.md&highlight=%E6%BA%90%E7%A0%81%E7%BC%96%E8%AF%91)，
MindSpore环境参见[MindSpore教程](https://www.mindspore.cn/tutorials/zh-CN/master/index.html)，环境安装后需要运行以下命令配置环境变量：

``` shell
export MS_DEV_ENABLE_FALLBACK=0
```

其余python依赖请参见[requirements.txt](https://gitee.com/mindspore/mindscience/tree/master/MindSPONGE/mindsponge/fold/requirements.txt)。

### MMseqs2安装

MMseqs2用于生成多序列比对(multiple sequence alignments，MSA)，MMseqs2安装和使用可以参考[MMseqs2 User Guide](https://mmseqs.com/latest/userguide.pdf)，安装完成后需要运行以下命令配置环境变量：

``` shell
export PATH=$(pwd)/mmseqs/bin/:$PATH
```


## 数据准备

### MSA所需数据库

- [uniref30_2103](http://wwwuser.gwdg.de/~compbiol/colabfold/uniref30_2103.tar.gz)：375G（下载68G）
- [colabfold_envdb_202108](http://wwwuser.gwdg.de/~compbiol/colabfold/colabfold_envdb_202108.tar.gz)：949G（下载110G）

数据处理参考[colabfold](http://colabfold.mmseqs.com)。

### Template所需工具和数据

#### 数据

- [pdb70](http://wwwuser.gwdg.de/~compbiol/data/hhsuite/databases/hhsuite_dbs/old-releases/pdb70_from_mmcif_200401.tar.gz)：56G(下载19G)
- [mmcif database](https://ftp.rcsb.org/pub/pdb/data/structures/divided/mmCIF/)： 206G（下载48G）
- [obsolete_pdbs](http://ftp.wwpdb.org/pub/pdb/data/status/obsolete.dat)：140K

#### 工具

- [HHsearch](https://github.com/soedinglab/hh-suite)
- [kalign](https://msa.sbc.su.se/downloads/kalign/current.tar.gz)


#### 推理结果

推理结果保存在 `./result` 中，共有两个文件，其中的pdb文件即为蛋白质结构预测结果，timings文件保存了运行过程中的时间信息和confidence信息。

```bash
{"pre_process_time": 418.57, "model_time": 122.86, "pos_process_time": 0.14, "all_time ": 541.56, "confidence ": 94.61789646019058}
```

## 推理性能

| 参数  | Fold(Ascend)                         |
| ------------------- | --------------------------- |
| 模型版本      | AlphaFold                       |
| 资源        | Ascend 910                  |
| 上传日期              | 2021-11-05                    |
| MindSpore版本   | master                 |
| 数据集 | CASP14 T1079 |
| seq_length          |      505                     |
| confidence  | 94.62 |
| TM-score | 98.01% |
|运行时间|541.56s|


## Citations

```bibtex
@misc{unpublished2021alphafold2,
    title   = {Alphafold2},
    author  = {John Jumper},
    year    = {2020},
    archivePrefix = {arXiv},
    primaryClass = {q-bio.BM}
}
```

```bibtex
@article{Rao2021.02.12.430858,
    author  = {Rao, Roshan and Liu, Jason and Verkuil, Robert and Meier, Joshua and Canny, John F. and Abbeel, Pieter and Sercu, Tom and Rives, Alexander},
    title   = {MSA Transformer},
    year    = {2021},
    publisher = {Cold Spring Harbor Laboratory},
    URL     = {https://www.biorxiv.org/content/early/2021/02/13/2021.02.12.430858},
    journal = {bioRxiv}
}
```

```bibtex
@article {Rives622803,
    author  = {Rives, Alexander and Goyal, Siddharth and Meier, Joshua and Guo, Demi and Ott, Myle and Zitnick, C. Lawrence and Ma, Jerry and Fergus, Rob},
    title   = {Biological Structure and Function Emerge from Scaling Unsupervised Learning to 250 Million Protein Sequences},
    year    = {2019},
    doi     = {10.1101/622803},
    publisher = {Cold Spring Harbor Laboratory},
    journal = {bioRxiv}
}
```

```bibtex
@article {Elnaggar2020.07.12.199554,
    author  = {Elnaggar, Ahmed and Heinzinger, Michael and Dallago, Christian and Rehawi, Ghalia and Wang, Yu and Jones, Llion and Gibbs, Tom and Feher, Tamas and Angerer, Christoph and Steinegger, Martin and BHOWMIK, DEBSINDHU and Rost, Burkhard},
    title   = {ProtTrans: Towards Cracking the Language of Life{\textquoteright}s Code Through Self-Supervised Deep Learning and High Performance Computing},
    elocation-id = {2020.07.12.199554},
    year    = {2021},
    doi     = {10.1101/2020.07.12.199554},
    publisher = {Cold Spring Harbor Laboratory},
    URL     = {https://www.biorxiv.org/content/early/2021/05/04/2020.07.12.199554},
    eprint  = {https://www.biorxiv.org/content/early/2021/05/04/2020.07.12.199554.full.pdf},
    journal = {bioRxiv}
}
```

```bibtex
@misc{king2020sidechainnet,
    title   = {SidechainNet: An All-Atom Protein Structure Dataset for Machine Learning}, 
    author  = {Jonathan E. King and David Ryan Koes},
    year    = {2020},
    eprint  = {2010.08162},
    archivePrefix = {arXiv},
    primaryClass = {q-bio.BM}
}
```

```bibtex
@misc{alquraishi2019proteinnet,
    title   = {ProteinNet: a standardized data set for machine learning of protein structure}, 
    author  = {Mohammed AlQuraishi},
    year    = {2019},
    eprint  = {1902.00249},
    archivePrefix = {arXiv},
    primaryClass = {q-bio.BM}
}
```

```bibtex
@misc{gomez2017reversible,
    title     = {The Reversible Residual Network: Backpropagation Without Storing Activations}, 
    author    = {Aidan N. Gomez and Mengye Ren and Raquel Urtasun and Roger B. Grosse},
    year      = {2017},
    eprint    = {1707.04585},
    archivePrefix = {arXiv},
    primaryClass = {cs.CV}
}
```

```bibtex
@misc{fuchs2021iterative,
    title   = {Iterative SE(3)-Transformers},
    author  = {Fabian B. Fuchs and Edward Wagstaff and Justas Dauparas and Ingmar Posner},
    year    = {2021},
    eprint  = {2102.13419},
    archivePrefix = {arXiv},
    primaryClass = {cs.LG}
}
```

```bibtex
@misc{satorras2021en,
    title   = {E(n) Equivariant Graph Neural Networks}, 
    author  = {Victor Garcia Satorras and Emiel Hoogeboom and Max Welling},
    year    = {2021},
    eprint  = {2102.09844},
    archivePrefix = {arXiv},
    primaryClass = {cs.LG}
}
```

```bibtex
@misc{su2021roformer,
    title   = {RoFormer: Enhanced Transformer with Rotary Position Embedding},
    author  = {Jianlin Su and Yu Lu and Shengfeng Pan and Bo Wen and Yunfeng Liu},
    year    = {2021},
    eprint  = {2104.09864},
    archivePrefix = {arXiv},
    primaryClass = {cs.CL}
}
```

```bibtex
@article{Gao_2020,
    title   = {Kronecker Attention Networks},
    ISBN    = {9781450379984},
    url     = {http://dx.doi.org/10.1145/3394486.3403065},
    DOI     = {10.1145/3394486.3403065},
    journal = {Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining},
    publisher = {ACM},
    author  = {Gao, Hongyang and Wang, Zhengyang and Ji, Shuiwang},
    year    = {2020},
    month   = {Jul}
}
```

```bibtex
@article {Si2021.05.10.443415,
    author  = {Si, Yunda and Yan, Chengfei},
    title   = {Improved protein contact prediction using dimensional hybrid residual networks and singularity enhanced loss function},
    elocation-id = {2021.05.10.443415},
    year    = {2021},
    doi     = {10.1101/2021.05.10.443415},
    publisher = {Cold Spring Harbor Laboratory},
    URL     = {https://www.biorxiv.org/content/early/2021/05/11/2021.05.10.443415},
    eprint  = {https://www.biorxiv.org/content/early/2021/05/11/2021.05.10.443415.full.pdf},
    journal = {bioRxiv}
}
```

```bibtex
@article {Costa2021.06.02.446809,
    author  = {Costa, Allan and Ponnapati, Manvitha and Jacobson, Joseph M. and Chatterjee, Pranam},
    title   = {Distillation of MSA Embeddings to Folded Protein Structures with Graph Transformers},
    year    = {2021},
    doi     = {10.1101/2021.06.02.446809},
    publisher = {Cold Spring Harbor Laboratory},
    URL     = {https://www.biorxiv.org/content/early/2021/06/02/2021.06.02.446809},
    eprint  = {https://www.biorxiv.org/content/early/2021/06/02/2021.06.02.446809.full.pdf},
    journal = {bioRxiv}
}
```

```bibtex
@article {Baek2021.06.14.448402,
    author  = {Baek, Minkyung and DiMaio, Frank and Anishchenko, Ivan and Dauparas, Justas and Ovchinnikov, Sergey and Lee, Gyu Rie and Wang, Jue and Cong, Qian and Kinch, Lisa N. and Schaeffer, R. Dustin and Mill{\'a}n, Claudia and Park, Hahnbeom and Adams, Carson and Glassman, Caleb R. and DeGiovanni, Andy and Pereira, Jose H. and Rodrigues, Andria V. and van Dijk, Alberdina A. and Ebrecht, Ana C. and Opperman, Diederik J. and Sagmeister, Theo and Buhlheller, Christoph and Pavkov-Keller, Tea and Rathinaswamy, Manoj K and Dalwadi, Udit and Yip, Calvin K and Burke, John E and Garcia, K. Christopher and Grishin, Nick V. and Adams, Paul D. and Read, Randy J. and Baker, David},
    title   = {Accurate prediction of protein structures and interactions using a 3-track network},
    year    = {2021},
    doi     = {10.1101/2021.06.14.448402},
    publisher = {Cold Spring Harbor Laboratory},
    URL     = {https://www.biorxiv.org/content/early/2021/06/15/2021.06.14.448402},
    eprint  = {https://www.biorxiv.org/content/early/2021/06/15/2021.06.14.448402.full.pdf},
    journal = {bioRxiv}
}
```