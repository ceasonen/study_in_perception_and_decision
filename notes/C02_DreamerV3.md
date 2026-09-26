# C02 · DreamerV3

推荐顺序：核心精读，世界模型与潜在决策。

[上游仓库](https://github.com/danijar/dreamerv3) · [本地源码](../repositories/closed_loop/C02_DreamerV3)

## 对应论文

- [Mastering Diverse Domains through World Models](https://arxiv.org/abs/2301.04104)，Nature 2025；arXiv 初版 2023。[下载的全文](../papers/closed_loop/dreamerv3.pdf)

## 为什么选择

DreamerV3 将观测、奖励与动力学建模到潜在状态，并在想象轨迹中学习策略，适合研究感知如何成为对行动有用的内部模型。

## 论文：要理解的方法与假设

RSSM、表示与动力学训练、潜在 rollout、价值和策略目标，以及不同量级任务的稳定化处理。

建议按以下入口追踪实现：

- [dreamerv3/agent.py](../repositories/closed_loop/C02_DreamerV3/dreamerv3/agent.py)
- [dreamerv3/rssm.py](../repositories/closed_loop/C02_DreamerV3/dreamerv3/rssm.py)
- [dreamerv3/configs.yaml](../repositories/closed_loop/C02_DreamerV3/dreamerv3/configs.yaml)

## 代码：作者如何组织实现

Agent 组织训练目标，RSSM／Encoder／Decoder 管潜在模型，embodied 组织环境、回放与运行；采用 JAX 的状态与随机数处理方式。

### 沿这条路径读

真实 batch → Encoder／RSSM → 表征与动力学目标 → imagined rollout → imag_loss／价值目标 → 参数更新。

### 要掌握的编程方法与练习

对比 PyTorch 可变对象与 JAX 显式参数／状态流，标出随机数、scan 和批时间轴。学会跨框架阅读训练实现。

## 学到什么程度

画出真实交互数据与想象轨迹各自在哪里使用，说明好重建与好决策之间可能存在的差异。

## 算力与复现门槛

先选较小配置和可部署的环境；八卡可支持并行任务或分布式实验，具体方式遵循本次下载版本。

作者维护的当前仓库说明它是基于 DreamerV2 的重新实现，与 Google／DeepMind 无关；使用 JAX，不能按 PyTorch 项目安装。当前 main 与原论文实验版本也可能不同。

## 带着什么问题读

潜在模型保留了哪些动作相关信息？想象误差如何累积，并影响长期策略选择？

本卡中的学习目标与问题是为本资料库提出的建议，不是论文已经证明的结论。本次只核对资料和源码，未运行该项目训练。

[返回学习路线](../docs/学习路线与选题判断.md) · [资源总表](../docs/资源总表.md)

[论文阅读指南](../docs/论文阅读指南.md) · [代码阅读指南](../docs/代码阅读指南.md)
