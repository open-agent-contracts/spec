# Gates

AOC v0.1.0 classifies each action with two fields:

- `effect_class`: what kind of effect the action can have.
- `gate`: what must happen before the action proceeds.

## Effect Class

The `effect_class` enum is closed in v0.1.0:

- `read_only`: no state change anywhere.
- `reversible_internal`: state change confined to this app, undoable.
- `external`: state change reaches outside this app, such as a third-party
  API, email, or payment surface, even if internally reversible.
- `irreversible`: state change cannot be undone by the contract author.

## Gate

The `gate` enum is closed in v0.1.0:

- `none`: agent may act. Maps to host-level consent.
- `preview`: agent must show evidence of effect before acting.
- `review_required`: must show and obtain explicit human approve/decline.
- `authorization_required`: must obtain authorization via an out-of-band flow.
- `forbidden`: agent must refuse to propose.

## Default Posture

Every non-`read_only` action should declare `review_required` or stricter.

The validator emits a finding when a non-`read_only` action declares
`gate: none`. This is a finding, not an error, because v0 separates "valid" from
"complete".

## Authorization Rule

If an action declares both:

- `gate: authorization_required`; and
- `effect_class: external` or `effect_class: irreversible`;

then the contract must set:

- `human_ask.channel: out_of_band`

The validator emits `E_OUT_OF_BAND_REQUIRED` when that rule is violated.

## Runtime Boundary

AOC declares the gate. A runtime, host, or framework must enforce it. A valid
contract does not prove that a runtime actually displayed a preview, collected
approval, completed an authorization flow, or refused a forbidden action.
