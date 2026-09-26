# 感知与决策博士学习资料库

面向已具备入门基础、尚未限定应用场景、至少可使用 8 张 RTX 4090 的学习者。按“视觉感知 → 序贯决策 → 感知决策闭环”组织第一批 **21 个研究／工具仓库、29 篇论文全文**。检索与收集日期：2026-09-26。

## 从哪里开始

先读[学习路线与选题判断](docs/学习路线与选题判断.md)，再按两种目标进入资料：**[读论文，提升研究理解](docs/论文阅读指南.md)**；**[读仓库，掌握实现方法](docs/代码阅读指南.md)**。原始全文在 `papers/`，原始源码在 `repositories/`，不会混在一个目录里。

[资源总表](docs/资源总表.md)链接到每个项目的学习卡。每张卡分别说明论文要理解的方法与假设、作者怎样组织代码、具体追踪顺序与练习，另含学习目标、算力建议和局限。

建议第一轮精读：**DETR → DINOv2 → ByteTrack；PPO → SAC；DrQ-v2 → DreamerV3；MAPPO**。其中最推荐的首个完整视觉决策学习项目是 **DrQ-v2**，随后进入世界模型或多智能体分支。

| 学习层次 | 主要资料 | 要建立的能力 |
| --- | --- | --- |
| 感知 | DETR、DINOv2／v3、ByteTrack、GlobalTrack、CSTrack、GroundingDINO | 对象、时序、多模态与任务相关表征 |
| 决策 | PPO／SAC、CleanRL、SB3、MAPPO、QMIX、TAPE、MALib | 策略学习、部分可观测、信用分配与协同 |
| 闭环 | DrQ-v2、DreamerV3、Habitat、ACT、Diffusion Policy | 从观测到状态、预测与行动 |
| 进阶分支 | CoS、OpenPI | 视觉语言奖励、推理与动作适配 |

GlobalTrack、CSTrack、TAPE、CoS 与黄凯奇老师参与的工作对应，学习卡中已说明。这里的路线是基于公开资料与学习条件提出的建议，不代表老师已经指定具体课题。

## 文件入口

- [12 周学习路线及方向分析](docs/学习路线与选题判断.md)
- [论文阅读指南](docs/论文阅读指南.md)与[论文笔记模板](docs/templates/论文笔记.md)
- [代码阅读指南](docs/代码阅读指南.md)与[代码笔记模板](docs/templates/代码笔记.md)
- [21 个仓库总表](docs/资源总表.md)
- [29 篇论文全文索引](docs/论文索引.md)
- [下载范围、外部数据和权重入口](docs/下载范围与额外资源.md)
- [逐项学习卡](notes/)
- [来源清单](resources/catalog.json)、[实际下载记录](resources/download_status.json)、[检查结果](resources/verification.json)
- [第三方来源与许可说明](THIRD_PARTY.md)

## 目录结构

```text
docs/                         学习路线、资源与论文索引、外部依赖说明
notes/                        每个项目一张学习卡
papers/
  overview/                   中文方向综述
  perception/                 视觉基础、检测、跟踪和表征论文
  decision/                   强化学习、协同与系统论文
  closed_loop/                视觉控制、世界模型、具身与动作论文
repositories/
  perception/                 7 个源码目录
  decision/                   6 个源码目录
  closed_loop/                8 个源码目录，包含展开的上游子模块
resources/                    来源、学习卡数据、下载与检查记录
scripts/                      顺序下载、生成索引和检查工具
downloads/                    本地保留归档与临时元数据，不重复上传
```

## 下载完成的含义

源码按公开分支归档逐项下载，已声明的子模块另行展开。第三方目录不保留各自的 `.git`，本仓库自身的 Git 用于统一提交。保留上游代码、配置、说明和许可；不把子项目注册成 Git submodule。

论文保存全文 PDF，并检查可解析性与页数。独立数据集、模型权重、场景与安装后的训练环境另行准备，不能将源码收集视为论文结果复现。M2RL 的真实代码入口需要账号申请与审核；本库保留相关论文，MALib 是单独的公开学习项目。

```sh
python3 scripts/download_resources.py
python3 scripts/build_indexes.py
python3 scripts/verify_resources.py
```

辅助工具需要 Python 3.11+、curl 和 Poppler（`pdfinfo`／`pdftotext`），不计算或验证文件哈希。各第三方项目安装与训练应采用其各自要求的环境；本资料库没有把 21 个不同依赖栈合成一个训练环境。
