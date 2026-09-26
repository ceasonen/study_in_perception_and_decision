# D05 · TAPE

推荐顺序：导师相关，MAPPO／QMIX 后精读。

[上游仓库](https://github.com/LxzGordon/TAPE) · [本地源码](../repositories/decision/D05_TAPE)

## 对应论文

- [TAPE: Leveraging Agent Topology for Cooperative Multi-Agent Policy Gradient](https://arxiv.org/abs/2312.15667)，AAAI 2024, 38(16), 17496–17504。[下载的全文](../papers/decision/tape.pdf)

## 为什么选择

TAPE 有黄凯奇老师参与，把智能体拓扑与 coalition utility 引入策略学习，适合研究哪些其他智能体应影响本体策略更新。

## 论文：要理解的方法与假设

集中与分散更新的失配、协作目标和图结构；分别追踪 stochastic／deterministic 两套实现。

建议按以下入口追踪实现：

- [stochastic/src/learners/offpg_learner.py](../repositories/decision/D05_TAPE/stochastic/src/learners/offpg_learner.py)
- [deterministic/src/learners/policy_gradient_v2.py](../repositories/decision/D05_TAPE/deterministic/src/learners/policy_gradient_v2.py)
- [stochastic/runalgo.sh](../repositories/decision/D05_TAPE/stochastic/runalgo.sh)

## 代码：作者如何组织实现

作者保留 stochastic 和 deterministic 两个实现目录，分别有 learner、controller、网络与配置，适合通过与原基线的对照定位方法改动。

### 沿这条路径读

先看 stochastic 的 OffPGLearner，再看 deterministic 的 PGLearner_v2；追踪拓扑／邻接关系进入目标与策略更新的路径。

### 要掌握的编程方法与练习

只围绕拓扑相关张量做一页追踪笔记：创建位置、维度、使用位置与梯度路径。学会阅读基于他人框架改造的论文代码。

## 学到什么程度

能够说明一条图边在学习目标中意味着什么，梳理论文假设与实际图结构设置。

## 算力与复现门槛

小任务与少量图设置先单卡；八卡适合更多任务、图配置和独立重复。环境采样资源仍需考虑。

作者仓库基于 SMAC、DOP、PAC；拓扑影响学习不等同于自动提供视觉通信系统，也不保证跨任务通用。

## 带着什么问题读

协作图应该根据什么信息调整？观测错误是否通过图结构放大，或者能被局部协作目标减轻？

本卡中的学习目标与问题是为本资料库提出的建议，不是论文已经证明的结论。本次只核对资料和源码，未运行该项目训练。

[返回学习路线](../docs/学习路线与选题判断.md) · [资源总表](../docs/资源总表.md)

[论文阅读指南](../docs/论文阅读指南.md) · [代码阅读指南](../docs/代码阅读指南.md)
