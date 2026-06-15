# FEATURE-007 S-10 - Local Launch Dry-Run

This is local staging for the FEATURE-007 S-10 v0 launch dry-run and
smoketest packet.

It does not publish the portal, create a public repository, register or
configure a domain, configure hosting, replace placeholder literals with
durable public values, run public portal CI, claim support availability,
announce launch, accept external contributions, send messages, spend money, or
run any credentialed check.

The packet exists so a maintainer can see exactly what must be true before the
portal can move from local staging to a public launch path.

## Files

- `maintainers/launch-dry-run.md` - gate checklist for placeholder
  replacement, portal-repo readiness, hygiene CI, publication, and launch.
- `maintainers/skeptical-reader-walkthrough.md` - maintainer-self skeptical
  reader pass for v0 local staging.
- `maintainers/smoketest/expected-inventory.json` - deterministic local
  inventory of staged portal surfaces.
- `maintainers/smoketest/portal_smoketest.py` - local stdlib smoke checker for
  the inventory above.
- `HYGIENE-RECEIPT.md` - S-10 receipt and boundary record.

## Local Smoke Command

Run from the repo root:

```bash
python3 maintainers/smoketest/portal_smoketest.py
```

The checker is local-only. It reads the staged portal source under
this repository content tree and the maintainer hygiene tools.
It does not read or write a public portal repository.

## Current Dry-Run Status

Local staging inventory can pass. Public launch cannot proceed yet.

The launch checklist still contains unresolved `AA_*_PLACEHOLDER` literals by
design, and the public portal repo / domain / hosting / launch gates remain
closed. S-9A hygiene CI must fail any publish branch that still contains those
placeholder literals.

## Operator Gates Still Closed

- Public portal repo creation and first transcription.
- Domain registration, DNS, hosting, and deploy.
- Placeholder replacement in portal-bound surfaces.
- License publication.
- Public support surface.
- Governance and open-pledge final sign-off.
- Public launch announcement.
- Any external submission, send, spend, credentialed check, or irreversible
  action.
