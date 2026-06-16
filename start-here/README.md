# Start here

> **v0 draft - quiet public setup**
> This is an early draft of an open standard. It is not a public release. It
> is not certified by any standards body. No paid support is available. Content
> may change before v1.

## What is an Agent Operating Contract?

An Agent Operating Contract (AOC) is a YAML file that an application publishes to describe itself to an AI agent. It lists the application's data (contexts), actions, gates (where human authorization is required), and receipts (what is recorded after acting). It is open because the schema, examples, and validator are public, with no licensing or vendor lock-in. With a contract, an agent can map the application before acting, ask better questions, and respect the gates the author declared.

## Three paths into the standard

- Path A - Just read the standard. See [the standard](../standard/).
- Path B - Write a contract by hand. See [adding a contract by hand](../guides/adding-a-contract-by-hand.md).
- Path C - Use tooling. See [validating your contract](../guides/validating-your-contract.md).

## Start with the hello-contract

```yaml
contract_version: 0.1.0

app:
  id: example.notes-app
  purpose: >
    A small notes application that lets one user read notes they have already
    written.

contexts:
  - id: ctx.note-list
    label: Note list
    description: The list of saved notes available to the user.

actions:
  - id: action.list-notes
    label: List saved notes
    effect_class: read_only
    gate: none

human_ask: {}

receipts: []

provenance:
  author: synthetic example catalog
  generated_at: "2026-06-14T00:00:00Z"
  generator: hand-authored
```

This is the smallest valid v0 contract. It describes a read-only action with no human-authorization gate. See [/examples/hello-contract/](../examples/hello-contract/) for the full entry.

Copy this, replace `example.notes-app` with your own app id, and you have a valid v0 contract.

## Use this contract with an AI agent

A contract gives an agent a compact map of your contexts, actions, gates, and receipts. Paste it into a chat or attach it to a tool. It helps the agent ask better questions about scope, data, and authorization. The contract is descriptive: it does not enforce runtime safety, certify the application, or replace your judgment.

## Check your contract's readiness

Once you have a contract file, run:

    aoc-author audit path/to/your-contract.yaml

This produces a local readiness report. It tells you which gates are declared, which receipts your runtime is expected to produce, and what the audit found about your contract's structure. It does not produce a score, a badge, or a certification claim.

To supply optional machine-readable context:

    aoc-author audit path/to/your-contract.yaml \
        --readiness-context path/to/readiness-context.yaml

See the [validator guide](../guides/validating-your-contract.md) for installation and full usage.

## What this site does not claim

- This standard is **not** a runtime enforcement engine.
- This standard is **not** a compliance certification.
- This site does **not** offer paid or guaranteed support at v0.
- An Agent Operating Contract does **not** guarantee safe autonomous operation.
- This site does **not** speak for any external standards body.
- Using an AOC does **not** require our tooling.
