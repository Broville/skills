# Reports for people with no technical background

## First screen

Use short sentences and answer, in order: Were security findings found? What happened? Why does it matter to me? What should I do next? What could not be checked? Avoid jargon, raw hashes, platform IDs, severity formulas, and reassuring scores. A novice should not need the appendix to understand the action.

Status semantics:
- GREEN — No security findings in the checked areas. State the checked scope and period. Explained activity and separate maintenance items may remain; do not call those security findings. Never say “guaranteed safe,” “completely clean,” or “nothing happened.”
- YELLOW — Something needs clarification or could not be checked. Use for suspicious but unconfirmed activity, owner-attribution questions, and material coverage gaps. Say explicitly whether any confirmed findings exist. If some sections are green but others have gaps, the overall report is yellow, not green.
- RED — Confirmed security findings need attention. Explain the specific verified fact. Use “Urgent verified concern” only when evidence supports urgency; red does not automatically mean data was stolen. Keep unresolved coverage visible even alongside red.

Always provide words and a symbol/label as well as color, strong contrast, legible type, keyboard-selectable prompts, and no color-only meaning. Avoid animations, remote fonts/scripts, tracking, and alarming decorative imagery. A self-contained HTML file is suitable; a text/Markdown fallback must preserve the same labels, counts, caveats, and prompts. Do not expose private report data to a hosted renderer without authorization.

## Organize findings

Separate four groups: security findings; warnings/questions; maintenance improvements; explained activity. Each item says what happened, why it matters, what is established versus unknown, and who should take the smallest next step. Do not mix “pin a dependency” into “someone stole your credentials.” Keep long evidence in an appendix with IDs, source dates, exact revisions, coverage tables and limitations. No credential values appear anywhere.

## Support prompts

Every finding, warning, maintenance item, and material gap gets a copyable standalone prompt. Name the scoped target, timeframe, finding/evidence references, uncertainty, and next safe step. Make clear that the user should provide the private report/evidence to the same trusted agent if it lacks context. A reference like E12 is not a public retrievable source; explain that the attached audit contains it. Do not embed secrets or turn a help prompt into authorization for remediation, account access expansion, execution, deletion, or third-party communication.

Example, entirely synthetic:

“Please help with finding F2 in my attached audit of Example project for April 1–2, 2030 UTC. The audit found an unfamiliar automation restart; evidence E7 shows the run and attempt. First check whether the activity matches my expected import, and explain the result in everyday language. Ask for missing context or required access permission. Do not run code, change access/settings, rotate credentials, delete anything, or contact anyone without the required approval.”

A gap prompt should ask the agent to identify the smallest missing record or permission decision, not say “grant all access.” A red finding prompt should ask for evidence preservation and a proposed containment plan with impact, not silently authorize that plan.

## Final quality check

Read just the first screen aloud: can someone say whether findings exist and what to do? Are numbers honest (confirmed findings versus warnings versus unavailable areas)? Does each sentence distinguish evidence from inference? Are expected activities explicitly closed only to their supported extent? Does every next action have a person and a clear step? Does the scope/timeframe remain visible if the report is forwarded? If any answer is no, revise before delivery.

The helper provides a conservative rendering baseline, not a substitute for these decisions. Its caller defines required streams and supplies the reviewed evidence. It cannot discover omitted scope, detect all secrets, or judge whether analyst conclusions are correct.
