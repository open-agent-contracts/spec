# Exporting To Agent2Agent

This guide describes how to project an Agent Operating Contract
into an Agent2Agent (A2A) v1.0 surface. A2A owns agent-to-agent
discovery and task lifecycle; the contract sits above the wire
and projects its agent-facing declarations into the Agent Card
and task states A2A defines. The contract does not replace A2A.

## What A2A Owns And What The Contract Owns

A2A v1.0 owns the Agent Card (a JSON metadata document that
describes an agent's identity, capabilities, skills, endpoint,
and authentication requirements), the task lifecycle with its
active, interrupted, and terminal states, and optional
capabilities like streaming, push notifications, and an
extended Agent Card. The contract owns the application-side
declaration of which actions exist, which gates each action
requires, which receipts the runtime should record, and which
asks must travel out-of-band. A2A does not classify skills by
effect class and does not specify a normative receipt
envelope; those are the contract's job.

## Projection Map

Each contract field projects into an A2A target as follows.

- `app.id` and `app.purpose` project losslessly into the
  Agent Card's identity and capabilities fields.
- `contexts` project as advisory metadata on Agent Card
  skills and into per-task `Message.parts` at runtime. A2A
  is agent-to-agent rather than app-to-agent, so contexts
  become discoverable skill surfaces rather than entity
  references.
- `actions` project into skills declared on the Agent Card.
  A2A's skill granularity is typically coarser than a
  contract action; one A2A skill may encompass several
  contract actions.
- `effect_class` is advisory on the projected skill. A2A
  does not classify skill effect natively, so the value
  rides as a non-normative annotation.
- `gate: review_required` projects into the A2A interrupted
  task state `TASK_STATE_INPUT_REQUIRED`. The interruption
  carries the data the client needs to satisfy the review
  and resume the task.
- `gate: authorization_required` projects into
  `TASK_STATE_AUTH_REQUIRED`. The client completes the
  authorization step and returns the task to an active
  state.
- `human_ask` projects losslessly into the data carried by
  `TASK_STATE_INPUT_REQUIRED` and the Message the client
  returns. A2A treats interruption-driven asks as
  first-class; the contract's `human_ask` shape rides
  directly on the wire.
- `receipts` project as A2A `Artifact` outputs and as
  task-state transitions. A2A does not specify a normative
  receipt envelope; the contract's envelope remains canonical
  and the Artifact transport carries the values.

## Why The A2A Alignment Is The Cleanest Surveyed

Across the surveyed standards, A2A's interrupted task states
are the cleanest semantic alignment with the contract's gate
vocabulary. `TASK_STATE_INPUT_REQUIRED` and
`TASK_STATE_AUTH_REQUIRED` are first-class states that
"require client interaction" by name; nothing else in the
public landscape names the human-loop pause as part of the
task lifecycle. The contract's `review_required` and
`authorization_required` gates project to these two states
one-to-one, which is the closest fit any standard offers.

This alignment is also why the contract does not try to own
agent-to-agent discovery. A2A already owns it. The contract's
job is to declare the gates; A2A's job is to interrupt the
task when a gate fires.

## What This Projection Does Not Promise

- It does not claim that A2A natively supports effect class.
  Effect class rides as advisory metadata.
- It does not claim that Agent Card publication is
  obligatory. Contexts and actions are advisory inventories,
  not mandatory public disclosures.
- It does not claim A2A endorsement. Endorsement decisions
  belong to the project maintainers and to the Technical
  Steering Committee of the A2A project.

## Public Sources Cited

- Agent2Agent home: `https://a2a-protocol.org/latest/`
- Agent2Agent specification:
  `https://a2a-protocol.org/latest/specification/`
