# /kc-gdd

<!-- This file is generated from skills/*/source.md. Edit the source file instead. -->

Execute the following workflow in the current working directory.
Treat this command as the user's explicit shortcut for the workflow below.

> Canonical source for this skill. Keep this file as the only executable source of truth.
> See `source.zh-CN.md` for the one-to-one Chinese translation used only for reading and understanding.

# Git Diff Review

## Description

Read the current repository diff and output a concise Chinese review of the changed files: what each file changed, whether the implementation can be smaller, and whether the changes may affect other modules or logic.

## Parameters

- Required: none.
- Optional language: Chinese by default; use English only when the user explicitly asks for English.
- Output: concise per-file change summaries plus review findings, minimal-implementation suggestions, and impact notes.

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

### 3. Write Chinese per-file change summaries

- Default output language is Chinese. Do not output English unless the user explicitly asks for English.
- Produce one concise main description for each changed file.
- Keep each description short, concrete, and action-oriented.
- Prefer wording like `新增登录按钮`, `补充 UserSession 类型`, `调整订单列表请求参数`, or `删除废弃支付回调`.
- Name the actual feature, type, field, component, config, or behavior that changed. Avoid vague summaries like `优化代码`, `修复一些问题`, or `更新逻辑`.
- If one file contains multiple tightly related edits, compress them into one sentence with the main intent.
- If the exact intent is uncertain, use cautious Chinese wording based on the code, such as `看起来是`, `大概率用于`, or `可能用于`.

### 4. Review the changed files

- After the per-file summaries, review the diff for actionable issues.
- Check whether each change stays within the smallest safe implementation for the apparent requirement.
- Flag redundant code, duplicated logic, unnecessary abstractions, speculative options, broad rewrites, or unrelated cleanup.
- Check whether the change should reuse an existing helper, component, type, API shape, or local pattern instead of adding new logic.
- Check whether shared modules, shared components, public types, config, database-related code, or cross-page behavior are affected.
- If a changed file may affect another module or caller, name the affected module or call path.
- If there are no actionable issues, say `未发现需要修改的问题。`
- Keep review comments concise and actionable; do not turn the answer into a long tutorial.

### 5. Keep the output compact

- Use this default output shape:
  - `改动文件`: flat list in the form `path: 中文简短描述`.
  - `审查结论`: findings ordered by severity, or `未发现需要修改的问题。`
  - `影响范围`: cross-module or behavior impact notes, or `未发现明显跨模块影响。`
- Keep the whole answer brief enough to scan.
- Do not collapse multiple files into one repository-level summary.

## Guardrails

- This workflow is for concise changed-file review, not for code editing or commit creation.
- The review is read-only by default. Do not modify code unless the user explicitly asks for fixes.
- Chinese is mandatory by default. English output is only allowed when the user explicitly requests English.
- Do not invent descriptions from filenames alone when the diff or file content is available.
- Do not use generic labels when a concrete business or technical noun is available in the code.
- Do not silently skip changed files unless the user explicitly narrows the scope.
- If a file's purpose cannot be determined with confidence, say that briefly rather than overstating certainty.
