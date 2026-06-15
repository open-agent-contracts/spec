# Conformance

AOC v0.1.0 uses exactly two conformance levels:

- `minimal`
- `complete`

These are documentation and validation levels. They are not certification
claims, readiness scores, badges, or endorsements.

## Minimal

A `minimal` contract:

- targets `contract_version: 0.1.0`;
- parses as YAML or JSON;
- carries the seven raw-required root keys;
- uses valid `effect_class` and `gate` enum values;
- satisfies the validator's error rules with zero `errors[]`.

A `minimal` contract may still emit `findings[]`. Findings identify coverage
gaps or advisory issues, not schema-invalid defects.

## Complete

A `complete` contract is `minimal` and also clears every validator-known
finding for v0.1.0.

That means:

- `contexts` is not empty;
- `actions` is not empty;
- `anti_claims` is not explicitly empty;
- non-`read_only` actions do not use `gate: none`;
- experimental fields are absent or marked non-experimental through the allowed
  stability sidecar so no `F_EXPERIMENTAL_FIELD` remains;
- `provenance.generator` is present;
- source-boundary findings are clear;
- declared export targets are known to the validator.

`complete` does not mean the runtime enforced the contract. It only means the
contract document is structurally valid and locally complete by the v0.1.0
validator's criteria.

## Non-Claims

The conformance levels do not claim:

- certification;
- legal compliance;
- runtime enforcement;
- marketplace approval;
- vendor endorsement;
- production readiness.

They are a way to talk about contract-document coverage without turning AOC
into a score or badge.
