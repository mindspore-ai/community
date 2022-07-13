# AlphaFold2-Chinese
中文版AlphaFold2开源模型复现-基于DeepMind&ColabFold&Mindspore：
* https://github.com/sokrypton/ColabFold
* https://github.com/deepmind/alphafold
* https://gitee.com/mindspore/mindscience/tree/master/MindSPONGE/mindsponge/fold

<div align=center>
<img src="https://gitee.com/turings-cat/community/blob/master/reproduce/AlphaFold2-Chinese/docs/seq_64.gif" alt="T1079" width="400"/>
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

蛋白质结构预测工具是利用计算机高效计算获取蛋白质空间结构的软件。该计算方法一直存在精度不足的缺陷，直至2020年谷歌DeepMind团队的[AlphaFold2](https://www.nature.com/articles/s41586-021-03819-2)【1】【2】取得CASP14比赛中蛋白质3D结构预测的榜首，才让这一缺陷得以弥补。本次开源的蛋白质结构预测推理工具模型部分与其相同，在多序列比对阶段，采用了[MMseqs2](https://www.biorxiv.org/content/10.1101/2021.08.15.456425v1.full.pdf)【3】进行序列检索，相比于原版算法端到端运算速度有2-3倍提升。

## 环境要求

### 硬件环境与框架

本代码运行基于Ascend处理器硬件环境与[MindSpore](https://www.mindspore.cn/) AI框架，当前版本需基于最新库上master代码（2021-11-08之后的代码）[编译](https://www.mindspore.cn/install/detail?path=install/r1.5/mindspore_ascend_install_source.md&highlight=%E6%BA%90%E7%A0%81%E7%BC%96%E8%AF%91)，
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

### MindSpore Serving安装

我们提供以服务模式运行推理，该模式使用MindSpore Serving提供高效推理服务，多条序列推理时避免重复编译，大幅提高推理效率，MindSpore Serving安装和配置可以参考[MindSpore Serving安装页面](https://www.mindspore.cn/serving/docs/zh-CN/r1.5/serving_install.html)。

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

## 脚本说明

### 脚本及样例代码

```bash
├── mindscience
    ├── MindSPONGE
        ├── mindsponge
            ├── fold
                ├── README_CN.md                    // fold 相关中文说明
                ├── run.py                          // 推理脚本
                ├── model.py                        // 主模型
                ├── requirements.txt                  // 依赖包
                ├── serving_server.py               // 服务模式服务端脚本
                ├── serving_cline.py                // 服务模式客户端脚本
                ├── fold_service
                    ├── servable_config.py              // 服务模式配置脚本
                ├── module
                    ├── basic_module.py                 // 基础模块
                    ├── evoformer_module.py             // evoformer模块
                    ├── structure_module.py             // 结构模块
                ├── data
                    ├── feature
                        ├── data_transforms.py              //msa和template数据处理
                        ├── feature_extraction.py           //msa和template特征提取
                    ├── tools
                        ├── data_process.py                 // 搜索msa和template
                        ├── data_tools.py                   // 数据处理脚本
                        ├── mmcif_parsing.py                // mmcif解析脚本
                        ├── msa_search.sh                   // mmseqs2搜索msa的shell脚本
                        ├── parsers.py                      // 解析文件脚本
                        ├── templates.py                    // 模板搜索脚本
                ├── config
                    ├── config.py                           //参数配置脚本
                    ├── global_config.py                    //全局参数配置脚本
                ├── common
                    ├── generate_pdb.py                     // 生成pdb
                    ├── r3.py                               // 3D坐标转换
                    ├── residue_constants.py                // 氨基酸残基常量
                    ├── utils.py                            // 功能函数
```

### 推理示例

```bash
用法：run.py [--seq_length PADDING_SEQENCE_LENGTH]
             [--input_fasta_path INPUT_PATH][--msa_result_path MSA_RESULT_PATH]
             [--database_dir DATABASE_PATH][--database_envdb_dir DATABASE_ENVDB_PATH]
             [--hhsearch_binary_path HHSEARCH_PATH][--pdb70_database_path PDB70_PATH]
             [--template_mmcif_dir TEMPLATE_PATH][--max_template_date TRMPLATE_DATE]
             [--kalign_binary_path KALIGN_PATH][--obsolete_pdbs_path OBSOLETE_PATH]


选项：
  --seq_length             补零后序列长度，目前支持256/512/1024/2048
  --input_fasta_path       FASTA文件，用于预测蛋白质结构的蛋白质序列
  --msa_result_path        保存mmseqs2检索得到的msa结果路径
  --database_dir           搜索msa时的数据库
  --database_envdb_dir     搜索msa时的扩展数据库
  --hhsearch_binary_path   hhsearch可执行文件路径
  --pdb70_database_path    供hhsearch使用的pdb70数据库路径
  --template_mmcif_dir     具有mmcif结构模板的路径
  --max_template_date      模板最新发布的时间
  --kalign_binary_path     kalign可执行文件路径
  --obsolete_pdbs_path     PDB IDs的映射文件路径
```

### 推理过程

 加载alphafold checkpoint，下载地址[点击这里](https://download.mindspore.cn/model_zoo/research/hpc/molecular_dynamics/protein_fold_1.ckpt)，根据自身需求选择合适蛋白质序列配置，当前提供256/512/1024/2048四个标准配置，推理过程如下：

1. 输入参数需要通过`fold_service/config.py`配置，参数含义参见[推理示例](#推理示例)

2. 参数配置好后，先使用`serving_server.py`启动服务端进程，进程成功启动时log显示如下：

    ``` log
        Serving: Serving gRPC server start success, listening on 127.0.0.1:5500
        Serving: Serving RESTful server start success, listening on 127.0.0.1:1500
    ```

3. 服务端进程成功启动后运行`serving_client.py`即可进行推理，第一次推理需要编译

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

### TMscore对比图

- 34条CASP14结果与alphafold2对比：

<div align=center>
<img src="https://gitee.com/turings-cat/community/blob/master/reproduce/AlphaFold2-Chinese/docs/all_experiment_data.jpg" alt="all_data" width="600"/>
</div>

### 预测结果对比图

- T1079(长度505)：

<div align=center>
<img src="https://gitee.com/turings-cat/community/blob/master/reproduce/AlphaFold2-Chinese/docs/seq_64.gif" alt="T1079" width="400"/>
</div>

- T1044(长度2180)：

<div align=center>
<img src="https://gitee.com/turings-cat/community/blob/master/reproduce/AlphaFold2-Chinese/docs/seq_21.jpg" alt="T1044" width="400"/>
</div>

## 引用

[1] Jumper J, Evans R, Pritzel A, et al. Applying and improving AlphaFold at CASP14[J].  Proteins: Structure, Function, and Bioinformatics, 2021.

[2] Jumper J, Evans R, Pritzel A, et al. Highly accurate protein structure prediction with AlphaFold[J]. Nature, 2021, 596(7873): 583-589.

[3] Mirdita M, Ovchinnikov S, Steinegger M. ColabFold-Making protein folding accessible to all[J]. BioRxiv, 2021.