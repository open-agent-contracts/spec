# The Standard

This local staging slice drafts the v0 normative standard pages for
`Open Agent Contracts`.

The pages describe Agent Operating Contract (AOC) v0.1.0 as a legibility
standard: a contract declares what an app exposes to an agent, which actions
exist, what effect class each action has, which human gate applies, how the app
asks a human when blocked, and which receipts the runtime is expected to leave.

This tree is not published and is not transcribed to a public portal repo.

## Sections

- [Concepts](concepts/)
- [Schema](schema/)
- [Vocabulary](vocabulary/)
- [Gates](gates/)
- [Receipts](receipts/)
- [Versioning](versioning/)
- [Conformance](conformance/)

## Public Schema Identifier

The public schema identifier for these pages is:

`https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json`

The private validator may carry an internal dogfood slug while it lives in this
monorepo. That internal value is not the public schema identifier and must not
be published as one.

## Placeholders Used

- `Open Agent Contracts` - FEATURE-007 plan section 4.1 P-1. Staging-only
  public name placeholder.
- `https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json` - FEATURE-007 plan section 4.1 P-7. Staging-only
  public schema identifier placeholder.
