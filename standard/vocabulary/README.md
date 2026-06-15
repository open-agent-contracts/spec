# Vocabulary

This page lists the v0.1.0 vocabulary used by the schema, validator, and portal
examples.

Public schema identifier for this vocabulary:

`https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json`

## Root Keys

| Key | Status | Notes |
|---|---|---|
| `contract_version` | stable | Semver target for the contract grammar. |
| `app` | stable | App identifier and plain-prose purpose. |
| `contexts` | stable | Agent-visible context catalog. |
| `actions` | stable | Agent-visible action catalog. |
| `human_ask` | stable | Human review or authorization channel. |
| `receipts` | stable | Declared runtime receipt event names. |
| `anti_claims` | stable | No-overclaim statements; optional-with-default in raw input. |
| `provenance` | stable | Authoring source and timestamp. |
| `user_values` | experimental | Builder-stated preferences or norms. |
| `hard_boundaries` | experimental | Explicit advisory boundary statements. |
| `export_targets` | experimental | Builder intent for future projection targets. |
| `stability` | experimental | Optional sidecar for field stability overrides. |

## Human Ask Channels

`human_ask.channel` may be:

- `in_app`
- `email_link`
- `push`
- `cli`
- `out_of_band`

`out_of_band` is required when a contract declares
`gate: authorization_required` for an `external` or `irreversible` action.

## Validator Result Shape

The local validator reports two channels:

- `errors[]` for invalid or unsafe-to-accept contract defects;
- `findings[]` for coverage gaps and advisory issues.

Each entry carries:

- `path`
- `code`
- `message`
- `severity`
- `doc`

## Stable Error Codes

- `E_SCHEMA_INVALID`
- `E_MISSING_REQUIRED_KEY`
- `E_MISSING_REQUIRED_SUBFIELD`
- `E_RESERVED_KEY_COLLISION`
- `E_HUMAN_ASK_REQUIRED`
- `E_RECEIPTS_R1`
- `E_RECEIPTS_R2`
- `E_RECEIPTS_R3`
- `E_OUT_OF_BAND_REQUIRED`
- `E_FORBIDDEN_FIELD`
- `E_VERSION_MISMATCH`

## Stable Finding Codes

- `F_EMPTY_CONTEXTS`
- `F_EMPTY_ACTIONS`
- `F_EMPTY_ANTI_CLAIMS`
- `F_NON_READONLY_GATE_NONE`
- `F_EXPERIMENTAL_FIELD`
- `F_GENERATOR_MISSING`
- `F_BOUNDARY_GREP_HIT`
- `F_UNUSED_EXPORT_TARGET`

Findings are not certification failures. They are coverage signals for
maintainers and implementers.
