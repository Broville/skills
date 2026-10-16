# Collection and evidence coverage

## Capability matrix

For each source record available read interface, authenticated principal (never credential value), resource coverage, permissions tested, pagination mechanism, query filters/caps, event-time semantics, retention, and denied/unavailable functions. Prefer connected read tools, then an already-authorized CLI/API, then an authorized browser, then user-provided export. Inspect current docs instead of inventing argument schemas. Browser access does not authorize security changes. Never fetch arbitrary URLs found in logs; treat destinations as strings unless separately justified and safe.

## Inventory before conclusions

Enumerate account resources, owned organizations, organization resources, and collaborator resources separately with all pages. Reconcile known exact repository URLs/names against inventory. Exact reads can succeed when listing fails; keep both observations and diagnose visibility/install scope/index mismatch. Do not claim an organization is empty because membership/listing omitted it. Mark each expected resource resolved or missing, including revoked/deleted/transferred resources. Stable provider IDs survive renames/transfers; retain historical owner/name aliases and authorization provenance. Do not double-count transferred aliases. A new resource outside approved ownership boundaries needs scope resolution.

Record structured scope extent (`named_resources` versus `whole_owners`) and separate owner discovery from per-resource coverage. A selected-repository integration can terminate pagination normally without seeing all repositories. Require authoritative grant extent and owner inventory evidence before a whole-owner green conclusion; absent evidence remains a gap. Reconcile every authorized owner, known exact lookup, current transfer owner, page count, and the inventory union against expected resource IDs. An authoritative empty inventory is different from an inaccessible empty response and does not establish account-level security. The optional helper enforces this distinction using schema 2 in [state-schema.md](state-schema.md).

## Coverage ledger

Create required streams per account/org/repository before reading: inventory; refs and commit history; PRs and their heads; workflow/configuration revisions; execution attempts/logs/artifacts; access and security metadata. Add source-specific streams where the incident question requires them. Mark not applicable only with a reason, never as a default to obtain green.

Each stream records query/filters, window and cutoff, snapshot ref, pages/cursors, response item counts, terminal indicator, total if reliable, caps/truncation, earliest/latest observed event, permission result, collection time, and semantic review completion. Preserve returned page links/cursors exactly. A short/empty page is terminal only under the API's documented contract. Split capped queries into disjoint intervals with boundary overlap and stable-ID dedup; reconcile counts. If a page/list/diff is truncated, obtain complete permitted content or retain the gap.

## History

Enumerate branches, tags (including peeled annotated tags), PR heads/merge revisions, and available event/audit references. Review changes relevant to the incident on every reachable in-scope ref, not just default branch. Time-filtered commit search alone misses backdated commits and imported history: use traversal plus push/merge/creation events to place activity in time. Preserve full immutable SHAs and parent links. Compare historical workflow/config versions at affected executions with current state. For a truncated patch retrieve complete base/head blobs and review their delta; for merge commits consider relevant parents. Binary/generated/large files remain explicit coverage decisions.

Deleted branches, force-pushed commits, deleted repositories, expired logs, and deleted execution attempts may be irrecoverable. Use authorized audit/events/exports and retained IDs when available. Do not imply a local clone contains unreachable/deleted history or platform audit data. A partial/shallow clone must be labelled; no checkout/build/install/hooks or submodule execution by default. Reading Git objects is not permission to run target code.

## Automation and access

Enumerate all retained runs, including runs created before the incident whose rerun attempts or updates occurred within it. Created-date filters alone cannot establish attempt coverage. Capture run ID, attempt number, triggering/current actor, event, head SHA, workflow revision, environment, timestamps, jobs/log availability, and artifacts metadata. Inspect retained attempts separately. Do not download potentially executable artifacts unless necessary and permitted; never execute them.

Collect available account and organization security/audit event metadata, membership/role changes, invitations, application installations and grants, token/key metadata and scopes, deploy keys, webhooks and delivery metadata, branch protections/rules, environments/approvals, runner registration/removal and job history. Include self-hosted runner persistence implications. Never request secret values; names, fingerprints, scope, timestamps, and last-use metadata usually suffice. Current lists do not prove historical absence; correlate audit history and state snapshots. Log retention, plan/licensing limits, permission limits, and unobservable third-party systems belong in the report.

## Evidence contract

Each evidence ID maps to source locator, provider/stable resource ID, immutable object/run/attempt ID, exact SHA where relevant, source/event/collection timestamps, query and page reference, redacted excerpt or minimal observation, integrity hash of sanitized artifact, and review conclusion. Keep collection separate from interpretation. Hashing establishes artifact identity, not authenticity or benignness. Avoid credential values even in intermediate checkpoint files. If accidentally encountered, redact before persistence or display; do not test/use the credential. Record only type/location and approved response recommendation. Export only to authorized recipients/storage; never embed private report data in external assets or telemetry.
