#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Build readable indexes and individual learning cards from curated records."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / "resources/catalog.json").read_text())
notes = json.loads((ROOT / "resources/learning_notes.json").read_text())
code_notes = json.loads((ROOT / "resources/code_reading.json").read_text())
status = json.loads((ROOT / "resources/download_status.json").read_text())
papers = {paper["id"]: paper for paper in catalog["papers"]}


def link_for(paper):
    return paper.get("url") or f"https://arxiv.org/abs/{paper['arxiv']}"


def repository_path(entry):
    return f"repositories/{entry['track']}/{entry['id']}_{entry['name']}"


def write_cards():
    folder = ROOT / "notes"
    folder.mkdir(exist_ok=True)
    for entry in catalog["repositories"]:
        note = notes[entry["id"]]
        coding = code_notes[entry["id"]]
        path = repository_path(entry)
        lines = [f"# {entry['id']} · {entry['name']}", "",
                 f"推荐顺序：{note['priority']}。", "",
                 f"[上游仓库](https://github.com/{entry['repo']}) · [本地源码](../{path})", "",
                 "## 对应论文", ""]
        for key in entry["papers"]:
            paper = papers[key]
            local = f"../papers/{paper['track']}/{key}.pdf"
            lines.append(f"- [{paper['title']}]({link_for(paper)})，{paper['venue']}。"
                         f"[下载的全文]({local})")
        lines += ["", "## 为什么选择", "", note["why"], "", "## 论文：要理解的方法与假设", "",
                  note["focus"], "", "建议按以下入口追踪实现：", ""]
        for point in note["entries"]:
            lines.append(f"- [{point}](../{path}/{point})")
        lines += ["", "## 代码：作者如何组织实现", "", coding["structure"], "",
                  "### 沿这条路径读", "", coding["trace"], "",
                  "### 要掌握的编程方法与练习", "", coding["practice"], "",
                  "## 学到什么程度", "", note["milestone"], "",
                  "## 算力与复现门槛", "", note["compute"], "", note["limits"], "",
                  "## 带着什么问题读", "", note["questions"], "",
                  "本卡中的学习目标与问题是为本资料库提出的建议，不是论文已经证明的结论。"
                  "本次只核对资料和源码，未运行该项目训练。", "",
                  "[返回学习路线](../docs/学习路线与选题判断.md) · [资源总表](../docs/资源总表.md)", ""]
        lines += ["[论文阅读指南](../docs/论文阅读指南.md) · [代码阅读指南](../docs/代码阅读指南.md)", ""]
        (folder / f"{entry['id']}_{entry['name']}.md").write_text("\n".join(lines))


def write_repository_index():
    lines = ["# 仓库与下载状态", "", "源码快照按收集日期保存，未初始化第三方 Git 仓库；"
             "Tianshou 保留用户提供的本地版本，来源另有记录。"
             "状态描述的是下载与目录检查，不代表已经复现论文。", "",
             "| 编号 | 项目与逐项分析 | 上游来源 | 下载状态 | 上游许可标记 |",
             "| --- | --- | --- | --- | --- |"]
    for entry in catalog["repositories"]:
        record = status["repositories"].get(entry["id"], {})
        good = record.get("status") == "downloaded" and record.get("repo") == entry["repo"]
        state = f"源码 {record.get('files', 0)} 文件" if good else "尚未完成"
        expanded = sum(module.get("status") == "downloaded" for module in record.get("submodules", []))
        stale = sum(module.get("status") == "stale_declaration" for module in record.get("submodules", []))
        if good and expanded:
            state += f"；另含 {expanded} 个子模块目录"
        if good and stale:
            state += f"；{stale} 个上游遗留声明已记录"
        license_name = record.get("license_api") or "未由 API 明确识别；查看原文"
        lines.append(f"| {entry['id']} | [{entry['name']}](../notes/{entry['id']}_{entry['name']}.md)"
                     f" | [{entry['repo']}](https://github.com/{entry['repo']}) | {state} | {license_name} |")
    lines += ["", "原始声明以每个源码目录内的 LICENSE／NOTICE／版权头为准；"
              "API 标记不是法律许可审核，也不覆盖单独发布的模型权重。", "",
              "M2RL 的真实代码入口需要申请审核，未下载。其论文保留在全文库，MALib 作为独立的公开学习项目。", "",
              "机器可读来源与下载记录：[catalog.json](../resources/catalog.json)、"
              "[download_status.json](../resources/download_status.json)。", ""]
    (ROOT / "docs/资源总表.md").write_text("\n".join(lines))


def write_paper_index():
    lines = ["# 论文全文索引", "", "题名与来源分别链接到原始论文页面。"
             "表中的发表信息用于定位正式论文；下载文件可能是 arXiv 版本，不默认为出版社版本。", "",
             "| 论文 | 发表信息 | 本地全文 | 页数 |",
             "| --- | --- | --- | --- |"]
    for paper in catalog["papers"]:
        record = status["papers"].get(paper["id"], {})
        file = f"papers/{paper['track']}/{paper['id']}.pdf"
        state = f"[PDF](../{file})" if record.get("status") == "downloaded" else "尚未完成"
        lines.append(f"| [{paper['title']}]({link_for(paper)}) | {paper['venue']}"
                     f" | {state} | {record.get('pages', '-')} |")
    lines += ["", "## 补充论文如何读", "",
              "ResNet／ViT：复习视觉骨干和表示方式，已熟悉者可快速跳过。", "",
              "PPO／SAC：重点对应 CleanRL、SB3 与 Tianshou 的程序，不把框架论文当成算法论文。", "",
              "Tianshou：JMLR 2022 框架论文用于理解模块化设计；当前源码是 v2，"
              "接口以本地代码和 CHANGELOG 为准。配合[RL 基础设施专题](RL基础设施学习专题.md)阅读。", "",
              "人机对抗智能技术、分布式强化学习综述与 M2RL：用于理解研究问题和系统组织，"
              "不要把分布式运行本身等同于新的学习算法。", "",
              "Habitat 1.0／2.0：按具体任务阅读平台设计；当前源码可能已覆盖后续功能。", "",
              "π₀／π₀.₅：比较动作生成与泛化训练，不把当前普通推理／模仿学习用法等同于在线 RL。", ""]
    (ROOT / "docs/论文索引.md").write_text("\n".join(lines))


def main():
    (ROOT / "docs").mkdir(exist_ok=True)
    write_cards()
    write_repository_index()
    write_paper_index()
    print(f"Built {len(catalog['repositories'])} learning cards and both indexes.")


if __name__ == "__main__":
    main()
