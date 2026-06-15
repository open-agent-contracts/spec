# Exporting To Model Context Protocol

This guide describes how to project an Agent Operating Contract
into a Model Context Protocol (MCP) server surface. MCP owns the
transport, OAuth flow, and elicitation mechanism for
agent-tool communication. The contract sits above MCP and
projects into it; the contract does not replace MCP.

## What MCP Owns And What The Contract Owns

MCP owns the JSON-RPC transport between an agent host and
servers that expose tools, resources, and prompts. It also
owns the OAuth 2.1 authorization flow for HTTP transports and
an elicitation mechanism with `form` and `url` modes. The
contract owns the application-side declaration of which
actions exist, which gates each action requires, which receipts
the runtime should record, and which asks must travel
out-of-band. MCP runtimes are expected to honour the gate and
receipt declarations the contract carries.

## Projection Map

Each contract field projects into an MCP target as follows.

- `app.id` and `app.purpose` project into the MCP server name
  and the initialize-result `instructions` field. The
  projection is advisory; MCP's `instructions` is free-form.
- `contexts` project into MCP `Resources`. The mapping is
  N:1: one contract context may map to several MCP resource
  URIs.
- `actions` project into MCP `Tools`. Tool name, description,
  and input schema match directly. `effect_class` and `gate`
  ride along as tool annotations.
- `gate: review_required` projects into host-side confirmation
  UI on top of MCP. `gate: authorization_required` projects
  into MCP elicitation `mode: "url"` so the user can complete
  the authorization step out-of-band.
- `human_ask` projects into MCP elicitation. Use `form` mode
  for low-sensitivity in-band questions; use `mode: "url"`
  for anything sensitive, including credentials, access
  tokens, and payment information.
- `receipts` have no native MCP target. Carry them
  out-of-band; MCP does not specify a receipt envelope.
- `contract_version` projects into MCP server metadata as an
  advisory value.

## The URL-Mode Sensitive-Data Rule

MCP's elicitation specification draws a hard line between
in-band `form` mode and out-of-band `url` mode. Servers must
not use `form` mode to request passwords, API keys, access
tokens, or payment credentials; those requests must use
`url` mode so the sensitive value never passes through the
agent's text channel. The contract's `human_ask.channel`
field maps directly: any ask whose value belongs in
`url` mode should be declared as `channel: "out_of_band"` in
the contract.

This rule is load-bearing. A contract that declares a sensitive
authorization step with a non-sensitive channel such as
`channel: "in_app"` will produce an MCP projection that violates
the elicitation specification on the first sensitive ask.

## Token-Passthrough Anti-Claim

MCP servers must not accept tokens that were not issued for
them, and must not forward tokens to downstream services.
The contract should carry an explicit anti-claim that
contracts do not authorize agents or runtimes to passthrough
tokens across service boundaries. A contract that allows
token passthrough is not honouring the MCP authorization
model.

## Tool-Annotation Provenance

MCP tool annotations are treated as untrusted unless the
server itself is trusted. When the contract's `effect_class`
and `gate` project as MCP tool annotations, the projection
should also carry a `provenance` reference (for example, a
link to the canonical contract document) so a host can
verify the annotation source before relying on it.

## What MCP Does Not Cover

MCP does not classify actions by effect class, does not own a
cross-runtime gate vocabulary, and does not specify a receipt
envelope. The contract fills those gaps; the MCP projection
carries the contract's values as advisory metadata where MCP
itself has no native field.

## Public Sources Cited

- MCP specification (latest):
  `https://modelcontextprotocol.io/specification/latest`
- MCP authorization (2025-11-25):
  `https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization`
- MCP client elicitation (2025-11-25):
  `https://modelcontextprotocol.io/specification/2025-11-25/client/elicitation`
