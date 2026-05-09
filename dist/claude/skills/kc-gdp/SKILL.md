---
name: kc-gdp
description: Describe the current repository's changed files one by one with short, concrete summaries, turn those summaries into one commit message, then commit and push the current branch. Use when the user types /kc-gdp, $kc-gdp, kc-gdp, or asks to summarize current changes and then push them in one flow.
---

> Canonical source for this skill. Keep this file as the only executable source of truth.
> See `source.zh-CN.md` for the one-to-one Chinese translation used only for reading and understanding.

# Git Diff Description Push

## Overview

Inspect all current changed files in the repository, generate one short and concrete description per file from the diff and surrounding context, synthesize those descriptions into one commit message, then stage the current repository changes, create one commit, and push the current branch.

## Workflow

### 1. Inspect the repository state first

- Treat `/kc-gdp` and `$kc-gdp` as explicit shortcuts for this workflow.
- Read `git status --short`, the current branch name, and the configured remotes before mutating anything.
- Identify all changed files first, including staged and unstaged tracked changes plus untracked files in the current worktree.
- If there are no local changes, say so plainly and stop.
- If there is no usable remote or the current branch cannot be pushed yet, explain the blocker and stop before creating a commit.

### 2. Generate short descriptions per file

- For each changed file, inspect its git diff first.
- Read the current file content when the diff alone is not enough to tell what changed.
- Read only the nearest surrounding code or references needed to describe the change accurately.
- For untracked files, inspect the file content directly and infer the purpose from its name and content.
- For deleted files, use the removal diff and surrounding references to describe what was removed.
- Output one short and concrete description per changed file.
- Prefer wording like `add login button`, `fill in UserSession type`, `adjust order list request params`, or `remove deprecated payment callback`.
- Avoid vague summaries like `optimize code`, `fix some issues`, or `update logic`.

### 3. Turn the descriptions into one commit message

- Use the per-file descriptions as the source material for the commit message.
- Compress them into one concise commit message that preserves the real changed nouns and actions.
- If the user provides trailing text after `/kc-gdp` or `$kc-gdp`, treat that text as an explicit commit message override, but still generate and show the per-file descriptions first.
- If the changed files appear unrelated to each other, call that out before committing so the user can redirect if needed.

### 4. Create one commit

- Stage the current repository changes using a non-interactive git command.
- Create exactly one commit using the derived commit message or the user's explicit override.
- If commit hooks fail, report the failure and stop. Do not bypass hooks unless the user explicitly asks.
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
