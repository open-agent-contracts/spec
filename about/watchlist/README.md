# Watchlist (`/about/watchlist/`)

This is the staged surface for the public `/about/watchlist/` page on
the `Open Agent Contracts` reference portal. The portal build
wraps this page text around the `watchlist.yaml` data file in this
directory.

## What the watchlist is

The watchlist records every primary source the portal pins for
projections, compat rows, and guidance pages. Each row names the source
surface, its primary URL or URLs, its review cadence in months, the date
it was last verified, and the next-review date. The watchlist is a
maintainer surface: it lives in version control, it is reviewed by the
same PR mechanics as other portal content, and it is the load-bearing
record the source-currency probe (under
`maintainers/source-currency/`) walks on its daily cron run.

## What the watchlist is not

The watchlist is not modified by the source-currency probe in v0. The
probe has issue-surface write semantics only per CONCEPT-002 plan
section 5.2. On a content-hash change the probe opens a portal-repo
issue tagged `source-currency` naming the page that needs review; it
never edits `watchlist.yaml`, never edits page frontmatter, and never
writes to any portal data file. Granting the probe write access to data
files is a deliberate future decision behind G-AUTOPUBLISH (CONCEPT-002
plan section 9.6); not in v0.

## How to update the watchlist

When the probe-emitted issue lands, the maintainer's workflow is:

1. Read the linked source URL.
2. Decide whether the change actually moves the version or projection.
3. Either pull `verified_on:` forward (and reset `next_review_due:` to
   `verified_on + cadence_months`) or pull `next_review_due:` forward
   only (and leave `verified_on:` untouched if the source did not move).
4. Submit the watchlist YAML edit as a portal-repo PR; merge through the
   normal review mechanics.

## Row inventory (v0)

This v0 watchlist carries twelve rows, one per primary source named in
CONCEPT-002 plan section 5.3:

- `mcp-spec-latest`
- `mcp-authorization`
- `mcp-elicitation`
- `openapi-spec`
- `a2a-home`
- `a2a-spec`
- `llms-txt`
- `openai-apps-sdk`
- `webmcp-cg-draft`
- `anthropic-agent-skills`
- `clawmagic-plugin-docs`
- `agents-json-wildcard` (watchlist-only; no v0 `/mappings/*` page per
  FEATURE-007 decision D-19)

The eleven mapping-status rows correspond one-to-one with the eight
`/mappings/*` pages staged in S-4 (the three `mcp-*` rows fan in to the
single `/mappings/mcp/` page; the two `a2a-*` rows fan in to the single
`/mappings/a2a/` page). The `agents-json-wildcard` row is watchlist-only
in v0.

## Gates Still Closed

The probe cannot run end-to-end against the public portal repo until
G-REPO-HOST + G-PROJECT-NAME + G-HOSTING clear and the portal repo
exists. The watchlist data is local-only staging content under
this repository; it is not
transcribed into any public surface in v0.
