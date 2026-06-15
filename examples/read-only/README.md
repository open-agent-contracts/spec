# Read-Only Example

This example uses the `notes-app` synthetic family to show a richer read-only
contract. It declares several contexts and several actions while keeping every
action side-effect-free.

Schema identifier shown by this page:

`https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json`

The body file is [`contract.yaml`](contract.yaml). It targets
`contract_version: 0.1.0`, uses no public schema-id field, and validates with
zero `errors[]`.

## What It Teaches

- Multiple contexts can describe the surfaces an agent may inspect.
- Multiple `read_only` actions can all use `gate: none`.
- A read-only-only contract does not need a human review channel.
- A read-only-only contract can leave `receipts` empty.

## Placeholders used

- `https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json` - FEATURE-007 plan section 4.1 P-7. The page
  surfaces the future public schema identifier; the YAML body does not.
