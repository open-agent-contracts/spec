# Concepts

An Agent Operating Contract (AOC) is a portable, machine-readable description
of the boundary between an app and an agent.

It is not a runtime, not a permission system, not a certification, and not a
replacement for the frameworks it can project into. It is a legibility
commitment: a builder states the app purpose, context surfaces, action catalog,
gate requirements, human-ask path, receipt expectations, and provenance in one
inspectable document.

`Open Agent Contracts` uses AOC v0.1.0 as the first public draft target.
The public schema identifier for these pages is
`https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json`.

## Contract Shape

A v0.1.0 contract has eight normalised root keys:

| Key | Category | Meaning |
|---|---|---|
| `contract_version` | deeply required | Semver value for the AOC standard target. v0.1.0 is the first target. |
| `app` | deeply required | App identity and purpose, with `id` and `purpose`. |
| `contexts` | shallow-required | Pages, entities, states, relationships, or provenance exposed to the agent. May be empty with a finding. |
| `actions` | shallow-required | Agent-visible action catalog. May be empty with a finding. |
| `human_ask` | shallow-required, conditional | How the app asks a human when an action needs review or authorization. May be `{}` only for all-read-only action sets. |
| `receipts` | shallow-required, conditional | Receipt event names a compliant runtime is expected to emit. |
| `anti_claims` | optional-with-default | No-overclaim statements. If absent, the validator can inject the canonical default list. |
| `provenance` | deeply required | Authoring source, timestamp, and optional generator label. |

Raw input must carry seven of these keys:

- `contract_version`
- `app`
- `contexts`
- `actions`
- `human_ask`
- `receipts`
- `provenance`

`anti_claims` is optional in raw input and present in the normalised shape.

## Action Shape

Each action carries:

- `id`
- `label`
- `inputs`
- `effect_class`
- `gate`

The required safety vocabulary is the pair `effect_class` plus `gate`. The
effect class describes what kind of consequence an action can have. The gate
describes what the agent or host must do before the action proceeds.

## Forward Tolerance

Readers must accept unknown root keys and unknown per-action keys as no-op
extensions unless the field name is in the closed forbidden-root-key list. This
lets implementations extend locally without making those extensions part of
the v0 standard.

## Non-Goals

AOC v0.1.0 does not:

- enforce runtime safety by itself;
- certify an app as ready;
- replace MCP, OpenAPI, A2A, llms.txt, WebMCP, vendor skill surfaces, or app
  SDKs;
- define OAuth or API transport mechanics;
- publish private doctrine, customer examples, or internal project names.
