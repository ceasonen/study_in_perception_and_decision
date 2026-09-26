# C08 · OpenPI

推荐顺序：前沿分支，确定机器人任务后进入。

[上游仓库](https://github.com/Physical-Intelligence/openpi) · [本地源码](../repositories/closed_loop/C08_OpenPI)

## 对应论文

- [π₀: A Vision-Language-Action Flow Model for General Robot Control](https://arxiv.org/abs/2410.24164)，arXiv 初版 2024。[下载的全文](../papers/closed_loop/pi0.pdf)
- [π₀.₅: a Vision-Language-Action Model with Open-World Generalization](https://arxiv.org/abs/2504.16054)，arXiv 初版 2025。[下载的全文](../papers/closed_loop/pi05.pdf)

## 为什么选择

OpenPI 的 π₀／π₀.₅ 将图像、语言和机器人状态映射到动作，适合建立视觉语言动作模型的结构性理解。

## 论文：要理解的方法与假设

视觉语言主干与动作专家、flow matching、数据 transforms、动作归一化和适配配置。

建议按以下入口追踪实现：

- [src/openpi/models/pi0.py](../repositories/closed_loop/C08_OpenPI/src/openpi/models/pi0.py)
- [src/openpi/training/config.py](../repositories/closed_loop/C08_OpenPI/src/openpi/training/config.py)
- [scripts/train.py](../repositories/closed_loop/C08_OpenPI/scripts/train.py)

## 代码：作者如何组织实现

TrainConfig 和 DataConfigFactory 管配置，transforms 接通机器人数据，Pi0 管模型，训练／服务／评估各有入口。

### 沿这条路径读

TrainConfig → 数据变换与归一化 → Pi0 的训练目标 → 优化器；推理侧图像／语言／状态 → 动作采样 → 反归一化 → 平台。

### 要掌握的编程方法与练习

写出一个 LIBERO 示例的数据契约，说明相机、状态与动作在每层的形状和单位。学会读可适配多平台模型的配置与接口设计。

## 学到什么程度

明确一个公开示例的输入与动作表示，先验证推理或适配流程，再讨论跨任务泛化。

## 算力与复现门槛

官方单卡估算：推理 >8GB、LoRA >22.5GB、全量 >70GB。4090 的 LoRA 余量小；同机可用 fsdp_devices 分片，当前不支持多节点训练。

依赖真实或成熟仿真机器人数据，源码不包含基础权重和全部数据。标准 OpenPI 学习路线不是在线 RL；动作与平台不匹配会直接阻碍迁移。

## 带着什么问题读

跨机器人动作空间如何对齐？语言理解、视觉定位和动作执行各自在失败中占多大作用？

本卡中的学习目标与问题是为本资料库提出的建议，不是论文已经证明的结论。本次只核对资料和源码，未运行该项目训练。

[返回学习路线](../docs/学习路线与选题判断.md) · [资源总表](../docs/资源总表.md)

[论文阅读指南](../docs/论文阅读指南.md) · [代码阅读指南](../docs/代码阅读指南.md)
