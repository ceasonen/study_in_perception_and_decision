# C06 · Diffusion-Policy

推荐顺序：模仿学习进阶，与 ACT 对照。

[上游仓库](https://github.com/real-stanford/diffusion_policy) · [本地源码](../repositories/closed_loop/C06_Diffusion-Policy)

## 对应论文

- [Diffusion Policy: Visuomotor Policy Learning via Action Diffusion](https://arxiv.org/abs/2303.04137)，RSS 2023。[下载的全文](../papers/closed_loop/diffusion_policy.pdf)

## 为什么选择

Diffusion Policy 把视觉条件下的动作序列分布交给扩散模型，适合理解多模态动作、序列预测与滚动执行。

## 论文：要理解的方法与假设

视觉编码、噪声预测训练、条件去噪与执行 horizon；把生成质量和控制实时性联系起来。

建议按以下入口追踪实现：

- [diffusion_policy/policy/diffusion_unet_image_policy.py](../repositories/closed_loop/C06_Diffusion-Policy/diffusion_policy/policy/diffusion_unet_image_policy.py)
- [diffusion_policy/workspace/train_diffusion_unet_image_workspace.py](../repositories/closed_loop/C06_Diffusion-Policy/diffusion_policy/workspace/train_diffusion_unet_image_workspace.py)
- [train.py](../repositories/closed_loop/C06_Diffusion-Policy/train.py)

## 代码：作者如何组织实现

Workspace 组织训练、checkpoint 与日志，Policy 实现 compute_loss 和 predict_action，配置负责组装数据与模型。

### 沿这条路径读

train.py／Workspace → dataset → DiffusionUnetImagePolicy.compute_loss → optimizer；评估侧 predict_action → 去噪 → 执行部分动作。

### 要掌握的编程方法与练习

区分训练的噪声时间步和真实环境时间步，标注 observation／prediction／action horizon。学会读生成模型用于控制时的双重时间轴。

## 学到什么程度

理解 Push-T 等任务从示范到策略执行的路径，能够比较动作多样性、任务成功率和推理延迟。

## 算力与复现门槛

单任务可先单卡尝试；八卡适合多个任务与种子。完整基准数据、仿真依赖与配置另行准备。

经典 Diffusion Policy 是模仿学习；不能因为生成动作就称其为在线强化学习。动作空间、horizon 与控制频率影响可比性。

## 带着什么问题读

较多去噪步骤带来的成功率收益是否值得延迟？多峰动作分布在什么任务中有实际价值？

本卡中的学习目标与问题是为本资料库提出的建议，不是论文已经证明的结论。本次只核对资料和源码，未运行该项目训练。

[返回学习路线](../docs/学习路线与选题判断.md) · [资源总表](../docs/资源总表.md)

[论文阅读指南](../docs/论文阅读指南.md) · [代码阅读指南](../docs/代码阅读指南.md)
