# Irreversible Example

This example uses the `checkout-helper` synthetic family to show an action
where the consequence cannot be undone by a simple local rollback.

Schema identifier shown by this page:

`https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json`

The body file is [`contract.yaml`](contract.yaml). It targets
`contract_version: 0.1.0`, uses no public schema-id field, and validates with
zero `errors[]`.

## What It Teaches

- `irreversible` actions require a strong gate.
- `authorization_required` plus `irreversible` requires an out-of-band
  human-ask channel.
- The receipt set should show proposal, approval/refusal, execution, and final
  outcome.

## Placeholders used

- `https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json` - FEATURE-007 plan section 4.1 P-7. The page
  surfaces the future public schema identifier; the YAML body does not.
