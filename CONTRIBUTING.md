# Contributing

This is the local-only contributor guide for `Open Agent Contracts`.
It refines the S-1 contribution shell into a usable guide while every
publication gate stays closed.

`Open Agent Contracts` is not yet accepting external pull requests.
The public repository identifier is gated and remains unset until the
relevant gate clears. Once it does, this file routes future contribution
discussion to that repository. Until then, all work happens inside the
project's authoring environment under the same maintainer discipline
this guide describes.

## Where Contributions Will Land

Public issue and pull-request discussion will move to
`open-agent-contracts/spec` after the public repository gate closes.
The placeholder is intentional: there is no public repository today,
and nothing here implies that an external repository exists or accepts
pull requests at the present moment.

Public support routing is gated. Until then the maintainer contact
line reads `support@openagentcontracts.org`. The placeholder is not a
working address, and no response window or availability is claimed.

## Maintainer Anti-Lock-In Checklist

Every change to the portal source carries a pull-request-template
checklist matching the items below. The checklist lives here so a
reader can see the standard the project holds itself to without
opening a pull request.

- Schema fields that only the project's own tooling can populate are
  forbidden. Every field must be hand-writable by a competent
  developer with documentation alone.
- No portal-side accounts are required for reading. If a "claim a
  badge" surface ships later, login is acceptable at that surface
  only.
- No paid validation as the only validator. If a hosted validator
  ships later, the open-source reference validator must reach the
  same verdict on the same input, modulo performance.
- No "preferred framework" tilting. Projections into Model Context
  Protocol, WebMCP, OpenAPI, Agent2Agent, and other framework formats
  must be of comparable depth, and any depth gap must be recorded
  honestly in the compatibility registry.
- No portal-private examples. Every example shipped publicly must
  validate against the public schema using the public reference
  tooling.
- Compatibility rows must declare gaps and sharp edges where they
  apply. Pretending more coverage than exists is treated as a
  regression and reverted.

## How To Propose A Change Locally

While the public repository gate is closed, contributions follow the
project's local authoring workflow:

- For prose, schema, projection-guide, or compatibility-row changes,
  draft the change in the corresponding staging directory and run
  the staged hygiene checks before requesting review.
- For pledge wording changes, file an Request For Comments under the
  project's governance-evolution slot. The pledge wording is gated
  and does not change through ordinary pull requests.
- For changes that touch placeholders directly, do not substitute
  settled values into staged content. The placeholders are the v0
  vocabulary; substitution happens at transcription time once the
  relevant gate clears.

## Public Posture

No claim of public availability, support availability, response time,
external endorsement, marketplace listing, or hosted service applies
to v0. Where this guide refers to "the public repository", "the public
domain", "the maintainer flag", or "a future issue tracker", each is
a slot reserved for a gated decision that has not been made yet.

## Placeholders Used

This file carries three placeholders from the project's staging
placeholder vocabulary:

- `Open Agent Contracts` - the public project name. Replaced
  when the public name gate clears.
- `open-agent-contracts/spec` - the public-repository identifier
  where issues and pull requests will land. Replaced when the public
  repository gate clears.
- `support@openagentcontracts.org` - the public support-contact
  address. Replaced when the support-identity gate clears.

Each placeholder must be replaced with the settled value before the
file is transcribed to a public repository or otherwise published
externally.
