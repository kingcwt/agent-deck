---
name: git-push
display_name: Git Push
description: Run the repository-required lint and quality checks, then commit the current repository changes with a required user-provided description and push only when every required check passes. Use when the user types /kc-gp followed by a non-empty description, $kc-gp followed by a non-empty description, kc-gp followed by a non-empty description, or asks to validate, commit, and push the current repository changes.
short_description: Validate, commit, and push [检查通过后提交推送]
default_prompt: Use $kc-gp <description> to inspect the current changes, run all repository-required lint and quality checks against the final state, and create and push one commit only if every required check passes.
codex_names: kc-gp
claude_skill_names: kc-gp
claude_commands: kc-gp
allow_implicit_invocation: false
---

> Canonical source for this skill. Keep this file as the only executable source of truth.
> See `source.zh-CN.md` for the one-to-one Chinese translation used only for reading and understanding.

# Git Push

## Description

Run the repository-required lint and quality checks, then commit the current repository changes with a required description and push the current branch only when every required check passes.

## Parameters

- Required: `<description>`, used as the commit message.
- Optional flags: none.
- Not supported by default: `--amend`, force-push, branch switching, or splitting into multiple commits.

## Shortcuts And Commands

- Codex shortcut: `$kc-gp`
- Codex full command: `$kc-gp <description>`
- Claude Code shortcut: `/kc-gp`
- Claude Code full command: `/kc-gp <description>`

## Examples

### Codex

```text
$kc-gp fix login redirect after auth refresh
$kc-gp feat: add region-manager entry selection page
```

### Claude Code

```text
/kc-gp fix login redirect after auth refresh
/kc-gp chore: sync generated skill docs
```

## Workflow

### 1. Require a commit description

- Treat `/kc-gp` and `$kc-gp` as explicit shortcuts for this workflow.
- Require non-empty trailing text after the shortcut. Treat that trailing text as the commit description and default commit message source.
- If the user does not provide a description, stop and ask for it instead of inventing one.
- Preserve the user's intent in the commit message. Only tighten wording when the original text is too vague to function as a commit message, and say so explicitly.

### 2. Inspect the repository state

- Read `git status --short`, the current branch name, and the configured remotes before mutating anything.
- Read repository-local instruction files and the project manifests, task definitions, and CI configuration that define the required validation commands before deciding which checks to run.
- Summarize which files are changed, whether changes are already staged, and which branch will be pushed.
- If there are no local changes, say so plainly and stop.
- If there is no usable remote or the current branch cannot be pushed yet, explain the blocker and stop before creating a commit.

### 3. Protect scope before committing

- Treat this workflow as an explicit “commit and push what is currently in this repository” action.
- By default, stage the current repository changes with one commit. Do not silently drop files from the commit set.
- If the worktree contains changes that appear unrelated to the user's stated intent, call that out before committing so the user can redirect if needed.
- Do not rewrite history, amend prior commits, force-push, or switch branches unless the user explicitly asks.

### 4. Pass the mandatory quality gate

- Treat the complete, final working-tree content intended for the commit as the validation target.
- Discover the applicable commands from repository-local instructions such as `AGENTS.md` or `CLAUDE.md`, package scripts, Makefiles or task runners, and CI configuration. Use the repository's actual commands instead of inventing a generic command.
- Run lint for every affected application or package that provides a lint command. If the repository defines build, typecheck, or another command as its lint validation, run that exact command.
- Also run every typecheck, test, build, or other quality check that repository instructions require for the changed scope. Never treat reviewing the diff as a replacement for executable validation.
- Respect explicit repository restrictions on commands. When a required command is forbidden, use only an explicitly documented equivalent; if no allowed equivalent exists, stop before staging and report that validation is blocked.
- Run `git diff --check` in addition to the repository-defined checks so whitespace errors are caught before staging.
- Require a successful exit status from every required command. If any check fails, cannot run, or cannot be identified reliably, stop before staging, committing, or pushing and report the exact blocker.
- Do not bypass this gate with `--no-verify`, by disabling or weakening lint rules, by adding ignores solely to hide failures, or because the user asks to skip validation.
- Do not repair application code inside this commit-and-push workflow. Report the failure and wait for a separate fix request.
- If any file changes after validation, rerun all checks affected by that change. Only the exact successfully validated state may be staged and committed.

### 5. Create the commit

- Stage the repository changes using a non-interactive git command.
- Create exactly one commit using the provided description as the commit message.
- If commit hooks fail, report the failure and stop. Never bypass hooks.
- If git rejects the commit because identity is missing or the index is empty, report the exact blocker and stop.

### 6. Push safely

- Push the current branch to its configured upstream when one exists.
- If the branch has no upstream but `origin` exists, push with upstream setup using the current branch name.
- If push is rejected because the remote has new commits, report that clearly and stop instead of forcing the push.
- If network or permission approval is required in the environment, request it rather than pretending the push succeeded.

### 7. Report the result

- Report the commit message used.
- Report the branch and remote target that were pushed.
- Report the resulting commit hash when available.
- If any step fails, report the exact failing step and the blocking error without padding.

## Guardrails

- This workflow is for explicit commit-and-push execution, not for code review or cleanup.
- Do not edit application code as part of this workflow unless the user separately asks for fixes.
- Do not create multiple commits from one invocation.
- Do not push to a different branch than the current branch unless the user explicitly asks.
- Never commit or push when required validation has failed, was skipped, could not run, or no longer matches the current file state.
- Never bypass commit hooks or the mandatory quality gate.
- Do not fabricate success. Verification must come from the actual git command results.
