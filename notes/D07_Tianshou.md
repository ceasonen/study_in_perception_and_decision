# D07 · Tianshou

推荐顺序：RL infra 主线；读通 CleanRL 后进入，与 SB3 对照。

[上游仓库](https://github.com/thu-ml/tianshou) · [本地源码](../repositories/decision/D07_Tianshou)

## 对应论文

- [Tianshou: A Highly Modularized Deep Reinforcement Learning Library](https://jmlr.org/papers/v23/21-1127.html)，JMLR 23(267):1–6, 2022。[下载的全文](../papers/decision/tianshou.pdf)
- [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347)，arXiv 2017。[下载的全文](../papers/decision/ppo.pdf)
- [Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor](https://arxiv.org/abs/1801.01290)，ICML 2018。[下载的全文](../papers/decision/sac.pdf)

## 为什么选择

Tianshou 是面向算法研发的 PyTorch RL 基础设施。这里重点学习如何把环境交互、结构化数据、回放、动作生成、学习更新与训练调度拆成可组合的接口，再把自己的算法接进去。用户提供的本地源码已纳入决策分类，不重新覆盖为线上最新版。

## 论文：要理解的方法与假设

JMLR 2022 论文用于理解模块化基础设施与统一接口的设计动机；PPO／SAC 论文用于理解优化目标。当前源码 pyproject.toml 标记为 2.0.1，v2 已分离 Policy 和 Algorithm，不能把旧论文图、旧版 PPOPolicy 路径或 process_fn／learn／post_process_fn 接口直接当作当前实现。

建议按以下入口追踪实现：

- [test/discrete/test_ppo_discrete.py](../repositories/decision/D07_Tianshou/test/discrete/test_ppo_discrete.py)
- [examples/mujoco/mujoco_sac.py](../repositories/decision/D07_Tianshou/examples/mujoco/mujoco_sac.py)
- [tianshou/algorithm/algorithm_base.py](../repositories/decision/D07_Tianshou/tianshou/algorithm/algorithm_base.py)
- [tianshou/algorithm/modelfree/ppo.py](../repositories/decision/D07_Tianshou/tianshou/algorithm/modelfree/ppo.py)
- [tianshou/algorithm/modelfree/sac.py](../repositories/decision/D07_Tianshou/tianshou/algorithm/modelfree/sac.py)
- [tianshou/data/batch.py](../repositories/decision/D07_Tianshou/tianshou/data/batch.py)
- [tianshou/data/collector.py](../repositories/decision/D07_Tianshou/tianshou/data/collector.py)
- [tianshou/data/buffer/buffer_base.py](../repositories/decision/D07_Tianshou/tianshou/data/buffer/buffer_base.py)
- [tianshou/data/buffer/vecbuf.py](../repositories/decision/D07_Tianshou/tianshou/data/buffer/vecbuf.py)
- [tianshou/env/venvs.py](../repositories/decision/D07_Tianshou/tianshou/env/venvs.py)
- [tianshou/trainer.py](../repositories/decision/D07_Tianshou/tianshou/trainer.py)
- [test/base/test_collector.py](../repositories/decision/D07_Tianshou/test/base/test_collector.py)
- [test/base/test_buffer.py](../repositories/decision/D07_Tianshou/test/base/test_buffer.py)
- [CHANGELOG.md](../repositories/decision/D07_Tianshou/CHANGELOG.md)

## 代码：作者如何组织实现

Policy 管 forward、动作映射与探索；Algorithm 管数据预处理、网络更新和更新后处理；Collector 管环境交互、episode 与状态重置；Batch／ReplayBuffer 管字段、索引与采样；向量环境管多个 worker；Trainer 管采样和更新节奏、评估与日志。High-level API 在这些机制上组装实验。

### 沿这条路径读

先读 test/discrete/test_ppo_discrete.py：DiscreteActorPolicy + PPO → Collector／VectorReplayBuffer → algorithm.run_training(OnPolicyTrainerParams) → OnPolicyTrainer 的采集与更新 → Algorithm._update 中 buffer.sample、_preprocess_batch、_update_with_batch、_postprocess_batch → 清空当轮 on-policy buffer。再读 examples/mujoco/mujoco_sac.py：SACPolicy + SAC → warm-up collect → OffPolicyTrainer → 按采样量计算更新次数并反复采样 → 双 critic、actor、alpha 与目标网络更新。

### 要掌握的编程方法与练习

先做 Batch 字段与 shape 表、episode 边界表和 Policy／Algorithm 职责图；再读 test/base 的 buffer／collector 测试，学习用简单环境验证数据语义。按 RL 基础设施专题逐步添加 CPU CartPole 入口、独立日志目录和保存／恢复检查，最后才接自定义算法与视觉编码器。不要仅把所有对象封装进一个类。

## 学到什么程度

能够从 CartPole PPO 入口画出 Policy、Algorithm、Collector、Buffer、Trainer 的职责和数据流，解释 PPO 与 SAC 的采样／更新差异，再在自己的练习目录搭建最小训练入口。详细任务见[RL 基础设施专题](../docs/RL基础设施学习专题.md)。

## 算力与复现门槛

先用 CPU 或单张 GPU 与少量向量环境检查完整链路。8 张 4090 优先用于独立种子、不同配置与任务；采样吞吐常取决于 CPU 与环境速度。向量环境、异步采样、单机多 GPU 和跨机器分布式是不同机制，应分别测量。

本库保留用户下载的 master 工作文件快照、MIT 许可、示例和测试。未安装依赖或运行训练；基于源码的阅读分析不保证达到论文基准结果。Python 要求见 pyproject.toml（^3.11）；不同环境需另装 extras。训练入口中的 state_dict 保存也不能直接视为完整恢复环境、buffer、随机数与全部调度状态。

## 带着什么问题读

哪些逻辑必须留在算法里，哪些适合交给 Collector／Trainer？并行环境的 env_id、episode 边界与 RNN state 怎样对齐？terminated／truncated 分别影响 reset 和 bootstrap 的哪一步？提高采样吞吐时，是否同时改变了每个样本的更新次数？

本卡中的学习目标与问题是为本资料库提出的建议，不是论文已经证明的结论。本次只核对资料和源码，未运行该项目训练。

[返回学习路线](../docs/学习路线与选题判断.md) · [资源总表](../docs/资源总表.md)

[论文阅读指南](../docs/论文阅读指南.md) · [代码阅读指南](../docs/代码阅读指南.md)
