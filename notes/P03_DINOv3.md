# P03 · DINOv3

推荐顺序：进阶，与 DINOv2 对照阅读。

[上游仓库](https://github.com/facebookresearch/dinov3) · [本地源码](../repositories/perception/P03_DINOv3)

## 对应论文

- [DINOv3](https://arxiv.org/abs/2508.10104)，arXiv 2025 technical report。[下载的全文](../papers/perception/dinov3.pdf)

## 为什么选择

DINOv3 展示视觉基础表征的进一步发展，尤其适合观察密集特征稳定性和尺度变化。选它是为了建立当前表征方法的视野。

## 论文：要理解的方法与假设

理解 Gram anchoring 为什么加入、约束什么，以及密集特征与图像级性能之间的关系。

建议按以下入口追踪实现：

- [dinov3/train/ssl_meta_arch.py](../repositories/perception/P03_DINOv3/dinov3/train/ssl_meta_arch.py)
- [dinov3/loss/gram_loss.py](../repositories/perception/P03_DINOv3/dinov3/loss/gram_loss.py)
- [dinov3/models/vision_transformer.py](../repositories/perception/P03_DINOv3/dinov3/models/vision_transformer.py)

## 代码：作者如何组织实现

SSLMetaArch 组织多个学习目标；GramLoss 单独封装特征结构约束，视觉骨干和训练配置分离。

### 沿这条路径读

DinoVisionTransformer → 学生与教师特征 → GramLoss → 组合训练损失。与 DINOv2 比较接口，而不是重新逐行阅读所有公共模块。

### 要掌握的编程方法与练习

找到一个损失权重由配置进入 loss 的路径，写下特征的层、维度和归一化位置。学会在既有训练系统中定位新增机制。

## 学到什么程度

能够用具体 patch 对应或密集预测案例比较 DINOv2／DINOv3；优先使用较小公开模型。

## 算力与复现门槛

用单卡推理和冻结特征起步，八卡支持下游学习；不把八卡 4090 当作复刻其大规模预训练的预算。

模型权重有独立访问流程与 DINOv3 专用许可；代码下载与权重可访问是两件事。

## 带着什么问题读

高质量密集特征是否改善动作相关对象定位？分辨率提升的收益能否覆盖推理延迟增加？

本卡中的学习目标与问题是为本资料库提出的建议，不是论文已经证明的结论。本次只核对资料和源码，未运行该项目训练。

[返回学习路线](../docs/学习路线与选题判断.md) · [资源总表](../docs/资源总表.md)

[论文阅读指南](../docs/论文阅读指南.md) · [代码阅读指南](../docs/代码阅读指南.md)
