#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Check file presence, paths, PDF readability, archive coverage, and upload sizes.

No file or Git object digests are calculated or compared.
"""

import json
import re
import subprocess
import tarfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def check_archive(archive, destination):
    errors = []
    checked = 0
    with tarfile.open(archive, "r:gz") as bundle:
        members = bundle.getmembers()
        prefix = members[0].name.split("/")[0]
        for member in members:
            relative = member.name.removeprefix(prefix).lstrip("/")
            if not relative or ".git" in Path(relative).parts or not member.isfile():
                continue
            target = destination / relative
            if not target.is_file():
                errors.append(f"Missing archive member: {target.relative_to(ROOT)}")
            elif target.stat().st_size != member.size:
                errors.append(f"Unexpected file size: {target.relative_to(ROOT)}")
            checked += 1
    return checked, errors


def main():
    catalog = json.loads((ROOT / "resources/catalog.json").read_text())
    status = json.loads((ROOT / "resources/download_status.json").read_text())
    notes = json.loads((ROOT / "resources/learning_notes.json").read_text())
    errors = []
    repo_results = []
    paper_results = []
    file_count = 0
    for entry in catalog["repositories"]:
        record = status["repositories"].get(entry["id"], {})
        label = f"{entry['id']}_{entry['name']}"
        if record.get("status") != "downloaded" or record.get("repo") != entry["repo"]:
            errors.append(f"Repository incomplete or wrong source: {label}")
            continue
        destination = ROOT / record["path"]
        archive = ROOT / "downloads/source_archives" / f"{label}.tar.gz"
        count, problems = check_archive(archive, destination)
        errors.extend(problems)
        file_count += count
        for module in record.get("submodules", []):
            if module.get("status") == "stale_declaration":
                continue
            module_destination = ROOT / module["path"]
            relative = module_destination.relative_to(destination)
            # Nested labels include their parent labels; match by exact archive URL
            # through the cached GitHub metadata filename used at download time.
            candidates = list((ROOT / "downloads/source_archives").glob(f"{label}_*.tar.gz"))
            matching = [p for p in candidates if p.name.endswith(
                str(relative).replace('/', '_') + ".tar.gz")]
            if not matching:
                # The downloader stores nested module labels with each ancestor.
                tokens = str(relative).replace('/', '_')
                matching = [p for p in candidates if tokens in p.name]
            if matching:
                sub_count, sub_errors = check_archive(matching[0], module_destination)
                file_count += sub_count
                errors.extend(sub_errors)
            elif not module_destination.is_dir() or not any(module_destination.iterdir()):
                errors.append(f"Empty or missing submodule: {module['path']}")
        for point in notes[entry["id"]]["entries"]:
            if not (destination / point).exists():
                errors.append(f"Learning-card entry missing: {label}/{point}")
        if not (ROOT / "notes" / f"{label}.md").is_file():
            errors.append(f"Missing learning card: {label}")
        repo_results.append({"id": entry["id"], "path": record["path"],
                             "files_in_main_archive": count,
                             "submodule_directories": sum(module.get("status") == "downloaded"
                                for module in record.get("submodules", [])),
                             "stale_submodule_declarations": sum(module.get("status") == "stale_declaration"
                                for module in record.get("submodules", []))})

    for paper in catalog["papers"]:
        record = status["papers"].get(paper["id"], {})
        destination = ROOT / "papers" / paper["track"] / f"{paper['id']}.pdf"
        if record.get("status") != "downloaded" or not destination.is_file():
            errors.append(f"Paper incomplete: {paper['id']}")
            continue
        result = subprocess.run(["pdfinfo", str(destination)], capture_output=True, text=True)
        if result.returncode:
            errors.append(f"PDF unreadable: {paper['id']}: {result.stderr.strip()}")
            continue
        pages = int(next(line.split(":", 1)[1] for line in result.stdout.splitlines()
                         if line.startswith("Pages:")))
        if pages != record["pages"]:
            errors.append(f"Page-count record mismatch: {paper['id']}")
        paper_results.append({"id": paper["id"], "pages": pages,
                              "bytes": destination.stat().st_size})

    nested_git = [str(p.relative_to(ROOT)) for p in (ROOT / "repositories").rglob(".git")]
    if nested_git:
        errors.append(f"Nested Git metadata: {nested_git}")
    sizes = []
    for folder in ("repositories", "papers"):
        for path in (ROOT / folder).rglob("*"):
            if path.is_file():
                size = path.stat().st_size
                sizes.append((size, str(path.relative_to(ROOT))))
                if size >= 100 * 1024 * 1024:
                    errors.append(f"Exceeds GitHub 100 MiB per-file limit: {path.relative_to(ROOT)}")
    # Validate relative links in our own authored documents, not upstream READMEs.
    for document in [ROOT / "README.md", * (ROOT / "docs").glob("*.md"),
                     * (ROOT / "notes").glob("*.md")]:
        for target in re.findall(r"\]\(([^)]+)\)", document.read_text()):
            if "://" in target or target.startswith("#"):
                continue
            local = target.split("#", 1)[0]
            if local and not (document.parent / local).exists():
                errors.append(f"Broken local link: {document.relative_to(ROOT)} -> {target}")
    result = {
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "checks": "Presence, archive-member sizes, PDF parsing/page counts, code-entry paths, local links, nested Git paths, upload sizes. No hash verification.",
        "repositories": repo_results, "papers": paper_results,
        "archive_files_checked": file_count, "nested_git_count": len(nested_git),
        "total_source_and_pdf_bytes": sum(size for size, _ in sizes),
        "largest_files": [{"bytes": size, "path": path} for size, path in sorted(sizes, reverse=True)[:8]],
        "errors": errors,
        "limitations": "No environment installation, model training, GPU execution, or paper-result reproduction was performed.",
    }
    (ROOT / "resources/verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(f"repositories={len(repo_results)}/{len(catalog['repositories'])}; "
          f"papers={len(paper_results)}/{len(catalog['papers'])}; "
          f"archive_files_checked={file_count}; nested_git={len(nested_git)}; errors={len(errors)}")
    for error in errors:
        print(error)
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
