# D03 · MAPPO

推荐顺序：核心精读，多智能体首个强基线。

[上游仓库](https://github.com/marlbenchmark/on-policy) · [本地源码](../repositories/decision/D03_MAPPO)

## 对应论文

- [The Surprising Effectiveness of PPO in Cooperative, Multi-Agent Games](https://arxiv.org/abs/2103.01955)，NeurIPS 2022；arXiv 初版 2021。[下载的全文](../papers/decision/mappo.pdf)

## 为什么选择

MAPPO 适合把单智能体 PPO 扩展到团队协作，建立集中训练分散执行的直觉，理解局部 actor 与全局 critic 的区别。

## 论文：要理解的方法与假设

共享或独立策略、集中价值网络、循环状态、死亡掩码、值归一化与小批量更新。

建议按以下入口追踪实现：

- [onpolicy/algorithms/r_mappo/r_mappo.py](../repositories/decision/D03_MAPPO/onpolicy/algorithms/r_mappo/r_mappo.py)
- [onpolicy/runner/shared/mpe_runner.py](../repositories/decision/D03_MAPPO/onpolicy/runner/shared/mpe_runner.py)
- [onpolicy/config.py](../repositories/decision/D03_MAPPO/onpolicy/config.py)

## 代码：作者如何组织实现

Runner 管环境交互，R_MAPPO 管参数更新，策略与 buffer 分开；shared／separated runner 区分策略共享方式。

### 沿这条路径读

MPERunner → 局部 obs／集中 critic 输入 → 动作采样 → 环境 step → buffer → return／优势 → R_MAPPO 更新。

### 要掌握的编程方法与练习

列出时间、并行环境、智能体和特征四个轴，跟踪 flatten 与 reshape。学会读多智能体循环状态、mask 和批处理。

## 学到什么程度

从较简单 MPE 协作任务入手，能够列清 actor／critic 各自看到什么，以及部署时能否获得这些输入。

## 算力与复现门槛

策略模型通常不大；CPU 采样、并行环境和多个种子比直接八卡同步更值得先优化。

SMAC 需要额外的游戏和环境；此仓库的典型任务是状态向量输入，不应称为已经实现了视觉感知决策闭环。

## 带着什么问题读

集中 critic 的改进依赖什么额外信息？观测缺失后性能变化来自感知、记忆还是协调？

本卡中的学习目标与问题是为本资料库提出的建议，不是论文已经证明的结论。本次只核对资料和源码，未运行该项目训练。

[返回学习路线](../docs/学习路线与选题判断.md) · [资源总表](../docs/资源总表.md)

[论文阅读指南](../docs/论文阅读指南.md) · [代码阅读指南](../docs/代码阅读指南.md)
