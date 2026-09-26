# C07 · CoS

推荐顺序：导师相关前沿，先读后选择。

[上游仓库](https://github.com/baaivision/CoS) · [本地源码](../repositories/closed_loop/C07_CoS)

## 对应论文

- [Unveiling Chain of Step Reasoning for Vision-Language Models with Fine-grained Rewards](https://arxiv.org/abs/2509.19003)，NeurIPS 2025（官方仓库标注）。[下载的全文](../papers/closed_loop/cos.pdf)

## 为什么选择

CoS 有黄凯奇老师参与，研究细粒度步骤奖励与视觉语言推理的强化学习训练，适合学习感知理解与奖励监督之间的联系。

## 论文：要理解的方法与假设

步骤推理数据、process reward model、强化学习与推理时扩展；核对每个模块实际公开的代码和外部资源。

建议按以下入口追踪实现：

- [internvl/train/internvl_chat_prm.py](../repositories/closed_loop/C07_CoS/internvl/train/internvl_chat_prm.py)
- [internvl/train/internvl_chat_finetune.py](../repositories/closed_loop/C07_CoS/internvl/train/internvl_chat_finetune.py)
- [eval/vqa/score_with_prm.py](../repositories/closed_loop/C07_CoS/eval/vqa/score_with_prm.py)

## 代码：作者如何组织实现

训练脚本将 ModelArguments、DataTrainingArguments、LazySupervisedDataset 与训练器连接；PRM、SFT 和评估脚本分开。

### 沿这条路径读

PRM／SFT 数据配置 → LazySupervisedDataset → 多模态 token／标签 → 模型与 trainer；评分侧追踪 score_with_prm.py。

### 要掌握的编程方法与练习

整理图像、特殊 token、标签 mask 和 reward 分数的对应。根据实际脚本列出已公开训练阶段，不把所有优化脚本都视为同一 RL 算法。

## 学到什么程度

整理基座、数据、奖励模型和训练流程的对应关系，解释过程奖励与最终答案奖励各自的偏差。

## 算力与复现门槛

先做模型推理与小规模适配；八卡 4090 仍需按模型大小、视觉 token、序列长度和分片配置估算显存。

这里的视觉语言推理并不是物理动作闭环；问答正确率不能代替导航或操作成功率。外部基座、权重和数据单独提供。

## 带着什么问题读

奖励是否鼓励看似合理却缺少视觉依据的步骤？步骤监督提升是否能迁移到真实行动任务？

本卡中的学习目标与问题是为本资料库提出的建议，不是论文已经证明的结论。本次只核对资料和源码，未运行该项目训练。

[返回学习路线](../docs/学习路线与选题判断.md) · [资源总表](../docs/资源总表.md)

[论文阅读指南](../docs/论文阅读指南.md) · [代码阅读指南](../docs/代码阅读指南.md)
