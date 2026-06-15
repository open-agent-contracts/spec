---
standard_version: v0.x
framework: mcp
framework_version_pinned: 2025-11-25
verified_on: 2026-06-13
next_review_due: 2026-09-13
freshness_status: green
---

# MCP Mapping

This page describes how an AOC v0.x contract projects into the Model Context
Protocol (MCP). It is a projection map, not a replacement claim.

Public schema identifier for this AOC reference: `https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json`.

## Status

- Framework: Model Context Protocol.
- Version pinned: 2025-11-25.
- Authority: project home (model-context-protocol org; specification is
  developed and released in public).
- AOC posture: projection target. AOC does not redefine MCP transport,
  authorization, or elicitation. AOC declares the action shape and the gate;
  MCP carries the transport and consent flow.

## Source Currency

Primary public sources cited:

- Specification overview: `https://modelcontextprotocol.io/specification/latest`
- Authorization section: `https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization`
- Elicitation section: `https://modelcontextprotocol.io/specification/2025-11-25/client/elicitation`

Re-verification cadence: 3 months. Active spec; URL-mode elicitation was
introduced in 2025-11-25 and may iterate.

## What Projects Cleanly

- An AOC `app.id` and `app.purpose` project into the MCP server name and the
  `instructions` field returned during initialization. The projection is
  advisory because MCP `instructions` is free-form prose.
- AOC `contexts[]` project into MCP Resources. The projection is lossy because
  AOC contexts are abstract entities and MCP Resources are URL-shaped, so a
  single AOC context often expands to several Resource URIs.
- AOC `actions[]` project into MCP Tools. Tool name, description, and input
  schema map cleanly. AOC `effect_class` and `gate` ride along as tool
  annotations, which MCP treats as untrusted unless the server is trusted.
- AOC `gate: authorization_required` projects into MCP elicitation
  `mode: "url"` for the consent step, paired with MCP's OAuth 2.1 + PKCE +
  RFC 8707 + RFC 9728 flow for protected resource access.
- AOC `gate: review_required` projects into MCP elicitation `mode: "form"`
  for in-band questions and into the host-side confirmation UI for explicit
  approve/decline.
- AOC `human_ask.channel: out_of_band` projects into MCP elicitation
  `mode: "url"` for sensitive asks (see the URL-mode rule below).

## Covered Fields

```yaml
covered_fields:
  - app
  - contexts
  - actions
  - effect_class
  - gate
  - human_ask
  - contract_version
```

## Gaps

```yaml
gaps:
  - field: receipts
    reason: "MCP has no receipt envelope. Receipts ship as a separate AOC artifact."
  - field: anti_claims
    reason: "MCP does not model anti-claim text natively. AOC carries the field."
```

## Sharp Edges

```yaml
sharp_edges:
  - "MCP tool annotations are treated as untrusted unless the server itself is trusted. An AOC effect_class or gate projected as an annotation must carry provenance, and the host should not trust annotations from unknown servers."
  - "MCP elicitation form mode MUST NOT carry passwords, API keys, access tokens, or payment credentials. The spec uses URL mode for those. AOC contracts that involve sensitive asks must set human_ask.channel to out_of_band so that the projection lands in URL mode."
  - "MCP authorization forbids token passthrough. An MCP server MUST NOT accept a token that was not issued for it, and MUST NOT forward a token to a downstream API. AOC contracts must not encode token-passthrough expectations into a projection."
  - "URL-mode elicitation must verify that the same user who initiated the elicitation completes the out-of-band step. AOC projections of authorization_required must bind to the originator's identity to avoid the phishing-takeover described in the elicitation specification."
  - "MCP cannot enforce safety at the protocol level. Tool Safety in the specification is a principles section, not an enforcement mechanism."
```

## URL-Mode Elicitation Rule

The MCP 2025-11-25 elicitation specification draws a hard line:

- MUST NOT use form mode to request passwords, API keys, access tokens, or
  payment credentials.
- MUST use URL mode for any such ask.
- MUST verify that the originator of the elicitation is the user completing
  the out-of-band step.
- MUST NOT pre-fetch URLs and MUST NOT open URLs without user consent.
- MUST show the full URL before consent, SHOULD highlight the domain, and
  SHOULD warn on Punycode.

AOC contracts honor this projection by routing sensitive asks through
`human_ask.channel: out_of_band` and by leaving the URL-handling rules to the
MCP host. AOC declares the requirement. MCP carries the consent step.

## Anti-Claims

- AOC does not replace MCP. AOC projects into MCP tools, resources, prompts,
  elicitation, and the OAuth 2.1 + PKCE + RFC 8707 + RFC 9728 flow. AOC does
  not redefine any of those.
- AOC does not authorize token passthrough across service boundaries.
- AOC does not certify any MCP server as safe. A valid AOC contract describes
  the boundaries an agent should respect. It does not prove that a runtime
  displayed a preview, collected approval, completed an authorization flow, or
  refused a forbidden action.
- AOC does not claim that the MCP specification body or any working group has
  endorsed this projection.
