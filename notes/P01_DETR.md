# P01 · DETR

推荐顺序：核心精读，先理解再做小规模验证。

[上游仓库](https://github.com/facebookresearch/detr) · [本地源码](../repositories/perception/P01_DETR)

## 对应论文

- [End-to-End Object Detection with Transformers](https://arxiv.org/abs/2005.12872)，ECCV 2020。[下载的全文](../papers/perception/detr.pdf)

## 为什么选择

DETR 把检测写成集合预测，适合学习目标查询、注意力、匹配与损失如何共同决定对象表示。对决策而言，它提供从像素到对象集合的概念桥梁。

## 论文：要理解的方法与假设

重点推导二分匹配、无对象类别和辅助损失；追踪 backbone、位置编码、transformer 与预测头的数据形状。

建议按以下入口追踪实现：

- [models/detr.py](../repositories/perception/P01_DETR/models/detr.py)
- [models/matcher.py](../repositories/perception/P01_DETR/models/matcher.py)
- [models/transformer.py](../repositories/perception/P01_DETR/models/transformer.py)

## 代码：作者如何组织实现

训练入口负责组装，模型、匹配器、criterion 与后处理分别实现。DETR 的 forward 输出预测，SetCriterion 负责监督，PostProcess 负责还原检测结果。

### 沿这条路径读

main.py → engine.py → DETR.forward → HungarianMatcher → SetCriterion → optimizer。记录图像 batch、object queries、pred_logits、pred_boxes 和 targets 的形状与坐标单位。

### 要掌握的编程方法与练习

单独说明 matcher 与 criterion 的输入输出约定；用一张图的预测解释后处理怎样缩放坐标。学会让模型、损失和展示逻辑保持清晰接口。

## 学到什么程度

能画出一张图像到一组目标框的计算图，解释为什么训练需要匹配，以及错检对象如何影响下游状态。

## 算力与复现门槛

先用预训练权重推理或小子集训练；官方原始 COCO 完整训练较长。八卡能支持训练探索，实际速度需在你的服务器测量。

上游仓库已归档；这是理解集合预测的经典代码，不应当作当前最快的检测方案。权重、COCO 和运行环境独立准备。

## 带着什么问题读

对象级表征是否足够支持动作选择？检测 AP 的提升在哪些失败情形下会转化为策略收益？

本卡中的学习目标与问题是为本资料库提出的建议，不是论文已经证明的结论。本次只核对资料和源码，未运行该项目训练。

[返回学习路线](../docs/学习路线与选题判断.md) · [资源总表](../docs/资源总表.md)

[论文阅读指南](../docs/论文阅读指南.md) · [代码阅读指南](../docs/代码阅读指南.md)
