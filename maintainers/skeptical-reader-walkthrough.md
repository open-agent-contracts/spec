# Skeptical Reader Walkthrough

Status: local maintainer-self walkthrough for v0 staging.

The goal is to read the staged portal as a skeptical builder would: can a
builder understand the standard, hand-write a contract, validate it, map it to
common agent surfaces, and see what is not promised?

## Reader Persona

The reader is a builder evaluating whether to adopt Agent Operating Contracts
without adopting a private toolchain.

The reader should assume no access to private project history, internal
workflows, customer data, hosted systems, screenshots, or transcripts.

## Walkthrough Steps

| Step | Local source | Question | Local result |
|---|---|---|---|
| 1 | S-1 home and IA shell | Is the portal shape understandable without a login or hosted account? | Pass for local staging. |
| 2 | S-2 standard pages | Are concepts, schema, vocabulary, gates, receipts, versioning, and conformance documented? | Pass for local staging. |
| 3 | S-3 examples | Are examples synthetic and validator-clean? | Pass for local staging; S-10 closeout reruns the validator. |
| 4 | S-4 mappings | Do mappings project AOC into existing surfaces instead of replacing them? | Pass for local staging. |
| 5 | S-5 compat registry | Are framework gaps and sharp edges visible? | Pass for local staging. |
| 6 | S-6 source-currency | Is source freshness visible without live automation claims? | Pass for local staging. |
| 7 | S-7 guides and changelog | Can a builder hand-author, validate, and project a contract without mandatory tooling? | Pass for local staging. |
| 8 | S-8 about/open/boundary | Are no-lock-in, anti-claims, public/private boundary, support limits, and governance posture visible? | Pass for local staging; final pledge/governance still gated. |
| 9 | S-9A/S-9B | Is there a hygiene path before public transcription? | Pass for local staging; real portal use remains gated. |
| 10 | S-10 launch checklist | Does the checklist refuse premature launch? | Pass for local staging. |

## Placeholder Visibility Pass

The reader confirms that unresolved placeholder literals remain visible in the
launch checklist and are treated as launch blockers, not as public values.

Required unresolved rows:

- P-1 public name placeholder.
- P-2 domain placeholder.
- P-3 package-id placeholder.
- P-4 marketplace-identity placeholder.
- P-5 support-identity placeholder.
- P-6 license-stack placeholder.
- P-7 schema-id placeholder.
- P-8 portal-repo placeholder.

Result: pass for local staging visibility only. The placeholders are explicit
and the launch checklist says they must be replaced before public portal
launch.

## Placeholder Replacement Evidence Pass

Status: deferred.

The full replacement-evidence pass required by the S-10 plan cannot complete
inside this local slice because the public portal branch does not exist here
and the operator-gated replacement evidence rows have not been recorded.

This is a launch blocker, not a local staging defect.

## Anti-Claim Pass

The reader verifies that the portal does not claim:

- autonomous safety;
- runtime enforcement;
- certification;
- marketplace approval;
- hosted support availability;
- third-party endorsement;
- public launch;
- external contribution availability today.

Result: pass for local staging.

## Remaining Launch Blockers

- No public portal repo exists in this local slice.
- No domain, DNS, hosting, or deploy path is configured.
- Placeholders are not resolved in a publish branch.
- S-9A has not run inside a real public portal repo.
- Rendered link checks have not run against a merged portal branch.
- Maintainer sign-off is not recorded.
- G-LAUNCH is not authorized.

## Verdict

The staged portal is credible enough for a local S-10 smoke packet.

It is not ready for public launch.
