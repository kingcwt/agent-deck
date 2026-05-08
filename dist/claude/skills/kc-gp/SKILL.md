---
name: kc-gp
description: Commit the current repository changes with a required user-provided description and push the current branch to the remote repository. Use when the user types /kc-gp followed by a non-empty description, $kc-gp followed by a non-empty description, kc-gp followed by a non-empty description, or asks to stage the current repo changes, create one git commit, and push that commit to the current branch on the remote.
---

> Canonical source for this skill. Keep this file as the only executable source of truth.
> See `source.zh-CN.md` for the one-to-one Chinese translation used only for reading and understanding.

# Git Push

## Overview

Stage the current repository changes, create one git commit using the description supplied after the shortcut, and push the current branch to the configured remote branch.

## Workflow

### 1. Require a commit description

- Treat `/kc-gp` and `$kc-gp` as explicit shortcuts for this workflow.
- Require non-empty trailing text after the shortcut. Treat that trailing text as the commit description and default commit message source.
- If the user does not provide a description, stop and ask for it instead of inventing one.
- Preserve the user's intent in the commit message. Only tighten wording when the original text is too vague to function as a commit message, and say so explicitly.

### 2. Inspect the repository state

- Read `git status --short`, the current branch name, and the configured remotes before mutating anything.
- Summarize which files are changed, whether changes are already staged, and which branch will be pushed.
- If there are no local changes, say so plainly and stop.
- If there is no usable remote or the current branch cannot be pushed yet, explain the blocker and stop before creating a commit.

### 3. Protect scope before committing

- Treat this workflow as an explicit “commit and push what is currently in this repository” action.
- By default, stage the current repository changes with one commit. Do not silently drop files from the commit set.
- If the worktree contains changes that appear unrelated to the user's stated intent, call that out before committing so the user can redirect if needed.
- Do not rewrite history, amend prior commits, force-push, or switch branches unless the user explicitly asks.

### 4. Create the commit

- Stage the repository changes using a non-interactive git command.
- Create exactly one commit using the provided description as the commit message.
- If commit hooks fail, report the failure and stop. Do not bypass hooks unless the user explicitly asks.
- If git rejects the commit because identity is missing or the index is empty, report the exact blocker and stop.

### 5. Push safely

- Push the current branch to its configured upstream when one exists.
- If the branch has no upstream but `origin` exists, push with upstream setup using the current branch name.
- If push is rejected because the remote has new commits, report that clearly and stop instead of forcing the push.
- If network or permission approval is required in the environment, request it rather than pretending the push succeeded.

### 6. Report the result

- Report the commit message used.
- Report the branch and remote target that were pushed.
- Report the resulting commit hash when available.
- If any step fails, report the exact failing step and the blocking error without padding.

## Guardrails

- This workflow is for explicit commit-and-push execution, not for code review or cleanup.
- Do not edit application code as part of this workflow unless the user separately asks for fixes.
- Do not create multiple commits from one invocation.
- Do not push to a different branch than the current branch unless the user explicitly asks.
- Do not fabricate success. Verification must come from the actual git command results.
