# D01 · CleanRL

推荐顺序：核心精读，逐行理解 PPO／SAC。

[上游仓库](https://github.com/vwxyzjn/cleanrl) · [本地源码](../repositories/decision/D01_CleanRL)

## 对应论文

- [CleanRL: High-quality Single-file Implementations of Deep Reinforcement Learning Algorithms](https://jmlr.org/papers/v23/21-1342.html)，JMLR 23(274), 1–18, 2022。[下载的全文](../papers/decision/cleanrl.pdf)
- [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347)，arXiv 2017。[下载的全文](../papers/decision/ppo.pdf)
- [Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor](https://arxiv.org/abs/1801.01290)，ICML 2018。[下载的全文](../papers/decision/sac.pdf)

## 为什么选择

CleanRL 的单文件实现适合你补齐算法到程序的细节：同一文件能看到采样、优势估计、更新、日志与评估。

## 论文：要理解的方法与假设

PPO 的概率比与 GAE；SAC 的双 Q、目标网络、重参数化和熵温度；核对环境终止与截断处理。

建议按以下入口追踪实现：

- [cleanrl/ppo.py](../repositories/decision/D01_CleanRL/cleanrl/ppo.py)
- [cleanrl/sac_continuous_action.py](../repositories/decision/D01_CleanRL/cleanrl/sac_continuous_action.py)
- [cleanrl/ppo_atari.py](../repositories/decision/D01_CleanRL/cleanrl/ppo_atari.py)

## 代码：作者如何组织实现

单文件依次包含 Args、环境工厂、网络与训练主循环，重复部分有意留在各算法文件中，便于看到完整流程。

### 沿这条路径读

Args → make_env → Agent／Actor／SoftQNetwork → rollout 或 replay → 目标估计 → loss → optimizer → 日志与评估。

### 要掌握的编程方法与练习

按数据生命周期给 PPO 文件分块，逐处标注 detach／no_grad、终止 mask 和 optimizer 更新。学会写一个可解释的最小训练程序。

## 学到什么程度

对一个熟悉的小环境解释完整训练循环，并能定位一次训练不稳定是数据、更新还是评估造成。

## 算力与复现门槛

经典控制任务可用 CPU／单卡；八卡最先用于独立种子和任务，单文件示例不应一律视为多卡同步实现。

这是参考实现，不是 PPO／SAC 论文作者原始代码；不同环境变体、实现版本及依赖要求应分别检查。

## 带着什么问题读

损失下降为何不保证回报上升？改网络与改 rollout 长度，分别改变了哪些条件？

本卡中的学习目标与问题是为本资料库提出的建议，不是论文已经证明的结论。本次只核对资料和源码，未运行该项目训练。

[返回学习路线](../docs/学习路线与选题判断.md) · [资源总表](../docs/资源总表.md)

[论文阅读指南](../docs/论文阅读指南.md) · [代码阅读指南](../docs/代码阅读指南.md)
