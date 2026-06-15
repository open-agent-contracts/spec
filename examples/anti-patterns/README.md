# Anti-Patterns

This entry uses the `checkout-helper` synthetic family to show a valid
`forbidden` action and four wrong-shape snippets. The shipped contract body is
valid; the snippets below are teaching material, not validator input files.

Schema identifier shown by this page:

`https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json`

The body file is [`contract.yaml`](contract.yaml). It targets
`contract_version: 0.1.0`, uses no public schema-id field, and validates with
zero `errors[]`.

## Valid Forbidden Action

The contract body includes an action that asks to collect a payment credential
inside the chat surface. That action is present so the boundary is visible, but
it is marked `gate: forbidden`.

## Wrong-Shape Snippets

These snippets are intentionally not stored as `.yaml` files in this staging
tree, because S-3's six example bodies must validate. They are annotations for
readers.

### Missing `contract_version`

```yaml
app:
  id: example.checkout-helper
```

Why wrong: `contract_version` is one of the seven raw-required root keys.

### Public schema id inside a contract body

```yaml
contract_version: 0.1.0
schema_id: https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json
```

Why wrong: contract bodies must not carry `$id`, `schema_id`,
`public_schema_id`, or `published_id`. The wrapping portal page can surface the
public schema placeholder; the body cannot.

### Non-read-only action with `gate: none`

```yaml
actions:
  - id: action.update-cart
    label: Update cart
    effect_class: reversible_internal
    gate: none
```

Why this is below the default posture: non-`read_only` actions should declare a
stricter gate. The validator treats this as a finding, not an error.

### External authorization without out-of-band human ask

```yaml
human_ask:
  channel: in_app
actions:
  - id: action.submit-order
    label: Submit order
    effect_class: external
    gate: authorization_required
```

Why wrong: `authorization_required` plus `external` requires
`human_ask.channel: out_of_band`.

## Placeholders used

- `https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json` - FEATURE-007 plan section 4.1 P-7. The page
  surfaces the future public schema identifier; the YAML body does not.
