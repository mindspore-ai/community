# MindSpore社区Pull Request调测命令指南

MindSpore社区当前涉及构建形态众多，因此提供多种门禁执行命令与调测指令，具体内容如下：

* 需要执行全量门禁时，执行 `/retest`，调度框架会根据当前pr修改内容自动分配最适合的门禁执行流程，在完成后打 `ci-pipeline-passed` 标签，拥有此标签的pr才可以被合入。
* 在确认自己的代码没有功能相关的修改的情况下（例如仅改动描述文档），在提交代码前创建前缀为 `code_docs` 的代码分支，再执行 `/retest` ，调库框架会自动执行代码检查相关任务，快速完成验证。
* 在需要验证特定后端的用例，或本地缺乏特定后端的验证环境时，可以根据个人需求触发特殊调测指令，需要注意的是这些调测执行在**执行完成后不会打 `ci-pipeline-passed` 标签**，仍然需要执行 `/retest` 来完成验证并最终合入
* 如果出现打了 `ci-pipeline-passed` 标签仍然无法合入的问题，请执行 `/check-pr` 检查当前PR对合入条件的满足状态：
    * 如果缺少足够的 `approved`，请联系committer协助合入代码
    * 如果ci-bot告警未签署CLA协议，请完成签署后执行 `/check-cla`
    * 如果以上条件均已齐备仍未合入，先尝试执行 `/check-pr` 与 `check-cla`，如果仍然无效请联系管理员或提交issue

特殊调测指令请参见下表，指令内容与范围仍在继续添加中，如果有特定需求请提交issue：

| 后端\门禁阶段 | 代码检查 | 编译 | UT | ST(门禁level0级用例)  | ST(版本level1级用例) | ST(门禁&版本级全量执行) |
|---------------|-----------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------|
| 全部后端  | 全部工具：`/retest_check`</br>CodeCheck工具：`/retest_codecheck` || 全部UT：`/retest_ut`</br>CPP UT：`/retest_ut_cpp`</br>Python UT：`/retest_ut_python` ||| |
| CPU Linux |   | `/retest_compile_cpu_x86`</br>`/retest_compile_cpu_arm` | | `/retest_smoke_cpu_x86`</br>`/retest_smoke_cpu_x86_fullcase`（跑完所有用例才退出）</br>`/retest_smoke_cpu_arm`</br>`/retest_smoke_cpu_arm_fullcase`（跑完所有用例才退出） | `/retest_smoke_cpu_x86_level1`</br>`/retest_smoke_cpu_x86_level1_fullcase`（跑完所有用例才退出）</br>`/retest_smoke_cpu_arm_level1`</br>`/retest_smoke_cpu_arm_level1_fullcase`（跑完所有用例才退出） | |
| CPU Windows   |   | `/retest_compile_windows`  | | `/retest_smoke_cpu_windows`</br>`/retest_smoke_cpu_windows_fullcase`（跑完所有用例才退出）| `/retest_smoke_cpu_windows_level1`</br>`/retest_smoke_cpu_windows_level1_fullcase`（跑完所有用例才退出）  | |
| CPU MacOS |   | `/retest_compile_cpu_x86_macos`</br>`/retest_compile_cpu_arm_macos` | | `/retest_smoke_cpu_x86_macos`</br>`/retest_smoke_cpu_x86_macos_fullcase`（跑完所有用例才退出）</br>`/retest_smoke_cpu_arm_macos`</br>`/retest_smoke_cpu_arm_macos_fullcase`（跑完所有用例才退出） | `/retest_smoke_cpu_x86_macos_level1`</br>`/retest_smoke_cpu_x86_macos_level1_fullcase`（跑完所有用例才退出）</br>`/retest_smoke_cpu_arm_macos_level1`</br>`/retest_smoke_cpu_arm_macos_level1_fullcase`（跑完所有用例才退出） | |
| GPU   |   | `/retest_compile_gpu_cuda10`</br>`/retest_compile_gpu_cuda11`</br>`/retest_compile_gpu_cuda11_py39`</br>`/retest_compile_gpu_cuda11_gcc9` | | `/retest_smoke_gpu_cuda10`</br>`/retest_smoke_gpu_cuda10_fullcase`（跑完所有用例才退出）</br>`/retest_smoke_gpu_cuda11`</br>`/retest_smoke_gpu_cuda11_fullcase`（跑完所有用例才退出） | `/retest_smoke_gpu_cuda10_level1`</br>`/retest_smoke_gpu_cuda10_level1_fullcase`（跑完所有用例才退出）</br>`/retest_smoke_gpu_cuda11_level1`</br>`/retest_smoke_gpu_cuda11_level1_fullcase`（跑完所有用例才退出） | |
| Ascend 310|   | `/retest_compile_ascend310`| | `/retest_smoke_ascend310`  | 不区分门禁级与版本级   | 不区分门禁级与版本级|
| Ascend 910|   | `/retest_compile_ascend`   | | `/retest_smoke_ascend`</br>`/retest_smoke_ascend_fullcase`（跑完所有用例才退出）  | `/retest_smoke_ascend_level1`</br>`/retest_smoke_ascend_level1_fullcase`| |
| Lite IOS  |   | `/retest_compile_lite_ios` | ||| |
