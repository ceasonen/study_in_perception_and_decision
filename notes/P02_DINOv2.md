# P02 · DINOv2

推荐顺序：核心精读，视觉表征首选起点。

[上游仓库](https://github.com/facebookresearch/dinov2) · [本地源码](../repositories/perception/P02_DINOv2)

## 对应论文

- [DINOv2: Learning Robust Visual Features without Supervision](https://arxiv.org/abs/2304.07193)，TMLR 2024；arXiv 初版 2023。[下载的全文](../papers/perception/dinov2.pdf)

## 为什么选择

DINOv2 适合学习不依赖下游标签的通用视觉特征。它能作为视觉决策研究中的冻结编码器参照，帮助区分表征能力与策略学习能力。

## 论文：要理解的方法与假设

理解 teacher–student、自蒸馏、图像级／patch 级目标及训练数据选择；先研究特征的下游表现。

建议按以下入口追踪实现：

- [dinov2/train/ssl_meta_arch.py](../repositories/perception/P02_DINOv2/dinov2/train/ssl_meta_arch.py)
- [dinov2/models/vision_transformer.py](../repositories/perception/P02_DINOv2/dinov2/models/vision_transformer.py)
- [hubconf.py](../repositories/perception/P02_DINOv2/hubconf.py)

## 代码：作者如何组织实现

SSLMetaArch 管理学生、教师和训练目标；DinoVisionTransformer 管理特征计算，配置和分布式训练另由外层组织。

### 沿这条路径读

先从 hubconf.py 理解推理模型怎样构建，再看 DinoVisionTransformer 的 token 流，最后追踪 SSLMetaArch 中学生反传与教师更新的边界。

### 要掌握的编程方法与练习

画出教师、学生、投影头和损失之间的调用关系，标明哪些变量需要梯度、哪些属于慢更新状态。学会阅读多分支训练代码。

## 学到什么程度

完成 patch 特征可视化，说明冻结特征能捕捉什么、遗漏什么，并能够把特征接到一个小下游头。

## 算力与复现门槛

单卡适合小模型推理、特征缓存和轻量头训练；八卡用于下游适配和多个对照。完整原始预训练规模远超普通学习复现。

通用特征并不自动具备时间记忆或动力学预测能力；仓库当前含后续模型扩展，应与本篇对应实现区分。

## 带着什么问题读

语义上好的特征能否保留速度、接触和可控性信息？任务训练与冻结编码器各自在哪些情况下有优势？

本卡中的学习目标与问题是为本资料库提出的建议，不是论文已经证明的结论。本次只核对资料和源码，未运行该项目训练。

[返回学习路线](../docs/学习路线与选题判断.md) · [资源总表](../docs/资源总表.md)

[论文阅读指南](../docs/论文阅读指南.md) · [代码阅读指南](../docs/代码阅读指南.md)
