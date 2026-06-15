---
standard_version: v0.x
framework: clawmagic
framework_version_pinned: 2026-06-13-snapshot
verified_on: 2026-06-13
next_review_due: 2026-09-13
freshness_status: green
---

# ClawMagic Plugin Mapping

This page describes how an AOC v0.x contract projects into the ClawMagic
plugin surface. It is a projection map for a vendor surface. ClawMagic
carries the closest existing per-action gate vocabulary on any vendor
surface, but the public manifest is not a portable open contract.

Public schema identifier for this AOC reference: `https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json`.

## Status

- Framework: ClawMagic plugin metadata.
- Version pinned: 2026-06-13 snapshot of the vendor plugin documentation.
- Authority: vendor surface (ClawMagic).
- AOC posture: projection target. ClawMagic carries per-action risk and
  confirmation fields, which are the closest existing native analog to AOC's
  `effect_class` plus `gate`. AOC remains the portable declaration; the
  ClawMagic plugin surface carries a vendor-specific rendering.

This is a vendor surface. AOC contracts do not depend on it.

## Source Currency

Primary public sources cited:

- Plugin development: `https://clawmagic.ai/docs/plugin-development`
- Plugin packaging: `https://clawmagic.ai/docs/plugin-packaging`

Re-verification cadence: 3 months. Vendor surface; source currency depends
on the vendor's own documentation cycle.

## What Projects Cleanly

- An AOC `app` field projects into the ClawMagic plugin manifest listing
  metadata: the manifest carries description, listing identity, and the
  overall plugin posture.
- AOC `contexts[]` project into the routing and lookbook structures the
  plugin uses to scope its work. The projection is advisory because
  ClawMagic does not declare a context catalog as a typed field.
- AOC `actions[]` project into the public action definitions inside
  `actionspec.json`. Each AOC action maps to one action entry with a key, a
  description, and an input schema.
- AOC `effect_class` projects into the ClawMagic per-action `risk_level`
  field. The projection is advisory; `risk_level` conflates effect with the
  needed confirmation, so the round-trip is not always clean.
- AOC `gate` projects into the ClawMagic per-action confirmation requirement.
  This is the closest existing native gate vocabulary on any surveyed
  vendor surface.
- AOC `human_ask` rides in the free-text fields the actionspec exposes
  alongside each action.

## Covered Fields

```yaml
covered_fields:
  - app
  - contexts (via routing and lookbook structures)
  - actions (via actionspec.json)
  - effect_class (implicit in per-action risk classification)
  - gate (per-action confirmation requirement)
  - human_ask
```

## Gaps

```yaml
gaps:
  - field: receipts
    reason: "Not modelled by the public manifest. Receipts ride alongside the plugin runtime rather than inside the manifest."
  - field: anti_claims
    reason: "Not modelled on the public manifest."
  - field: provenance
    reason: "Not modelled on the public manifest."
```

## Sharp Edges

```yaml
sharp_edges:
  - "The plugin surface is vendor-specific. Cross-vendor portability is not implied by ClawMagic's manifest fields, even where the manifest carries a per-action confirmation requirement."
  - "The plugin type enumeration is vendor-private. AOC does not export it, and the portal does not name the enum members on this page. A plugin author who needs the enum should read the vendor documentation directly."
  - "The per-action risk_level conflates effect with confirmation needs. AOC keeps effect_class and gate as separate fields so that a maintainer can reason about each axis independently."
  - "Source currency for the plugin documentation depends on the vendor's own cycle. Re-verification at three months is the load-bearing mitigation."
```

## Why This Projection Is Labelled Complete For The Manifest

The ClawMagic public manifest carries every AOC field except `receipts`,
`anti_claims`, and `provenance`. Among surveyed vendor surfaces this is the
deepest coverage of AOC's per-action gate concept. The label reflects the
fit between AOC actions and the actionspec; it does not endorse the vendor
surface or claim portability beyond ClawMagic.

## Anti-Claims

- AOC does not certify a vendor surface. ClawMagic is a projection target,
  not a source of truth. The portal reports gaps and sharp edges; it does
  not endorse the vendor surface.
- AOC does not claim that ClawMagic has reviewed or approved this
  projection.
- AOC does not adopt the ClawMagic plugin type enumeration into its own
  vocabulary. The enum stays vendor-private.
- AOC does not promise that a ClawMagic plugin will enforce a declared
  AOC gate. The plugin runtime is responsible for enforcement; AOC
  describes the boundary.
