# Examples

These examples show six ways to read and write AOC v0.1.0 contracts. They are
synthetic and derive only from the locked v0 app families:

- `notes-app`
- `calendar-assistant`
- `checkout-helper`

Each entry has a short narrative page and a YAML contract body. YAML is used
because it is the canonical v0 authoring form; JSON remains a lossless mirror
form for tooling that prefers JSON.

Public schema identifier for these pages:

`https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json`

The schema identifier is shown only in the page text. The example contract
bodies do not carry `$id`, `schema_id`, `public_schema_id`, or `published_id`
fields.

## Entry Set

| Entry | App family | Focus |
|---|---|---|
| [`hello-contract/`](hello-contract/) | `notes-app` | Smallest hand-authorable contract. |
| [`read-only/`](read-only/) | `notes-app` | Read-only contexts and actions. |
| [`reversible/`](reversible/) | `calendar-assistant` | Reversible internal action with human review. |
| [`external/`](external/) | `calendar-assistant` | External action with out-of-band authorization. |
| [`irreversible/`](irreversible/) | `checkout-helper` | Irreversible action with authorization and receipt coverage. |
| [`anti-patterns/`](anti-patterns/) | `checkout-helper` | Valid `forbidden` action plus wrong-shape snippets. |

## Validation

All six YAML bodies target `contract_version: 0.1.0` and validate with zero
`errors[]` and zero `findings[]` against the local v0.1.0 validator.

## Boundary Rules

The examples are not copied from a real product, customer record, private
workspace, support mailbox, hosted runtime, or agent transcript. They do not
claim production readiness, certification, marketplace approval, vendor
endorsement, support availability, public launch, or runtime enforcement.

## Placeholders used

- `https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json` - FEATURE-007 plan section 4.1 P-7. The wrapping
  page surfaces the future public schema identifier. The contract bodies use
  only `contract_version: 0.1.0`.
