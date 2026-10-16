# Analysis and closure

## Reconstruct a timeline

Correlate observed platform events, push/merge times, execution attempt times, app/key/hook changes, runner activity, and user statements. Distinguish actor (authenticated account performing an action), author/committer (declared Git identity), signer (cryptographic signing identity), bot/app installation, and human operator. Verification of a signature proves only the stated verification property; it does not prove authorization or uncompromised credentials. A current authenticated principal or user login is not proof they authored past events.

Unknown aliases, old author dates, unsigned commits, initial import bursts, and migration-preserved authorship require investigation, not alarm by themselves. Compare immutable content, source/import history, platform actors, signing metadata, and expected automation. Ask the owner about a precisely described event with time, repository, action, and evidence. Record their response as attribution evidence; it closes only that question, not independent harmful code or unexplained access. Keep contradictory evidence visible. Never attribute malicious intent from a name alone.

## Trace source to sink without execution

For each relevant historical and current workflow, trace entry event and trust boundary → permissions/secrets/OIDC/cloud access → checked-out revision → local/composite/reusable actions and invoked scripts → dependencies → commands/network/upload destinations. Check untrusted PR input, expression/command injection, privileged workflow events, write tokens, environment bypass, mutable action/container references, download-and-execute patterns, encoded payloads, credential collection, persistence, and runner reuse. Follow local paths at the exact executed SHA, not today's branch. Reusable external actions and dynamically fetched code need their resolved immutable revision where available; uninspectable transitive dependencies remain explicit limits.

A network command is not automatically exfiltration. Determine data source, reachability, privileges available to that particular event/attempt, destination ownership, intended purpose, execution evidence, and whether sensitive content could leave the boundary. Separate capability to expose, evidence of execution, and verified disclosure. Never probe a suspicious destination or replay a payload. Logs may not show encrypted/dynamic flows; absence is not proof. A confirmed unauthorized change can be a security finding even if actual theft is unproven.

## Review reuse

Use duplicate elimination for exact records by stable IDs. For content reviews require same normalized repository-relative path, full byte-for-byte patch/blob hashes, exact base/head revisions, equivalent execution/trust/secret context, and a reference to an actual completed semantic review. An identical script with different permissions or invoked inputs needs contextual review. Filename-only, title-only, short hash, truncated diff, or mere hash-computation are never proof of a completed review. Record all affected revisions/resources even when content review is reused.

## Findings and completion

Classify each observation:
- Confirmed security finding: evidence demonstrates unauthorized or harmful change/activity; say what is and is not established.
- Warning: suspicious or unresolved attribution, plausible exposure without execution proof, or material evidence gap.
- Maintenance: generic hardening or quality issue without compromise evidence; keep separate from incident findings.
- Expected activity: corroborated bot/import/user activity; explain briefly and close that scoped concern.

Use confirmed findings to prioritize urgent, minimal next steps. Do not mutate settings, revoke access, rotate secrets, delete objects, stop jobs, or send third-party notices merely because the audit recommends it. Explain impact and obtain required authorization. Preserve evidence before any separately authorized remediation.

Finish when all authorized in-scope streams have terminal/review evidence or an explicit reason they cannot be completed; meaningful hypotheses have findings or bounded uncertainty; owner attribution is resolved or clearly pending; and reports give actionable next steps. Completion of the audit is not proof that every historical event was recoverable or that all third-party dependencies were safe. If more evidence requires the user, deliver current results and the smallest access/export/confirmation request rather than silently waiting forever.
