---
name: agent-code-review
description: Coordinate independent review of a coding candidate against correctness, requirements and project context, with evidence-based findings and bounded repairs. Use when requested or required by session/project instructions after code, tests, executable notebooks or behavior-affecting configuration changes. Reviewer-only subtasks perform their assigned review without launching this workflow again.
---

# Agent code review

Produce a review record tied to the actual final candidate, with independent findings and explicit verification limits. Follow the user's requested scope and existing authorization. This workflow does not itself permit merging, deploying, publishing or external messages.

## 1. Establish scope and evidence

Before implementation when possible, record the requested behavior, constraints, acceptance criteria and relevant project decisions. Use the user's actual words for decisive constraints. Distinguish agreed requirements from inferred assumptions. If invoked after writing code, reconstruct these from the request and source documents, not from what the implementation happens to do. Read applicable project instructions and nearby callers/tests/contracts.

Use the repository's established review-record location or a task-local output folder. For a tiny edit the record can be in the response; a substantial task should retain it in a file. Adapt [assets/review-record.md](assets/review-record.md), omitting irrelevant fields. Keep secrets and unrelated private material out of review packets and logs.

Identify the review scope: this task's changes, a specified branch/commit range, or another explicit candidate. Inventory pre-existing edits without taking ownership or undoing them. If an inseparable existing edit changes behavior, include it as a dependency and state that boundary.

Bind each candidate to a base and a version. For committed code record the base and candidate commit IDs and whether the working tree is clean. For uncommitted work also retain the relevant staged/unstaged diff, changed/untracked file list and content hashes or a safe snapshot; HEAD alone is insufficient. Without Git, use a before/after snapshot or a manifest of relevant paths and hashes, explicitly noting any missing baseline. Include relevant configuration and dependency versions. Use source-data identifiers/hashes when they affect scientific validation. Do not package credentials or large datasets indiscriminately.

## 2. Implement, check and freeze

The main agent or designated implementer owns edits. Run applicable repository checks and targeted validation of the changed behavior. Record commands, environment, observed outcomes and the candidate they tested. Do not label an intended command, an author's assertion, or a smoke test as completed acceptance validation.

Use meaningful existing checks first. Add a regression test or independent reference case when it can demonstrate a material defect or requirement; do not invent tests merely to mirror implementation or for trivial cosmetic edits. Failed, unavailable, skipped and timed-out checks remain distinct.

Freeze implementation changes while reviewers read it. Test outputs belong in isolated scratch locations; serialize checks if they share mutable state. Reviewers may inspect dependencies and run safe checks, but must not edit the implementation or change the environment. A prompt is a role constraint, not sandbox isolation. If another actor changes the candidate mid-review, mark affected evidence stale and re-establish a stable candidate.

## 3. Dispatch independent reviewers

Read [references/reviewer-prompts.md](references/reviewer-prompts.md) and select by consequence:

- Small, low-consequence code change: one fresh reviewer covers both correctness and context.
- Ordinary behavioral change: correctness and context reviewers in parallel.
- Substantial additional risk: add a specialist for the dominant risk. For multiple unrelated risks, cover them sequentially or split the scope; do not force unrelated expertise into one pass.

Use available subagent tools, not new user-owned chats. Give reviewers a fresh context: with `collaboration.spawn_agent`, use `fork_turns="none"`; omit model overrides unless explicitly requested or otherwise required. Other runtimes should use their supported equivalent. Provide the full required review packet and relevant file paths, not the author's deliberations. If fresh context is unavailable, disclose the weaker independence. Do not claim a different model was used without runtime evidence.

Each packet contains: original request and later corrections, applicable instructions, acceptance criteria, relevant decisions/contracts, exact candidate and base, scope, dependencies, test evidence and gaps. The reviewer must retrieve pertinent context directly from those sources. Do not withhold raw test failures or known constraints to simulate independence. Hold back the author's persuasive rationale and other reviewers' conclusions until independent initial findings return.

Use only available concurrency. The usual arrangement is the main agent plus two reviewers, or plus three with a specialist; queue roles if fewer slots exist. Reviewer-only agents must not spawn more reviewers. Wait for all selected roles; replace failed reviewers where feasible and report any remaining coverage gap. Do not start repairs while initial reviewers are still reading a shared candidate.

## 4. Reconcile evidence

Every finding needs a location, triggering condition, consequence, evidence and a proposed verification. Distinguish confirmed defects, plausible but unverified concerns and questions. A line-by-line argument can establish a defect without a runtime reproduction; label the evidence accurately. Do not manufacture findings to fill a quota.

Use severity consistently:

- P0: immediate critical harm, exploitable exposure or destructive corruption; stop the affected action.
- P1: major correctness, security, data-integrity or compatibility failure; blocks PASS.
- P2: meaningful localized defect; blocks PASS if it violates an acceptance criterion or materially undermines the result. Otherwise fix within scope or explicitly document a justified deferral.
- P3: optional improvement; does not block PASS and does not justify scope expansion.

Merge duplicates while retaining their evidence. Resolve by reproduction, a traced code path, contract or independent calculation, not majority voting or confidence scores. Passing tests do not automatically disprove an uncovered case. The author may explain or rebut; dismiss a finding only with recorded evidence. A credible unresolved concern affecting a material criterion prevents PASS even if nobody reproduced it yet.

Fix confirmed, in-scope material defects. Turn a real defect into a focused regression check when useful. Do not weaken acceptance criteria or alter expected results merely to make tests pass. User decisions are needed for materially ambiguous requirements or tradeoffs beyond current authorization; make the issue concrete and finish unaffected work first. Routine reversible repairs do not require another permission request.

## 5. Repair with a stopping rule

Allow one initial review and at most two repair-and-review rounds: three review passes total. Keep this counter for the whole coherent change; new agent names or candidate IDs do not reset it. Stop earlier when all criteria are satisfied. If the same finding recurs or conflicting requirements prevent convergence, diagnose the cause instead of adding reviewers indefinitely.

Every repair creates a new candidate. Rerun affected checks and obtain independent re-review of the fix, its dependencies and regression risk. Previously resolved findings and rationale may be given at this stage. Preserve unaffected evidence only when its applicability to the new candidate is justified. Any later substantive edit invalidates affected review results. If the budget is exhausted, return the bounded result with unresolved issues and recommended next action; do not claim completion or silently reset the loop. A user can explicitly authorize a further cycle.

## 6. Decide and report

Use exactly one review outcome:

- **PASS:** selected review roles completed, required criteria and checks have evidence on the current candidate, and no material finding or uncertainty remains unresolved. Record any non-material deferred issues.
- **CHANGES_REQUIRED:** a confirmed material defect or acceptance failure remains. Record additional evidence gaps separately.
- **INCOMPLETE:** no confirmed remaining blocker has been established, but missing context, unavailable checks, stale evidence or incomplete reviewer coverage prevents a justified PASS.

If delegation is unavailable, still perform useful direct checks and describe the result as direct review; the independent-review gate remains INCOMPLETE. Never present an implementer's self-review as independent.

The final handoff states: outcome and candidate, behavior changed, reviewers used, observed checks, resolved and open findings, and any remaining decision. Separate software execution, numerical verification, domain validity and production completion where applicable. The review is advice and evidence, not a guarantee or human sign-off. Honor existing human approvals without asking again unless the action or material risk has changed.
