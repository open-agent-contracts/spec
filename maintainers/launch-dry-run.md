# V0 Launch Dry-Run

Status: local staging only.

This checklist is for a future maintainer walking the v0 portal toward public
launch. It is not a launch announcement and it is not signed off for
publication.

## Boundary

This dry-run does not create a public repository, register a domain, configure
hosting, publish content, transcribe to a public portal repo, replace
placeholders, claim support availability, accept external PRs, run credentialed
checks, submit anything, send messages, spend money, or announce launch.

## Placeholder Resolution Checklist

Every placeholder below must be replaced with an operator-locked value before
the corresponding surface is transcribed to the public portal repo or included
in a launch branch.

| Slot | Placeholder | Required gate | Local surfaces to inspect | Current status |
|---|---|---|---|---|
| P-1 | `Open Agent Contracts` | G-NAME-BRAND + G-PROJECT-NAME | S-1, S-2, S-7, S-8 | OPEN - replacement evidence not recorded. |
| P-2 | `openagentcontracts.org` | G-NAME-DOMAIN + G-DOMAIN + G6 irreversible boundary | S-1, S-8 | OPEN - replacement evidence not recorded. |
| P-3 | `agent-contract-kit` | G-NAME-PACKAGE + G-PROJECT-NAME | S-7, S-8 | OPEN - replacement evidence not recorded. |
| P-4 | `Agent Contract Kit` | G-NAME-CATEGORY + G-NAME-PACKAGE + FEATURE-006 plan-leg shape | S-1 reserved footer slot, future S-4 link only | OPEN - replacement evidence not recorded. |
| P-5 | `support@openagentcontracts.org` | G-NAME-SUPPORT | S-1, S-8 | OPEN - replacement evidence not recorded. |
| P-6 | `schema/examples CC0-1.0; validator/plugin code Apache-2.0; portal/docs CC BY 4.0` | G-NAME-LICENSE + G-LICENSE | S-1, S-8 | OPEN - replacement evidence not recorded. |
| P-7 | `https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json` | G-NAME-BRAND + G-PROJECT-NAME + artifact-name + API-name | S-2, S-3 wrapping page, S-4 mapping pages | OPEN - replacement evidence not recorded. |
| P-8 | `open-agent-contracts/spec` | G-REPO-HOST + G-PROJECT-NAME + G-HOSTING | S-1, S-6, S-8 | OPEN - replacement evidence not recorded. |

Replacement evidence is not yet present. Add one dated evidence row per slot
when the operator-gated value has been applied in the public portal branch.
Until then, this section is an explicit launch blocker, not a sign-off.

## Launch Gate Checklist

| Gate | Local dry-run result | Public-launch status |
|---|---|---|
| S-1 IA shell present | Local smoke checks the IA files. | Must be transcribed to public repo after repo gate. |
| S-2 standard pages present | Local smoke checks all standard pages. | Must be transcribed after placeholder replacement. |
| S-3 examples present and validator-clean | Local build evidence says six bodies validate; S-10 closeout reruns validation. | Must be transcribed after schema-id placeholder replacement. |
| S-4 mappings present | Local smoke checks eight mapping pages. | Must be transcribed after source-currency and hygiene gates. |
| S-5 compat registry present | Local smoke checks eight YAML rows and the index. | Must be transcribed after freshness review. |
| S-6 badge, watchlist, probe, and dashboard present | Local smoke checks staged files and badge states. | Probe cannot run against public repo until repo/hosting gates clear. |
| S-7 changelog and guides present | Local smoke checks six guides and the initial changelog. | Changelog discipline must be enforced by portal CI. |
| S-8 about, open pledge, boundary, and contributing present | Local smoke checks files. | G-OPEN and G-GOVERNANCE still gate launch. |
| S-9A hygiene CI present | Local focused tests pass. | Must run green inside the real portal repo before launch. |
| S-9B transcription helper present | Local focused tests pass. | Helper is optional and remains monorepo-local. |
| S-10 local smoke report green | Local staging inventory smoke passes only. | Not sufficient for public launch by itself. |
| Placeholder scan green on publish branch | Deferred; placeholders remain in local staging by design. | Required before launch. |
| Rendered link check green on publish branch | Deferred; no merged public portal branch exists. | Required before launch. |
| Deterministic render check green on publish branch | S-9A fixture proves the check shape locally; publish-branch run is deferred. | Required before launch. |
| Maintainer sign-off recorded | Not recorded; this file is authored but not signed. | Required before launch. |
| G-LAUNCH authorized | Not authorized by this slice. | Required before announcement. |

## Local Smoke Command

Run from the repo root:

```bash
python3 maintainers/smoketest/portal_smoketest.py
```

The smoke checker verifies the local staged inventory only. It does not fetch
external URLs, create a public repo, run portal-hosted CI, or write files.

## Skeptical Reader Pass

Use `maintainers/skeptical-reader-walkthrough.md`.

For v0, the skeptical reader is maintainer-self. External skeptical review is
deferred until a later release track.

## Sign-Off

Current sign-off: not signed.

The maintainer must not sign this checklist until the public portal branch is
placeholder-free, S-9A hygiene CI is green in that branch, local and rendered
links are green, the operator gates above are cleared, and G-LAUNCH is
explicitly authorized.
