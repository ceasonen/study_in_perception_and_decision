# P07 · GroundingDINO

推荐顺序：进阶，用于开放词表与语言目标。

[上游仓库](https://github.com/IDEA-Research/GroundingDINO) · [本地源码](../repositories/perception/P07_GroundingDINO)

## 对应论文

- [Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection](https://arxiv.org/abs/2303.05499)，ECCV 2024；arXiv 初版 2023。[下载的全文](../papers/perception/groundingdino.pdf)

## 为什么选择

GroundingDINO 将语言条件接到目标检测，可用于理解任务描述怎样决定应该感知什么，而不只识别固定类别。

## 论文：要理解的方法与假设

文本与视觉特征的交互、语言引导的查询以及框和短语的对应；注意得分阈值和词语组合的影响。

建议按以下入口追踪实现：

- [groundingdino/models/GroundingDINO/groundingdino.py](../repositories/perception/P07_GroundingDINO/groundingdino/models/GroundingDINO/groundingdino.py)
- [groundingdino/util/inference.py](../repositories/perception/P07_GroundingDINO/groundingdino/util/inference.py)
- [demo/inference_on_a_image.py](../repositories/perception/P07_GroundingDINO/demo/inference_on_a_image.py)

## 代码：作者如何组织实现

推理 util 管理 load_model／load_image／predict／annotate，GroundingDINO 模型负责视觉语言融合。可先读完整推理链再读大型模型内部。

### 沿这条路径读

图像和 caption → preprocess_caption → 模型输入 → GroundingDINO.forward → 框与短语筛选 → annotate。

### 要掌握的编程方法与练习

说明文本阈值和框阈值发生在哪里，整理图像坐标与输出框约定。学会把算法模型封装成可调用推理接口。

## 学到什么程度

对同一图像改变指令，检查目标定位变化与失败案例，并说明定位结果如何进入下游任务状态。

## 算力与复现门槛

先单卡运行推理；下游微调与原始开放词表预训练是不同预算。CUDA 自定义算子也需要对应编译环境。

开放词表定位不等于可交互性理解；正确定位杯子仍不代表能够预测抓取接触、稳定性或执行动作。

## 带着什么问题读

语言指定目标时，关系和属性歧义如何影响策略？检测置信度能否辅助重新观察或澄清？

本卡中的学习目标与问题是为本资料库提出的建议，不是论文已经证明的结论。本次只核对资料和源码，未运行该项目训练。

[返回学习路线](../docs/学习路线与选题判断.md) · [资源总表](../docs/资源总表.md)

[论文阅读指南](../docs/论文阅读指南.md) · [代码阅读指南](../docs/代码阅读指南.md)
