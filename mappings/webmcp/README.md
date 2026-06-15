---
standard_version: v0.x
framework: webmcp
framework_version_pinned: cg-draft-2025-08-13+
verified_on: 2026-06-13
next_review_due: 2026-07-13
freshness_status: yellow
---

# WebMCP Mapping

This page describes how an AOC v0.x contract projects into the WebMCP browser
API. It is a starter projection map. WebMCP is a W3C Community Group Draft
report. Breaking changes are expected.

Public schema identifier for this AOC reference: `https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json`.

## Status

- Framework: WebMCP.
- Version pinned: W3C Web Machine Learning Community Group Draft, initial
  publication 2025-08-13; specification has evolved significantly since.
- Authority: W3C Community Group. Pre-standards. Treat as a signal of intent,
  not as a stable contract surface.
- AOC posture: starter projection target for actions only. The freshness
  status flips to yellow within thirty days of the next-review-due date
  because the specification is pre-stable.

## Open Question: Human Confirmation

WebMCP explicitly flags human-confirmation behavior as an Open Question
(issues #165 and #50). The specification acknowledges the gap but does not
yet specify a mechanism. Until the Community Group resolves these issues, an
AOC projection into WebMCP cannot rely on the browser to enforce a gate.

The portal will revise this mapping once the Open Question closes.

## Source Currency

Primary public source cited:

- Specification repository: `https://github.com/webmachinelearning/webmcp`

Re-verification cadence: 1 month. Pre-stable W3C Community Group Draft;
breaking changes are expected. Re-verify monthly until the draft stabilizes.

## What Projects Cleanly

- AOC `actions[]` project into `document.modelContext.registerTool()` calls.
  Each action becomes one registered tool with a name, description, JSON
  Schema input shape, and an `execute` callback. The shape is lossless.
- AOC `effect_class` and `gate` are advisory only. WebMCP has no native gate
  vocabulary. The browser does not enforce them. AOC contracts should not
  assume WebMCP will enforce a gate in the near term.
- AOC `human_ask` is out-of-band on WebMCP. Page authors implement the
  confirmation UI. AOC describes the ask.

## Covered Fields

```yaml
covered_fields:
  - actions
```

## Gaps

```yaml
gaps:
  - field: effect_class
    reason: "No native classification on WebMCP. The browser does not type effects."
  - field: gate
    reason: "Human confirmation is an Open Question in the WebMCP Community Group Draft (issues #165 and #50). Until it closes, the browser cannot enforce a gate."
  - field: human_ask
    reason: "Modelled out-of-band by page authors; WebMCP does not specify the ask shape."
  - field: receipts
    reason: "No receipt surface in the browser API."
  - field: anti_claims
    reason: "Not modelled."
  - field: provenance
    reason: "Not modelled."
  - field: contexts
    reason: "WebMCP exposes a tool-registration surface, not a context surface."
```

## Sharp Edges

```yaml
sharp_edges:
  - "WebMCP is pre-stable. The API surface, the response model, and the human-confirmation behavior are all subject to change before the Community Group draft stabilizes. Adopters should pin a specific commit and re-verify monthly."
  - "Human confirmation is unresolved. An AOC contract that projects a gate into WebMCP today cannot count on the browser to display, confirm, or refuse. The host page or the higher-level runtime is responsible until the Open Question closes."
  - "Browser-side tool registration shifts the trust boundary. A page that registers an irreversible-effect tool puts the burden of confirmation on either the page author or the calling agent. AOC carries the declaration; the page must enforce."
  - "Chrome ships behind a feature flag at the time of source retrieval. Adopters cannot assume general availability."
```

## Why This Projection Is Labelled Starter

WebMCP covers only the `actions[]` field at registration time. Every other
AOC field is either advisory, out-of-band, or absent. The starter label
reflects that scope.

The projection cannot upgrade to a richer label until the Community Group
resolves the human-confirmation Open Question.

## Anti-Claims

- AOC does not replace WebMCP. AOC projects into
  `document.modelContext.registerTool()` where WebMCP is implemented.
  Human-confirmation behavior is an Open Question in WebMCP today; AOC
  declares the gate, the host enforces it.
- AOC does not promise that WebMCP is stable. The pre-stable Community Group
  Draft status is the load-bearing reason this projection is labelled
  starter and re-verified monthly.
- AOC does not claim that the W3C Web Machine Learning Community Group has
  endorsed this projection.
