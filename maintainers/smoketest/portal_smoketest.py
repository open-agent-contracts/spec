#!/usr/bin/env python3
"""Local portal setup smoke checker.

The checker reads only local repository files. It does not fetch URLs,
create or mutate GitHub state, run hosted CI, write files, or perform
credentialed checks.
"""

import json
import re
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT.parents[2]
STAGING_ROOT = PROJECT_ROOT
INVENTORY = SCRIPT.with_name("expected-inventory.json")

LOCAL_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SKIP_SCHEMES = (
    "http://",
    "https://",
    "mailto:",
    "tel:",
)


def _load_inventory():
    with INVENTORY.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _read(path):
    return path.read_text(encoding="utf-8")


def _portal_path(rel):
    return STAGING_ROOT / rel


def _tool_path(rel):
    return PROJECT_ROOT / rel


def check_required_files(data):
    failures = []
    counts = []
    for group in data["groups"]:
        missing = []
        empty = []
        for rel in group["paths"]:
            path = _portal_path(rel)
            if not path.is_file():
                missing.append(rel)
            elif path.stat().st_size == 0:
                empty.append(rel)
        if missing or empty:
            if missing:
                failures.append(
                    group["name"] + " missing: " + ", ".join(sorted(missing))
                )
            if empty:
                failures.append(
                    group["name"] + " empty: " + ", ".join(sorted(empty))
                )
        counts.append((group["name"], len(group["paths"])))
    for rel in data.get("monorepo_tools", []):
        path = _tool_path(rel)
        if not path.is_file():
            failures.append("monorepo tool missing: " + rel)
    return counts, failures


def check_content(data):
    failures = []
    for entry in data["content_checks"]:
        rel = entry["path"]
        path = _portal_path(rel)
        if not path.is_file():
            failures.append("content check target missing: " + rel)
            continue
        text = _read(path)
        for needle in entry["contains"]:
            if needle not in text:
                failures.append(rel + " missing marker: " + needle)
    return failures


def _target_from_link(source, href):
    if not href or href.startswith("#") or href.startswith(SKIP_SCHEMES):
        return None
    if href.startswith("data:") or href.startswith("javascript:"):
        return None
    clean = href.split("#", 1)[0].split("?", 1)[0]
    if not clean:
        return None
    target = (source.parent / clean).resolve()
    if href.endswith("/") or clean.endswith("/"):
        return target / "README.md"
    if target.is_dir():
        return target / "README.md"
    return target


def check_local_markdown_links(data):
    failures = []
    markdown_paths = []
    for group in data["groups"]:
        for rel in group["paths"]:
            if rel.endswith(".md"):
                markdown_paths.append(_portal_path(rel))

    for path in markdown_paths:
        if not path.is_file():
            continue
        text = _read(path)
        for href in LOCAL_LINK_RE.findall(text):
            target = _target_from_link(path, href)
            if target is None:
                continue
            try:
                target.relative_to(PROJECT_ROOT)
            except ValueError:
                failures.append(
                    str(path.relative_to(PROJECT_ROOT))
                    + " link escapes project: "
                    + href
                )
                continue
            if not target.exists():
                failures.append(
                    str(path.relative_to(PROJECT_ROOT))
                    + " unresolved local link: "
                    + href
                )
    return failures


def check_ascii(paths):
    failures = []
    for path in paths:
        if not path.is_file():
            continue
        data = path.read_bytes()
        try:
            data.decode("ascii")
        except UnicodeDecodeError as exc:
            failures.append(
                str(path.relative_to(PROJECT_ROOT))
                + " non-ascii byte at offset "
                + str(exc.start)
            )
    return failures


def main():
    data = _load_inventory()
    counts, failures = check_required_files(data)
    failures.extend(check_content(data))
    failures.extend(check_local_markdown_links(data))

    ascii_paths = []
    for group in data["groups"]:
        for rel in group["paths"]:
            ascii_paths.append(_portal_path(rel))
    for rel in data.get("monorepo_tools", []):
        ascii_paths.append(_tool_path(rel))
    failures.extend(check_ascii(ascii_paths))

    status = "pass" if not failures else "fail"
    print("# Open Agent Contracts Local Smoketest Report")
    print()
    print("status: " + status)
    print("project_root: " + str(PROJECT_ROOT))
    print("staging_root: " + str(STAGING_ROOT))
    print()
    print("| group | files_checked |")
    print("|---|---:|")
    for name, count in counts:
        print("| " + name + " | " + str(count) + " |")
    print()
    if failures:
        print("## Failures")
        print()
        for failure in failures:
            print("- " + failure)
    else:
        print("## Result")
        print()
        print("Local repository inventory smoke passed.")
        print()
        print("This does not authorize public launch, Pages, domain")
        print("setup, hosting, marketplace submission, package")
        print("publication, support publication, or credentialed checks.")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
