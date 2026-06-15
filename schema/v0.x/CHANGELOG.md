# AOC Schema Changelog (v0.x)

This file tracks per-version changes to the Agent Operating Contract
schema under `schema/v0.x/`.

The `aoc/v0.x` namespace is **internal / dogfood only** while the
schema lives inside the monorepo. The published public `$id` value is
operator-gated by `G-NAME-BRAND` + artifact-name + API-name resolution
(CONCEPT-004 plan §§5.1 and 6.1). The eventual rename from the internal
slug to a public URL is **orthogonal to `contract_version`** and does
not itself bump the version.

Per CONCEPT-001 plan §3.1, `v0.x` is explicitly pre-stable; breaking
changes are permitted within v0. Within v0 the migrator (not direct
cross-minor read) is the load-bearing compatibility mechanism.

---

## 0.1.0 — 2026-06-13

Initial schema.

### Added

- Seven raw-required root keys: `contract_version`, `app`, `contexts`,
  `actions`, `human_ask`, `receipts`, `provenance`
  (FEATURE-002 plan §2.1, CONCEPT-001 plan §2.1).
- `anti_claims` as the optional-with-default eighth root key. Default
  value carries the canonical A0..A14 anti-claim list per CONCEPT-001
  plan §8.1. Absent raw input → normalized output carries the default
  list. Explicit `[]` → coverage finding `F_EMPTY_ANTI_CLAIMS` (the
  finding is the validator's job; the schema accepts the empty array).
- Closed `effect_class` enum (`read_only`, `reversible_internal`,
  `external`, `irreversible`) per CONCEPT-001 plan §2.2 and
  CONCEPT-004 plan §4.1.3.
- Closed `gate` enum (`none`, `preview`, `review_required`,
  `authorization_required`, `forbidden`) per CONCEPT-001 plan §2.2.
- `human_ask.channel` v0 enum (`in_app`, `email_link`, `push`, `cli`,
  `out_of_band`) per CONCEPT-001 plan §5.4.
- Optional v0 fields with declared field-stability per CONCEPT-001
  plan §2.3 and §3.2: per-action `inputs`, `cooldown`, `two_key`,
  `binding_status`, `rollback`, root-level `user_values`,
  `hard_boundaries`, `export_targets`, and the `stability` sidecar
  map.
- Closed deferred-root-key denylist per FEATURE-002 plan §2.3 (the
  14 named readiness / cryptographic-attestation / public-name-spec
  keys). Encoded as a `not`/`anyOf` block on the schema. Every other
  unknown root key is accepted silently per CONCEPT-001 plan §2.8
  forward tolerance.
- Identifier policy per CONCEPT-001 plan §2.7: opaque, builder-chosen
  non-empty strings; no central registry; no collision check.
- Canonical serialization: YAML is canonical, JSON is the lossless
  mirror (CONCEPT-001 plan §2.6). A single schema validates both
  forms via the parser's normalized object tree; the
  `examples/_canonical.yaml` ↔ `examples/_canonical.json` pair is
  the lossless-interchange evidence shipped alongside the schema.

### Notes for cold-readers

- `$id: "aoc/v0.1.0"` is the **internal / dogfood** value only. The
  `$comment` on `$id` is the durable cold-read warning so a future
  reader does not assume this URI is the public namespace.
- The schema deliberately does NOT enforce: the `human_ask`
  conditional shallow-required rule, the receipt-coverage rules
  R-1..R-4, the `out_of_band` requirement, `provenance.generator`
  absence, or the advisory grep-token scan. Those are the semantic
  rule engine's job; the FEATURE-002 validator CLI ships in a later
  build slice (Slice F002-C).
- `anti_claims` is **not** placed in the schema's top-level
  `required` array. This is the raw-input-optional rule
  (FEATURE-002 plan §2.1 — rev-2 absorbed blocker B-1). The
  normalized output still carries the A0..A14 default value via the
  JSON Schema `default` keyword.

### Out of scope for this changelog entry

- `aoc validate` CLI (deferred to FEATURE-002 build Slice F002-C).
- Semantic rule engine (deferred to FEATURE-002 build Slice F002-C).
- `actionspec.json` / `llms.txt` projection generators (deferred to
  FEATURE-002 build Slice F002-D).
- Runtime-obligation documentation alongside the validator
  (deferred to Slice F002-C).
- Public schema `$id` URL value, public CLI binary name, license text
  (operator-gated per CONCEPT-004 plan §§5–6; not in v0).
