# C03 · Habitat-Lab

推荐顺序：进阶平台，先确定导航或操作任务。

[上游仓库](https://github.com/facebookresearch/habitat-lab) · [本地源码](../repositories/closed_loop/C03_Habitat-Lab)

## 对应论文

- [Habitat: A Platform for Embodied AI Research](https://arxiv.org/abs/1904.01201)，ICCV 2019。[下载的全文](../papers/closed_loop/habitat.pdf)
- [Habitat 2.0: Training Home Assistants to Rearrange their Habitat](https://arxiv.org/abs/2106.14405)，NeurIPS 2021。[下载的全文](../papers/closed_loop/habitat2.pdf)

## 为什么选择

Habitat-Lab 将任务、数据、策略训练与评估组织起来，适合学习视觉导航、记忆与长时程决策如何形成完整实验。

## 论文：要理解的方法与假设

episode、sensor、task、measure 和训练器接口；区分任务逻辑、策略模型与底层模拟器。

建议按以下入口追踪实现：

- [habitat-lab/habitat/core/env.py](../repositories/closed_loop/C03_Habitat-Lab/habitat-lab/habitat/core/env.py)
- [habitat-baselines/habitat_baselines/rl/ppo/ppo.py](../repositories/closed_loop/C03_Habitat-Lab/habitat-baselines/habitat_baselines/rl/ppo/ppo.py)
- [README.md](../repositories/closed_loop/C03_Habitat-Lab/README.md)

## 代码：作者如何组织实现

Env 管 episode 与任务，传感器和指标通过接口接入，baselines 中的 PPO 与 runner 负责学习。任务平台与算法库分层。

### 沿这条路径读

配置 → Env.reset → sensors／task observations → 策略 → Env.step → measures／reward → 训练或评估。

### 要掌握的编程方法与练习

整理一次 step 返回值是由哪些层构成，区别成功指标和训练奖励。学会读任务平台的插件接口与配置组合。

## 学到什么程度

理解一个导航任务的观测、动作、终止与成功指标，能解释场景泛化与同场景测试的区别。

## 算力与复现门槛

八卡可用于导航训练，但 CPU、场景加载、渲染吞吐和数据存储可能成为主要瓶颈。

Lab 与 Sim 的版本必须匹配；普通源码不包含全部场景。HM3D／Matterport3D 等资源可能要求申请或同意条款。

## 带着什么问题读

策略是否依赖训练场景记忆？视觉信息、深度信息与历史记忆分别解决了哪些困难？

本卡中的学习目标与问题是为本资料库提出的建议，不是论文已经证明的结论。本次只核对资料和源码，未运行该项目训练。

[返回学习路线](../docs/学习路线与选题判断.md) · [资源总表](../docs/资源总表.md)

[论文阅读指南](../docs/论文阅读指南.md) · [代码阅读指南](../docs/代码阅读指南.md)
