"""Tests for the FEATURE-007 portal-repo hygiene CI.

Standard library only. The test harness feeds each negative fixture
tree to the scanner as an explicit `--tree` argument; it never points
a recursive walker at the fixtures directory.

This test file lives outside the fixture directory and therefore must
not carry raw policy literals; it asserts behavior by checking row
citations and exit codes in the scanner output.
"""

import io
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
HYGIENE_DIR = os.path.dirname(HERE)
FIXTURES_ROOT = os.path.join(HYGIENE_DIR, "fixtures")
HYGIENE_CI = os.path.join(HYGIENE_DIR, "hygiene_ci.py")

# Import the module under test directly so we can also exercise the
# in-process API. The CLI is exercised via subprocess.
sys.path.insert(0, HYGIENE_DIR)
import hygiene_ci  # noqa: E402


def _run_cli(*args):
    proc = subprocess.run(
        [sys.executable, HYGIENE_CI] + list(args),
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


def _fixture(name):
    return os.path.join(FIXTURES_ROOT, name)


class FixtureExclusionConstantTests(unittest.TestCase):
    """The exclusion constant is load-bearing and shared by tool,
    workflow, README, and tests."""

    def test_fixture_exclude_glob_value(self):
        self.assertEqual(
            hygiene_ci.FIXTURE_EXCLUDE_GLOB,
            "maintainers/hygiene/fixtures/**",
        )

    def test_fixture_exclude_prefix_value(self):
        self.assertEqual(
            hygiene_ci.FIXTURE_EXCLUDE_PREFIX,
            "maintainers/hygiene/fixtures/",
        )


class CleanScanTests(unittest.TestCase):
    """A clean portal fixture passes every scan."""

    def test_clean_portal_passes(self):
        rc, out, err = _run_cli("scan", _fixture("clean-portal"))
        self.assertEqual(rc, 0, msg="stderr=" + err)
        self.assertIn("scan clean", out)
        self.assertEqual(err, "")


class DirtyScanTests(unittest.TestCase):
    """Each negative fixture fires with the correct citation."""

    def test_private_role_fixture_fails_with_section_7_1_citation(self):
        rc, out, err = _run_cli("scan", _fixture("dirty-private-role"))
        self.assertEqual(rc, 1)
        self.assertIn(
            "CONCEPT-002 plan section 7.1 hard non-export role row", err
        )
        self.assertIn("private role-token", err)

    def test_internal_tooling_fixture_fails_with_section_7_4_citation(self):
        rc, out, err = _run_cli("scan", _fixture("dirty-internal-tooling"))
        self.assertEqual(rc, 1)
        self.assertIn(
            "CONCEPT-002 plan section 7.4 orchestrator row", err
        )

    def test_internal_substrate_fixture_fails_under_allowed_mapping_path(self):
        rc, out, err = _run_cli(
            "scan", _fixture("dirty-internal-substrate")
        )
        self.assertEqual(rc, 1)
        self.assertIn(
            "CONCEPT-002 plan section 7.4 internal authoring substrate row",
            err,
        )
        # The fixture also exercises the path-conditional public
        # vendor row in an allowed path: that row should NOT trip
        # under the mapping prefix.
        self.assertNotIn(
            "public vendor name outside allowed portal paths", err
        )


class VendorPathConditionalTests(unittest.TestCase):
    """The CONCEPT-002 plan section 7.4 public vendor row is allowed
    only under the named portal paths."""

    def test_vendor_allowed_under_mapping_prefix(self):
        rc, out, err = _run_cli(
            "scan", _fixture("vendor-allowed-mapping")
        )
        self.assertEqual(rc, 0, msg="stderr=" + err)
        self.assertIn("scan clean", out)

    def test_vendor_allowed_in_compat_plugin_yaml(self):
        rc, out, err = _run_cli(
            "scan", _fixture("vendor-allowed-compat-yaml")
        )
        self.assertEqual(rc, 0, msg="stderr=" + err)
        self.assertIn("scan clean", out)

    def test_vendor_allowed_in_compat_index_html(self):
        rc, out, err = _run_cli(
            "scan", _fixture("vendor-allowed-compat-index")
        )
        self.assertEqual(rc, 0, msg="stderr=" + err)
        self.assertIn("scan clean", out)

    def test_vendor_disallowed_in_other_mapping(self):
        rc, out, err = _run_cli(
            "scan", _fixture("vendor-disallowed-other-mapping")
        )
        self.assertEqual(rc, 1)
        self.assertIn(
            "CONCEPT-002 plan section 7.4 public vendor path-conditional row",
            err,
        )

    def test_vendor_disallowed_in_other_compat_row(self):
        rc, out, err = _run_cli(
            "scan", _fixture("vendor-disallowed-other-compat")
        )
        self.assertEqual(rc, 1)
        self.assertIn(
            "CONCEPT-002 plan section 7.4 public vendor path-conditional row",
            err,
        )


class PlaceholderAlwaysBlockTests(unittest.TestCase):
    """Every FEATURE-007 plan section 4.1 P-row is always-block."""

    def test_p1_fixture_fails_with_p1_citation(self):
        rc, out, err = _run_cli("scan", _fixture("placeholder-p1"))
        self.assertEqual(rc, 1)
        self.assertIn("FEATURE-007 plan section 4.1 P-1", err)

    def test_p2_fixture_in_markdown_link_fails_with_p2_citation(self):
        rc, out, err = _run_cli("scan", _fixture("placeholder-p2-link"))
        self.assertEqual(rc, 1)
        self.assertIn("FEATURE-007 plan section 4.1 P-2", err)

    def test_p7_fixture_in_yaml_frontmatter_fails_with_p7_citation(self):
        rc, out, err = _run_cli(
            "scan", _fixture("placeholder-p7-frontmatter")
        )
        self.assertEqual(rc, 1)
        self.assertIn("FEATURE-007 plan section 4.1 P-7", err)

    def test_no_placeholders_fixture_passes(self):
        rc, out, err = _run_cli("scan", _fixture("no-placeholders"))
        self.assertEqual(rc, 0, msg="stderr=" + err)
        self.assertIn("scan clean", out)


class RenderCompareTests(unittest.TestCase):
    """Deterministic rebuild integrity check."""

    def test_byte_identical_pair_passes(self):
        rc, out, err = _run_cli(
            "render-compare",
            os.path.join(_fixture("render-pair-clean"), "a"),
            os.path.join(_fixture("render-pair-clean"), "b"),
        )
        self.assertEqual(rc, 0, msg="stderr=" + err)
        self.assertIn("render-compare clean", out)

    def test_divergent_pair_fails_and_names_divergent_file(self):
        rc, out, err = _run_cli(
            "render-compare",
            os.path.join(_fixture("render-pair-divergent"), "a"),
            os.path.join(_fixture("render-pair-divergent"), "b"),
        )
        self.assertEqual(rc, 1)
        self.assertIn("render-compare failed", err)
        self.assertIn("changelog/index.html", err)
        self.assertIn("differs", err)


class FixtureIsolationTests(unittest.TestCase):
    """The production scan excludes maintainers/hygiene/fixtures/**."""

    def test_production_scan_of_staged_tree_is_clean(self):
        # The s-9/ staging root contains both the production hygiene
        # tooling (which must scan clean) and the fixtures (which
        # must be excluded). Walking from the s-9 root verifies the
        # exclusion is wired.
        staging_root = os.path.dirname(
            os.path.dirname(HYGIENE_DIR)
        )  # .../s-9
        rc, out, err = _run_cli("scan", staging_root)
        self.assertEqual(rc, 0, msg="stderr=" + err)
        self.assertIn("scan clean", out)

    def test_include_fixtures_flag_does_surface_negative_fixtures(self):
        staging_root = os.path.dirname(
            os.path.dirname(HYGIENE_DIR)
        )
        rc, out, err = _run_cli(
            "scan", "--include-fixtures", staging_root
        )
        self.assertEqual(rc, 1)
        self.assertIn("portal-bound violations found", err)

    def test_tripwire_neighbor_does_not_taint_explicit_clean_scan(self):
        # Scanning a clean fixture directly succeeds even though a
        # tripwire fixture (carrying every blocked literal) sits in
        # the sibling directory under maintainers/hygiene/fixtures/.
        # If the scanner ever started walking outside its --tree
        # argument it would trip the tripwire and fail this test.
        rc, out, err = _run_cli("scan", _fixture("clean-portal"))
        self.assertEqual(rc, 0, msg="stderr=" + err)


class APITests(unittest.TestCase):
    """In-process scan_tree() + render_compare() shape."""

    def test_scan_tree_returns_violation_tuples(self):
        violations = hygiene_ci.scan_tree(_fixture("dirty-private-role"))
        self.assertTrue(len(violations) >= 1)
        v = violations[0]
        # rel_path, line_no, line_text, match_text, row_id, citation, reason
        self.assertEqual(len(v), 7)
        self.assertIsInstance(v[1], int)
        self.assertTrue(
            v[5].startswith("CONCEPT-002 plan section 7.1")
        )

    def test_scan_tree_clean_returns_empty(self):
        violations = hygiene_ci.scan_tree(_fixture("clean-portal"))
        self.assertEqual(violations, [])

    def test_render_compare_clean_returns_empty(self):
        a = os.path.join(_fixture("render-pair-clean"), "a")
        b = os.path.join(_fixture("render-pair-clean"), "b")
        self.assertEqual(hygiene_ci.render_compare(a, b), [])

    def test_render_compare_divergent_reports_file(self):
        a = os.path.join(_fixture("render-pair-divergent"), "a")
        b = os.path.join(_fixture("render-pair-divergent"), "b")
        diffs = hygiene_ci.render_compare(a, b)
        self.assertTrue(len(diffs) >= 1)
        rels = [d[0] for d in diffs]
        self.assertIn("changelog/index.html", rels)

    def test_path_allowed_helper_honors_prefix_and_files(self):
        prefixes = ("mappings/clawmagic/",)
        files = ("compat/clawmagic-plugin.yaml", "compat/index.html")
        self.assertTrue(
            hygiene_ci._path_allowed_for_row(
                "mappings/clawmagic/index.md", (prefixes, files)
            )
        )
        self.assertTrue(
            hygiene_ci._path_allowed_for_row(
                "compat/clawmagic-plugin.yaml", (prefixes, files)
            )
        )
        self.assertTrue(
            hygiene_ci._path_allowed_for_row(
                "compat/index.html", (prefixes, files)
            )
        )
        self.assertFalse(
            hygiene_ci._path_allowed_for_row(
                "mappings/openapi/index.md", (prefixes, files)
            )
        )
        self.assertFalse(
            hygiene_ci._path_allowed_for_row(
                "compat/other.yaml", (prefixes, files)
            )
        )


class PolicyTableTests(unittest.TestCase):
    """Sanity asserts on the assembled policy table."""

    def test_eight_placeholder_rows_present(self):
        placeholder_rows = [
            row for row in hygiene_ci.POLICY_ROWS if row[0].startswith("P-")
        ]
        ids = sorted(set(row[0] for row in placeholder_rows))
        self.assertEqual(
            ids,
            ["P-1", "P-2", "P-3", "P-4", "P-5", "P-6", "P-7", "P-8"],
        )

    def test_path_conditional_row_is_public_vendor(self):
        path_cond = [
            row for row in hygiene_ci.POLICY_ROWS if row[4] == "path_conditional"
        ]
        self.assertEqual(len(path_cond), 1)
        self.assertEqual(path_cond[0][0], "S74-public-vendor")


if __name__ == "__main__":
    unittest.main()
