# Validating Your Contract

This guide describes how to validate an Agent Operating Contract
document against the v0 schema. Validation is optional. The
hand-authoring guide showed that a contract is a plain document
you can write without any tool; this guide adds a second pair of
eyes that catches missing fields, wrong types, forbidden root
keys, and other shape problems before you ship the contract.

## What Validation Is And Is Not

Validation answers two questions:

1. Does the document match the v0 schema (is the shape right)?
2. Do the contract's semantic rules hold (do the enums line up,
   are the required fields present, are sensitive asks routed
   out-of-band, do the receipt events match the action set)?

Validation does not execute the contract. It does not call any
external service, register the contract anywhere, or generate
side effects. It is a read-only check that runs against the
single file you point it at.

## Choosing A Validator

The reference validator is a small command-line tool that ships
with this project. Any other tool that loads the v0 schema and
the contract document, applies the published semantic rules, and
returns errors and findings is also a valid validator. The
contract format is open; the validator is not a gatekeeper.

For the rest of this guide the command surface is written as
`agent-contract-kit`, which is the public package
identifier slot. The actual public package and binary name are
not yet resolved on the public portal, and the placeholder will
be replaced once the project's naming decision lands. Do not
rely on any specific public binary name until the placeholder is
resolved on the published portal.

## Common Validation Surfaces

The patterns below describe how a validator is typically
invoked. Substitute `agent-contract-kit` with the name of
the validator you are using.

### Validate One File

```text
agent-contract-kit validate path/to/aoc.yaml
```

The validator reads the file, loads the v0 schema, and prints
errors and findings. A clean run prints no errors and exits with
code zero.

### Validate A Directory

```text
agent-contract-kit validate path/to/contracts/
```

Validators that accept a directory walk every YAML and JSON file
in the tree and report per-file results. Use this pattern when
several contracts live next to each other.

### Target A Specific Version

```text
agent-contract-kit validate --target-version 0.1.0 path/to/aoc.yaml
```

The `--target-version` flag pins the validator to the requested
contract version. If the document's `contract_version` does not
match, the validator short-circuits with a clear version-mismatch
error rather than reporting a long list of incidental shape
problems.

## What The Validator Checks

A v0 validator covers the following classes of problem:

- **Structural**: required root keys present, types correct,
  forbidden root keys absent, enum values within the closed
  v0 sets.
- **Semantic**: `effect_class` and `gate` consistent with each
  other (for example, `irreversible` actions should not carry
  `gate: none`); sensitive asks routed through
  `human_ask.channel: "out_of_band"`; receipts referenced by
  actions exist in the contract's receipt list.
- **Coverage**: every action declares an `effect_class`, every
  external or irreversible action declares a non-trivial gate,
  the receipt list covers proposal and execution events.

Errors mean the contract violates the schema and should be
fixed before use. Findings are advisory: they flag patterns the
contract could improve, like a `read_only` action that still
carries a `review_required` gate.

## Reading The Output

A clean validator run looks roughly like this:

```text
path/to/aoc.yaml
  errors:   0
  findings: 0
  exit:     0
```

A failing run looks roughly like this:

```text
path/to/aoc.yaml
  errors:   2
  findings: 1
  details:
    - missing required key: app.purpose
    - forbidden root key: secrets
    - finding: action "create-note" has effect_class
      reversible_internal but gate authorization_required
  exit:     1
```

The exact rendering varies between validators; the important
parts are the error count, the finding count, and an exit code
that signals success or failure to scripts.

## A Suggested Authoring Loop

The simplest authoring loop is:

1. Edit the contract.
2. Run `agent-contract-kit validate path/to/aoc.yaml`.
3. Fix any errors first; then look at findings.
4. Repeat until errors and findings are both at zero, or until
   every remaining finding is one you have an explicit reason
   to keep.

This loop is editor-agnostic; nothing depends on a specific
runtime or a portal account.

## Naming Placeholder Note

The validator command surface in this guide uses
`agent-contract-kit` because the public package
identifier slot is still unresolved on the public portal. The
portal will replace the placeholder with the resolved value
once the project's naming decision lands. If you see a fixed
binary name on a third-party page, treat it as that party's
working slug, not as a public promise.

## Public Sources Cited

This guide describes the v0 validator surface and the schema
shape it checks. The schema itself is published on
`/standard/schema/`; no external standards are cited in this
guide.
