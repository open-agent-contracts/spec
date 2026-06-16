# Open Agent Contracts

Open Agent Contracts is a draft open grammar for agent-ready apps.

An agent-ready app tells a personal agent what the app is for, what
context is available, which actions exist, what each action can change,
which actions need preview or human authorization, and what receipt proves
what happened.

This repository is the quiet public setup home for the v0 specification and
reference portal content. GitHub Pages is enabled for a small static front
door at `openagentcontracts.org`. It does not announce a public launch, publish
packages, submit marketplace listings, or claim certification.

## Start Here

- [Start here - what is an AOC and how do I use one?](start-here/)

- [The Standard](standard/)
- [Examples](examples/)
- [Framework Mappings](mappings/)
- [Compatibility Registry](compat/)
- [Guides](guides/)
- [Changelog](changelog/)
- [No-Lock-In Pledge](open/)
- [About](about/)

## Repository Contents

- `schema/v0.x/` - v0.1.0 JSON Schema and schema changelog.
- `standard/` - concepts, vocabulary, gates, receipts, versioning, and
  conformance.
- `examples/` - synthetic example contracts.
- `mappings/` - how Agent Operating Contracts project into adjacent agent and
  API surfaces.
- `compat/` - initial compatibility rows and registry index.
- `maintainers/` - hygiene, source-currency, and launch-readiness tools.

## Current Status

The v0 packet is setup-stage content. It has been transcribed into this clean
repository without private source history.

Still not done:

- public launch authorization;
- public support surface setup;
- marketplace submission;
- package publication;
- certification claims.

## Local Checks

Run the hygiene scan:

```bash
python3 maintainers/hygiene/hygiene_ci.py scan .
```

Run the inventory smoke:

```bash
python3 maintainers/smoketest/portal_smoketest.py
```

Both checks are local-only. They do not fetch external URLs, publish the
repository, open issues, send messages, spend money, or use credentials.
