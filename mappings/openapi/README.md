---
standard_version: v0.x
framework: openapi
framework_version_pinned: 3.2.0
verified_on: 2026-06-13
next_review_due: 2026-12-13
freshness_status: green
---

# OpenAPI Mapping

This page describes how an AOC v0.x contract projects into an OpenAPI 3.2.0
description. It is a starter projection map, not a complete one. AOC does not
replace OpenAPI; the two sit together.

Public schema identifier for this AOC reference: `https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json`.

## Status

- Framework: OpenAPI Specification.
- Version pinned: 3.2.0 (released 2025-09-19).
- Authority: OpenAPI Initiative (Linux Foundation project).
- AOC posture: starter projection target. OpenAPI owns the HTTP API surface.
  AOC owns effect and gate classification of actions. The two are
  complementary, not competing.

## Source Currency

Primary public source cited:

- Specification: `https://spec.openapis.org/oas/latest.html`

Re-verification cadence: 6 months. OpenAPI is a mature specification with a
slow release cadence (3.2.0 shipped 2025-09).

## What Projects Cleanly

- An AOC `app` field projects into the OpenAPI `info` object. `info.title`
  and `info.description` carry the public-facing identity.
- AOC `actions[]` project into `paths.*.operation` entries. Each action maps
  to one `operationId`. The shape is lossless.
- AOC `effect_class` projects into the vendor extension
  `x-aoc-effect-class` on the operation. OpenAPI 3.2 supports specification
  extensions, so the projection is lossless on shape.
- AOC `gate` projects into the vendor extension `x-aoc-gate` on the
  operation. When a gate is `authorization_required` the projection should
  also carry an OpenAPI Security Requirement Object (for example an OAuth2
  scheme) so that the OpenAPI consumer sees the required scope alongside the
  declarative gate.
- AOC `human_ask` projects into the vendor extension `x-aoc-human-ask` on
  the operation. There is no native OpenAPI equivalent.
- AOC `receipts[]` project into the OpenAPI `webhooks` field. Each receipt
  becomes a webhook payload shape. This is the cleanest native representation
  of receipts in OpenAPI 3.1+.
- AOC `contexts[]` project either as OpenAPI `tags` or as the vendor
  extension `x-aoc-context`. OpenAPI has no first-class context concept, so
  the projection is lossy.

## Covered Fields

```yaml
covered_fields:
  - app
  - actions
  - effect_class
  - gate
  - human_ask
  - receipts
```

## Gaps

```yaml
gaps:
  - field: contexts
    reason: "OpenAPI has no first-class concept of an agent-visible context surface. The projection uses tags or the x-aoc-context extension and accepts the loss."
  - field: anti_claims
    reason: "OpenAPI does not model anti-claim text. AOC carries the field."
  - field: provenance
    reason: "OpenAPI does not model contract provenance. AOC carries the field."
```

## Sharp Edges

```yaml
sharp_edges:
  - "OpenAPI is a description of a callable surface. It does not classify endpoints by effect or reversibility. AOC's effect_class is the load-bearing addition; without it, an OpenAPI document does not tell an agent which endpoints are safe to call without confirmation."
  - "Webhook payloads in OAS 3.2 require careful alignment of the parent operation's authorization scheme with the webhook's security expectations. A receipt webhook should not be reachable by a less-authenticated caller than the operation it acknowledges."
  - "Security Requirement Objects allow alternative schemes to satisfy a requirement. An AOC gate that maps to authorization_required must not be interpreted as a single OAuth flow if the OpenAPI document offers multiple satisfying schemes; the gate names the requirement, not the mechanism."
  - "A vendor extension is non-normative to OpenAPI tooling. Consumers that ignore x-aoc-* extensions will not see the gate or effect class. AOC contracts that ship through OpenAPI must keep the source AOC document as the source of truth, with the OpenAPI projection as a derived artifact."
```

## Why This Projection Is Labelled Starter

OpenAPI loses two AOC fields without vendor extensions (`anti_claims` and
`provenance`) and one field with a lossy mapping (`contexts`). The remaining
fields project cleanly. The `starter` label reflects the gap, not the value
of the projection.

A future revision may upgrade this label once a portable extension set is
broadly adopted.

## Anti-Claims

- AOC does not replace OpenAPI. AOC describes which actions exist and which
  gates they require. OpenAPI describes the HTTP API surface. The two sit
  together.
- AOC does not claim that the OpenAPI Initiative or the Linux Foundation has
  reviewed or approved this projection.
- AOC does not require that a service expose its description as OpenAPI. The
  OpenAPI projection is one of several possible targets.
