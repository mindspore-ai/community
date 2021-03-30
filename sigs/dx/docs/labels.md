# The Issue/PR Label List

| Labels                  | Type                 | SubType             | Source nodes                 | Explanation in Chinese        | Explanation in English                                        |
|-------------------------|----------------------|---------------------|-------------------------------|--------------------------|----------------------------------------------------------|
|                         |                      |                     | ccsrc                         | c++代码                    | c++ code                                                 |
| comp/data               | comp                 | data                | -- minddata                   | data内部实现                 | data internal implementation                             |
| comp/parallel           | comp                 | parallel            | -- frontend -- parallel       | 对内实现                     | parallel internal implementation                         |
| comp/optimizer          | comp                 | optimizer           | -- frontend -- optimizer      | 硬件无关优化                   | Hardware independent optimization                        |
| comp/pynative           | comp                 | pynative            | -- pipeline -- pynative       | 动态图                      | Dynamic diagram                                          |
| comp/kernel             | comp                 | kernel              | -- beckend -- kernel_compiler | 算子内核 编译                  | Operator kernel, Compilation                             |
| comp/runtime            | comp                 | runtime             | -- runtime                    | 运行时                      | runtime                                                  |
| comp/device             | comp                 | device              | -- runtime - device           | 各类硬件操作封装                 | hardware operation package                               |
| comp/pipeline           | comp                 | pipeline            | -- pipeline -- jit            | 静态图                      | Static diagram                                           |
| comp/parser             | comp                 | parser              | -- pipeline -- jit - parse    | py-c++转换                 | Py-c + + conversion                                      |
| comp/optimizer          | comp                 | optimizer           | -- beckend -- optimizer       | 硬件相关优化                   | Hardware dependent optimization                          |
| comp/cxx-api            | comp                 | cxx-api             | --cxx_api                     | c++ API                  | c++ API                                                  |
| comp/debug              | comp                 | debug               | --debug                       | 调试功能 （易用性）               | Debugging function (ease of use)                         |
| comp/profiler           | comp                 | profiler            | --profiler                    | 性能统计                     | Performance statistics                                   |
| comp/ps                 | comp                 | ps                  | --ps                          | 参数服务器                    | Parameter server                                         |
| comp/pybind-api         | comp                 | pybind-api          | --pybind_api                  | c++调用py api              | Calling python API with C + +                            |
| comp/transform          | comp                 | transform           | --transform                   | mindspore cann onnx格式转换  | Mindpool, cann and onnx format conversion                |
| comp/vm                 | comp                 | vm                  | --vm                          | 硬件无关/相关优化转换              | Hardware independent / dependent optimization conversion |
| comp/py-com             | comp                 | py-com              | communication                 | communication python对外接口 | Communication Python external interface                  |
| comp/py-compression     | comp                 | py-compression      | compression                   | compression python对外接口   | compression Python external interface                    |
| comp/py-core            | comp                 | py-core             | core                          | core python对外接口          | core Python external interface                           |
| comp/ir                 | comp                 | ir                  | -- ir                         | 图定义                      | Graph definition                                         |
| comp/py-data            | comp                 | py-data             | dataset                       | data的python对外接口          | data Python external interface                           |
| comp/py-explainer       | comp                 | py-explainer        | explainer                     | 可解释python对外接口            | Interpretable Python external interface                  |
| comp/graph-utils        | comp                 | graph-utils         | graph_utils                   |                          |                                                          |
| comp/infer              | comp                 | infer               | lite                          |                          |                                                          |
| comp/mindrecord         | comp                 | mindrecord          | mindrecord                    | data的py对外接口 数据结构         | Python external interface data， data structure           |
| comp/api                | comp                 | api                 | nn                            |                          |                                                          |
| comp/numpy              | comp                 | numpy               | numpy                         |                          |                                                          |
| comp/operator           | comp                 | operator            | ops                           | 算子相关                     | Operator correlation                                     |
| comp/py-parallel        | comp                 | py-parallel         | parallel                      | py对外接口                   | Parallel Python external interface                       |
| comp/py-profiler        | comp                 | py-profiler         | profiler                      |                          |                                                          |
| comp/train              | comp                 | train               | train                         | 训练接口                     | Training interface                                       |
| comp/build-install      | comp                 | build-install       | build.sh                      | 构建脚本                     | Build script                                             |
| comp/mindzoo            | comp                 | mindzoo             | model_zoo                     | model zoo                | model zoo                                                |
| comp/checkpoint         | comp                 | checkpoint          |                               |                          |                                                          |
| comp/example            | comp                 | example             |                               |                          |                                                          |
| comp/environment        | comp                 | environment         |                               |                          |                                                          |
| comp/ci                 | comp                 | ci                  |                               |                          |                                                          |
| comp/ad                 | comp                 | ad                  |                               |                          |                                                          |
| comp/log                | comp                 | log                 |                               |                          |                                                          |
| device/gpu              | device               | gpu                 |                               | 在gpu设备上                  | on gpu device                                            |
| device/cpu              | device               | cpu                 |                               | 在cpu设备上                  | on cpu device                                            |
| device/ascend           | device               | ascend              |                               | 在ascend设备上               | on ascend device                                         |
| sig/frontend            | sig                  | FrontEnd            |                               | FrontEnd SIG             | FrontEnd SIG                                             |
| sig/compiler            | sig                  | Compiler            |                               | Compiler SIG             | Compiler SIG                                             |
| sig/executor            | sig                  | Executor            |                               | Executor SIG             | Executor SIG                                             |
| sig/modelzoo            | sig                  | ModelZoo            |                               | ModelZoo SIG             | ModelZoo SIG                                             |
| sig/data                | sig                  | Data                |                               | Data SIG                 | Data SIG                                                 |
| sig/graph-engine        | sig                  | GraphEngine         |                               | GraphEngine SIG          | GraphEngine SIG                                          |
| sig/visualization       | sig                  | Visualization       |                               | Visualization SIG        | Visualization SIG                                        |
| sig/security            | sig                  | Security            |                               | Security SIG             | Security SIG                                             |
| sig/akg                 | sig                  | AKG                 |                               | AKG SIG                  | AKG SIG                                                  |
| sig/mslite              | sig                  | MSLITE              |                               | MSLITE SIG               | MSLITE SIG                                               |
| sig/mdp                 | sig                  | MDP                 |                               | MDP SIG                  | MDP SIG                                                  |
| sig/parallel            | sig                  | Parallel            |                               | Parallel SIG             | Parallel SIG                                             |
| sig/adaptivetraining    | sig                  | AdaptiveTraining    |                               | AdaptiveTraining SIG     | AdaptiveTraining SIG                                     |
| sig/serving             | sig                  | Serving             |                               | Serving SIG              | Serving SIG                                              |
| sig/DX                  | sig                  | DevelopereXperience |                               | DevelopereXperience SIG  | DevelopereXperience SIG                                  |
| kind/bug                | kind                 | bug                 |                               | 类型 BUG                   | kind: bug                                                |
| kind/trustworthiness    | kind                 | trustworthiness     |                               | 可信计算                     | kind: trustworthiness                                    |
| kind/security           | kind                 | security            |                               | 类型 security              | kind: security                                           |
| kind/roadmap            | kind                 | roadmap             |                               | 对应图                      | kind:roadmap                                             |
| kind/reliability        | kind                 | reliability         |                               | 可靠性                      | kind:reliability                                         |
| kind/question           | kind                 | question            |                               | 类型 question              | kind:question                                            |
| kind/mindless           | kind                 | mindless            |                               |                          |                                                          |
| kind/maintenance        | kind                 | maintenance         |                               |                          |                                                          |
| kind/generality         | kind                 | generality          |                               |                          |                                                          |
| kind/function           | kind                 | function            |                               | 功能                       | kind:function                                            |
| kind/feature            | kind                 | feature             |                               | 类型 feature               | kind:feature                                             |
| kind/task               | kind                 | task                |                               | 类型 task                  | kind:task                                                |
| kind/enhancement        | kind                 | enhancement         |                               | 类型 enhancement           | kind:enhancement                                         |
| kind/docs               | kind                 | docs                |                               | 类型 docs                  | kind:docs                                                |
| kind/testing            | kind                 | testing             |                               | 类型 test                  | kind:test                                                |
| kind/performance        | kind                 | performance         |                               | 类型 performance           | kind:performance                                         |
| kind/discussion         | kind                 | discussion          |                               | 类型 discussion            | kind:discussion                                          |
| stat/RFC                | stat                 | RFC                 |                               | 新 feature                | new feature                                              |
| stat/wait-response      | stat                 | wait-response       |                               | 等待回复                     | waiting response                                         |
| stat/need-help          | stat                 | need-help           |                               | 寻求社区贡献                   | contributor welcome                                      |
| stat/waiting-mindsporer | stat                 | waiting-mindsporer  |                               | 等待开发者                    | waiting mindsporer                                       |
| stat/stall              | stat                 | stall               |                               | 冻结                       | stall                                                    |
| stat/WIP                | stat                 | WIP                 |                               | work in process          | work in process                                          |
| stat/duplicate          | stat                 | duplicate           |                               | 重复                       | duplicate                                                |
| stat/help-wanted        | stat                 | help-wanted         |                               | help wanted              | help wanted                                              |
| stat/invalid            | stat                 | invalid             |                               | 不合法                      | invalid                                                  |
| stat/need-squash        | stat                 | need-squash         |                               | need squash              | need squash                                              |
| stat/need-update        | stat                 | need-update         |                               | need squash              | need squash                                              |
| stat/suprceded          | stat                 | suprceded           |                               | suprceded                | suprceded                                                |
| stat/wontfix            | stat                 | wontfix             |                               | wontfix                  | wontfix                                                  |
| env/windows             | env                  | windows             |                               | 环境：windows               | Environment: Windows                                     |
| env/macos               | env                  | macos               |                               | 环境：Macos                 | Environment: Macos                                       |
| env/linux               | env                  | linux               |                               | 环境：Linux                 | Environment: Linux                                       |
| env/other               | env                  | other               |                               | 环境：other                 | Environment: Other                                       |
| mind/1.0.0              | mind                 | 1.0.0               |                               | 版本号:1.0.0                | version:1.0.0                                            |
| mind/0.7.0-beta         | mind                 | 0.7.0-beta          |                               | 版本号:0.7.0-beta           | version:0.7.0-beta                                       |
| mind/0.5.0-beta         | mind                 | 0.5.0-beta          |                               | 版本号:0.5.0-beta           | version:0.5.0-beta                                       |
| mind/0.3.0-alpha        | mind                 | 0.3.0-alpha         |                               | 版本号:0.3.0-beta           | version:0.3.0-beta                                       |
| mind/0.6.0-beta         | mind                 | 0.6.0-beta          |                               | 版本号:0.6.0-beta           | version:0.6.0-beta                                       |
| Reoccur/Occasionally    | Reoccur              | Occasionally        |                               | 重新出现                     | Reappear                                                 |
| usability/other         | usability            | other               |                               | 易用性：其他方面                 | usability:other                                          |
| usability/api           | usability            | api                 |                               | 易用性：api                  | usability:api                                            |
| usability/modelzoo      | usability            | modelzoo            |                               | 易用性：mindzoo              | usability:mindzoo                                        |
| usability/web/doc       | usability            | web/doc             |                               | 易用性：web/doc              | usability:web/doc                                        |
| usability/mi            | usability            | mi                  |                               | 易用性：mi                   | usability:mi                                             |
| usability/vm            | usability            | vm                  |                               | 易用性：vm                   | usability:vm                                             |
| usability               | usability            |                     |                               |                          |                                                          |
| usability-api           | usability-api        |                     |                               |                          |                                                          |
| usability-modelzoo      | usability-modelzoo   |                     |                               |                          |                                                          |
| usability-web/doc       | usability-web/doc    |                     |                               |                          |                                                          |
| usability-vm            | usability-vm         |                     |                               |                          |                                                          |
| usability-mi            | usability-mi         |                     |                               |                          |                                                          |
| good first issue        | good first issue     |                     |                               | good first issue         | good first issue                                         |
| mindspore-assistant     | mindspore-assistant  |                     |                               | mindspore 助手             | mindspore assistant                                      |
| mindspore-cla/no        | mindspore-cla/no     |                     |                               | 签署CLA:否                  | Signing CLA: no                                          |
| mindspore-cla/yes       | mindspore-cla/yes    |                     |                               | 签署CLA:是                  | Signing CLA: yes                                         |
| mindspore-contrib       | mindspore-contrib    |                     |                               | 贡献                       | contribution                                             |
| approved                | approved             |                     |                               | pr标签: 批准                 | PR label: approved                                       |
| ci-pipeline-failed      | ci-pipeline-failed   |                     |                               | pr标签 失败                  | PR label: failed                                         |
| ci-pipeline-passed      | ci-pipeline-passed   |                     |                               | pr标签 通过                  | PR label: passed                                         |
| ci-pipeline-passed-t    | ci-pipeline-passed-t |                     |                               | pr标签 通过                  | PR label: passed                                         |
| ci-pipeline-running     | ci-pipeline-running  |                     |                               | pr标签 运行中                 | PR label: running                                        |
