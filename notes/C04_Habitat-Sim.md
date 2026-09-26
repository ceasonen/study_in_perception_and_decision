# C04 · Habitat-Sim

推荐顺序：配套平台，重点理解接口。

[上游仓库](https://github.com/facebookresearch/habitat-sim) · [本地源码](../repositories/closed_loop/C04_Habitat-Sim)

## 对应论文

- [Habitat: A Platform for Embodied AI Research](https://arxiv.org/abs/1904.01201)，ICCV 2019。[下载的全文](../papers/closed_loop/habitat.pdf)
- [Habitat 2.0: Training Home Assistants to Rearrange their Habitat](https://arxiv.org/abs/2106.14405)，NeurIPS 2021。[下载的全文](../papers/closed_loop/habitat2.pdf)

## 为什么选择

Habitat-Sim 是 Habitat 的底层 3D 模拟器，提供传感器、渲染和物理交互。学习它能明确视觉观测到底如何产生。

## 论文：要理解的方法与假设

simulator／agent／sensor 的关系、渲染与物理步进；把模拟器职责与上层策略学习分开。

建议按以下入口追踪实现：

- [src/esp/sim/Simulator.cpp](../repositories/closed_loop/C04_Habitat-Sim/src/esp/sim/Simulator.cpp)
- [src_python/habitat_sim/agent/agent.py](../repositories/closed_loop/C04_Habitat-Sim/src_python/habitat_sim/agent/agent.py)
- [src/esp/sensor/Sensor.h](../repositories/closed_loop/C04_Habitat-Sim/src/esp/sensor/Sensor.h)

## 代码：作者如何组织实现

Python Agent 和配置连接传感器／动作，C++ Simulator 管场景和物理过程，中间有语言绑定。它主要是仿真基础设施。

### 沿这条路径读

Python 配置与 Agent 动作 → Simulator 步进 → 场景／传感器状态 → 渲染观测 → Python 返回值。

### 要掌握的编程方法与练习

用一张调用图划出 Python、C++ 和第三方引擎边界。第一轮跳过 deps 内部，只在具体问题需要时深入。学会阅读跨语言系统。

## 学到什么程度

能够描述一个动作到下一帧图像的数据链路，识别相机、坐标系和碰撞配置会怎样影响结果。

## 算力与复现门槛

GPU 主要用于渲染与部分模型计算；先用预编译包和小场景验证，源码编译需要 C++ 工具链。

上游依赖多个嵌套子模块，这次单独补齐；它们是源码依赖，不等于场景数据和已构建的模拟器。

## 带着什么问题读

观测退化能否由传感器参数控制？模拟与真实环境之间最需要关心哪些差异？

本卡中的学习目标与问题是为本资料库提出的建议，不是论文已经证明的结论。本次只核对资料和源码，未运行该项目训练。

[返回学习路线](../docs/学习路线与选题判断.md) · [资源总表](../docs/资源总表.md)

[论文阅读指南](../docs/论文阅读指南.md) · [代码阅读指南](../docs/代码阅读指南.md)
