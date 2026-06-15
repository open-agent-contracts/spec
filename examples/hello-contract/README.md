# Hello Contract

This is the smallest hand-authorable AOC v0.1.0 example in the portal set. It
uses the `notes-app` synthetic family and declares one read-only action.

Schema identifier shown by this page:

`https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json`

The body file is [`contract.yaml`](contract.yaml). It targets
`contract_version: 0.1.0`, uses no public schema-id field, and validates with
zero `errors[]`.

## What It Teaches

- A contract can be useful before it describes every app capability.
- A read-only action may use `gate: none`.
- `human_ask: {}` and `receipts: []` are valid when every action is
  `read_only`.
- `anti_claims` may be omitted in raw input because v0 defines a default.

## Placeholders used

- `https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json` - FEATURE-007 plan section 4.1 P-7. The page
  surfaces the future public schema identifier; the YAML body does not.
