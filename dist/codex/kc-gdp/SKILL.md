---
name: kc-gdp
description: Describe the current repository's changed files one by one with short, concrete summaries, turn those summaries into a multi-line commit message, then commit and push the current branch. Use when the user types /kc-gdp, $kc-gdp, kc-gdp, or asks to summarize current changes and then push them in one flow.
---

> Canonical source for this skill. Keep this file as the only executable source of truth.
> See `source.zh-CN.md` for the one-to-one Chinese translation used only for reading and understanding.

# Git Diff Description Push

## Description

Read the current repository diff, generate one short description per changed file when no custom message is provided, build a commit message, then commit and push the current branch. Generated descriptions default to Chinese, and switch to English only when `-e` is passed.

## Parameters

- Required: none.
- Optional `-e`: switch generated descriptions and summary line to English.
- Optional `[commit message]`: when any non-empty text follows the shortcut, use all remaining text as the complete commit message.
- Supported format: `[-e] [commit message]`.

## Shortcuts And Commands

- Codex shortcut: `$kc-gdp`
- Codex full command: `$kc-gdp [-e] [commit message]`
- Claude Code shortcut: `/kc-gdp`
- Claude Code full command: `/kc-gdp [-e] [commit message]`

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

### 2. Resolve the commit message mode

- After the shortcut, preserve the user's remaining text as one raw argument payload, including internal line breaks, blank lines, punctuation, and spacing that belongs to the message.
- Support only one optional language flag right after the shortcut: if the raw payload starts with an exact `-e` token, remove that token and only the separator whitespace immediately after it before checking whether custom message text remains.
- If any non-empty custom message text remains after optional `-e` removal, use that text as the complete commit message instead of generating a summary line or appending generated per-file description lines.
- Custom commit message text may span multiple lines. Do not collapse it to one line, split it on newlines, or drop later lines.
- If no non-empty custom message text remains, continue with the default generated-description flow below.

### 3. Generate one short description per changed file

- Inspect each changed file's diff first.
- Read the current file content only when the diff alone is not enough to tell what changed.
- Default the generated per-file descriptions to Chinese. Switch them to English only when the user explicitly passes `-e`.
- Keep each description short, concrete, and action-oriented.
- Do not fall back to vague summaries like `optimize code`, `fix some issues`, or `update logic`.

### 4. Build one multi-line commit message

- Use the per-file descriptions as the source material for the commit message.
- The first line must be one short overall summary line for the whole change set.
- The following lines must include the generated per-file descriptions, one description per line.
- Only run this generated-message step when the user did not provide custom commit message text after the shortcut.
- Keep the generated description lines as plain descriptions instead of prefixing them with file paths unless a path is truly needed for disambiguation.
- If the changed files appear unrelated to each other, call that out before committing so the user can redirect if needed.

### 5. Create one commit

- Stage the current repository changes using a non-interactive git command.
- Create exactly one commit using either the complete custom commit message or the derived generated multi-line commit message.
- Use a non-interactive git command that preserves line breaks in the final commit message, such as writing the message to a temporary file and committing with `git commit -F <file>`.
- If commit hooks fail, report the failure and stop.
- If git rejects the commit because identity is missing or the index is empty, report the exact blocker and stop.

### 6. Push safely

- Push the current branch to its configured upstream when one exists.
- If the branch has no upstream but `origin` exists, push with upstream setup using the current branch name.
- If push is rejected because the remote has new commits, report that clearly and stop instead of forcing the push.
- If network or permission approval is required in the environment, request it rather than pretending the push succeeded.

### 7. Report the result

- Report the per-file descriptions you generated, or state that a custom commit message was used when generation was skipped.
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
