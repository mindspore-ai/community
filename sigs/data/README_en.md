# MindSpore Data Special Interest Group (SIG)

This is the working repo for the Data special interest group (SIG). This repo contains all the artifacts, materials, meeting notes and proposals regarding **dataset - data processing** and **mindrecord - data format** in MindSpore. Feedbacks and contributions are welcome.

1. **Data Processing**: You can understand it as a Dataset, which is mainly responsible for reading the user's data into a Dataset, then performing related data enhancement operations (such as: resize, onehot, rotate, shuffle, batch ...), and finally provide the Dataset to the training process.
2. **Data Format**: It can conveniently normalize the user's training data to a unified format (MindRecord). The specific operation steps are as follows: The user can easily convert the training data into MindRecord data by defining the training data schema and calling the Python API interface. The format is then read into a Dataset through MindDataset and provided to the training process.

## SIG Leads

* Liu Cunwei (Huawei)

## Logistics

* SIG leads will drive the meeting.
* Meeting announcement will be posted on our gitee channel: <https://gitee.com/mindspore/community/tree/master/sigs/data>
* Feedbacks and topic requests are welcome by all.

## Discussion

* Slack channel: <https://app.slack.com/client/TUKCY4QDR/C010RPN6QNP?cdn_fallback=2>
* Documents and artifacts: <https://gitee.com/mindspore/community/tree/master/sigs/data>

## Representative videos

* [mindspore data processing introduction](https://www.bilibili.com/video/BV1RZ4y1W7FL)
* [mindspore data loading and data format conversion](https://mindspore-website.obs.cn-north-4.myhuaweicloud.com/teaching_video/video/%E5%8A%A0%E8%BD%BD%E6%95%B0%E6%8D%AE%E9%9B%86%E4%B8%8E%E8%BD%AC%E6%8D%A2%E6%A0%BC%E5%BC%8F.mp4)
* [optimize data processing](https://mindspore-website.obs.cn-north-4.myhuaweicloud.com/teaching_video/video/%E4%BC%98%E5%8C%96%E6%95%B0%E6%8D%AE%E5%A4%84%E7%90%86.mp4)

## Main issue To be solved

> Here we call for developer joining us to develop a better Dataset processing system, following is mainly issue in each season.<br>
> **Comment in issue please if you have any quetions and for better communication**.
> Also you can find all the issue in gitee by filter with label [comp/data](https://gitee.com/mindspore/mindspore/issues?assignee_id=&author_id=&branch=&collaborator_ids=&issue_search=&label_ids=58023093&label_text=comp/data&milestone_id=&program_id=&scope=&sort=&state=open)

* [Main issue of Q3](https://gitee.com/mindspore/mindspore/issues/I3MXRO)

## Meeting notes

* [Thursday April 2, 2020](./meetings/001-20200402.md)
* [Friday May 15, 2020](./meetings/002-20200515.md)
* [Wednesday June 03, 2020](./meetings/003-20200603.md)
* [Friday July 03, 2020](./meetings/004-20200703.md)
* [Wednesday August 05, 2020](./meetings/005-20200805.md)
* [Thursday August 06, 2020](./meetings/006-20200806.md)
* [Thursday September 03, 2020](./meetings/007-20200903.md)
* [Friday October 16, 2020](./meetings/008-20201016.md)
* [Wednesday November 04, 2020](./meetings/009-20201104.md)
* [Monday November 23, 2020](./meetings/010-20201123.md)
* [Wednesday April 14, 2021](./meetings/011-20210414.md)

