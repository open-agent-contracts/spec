# Adding A Contract By Hand

This guide shows that you can write an Agent Operating Contract for
your own application using only a text editor. You do not need a
portal account, a hosted service, a paid tool, or any
project-specific command-line tool. The validator covered in a
separate guide is an optional follow-up; the hand-authored shape on
this page is by itself a valid contract.

## Why This Guide Exists

The Agent Operating Contract is a public, open grammar. A contract
is a small YAML or JSON document with a handful of well-known
fields. If a tool ever requires you to install or sign up for
something just to write the contract document itself, that tool is
not honouring the no-lock-in posture. This guide proves that the
hand-authored path is always available.

## What You Need

- A text editor that saves UTF-8 plain text.
- An idea of which application you are describing and which
  actions agents may take inside it.
- Roughly twenty minutes for a small application.

You do not need a package manager, a runtime, a portal account, an
API key, network access, or any vendor-specific tooling.

## The Smallest Useful Contract

A minimal v0 contract has the following structure. The example
below is synthetic and describes a hypothetical local note-taking
application.

```yaml
contract_version: "0.1.0"
app:
  id: "notes-app"
  purpose: |
    A local-only note-taking application. Agents should help
    capture and organise short personal notes, never publish them
    to a third party.
provenance:
  author: "human"
  generator: "hand-authored"
  generated_at: "2026-06-14T12:00:00Z"
contexts:
  - id: "note-list"
    label: "Note list"
    purpose: "The list of notes the user currently sees."
  - id: "selected-note"
    label: "Selected note"
    purpose: "The note the user is editing right now."
actions:
  - id: "create-note"
    label: "Create note"
    effect_class: "reversible_internal"
    gate: "review_required"
  - id: "delete-note"
    label: "Delete note"
    effect_class: "irreversible"
    gate: "review_required"
human_ask:
  channel: "in_app"
  note: "Use plain language; never request credentials in chat."
receipts:
  - "proposed"
  - "approved"
  - "refused"
  - "executed"
  - "outcome_recorded"
anti_claims:
  - "This contract does not authorize the agent to send notes to
    any external service."
```

If you save that file as `aoc.yaml` next to your application's
source, you have a contract. Nothing else is required to make it
exist.

## Field-By-Field Walkthrough

The fields above are the v0 mandatory minimum; the rest of this
section walks through what each one means and how to fill it in by
hand for your own application.

### `contract_version`

The validator-target version string the contract is written
against. Use `"0.1.0"` for v0 contracts.

### `app`

A short identity block for the application the contract describes.

- `id`: a short, lowercase, hyphenated identifier. Pick something
  stable that you control.
- `purpose`: a few sentences that describe what the application is
  for from an agent's point of view. Write for an agent that has
  never seen the app before.

### `provenance`

A small block that records who wrote the contract and when. For a
hand-authored contract, the simplest values are
`author: "human"`, `generator: "hand-authored"`, and
`generated_at: "<ISO-8601 timestamp>"`. If a tool authored it, the
tool should record itself here.

### `contexts`

The agent-facing surfaces inside the application. A context is
something an agent should read or subscribe to before suggesting
actions. Contexts are entity-shaped, not URL-shaped. Two or three
contexts is enough for a small application. Give each context an
`id`, a short `label`, and a plain-language `purpose`.

### `actions`

The things an agent may propose. Each action carries:

- `id`: a short, stable identifier.
- `label`: a short human-readable action name.
- `effect_class`: one of `read_only`, `reversible_internal`,
  `external`, or `irreversible`.
- `gate`: one of `none`, `preview`, `review_required`,
  `authorization_required`, or `forbidden`.

The pairing rule is simple: anything beyond `read_only` should
default to `review_required` or stricter. `irreversible` actions
should default to `review_required` or `authorization_required`.

### `human_ask`

How an agent may ask a person for input. `channel: "in_app"` is for
non-sensitive questions inside the application; `channel:
"out_of_band"` is required when the ask involves credentials,
payment, or any other sensitive value that should not pass through
the agent's text channel.

### `receipts`

The events the contract expects the runtime to record. The four
events most contracts record are `proposed`, `approved` or
`refused`, `executed`, and `outcome_recorded`. Receipts are owned by
the contract; runtimes that import the contract are expected to
honour them.

### `anti_claims`

Things the contract explicitly does not authorize. Anti-claims are
how a contract becomes auditable: a reviewer can see what was
intentionally ruled out, not only what was permitted.

## A Hand-Authoring Checklist

If you are writing a contract from scratch, the following
checklist usually produces a usable v0 document:

1. Identify the application and its purpose from an agent's point
   of view.
2. List the contexts an agent should read before acting.
3. List the actions an agent may propose. For each action, write
   the `effect_class` first, then the `gate`.
4. For any action with `effect_class: external` or
   `effect_class: irreversible`, default the gate to at least
   `review_required`. Use `authorization_required` if the action
   touches a protected resource.
5. Write the `human_ask` block. Default the channel to
   `out_of_band` if any plausible ask involves credentials,
   payment, or other sensitive values.
6. List the receipt events you expect to be recorded.
7. Write at least one anti-claim that captures something the
   contract intentionally does not authorize.

That checklist alone produces a contract a reviewer can read and
that a runtime can consume. The validator guide describes how to
check the document against the v0 schema as an optional follow-up.

## What This Guide Does Not Cover

- Programmatic generation of contracts from existing source.
- Projection of the contract into Model Context Protocol,
  OpenAPI, or Agent2Agent surfaces. Each projection has its own
  guide.
- Hosted or paid services.

## Public Sources Cited

This guide is hand-authoring-only and cites no external standards
in its body. The projection guides cite the relevant primary
sources for each export surface.
