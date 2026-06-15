"""Source-currency probe for the Open Agent Contracts reference portal.

The probe walks the maintainer-edited watchlist YAML, fetches each
primary URL (or reads a local fixture snapshot when in fixture mode),
computes a SHA-256 content hash, and compares the new hash against the
prior hash recorded in the probe state file. On any change it emits a
deterministic issue payload tagged ``source-currency`` naming the page
that needs review. If the change also touches a version-string signal
declared on the row, the payload is additionally tagged
``framework-version-bump``.

Issue-surface write semantics only (CONCEPT-002 plan section 5.2). The
probe never edits page frontmatter, the watchlist YAML, or any portal
data file. The probe's only write surfaces are its own state file
(``--state``) and its issue payload output (``--output-json``); the
state file lives at ``maintainers/source-currency/state/probe-state.json``
in the portal repo and is itself read-only against the watchlist.

Subcommands:

``check``
    Walk the watchlist, fetch each primary URL or load a fixture
    snapshot, compute the hash, compare against the state file, and
    emit issue payloads for changed rows.

``emit-issues``
    Read the issue payload JSON produced by ``check`` and (in the
    portal repo, once G-REPO-HOST clears) open portal-repo issues
    against ``--repo``. This subcommand is intentionally inert in the
    monorepo staging tree: without a portal repo and a portal-repo
    credential surface it only echoes the payloads it would open.

``status``
    Walk a directory of page-frontmatter files and emit the
    maintainer status-dashboard Markdown listing pages whose
    ``freshness_status`` is yellow or red, computed against the
    ``--today`` argument (default: today's date).

The probe is deliberately small, stdlib-shaped, and credential-free.
External calls happen only when ``check`` is invoked without
``--fixture-dir`` and only against the public URLs in the watchlist.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import sys
import urllib.request
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

import yaml


SCHEMA_VERSION = 1
PROBE_USER_AGENT = "AA-source-currency-probe/0.1 (issue-surface-only)"
ISSUE_TITLE_TEMPLATE = "source-currency: {surface} changed"
ISSUE_VERSION_TITLE_TEMPLATE = "framework-version-bump: {surface}"
DEFAULT_LABEL = "source-currency"
VERSION_LABEL = "framework-version-bump"
THIRTY_DAYS = _dt.timedelta(days=30)


def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise SystemExit(f"watchlist {path} did not parse to a mapping")
    return data


def _load_state(path: Optional[Path]) -> Dict[str, Any]:
    if path is None or not path.exists():
        return {"schema_version": SCHEMA_VERSION, "rows": {}}
    with path.open("r", encoding="utf-8") as handle:
        state = json.load(handle)
    if not isinstance(state, dict) or "rows" not in state:
        raise SystemExit(f"state file {path} is not a probe-state JSON object")
    return state


def _save_state(path: Optional[Path], state: Dict[str, Any]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2, sort_keys=True)
        handle.write("\n")


def _fixture_path(fixture_dir: Path, url: str) -> Path:
    """Map a URL to a deterministic local fixture filename.

    The fixture filename is the SHA-256 hex digest of the URL plus
    ``.html``. This keeps the mapping deterministic and avoids any need
    to invent filesystem-safe slugs for arbitrary URL shapes.
    """
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()
    return fixture_dir / f"{digest}.html"


def _fetch_url_bytes(url: str, timeout: float = 30.0) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": PROBE_USER_AGENT},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def _load_url_bytes(url: str, fixture_dir: Optional[Path]) -> bytes:
    if fixture_dir is not None:
        path = _fixture_path(fixture_dir, url)
        if not path.exists():
            raise SystemExit(
                f"fixture missing for url={url}: expected {path}"
            )
        return path.read_bytes()
    return _fetch_url_bytes(url)


def _content_hash(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _version_signal_hits(
    payload_bytes: bytes,
    prior_payload_bytes: Optional[bytes],
    signals: Sequence[str],
) -> List[str]:
    """Return the version signals whose presence changed between snapshots.

    A version-string change is signalled when any declared regex is
    present in exactly one of the two payloads, or when the count of
    matches across the two payloads differs. This is intentionally
    coarse: the probe does not try to parse version numbers itself.
    """
    if not signals:
        return []
    if prior_payload_bytes is None:
        return []
    payload_text = payload_bytes.decode("utf-8", errors="replace")
    prior_text = prior_payload_bytes.decode("utf-8", errors="replace")
    hits: List[str] = []
    for signal in signals:
        try:
            pattern = re.compile(signal, flags=re.IGNORECASE)
        except re.error:
            continue
        new_count = len(pattern.findall(payload_text))
        old_count = len(pattern.findall(prior_text))
        if new_count != old_count:
            hits.append(signal)
    return hits


def _row_id(row: Dict[str, Any]) -> str:
    row_id = row.get("id")
    if not isinstance(row_id, str) or not row_id:
        raise SystemExit(f"watchlist row missing id: {row!r}")
    return row_id


def _row_urls(row: Dict[str, Any]) -> List[str]:
    urls = row.get("primary_urls") or []
    if isinstance(urls, str):
        return [urls]
    return [str(url) for url in urls]


def _build_issue_payload(
    row: Dict[str, Any],
    url_changes: List[Dict[str, Any]],
    version_hits: List[str],
) -> Dict[str, Any]:
    labels = [DEFAULT_LABEL]
    if version_hits:
        labels.append(VERSION_LABEL)
    title = ISSUE_TITLE_TEMPLATE.format(surface=row.get("surface") or _row_id(row))
    if version_hits:
        title = ISSUE_VERSION_TITLE_TEMPLATE.format(
            surface=row.get("surface") or _row_id(row)
        )
    body_lines = [
        f"Watchlist row: {_row_id(row)}",
        f"Surface: {row.get('surface', '(unnamed)')}",
        "",
        "Changed URLs (new content hash differs from prior probe run):",
    ]
    for change in url_changes:
        body_lines.append(
            f"- {change['url']}"
            f"  prior_hash={change.get('prior_hash', '(none)')}"
            f"  new_hash={change['new_hash']}"
        )
    if version_hits:
        body_lines.extend(
            [
                "",
                "Version-signal hits (regex matches whose count moved between snapshots):",
            ]
        )
        for signal in version_hits:
            body_lines.append(f"- {signal}")
    body_lines.extend(
        [
            "",
            (
                "Action: open a portal-repo PR that either re-pins the "
                "framework version and resets verified_on:, or pulls "
                "next_review_due: forward so the time-based badge flip "
                "rerenders yellow at the next build. The probe never "
                "writes to page frontmatter, watchlist.yaml, or any "
                "portal data file."
            ),
        ]
    )
    return {
        "row_id": _row_id(row),
        "surface": row.get("surface"),
        "title": title,
        "labels": labels,
        "body": "\n".join(body_lines),
        "url_changes": url_changes,
        "version_signal_hits": version_hits,
    }


def cmd_check(args: argparse.Namespace) -> int:
    watchlist_path = Path(args.watchlist)
    watchlist = _load_yaml(watchlist_path)
    state_path: Optional[Path] = Path(args.state) if args.state else None
    fixture_dir: Optional[Path] = (
        Path(args.fixture_dir) if args.fixture_dir else None
    )
    state = _load_state(state_path)
    next_rows: Dict[str, Any] = dict(state.get("rows", {}))
    issue_payloads: List[Dict[str, Any]] = []
    for row in watchlist.get("sources", []):
        row_id = _row_id(row)
        prior_row = state.get("rows", {}).get(row_id, {})
        prior_url_hashes: Dict[str, str] = prior_row.get("url_hashes", {})
        prior_url_payloads: Dict[str, str] = prior_row.get("url_payloads", {})
        url_changes: List[Dict[str, Any]] = []
        new_url_hashes: Dict[str, str] = {}
        new_url_payloads: Dict[str, str] = {}
        all_version_hits: List[str] = []
        for url in _row_urls(row):
            payload_bytes = _load_url_bytes(url, fixture_dir)
            new_hash = _content_hash(payload_bytes)
            new_url_hashes[url] = new_hash
            payload_b64 = payload_bytes.hex()
            new_url_payloads[url] = payload_b64
            prior_hash = prior_url_hashes.get(url)
            if prior_hash != new_hash:
                url_changes.append(
                    {
                        "url": url,
                        "prior_hash": prior_hash,
                        "new_hash": new_hash,
                    }
                )
                prior_payload_hex = prior_url_payloads.get(url)
                prior_payload_bytes = (
                    bytes.fromhex(prior_payload_hex)
                    if isinstance(prior_payload_hex, str)
                    and prior_payload_hex
                    else None
                )
                version_hits = _version_signal_hits(
                    payload_bytes,
                    prior_payload_bytes,
                    row.get("version_signals") or [],
                )
                all_version_hits.extend(version_hits)
        next_rows[row_id] = {
            "url_hashes": new_url_hashes,
            "url_payloads": new_url_payloads,
        }
        if url_changes and prior_url_hashes:
            issue_payloads.append(
                _build_issue_payload(row, url_changes, sorted(set(all_version_hits)))
            )
    state_out = {"schema_version": SCHEMA_VERSION, "rows": next_rows}
    if not args.no_state_write:
        _save_state(state_path, state_out)
    output_path: Optional[Path] = (
        Path(args.output_json) if args.output_json else None
    )
    payload_doc = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": _dt.date.today().isoformat(),
        "issue_payloads": issue_payloads,
    }
    if output_path is None:
        json.dump(payload_doc, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as handle:
            json.dump(payload_doc, handle, indent=2, sort_keys=True)
            handle.write("\n")
    return 1 if issue_payloads else 0


def cmd_emit_issues(args: argparse.Namespace) -> int:
    """Print the issue payloads the maintainer would open against --repo.

    This subcommand is intentionally inert in monorepo staging: it does
    not import a public-repo API client and does not call `gh`. After
    the portal repo exists (G-REPO-HOST clear) the maintainer wires the
    actual GitHub API call inside the portal repo's own workflow.
    """
    input_path = Path(args.input_json)
    with input_path.open("r", encoding="utf-8") as handle:
        payload_doc = json.load(handle)
    repo = args.repo or "open-agent-contracts/spec"
    issues = payload_doc.get("issue_payloads", [])
    sys.stdout.write(
        f"# DRY RUN: {len(issues)} issue payloads would be opened "
        f"against {repo}\n"
    )
    for issue in issues:
        sys.stdout.write(
            json.dumps(
                {
                    "repo": repo,
                    "title": issue.get("title"),
                    "labels": issue.get("labels"),
                    "body": issue.get("body"),
                },
                indent=2,
                sort_keys=True,
            )
        )
        sys.stdout.write("\n")
    return 0


def _parse_date(value: str) -> _dt.date:
    return _dt.date.fromisoformat(value)


def _freshness_status(
    today: _dt.date, next_review_due: _dt.date
) -> str:
    if today >= next_review_due:
        return "red"
    if next_review_due - today <= THIRTY_DAYS:
        return "yellow"
    return "green"


def _iter_frontmatter_files(root: Path) -> Iterable[Path]:
    for dirpath, _dirnames, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith((".md", ".markdown")):
                yield Path(dirpath) / filename


def _read_frontmatter(path: Path) -> Optional[Dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    block = text[4:end]
    try:
        data = yaml.safe_load(block)
    except yaml.YAMLError:
        return None
    if not isinstance(data, dict):
        return None
    return data


def cmd_status(args: argparse.Namespace) -> int:
    pages_dir = Path(args.pages_dir)
    today = (
        _parse_date(args.today) if args.today else _dt.date.today()
    )
    rows: List[Dict[str, Any]] = []
    for path in sorted(_iter_frontmatter_files(pages_dir)):
        frontmatter = _read_frontmatter(path)
        if frontmatter is None:
            continue
        due_raw = frontmatter.get("next_review_due")
        if not due_raw:
            continue
        try:
            due_date = (
                due_raw
                if isinstance(due_raw, _dt.date)
                else _parse_date(str(due_raw))
            )
        except ValueError:
            continue
        status = _freshness_status(today, due_date)
        if status == "green":
            continue
        rows.append(
            {
                "path": str(path.relative_to(pages_dir)),
                "verified_on": str(frontmatter.get("verified_on", "")),
                "next_review_due": str(due_date),
                "freshness_status": status,
            }
        )
    red_rows = [row for row in rows if row["freshness_status"] == "red"]
    yellow_rows = [row for row in rows if row["freshness_status"] == "yellow"]
    lines = [
        "---",
        "title: Maintainer status dashboard",
        f"generated_at: {today.isoformat()}",
        f"build_date: {today.isoformat()}",
        "generator: maintainers/source-currency/source_currency_probe.py status",
        "inputs: page frontmatter under the portal source tree",
        "contains_credentials: false",
        "---",
        "",
        "# Maintainer status dashboard",
        "",
        (
            "Generated at build from page frontmatter per CONCEPT-002 "
            "plan section 5.4. Read-only against page frontmatter; "
            "never writes to page frontmatter, the watchlist YAML, or "
            "any portal data file."
        ),
        "",
        "## Past-due pages (red)",
        "",
    ]
    if red_rows:
        for row in red_rows:
            lines.append(
                f"- `{row['path']}` "
                f"(verified_on={row['verified_on']}, "
                f"next_review_due={row['next_review_due']})"
            )
    else:
        lines.append(f"No past-due pages on the {today.isoformat()} build.")
    lines.extend(["", "## Pages within the 30-day review window (yellow)", ""])
    if yellow_rows:
        for row in yellow_rows:
            lines.append(
                f"- `{row['path']}` "
                f"(verified_on={row['verified_on']}, "
                f"next_review_due={row['next_review_due']})"
            )
    else:
        lines.append(
            f"No pages within the 30-day review window on the "
            f"{today.isoformat()} build."
        )
    output = "\n".join(lines) + "\n"
    output_path: Optional[Path] = (
        Path(args.output) if args.output else None
    )
    if output_path is None:
        sys.stdout.write(output)
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Source-currency probe for the Open Agent Contracts "
            "reference portal."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser(
        "check",
        help=(
            "Walk the watchlist, fetch each URL or load fixtures, "
            "compute hashes, compare against the state file, emit "
            "issue payloads for changed rows."
        ),
    )
    check.add_argument(
        "--watchlist",
        required=True,
        help="Path to the watchlist YAML.",
    )
    check.add_argument(
        "--state",
        default=None,
        help=(
            "Path to the probe state JSON file. Created on first run "
            "with no issue payloads; updated in place on every "
            "subsequent run unless --no-state-write is passed."
        ),
    )
    check.add_argument(
        "--fixture-dir",
        default=None,
        help=(
            "Optional directory of pre-staged URL snapshots used "
            "instead of live HTTP fetches. The filename for each URL "
            "is the SHA-256 hex digest of the URL plus .html."
        ),
    )
    check.add_argument(
        "--output-json",
        default=None,
        help=(
            "Optional path to write the issue payload JSON. If "
            "omitted, the payload is printed to standard output."
        ),
    )
    check.add_argument(
        "--no-state-write",
        action="store_true",
        help=(
            "Do not update the state file even if --state is set. "
            "Useful for read-only verification."
        ),
    )
    check.set_defaults(func=cmd_check)

    emit = subparsers.add_parser(
        "emit-issues",
        help=(
            "Echo the issue payloads that would be opened against "
            "--repo. Inert in monorepo staging; the actual portal-repo "
            "issue calls are wired only after G-REPO-HOST clears."
        ),
    )
    emit.add_argument(
        "--input-json",
        required=True,
        help="Path to the issue payload JSON produced by `check`.",
    )
    emit.add_argument(
        "--repo",
        default=None,
        help=(
            "Portal repo identifier (e.g. owner/name). Defaults to "
            "the open-agent-contracts/spec literal."
        ),
    )
    emit.set_defaults(func=cmd_emit_issues)

    status = subparsers.add_parser(
        "status",
        help=(
            "Generate the maintainer status dashboard from page "
            "frontmatter (yellow / red rows only)."
        ),
    )
    status.add_argument(
        "--pages-dir",
        required=True,
        help="Directory containing portal pages with YAML frontmatter.",
    )
    status.add_argument(
        "--today",
        default=None,
        help=(
            "Optional ISO date used as 'today' for the freshness "
            "calculation. Default: today's date."
        ),
    )
    status.add_argument(
        "--output",
        default=None,
        help="Optional output path. Default: standard output.",
    )
    status.set_defaults(func=cmd_status)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
