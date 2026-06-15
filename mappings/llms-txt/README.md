---
standard_version: v0.x
framework: llms-txt
framework_version_pinned: 2024-09-03-proposal
verified_on: 2026-06-13
next_review_due: 2026-09-13
freshness_status: green
---

# llms.txt Mapping

This page describes how an AOC v0.x contract projects into an llms.txt file.
It is a starter projection map. llms.txt is a community proposal, not an
adopted standard.

Public schema identifier for this AOC reference: `https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json`.

## Status

- Framework: llms.txt.
- Version pinned: 2024-09-03 proposal authored by Jeremy Howard.
- Authority: personal and community proposal. Not a standards body output.
  Status remains open for community input.
- AOC posture: starter projection target. llms.txt owns content discovery
  for LLM context windows. AOC owns the action and gate vocabulary that
  llms.txt deliberately does not address.

llms.txt is a community proposal. Treating it as an adopted standard would
misrepresent the source.

## Source Currency

Primary public source cited:

- Proposal home: `https://llmstxt.org/`

Re-verification cadence: 3 months. Status change matters more than content
change; the proposal could move toward adoption or be superseded.

## What Projects Cleanly

- An AOC `app.purpose` projects into the H1 project name and the blockquote
  summary at the top of the llms.txt file. The projection is lossless because
  llms.txt only requires the H1 plus a short summary.
- AOC `contexts[]` project into an H2 file list of markdown hyperlinks, with
  each context linking out to a deeper file. The projection is lossy because
  llms.txt stores only the link text and the URL.
- AOC `actions[]` project into an H2 file list of markdown hyperlinks, with
  each action linking out to a per-action page. The projection is lossy for
  the same reason.
- The AOC document itself can be linked from the llms.txt file as a
  canonical-contract entry.

## Covered Fields

```yaml
covered_fields:
  - app.purpose
  - contexts (as links)
  - actions (as links)
```

## Gaps

```yaml
gaps:
  - field: effect_class
    reason: "Out of scope for llms.txt. The proposal is a read-only content discovery surface."
  - field: gate
    reason: "Out of scope for llms.txt. There is no native gate vocabulary."
  - field: human_ask
    reason: "Out of scope for llms.txt."
  - field: receipts
    reason: "Out of scope for llms.txt."
  - field: anti_claims
    reason: "Out of scope for llms.txt."
  - field: provenance
    reason: "Out of scope for llms.txt."
```

## Sharp Edges

```yaml
sharp_edges:
  - "llms.txt is a community proposal. The portal must mark this status accurately and must not call llms.txt the standard for content discovery."
  - "llms.txt is read-only by design. An AOC contract that links from llms.txt is a pointer, not a callable surface. Any action that requires a gate must be resolved out of llms.txt before it is exercised."
  - "The proposal has only one required section (the H1 project name). Maintainers should not assume any other field carries semantic weight across implementers."
  - "The proposal has been stable for more than eighteen months at re-verification time. Stability is not the same as adoption. The re-verification cadence stays at three months so the portal catches a status change."
```

## Why This Projection Is Labelled Starter

llms.txt is intentionally narrow. Only `app.purpose` and link lists for
contexts and actions project cleanly. The starter label reflects the
content-discovery scope, not the quality of the projection.

## Anti-Claims

- AOC does not replace llms.txt. AOC may be linked from an llms.txt file as
  a canonical-contract entry. AOC does not replace the llms.txt
  content-discovery purpose.
- AOC does not adopt llms.txt as a standards-body-grade specification.
  llms.txt is a community proposal authored in 2024 and remains open for
  community input. The portal cites its status accurately.
- AOC does not claim that the llms.txt author or any community body has
  endorsed this projection.
