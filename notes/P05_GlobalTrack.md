# P05 · GlobalTrack

推荐顺序：导师相关，重点读思想与失败模式。

[上游仓库](https://github.com/huanglianghua/GlobalTrack) · [本地源码](../repositories/perception/P05_GlobalTrack)

## 对应论文

- [GlobalTrack: A Simple and Strong Baseline for Long-term Tracking](https://arxiv.org/abs/1912.08531)，AAAI 2020。[下载的全文](../papers/perception/globaltrack.pdf)

## 为什么选择

GlobalTrack 有黄凯奇老师参与，使用全图实例搜索应对长期目标丢失，是理解目标重定位与长期感知的合适材料。

## 论文：要理解的方法与假设

查询调制的检测结构、全图搜索与跨查询损失；与依赖局部运动连续性的跟踪方法比较。

建议按以下入口追踪实现：

- [trackers/global_track.py](../repositories/perception/P05_GlobalTrack/trackers/global_track.py)
- [modules/modulators.py](../repositories/perception/P05_GlobalTrack/modules/modulators.py)
- [modules/qg_rcnn.py](../repositories/perception/P05_GlobalTrack/modules/qg_rcnn.py)

## 代码：作者如何组织实现

GlobalTrack 是跟踪接口，RPN_Modulator／RCNN_Modulator 将查询特征接到检测模块；训练和在线调用走不同外层路径。

### 沿这条路径读

目标初始化 → 查询特征缓存 → 新帧特征 → 查询调制 RPN／RCNN → 候选框 → 跟踪输出。

### 要掌握的编程方法与练习

整理初始化与逐帧更新各自的输入、缓存和返回值，标出训练专用模块。学会在成熟框架中理解自定义模块的接入位置。

## 学到什么程度

用论文图和代码解释暂时跟踪失败为何不必一直累积，并明确它仍可能出现的误匹配。

## 算力与复现门槛

先读代码和做推理；从头训练需相应跟踪数据与初始化权重。算力并不是主要入门障碍。

项目采用较旧的 mmdetection／环境栈，仓库已包含其源码；优先独立环境或容器，不能假设当前 PyTorch 可直接兼容。

## 带着什么问题读

主动移动相机与全图重定位能否互补？重定位不确定性怎样传递给策略？

本卡中的学习目标与问题是为本资料库提出的建议，不是论文已经证明的结论。本次只核对资料和源码，未运行该项目训练。

[返回学习路线](../docs/学习路线与选题判断.md) · [资源总表](../docs/资源总表.md)

[论文阅读指南](../docs/论文阅读指南.md) · [代码阅读指南](../docs/代码阅读指南.md)
