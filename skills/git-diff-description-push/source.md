---
name: git-diff-description-push
display_name: Git Diff Description Push
description: Describe the current repository's changed files one by one with short, concrete summaries, turn those summaries into a multi-line commit message, then commit and push the current branch. Use when the user types /kc-gdp, $kc-gdp, kc-gdp, or asks to summarize current changes and then push them in one flow.
short_description: Describe current changes, commit, and push [先生成描述再提交推送]
default_prompt: Use $kc-gdp to summarize the current changed files, derive a multi-line commit message from those descriptions, create one commit, and push the current branch.
codex_names: kc-gdp
claude_skill_names: kc-gdp
claude_commands: kc-gdp
allow_implicit_invocation: false
---

> Canonical source for this skill. Keep this file as the only executable source of truth.
> See `source.zh-CN.md` for the one-to-one Chinese translation used only for reading and understanding.

# Git Diff Description Push

## Overview

Inspect all current changed files in the repository, generate one short and concrete description per file from the diff and surrounding context, synthesize those descriptions into a multi-line commit message, then stage the current repository changes, create one commit, and push the current branch.

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

### 3. Turn the descriptions into one multi-line commit message

- Use the per-file descriptions as the source material for the commit message.
- The commit message must not collapse all changes into one sentence.
- Build a multi-line commit message instead:
  - first line: one short overall summary line for the whole change set
  - following lines: include the generated per-file descriptions, one file per line
- Keep the generated per-file lines concrete and readable instead of prefixing them with raw paths unless the path is needed to disambiguate.
- If the user provides trailing text after `/kc-gdp` or `$kc-gdp`, treat that text as the explicit first summary line, but still append the generated per-file descriptions below it line by line.
- If the changed files appear unrelated to each other, call that out before committing so the user can redirect if needed.

Use a structure like:

```text
feat: add region-manager entry selection flow
新增首页头像菜单里的切换版本入口
新增登录后的入口选择页
调整登录后默认跳转到 /entry
新增地区经理首页路由和权限判断
```

### 4. Create one commit

- Stage the current repository changes using a non-interactive git command.
- Create exactly one commit using the derived multi-line commit message or the user's explicit first line plus generated per-file lines.
- Use a non-interactive git command that preserves line breaks in the final commit message.
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
