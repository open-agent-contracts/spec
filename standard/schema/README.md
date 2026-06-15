# Schema

The v0.1.0 schema documents the AOC grammar for both canonical YAML and lossless
JSON mirrors.

Public schema identifier:

`https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json`

The implementation currently uses a private internal dogfood slug while the
schema file lives in the monorepo. That internal value is not a public schema
identifier, is not a durable public URL, and does not replace the placeholder
above.

## Root Requirements

Raw input requires exactly seven root keys:

- `contract_version`
- `app`
- `contexts`
- `actions`
- `human_ask`
- `receipts`
- `provenance`

The normalised shape has eight root keys because `anti_claims` is
optional-with-default.

## Required Subfields

Deeply required roots:

- `contract_version`: non-empty semver string.
- `app`: object with non-empty `id` and `purpose`.
- `provenance`: object with non-empty `author` and `generated_at`.

Action objects require:

- `id`
- `label`
- `effect_class`
- `gate`

The v0 schema accepts `inputs` as a free-form object. A stricter input schema
is a future-version concern, not a v0.1.0 requirement.

## Closed Enums

`effect_class` must be one of:

- `read_only`
- `reversible_internal`
- `external`
- `irreversible`

`gate` must be one of:

- `none`
- `preview`
- `review_required`
- `authorization_required`
- `forbidden`

Unknown enum values are schema errors.

## Optional And Experimental Fields

Stable in v0:

- the root vocabulary listed above;
- `actions[].id`;
- `actions[].label`;
- `actions[].effect_class`;
- `actions[].gate`;
- `human_ask`;
- `receipts`;
- `anti_claims`;
- `provenance`.

Experimental in v0:

- `actions[].inputs` shape;
- `actions[].cooldown`;
- `actions[].two_key`;
- `actions[].binding_status`;
- `user_values`;
- `hard_boundaries`;
- `export_targets`.

Deprecated in v0:

- none.

## Forbidden Root Keys

The v0 validator rejects a closed list of root keys so that deferred concepts
do not quietly become part of the standard.

Readiness-score keys:

- `readiness_score`
- `agent_ready`
- `agent_readiness`
- `readiness_grade`

Cryptographic-attestation keys:

- `signature`
- `signatures`
- `attestation`
- `attestations`
- `signed_by`
- `signing_key`

Public-schema-id keys inside a contract document:

- `$id`
- `schema_id`
- `public_schema_id`
- `published_id`

The schema file may have schema metadata. A contract document must not use
these fields to claim a public schema identifier.
