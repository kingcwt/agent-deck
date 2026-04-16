---
name: diff-review
display_name: Diff Review
description: Review and explain the current editor file's git changes. Use when the user types /df, /diff-review, $df, $diff-review, df, or asks to analyze the current file diff, explain each change point and why it exists, connect the edits to surrounding code and project context, judge whether the edits are necessary, and check whether the implementation stays minimal, reuses existing code, and avoids unrelated shared-code edits or opportunistic refactors.
short_description: Analyze a file diff for intent, necessity, and scope control
default_prompt: Use $df to inspect the current file diff, explain the meaning of the changes, judge whether they are necessary, and flag non-minimal or risky edits.
codex_names: df,diff-review
claude_skill_names: df,diff-review
claude_commands: df,diff-review
allow_implicit_invocation: false
---

> Canonical source for this skill. Keep this file as the only executable source of truth.
> See `source.zh-CN.md` for the one-to-one Chinese translation used only for reading and understanding.

# Diff Review

## Overview

Review the current editor file's git changes before trusting them. Explain each change point in that file, why it was changed, what surrounding references and project context it depends on, whether the change is necessary, and whether the scope stays minimal and justified.

## Workflow

### 1. Locate the review target

- Treat `/df` and `/diff-review` as explicit review shortcuts.
- Treat the current editor file as the review target by default. The user is invoking this for the file they currently have open or selected.
- Review exactly one file per invocation. Do not switch to another changed file and do not expand the review scope to the whole repository diff.
- Inspect that file's git diff first. If the file has no git changes, say so plainly and stop.
- Use other files only as supporting context for understanding the current file's edits, never as additional review targets.

### 2. Read context before judging

- Read the full changed file, not just the diff hunk.
- Read the nearest directly related code needed to understand each change point, such as imported helpers, sibling functions, nearby types, call sites, and upstream or downstream references.
- Reuse existing project constraints from repo instructions, comments, and local conventions instead of inventing new standards.
- Do not approve or reject a change from the patch alone when surrounding code would materially change the judgment.

### 3. Explain the change

- Break the current file diff into meaningful change points instead of describing the file as one undifferentiated edit.
- For each change point, summarize the actual behavior or structural change in concrete terms.
- For each change point, explain why the author likely made it and what problem it is trying to solve.
- For each change point, connect it to the surrounding references and project context that make the edit meaningful.
- Call out whether each change point affects business logic, data flow, UI behavior, error handling, performance, shared interfaces, or only local readability.
- Distinguish intent from inference. If the reason is not explicit, say it is your inference from code and context.

### 4. Judge necessity

- For each meaningful edit, decide whether it is:
  - necessary for the stated requirement
  - reasonable but optional
  - questionable or unrelated
- Check whether the same goal could be achieved with a smaller local change.
- Check whether the change reuses existing helpers, types, components, or patterns before introducing new logic.
- Flag edits that widen scope without a clear requirement, especially public utilities, shared packages, common config, schema-related code, or broad refactors.

### 5. Check minimal-change discipline

- Explicitly look for signs of overreach:
  - unrelated cleanup or formatting churn
  - opportunistic optimization
  - shared-code edits that are not required by the task
  - duplicated logic instead of reusing existing code
  - interface expansion that forces downstream changes
- If a public or shared module changed, explain why that might be risky and whether a local-module alternative exists.
- If the change is justified, say why the broader touch area is actually required.

### 6. Report clearly

- Start with findings, ordered by severity, when you detect unnecessary, risky, or weakly justified edits.
- Then provide a compact summary covering:
  - the current file being reviewed
  - each meaningful change point in the file
  - why each change point exists
  - what references or project context each point depends on
  - whether each point is necessary
  - whether the overall scope is minimal
- When useful, end with a clear verdict such as `necessary`, `acceptable but could be smaller`, or `should be revised`.

## Guardrails

- This is a review and explanation workflow first, not an editing workflow.
- Do not silently modify code unless the user explicitly asks for fixes after the review.
- Prefer concrete file and line references over vague commentary.
- Do not turn this into a multi-file review. The subject under review is always the current file's git diff.
- Do not label a shared-code change as acceptable unless you can explain why a local change would not work.
- If there is no diff to inspect, say so plainly and stop instead of inventing a review.
