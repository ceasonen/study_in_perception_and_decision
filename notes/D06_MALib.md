# D06 · MALib

推荐顺序：进阶工具，种群与分布式训练。

[上游仓库](https://github.com/sjtu-marl/malib) · [本地源码](../repositories/decision/D06_MALib)

## 对应论文

- [MALib: A Parallel Framework for Population-based Multi-agent Reinforcement Learning](https://jmlr.org/papers/v24/22-0169.html)，JMLR 24(150), 1–12, 2023。[下载的全文](../papers/decision/malib.pdf)
- [Distributed Deep Reinforcement Learning: A Survey and A Multi-Player Multi-Agent Learning Toolbox](https://arxiv.org/abs/2212.00253)，Machine Intelligence Research 21(3), 411–430, 2024；下载 arXiv 2022 版本。[下载的全文](../papers/decision/distributed_rl.pdf)

## 为什么选择

MALib 展示种群学习、自博弈与策略空间响应等训练范式，帮助区分单个策略更新、策略种群演化和系统并行。

## 论文：要理解的方法与假设

任务分发、actor／evaluator／learner、数据服务与 PSRO；先读小型博弈示例。

建议按以下入口追踪实现：

- [examples/run_psro.py](../repositories/decision/D06_MALib/examples/run_psro.py)
- [examples/run_gym.py](../repositories/decision/D06_MALib/examples/run_gym.py)
- [malib](../repositories/decision/D06_MALib/malib)

## 代码：作者如何组织实现

示例创建 scenario，scenario 组织策略学习与评估，分布式 workers 和数据服务承担采样、训练及调度。

### 沿这条路径读

run_psro.py → scenario 设置 → 任务分发 → rollout／learner → 策略评估 → 种群更新。

### 要掌握的编程方法与练习

画出函数调用和跨进程消息两种不同的边，列出模型参数与采样数据各自何时传输。学会读分布式训练系统的职责和资源配置。

## 学到什么程度

画出训练任务与评估任务之间的数据和参数流，理解为什么赢当前对手不等于对所有对手稳健。

## 算力与复现门槛

小型博弈起步不需要八卡；随后用多卡支持多个学习器或独立策略。Ray 和 CPU／内存资源要与 GPU 一起规划。

这是上海交大等作者的独立项目，不是自动化所 M2RL 的代码；环境栈较旧，官方说明主要支持 Linux。

## 带着什么问题读

对手种群的覆盖程度如何影响泛化？系统吞吐和学习效率分别用什么量度？

本卡中的学习目标与问题是为本资料库提出的建议，不是论文已经证明的结论。本次只核对资料和源码，未运行该项目训练。

[返回学习路线](../docs/学习路线与选题判断.md) · [资源总表](../docs/资源总表.md)

[论文阅读指南](../docs/论文阅读指南.md) · [代码阅读指南](../docs/代码阅读指南.md)
