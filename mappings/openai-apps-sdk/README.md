---
standard_version: v0.x
framework: openai-apps-sdk
framework_version_pinned: 2026-06-13-snapshot
verified_on: 2026-06-13
next_review_due: 2026-09-13
freshness_status: green
---

# OpenAI Apps SDK Mapping

This page describes how an AOC v0.x contract projects into the OpenAI Apps
SDK surface. It is an indirect projection: the SDK is built on top of MCP
servers plus a ChatGPT widget runtime, so most AOC fields inherit the MCP
projection.

Public schema identifier for this AOC reference: `https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json`.

## Status

- Framework: OpenAI Apps SDK.
- Version pinned: 2026-06-13 snapshot of the developer page.
- Authority: vendor surface (OpenAI).
- AOC posture: indirect projection via MCP. AOC does not change MCP. AOC
  describes the action and gate vocabulary; the Apps SDK carries it through
  the underlying MCP server and renders the widget UI.

This is a vendor surface. Adoption of the Apps SDK is a publishing decision
for the app developer, not a property of AOC.

## Source Currency

Primary public source cited:

- Developer overview: `https://developers.openai.com/apps-sdk`

Re-verification cadence: 3 months. Vendor surface; self-serve publishing was
listed as coming soon at retrieval time, so the submission flow can change.

## What Projects Cleanly

- The Apps SDK pipeline asks the developer to define an MCP server, supply a
  widget runtime, and publish through OpenAI's submission flow. The MCP
  server is the load-bearing surface for the AOC projection.
- AOC fields inherit the MCP projection (see the MCP mapping page). AOC
  `app.purpose` rides in the MCP server `instructions`. AOC `contexts[]`
  ride in MCP Resources. AOC `actions[]` ride in MCP Tools. AOC `gate`
  rides in MCP elicitation form mode or URL mode depending on sensitivity.
- The widget runtime adds a ChatGPT-side UI layer above MCP. AOC does not
  model widget UI; the widget runtime is responsible for the rendering of
  any preview, review, or authorization step.

## Covered Fields

```yaml
covered_fields:
  - inherits the MCP projection
```

## Gaps

```yaml
gaps:
  - field: receipts
    reason: "The ChatGPT widget runtime does not specify a receipt envelope. Receipts ride alongside the underlying MCP transport rather than inside the SDK."
  - field: anti_claims
    reason: "Not modelled on the Apps SDK developer surface."
  - field: provenance
    reason: "Not modelled on the Apps SDK developer surface."
```

## Sharp Edges

```yaml
sharp_edges:
  - "Self-serve publishing was listed as coming soon at retrieval time. The submission flow can change. AOC contracts should not embed assumptions about a specific submission step."
  - "The widget runtime is OpenAI-side. The same AOC contract that ships into ChatGPT through the Apps SDK does not automatically ship into a different LLM host. Portability flows from the MCP layer, not from the Apps SDK."
  - "The Apps SDK page exposes the widget runtime as a UI surface. AOC does not model widget UI. A maintainer reading this projection must not infer that a widget runtime substitutes for an AOC gate."
```

## Why This Projection Is Labelled Indirect Via MCP

The Apps SDK does not own its own contract grammar. The MCP server is the
contract-bearing surface; the widget runtime is the rendering surface. AOC
projects into the MCP layer, and the Apps SDK consumes whatever MCP
exposes. See the MCP mapping page for the field-by-field projection.

## Anti-Claims

- AOC does not certify a vendor surface. The OpenAI Apps SDK is a projection
  target, not a source of truth.
- AOC does not claim that OpenAI, ChatGPT, or any OpenAI product has
  endorsed this projection.
- AOC does not promise that the Apps SDK self-serve flow is stable. The
  re-verification cadence is the load-bearing mitigation.
