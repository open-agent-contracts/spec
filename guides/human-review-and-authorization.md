# Human Review And Authorization

This guide collects the human-loop best practices the contract
expects implementers to follow. Each item is grounded in a
public primary source. The contract's `gate` enum and
`human_ask` shape are the declarative side of these practices;
the runtime is responsible for honouring them.

This is guidance. It is not a certification, a compliance
claim, or an audit document.

## Consent Before Tool Invocation

A host must obtain explicit user consent before invoking any
tool, and should provide clear interface elements for
reviewing and authorizing the activity that follows. The
contract's `gate` enum reinforces this norm: any action with
an effect class beyond `read_only` defaults to
`review_required` or stricter, so a runtime that honours the
gate cannot run such an action silently.

A contract that declares `gate: none` on a non-`read_only`
action is asking the runtime to skip the consent step; the
validator will surface a finding, and a careful reviewer will
question the declaration.

## Sensitive Asks Travel Out-Of-Band

Sensitive values must not pass through the agent's text
channel. The MCP elicitation specification draws the line
explicitly: servers must not request passwords, API keys,
access tokens, or payment credentials through an in-band
form; those requests must use URL-mode elicitation so the
value is collected in a separate trusted surface.

The contract carries the same rule. `human_ask.channel`
should be `out_of_band` whenever the ask plausibly involves
credentials, payment, or other sensitive information. The
host is then responsible for presenting the out-of-band
surface; the contract is responsible for declaring that the
ask must travel that way.

## OAuth 2.1 With PKCE Is The Floor For Protected Resources

When an action's gate is `authorization_required` and the
target is a protected MCP server, the authorization flow must
use OAuth 2.1 with PKCE, with the client supplying the
Resource Indicator (RFC 8707) and the server publishing
Protected Resource Metadata (RFC 9728). The contract does not
re-specify those mechanics; it declares which actions need
authorization and leaves the OAuth flow to the runtime.

## Token-Passthrough Is Forbidden

MCP servers must not accept tokens that were not issued for
them, and must not forward tokens to downstream services. The
"confused deputy" incidents documented in the MCP authorization
specification are the reason. The contract carries an explicit
anti-claim that contracts do not authorize agents or runtimes
to passthrough tokens across service boundaries, so that any
projection that quietly enables passthrough is visibly out of
line with the contract.

## Originator Identity Must Be Bound

When an action's gate is `authorization_required` and the
projection uses MCP URL-mode elicitation, the runtime must
verify that the user who initiated the elicitation is the user
completing the out-of-band step. Without that binding, a
hostile party who learns the elicitation URL can impersonate
the originator and complete the authorization on their
behalf. The contract's guidance for any `authorization_required`
projection is therefore: bind the out-of-band step to the
originator's identity, or do not project the action through
URL-mode elicitation at all.

## Safe URL Handling

When the runtime presents a URL the user must visit to
complete an out-of-band step, the URL must be shown in full
before consent, the runtime must not pre-fetch or auto-open
the URL, the surface should highlight the registrable domain
to mitigate subdomain spoofing, and the surface should warn
on Punycode in the displayed URL. The contract relies on the
host to apply these rules; the rules themselves are the MCP
elicitation specification's "Safe URL Handling" section.

## Third-Party Skills And Plugins Must Be Audited

The Anthropic Agent Skills overview is explicit: use Skills
from trusted sources only, audit them as you would any
installed software, and treat external sources as risky. The
same posture applies to third-party contracts. A contract
imported from outside the project's trust boundary should be
audited as if it were a third-party plugin; the contract's
optional `provenance` field is the anchor that audit uses.

## Reading The Anti-Claims

Several of the practices above project into the contract's
`anti_claims` list. Anti-claims are not legal disclaimers;
they are the contract's record of what it intentionally does
not authorize. An anti-claim like "this contract does not
authorize token passthrough across service boundaries" makes
a previously implicit rule reviewable. A reviewer can see
what the contract intentionally rules out, not just what it
permits.

## What This Guide Is Not

- It is not a certification or compliance claim.
- It is not a substitute for the source specifications it
  cites.
- It is not exhaustive. The contract's gate vocabulary and
  human-ask shape capture the cross-runtime norms; specific
  surfaces may add their own.

## Public Sources Cited

- MCP specification (latest):
  `https://modelcontextprotocol.io/specification/latest`
- MCP authorization (2025-11-25):
  `https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization`
- MCP client elicitation (2025-11-25):
  `https://modelcontextprotocol.io/specification/2025-11-25/client/elicitation`
- Agent2Agent specification:
  `https://a2a-protocol.org/latest/specification/`
- Anthropic Agent Skills overview:
  `https://platform.claude.com/docs/en/docs/agents-and-tools/agent-skills/overview`
