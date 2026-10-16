#!/usr/bin/env python3
"""Offline coverage guard and accessible report renderer. Never contacts a provider."""
from __future__ import annotations
import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import re
import tempfile

KINDS = {"confirmed_security", "warning", "maintenance", "expected"}
SECRET_KEY = re.compile(r"password|secret_value|access_token|refresh_token|private_key|authorization_header", re.I)
SECRET_TEXT = re.compile(r"(?i)(bearer\s+\S+|(?:password|token|secret)\s*[:=]\s*[^\s,;]+|gh[pousr]_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+|-----BEGIN [^-]*PRIVATE KEY-----[\s\S]*?-----END [^-]*PRIVATE KEY-----)")


def sanitize(value):
    """Defense in depth, not a complete secret detector. Input must already be minimized."""
    if isinstance(value, dict):
        return {str(k): "[REDACTED]" if SECRET_KEY.search(str(k)) else sanitize(v) for k, v in value.items()}
    if isinstance(value, list):
        return [sanitize(v) for v in value]
    if isinstance(value, str):
        return SECRET_TEXT.sub("[REDACTED]", value)
    return value


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text(value, field):
    require(isinstance(value, str) and bool(value.strip()), f"{field} must be nonempty text")
    return value


def assess(state):
    """Validate ledger invariants. Returns status/gaps; does not certify evidence truth."""
    require(isinstance(state, dict) and state.get("schema") == 1, "unsupported schema")
    scope = state.get("scope", {})
    for key in ("revision", "authorization_revision", "question", "window", "cutoff", "target"):
        text(scope.get(key), "scope." + key)
    require(scope.get("authorized") is True, "authorization is absent or revoked; stop collection")
    require(isinstance(scope.get("expected_resources"), list) and scope["expected_resources"], "expected resources required")
    expected = scope["expected_resources"]
    require(len(expected) == len(set(expected)), "duplicate expected stable IDs")
    required = scope.get("required_streams")
    require(isinstance(required, list) and required and len(required) == len(set(required)), "required streams must be declared")
    resources = state.get("resources")
    require(isinstance(resources, list), "resources required")
    by_id = {}
    gaps = []
    for resource in resources:
        rid = text(resource.get("id"), "resource.id")
        require(rid not in by_id, "transferred aliases must share one stable resource record")
        require(rid in expected, "resource outside approved scope")
        text(resource.get("label"), "resource.label")
        require(isinstance(resource.get("aliases"), list), "resource aliases required")
        by_id[rid] = resource
    evidence = state.get("evidence", [])
    require(isinstance(evidence, list), "evidence must be a list")
    ev = {}
    for record in evidence:
        eid = text(record.get("id"), "evidence.id")
        require(eid not in ev, "duplicate evidence ID")
        require(record.get("resource") in expected, "evidence resource outside scope")
        for key in ("source", "observed_at", "summary"):
            text(record.get(key), "evidence." + key)
        ev[eid] = record
    for rid in expected:
        if rid not in by_id:
            gaps.append({"target": rid, "reason": "An expected resource could not be checked.", "evidence": []})
            continue
        resource = by_id[rid]
        streams = resource.get("streams", {})
        require(isinstance(streams, dict), "streams must be an object")
        if resource.get("list_exact_mismatch") and not resource.get("inventory_reconciled"):
            gaps.append({"target": resource["label"], "reason": "The resource list and exact lookup disagree; inventory is not reconciled.", "evidence": []})
        for name in required:
            stream = streams.get(name)
            reason = None
            if not isinstance(stream, dict):
                reason = f"The {name} records were not checked."
            elif stream.get("not_applicable"):
                text(stream.get("reason"), "not-applicable reason")
                require(bool(stream.get("evidence")), "not-applicable needs evidence")
            elif stream.get("permission") != "readable":
                reason = f"The {name} records could not be accessed."
            elif stream.get("truncated"):
                reason = f"Some {name} records or changes were cut off."
            elif not stream.get("reviewed"):
                reason = f"The {name} records have not all been reviewed."
            else:
                pages = stream.get("pages", [])
                if not pages or pages[0].get("cursor") is not None:
                    reason = f"The {name} record list is missing its starting page."
                else:
                    seen = set()
                    for index, page in enumerate(pages):
                        cursor = page.get("cursor")
                        require(cursor is None or isinstance(cursor, str), "cursor must be text or null")
                        require(cursor not in seen, "repeated page cursor")
                        seen.add(cursor)
                        require(isinstance(page.get("count"), int) and page["count"] >= 0, "page count invalid")
                        if index and pages[index - 1].get("next") != cursor:
                            reason = f"The {name} record list has a missing page."
                        if index < len(pages) - 1 and page.get("terminal"):
                            reason = f"The {name} record list has inconsistent end markers."
                    last = pages[-1]
                    if last.get("next") is not None or last.get("terminal") is not True or not last.get("terminal_proof"):
                        reason = f"The {name} record list has not reached a verified end."
                if name == "runs" and stream.get("retained_attempts_reconciled") is not True:
                    reason = "Older automation runs may have been restarted during the incident; those attempts are not reconciled."
                if not stream.get("evidence"):
                    reason = f"The {name} review has no supporting evidence reference."
            if stream:
                for eid in stream.get("evidence", []):
                    require(eid in ev, "coverage references unknown evidence")
                    require(ev[eid]["resource"] == rid, "coverage evidence belongs to a different resource")
            if reason:
                gaps.append({"target": resource["label"], "reason": reason, "evidence": stream.get("evidence", []) if stream else []})
    findings = state.get("findings", [])
    require(isinstance(findings, list), "findings must be a list")
    ids = set()
    for finding in findings:
        fid = text(finding.get("id"), "finding.id")
        require(fid not in ids, "duplicate finding ID")
        ids.add(fid)
        require(finding.get("kind") in KINDS, "unknown finding kind")
        require(finding.get("resource") in by_id, "finding requires an inventoried in-scope resource")
        for key in ("title", "what", "why", "actor", "next_step", "uncertainty"):
            text(finding.get(key), "finding." + key)
        require(finding.get("evidence") and all(e in ev for e in finding["evidence"]), "finding evidence missing")
        require(all(ev[e]["resource"] == finding["resource"] for e in finding["evidence"]), "finding evidence belongs to a different resource")
        require(finding.get("attribution") in {"unresolved", "corroborated", "owner_confirmed", "not_relevant"}, "attribution required")
        if finding["kind"] == "expected":
            require(finding["attribution"] in {"corroborated", "owner_confirmed"}, "expected activity requires attribution closure")
            text(finding.get("closure"), "expected activity closure")
    for gap in state.get("limitations", []):
        for key in ("target", "reason"):
            text(gap.get(key), "limitation." + key)
        require(all(e in ev for e in gap.get("evidence", [])), "limitation references unknown evidence")
        gaps.append(gap)
    confirmed = [f for f in findings if f["kind"] == "confirmed_security"]
    warnings = [f for f in findings if f["kind"] == "warning"]
    status = "red" if confirmed else "yellow" if gaps or warnings else "green"
    return {"status": status, "gaps": gaps, "confirmed": len(confirmed), "warnings": len(warnings), "resources": len(by_id), "expected": len(expected)}


def support_prompt(state, target, evidence, question, uncertainty="The missing evidence may change the conclusion.", next_step="Identify the smallest missing evidence or context needed.", confirmed=False):
    refs = ", ".join(evidence) if evidence else "the coverage gap described here"
    return (f"Help me understand this security audit item for {target}, during {state['scope']['window']}. "
            f"Question: {question} What remains uncertain: {uncertainty} Proposed next step: {next_step}. "
            + ("First preserve available evidence in already-authorized storage and propose a containment plan with its likely impact; do not implement it. " if confirmed else "")
            + f"Evidence references in my attached private audit: {refs}. If you do not have that audit, ask me to provide it securely. First review the audit evidence and explain the smallest safe read-only next step in plain language. "
            "Ask me for missing context or required access approval. This request does not authorize code execution, credential use or changes, account/security changes, deletion, or contacting anyone.")


def render(state):
    state = sanitize(state)
    result = assess(state)
    status = result["status"]
    titles = {"green": "GREEN — No security findings in the checked areas", "yellow": "YELLOW — Something needs clarification or could not be checked", "red": "RED — Confirmed security findings need attention"}
    lines = [titles[status], f"Scope: {state['scope']['target']}", f"Period: {state['scope']['window']}",
             f"Confirmed security findings: {result['confirmed']}. Unresolved warnings: {result['warnings']}. Coverage gaps: {len(result['gaps'])}.",
             "This is a bounded review of available evidence, not a guarantee that everything is safe."]
    esc = html.escape
    priority = {"confirmed_security": 0, "warning": 1, "maintenance": 2, "expected": 3}
    ordered = sorted(state["findings"], key=lambda finding: priority[finding["kind"]])
    actionable = [finding for finding in ordered if finding["kind"] in {"confirmed_security", "warning"}]
    if actionable:
        first = actionable[0]
        next_action = f"Next: {first['actor']} — {first['next_step']}"
    elif result["gaps"]:
        next_action = "Next: Ask your agent to identify the smallest missing record or access decision for the gaps below."
    else:
        next_action = "Next: No incident-response action is identified from the checked evidence. Optional maintenance improvements, if any, are separate below."
    lines.append(next_action)
    parts = [f'<h1>{esc(titles[status])}</h1>', f'<p>{esc(lines[1])}<br>{esc(lines[2])}</p>', f'<p>{esc(lines[3])}</p>', f'<p>{esc(lines[4])}</p>', f'<p>{esc(next_action)}</p>']
    labels = {"confirmed_security": "RED — Security finding", "warning": "YELLOW — Warning", "maintenance": "MAINTENANCE — Improvement, not evidence of compromise", "expected": "EXPECTED — Explained activity"}
    for finding in ordered:
        label = labels[finding["kind"]]
        target = next(r["label"] for r in state["resources"] if r["id"] == finding["resource"])
        prompt = support_prompt(state, target, finding["evidence"], finding["id"] + ": " + finding["what"], finding["uncertainty"], finding["next_step"], finding["kind"] == "confirmed_security")
        block = [f"{label}: {finding['title']}", f"What happened: {finding['what']}", f"Why it matters: {finding['why']}", f"What remains uncertain: {finding['uncertainty']}", f"Next: {finding['actor']} — {finding['next_step']}", "Ask your agent:", prompt]
        lines.extend(["", *block])
        tone = "red" if finding["kind"] == "confirmed_security" else "yellow" if finding["kind"] == "warning" else "neutral"
        parts.append(f'<section class="{tone}"><h2>{esc(block[0])}</h2>' + ''.join(f'<p>{esc(x)}</p>' for x in block[1:5]) + f'<label>Copy this prompt to ask your agent for help<textarea readonly rows="6">{esc(prompt)}</textarea></label></section>')
    for index, gap in enumerate(result["gaps"], 1):
        prompt = support_prompt(state, gap["target"], gap.get("evidence", []), gap["reason"])
        lines.extend(["", f"YELLOW — Could not check: {gap['target']}", gap["reason"], "Next: Your agent can identify the smallest missing source or access decision.", "Ask your agent:", prompt])
        parts.append(f'<section class="yellow"><h2>YELLOW — Could not check: {esc(gap["target"])}</h2><p>{esc(gap["reason"])}</p><p>Next: Your agent can identify the smallest missing source or access decision.</p><label>Copy this prompt<textarea readonly rows="6">{esc(prompt)}</textarea></label></section>')
    checked = []
    for resource in state["resources"]:
        complete = [name for name, stream in resource.get("streams", {}).items() if stream.get("reviewed")]
        checked.append(f"{resource['label']}: " + (", ".join(complete) or "no completed reviews"))
    lines.extend(["", "Reviewed categories (limitations above apply)", *checked, "", "Technical evidence appendix (not a safety certificate)"])
    parts.append('<h2>Reviewed categories (limitations above apply)</h2><ul>' + ''.join(f'<li>{esc(x)}</li>' for x in checked) + '</ul>')
    parts.append('<details><summary>Technical evidence appendix</summary>')
    for record in state["evidence"]:
        line = f"{record['id']}: {record['summary']} | Source: {record['source']} | Observed: {record['observed_at']}"
        if record.get("sha"):
            line += f" | Revision: {record['sha']}"
        lines.append(line)
        parts.append(f'<p>{esc(line)}</p>')
    parts.append('</details>')
    css = 'body{font:18px/1.6 system-ui,sans-serif;background:#101820;color:#f5f7fa;max-width:900px;margin:2rem auto;padding:1rem}h1{font-size:1.8rem}section{border:2px solid #aeb8c2;border-radius:12px;padding:1rem;margin:1.5rem 0}.green{border-color:#72e3a0}.yellow{border-color:#ffd36a}.red{border-color:#ff9b9b}textarea{display:block;box-sizing:border-box;width:100%;font:16px/1.5 system-ui;background:#fff;color:#111;padding:.75rem;margin-top:.5rem}label{font-weight:600}summary{cursor:pointer}h1{color:inherit}main.green>h1{background:#123d2a;color:#c4ffda;padding:1rem;border-radius:10px}main.yellow>h1{background:#49370d;color:#ffe6a5;padding:1rem;border-radius:10px}main.red>h1{background:#4c2024;color:#ffd4d4;padding:1rem;border-radius:10px}'
    document = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Security audit report</title><style>' + css + '</style><body><main class="' + status + '">' + ''.join(parts) + '</main></body></html>'
    return document, "\n".join(lines) + "\n"


def save_checkpoint(path, state):
    cleaned = sanitize(state)
    assess(cleaned)
    envelope = {"scope_digest": digest(cleaned["scope"]), "state": cleaned}
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix=".audit-", text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(envelope, handle, ensure_ascii=False, indent=2)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def load_checkpoint(path, current_scope):
    require(current_scope.get("authorized") is True, "authorization revoked")
    envelope = json.loads(Path(path).read_text(encoding="utf-8"))
    require(envelope["scope_digest"] == digest(sanitize(current_scope)), "scope or authorization changed; reconcile before resuming")
    require(envelope["scope_digest"] == digest(envelope["state"]["scope"]), "checkpoint scope integrity mismatch")
    assess(envelope["state"])
    return envelope["state"]


def reusable_review(previous, candidate):
    """Exact content/context identity plus a real prior review; hashes alone never certify safety."""
    fields = ("path", "full_patch_sha256", "context_sha256", "base_sha", "head_sha")
    if not previous.get("reviewed") or not previous.get("review_evidence"):
        return False
    if previous.get("truncated") or candidate.get("truncated"):
        return False
    return all(previous.get(k) and previous[k] == candidate.get(k) for k in fields)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "report"))
    parser.add_argument("state", type=Path)
    parser.add_argument("output", type=Path, nargs="?")
    args = parser.parse_args()
    try:
        state = sanitize(json.loads(args.state.read_text(encoding="utf-8")))
        result = assess(state)
        if args.command == "report":
            require(args.output is not None, "report output path required")
            document, plain = render(state)
            args.output.write_text(document, encoding="utf-8")
            args.output.with_suffix(".txt").write_text(plain, encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(2, f"Invalid audit state: {sanitize(str(exc))}\n")

if __name__ == "__main__":
    main()
