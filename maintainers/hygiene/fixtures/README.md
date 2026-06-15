# Hygiene CI Fixtures

These fixture trees deliberately contain the policy literals the
hygiene CI is built to refuse. They live under this directory so
that the production scan can exclude them via the
`maintainers/hygiene/fixtures/` prefix. The negative-fixture test
step invokes the scanner explicitly against each dirty subtree and
asserts non-zero exit.

This README itself uses citation references rather than restating
policy literals; the literal text lives inside the per-fixture
files.

## Inventory

| Fixture | Expectation | Source |
|---|---|---|
| `clean-portal/` | pass | baseline reference |
| `dirty-private-role/` | fail | CONCEPT-002 plan section 7.1 role row |
| `dirty-internal-tooling/` | fail | CONCEPT-002 plan section 7.4 orchestrator row |
| `vendor-allowed-mapping/` | pass | CONCEPT-002 plan section 7.4 path-conditional row (mapping path) |
| `vendor-allowed-compat-yaml/` | pass | CONCEPT-002 plan section 7.4 path-conditional row (compat yaml) |
| `vendor-allowed-compat-index/` | pass | CONCEPT-002 plan section 7.4 path-conditional row (compat index) |
| `vendor-disallowed-other-mapping/` | fail | CONCEPT-002 plan section 7.4 path-conditional row (out-of-allowlist mapping) |
| `vendor-disallowed-other-compat/` | fail | CONCEPT-002 plan section 7.4 path-conditional row (out-of-allowlist compat row) |
| `dirty-internal-substrate/` | fail | CONCEPT-002 plan section 7.4 internal authoring substrate row, demonstrating that an always-block row fires even under an allowed mapping path |
| `placeholder-p1/` | fail | FEATURE-007 plan section 4.1 P-1 |
| `placeholder-p2-link/` | fail | FEATURE-007 plan section 4.1 P-2 inside a markdown link |
| `placeholder-p7-frontmatter/` | fail | FEATURE-007 plan section 4.1 P-7 inside YAML frontmatter |
| `no-placeholders/` | pass | FEATURE-007 plan section 4.1, all eight placeholders absent |
| `render-pair-clean/` | pass | byte-identical `a/` and `b/` rendered output trees |
| `render-pair-divergent/` | fail | divergent `a/` and `b/` rendered output trees |
| `tripwire/` | fail (and isolation tripwire) | bundles every blocked literal; presence near a clean target verifies the scanner is honoring the explicit input |

## Invariant

Adding a fixture that carries a raw policy literal anywhere outside
`maintainers/hygiene/fixtures/` would either fail the production
scan (good) or require weakening the exclusion (bad). Keep new
negative fixtures inside this directory.
