# Exporting To OpenAPI

This guide describes how to project an Agent Operating Contract
into an OpenAPI 3.2 document. OpenAPI owns the HTTP API surface;
the contract owns the agent-side declarations of effect class,
gate, human-ask shape, and receipts. The contract projects into
OpenAPI; the contract does not replace it.

## What OpenAPI Owns And What The Contract Owns

OpenAPI 3.2 owns the description of an HTTP API: paths,
operations, parameters, schemas, declarative security
requirements, callbacks, and webhooks. The contract owns the
classification of each action by effect, the gate vocabulary
that says when human review or authorization is required, the
out-of-band shape for sensitive asks, and the receipt envelope
the runtime should record. OpenAPI does not classify endpoints
by effect or reversibility; it does not specify a gate
vocabulary; it does not own a receipt envelope.

## Projection Map

Each contract field projects into an OpenAPI target as
follows.

- `app` projects into the OpenAPI `info` object. Use
  `info.title` for the application name and
  `info.description` for the purpose statement.
- `contexts` have no first-class OpenAPI concept. Carry them
  as OpenAPI tags or as a vendor extension such as
  `x-aoc-context` on the relevant operations.
- `actions` project into `paths.*.operation` entries. Each
  contract action maps to one `operationId`.
- `effect_class` projects as a vendor extension
  `x-aoc-effect-class` on the operation. OpenAPI 3.2
  supports specification extensions, so this projection is
  lossless on shape.
- `gate` projects as `x-aoc-gate` on the operation, paired
  with an OpenAPI Security Requirement Object when the gate
  is `authorization_required`. An OAuth2 security scheme
  represents the authorization step in OpenAPI's own
  vocabulary; the contract's `gate` value remains the
  declarative source of truth.
- `human_ask` projects as `x-aoc-human-ask`. OpenAPI does not
  have a native equivalent.
- `receipts` project through OpenAPI 3.2 webhooks. Each
  receipt event is modelled as a webhook payload. The
  contract's receipt list remains canonical; the OpenAPI
  webhook entries are the transport.

## The `x-aoc-*` Extension Style

The contract uses a short, consistent extension prefix so the
OpenAPI document remains readable and so a reader can recognise
contract-sourced metadata at a glance. The extensions are not
required by OpenAPI; they are how the contract carries fields
that have no native OpenAPI target. A tool that does not
understand the extensions can still consume the OpenAPI
document; the contract simply degrades to whatever the tool
already supports.

## Receipts Via Webhooks

OpenAPI 3.1 added `webhooks`, and OpenAPI 3.2 carries them
forward. Receipts project cleanly as webhook payloads: each
event the contract names becomes a webhook entry with a
schema for the payload shape. This projection is honest about
what OpenAPI offers natively. Webhooks are a transport for
receipts; OpenAPI does not specify a receipt envelope of its
own, so the contract's envelope remains the source of truth.

## Authorization Alignment

When an action's gate is `authorization_required`, the
OpenAPI projection should pair the `x-aoc-gate` value with a
Security Requirement that names the authorization scheme. A
contract that declares `authorization_required` without a
matching OpenAPI Security Requirement is internally
inconsistent; the validator on the contract side, and any
OpenAPI linter on the transport side, should both flag the
mismatch.

## What This Projection Does Not Promise

- It does not claim that OpenAPI natively supports a gate
  enum. It carries the contract's gate via an extension.
- It does not claim that webhooks turn OpenAPI into a
  receipt-bearing standard. Receipts remain owned by the
  contract.
- It does not address browser-side or agent-to-agent
  transports. Those have their own projection guides.

## Public Sources Cited

- OpenAPI specification (latest):
  `https://spec.openapis.org/oas/latest.html`
