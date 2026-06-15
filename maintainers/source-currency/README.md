# Source-currency probe

This directory stages the source-currency probe for the
`Open Agent Contracts` reference portal. The probe walks the
maintainer-edited watchlist at `about/watchlist/watchlist.yaml`,
fetches each primary URL (or loads a local fixture snapshot when in
fixture mode), computes a content hash, and opens a portal-repo issue
tagged `source-currency` when the hash changes. On a hash change that
also touches a version-string signal declared on the watchlist row,
the probe additionally tags the issue `framework-version-bump`.

## Issue-Surface Write Semantics Only

Per CONCEPT-002 plan section 5.2, the probe has issue-surface write
semantics only. It never edits page frontmatter, the watchlist YAML,
or any portal data file. The probe's only write surfaces are:

- its own state file (the `--state` argument);
- its issue payload output (the `--output-json` argument or standard
  output).

Granting the probe write access to data files in a later iteration is
gated by G-AUTOPUBLISH (CONCEPT-002 plan section 9.6).

## Files

- `source_currency_probe.py` - the probe (Python stdlib plus `pyyaml`,
  which is already a runtime dependency at
  `requirements-runtime.txt` in the source project).
- `source-currency.yml` - the inert staged GitHub Actions workflow
  that runs the probe on a daily cron once transcribed into the
  portal repo. References the portal repo only via
  `open-agent-contracts/spec` and the project only via
  `Open Agent Contracts`. Carries no credentials, tokens, or
  real repository identifiers.
- `fixtures/` - deterministic local fixtures used to verify the probe
  and dashboard logic without any network call:
  - `clean/` - prior hashes match current snapshots; no issue.
  - `changed/` - one row's content changed (and its version-signal
    regex match-count shifted), one row's content changed without a
    version-signal shift; expected output: two issue payloads, one
    labelled `source-currency` and `framework-version-bump`, one
    labelled `source-currency` only.
  - `dashboard/` - sample page-frontmatter trees the `status`
    subcommand consumes: one clean tree where the dashboard reads
    "no past-due pages" and "no pages within the 30-day review
    window"; one past-due tree where the dashboard lists the past-due
    page and excludes the green sibling.

## Subcommands

The probe is invoked as:

```text
python source_currency_probe.py <subcommand> [options]
```

### `check`

Walk the watchlist, fetch each URL or load a fixture snapshot,
compute hashes, compare against the state file, and emit issue
payloads for changed rows.

```text
python source_currency_probe.py check \
  --watchlist about/watchlist/watchlist.yaml \
  --state state/probe-state.json \
  --output-json /tmp/issues.json
```

For local fixture testing add `--fixture-dir <DIR>` and the probe
loads each URL's payload from `<DIR>/<sha256(url)>.html` instead of
calling the network.

The state file lives next to the probe in the portal repo (e.g.
`maintainers/source-currency/state/probe-state.json`). It records the
prior content hash plus the hex-encoded prior payload bytes per URL,
which the version-signal comparison reads on the next run.

Exit code:

- `0` if no issue payloads were emitted (clean run);
- `1` if at least one issue payload was emitted.

### `emit-issues`

Echo the issue payloads that would be opened against `--repo`. This
subcommand is intentionally inert in monorepo staging - it does not
call a portal-repo API and does not require credentials. After
G-REPO-HOST clears, the maintainer either wires an explicit API call
in the portal-repo workflow or treats this command as a dry-run check
before opening issues by hand.

```text
python source_currency_probe.py emit-issues \
  --input-json /tmp/issues.json \
  --repo open-agent-contracts/spec
```

### `status`

Generate the maintainer status dashboard from page frontmatter. Lists
pages whose `freshness_status` against the `--today` argument is
yellow or red. The clean default reads "no past-due pages" and "no
pages within the 30-day review window".

```text
python source_currency_probe.py status \
  --pages-dir <portal-source-tree> \
  --today 2026-06-14
```

## Gates Still Closed

- The probe cannot run end-to-end against the public portal repo
  until G-REPO-HOST + G-PROJECT-NAME + G-HOSTING clear and the portal
  repo exists. Until then the probe runs only locally against the
  fixture snapshots.
- The probe never writes to page frontmatter, the watchlist YAML, or
  any portal data file in v0; that capability is gated by
  G-AUTOPUBLISH.

## Hygiene Rules

- The probe is Python stdlib plus `pyyaml`; no other dependency is
  introduced.
- The staged workflow file references the portal repo only via
  `open-agent-contracts/spec` and the project only via
  `Open Agent Contracts`.
- The staged workflow file embeds no credential, secret, or token
  variable; the issue-emission step is deliberately deferred to
  portal-repo transcription time.
- The fixture URLs use the RFC 6761 `.invalid` TLD so they cannot
  reach the network even by accident.
- The probe deliberately stores the hex-encoded prior payload so the
  version-signal comparison is deterministic and does not need to
  re-fetch the prior content.
