# C01 · DrQ-v2

推荐顺序：核心精读，最推荐的首个视觉决策项目。

[上游仓库](https://github.com/facebookresearch/drqv2) · [本地源码](../repositories/closed_loop/C01_DrQ-v2)

## 对应论文

- [Mastering Visual Continuous Control: Improved Data-Augmented Reinforcement Learning](https://arxiv.org/abs/2107.09645)，ICLR 2022；arXiv 初版 2021。[下载的全文](../papers/closed_loop/drqv2.pdf)

## 为什么选择

DrQ-v2 从像素观测学习连续动作控制，结构相对简洁，是把视觉编码器、增强、经验回放与策略学习连起来的好起点。

## 论文：要理解的方法与假设

随机位移增强、卷积编码器、off-policy 更新、探索噪声与 replay buffer；追踪增强后观测进入 Q 和 actor 的路径。

建议按以下入口追踪实现：

- [drqv2.py](../repositories/closed_loop/C01_DrQ-v2/drqv2.py)
- [train.py](../repositories/closed_loop/C01_DrQ-v2/train.py)
- [replay_buffer.py](../repositories/closed_loop/C01_DrQ-v2/replay_buffer.py)

## 代码：作者如何组织实现

Workspace 管生命周期，DrQV2Agent 管学习，Encoder／Actor／Critic 封装网络，replay_buffer.py 管采样。

### 沿这条路径读

Workspace → 环境图像与动作 → replay → RandomShiftsAug／Encoder → Critic 更新 → Actor 更新 → target 更新。

### 要掌握的编程方法与练习

标出每个 optimizer 包含哪些参数、encoder 在什么更新中收到梯度。学会检查共享编码器与 actor–critic 的更新边界。

## 学到什么程度

读懂一个 DeepMind Control 视觉任务的完整训练流程，并能解释同一任务的状态输入与像素输入区别。

## 算力与复现门槛

从单卡任务开始，八卡优先分配给独立任务、种子或配置；训练时间以实际任务和采样吞吐为准。

上游已归档；需要 MuJoCo／dm_control 和相应渲染环境。论文中的典型耗时不是你服务器的速度保证。

## 带着什么问题读

增强为什么有助于样本效率？随机位移会不会丢失某些任务必需的位置信息？

本卡中的学习目标与问题是为本资料库提出的建议，不是论文已经证明的结论。本次只核对资料和源码，未运行该项目训练。

[返回学习路线](../docs/学习路线与选题判断.md) · [资源总表](../docs/资源总表.md)

[论文阅读指南](../docs/论文阅读指南.md) · [代码阅读指南](../docs/代码阅读指南.md)
