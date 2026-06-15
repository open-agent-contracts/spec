# Reversible Example

This example uses the `calendar-assistant` synthetic family to show an internal
change that can be reviewed and undone before anything leaves the app.

Schema identifier shown by this page:

`https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json`

The body file is [`contract.yaml`](contract.yaml). It targets
`contract_version: 0.1.0`, uses no public schema-id field, and validates with
zero `errors[]`.

## What It Teaches

- `reversible_internal` actions should use a stricter gate than `none`.
- `review_required` actions require a human-ask channel and approval/refusal
  receipts.
- `executed` is still part of the receipt set when a reviewed action can run.

## Placeholders used

- `https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json` - FEATURE-007 plan section 4.1 P-7. The page
  surfaces the future public schema identifier; the YAML body does not.
