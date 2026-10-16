# Optional GitHub read adapter

This is a mapping guide, not a dependency on GitHub or a grant of access. Use the host's documented connected tools first. For other providers map the same evidence categories to equivalent APIs and explicitly record unsupported history. Verify current endpoint permissions/limits before use; API versions and retention can change.

For an already installed, authorized GitHub CLI session, these are read-only examples. Substitute only verified in-scope owner/repository names. Do not print authentication tokens or change login permissions to make a command work.

```sh
gh api --paginate --slurp 'user/repos?affiliation=owner,organization_member,collaborator&per_page=100'
gh api --paginate --slurp 'user/orgs?per_page=100'
gh api 'repos/OWNER/REPOSITORY'
gh api --paginate --slurp 'orgs/ORGANIZATION/repos?per_page=100&type=all'
gh api --paginate --slurp 'repos/OWNER/REPOSITORY/branches?per_page=100'
gh api --paginate --slurp 'repos/OWNER/REPOSITORY/tags?per_page=100'
gh api --paginate --slurp 'repos/OWNER/REPOSITORY/pulls?state=all&per_page=100'
gh api --paginate --slurp 'repos/OWNER/REPOSITORY/actions/runs?per_page=100'
gh api 'repos/OWNER/REPOSITORY/actions/runs/RUN_ID/attempts/ATTEMPT_NUMBER'
```

Expected output is JSON records or a documented access error. Save only necessary redacted evidence, not a blind dump of logs or credentials. `--paginate` does not defeat search caps or establish semantic review. If the connector omits pagination headers, obtain its continuation contract; otherwise record incomplete enumeration. Preserve GitHub numeric/node IDs and historical names for transferred repositories. Installation-scoped discovery can omit an accessible exact repository; reconcile both.

Run lists filtered by actor, branch, check suite, created date, event, head SHA, or status may be capped at 1,000 per search. Follow all pages and reconcile caps using permitted partitioning. Critically, `created` filters run creation, not every later attempt. Enumerate retained runs beyond the incident creation interval and inspect run attempts, update/start times, actor and triggering actor; do not stop solely when creation dates become old. Missing earlier attempts/logs remain limitations.

Read workflow files at actual execution revisions, and separate PR head/merge refs from privileged base workflow contexts. Trace reusable workflows, local actions, invoked scripts, token permissions, environment secrets, and OIDC grants. API commit verification metadata supplements but does not replace actor/audit attribution. Current user identity from `user` is not the actor for historical commits.

With already authorized access, inspect organization audit logs, personal security history exports/UI, app installations/grants, deploy and SSH key metadata, webhooks, environment/rules settings, and runner history. Availability depends on permissions, plan, and retention. Do not request token values, add scopes, authorize an app, or assume an audit-log denial is an empty log. Keep third-party service internals explicitly out of coverage unless separately authorized and examined.

Authoritative references (recheck at execution time):
- [Workflow runs and attempts](https://docs.github.com/en/rest/actions/workflow-runs)
- [REST pagination](https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api)
- [Organization audit log](https://docs.github.com/en/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/reviewing-the-audit-log-for-your-organization)
- [GitHub CLI API](https://cli.github.com/manual/gh_api)
