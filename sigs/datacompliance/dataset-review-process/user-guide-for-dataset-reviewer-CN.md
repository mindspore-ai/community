# 数据集review助手使用指导

## 目录

1. **[数据集review助手逻辑架构](#1.%20数据集review助手逻辑架构)**
2. **[数据集审核入口](#2.%20数据集审核入口)**
3. **[数据集review助手模块介绍](#3.%20数据集review助手模块介绍)**
4. **[数据集单点/批量审核上传](#4.%20数据集单点/批量审核上传)**
5. **[数据集AIBOM信息维护](#5.%20数据集AIBOM信息维护)**
6. **[数据集结论必要属性预览与下载](#6.%20数据集结论必要属性预览与下载)**

## 1. 数据集review助手逻辑架构

<img src='.\imgs\dataset_reviewer_logic_architecture_CN.png' alt="数据集review助手逻辑架构" align='left'/>

## 2. 数据集审核入口

- 在[数据信息共享平台](http://www.opendataology.com:30800/)中，通过Login按钮登录后，点击Review，跳转至数据集review助手模块；

![image-20230131143410988](.\imgs\dataset_reviewer_entrance.png)

## 3. 数据集review助手模块介绍

- Review upload：数据集单点审核上传
- Review upload by file：数据集批量审核上传
- AIBOM：AIBOM信息补充与维护
- Reviewed dataset：数据集审核开放下载

<img src='.\imgs\dataset_reviewer_module_intro.png' align='left'/>

## 4. 数据集单点/批量审核上传

- Review upload (数据集单点审核上传): 通过填写单个数据集的name、location、originator即可提交审核。
- Review upload by file (数据集批量审核上传): 在Excel或CSV中按模板格式批量添加审核项。
- name：数据集名称。
- location：数据集官网。
- originator：贡献者清单，以逗号和空格分割。

### 4.1 数据集单点审核上传

<img src='.\imgs\single_dataset_uploading.png' align='left'/>

### 4.2 数据集批量审核上传

<center class="half">
    <img src=".\imgs\batch_datasets_uploading_1.png" width="350" height="320"/><img src=".\imgs\batch_datasets_uploading_2.png" width="790" height="320"/>
</center>

## 5. 数据集AIBOM信息维护

- 在AIBOM界面可预览数据集各AIBOM属性。
- edit：补充或维护数据集的AIBOM信息，并保存。
- submit：确认该数据集的AIBOM待审核信息，并提交至审核侧。
- delete：该数据集无需审核，可直接删除。

<img src='.\imgs\AIBOM_preview.png' align='left'/>

### 5.1 点击edit后可补充数据集AIBOM必要属性详情信息

<img src='.\imgs\AIBOM_edit.png' align='left'/>

- name*: 数据集名称
- location*: 数据集官网
- originator*: 贡献者清单，多贡献者时以逗号和空格分割。
- license location*: 许可地址链接
- concluded license: 在[SPDX License List](https://spdx.org/licenses)中认证的License。
- declared license: 自定义许可的内容 (如license、term of use、citation、reference等中英文关键字)。
- type*: 数据集内容类型。
- size*: 数据集总大小。
- intended use*: 数据集官方使用目的。
- checksum: 校验和。
- data collection process: 数据集收集过程。
- known biases: 是否有任何偏见。
- sensitive personal information: 是否有个人隐私信息。
- offensive content: 是否有冒犯内容。
- rejection notes: 若此数据集审核被驳回，则显示原因。

注：concluded license和declared license至少有一项非空。

## 6. 数据集结论必要属性预览与下载

![image-20230131170554141](.\imgs\initial_result_preview.png)

![image-20230131170602398](.\imgs\initial_result_download.png)

- 通过点击download可下载已初步审核过的数据集。
- review result*: 审核结论，判断是否可上线。
- dataset commercially used*: 数据集是否可商业使用。
- dataset commercially distributed*: 数据集是否可商业分发。
- product commercially published*: 是否可集成至产品商业发布。
- notes: 结论备注。

