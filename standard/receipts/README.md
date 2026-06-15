# Receipts

AOC owns the receipt envelope for v0.1.0. No surveyed framework owns a portable
receipt-of-record shape for proposal, approval, refusal, execution, and outcome
capture across runtimes.

The `receipts` field is an array of event-name strings the contract says a
compliant runtime is expected to emit.

## Canonical Vocabulary

The canonical recommended receipt names are:

- `proposed`: agent has presented a proposed action.
- `approved`: human or equivalent authority approved the proposal.
- `refused`: human or equivalent authority declined the proposal.
- `executed`: the action ran.
- `outcome_recorded`: the executed action's outcome is captured.

Contracts may add custom receipt names. Unknown receipt names are accepted.

## Coverage Rules

The v0 validator enforces these receipt-coverage rules:

- R-1: for any non-`read_only` action, `receipts[]` must include `proposed`.
- R-2: for any action with `gate` of `review_required` or
  `authorization_required`, `receipts[]` must include at least one of
  `approved` or `refused`.
- R-3: for any non-`forbidden` action whose `gate` allows execution,
  `receipts[]` must include `executed`.
- R-4: custom receipt names are allowed.

`outcome_recorded` is recommended but not validator-enforced in v0.1.0.

## Runtime Obligation

The validator can only inspect the declaration. A runtime is responsible for
actually emitting each declared event when it runs.

Receipts are operational artifacts for the agent-app interaction. They are not
a substitute for a regulatory audit log.
