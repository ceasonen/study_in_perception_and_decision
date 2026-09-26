# C05 · ACT

推荐顺序：模仿学习路线首个项目。

[上游仓库](https://github.com/tonyzhaozh/act) · [本地源码](../repositories/closed_loop/C05_ACT)

## 对应论文

- [Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware](https://arxiv.org/abs/2304.13705)，RSS 2023。[下载的全文](../papers/closed_loop/act.pdf)

## 为什么选择

ACT 通过视觉条件和动作块学习操作，结构较清楚，可以学习示范、历史与执行动作之间的关系，补充强化学习之外的决策范式。

## 论文：要理解的方法与假设

条件 VAE、动作块、temporal ensembling、示范数据和闭环执行；理解为什么预测多步动作能降低逐步误差。

建议按以下入口追踪实现：

- [policy.py](../repositories/closed_loop/C05_ACT/policy.py)
- [imitate_episodes.py](../repositories/closed_loop/C05_ACT/imitate_episodes.py)
- [detr/models/detr_vae.py](../repositories/closed_loop/C05_ACT/detr/models/detr_vae.py)

## 代码：作者如何组织实现

imitate_episodes.py 分别组织训练与 eval，ACTPolicy 负责策略封装，DETRVAE 模型在 detr 子目录，数据处理通过 utils 接入。

### 沿这条路径读

示范 batch → forward_pass／ACTPolicy → DETRVAE → 重建和 KL 目标 → optimizer；eval_bc 中再追踪动作块与 temporal aggregation。

### 要掌握的编程方法与练习

列出训练和推理两条 forward 路径的不同输入，核对动作归一化与反归一化。学会读条件生成策略及闭环评估代码。

## 学到什么程度

在官方仿真任务中理解数据生成、训练、执行和成功率评估，区分训练损失与真正完成任务。

## 算力与复现门槛

先单卡做一个仿真任务，八卡用于多个条件和任务；真实 ALOHA 实验还需要机器人与操作数据。

ACT 属于模仿学习，不是在线强化学习；低训练误差不能保证分布外状态下的稳定控制。

## 带着什么问题读

动作块长度怎样影响反馈响应？遇到未见过的扰动时，策略如何从错误状态恢复？

本卡中的学习目标与问题是为本资料库提出的建议，不是论文已经证明的结论。本次只核对资料和源码，未运行该项目训练。

[返回学习路线](../docs/学习路线与选题判断.md) · [资源总表](../docs/资源总表.md)

[论文阅读指南](../docs/论文阅读指南.md) · [代码阅读指南](../docs/代码阅读指南.md)
