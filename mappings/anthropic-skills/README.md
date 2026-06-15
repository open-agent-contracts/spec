---
standard_version: v0.x
framework: anthropic-skills
framework_version_pinned: 2026-06-13-snapshot
verified_on: 2026-06-13
next_review_due: 2026-09-13
freshness_status: green
---

# Anthropic Agent Skills Mapping

This page describes how an AOC v0.x contract projects into the Anthropic
Agent Skills surface. It is a starter projection map for a vendor surface.
SKILL.md fields are well-defined, but they are not a portable contract.

Public schema identifier for this AOC reference: `https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json`.

## Status

- Framework: Anthropic Agent Skills.
- Version pinned: 2026-06-13 snapshot of the vendor overview page.
- Authority: vendor surface (Anthropic). Loaded across the Claude API,
  claude.ai, Claude Code, the AWS Claude Platform, and Microsoft Foundry.
- AOC posture: starter projection target. AOC describes the action and gate
  vocabulary. SKILL.md captures a progressive-disclosure capability bundle
  for Claude. The two carry different information.

This is a vendor surface. AOC contracts do not depend on it.

## Source Currency

Primary public source cited:

- Overview: `https://platform.claude.com/docs/en/docs/agents-and-tools/agent-skills/overview`

Re-verification cadence: 3 months. Vendor surface; the overview can change
without a version bump.

## What Projects Cleanly

- AOC `app.purpose` projects into the SKILL.md frontmatter `description`
  field. The vendor surface caps the description at 1024 characters, so a
  long AOC purpose is truncated at projection time.
- AOC `contexts[]` project into bundled markdown files that the SKILL.md
  references. The projection is advisory because Skills load files
  progressively rather than declaring a typed context catalog.
- AOC `actions[]` project into bundled scripts and instructions that the
  SKILL.md body describes. The projection is advisory because Skills do not
  declare an action catalog as a separate field.
- AOC `effect_class` and `gate` live in SKILL.md body prose. There is no
  native enum.

## Covered Fields

```yaml
covered_fields:
  - app.purpose (as description, length-capped at 1024 chars)
  - contexts (as bundled markdown files)
  - actions (as scripts and instructions)
```

## Gaps

```yaml
gaps:
  - field: effect_class
    reason: "No native enum on SKILL.md. The classification lives in body prose only."
  - field: gate
    reason: "No native enum on SKILL.md. The vendor surface uses a trust-and-audit posture rather than a declarative gate."
  - field: human_ask
    reason: "Not modelled on SKILL.md."
  - field: receipts
    reason: "Not modelled on SKILL.md."
  - field: anti_claims
    reason: "Not modelled."
  - field: provenance
    reason: "Not modelled. The vendor page recommends auditing untrusted Skills like installing software, but the SKILL.md frontmatter does not carry a provenance field."
```

## Sharp Edges

```yaml
sharp_edges:
  - "SKILL.md frontmatter caps the description at 1024 characters and the name at 64 characters with a lowercase-hyphen pattern. AOC app.purpose strings that exceed these limits are truncated or rejected at projection time."
  - "Skills can invoke tools in ways that do not match their stated purpose. AOC actions[] should be treated as the canonical declaration. A SKILL.md must not be trusted to enforce an AOC gate."
  - "Anthropic's own guidance is to only use Skills from trusted sources and to audit them like installing software. AOC provenance is the audit anchor; the SKILL.md frontmatter does not carry it natively."
  - "Skills do not sync across Claude surfaces. A Skill loaded into the Claude API is not automatically available in Claude Code, claude.ai, the AWS Claude Platform, or Microsoft Foundry. Portability claims must not be inferred."
```

## Why This Projection Is Labelled Starter

The Anthropic Skills surface covers only three AOC fields and does so
indirectly. Every gate-shaped field lives in body prose. The starter label
reflects that gap.

This is a vendor surface. Portability across Claude products is not
guaranteed.

## Anti-Claims

- AOC does not certify a vendor surface. Anthropic Skills is a projection
  target, not a source of truth. The portal reports gaps; it does not
  endorse the vendor surface.
- AOC does not claim that Anthropic, Claude, or any Anthropic product has
  endorsed this projection.
- AOC does not promise that a Skill enforces a declared gate. The vendor
  guidance is to audit untrusted Skills like installing software. A valid AOC
  contract describes the boundary; a runtime is responsible for the
  enforcement.
