---
name: diff-review
display_name: Diff Review
description: Review and explain only the current editor file's git changes. Use when the user types /df, /diff-review, $df, $diff-review, df, or asks to analyze the current file diff, list the changed code first, explain what those edits are doing, connect the edits to surrounding code and project context, judge whether they are necessary, and check whether the implementation stays minimal, reuses existing code, and avoids unrelated shared-code edits or opportunistic refactors.
short_description: Analyze a file diff for intent, necessity, and scope control [对当前的GIT更改做审查]
default_prompt: Use $df to inspect only the current file diff, list the changed code first, explain what the edits are doing, then judge whether they are necessary and flag non-minimal or risky edits.
codex_names: df,diff-review
claude_skill_names: df,diff-review
claude_commands: df,diff-review
allow_implicit_invocation: false
---

> Canonical source for this skill. Keep this file as the only executable source of truth.
> See `source.zh-CN.md` for the one-to-one Chinese translation used only for reading and understanding.

# Diff Review

## Description

Review only the current file's git changes, explain what each change is doing, and judge whether the change is necessary and minimal.

## Parameters

- Required: none.
- Review target: exactly one current file with git changes.
- Optional flags: none.
- Not supported by default: repository-wide diff review, multi-file batching, or automatic code fixes.

## Shortcuts And Commands

- Codex shortcuts: `$df`, `$diff-review`
- Codex full commands: `$df`, `$diff-review`
- Claude Code shortcuts: `/df`, `/diff-review`
- Claude Code full commands: `/df`, `/diff-review`

## Examples

### Codex

```text
$df
$diff-review
```

### Claude Code

```text
/df
/diff-review
```

## Workflow

### 1. Locate the review target

- Treat `/df` and `/diff-review` as explicit review shortcuts.
- Treat the current editor file as the review target by default. The user is invoking this for the file they currently have open or selected.
- Review exactly one file per invocation. Do not switch to another changed file and do not expand the review scope to the whole repository diff.
- Resolve the target to one concrete file path before reading any diff. If the environment does not expose the current file path, ask the user for that path instead of falling back to a repository-wide review.
- Inspect that file's git diff first. If the file has no git changes, say so plainly and stop.
- When reading git changes, always use a file-scoped diff command or equivalent path-limited diff input. Never review a bare repository-wide diff as a substitute for the current file.
- Use other files only as supporting context for understanding the current file's edits, never as additional review targets.

### 2. Read context before judging

- Read the full changed file, not just the diff hunk.
- Read the nearest directly related code needed to understand each change point, such as imported helpers, sibling functions, nearby types, call sites, and upstream or downstream references.
- Reuse existing project constraints from repo instructions, comments, and local conventions instead of inventing new standards.
- Do not approve or reject a change from the patch alone when surrounding code would materially change the judgment.

### 3. Explain the change

- Start by showing the changed code from the current file only. Present the diff hunks, or a compact hunk-by-hunk excerpt, before giving evaluative commentary.
- Break the current file diff into meaningful change points instead of describing the file as one undifferentiated edit.
- The first explanatory step after showing the code is to say what the changed code is doing now. Do this before discussing necessity, risks, or alternative designs.
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

- Use this output order unless the user explicitly asks for another format:
  - `Changed code`: list the current file's modified hunks first
  - `What the change is doing`: explain each hunk or change point in plain terms
  - `Context and why`: connect the edits to nearby code and inferred intent
  - `Assessment`: judge necessity, scope discipline, and risks
- In `Changed code`, include only the current file's diff content. Do not mix in hunks from other files.
- In `What the change is doing`, explain the behavior change before offering opinions about whether the change is good.
- In `Assessment`, surface findings ordered by severity when you detect unnecessary, risky, or weakly justified edits.
- Make sure the full report still covers:
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
- Do not replace the current-file review with a staged diff summary, full `git diff`, or “all changed files” overview.
- Do not label a shared-code change as acceptable unless you can explain why a local change would not work.
- If there is no diff to inspect, say so plainly and stop instead of inventing a review.
