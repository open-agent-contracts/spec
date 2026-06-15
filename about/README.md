# About

## Mission

`Open Agent Contracts` is an open standard project. The standard it
publishes is the Agent Operating Contract (AOC), a vendor-neutral grammar
for describing what an application allows a personal agent to do on a
user's behalf, which actions need human review or authorization, and how
those actions are receipted afterwards.

The project ships the standard, a reference JSON Schema, a reference
validator, synthetic worked examples, projection mappings into adjacent
public surfaces (Model Context Protocol, OpenAPI, Agent2Agent, llms.txt,
and others), and a compatibility registry that records what each
surveyed surface covers and where it falls short. The standard is the
public good; `Open Agent Contracts` aims to be a reliable steward of
that standard rather than a gatekeeper to it.

## License Stack

License terms for each content class are gated and remain unset until
the project's licensing decisions land. Until then every cell in the
table below reads as a placeholder.

| Content class | License |
|---|---|
| Portal prose and guides | `schema/examples CC0-1.0; validator/plugin code Apache-2.0; portal/docs CC BY 4.0` |
| Reference JSON Schema | `schema/examples CC0-1.0; validator/plugin code Apache-2.0; portal/docs CC BY 4.0` |
| Synthetic worked examples | `schema/examples CC0-1.0; validator/plugin code Apache-2.0; portal/docs CC BY 4.0` |
| Reference validator code | `schema/examples CC0-1.0; validator/plugin code Apache-2.0; portal/docs CC BY 4.0` |
| Compatibility registry data | `schema/examples CC0-1.0; validator/plugin code Apache-2.0; portal/docs CC BY 4.0` |

A `LICENSE` file at the portal repository root records the project's
licensing decision once the relevant gates clear.

## Provisional Naming

Project names, package ids, domain, and public schema namespace in this
portal are provisional until the project's naming gate clears. Internal
dogfood examples may reference `aoc/v0.x`, but the published schema
`$id` remains gated.

By way of example, the four deferred identifiers this callout covers
appear in staging as `Open Agent Contracts` (the public project
name), `openagentcontracts.org` (the primary public domain),
`agent-contract-kit` (the durable package id used by any future
reference validator distribution), and `https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json` (the
public schema `$id` URI). Each is replaced with a settled value when
the corresponding gate closes; until then the staging tree shows the
placeholder so a reader can see the substitution slot.

## Public And Private Boundary

This portal publishes a standard, a reference schema, a reference
validator, synthetic examples, projection guides, and a compatibility
registry. It does not publish private context.

Concretely, the public surface of this portal is limited to material
that an outside reader can verify against publicly cited sources or
against the synthetic examples shipped here. The portal does not
import private orchestration substrate, private maintainer context,
private customer data, private credentials or secrets, session
transcripts of private systems, screenshots of private systems,
internal monorepo paths, or any unreleased commercial strategy.
Every example shipped here is synthetic and validates against the
public schema using only the public reference validator.

This portal contains only synthetic, public-safe material; private internal context is intentionally excluded.

The discipline above states the rule the project enforces on its own
publication surface. It does not name any source project from which
the project derives. The provenance of that discipline, where the
project chooses to publish it as provenance, is a separate maintainer
decision.

## Governance Posture

`Open Agent Contracts` ships v0 under a current maintainer-led
posture. There is no named maintainer in v0; the maintainer flag is
gated and remains unset until the governance gate clears.

The portal reserves a governance-evolution RFC slot. When the
governance posture changes (for example by adding co-maintainers,
moving to a working-group model, or chartering a steering committee)
the change is proposed as an RFC in that slot, reviewed in public,
and then recorded on this page with a dated entry. The RFC mechanism
is the public seam for evolving governance without re-asking each
underlying decision case-by-case.

## What This Is Not

The standard `Open Agent Contracts` publishes is deliberately
narrow. The list below records the things the v0 standard is not.
Each line uses the wording the project's anti-claim list records and
is shipped verbatim so a reader can scan it without ambiguity.

1. AOC is not a runtime.
2. AOC is not a compliance certification.
3. AOC does not replace MCP.
4. AOC does not replace OpenAPI.
5. AOC does not replace A2A.
6. AOC does not replace llms.txt.
7. AOC does not promise that an agent will behave well.
8. AOC does not authorize token passthrough (MCP `/authorization` "Access Token Privilege Restriction" forbids this).
9. AOC does not replace WebMCP. (Human confirmation is Open Question in WebMCP; AOC declares, host enforces.)
10. AOC does not certify vendor-specific agent surfaces.
11. AOC does not ship a numeric readiness score.
12. AOC does not bind external regulations to its receipt format.
13. AOC does not adopt llms.txt as a standards-body-grade specification (it is cited as a community proposal).
14. AOC does not promise that WebMCP, agents.json, or OpenAI Apps SDK self-serve are stable.

Each item is restated on the projection pages that touch the relevant
vendor surface so a reader who arrives at a specific projection guide
encounters the same restraint in context.

## Support

Public support routing is gated. Until the relevant gate clears, the
contact line below carries a placeholder. The placeholder is not a
working address and is not monitored. No availability window, response
time, or commercial-support arrangement is claimed.

Contact: `support@openagentcontracts.org`.

Bug reports, projection corrections, compatibility-registry updates,
and pledge wording feedback move through the project's issue tracker
once the public repository gate clears; until then those channels are
local to the project's authoring environment and are not externally
reachable.
