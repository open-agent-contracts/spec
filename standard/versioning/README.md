# Versioning

AOC v0.1.0 is the first draft target.

Public schema identifier for the v0 pages:

`https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json`

## Contract Version

Every contract document carries `contract_version`.

For the first v0 validator target, the value is:

`0.1.0`

The public schema identifier is separate from `contract_version`. Replacing
`https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json` with a durable public identifier later does not by
itself bump `contract_version`.

## v0 Stability

v0 is explicitly pre-stable:

- breaking changes are allowed within v0;
- each breaking change must ship a changelog note;
- each breaking change must ship a migration path;
- later v0 readers are not required to directly read earlier v0 contracts
  without a migration step.

The direct backward-compatible minor-version promise starts at v1.0, not v0.

## Version Mismatch

The validator targets one contract version at a time. If a contract's
`contract_version` does not match the validator target, the validator emits
`E_VERSION_MISMATCH`.

The mismatch entry must point the implementer toward the migration path rather
than silently best-effort-reading a different v0 contract shape.

## Archives

Published documentation for a deprecated version is not deleted. Deprecated
fields should move to a future `/standard/deprecated/` page when such fields
exist. v0.1.0 has no deprecated fields.
