# P06 · CSTrack

推荐顺序：导师相关进阶，多模态和时序学习。

[上游仓库](https://github.com/XiaokunFeng/CSTrack) · [本地源码](../repositories/perception/P06_CSTrack)

## 对应论文

- [CSTrack: Enhancing RGB-X Tracking via Compact Spatiotemporal Features](https://arxiv.org/abs/2505.19434)，ICML 2025。[下载的全文](../papers/perception/cstrack.pdf)

## 为什么选择

CSTrack 有黄凯奇老师参与，关注 RGB 与深度、热红外、事件等模态的紧凑时空表示。它与你的多源感知学习有直接联系。

## 论文：要理解的方法与假设

空间紧凑模块和时间紧凑模块；比较模态内、模态间与时间建模分别承担的作用。

建议按以下入口追踪实现：

- [lib/models/cstrack_s1/cstrack_s1.py](../repositories/perception/P06_CSTrack/lib/models/cstrack_s1/cstrack_s1.py)
- [lib/models/cstrack_s2/cstrack_s2.py](../repositories/perception/P06_CSTrack/lib/models/cstrack_s2/cstrack_s2.py)
- [tracking/train.py](../repositories/perception/P06_CSTrack/tracking/train.py)

## 代码：作者如何组织实现

CSTRACK_S1 与 CSTRACK_S2 显式区分训练阶段，模型工厂构建模块，训练与评估通过对应配置连接。

### 沿这条路径读

RGB 与 X 的预处理 → 空间特征模块 → 阶段二时间模块 → 预测头 → loss；再看阶段一权重如何进入阶段二。

### 要掌握的编程方法与练习

整理两阶段之间的参数初始化与配置依赖，区分实时历史状态和训练样本窗口。学会读分阶段训练和时序状态代码。

## 学到什么程度

理解两阶段训练，能够说明测试输入模态、历史信息与目标初始化，列出一个具体模态失效案例。

## 算力与复现门槛

官方提供多卡训练命令；八卡可尝试其训练与对照，但多种跟踪数据的准备成本需要单独安排。

此处是 ICML 2025 的 RGB-X CSTrack，区别于早期同名多目标跟踪工作；数据与预训练权重不在普通源码归档中。

## 带着什么问题读

融合增益来自额外可靠信息还是数据规模？某一模态退化时，紧凑表征是否会把错误传递给决策？

本卡中的学习目标与问题是为本资料库提出的建议，不是论文已经证明的结论。本次只核对资料和源码，未运行该项目训练。

[返回学习路线](../docs/学习路线与选题判断.md) · [资源总表](../docs/资源总表.md)

[论文阅读指南](../docs/论文阅读指南.md) · [代码阅读指南](../docs/代码阅读指南.md)
