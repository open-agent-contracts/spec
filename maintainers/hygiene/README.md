# Portal-repo Hygiene CI

Local staging artifact for the FEATURE-007 public reference portal.
This is not wired into any live portal repository. After maintainer
transcription, the workflow will run as required CI inside the
public portal repo on every pull request and on the nightly cron
build.

## What this tree IS

A small Python-standard-library hygiene CI tool, a fixture set, a
focused test suite, and a staged GitHub Actions workflow. The tool
implements the four CONCEPT-002 plan section 7.5 checks plus the
FEATURE-007 plan section 4.1 placeholder always-block extension.

## What this tree is NOT

- It is NOT wired into a live portal repository. Local staging only.
- It does NOT carry real credentials, repository secrets, resolved
  public repo identifiers, hosting infrastructure, or domain names.
- It does NOT replace any FEATURE-007 plan section 4.1 placeholder
  with operator-locked values. The CI blocks every placeholder
  literal in any portal-bound surface; placeholder resolution is
  operator-driven, not tool-driven.
- It is NOT the contributor-side transcription helper (S-9B). That
  helper is a sibling write scope and lives permanently in the
  monorepo; this tree is the load-bearing public-safety guarantee
  inside the portal repo itself.

## The four CONCEPT-002 plan section 7.5 checks

| Step | Check | This tree |
|---|---|---|
| 1 | Source-tree scan against the CONCEPT-002 plan section 7.1 hard non-export list (always-block). | `hygiene_ci.py scan <tree>` |
| 2 | Source-tree scan against the CONCEPT-002 plan section 7.4 substitution-map row policies (always-block plus one path-conditional public vendor row). | `hygiene_ci.py scan <tree>` |
| 3 | Post-render scan applying the same row policies to the rendered output tree. | `hygiene_ci.py scan <rendered-tree>` |
| 4 | Deterministic-render integrity check: byte-for-byte compare of two rendered output trees by file set and per-file SHA-256. | `hygiene_ci.py render-compare <a> <b>` |

Steps 1, 2, and 3 share a single scan engine; the difference is
only which tree is scanned. The hygiene CI staging workflow runs
all four steps; see `hygiene-ci.yml`.

## Row-policy model

Every policy row is one of:

- **always-block**: any occurrence of the row pattern in a
  portal-bound surface is a build failure.
- **path-conditional**: an occurrence is allowed only when the
  containing file's portal-relative path matches one of the row's
  allowed paths; outside those paths the occurrence is a build
  failure.

v0 carries exactly one path-conditional row: the
CONCEPT-002 plan section 7.4 public vendor row. The allowed
paths for the public vendor row are:

- the `mappings/<vendor>/` prefix for that vendor's mapping page;
- the `compat/<vendor>-plugin.yaml` plugin compatibility row;
- the `compat/index.html` generated registry index page.

Outside those paths the public vendor row fires; everywhere else
the row remains always-block-shaped.

Every CONCEPT-002 plan section 7.1 row is always-block.

Every FEATURE-007 plan section 4.1 placeholder literal is
always-block in any portal-bound surface. v0 carries eight
placeholder rows: P-1 through P-8.

Each row carries a citation. Failures print the offending file
and line and the source-plan citation.

## FEATURE-007 plan section 4.1 placeholder coverage

All eight placeholders are always-block in any portal-bound
surface:

| Row | Source | Mode |
|---|---|---|
| P-1 | FEATURE-007 plan section 4.1 P-1 | always-block |
| P-2 | FEATURE-007 plan section 4.1 P-2 | always-block |
| P-3 | FEATURE-007 plan section 4.1 P-3 | always-block |
| P-4 | FEATURE-007 plan section 4.1 P-4 | always-block |
| P-5 | FEATURE-007 plan section 4.1 P-5 | always-block |
| P-6 | FEATURE-007 plan section 4.1 P-6 | always-block |
| P-7 | FEATURE-007 plan section 4.1 P-7 | always-block |
| P-8 | FEATURE-007 plan section 4.1 P-8 | always-block |

Maintainers do not edit the placeholder ids inside `hygiene_ci.py`
directly; the ids are assembled from non-matching fragments to
avoid the self-failing-policy trap (see below). Adding a new
placeholder row requires a plan amendment to FEATURE-007 plan
section 4.1 first.

## Load-bearing fixture exclusion

The constant `FIXTURE_EXCLUDE_PREFIX` inside `hygiene_ci.py` is
the exact path-glob prefix:

```
maintainers/hygiene/fixtures/
```

This constant is used by:

- the production source-tree scan (steps 1 and 2);
- the production post-render scan (step 3);
- the focused fixture regression suite, which points the scanner at
  fixture subtrees directly and separately proves the exclusion is
  load-bearing;
- this README and the hygiene receipt.

Removing or weakening the exclusion would cause the production
hygiene scan to fail itself on the negative fixtures it is
intended to exclude. The fixtures exist to be refused; the
production scan exists to refuse real authoring paths. Mixing
them collapses the contract.

The corresponding glob form is `maintainers/hygiene/fixtures/**`
and is exposed as `FIXTURE_EXCLUDE_GLOB` for documentation parity
with grep-style invocations.

## Avoiding the self-failing policy-file trap

`hygiene_ci.py`, this `README.md`, `HYGIENE-RECEIPT.md`,
`hygiene-ci.yml`, and `tests/test_hygiene_ci.py` are all
portal-bound staging files. Production scans must walk them
without tripping.

To avoid that trap:

- The tool source assembles every policy literal at module load
  from non-matching fragments. The full literal never appears as
  a contiguous byte sequence in `hygiene_ci.py`.
- Documentation files (this README, the hygiene receipt, the
  workflow) cite the source-plan rows and the fixture filenames
  rather than restating the blocked literals.
- The test file lives outside `fixtures/` and therefore must not
  carry raw literals either; it asserts behavior through
  citation strings and exit codes rather than constructing the
  literals itself.

Raw negative terms and raw placeholder literals belong only
inside `fixtures/`, which the production scan excludes.

## Staged file inventory

```
maintainers/hygiene/
  README.md                       (this file)
  HYGIENE-RECEIPT.md
  hygiene_ci.py
  hygiene-ci.yml
  tests/
    test_hygiene_ci.py
  fixtures/
    README.md
    clean-portal/...
    dirty-private-role/...
    dirty-internal-tooling/...
    vendor-allowed-mapping/...
    vendor-allowed-compat-yaml/...
    vendor-allowed-compat-index/...
    vendor-disallowed-other-mapping/...
    vendor-disallowed-other-compat/...
    dirty-internal-substrate/...
    placeholder-p1/...
    placeholder-p2-link/...
    placeholder-p7-frontmatter/...
    no-placeholders/...
    render-pair-clean/{a,b}/...
    render-pair-divergent/{a,b}/...
    tripwire/...
```

## How to run the tool locally against fixture trees

Source-tree / post-render scan on a single fixture tree:

```
python3 hygiene_ci.py scan fixtures/clean-portal
python3 hygiene_ci.py scan fixtures/dirty-private-role
python3 hygiene_ci.py scan fixtures/placeholder-p1
```

The first command exits `0`. The second and third exit `1` and
print one or more line-oriented violation reports to stderr.

Deterministic render comparison:

```
python3 hygiene_ci.py render-compare \
  fixtures/render-pair-clean/a fixtures/render-pair-clean/b
python3 hygiene_ci.py render-compare \
  fixtures/render-pair-divergent/a fixtures/render-pair-divergent/b
```

The first exits `0`. The second exits `1` and names the divergent
file.

Focused test suite (27 tests, standard library only):

```
python3 -m unittest discover -s tests -v
```

## How the future portal repo would wire the staged workflow

After transcription the workflow file lives at
`/maintainers/hygiene/hygiene-ci.yml` at the portal repo root.
The portal repo's `.github/workflows/hygiene.yml` (or equivalent
platform shape) invokes it on every pull request, every nightly
cron build, and on manual dispatch.

The staged workflow shows the four steps in order:

1. Source-tree hygiene scan against the portal repo source tree
   (`hygiene_ci.py scan .`), honoring the fixture exclusion.
2. Two clean-workspace renders of the portal site.
3. Post-render hygiene scan against the first render tree
   (`hygiene_ci.py scan build/first`).
4. Render integrity check comparing the two renders
   (`hygiene_ci.py render-compare build/first build/second`).

Plus a focused fixture regression suite. The suite points at
individual clean, dirty, allowed, and disallowed fixture subtrees
directly, and it also disables the fixture exclusion against the
staged tree to prove the exclusion is load-bearing.

The two render commands are placeholder stubs in this local staging
artifact. Until a future portal-repo maintainer replaces them with
the real static-site build command, the workflow-level deterministic
render step proves wiring shape only; the focused fixture tests
exercise real render-compare pass/fail behavior.

## Acceptance

| Acceptance (CONCEPT-002 plan section 8.9 + FEATURE-007 plan section 6.9) | Evidence |
|---|---|
| Clean fixture tree passes (source + post-render). | `tests/test_hygiene_ci.py::CleanScanTests`, `RenderCompareTests::test_byte_identical_pair_passes` |
| Path-conditional public vendor row allowed under mapping prefix, compat plugin yaml, compat index html. | `VendorPathConditionalTests::test_vendor_allowed_*` (three tests) |
| Path-conditional public vendor row blocked outside allowed paths (mapping + compat). | `VendorPathConditionalTests::test_vendor_disallowed_*` (two tests) |
| Internal authoring substrate row blocked under any path including an allowed mapping path. | `DirtyScanTests::test_internal_substrate_fixture_fails_under_allowed_mapping_path` |
| Deterministic render compare green on byte-identical pair, red on divergent pair naming the divergent file. | `RenderCompareTests::test_*` (two tests) |
| Hygiene receipt records 0 portal-repo writes. | `HYGIENE-RECEIPT.md` |
| Every FEATURE-007 plan section 4.1 placeholder always-block. | `PlaceholderAlwaysBlockTests::test_*` (four tests) + `PolicyTableTests::test_eight_placeholder_rows_present` |
| Fixture exclusion is load-bearing harness invariant. | `FixtureExclusionConstantTests::test_*` + `FixtureIsolationTests::test_*` |
