---
standard_version: v0.x
framework: a2a
framework_version_pinned: 1.0
verified_on: 2026-06-13
next_review_due: 2026-09-13
freshness_status: green
---

# A2A Mapping

This page describes how an AOC v0.x contract projects into the Agent2Agent
(A2A) Protocol. It is a projection map, not a replacement claim.

Public schema identifier for this AOC reference: `https://schemas.openagentcontracts.org/aoc/v0.1.0/contract.schema.json`.

## Status

- Framework: Agent2Agent Protocol (A2A).
- Version pinned: v1.0.
- Authority: Linux Foundation A2A project, with a multi-vendor Technical
  Steering Committee.
- AOC posture: projection target for agent-to-agent surfaces. AOC does not
  redefine the A2A wire protocol or task lifecycle. AOC describes the action
  catalog and the gate; A2A carries the agent-to-agent transport and the
  interruption pattern.

## Source Currency

Primary public sources cited:

- Project home: `https://a2a-protocol.org/latest/`
- Specification: `https://a2a-protocol.org/latest/specification/`

Re-verification cadence: 3 months. v1.0 is recently announced and 1.x
iteration is expected.

## What Projects Cleanly

- An AOC `app.id` and `app.purpose` project into the A2A Agent Card identity
  and capabilities fields. The Agent Card is a JSON metadata document
  describing identity, capabilities, skills, service endpoint, and
  authentication requirements.
- AOC `contexts[]` project into Agent Card skills and per-task message parts.
  The projection is advisory because A2A is the agent-to-agent surface and
  the AOC contexts are abstract entities the calling agent reasons about.
- AOC `actions[]` project into A2A skills declared on the Agent Card. A2A
  skill granularity is coarser than AOC action granularity, so one A2A skill
  often encompasses several AOC actions.
- AOC `gate: review_required` projects 1:1 into A2A
  `TASK_STATE_INPUT_REQUIRED`. The A2A interrupted-task state requires client
  interaction before the task can resume.
- AOC `gate: authorization_required` projects 1:1 into A2A
  `TASK_STATE_AUTH_REQUIRED`. The A2A interrupted-task state requires the
  client to complete an authorization step before the task can resume.
- AOC `human_ask` data carries naturally into the message that the client
  returns when responding to an interrupted task.

A2A's interrupted-task states are the cleanest semantic alignment of AOC's
gate concept across any surveyed standard.

## Covered Fields

```yaml
covered_fields:
  - app
  - contexts
  - actions
  - gate
  - human_ask
```

## Gaps

```yaml
gaps:
  - field: effect_class
    reason: "A2A does not classify skill effect. The projection carries effect_class as advisory metadata on the skill, not as a typed enum."
  - field: receipts
    reason: "A2A models task outputs as Artifacts and emits task-state transitions. There is no normative receipt-of-record envelope. AOC receipts ride alongside the A2A transport rather than inside it."
  - field: anti_claims
    reason: "A2A does not model anti-claim text natively."
```

## Sharp Edges

```yaml
sharp_edges:
  - "A2A skill granularity is coarser than AOC action granularity. A single A2A skill commonly maps to many AOC actions. Maintainers should not assume one-to-one alignment when reading projections."
  - "Agent Card publication can leak unintended capabilities if the card is published without privacy review. AOC contexts[] and actions[] are advisory inventories, not obligatory disclosures of every internal capability."
  - "A2A interrupted-task states require client interaction. A runtime that ignores INPUT_REQUIRED or AUTH_REQUIRED is non-conformant. AOC declares which gate; A2A carries the interruption."
  - "A2A optional capabilities such as streaming, pushNotifications, and extendedAgentCard are framework-side concerns. AOC does not model them and does not require them."
```

## Interrupted-Task State Alignment

A2A task states include both active states such as `TASK_STATE_SUBMITTED` and
`TASK_STATE_WORKING`, the interrupted states `TASK_STATE_INPUT_REQUIRED` and
`TASK_STATE_AUTH_REQUIRED`, and the terminal states `TASK_STATE_COMPLETED`,
`TASK_STATE_FAILED`, `TASK_STATE_CANCELED`, and `TASK_STATE_REJECTED`.

AOC gates land on the two interrupted states without translation loss:

- `review_required` -> `TASK_STATE_INPUT_REQUIRED`
- `authorization_required` -> `TASK_STATE_AUTH_REQUIRED`

The mapping is semantic, not declarative. AOC carries the declaration; A2A
carries the transition.

## Anti-Claims

- AOC does not replace A2A. AOC does not specify an agent-to-agent wire
  protocol. A `gate: review_required` action projects into
  `TASK_STATE_INPUT_REQUIRED`, not the other way around.
- AOC does not claim Technical Steering Committee endorsement or any review
  by the A2A project, the Linux Foundation, or any member organization.
- AOC does not promise that a runtime will honor an A2A interruption. A valid
  contract describes the gate; the runtime is responsible for enforcement.
