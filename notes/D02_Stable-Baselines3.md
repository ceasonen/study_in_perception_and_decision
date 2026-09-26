# D02 · Stable-Baselines3

推荐顺序：核心工具，用于可靠实验基线。

[上游仓库](https://github.com/DLR-RM/stable-baselines3) · [本地源码](../repositories/decision/D02_Stable-Baselines3)

## 对应论文

- [Stable-Baselines3: Reliable Reinforcement Learning Implementations](https://jmlr.org/papers/v22/20-1364.html)，JMLR 22(268), 1–8, 2021。[下载的全文](../papers/decision/sb3.pdf)
- [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347)，arXiv 2017。[下载的全文](../papers/decision/ppo.pdf)
- [Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor](https://arxiv.org/abs/1801.01290)，ICML 2018。[下载的全文](../papers/decision/sac.pdf)

## 为什么选择

Stable-Baselines3 提供模块化强化学习实现，适合作为对照基线，并学习策略、buffer、环境封装与训练器的分工。

## 论文：要理解的方法与假设

把 CleanRL 中读懂的步骤映射到这里的模块；重点核对观测归一化、评估、保存和加载。

建议按以下入口追踪实现：

- [stable_baselines3/ppo/ppo.py](../repositories/decision/D02_Stable-Baselines3/stable_baselines3/ppo/ppo.py)
- [stable_baselines3/sac/sac.py](../repositories/decision/D02_Stable-Baselines3/stable_baselines3/sac/sac.py)
- [stable_baselines3/common/buffers.py](../repositories/decision/D02_Stable-Baselines3/stable_baselines3/common/buffers.py)

## 代码：作者如何组织实现

算法继承公共训练基类，策略、buffer、callback 与环境接口独立。PPO／SAC 的专用逻辑嵌入共享生命周期。

### 沿这条路径读

公开 learn 接口 → 公共采样流程 → buffer → PPO.train／SAC.train → 网络与优化器。把一次更新映射回 CleanRL 的单文件实现。

### 要掌握的编程方法与练习

画出算法类的继承与组合关系，说明新增一个 loss 应改专用算法还是公共基类。学会读模块化训练库和控制扩展范围。

## 学到什么程度

建立同一环境下的训练与独立评估流程，理解 vectorized environments 和 checkpoint 的边界。

## 算力与复现门槛

小任务可单卡或 CPU；增加并行环境会消耗 CPU。标准算法实现并不自动提供八卡 DDP。

框架不能替代问题定义；自定义观测、奖励与终止逻辑仍需你自己检查。避免把它的默认参数视为所有任务最优。

## 带着什么问题读

评估是否使用了训练时不可获得的信息？观测归一化统计在训练和测试之间如何管理？

本卡中的学习目标与问题是为本资料库提出的建议，不是论文已经证明的结论。本次只核对资料和源码，未运行该项目训练。

[返回学习路线](../docs/学习路线与选题判断.md) · [资源总表](../docs/资源总表.md)

[论文阅读指南](../docs/论文阅读指南.md) · [代码阅读指南](../docs/代码阅读指南.md)
