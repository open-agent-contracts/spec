# External Example

This example uses the `calendar-assistant` synthetic family to show an action
that changes a connected calendar surface outside the local app state.

Schema identifier shown by this page:

`https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json`

The body file is [`contract.yaml`](contract.yaml). It targets
`contract_version: 0.1.0`, uses no public schema-id field, and validates with
zero `errors[]`.

## What It Teaches

- `external` actions with `authorization_required` require
  `human_ask.channel: out_of_band`.
- The agent must not collect credentials inside the conversational surface.
- External execution needs proposal, approval/refusal, execution, and outcome
  receipt vocabulary.

## Placeholders used

- `https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json` - FEATURE-007 plan section 4.1 P-7. The page
  surfaces the future public schema identifier; the YAML body does not.
