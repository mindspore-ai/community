# MindSpore Parallel Special Interest Group (SIG)

This is the working repository for the Parallel Special Interest Group (SIG). This repository contains all the artifacts, materials, meeting notes and proposals regarding **Auto-parallel**, **Model-parallel**, **Pipelined model-parallel**, **Tensor partitioning**, **Cost model**. Feedback and contributions are welcome.
1. **Auto-parallel**: The sizes of popular DNN models are getting larger, thus it is desired to automatically find an efficient way to parallelize the execution (training and inference) of the giant DNNs. This is the ultimate goal of this SIG.
2. **Model-parallel**: Unlike Data-parallel in which each device holds the entire model in training, Model-parallel is to partition the model to available devices, so that each device holds a slice of the entire model. Model-parallel is a more suitable approach for training giant models.  
3. **Pipelined model-parallel**: This is a paradigm to implement Model-parallel. This paradigm is to assign operators of a DNN model to different devices, so that different training batches can be pipelined.
4. **Tensor partitioning**: This is another paradigm to implement Model-parallel. This paradigm is to partition tensors of each operator in a DNN model, so that the devices obtain *symmetric* sequences of sliced operators.

# SIG Leads

* Cheng Li (University of Science and Technology of China)

# Logistics

* SIG leads will drive the meeting.
* Meeting annoucement will be posted on our gitee channel: https://gitee.com/mindspore/community/tree/master/sigs/parallel
* Feedbacks and topic requests are welcomed by all.

# Discussion

* Slack channel: https://app.slack.com/client/TUKCY4QDR/CUZ3FESNS?cdn_fallback=2
* Documents and artifacts: https://gitee.com/mindspore/community/tree/master/sigs/parallel

# Meeting notes