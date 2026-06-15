---
title: Maintainer status dashboard
generated_at: 2026-06-14
build_date: 2026-06-14
generator: maintainers/source-currency/source_currency_probe.py status
inputs: page frontmatter under the portal source tree
contains_credentials: false
---

# Maintainer status dashboard

This page is generated at build from page frontmatter per CONCEPT-002
plan section 5.4. It lists every page whose `freshness_status` is
yellow or red so the maintainer can plan review work without walking
the whole portal tree.

The generator under `maintainers/source-currency/source_currency_probe.py
status` reads only page frontmatter; it never writes to page
frontmatter, the watchlist YAML, or any portal data file.

## Past-due pages (red)

No past-due pages on the 2026-06-14 build.

## Pages within the 30-day review window (yellow)

No pages within the 30-day review window on the 2026-06-14 build.

## Notes

- Yellow rows surface here whenever page frontmatter makes a page
  yellow under the CONCEPT-002 section 5.1 time-based rule. In the
  clean fixture, no page is inside the thirty-day review window, so
  the section above reads "No pages within the 30-day review window
  on the 2026-06-14 build."
- The S-5 compat index marks WebMCP yellow inside its own page, but
  that yellow status is on the compat row, not on a frontmatter-bearing
  portal page; the dashboard generator therefore does not surface it
  here. The compat-row freshness model lives in S-5; the page-level
  freshness model lives in S-6.
- An explicitly past-due fixture (`fixtures/dashboard/past-due/`)
  demonstrates the rendered shape this page takes when a page is past
  due. See `maintainers/source-currency/fixtures/dashboard/past-due/expected-status.md`
  for the rendered fixture output.
