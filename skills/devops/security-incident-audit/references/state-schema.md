# Offline helper contract

The Python helper is optional and has no network, provider, credential, shell-execution, or remediation capability. Supply a minimized, already-redacted JSON ledger. It guards common bookkeeping mistakes, not the truth of evidence, hidden scope, every possible secret, or analyst judgment. Keep full raw evidence separately only when necessary and authorized. Do not pass credentials as arguments or fields.

## Schema version 1

Top-level fields:
- `schema`: integer 1.
- `scope`: `revision`, `authorization_revision`, `question`, `target`, `window`, `cutoff` (nonempty text), `authorized` (true), `expected_resources` (unique stable-ID list), `required_streams` (unique names). Define required streams before investigation, not to manufacture green. Include inventory, refs/history, workflows, runs/attempts, access/audit metadata as relevant; explain exclusions in limitations.
- `resources`: one record per provider-qualified stable ID with `id`, readable `label`, `aliases` array, and `streams` object keyed by required stream name. Transfers append aliases, not duplicate records. A list/exact-read mismatch uses `list_exact_mismatch: true`; only set `inventory_reconciled: true` after evidence-backed resolution.
- `evidence`: unique `id`, in-scope `resource`, `source` locator, `observed_at`, and redacted `summary`; add full immutable `sha` where applicable. Additional permitted local ledger detail may include object/attempt ID, collection timestamp, page/query references, source timestamps, artifact digest, and review conclusions. The basic renderer displays only selected fields; preserve a separate complete technical appendix.
- `findings`: unique `id`, `resource`, `kind` (`confirmed_security`, `warning`, `maintenance`, `expected`), plain-language `title`, `what`, `why`, `actor`, `next_step`, `uncertainty` (explicitly say none known if appropriate), nonempty `evidence` ID list bound to that same resource, and `attribution` (`unresolved`, `corroborated`, `owner_confirmed`, `not_relevant`). Expected activity needs corroborated/owner-confirmed attribution and `closure` text. Changes to classification require actual evidence, not merely changing a field.
- `limitations`: list of `{target, reason, evidence: [IDs]}`. Include unavailable/deleted evidence, retention and third-party dependency limits not represented by streams. Every entry makes the overall result at least yellow.

Each stream contains `permission: "readable"` or another outcome, `reviewed` boolean, `truncated` boolean, `evidence` ID list whose records belong to the same resource, and ordered `pages`. Each page contains `cursor` (null for start), `next` (cursor or null), `count` (nonnegative integer), `terminal` boolean, and final `terminal_proof` describing the documented end indicator. Adjacent cursors must join. Empty pages alone are not terminal proof. A stream may instead have `not_applicable: true`, a specific `reason`, and evidence IDs. The helper cannot judge whether that exclusion is justified.

For a stream named `runs`, additionally require `retained_attempts_reconciled: true` only after checking older-created retained runs for incident-window reruns and their attempts. Provider caps/truncated diffs require `truncated: true` until complete source content is obtained and reviewed. Page counters do not prove that a filtered API covers all required history.

Operational checkpoint detail can include next cursor, last completed page, per-repository exact reviewed SHAs, query filters, collection cutoff, overlapping timestamp watermark, and pending tasks. Preserve these fields in the ledger. `save_checkpoint(path, state)` atomically writes sanitized JSON with a scope digest; `load_checkpoint(path, current_scope)` refuses changed scope or authorization and revocation. Current host permissions must also be rechecked outside the helper. This digest detects accidental changes, not malicious tampering; use authorized protected storage.

`reusable_review(previous, candidate)` requires matching path, exact full `base_sha` and `head_sha`, full patch SHA-256 and semantic context SHA-256, no truncation, and an actual prior review/evidence reference. Compute hashes from full bytes and canonical trust/inputs/permissions context. Record exact base/head revisions alongside each review and its reuse mapping. This function does not perform the semantic review or authenticate the supplied hashes.

## Commands

From the skill directory:

```sh
python -B scripts/audit_state.py validate audit-state.json
python -B scripts/audit_state.py report audit-state.json report.html
python -B scripts/test_audit_state.py
```

Exit 0 means valid bookkeeping/report generation, not “safe.” JSON output includes `status`, counts, and gaps. Exit 2 means invalid input or output failure. Reports are self-contained HTML and a `.txt` sibling. Paths must be authorized, non-sensitive output destinations; avoid overwriting an existing report unintentionally. The helper does not upload anything or share files.

The tests provide `fixture()` as a small synthetic input example, and test observable state changes rather than merely matching instruction phrases. Use a separate temporary output directory to avoid committing report/checkpoint artifacts.

## Redaction boundary

The helper replaces common secret-labelled fields, bearer credentials, token/password assignments, familiar token prefixes, and private-key blocks. This is defense in depth, not a general secret scanner. Minimize data before normalization; review all HTML/text/checkpoint outputs before delivery. Avoid sensitive personal metadata unless essential. In particular, unknown secret formats or values embedded without labels may not be detected. Never describe the sanitizer as guaranteeing safe publication.
