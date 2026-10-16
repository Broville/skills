# Intake and autonomy

Gather or infer from explicit context, then confirm only unresolved material choices:

- What prompted concern and what decision should this audit support?
- Which accounts/owners, organizations, exact repositories, external integrations, and incident interval are authorized? Identify personal ownership, owned organization resources, and collaborator-only resources separately. Membership is not ownership or authority to inspect other people's data.
- What timezone describes the incident? Store original timestamps and normalized UTC, including offset ambiguity. Choose and record a fixed observation cutoff.
- Which people, bots, migration/import jobs, scheduled automation, and legitimate devices are expected? Unknown is allowed; do not block all work awaiting an exhaustive list.
- Which existing connectors/API sessions, exports, or browser environments may be used? Does local computer control need separate permission? What metadata/log access is missing?
- Who can receive outputs, where may private evidence be stored, and what retention/deletion policy applies? Default to private user delivery and minimum redacted evidence, not public uploads.
- Is this read-only? Default yes. Record any narrowly authorized remediation separately; credentials, access changes, external messages, deletion, purchases, and running code still follow platform and user approval rules.

Maintain a compact scope record with a revision, authorization revision, source of authorization, included/excluded resource IDs, incident bounds, observation cutoff, permitted environments, and output destinations. An extra accessible organization is a discovery candidate, not automatically authorized scope. Ask once if adding it materially changes scope. Use symbolic labels in public examples.

Autonomous execution means choosing safe order, paginating, inspecting immutable content, correlating, retrying transient read failures after checking their nature, and finishing deliverables without asking the same questions again. It does not mean claiming new permissions. Distinguish unsupported capability, missing permission, explicitly denied action, and uncertain operation outcome. Do not retry denial through another route. For uncertain mutations, verify state first; this audit normally performs none.

Use two concurrent evidence requests by default; increase to four only when provider limits and host capacity allow. Honor Retry-After/reset headers, reduce concurrency on throttling, and checkpoint before waiting. Retry transient idempotent reads at most three times with bounded backoff; thereafter record the gap and continue other work. Do not run endless scans or silently widen the time window. Explain a newly necessary scope expansion before doing it.

Checkpoint safely after each complete page and repository. Store next cursor, terminal-page proof, resource/version IDs, reviewed exact SHAs, dedup references, gaps, and completed tasks. Use atomic replacement in an authorized output directory. On resume compare scope revision, authorization revision, cutoff, and current permission availability. Revalidate moving refs and newly changed data with overlap; do not reuse a watermark after a force push, transfer, or changed query without reconciliation. Authorization revocation stops affected collection immediately; retain/dispose existing evidence only as permitted.
