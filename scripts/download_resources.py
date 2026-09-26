#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Sequentially collect public source snapshots and papers; no digest operations."""

import argparse
import configparser
import json
import shutil
import subprocess
import tarfile
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "resources/catalog.json"
REPORT = ROOT / "resources/download_status.json"


def stamp():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def download(url, target):
    if target.exists() and target.stat().st_size:
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + ".part")
    subprocess.run(
        ["curl", "--fail", "--location", "--silent", "--show-error",
         "--retry", "2", "--connect-timeout", "20", "--max-time", "1800",
         "--user-agent", "perception-decision-study/1.0",
         "--output", str(temporary), url], check=True,
    )
    if not temporary.stat().st_size:
        raise ValueError(f"Empty response: {url}")
    temporary.replace(target)


def api(url, name):
    target = ROOT / "downloads/metadata" / f"{name}.json"
    download(url, target)
    return json.loads(target.read_text())


def extract(archive, destination):
    """Read all members and unpack with Python's data extraction filter."""
    destination.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive, "r:gz") as bundle:
        members = bundle.getmembers()
        prefix = members[0].name.split("/")[0]
        count = 0
        for member in members:
            relative = member.name.removeprefix(prefix).lstrip("/")
            if not relative or ".git" in Path(relative).parts:
                continue
            member.name = relative
            if member.islnk():
                member.linkname = member.linkname.removeprefix(prefix).lstrip("/")
            bundle.extract(member, destination, filter="data")
            count += member.isfile()
    return count


def submodules(repo, ref, directory, records, label, depth=0):
    modules = directory / ".gitmodules"
    if not modules.exists():
        return
    if depth > 5:
        raise ValueError("Unexpectedly deep submodule tree")
    configuration = configparser.ConfigParser()
    configuration.read(modules)
    for section in configuration.sections():
        relative = configuration[section]["path"]
        url = configuration[section]["url"]
        if url.startswith("../"):
            parent = repo.split("/")[0]
            url = f"https://github.com/{parent}/{url.removeprefix('../')}"
        child_repo = url.removesuffix(".git").removeprefix("https://github.com/")
        child_repo = child_repo.removeprefix("git@github.com:")
        if child_repo.count("/") != 1:
            raise ValueError(f"Unsupported submodule URL: {url}")
        safe_label = f"{label}_{relative.replace('/', '_')}"
        try:
            information = api(
                f"https://api.github.com/repos/{repo}/contents/{quote(relative)}?ref={quote(ref)}",
                safe_label,
            )
        except subprocess.CalledProcessError:
            tree = api(
                f"https://api.github.com/repos/{repo}/git/trees/{quote(ref)}?recursive=1",
                f"{label}_tree",
            )
            if not tree.get("truncated") and not any(
                node["path"] == relative for node in tree["tree"]
            ):
                records.append({"declared_path": relative, "source": url,
                                "status": "stale_declaration",
                                "note": "The upstream .gitmodules entry has no corresponding path in the complete upstream tree."})
                print(f"  stale upstream submodule declaration: {relative}", flush=True)
                continue
            raise
        # This is an existing upstream reference returned by GitHub, not a computed digest.
        child_ref = information["sha"]
        archive_url = f"https://codeload.github.com/{child_repo}/tar.gz/{child_ref}"
        archive = ROOT / "downloads/source_archives" / f"{safe_label}.tar.gz"
        download(archive_url, archive)
        child_directory = directory / relative
        count = extract(archive, child_directory)
        records.append({"path": str(child_directory.relative_to(ROOT)),
                        "source": f"https://github.com/{child_repo}",
                        "upstream_ref": child_ref, "files": count,
                        "archive_url": archive_url, "status": "downloaded"})
        print(f"  submodule {child_repo}: {count} files", flush=True)
        submodules(child_repo, child_ref, child_directory, records, safe_label, depth + 1)


class CitationParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.values = {}

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "meta" and attributes.get("name", "").startswith("citation_"):
            self.values.setdefault(attributes["name"], []).append(attributes.get("content", ""))


def save(report):
    report["updated_at"] = stamp()
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")


def collect_repositories(catalog, report):
    for index, entry in enumerate(catalog["repositories"], 1):
        label = f"{entry['id']}_{entry['name']}"
        prior = report["repositories"].get(entry["id"], {})
        if prior.get("status") == "downloaded" and prior.get("repo") == entry["repo"]:
            continue
        record = {"repo": entry["repo"], "started_at": stamp(), "submodules": []}
        report["repositories"][entry["id"]] = record
        print(f"REPO {index}/{len(catalog['repositories'])} {label}", flush=True)
        try:
            meta = api(f"https://api.github.com/repos/{entry['repo']}", label)
            branch = meta["default_branch"]
            archive_url = f"https://codeload.github.com/{entry['repo']}/tar.gz/refs/heads/{branch}"
            archive = ROOT / "downloads/source_archives" / f"{label}.tar.gz"
            destination = ROOT / "repositories" / entry["track"] / label
            download(archive_url, archive)
            count = extract(archive, destination)
            record.update({"path": str(destination.relative_to(ROOT)), "branch": branch,
                           "archive_url": archive_url, "files": count,
                           "archive_bytes": archive.stat().st_size,
                           "archived_upstream": meta.get("archived"),
                           "license_api": (meta.get("license") or {}).get("spdx_id"),
                           "upstream_url": meta.get("html_url")})
            submodules(entry["repo"], branch, destination, record["submodules"], label)
            record.update(status="downloaded", completed_at=stamp())
            print(f"  downloaded {count} files", flush=True)
        except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
            record.update(status="failed", error=str(error))
            print(f"  FAILED: {error}", flush=True)
        save(report)


def collect_papers(catalog, report):
    for index, entry in enumerate(catalog["papers"], 1):
        if report["papers"].get(entry["id"], {}).get("status") == "downloaded":
            continue
        arxiv = entry.get("arxiv")
        url = entry.get("url", f"https://arxiv.org/abs/{arxiv}")
        pdf_url = entry.get("pdf", f"https://arxiv.org/pdf/{arxiv}")
        destination = ROOT / "papers" / entry["track"] / f"{entry['id']}.pdf"
        record = {"title": entry["title"], "landing_url": url, "pdf_url": pdf_url}
        report["papers"][entry["id"]] = record
        print(f"PAPER {index}/{len(catalog['papers'])} {entry['id']}", flush=True)
        try:
            if not url.lower().endswith(".pdf"):
                html = ROOT / "downloads/metadata" / f"paper_{entry['id']}.html"
                download(url, html)
                parser = CitationParser()
                parser.feed(html.read_text(errors="replace"))
                record["citation_metadata"] = parser.values
            download(pdf_url, destination)
            with destination.open("rb") as stream:
                if stream.read(5) != b"%PDF-":
                    raise ValueError("Response is not a PDF")
            info = subprocess.run(["pdfinfo", str(destination)], check=True,
                                  capture_output=True, text=True).stdout
            pages = next(line.split(":", 1)[1].strip() for line in info.splitlines()
                         if line.startswith("Pages:"))
            first_page = ROOT / "downloads/metadata" / f"paper_{entry['id']}_first_page.txt"
            subprocess.run(["pdftotext", "-f", "1", "-l", "1", str(destination),
                            str(first_page)], check=True)
            record.update(status="downloaded", completed_at=stamp(), pages=int(pages),
                          bytes=destination.stat().st_size,
                          path=str(destination.relative_to(ROOT)))
            print(f"  downloaded {pages} pages", flush=True)
        except (OSError, ValueError, StopIteration, subprocess.CalledProcessError) as error:
            record.update(status="failed", error=str(error))
            print(f"  FAILED: {error}", flush=True)
        save(report)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=["repositories", "papers", "all"], default="all")
    arguments = parser.parse_args()
    if not shutil.which("curl") or not shutil.which("pdfinfo"):
        raise SystemExit("curl and Poppler pdfinfo/pdftotext are required")
    catalog = json.loads(CATALOG.read_text())
    report = json.loads(REPORT.read_text()) if REPORT.exists() else {
        "started_at": stamp(), "repositories": {}, "papers": {},
        "scope": "Public source snapshots with recursive submodules and full PDFs; no datasets, model weights, Git history, or hash verification.",
    }
    if arguments.only in ("all", "repositories"):
        collect_repositories(catalog, report)
    if arguments.only in ("all", "papers"):
        collect_papers(catalog, report)
    failures = [key for group in ("repositories", "papers")
                for key, value in report[group].items() if value["status"] != "downloaded"]
    print(f"DONE: repositories={len(report['repositories'])}, papers={len(report['papers'])}, failures={failures}")
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
