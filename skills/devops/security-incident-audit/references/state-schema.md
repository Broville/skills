# Offline helper contract

The Python helper is optional and has no network, provider, credential, shell-execution, or remediation capability. Supply a minimized, already-redacted JSON ledger. It guards common bookkeeping mistakes, not the truth of evidence, hidden scope, every possible secret, or analyst judgment. Keep full raw evidence separately only when necessary and authorized. Do not pass credentials as arguments or fields.

## Schema version 2

Top-level fields:
- `schema`: integer 2. Version 1 is rejected rather than silently treated as bounded or complete.
- `scope`: `revision`, `authorization_revision`, `question`, `target`, `window`, `cutoff` (nonempty text), `authorized` (true), `extent` (`named_resources` or `whole_owners`), `expected_resources` (unique stable-ID list), `required_streams` (unique names). For named resources, expected IDs must be nonempty and no whole-owner list is allowed. For whole owners, `owners` must list explicitly authorized `{id, label}` records; expected IDs may be empty only with the discovery outcome exposed. Define required streams before investigation, not to manufacture green. Include inventory, refs/history, workflows, runs/attempts, access/audit metadata as relevant; explain exclusions in limitations.
- `resources`: one record per provider-qualified stable ID with `id`, readable `label`, `aliases` array, and `streams` object keyed by required stream name. Whole-owner records also require `owner` matching the authoritative current inventory. Transfers append aliases, not duplicate records. A list/exact-read mismatch uses `list_exact_mismatch: true`; only set `inventory_reconciled: true` after evidence-backed resolution.
- `evidence`: unique `id`, exactly one in-scope `resource` or `owner`, `source` locator, `observed_at`, and redacted `summary`; add full immutable `sha` where applicable. Additional permitted local ledger detail may include object/attempt ID, collection timestamp, page/query references, source timestamps, artifact digest, and review conclusions. The basic renderer displays only selected fields; preserve a separate complete technical appendix.
- `findings`: unique `id`, `resource`, `kind` (`confirmed_security`, `warning`, `maintenance`, `expected`), plain-language `title`, `what`, `why`, `actor`, `next_step`, `uncertainty` (explicitly say none known if appropriate), nonempty `evidence` ID list bound to that same resource, and `attribution` (`unresolved`, `corroborated`, `owner_confirmed`, `not_relevant`). Expected activity needs corroborated/owner-confirmed attribution and `closure` text. Changes to classification require actual evidence, not merely changing a field.
- `limitations`: list of `{target, reason, evidence: [IDs]}`. Include unavailable/deleted evidence, retention and third-party dependency limits not represented by streams. Every entry makes the overall result at least yellow.

Each stream contains `permission: "readable"` or another outcome, `reviewed` boolean, `truncated` boolean, `evidence` ID list whose records belong to the same resource, and ordered `pages`. Each page contains `cursor` (null for start), `next` (cursor or null), `count` (nonnegative integer), `terminal` boolean, and final `terminal_proof` describing the documented end indicator. Adjacent cursors must join. Empty pages alone are not terminal proof. A stream may instead have `not_applicable: true`, a specific `reason`, and evidence IDs. The helper cannot judge whether that exclusion is justified.

For a stream named `runs`, additionally require `retained_attempts_reconciled: true` only after checking older-created retained runs for incident-window reruns and their attempts. Provider caps/truncated diffs require `truncated: true` until complete source content is obtained and reviewed. Page counters do not prove that a filtered API covers all required history.

Operational checkpoint detail can include next cursor, last completed page, per-repository exact reviewed SHAs, query filters, collection cutoff, overlapping timestamp watermark, and pending tasks. Preserve these fields in the ledger. `save_checkpoint(path, state)` atomically writes sanitized JSON with a scope digest; `load_checkpoint(path, current_scope)` refuses changed scope or authorization and revocation. Current host permissions must also be rechecked outside the helper. This digest detects accidental changes, not malicious tampering; use authorized protected storage.

`reusable_review(previous, candidate)` requires matching path, exact full `base_sha` and `head_sha`, full patch SHA-256 and semantic context SHA-256, no truncation, and an actual prior review/evidence reference. Compute hashes from full bytes and canonical trust/inputs/permissions context. Record exact base/head revisions alongside each review and its reuse mapping. This function does not perform the semantic review or authenticate the supplied hashes.


## Whole-owner discovery is separate from repository pagination

A connector can finish every page while seeing only selected resources. That does not establish a whole-account/organization inventory. Never infer completeness from terminal pages alone, a successful exact read, current account identity, or access to one repository. The renderer derives its scope line from `extent` and IDs/labels, not the free-text `target`: a named-resource ledger cannot display a whole-account claim.

For `whole_owners`, top-level `discovery` contains one record per authorized owner:
- `owner`: matching stable owner ID.
- `permission`: `readable` only after testing access.
- `grant_extent`: `all_owned` only when authoritative metadata proves this source covers all owned resources for the requested resource inventory, including private/archived resources as applicable. Use `selected`, `partial`, or `unknown` otherwise. Never expand credentials to obtain green.
- `authoritative`: true only when the owner-inventory source is appropriate and grant coverage is established; `reviewed`: true only after review; `truncated`: false only when no cap/cutoff remains.
- `pages`: the same contiguous cursor/terminal-proof records as streams. Their item counts must reconcile with the unique inventory IDs; unresolved duplicates or changing snapshots stay yellow.
- `resource_ids`: unique stable IDs returned by owner inventory at the fixed cutoff.
- `exact_resource_ids`: known current in-scope IDs found by exact lookup or independent sources; `exact_lookups_reconciled`: true only after reconciling them. Every exact ID must be present in the authoritative inventory; a mismatch remains yellow until resolved rather than toggled away.
- `evidence`: nonempty IDs of evidence records bound to this owner, establishing source authority, grant coverage, and inventory completion. Evidence about a single repository cannot substitute.

Missing/partial/unknown access, missing owners, nonterminal pages, truncation, missing evidence, count mismatches, or exact-lookup discrepancies produce yellow even when every visible repository stream is reviewed. The union of owner inventories must equal `expected_resources`, and current ownership must reconcile. A transfer can retain aliases but cannot count as currently owned by two owners. Resolve missing identities by updating the authorized scope revision and ledger, not dropping them.

An authoritative empty inventory can be green only for the empty owned-resource inventory. The report explicitly says there were no owned resources to review and this does not assess account-level security. An empty denied/unknown inventory is yellow. Account access/security metadata needs its own authorized resource/streams; empty repository enumeration never clears the account itself. Owner lists are explicit authorized scope, not proof that every organization related to a user was discovered. If the user's intent includes discovering all their organizations, collect authoritative owner-list evidence too and retain a limitation until that owner set is reconciled.

### Migrating old checkpoints

Do not change `schema: 1` to 2 alone or default every old ledger to named resources. Re-read the original authorized request, establish the actual extent, identify owners or exact named resources, and collect missing discovery evidence. Bump scope revision; old scope digests must not be reused. If intent or grant completeness is unknown, stop the affected conclusion and request the smallest missing decision/evidence. Existing reviewed repository evidence can remain, but cannot create whole-owner completeness. No English keyword matching is used to guess scope.

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
