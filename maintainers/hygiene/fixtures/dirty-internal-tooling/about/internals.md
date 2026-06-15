# Internals

This fixture leaks the private orchestrator command bin/loom into
portal-bound copy. The hygiene CI must refuse this string per
CONCEPT-002 plan section 7.4 orchestrator row.
