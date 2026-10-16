#!/usr/bin/env python3
"""Synthetic behavioral tests; no network, credentials, or real account data."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from audit_state import assess, render, sanitize, save_checkpoint, load_checkpoint, reusable_review


def fixture():
    return {"schema": 2,
        "scope": {"extent": "named_resources", "revision": "scope-v1", "authorization_revision": "grant-v1", "authorized": True,
            "question": "Was the unexpected automation authorized?", "target": "Example workspace",
            "window": "2030-04-01 through 2030-04-02 UTC", "cutoff": "2030-04-03T00:00:00Z",
            "expected_resources": ["provider:repo:101"], "required_streams": ["history", "runs"]},
        "resources": [{"id": "provider:repo:101", "label": "Example project", "aliases": ["sample/project"],
            "streams": {name: {"permission": "readable", "reviewed": True, "truncated": False,
                "pages": [{"cursor": None, "next": None, "count": 1, "terminal": True, "terminal_proof": "Provider reported no next page"}],
                "retained_attempts_reconciled": True, "evidence": ["E1"]} for name in ["history", "runs"]}}],
        "evidence": [{"id": "E1", "resource": "provider:repo:101", "source": "synthetic export row 1", "observed_at": "2030-04-03T00:00:00Z", "summary": "Reviewed complete synthetic history and retained run attempts."}],
        "findings": [], "limitations": []}


def whole_fixture():
    state = fixture()
    state["scope"].update(extent="whole_owners", owners=[{"id": "provider:owner:10", "label": "Synthetic owner"}], target="All owned resources")
    state["resources"][0]["owner"] = "provider:owner:10"
    state["evidence"].append({"id": "D1", "owner": "provider:owner:10", "source": "synthetic authoritative owner export",
                              "observed_at": "2030-04-03T00:00:00Z", "summary": "All-owned grant and complete owner inventory verified."})
    state["discovery"] = [{"owner": "provider:owner:10", "permission": "readable", "grant_extent": "all_owned",
        "authoritative": True, "reviewed": True, "truncated": False, "resource_ids": ["provider:repo:101"],
        "exact_resource_ids": ["provider:repo:101"], "exact_lookups_reconciled": True, "evidence": ["D1"],
        "pages": [{"cursor": None, "next": None, "count": 1, "terminal": True, "terminal_proof": "documented owner endpoint end"}]}]
    return state


def finding(kind="warning", attribution="unresolved"):
    return {"id": "F1", "resource": "provider:repo:101", "kind": kind, "title": "Unexpected automation",
        "what": "An automation restarted during the review period.", "why": "We need to establish whether this was expected.",
        "uncertainty": "We do not yet know who authorized it.", "actor": "You", "next_step": "Confirm whether you requested this exact restart.", "evidence": ["E1"],
        "attribution": attribution, "closure": "The owner confirmed this exact restart and the reviewed behavior matched the import."}


class AuditTests(unittest.TestCase):
    def test_complete_no_findings_is_scoped_green(self):
        state = fixture()
        self.assertEqual(assess(state)["status"], "green")
        html, plain = render(state)
        self.assertIn("No security findings in the checked areas", plain)
        self.assertIn("not a guarantee", plain)
        self.assertNotIn("everything is safe.</h1>", html)

    def test_pagination_requires_contiguous_terminal_pages(self):
        s = fixture(); pages = s["resources"][0]["streams"]["history"]["pages"]
        pages[0].update(next="page2", terminal=False)
        self.assertEqual(assess(s)["status"], "yellow")
        pages.append({"cursor": "page3", "next": None, "count": 0, "terminal": True, "terminal_proof": "documented end"})
        self.assertEqual(assess(s)["status"], "yellow")
        pages[-1]["cursor"] = "page2"
        self.assertEqual(assess(s)["status"], "green")

    def test_transfer_is_one_stable_resource(self):
        s = fixture(); s["resources"][0]["aliases"].append("new-owner/project")
        self.assertEqual(assess(s)["resources"], 1)
        s["resources"].append(copy.deepcopy(s["resources"][0]))
        with self.assertRaises(ValueError): assess(s)

    def test_exact_read_list_mismatch_and_missing_org(self):
        s = fixture(); r = s["resources"][0]; r["list_exact_mismatch"] = True
        self.assertEqual(assess(s)["status"], "yellow")
        r["inventory_reconciled"] = True
        self.assertEqual(assess(s)["status"], "green")
        s["scope"]["expected_resources"].append("provider:repo:102")
        self.assertEqual(assess(s)["status"], "yellow")

    def test_old_run_attempt_cannot_be_skipped(self):
        s = fixture(); stream = s["resources"][0]["streams"]["runs"]
        stream["retained_attempts_reconciled"] = False
        self.assertEqual(assess(s)["status"], "yellow")
        s["evidence"][0]["summary"] = "Old run created before window; attempt 2 restarted in window and was reviewed."
        stream["retained_attempts_reconciled"] = True
        self.assertEqual(assess(s)["status"], "green")

    def test_expected_bot_import_needs_attribution(self):
        s = fixture(); s["findings"] = [finding("expected")]
        with self.assertRaises(ValueError): assess(s)
        s["findings"][0]["attribution"] = "corroborated"
        self.assertEqual(assess(s)["status"], "green")

    def test_owner_confirmation_only_closes_specific_item(self):
        s = fixture(); s["findings"] = [finding()]
        self.assertEqual(assess(s)["status"], "yellow")
        s["findings"][0].update(kind="expected", attribution="owner_confirmed")
        self.assertEqual(assess(s)["status"], "green")
        bad = finding("confirmed_security", "not_relevant"); bad["id"] = "F2"; s["findings"].append(bad)
        self.assertEqual(assess(s)["status"], "red")

    def test_missing_permission_truncation_and_retention_never_green(self):
        for change in ({"permission": "denied"}, {"truncated": True}, {"reviewed": False}):
            s = fixture(); s["resources"][0]["streams"]["history"].update(change)
            self.assertEqual(assess(s)["status"], "yellow")
        s = fixture(); s["limitations"] = [{"target": "Example project", "reason": "Earlier deleted logs were not retained.", "evidence": []}]
        self.assertEqual(assess(s)["status"], "yellow")
        self.assertIn("Could not check", render(s)[1])

    def test_sanitization_and_html_injection(self):
        s = fixture(); s["evidence"][0]["summary"] = '<script>alert(1)</script> token=synthetic-secret'
        s["evidence"][0]["access_token"] = "synthetic-credential"
        html, plain = render(s)
        self.assertNotIn("synthetic-secret", html + plain)
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "checkpoint.json"; save_checkpoint(p, s)
            self.assertNotIn("synthetic-credential", p.read_text())

    def test_checkpoint_resume_changed_scope_and_revocation(self):
        s = fixture()
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "state.json"; save_checkpoint(p, s)
            self.assertEqual(load_checkpoint(p, s["scope"]), s)
            new = dict(s["scope"], revision="scope-v2")
            with self.assertRaises(ValueError): load_checkpoint(p, new)
            new = dict(s["scope"], authorized=False)
            with self.assertRaises(ValueError): load_checkpoint(p, new)
            s["scope"]["authorized"] = False
            with self.assertRaises(ValueError): save_checkpoint(p, s)

    def test_dedup_requires_exact_full_content_context_and_review(self):
        p = {"path": "ci/build.yml", "full_patch_sha256": "a" * 64, "context_sha256": "b" * 64,
             "base_sha": "1" * 40, "head_sha": "2" * 40, "reviewed": True, "review_evidence": "E1", "truncated": False}
        self.assertTrue(reusable_review(p, dict(p)))
        for change in ({"base_sha": "3" * 40}, {"head_sha": "4" * 40}, {"path": "ci/other.yml"}, {"context_sha256": "c" * 64}, {"truncated": True}, {"full_patch_sha256": "d" * 64}):
            self.assertFalse(reusable_review(p, dict(p, **change)))
        self.assertFalse(reusable_review(dict(p, reviewed=False), p))

    def test_support_prompts_and_maintenance_separation(self):
        s = fixture(); s["findings"] = [finding("maintenance", "not_relevant")]
        self.assertEqual(assess(s)["status"], "green")
        html, plain = render(s)
        self.assertIn("not evidence of compromise", plain)
        self.assertIn("Example project", plain)
        self.assertIn("E1", plain)
        self.assertIn("does not authorize", plain)
        self.assertIn("<textarea", html)
        self.assertNotIn("src=", html)

    def test_no_evidence_and_unknown_findings_rejected(self):
        s = fixture(); s["findings"] = [finding()]; s["findings"][0]["evidence"] = ["missing"]
        with self.assertRaises(ValueError): assess(s)
        s = fixture(); s["resources"][0]["streams"]["history"]["evidence"] = []
        self.assertEqual(assess(s)["status"], "yellow")

    def test_cross_resource_evidence_cannot_turn_missing_review_green(self):
        s = fixture(); s["scope"]["expected_resources"].append("provider:repo:102")
        other = copy.deepcopy(s["resources"][0]); other["id"] = "provider:repo:102"; other["label"] = "Other project"
        s["resources"].append(other)
        with self.assertRaisesRegex(ValueError, "different resource"): assess(s)
        other["streams"] = {}
        s["findings"] = [finding()]; s["findings"][0]["resource"] = "provider:repo:102"
        with self.assertRaisesRegex(ValueError, "different resource"): assess(s)

    def test_confirmed_support_prompt_preserves_uncertainty_and_boundary(self):
        s = fixture(); s["findings"] = [finding("confirmed_security", "not_relevant")]
        s["findings"][0]["uncertainty"] = "The uploaded contents were not retained."
        html, plain = render(s)
        self.assertIn("The uploaded contents were not retained.", html)
        self.assertIn("propose a containment plan", plain)
        self.assertIn("do not implement it", plain)
        self.assertIn("F1", plain)
        self.assertIn("Confirm whether you requested", html)

    def test_report_prioritizes_findings_and_green_has_next_step(self):
        s = fixture(); explained = finding("expected", "owner_confirmed"); urgent = finding("confirmed_security", "not_relevant"); urgent["id"] = "F2"
        s["findings"] = [explained, urgent]
        html, plain = render(s)
        self.assertLess(plain.index("RED — Security finding"), plain.index("EXPECTED — Explained activity"))
        self.assertIn("No incident-response action is identified", render(fixture())[1])

    def test_whole_scope_partial_unknown_or_missing_discovery_cannot_green(self):
        for update in ({"grant_extent": "selected"}, {"grant_extent": "unknown"}, {"permission": "denied"},
                       {"authoritative": False}, {"evidence": []}, {"truncated": True}, {"reviewed": False}, {"pages": []}):
            s = whole_fixture(); s["discovery"][0].update(update)
            self.assertEqual(assess(s)["status"], "yellow", update)
        s = whole_fixture(); del s["discovery"]
        self.assertEqual(assess(s)["status"], "yellow")
        self.assertIn("YELLOW", render(s)[1])
        self.assertEqual(assess(whole_fixture())["status"], "green")

    def test_free_text_cannot_expand_named_scope_headline(self):
        s = fixture(); s["scope"]["target"] = "All repositories across every account"
        self.assertEqual(assess(s)["status"], "green")
        report = render(s)[1]
        self.assertIn("Named resources only: Example project", report)
        self.assertNotIn("Scope: All repositories", report)
        self.assertIn("not a whole-account", report)

    def test_owner_discovery_exact_lookup_counts_and_evidence_binding(self):
        for change in ({"exact_resource_ids": ["provider:repo:999"]}, {"exact_lookups_reconciled": False},
                       {"resource_ids": []}, {"resource_ids": ["provider:repo:101", "provider:repo:999"]}):
            s = whole_fixture(); s["discovery"][0].update(change)
            self.assertEqual(assess(s)["status"], "yellow")
        s = whole_fixture(); s["discovery"][0]["evidence"] = ["E1"]
        with self.assertRaisesRegex(ValueError, "same owner"): assess(s)
        s = whole_fixture(); s["resources"][0]["owner"] = "wrong-owner"
        self.assertEqual(assess(s)["status"], "yellow")
        s = whole_fixture(); s["discovery"][0]["pages"][0]["count"] = 0
        self.assertEqual(assess(s)["status"], "yellow")

    def test_multiple_owners_must_each_have_complete_inventory(self):
        s = whole_fixture(); s["scope"]["owners"].append({"id": "provider:owner:20", "label": "Second synthetic owner"})
        self.assertEqual(assess(s)["status"], "yellow")
        s["evidence"].append({"id": "D2", "owner": "provider:owner:20", "source": "synthetic second owner inventory", "observed_at": "2030-04-03T00:00:00Z", "summary": "Authoritative empty inventory."})
        second = copy.deepcopy(s["discovery"][0]); second.update(owner="provider:owner:20", evidence=["D2"], resource_ids=[], exact_resource_ids=[]); second["pages"][0]["count"] = 0
        s["discovery"].append(second)
        self.assertEqual(assess(s)["status"], "green")
        second["evidence"] = ["D1"]
        with self.assertRaisesRegex(ValueError, "same owner"): assess(s)

    def test_empty_authoritative_inventory_and_unavailable_empty_differ(self):
        s = whole_fixture(); s["scope"]["expected_resources"] = []; s["resources"] = []; s["evidence"] = [s["evidence"][1]]
        s["discovery"][0].update(resource_ids=[], exact_resource_ids=[]); s["discovery"][0]["pages"][0]["count"] = 0
        self.assertEqual(assess(s)["status"], "green")
        self.assertIn("does not assess account-level security", render(s)[1])
        s["discovery"][0]["permission"] = "denied"
        self.assertEqual(assess(s)["status"], "yellow")
        s["discovery"] = []
        self.assertEqual(assess(s)["status"], "yellow")

    def test_schema_migration_and_discovery_change_invalidate_resume(self):
        s = fixture(); s["schema"] = 1
        with self.assertRaisesRegex(ValueError, "schema 2"): assess(s)
        s = fixture(); del s["scope"]["extent"]
        with self.assertRaisesRegex(ValueError, "scope extent"): assess(s)
        s = whole_fixture()
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "checkpoint.json"; save_checkpoint(path, s)
            changed = copy.deepcopy(s["scope"]); changed["owners"].append({"id": "provider:owner:20", "label": "New owner"})
            with self.assertRaisesRegex(ValueError, "changed"): load_checkpoint(path, changed)

    def test_owner_inventory_pagination_and_transfers(self):
        s = whole_fixture(); pages = s["discovery"][0]["pages"]
        pages[0].update(next="next", terminal=False)
        self.assertEqual(assess(s)["status"], "yellow")
        pages.append({"cursor": "next", "next": None, "count": 0, "terminal": True, "terminal_proof": "documented end"})
        self.assertEqual(assess(s)["status"], "green")
        s["resources"][0]["aliases"].append("former-owner/project")
        self.assertEqual(assess(s)["status"], "green")
        s["scope"]["owners"].append({"id": "provider:owner:20", "label": "Former owner"})
        s["evidence"].append({"id": "D2", "owner": "provider:owner:20", "source": "old owner export", "observed_at": "2030-04-03T00:00:00Z", "summary": "Unreconciled old resource owner."})
        old = copy.deepcopy(s["discovery"][0]); old.update(owner="provider:owner:20", evidence=["D2"]); s["discovery"].append(old)
        self.assertEqual(assess(s)["status"], "yellow")

if __name__ == "__main__":
    unittest.main(verbosity=2)
