---
name: kc-gdd
description: Describe the current repository's changed files one by one with short, concrete summaries based on each file's git diff and surrounding context. Use when the user types /kc-gdd, $kc-gdd, kc-gdd, or asks to find all current changed files and produce a brief per-file description of what was changed.
---

> Canonical source for this skill. Keep this file as the only executable source of truth.
> See `source.zh-CN.md` for the one-to-one Chinese translation used only for reading and understanding.

# Git Diff Description

## Description

Read the current repository diff and output one short, concrete description for each changed file.

## Parameters

- Required: none.
- Optional flags: none.
- Output: one short, concrete description per changed file.

## Shortcuts And Commands

- Codex shortcut: `$kc-gdd`
- Codex full command: `$kc-gdd`
- Claude Code shortcut: `/kc-gdd`
- Claude Code full command: `/kc-gdd`

## Examples

### Codex

```text
$kc-gdd
```

### Claude Code

```text
/kc-gdd
```

## Workflow

### 1. Find the changed files first

- Treat `/kc-gdd` and `$kc-gdd` as explicit shortcuts for this workflow.
- Treat the invocation itself as the whole task for this turn. Do not continue the previous conversation topic or answer the last non-command question instead of running this workflow.
- Start from the current repository state and identify all changed files before writing any descriptions.
- Include staged and unstaged tracked changes, plus untracked files when they are part of the current worktree.
- Preserve the file-level scope. The primary output unit is one description per changed file.
- If there are no changed files, say so plainly and stop.

### 2. Read the diff with enough context

- For each changed file, inspect its git diff first.
- Read the current file content when the diff alone is not enough to tell what changed.
- Read only the nearest surrounding code or references needed to understand the change accurately, such as the related component, type, helper, or call site.
- For untracked files, inspect the file content directly and infer the purpose from its name and content.
- For deleted files, use the removal diff and surrounding references to describe what was removed.

### 3. Write one short description per file

- Produce exactly one main description for each changed file unless the user explicitly asks for more detail.
- Keep each description short, concrete, and action-oriented.
- Prefer wording like `add login button`, `fill in UserSession type`, `adjust order list request params`, or `remove deprecated payment callback`.
- Name the actual feature, type, field, component, config, or behavior that changed. Avoid vague summaries like `optimize code`, `fix some issues`, or `update logic`.
- If one file contains multiple tightly related edits, compress them into one short sentence with the main intent.
- If the exact intent is uncertain, use cautious wording based on the code, such as `appear to`, `likely`, or `used to`.

### 4. Keep the output compact

- Default to a flat file-by-file list in the form `path: short description`.
- Keep the descriptions brief enough that the user can scan the whole change set quickly.
- Do not expand into long explanations, review findings, or step-by-step reasoning unless the user asks.
- Do not collapse multiple files into one repository-level summary when the user asked for per-file descriptions.

## Guardrails

- This workflow is for concise diff description, not for code review, code editing, or commit creation.
- Do not invent descriptions from filenames alone when the diff or file content is available.
- Do not use generic labels when a concrete business or technical noun is available in the code.
- Do not silently skip changed files unless the user explicitly narrows the scope.
- If a file's purpose cannot be determined with confidence, say that briefly rather than overstating certainty.
