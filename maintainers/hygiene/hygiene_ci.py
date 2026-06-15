#!/usr/bin/env python3
"""Portal-repo hygiene CI for FEATURE-007 v0.

Implements the four CONCEPT-002 plan section 7.5 checks plus the
FEATURE-007 plan section 4.1 placeholder always-block extension:

  1. Source-tree scan against the CONCEPT-002 plan section 7.1 hard
     non-export list (always-block; expressible patterns).
  2. Source-tree scan against the CONCEPT-002 plan section 7.4
     substitution-map row policies (always-block plus one v0
     path-conditional public vendor row).
  3. Post-render scan applying the same row policies to a rendered
     output tree.
  4. Deterministic render integrity check: byte-for-byte compare of
     two rendered output trees by file set and per-file SHA-256.

Also enforces FEATURE-007 plan section 4.1 placeholder literals
(P-1 through P-8) as always-block in any portal-bound surface.

Fixture trees under the FIXTURE_EXCLUDE_PREFIX path are skipped by
production scans and exercised explicitly by the negative-fixture
test step. The exclusion is load-bearing: without it the production
scan would trip on the negative fixtures that exist to be refused.

The tool intentionally avoids carrying raw policy literals in its
own source. Each row pattern is assembled at module load from
non-matching fragments, so the production scan does not self-hit
when it walks this file. See README for the harness invariant.
"""

import argparse
import hashlib
import os
import re
import sys


# ----------------------------------------------------------------------
# Load-bearing fixture exclusion constant.
#
# Used by:
#   - production source-tree scan (step 1, 2);
#   - production post-render scan (step 3);
#   - the negative-fixture test step (paths it points at start with
#     this prefix when invoked from the portal-repo root);
#   - README and HYGIENE-RECEIPT documentation.
#
# Removing or weakening this exclusion would cause the production
# hygiene scan to fail itself the moment any negative fixture exists,
# even when no real authoring path has leaked a policy literal.
# ----------------------------------------------------------------------

FIXTURE_EXCLUDE_GLOB = "maintainers/hygiene/fixtures/**"
FIXTURE_EXCLUDE_PREFIX = "maintainers/hygiene/fixtures/"


# ----------------------------------------------------------------------
# Files the production scan reads. The portal v0 ships markdown,
# YAML, HTML, and a small number of plain-text adjuncts. Binary
# rendered assets (images, fonts) are not scanned because the
# blocked-term policy is text-shaped.
# ----------------------------------------------------------------------

SCAN_EXTENSIONS = (
    ".md",
    ".markdown",
    ".yaml",
    ".yml",
    ".html",
    ".htm",
    ".txt",
    ".json",
)


# ----------------------------------------------------------------------
# Policy literals assembled from non-matching fragments so this file
# is not a self-hit for the production scan.
# ----------------------------------------------------------------------


def _join(*parts):
    return "".join(parts)


# FEATURE-007 plan section 4.1 placeholder literals (P-1 .. P-8).
# The shared prefix "AA" plus suffix produced by joining "_PLACE" with
# "HOLDER" only assembles into the full literal at runtime; the source
# bytes never carry the full literal.

_PH_PREFIX = "AA"
_PH_SUFFIX = _join("_PLACE", "HOLDER")

_PH_MIDS = [
    ("P-1", "_PUBLIC_NAME"),
    ("P-2", "_DOMAIN"),
    ("P-3", "_PACKAGE_ID"),
    ("P-4", "_MARKETPLACE_IDENTITY"),
    ("P-5", "_SUPPORT_IDENTITY"),
    ("P-6", "_LICENSE_STACK"),
    ("P-7", "_SCHEMA_ID"),
    ("P-8", "_PORTAL_REPO"),
]

PLACEHOLDER_LITERALS = [
    (row, _PH_PREFIX + mid + _PH_SUFFIX) for row, mid in _PH_MIDS
]


# CONCEPT-002 plan section 7.1 + section 7.4 row 1: private role
# tokens. Each name is assembled from a head and a fixed "-bear"
# suffix; the literal is only assembled at runtime.

_ROLE_BEAR_SUFFIX = _join("-", "bear")
_ROLE_HEADS = [
    "audit",
    "operator",
    "story",
    "scribe",
    "harvester",
    "scheduler",
    "steward",
]
ROLE_LITERALS = [head + _ROLE_BEAR_SUFFIX for head in _ROLE_HEADS]
ROLE_CUB_LITERAL = _join("bear", "-cub")


# CONCEPT-002 plan section 7.4 internal authoring substrate row.
# Assembled fragment-wise.
SUBSTRATE_LITERAL = _join("CAI", "RN")


# CONCEPT-002 plan section 7.4 BEAR doctrine row. The prefix is
# assembled the same way; the suffixed forms are word-boundary
# matched as the full literal.
BEAR_PREFIX_LITERAL = _join("BE", "AR")
BEAR_DOCTRINE_SUFFIXES = [
    "-CONSTITUTION",
    "-DOMAINS",
    "-PHASES",
    "-COUNCIL",
    "-CREED",
    "-MYTHOS",
]
BEAR_DOCTRINE_LITERALS = [
    BEAR_PREFIX_LITERAL + suf for suf in BEAR_DOCTRINE_SUFFIXES
]
BEAR_PRINCIPLE_LITERAL = _join("PRINCIPLE", "-001")


# CONCEPT-002 plan section 7.4 LEO row. Private operator / customer
# identity. Each literal is assembled fragment-wise.
LEO_LITERAL = _join("L", "EO")
LEO_CORE_LITERAL = _join("L", "EO Core")
LIONS_LITERAL = _join("Lio", "ns")
LIONS_FULL_LITERAL = _join("Lio", "ns Equipment UK")
LEO_PREFIX_FRAGMENT = _join("le", "o_")


# CONCEPT-002 plan section 7.4 orchestrator row. Private orchestrator
# names and commands.
BIN_PREFIX = _join("bin", "/")
ORCH_BIN_TAILS = [
    "loom",
    "operator-bear",
    "trinity",
    "scheduler-bear",
    "leo-notify",
]
ORCH_BIN_LITERALS = [BIN_PREFIX + tail for tail in ORCH_BIN_TAILS]
ORCH_NAME_TRINITY = _join("Trin", "ity")
ORCH_NAME_LOOM = _join("Lo", "om")


# CONCEPT-002 plan section 7.1 + section 7.4 monorepo path row.
# Internal authoring substrate paths.
MONOREPO_PATH_PROJECT = _join("projects/", "agent-augmentation/")
MONOREPO_PATH_LEO_DOC = _join("docs/", "leo-doctrine/")
MONOREPO_PATH_BEAR_DOC = _join("docs/", "bear-doctrine/")


# CONCEPT-002 plan section 7.4 public vendor path-conditional row.
# Assembled fragment-wise so this file does not carry the literal.
VENDOR_PUBLIC_LITERAL = _join("Claw", "Magic")

# Allowed portal-relative path shapes for the public vendor row.
VENDOR_ALLOWED_PREFIXES = (
    _join("mappings/clawmagic/"),
)
VENDOR_ALLOWED_FILES = (
    _join("compat/clawmagic-plugin.yaml"),
    _join("compat/index.html"),
)


# ----------------------------------------------------------------------
# Policy table.
#
# Each entry is:
#   (row_id, regex_pattern_source, citation, reason, policy,
#    allowed_paths_or_None)
#
# policy is "always_block" or "path_conditional". For
# "path_conditional" entries, allowed_paths_or_None is a tuple
# (prefixes, files) of portal-relative path shapes where the literal
# is allowed.
# ----------------------------------------------------------------------


def _word_boundary(literal):
    return r"\b" + re.escape(literal) + r"\b"


def _bare_literal(literal):
    return re.escape(literal)


def _build_policy_rows():
    rows = []

    # FEATURE-007 plan section 4.1 placeholder literals (P-1 .. P-8).
    for row_id, literal in PLACEHOLDER_LITERALS:
        rows.append((
            row_id,
            _bare_literal(literal),
            "FEATURE-007 plan section 4.1 " + row_id,
            "placeholder literal " + row_id,
            "always_block",
            None,
        ))

    # CONCEPT-002 plan section 7.1 hard non-export list (role
    # mythology row + internal monorepo path row).
    for literal in ROLE_LITERALS:
        rows.append((
            "S71-roles",
            _word_boundary(literal),
            "CONCEPT-002 plan section 7.1 hard non-export role row",
            "private role-token",
            "always_block",
            None,
        ))
    rows.append((
        "S71-roles",
        _word_boundary(ROLE_CUB_LITERAL),
        "CONCEPT-002 plan section 7.1 hard non-export role row",
        "private role-token",
        "always_block",
        None,
    ))

    # CONCEPT-002 plan section 7.4 BEAR doctrine row.
    for literal in BEAR_DOCTRINE_LITERALS:
        rows.append((
            "S74-doctrine",
            _word_boundary(literal),
            "CONCEPT-002 plan section 7.4 doctrine row",
            "internal doctrine name",
            "always_block",
            None,
        ))
    rows.append((
        "S74-doctrine",
        _word_boundary(BEAR_PRINCIPLE_LITERAL),
        "CONCEPT-002 plan section 7.4 doctrine row",
        "internal doctrine name",
        "always_block",
        None,
    ))
    rows.append((
        "S74-doctrine",
        _word_boundary(BEAR_PREFIX_LITERAL),
        "CONCEPT-002 plan section 7.4 doctrine row",
        "internal doctrine prefix",
        "always_block",
        None,
    ))

    # CONCEPT-002 plan section 7.4 LEO / customer-identity row.
    rows.append((
        "S74-leo",
        _word_boundary(LIONS_FULL_LITERAL),
        "CONCEPT-002 plan section 7.4 customer identity row",
        "private operator entity",
        "always_block",
        None,
    ))
    rows.append((
        "S74-leo",
        _word_boundary(LEO_CORE_LITERAL),
        "CONCEPT-002 plan section 7.4 customer identity row",
        "internal product line",
        "always_block",
        None,
    ))
    rows.append((
        "S74-leo",
        _word_boundary(LEO_LITERAL),
        "CONCEPT-002 plan section 7.4 customer identity row",
        "internal product name",
        "always_block",
        None,
    ))
    rows.append((
        "S74-leo",
        _word_boundary(LIONS_LITERAL),
        "CONCEPT-002 plan section 7.4 customer identity row",
        "private operator entity",
        "always_block",
        None,
    ))
    rows.append((
        "S74-leo",
        r"\b" + re.escape(LEO_PREFIX_FRAGMENT) + r"[A-Za-z][A-Za-z0-9_]*",
        "CONCEPT-002 plan section 7.4 customer identity row",
        "internal namespace identifier",
        "always_block",
        None,
    ))

    # CONCEPT-002 plan section 7.4 orchestrator row.
    for literal in ORCH_BIN_LITERALS:
        rows.append((
            "S74-orchestrator",
            _word_boundary(literal),
            "CONCEPT-002 plan section 7.4 orchestrator row",
            "private orchestrator command",
            "always_block",
            None,
        ))
    rows.append((
        "S74-orchestrator",
        _word_boundary(ORCH_NAME_TRINITY),
        "CONCEPT-002 plan section 7.4 orchestrator row",
        "private orchestrator name",
        "always_block",
        None,
    ))
    rows.append((
        "S74-orchestrator",
        _word_boundary(ORCH_NAME_LOOM),
        "CONCEPT-002 plan section 7.4 orchestrator row",
        "private orchestrator name",
        "always_block",
        None,
    ))

    # CONCEPT-002 plan section 7.1 + section 7.4 internal monorepo
    # path row.
    for literal in (
        MONOREPO_PATH_PROJECT,
        MONOREPO_PATH_LEO_DOC,
        MONOREPO_PATH_BEAR_DOC,
    ):
        rows.append((
            "S74-monorepo-path",
            _bare_literal(literal),
            "CONCEPT-002 plan section 7.4 monorepo path row",
            "internal monorepo path",
            "always_block",
            None,
        ))

    # CONCEPT-002 plan section 7.4 internal authoring substrate row.
    rows.append((
        "S74-substrate",
        _word_boundary(SUBSTRATE_LITERAL),
        "CONCEPT-002 plan section 7.4 internal authoring substrate row",
        "internal authoring substrate name",
        "always_block",
        None,
    ))

    # CONCEPT-002 plan section 7.4 public vendor path-conditional row.
    rows.append((
        "S74-public-vendor",
        _word_boundary(VENDOR_PUBLIC_LITERAL),
        "CONCEPT-002 plan section 7.4 public vendor path-conditional row",
        "public vendor name outside allowed portal paths",
        "path_conditional",
        (VENDOR_ALLOWED_PREFIXES, VENDOR_ALLOWED_FILES),
    ))

    return rows


POLICY_ROWS = _build_policy_rows()
_POLICY_COMPILED = [
    (row_id, re.compile(pattern), citation, reason, policy, allowed)
    for (row_id, pattern, citation, reason, policy, allowed) in POLICY_ROWS
]


# ----------------------------------------------------------------------
# Scan helpers.
# ----------------------------------------------------------------------


def _normalize_rel_path(rel_path):
    """Return rel_path with forward-slash separators, no leading slash."""
    norm = rel_path.replace(os.sep, "/")
    while norm.startswith("./"):
        norm = norm[2:]
    if norm.startswith("/"):
        norm = norm.lstrip("/")
    return norm


def _path_allowed_for_row(rel_path, allowed):
    """Return True if rel_path is inside one of the allowed prefixes or
    matches one of the allowed file paths for a path-conditional row.
    rel_path is the file's path relative to the scan root, normalized
    with forward slashes and no leading slash.
    """
    if allowed is None:
        return False
    prefixes, files = allowed
    for prefix in prefixes:
        if rel_path.startswith(prefix):
            return True
    for path in files:
        if rel_path == path:
            return True
    return False


def _iter_scan_files(scan_root, include_fixtures):
    """Yield (absolute_path, rel_path) for every file under scan_root
    that should be scanned. rel_path uses forward-slash separators.
    Skips files under FIXTURE_EXCLUDE_PREFIX when include_fixtures is
    False (the production default).
    """
    for dirpath, dirnames, filenames in os.walk(scan_root):
        # Stable directory order so error reports are deterministic.
        dirnames.sort()
        filenames.sort()
        for name in filenames:
            abs_path = os.path.join(dirpath, name)
            rel_path = _normalize_rel_path(
                os.path.relpath(abs_path, scan_root)
            )
            if not include_fixtures and rel_path.startswith(
                FIXTURE_EXCLUDE_PREFIX
            ):
                continue
            ext = os.path.splitext(name)[1].lower()
            if ext not in SCAN_EXTENSIONS:
                continue
            yield abs_path, rel_path


def _read_text(abs_path):
    with open(abs_path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def _scan_file(rel_path, text):
    """Return list of violation tuples for a single file.

    Each tuple is (rel_path, line_no, line_text, match_text, row_id,
    citation, reason).
    """
    violations = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for (
            row_id,
            compiled,
            citation,
            reason,
            policy,
            allowed,
        ) in _POLICY_COMPILED:
            for match in compiled.finditer(line):
                if policy == "path_conditional" and _path_allowed_for_row(
                    rel_path, allowed
                ):
                    continue
                violations.append(
                    (
                        rel_path,
                        line_no,
                        line.rstrip(),
                        match.group(0),
                        row_id,
                        citation,
                        reason,
                    )
                )
    return violations


def scan_tree(scan_root, include_fixtures=False):
    """Run the source-tree / post-render scan on scan_root and return
    a list of violation tuples.
    """
    all_violations = []
    for abs_path, rel_path in _iter_scan_files(scan_root, include_fixtures):
        try:
            text = _read_text(abs_path)
        except OSError as exc:
            all_violations.append(
                (
                    rel_path,
                    0,
                    "",
                    "",
                    "scan-error",
                    "hygiene-ci internal",
                    "could not read file: " + str(exc),
                )
            )
            continue
        all_violations.extend(_scan_file(rel_path, text))
    return all_violations


# ----------------------------------------------------------------------
# Deterministic render integrity check (step 4).
# ----------------------------------------------------------------------


def _hash_file(abs_path):
    h = hashlib.sha256()
    with open(abs_path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _index_tree(root):
    """Return dict rel_path -> sha256 for every regular file in root."""
    index = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        filenames.sort()
        for name in filenames:
            abs_path = os.path.join(dirpath, name)
            rel_path = _normalize_rel_path(
                os.path.relpath(abs_path, root)
            )
            index[rel_path] = _hash_file(abs_path)
    return index


def render_compare(tree_a, tree_b):
    """Compare two rendered output trees by file set + per-file SHA-256.

    Return list of difference tuples (rel_path, kind, detail).
    kind is one of: "differs", "missing_in_a", "missing_in_b".
    Empty list means byte-identical.
    """
    index_a = _index_tree(tree_a)
    index_b = _index_tree(tree_b)
    diffs = []
    all_rels = sorted(set(index_a.keys()) | set(index_b.keys()))
    for rel_path in all_rels:
        in_a = rel_path in index_a
        in_b = rel_path in index_b
        if in_a and not in_b:
            diffs.append((rel_path, "missing_in_b", index_a[rel_path]))
        elif in_b and not in_a:
            diffs.append((rel_path, "missing_in_a", index_b[rel_path]))
        elif index_a[rel_path] != index_b[rel_path]:
            diffs.append(
                (
                    rel_path,
                    "differs",
                    "a=" + index_a[rel_path][:12]
                    + " b=" + index_b[rel_path][:12],
                )
            )
    return diffs


# ----------------------------------------------------------------------
# CLI.
# ----------------------------------------------------------------------


def _format_scan_violation(v):
    rel_path, line_no, line_text, match_text, row_id, citation, reason = v
    return (
        rel_path + ":" + str(line_no) + ": "
        + reason + " " + repr(match_text)
        + " (cite " + citation + ")"
    )


def _format_scan_violation_context(v):
    rel_path, line_no, line_text, match_text, row_id, citation, reason = v
    return "  " + rel_path + ":" + str(line_no) + ": " + line_text


def _cmd_scan(args):
    scan_root = args.tree
    if not os.path.isdir(scan_root):
        sys.stderr.write(
            "hygiene-ci: scan root is not a directory: " + scan_root + "\n"
        )
        return 2
    violations = scan_tree(
        scan_root, include_fixtures=args.include_fixtures
    )
    if violations:
        sys.stderr.write("hygiene-ci: portal-bound violations found\n")
        for v in violations:
            sys.stderr.write(_format_scan_violation(v) + "\n")
            sys.stderr.write(_format_scan_violation_context(v) + "\n")
        sys.stderr.write(
            "hygiene-ci: "
            + str(len(violations))
            + " violations\n"
        )
        return 1
    sys.stdout.write(
        "hygiene-ci: scan clean (root=" + scan_root + ")\n"
    )
    return 0


def _cmd_render_compare(args):
    for label, tree in (("a", args.tree_a), ("b", args.tree_b)):
        if not os.path.isdir(tree):
            sys.stderr.write(
                "hygiene-ci: render-compare tree "
                + label
                + " is not a directory: "
                + tree
                + "\n"
            )
            return 2
    diffs = render_compare(args.tree_a, args.tree_b)
    if diffs:
        sys.stderr.write(
            "hygiene-ci: render-compare failed\n"
        )
        for rel_path, kind, detail in diffs:
            sys.stderr.write(
                rel_path + ": " + kind + " (" + detail + ")\n"
            )
        sys.stderr.write(
            "hygiene-ci: " + str(len(diffs)) + " divergent files\n"
        )
        return 1
    sys.stdout.write(
        "hygiene-ci: render-compare clean (a="
        + args.tree_a
        + " b="
        + args.tree_b
        + ")\n"
    )
    return 0


def _build_parser():
    parser = argparse.ArgumentParser(
        prog="hygiene-ci",
        description=(
            "FEATURE-007 portal-repo hygiene CI. Implements the four "
            "CONCEPT-002 plan section 7.5 checks: source-tree scan "
            "(steps 1 and 2), post-render scan (step 3), deterministic "
            "render compare (step 4); plus the FEATURE-007 plan section "
            "4.1 placeholder always-block extension. Fixture trees "
            "under maintainers/hygiene/fixtures/ are skipped by default "
            "(production scans) and exercised explicitly by the "
            "negative-fixture test step."
        ),
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    scan_p = sub.add_parser(
        "scan",
        help=(
            "Walk a source tree or rendered output tree and report "
            "portal-bound violations against the row policies "
            "(steps 1, 2, 3)."
        ),
    )
    scan_p.add_argument(
        "tree",
        help="Root directory to scan.",
    )
    scan_p.add_argument(
        "--include-fixtures",
        action="store_true",
        help=(
            "Disable the maintainers/hygiene/fixtures/ exclusion. "
            "Used by the negative-fixture test step when invoked "
            "from the portal-repo root; not used in production."
        ),
    )
    scan_p.set_defaults(func=_cmd_scan)

    compare_p = sub.add_parser(
        "render-compare",
        help=(
            "Compare two rendered output trees by file set and "
            "per-file SHA-256 (step 4 deterministic render check)."
        ),
    )
    compare_p.add_argument("tree_a", help="First rendered output tree.")
    compare_p.add_argument("tree_b", help="Second rendered output tree.")
    compare_p.set_defaults(func=_cmd_render_compare)

    return parser


def main(argv=None):
    parser = _build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
