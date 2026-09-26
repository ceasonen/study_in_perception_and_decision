# P04 · ByteTrack

推荐顺序：核心精读，时序感知基础。

[上游仓库](https://github.com/FoundationVision/ByteTrack) · [本地源码](../repositories/perception/P04_ByteTrack)

## 对应论文

- [ByteTrack: Multi-Object Tracking by Associating Every Detection Box](https://arxiv.org/abs/2110.06864)，ECCV 2022。[下载的全文](../papers/perception/bytetrack.pdf)

## 为什么选择

ByteTrack 的设计较容易读懂：把低置信检测也用于关联，便于理解检测不确定性如何影响轨迹与身份维持。

## 论文：要理解的方法与假设

两阶段关联、预测与匹配、轨迹状态切换；把检测器性能和关联器性能分开理解。

建议按以下入口追踪实现：

- [yolox/tracker/byte_tracker.py](../repositories/perception/P04_ByteTrack/yolox/tracker/byte_tracker.py)
- [yolox/tracker/matching.py](../repositories/perception/P04_ByteTrack/yolox/tracker/matching.py)
- [yolox/tracker/kalman_filter.py](../repositories/perception/P04_ByteTrack/yolox/tracker/kalman_filter.py)

## 代码：作者如何组织实现

STrack 保存单条轨迹的状态，BYTETracker 管理轨迹集合，matching 模块提供关联计算。它是有状态的流式程序。

### 沿这条路径读

逐帧检测框 → BYTETracker.update → 预测与第一轮关联 → 第二轮关联 → 激活、丢失、删除轨迹集合 → 输出轨迹。

### 要掌握的编程方法与练习

手画一条轨迹的状态机，解释连续两帧调用时哪些数据被保留。学会区分单对象状态、集合管理和可复用匹配函数。

## 学到什么程度

可视化遮挡前后的轨迹，能够解释一次 ID 切换的来源，同时报告检测与跟踪指标。

## 算力与复现门槛

推理和分析通常先单卡；检测器训练另计。八卡可支持检测器训练或多种视频条件的对照。

本方法提供跟踪，不直接生成控制动作；把轨迹用于决策还需要任务、状态接口和奖励。

## 带着什么问题读

低置信目标的持续跟踪对避障或目标追随有哪些帮助？误保留背景目标会带来什么下游代价？

本卡中的学习目标与问题是为本资料库提出的建议，不是论文已经证明的结论。本次只核对资料和源码，未运行该项目训练。

[返回学习路线](../docs/学习路线与选题判断.md) · [资源总表](../docs/资源总表.md)

[论文阅读指南](../docs/论文阅读指南.md) · [代码阅读指南](../docs/代码阅读指南.md)
