# /kc-gdp

<!-- This file is generated from skills/*/source.md. Edit the source file instead. -->

Execute the following workflow in the current working directory.
Treat this command as the user's explicit shortcut for the workflow below.

> Canonical source for this skill. Keep this file as the only executable source of truth.
> See `source.zh-CN.md` for the one-to-one Chinese translation used only for reading and understanding.

# Git Diff Description Push

## Description

Read the current repository diff, generate one short description per changed file, build a multi-line commit message from those descriptions, then commit and push the current branch. Generated descriptions default to Chinese, and switch to English only when `-e` is passed.

## Parameters

- Required: none.
- Optional `-e`: switch generated descriptions and summary line to English.
- Optional `[summary line]`: use the trailing text as the first line of the commit message.
- Supported format: `[-e] [summary line]`.

## Shortcuts And Commands

- Codex shortcut: `$kc-gdp`
- Codex full command: `$kc-gdp [-e] [summary line]`
- Claude Code shortcut: `/kc-gdp`
- Claude Code full command: `/kc-gdp [-e] [summary line]`

## Examples

### Codex

```text
$kc-gdp
$kc-gdp feat: add region-manager entry selection flow
$kc-gdp -e
$kc-gdp -e feat: add region-manager entry selection flow
```

### Claude Code

```text
/kc-gdp
/kc-gdp feat: add region-manager entry selection flow
/kc-gdp -e
/kc-gdp -e feat: add region-manager entry selection flow
```

## Workflow

### 1. Inspect the repository state

- Treat `/kc-gdp` and `$kc-gdp` as explicit shortcuts for this workflow.
- Treat the invocation itself as the whole task for this turn. Do not continue the previous conversation topic or reuse an earlier conclusion like `already committed`, `no changes`, or `repository is clean` without re-checking the current repository state.
- Support only one optional language flag right after the shortcut: `-e` switches the generated descriptions to English.
- Read `git status --short`, the current branch name, and the configured remotes before mutating anything.
- Use the fresh `git status --short` result from this invocation as the source of truth for whether local changes exist. If the worktree and index are not empty, do not claim there are no changes.
- Identify all changed files first, including staged, unstaged, and untracked files in the current worktree.
- If there are no local changes, say so plainly and stop.
- If there is no usable remote or the current branch cannot be pushed yet, explain the blocker and stop before creating a commit.

### 2. Generate one short description per changed file

- Inspect each changed file's diff first.
- Read the current file content only when the diff alone is not enough to tell what changed.
- Default the generated per-file descriptions to Chinese. Switch them to English only when the user explicitly passes `-e`.
- Keep each description short, concrete, and action-oriented.
- Do not fall back to vague summaries like `optimize code`, `fix some issues`, or `update logic`.

### 3. Build one multi-line commit message

- Use the per-file descriptions as the source material for the commit message.
- The first line must be one short overall summary line for the whole change set.
- The following lines must include the generated per-file descriptions, one description per line.
- If the user provides trailing text after the shortcut, remove only an exact leading `-e` token when present, then treat the remaining text as the explicit first summary line.
- Keep the generated description lines as plain descriptions instead of prefixing them with file paths unless a path is truly needed for disambiguation.
- If the changed files appear unrelated to each other, call that out before committing so the user can redirect if needed.

### 4. Create one commit

- Stage the current repository changes using a non-interactive git command.
- Create exactly one commit using the derived multi-line commit message or the user's explicit first line plus generated per-file lines.
- Use a non-interactive git command that preserves line breaks in the final commit message.
- If commit hooks fail, report the failure and stop.
- If git rejects the commit because identity is missing or the index is empty, report the exact blocker and stop.

### 5. Push safely

- Push the current branch to its configured upstream when one exists.
- If the branch has no upstream but `origin` exists, push with upstream setup using the current branch name.
- If push is rejected because the remote has new commits, report that clearly and stop instead of forcing the push.
- If network or permission approval is required in the environment, request it rather than pretending the push succeeded.

### 6. Report the result

- Report the per-file descriptions you generated.
- Report the commit message used.
- Report the branch and remote target that were pushed.
- Report the resulting commit hash when available.
- If any step fails, report the exact failing step and the blocking error without padding.

## Guardrails

- This workflow combines concise diff description with explicit commit-and-push execution.
- Do not edit application code as part of this workflow unless the user separately asks for fixes.
- Do not silently drop changed files from the commit set.
- Do not create multiple commits from one invocation.
- Do not rewrite history, amend prior commits, force-push, or switch branches unless the user explicitly asks.
- Do not fabricate success. Verification must come from the actual git command results.
