# D04 · PyMARL

推荐顺序：核心对照，价值分解视角。

[上游仓库](https://github.com/oxwhirl/pymarl) · [本地源码](../repositories/decision/D04_PyMARL)

## 对应论文

- [QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning](https://arxiv.org/abs/1803.11485)，ICML 2018。[下载的全文](../papers/decision/qmix.pdf)

## 为什么选择

PyMARL 中的 QMIX 便于理解团队回报如何分配到个体动作价值，并与 MAPPO 的策略梯度路线形成对照。

## 论文：要理解的方法与假设

单调 mixing network、全局状态条件化、局部 Q 网络、序列回放与训练目标。

建议按以下入口追踪实现：

- [src/modules/mixers/qmix.py](../repositories/decision/D04_PyMARL/src/modules/mixers/qmix.py)
- [src/learners/q_learner.py](../repositories/decision/D04_PyMARL/src/learners/q_learner.py)
- [src/controllers/basic_controller.py](../repositories/decision/D04_PyMARL/src/controllers/basic_controller.py)

## 代码：作者如何组织实现

controller 选动作，runner 采样 episode，EpisodeBatch 保存序列，QLearner 更新个体网络与 QMixer。

### 沿这条路径读

环境局部观测 → BasicMAC → 个体 Q → 动作 → EpisodeBatch → QLearner → QMixer → TD 目标。

### 要掌握的编程方法与练习

整理在线网络与 target 网络的同步，画出 episode mask 和填充位置。学会读序列 replay 与联合价值训练。

## 学到什么程度

能够解释单调性为何帮助分散执行，同时指出哪些联合价值关系无法由这种约束充分表示。

## 算力与复现门槛

先单卡加足够 CPU 采样；八卡用于任务和种子对照。原始 SMAC 训练链路的版本与场景需要固定。

原始代码与游戏依赖较旧；SMAC／SMACv2 与游戏版本差异会影响比较，不混用不同环境的胜率。

## 带着什么问题读

协作失败是表示约束、探索不足，还是个体局部信息不足？与 MAPPO 比较时哪些条件必须一致？

本卡中的学习目标与问题是为本资料库提出的建议，不是论文已经证明的结论。本次只核对资料和源码，未运行该项目训练。

[返回学习路线](../docs/学习路线与选题判断.md) · [资源总表](../docs/资源总表.md)

[论文阅读指南](../docs/论文阅读指南.md) · [代码阅读指南](../docs/代码阅读指南.md)
