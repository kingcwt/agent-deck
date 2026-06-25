# /kc-pi

<!-- This file is generated from skills/*/source.md. Edit the source file instead. -->

Execute the following workflow in the current working directory.
Treat this command as the user's explicit shortcut for the workflow below.

> Canonical source for this skill. Keep this file as the only executable source of truth.
> See `source.zh-CN.md` for the one-to-one Chinese translation used only for reading and understanding.

# Init

## Description

Inspect the current project, verify dependencies, install only when needed, start the main local process, verify it, and summarize how the project runs.

## Parameters

- Required: none.
- Optional flags: none.
- Working scope: the current repository or workspace only.

## Shortcuts And Commands

- Codex shortcut: `$kc-pi`
- Codex full command: `$kc-pi`
- Claude Code shortcut: `/kc-pi`
- Claude Code full command: `/kc-pi`

## Examples

### Codex

```text
$kc-pi
```

### Claude Code

```text
/kc-pi
```

## Workflow

### 1. Inspect

- Read the top-level manifests, lockfiles, README files, env files, and primary config files before running anything substantial.
- Determine the project type, package manager, main scripts, likely entrypoint, default port, and whether private registries, local tarballs, or workspace packages are involved.
- Identify whether the repository already has dependency artifacts or generated files, then evaluate whether they match the manifests and lockfiles well enough to proceed without installation.

### 2. Dependency Check And Install

- Use the package manager implied by the lockfile or project scripts.
- Check whether dependencies appear current before installing. Use local evidence such as dependency directories, package-manager metadata, lockfiles, manifest timestamps, install-state files, and workspace package links when they exist.
- Skip installation when the dependency artifacts are present and appear consistent with the manifests and lockfiles. Record the evidence used for the skip.
- Install only when dependencies are missing, stale, inconsistent with the lockfile, or the start/verification step fails with a dependency-related error.
- When installation is needed, prefer lockfile-respecting commands such as `pnpm install --frozen-lockfile`, `npm ci`, or the closest equivalent.
- Preserve the existing registry configuration by default. If install fails because the configured registry is unreachable, report the exact failure and retry with a per-command registry override before editing config files.
- Allow normal setup hooks to run unless a specific hook is non-essential and blocks progress.

### 3. Start

- Choose the canonical local startup command from the project scripts and docs.
- Start the primary dev server or the most useful verification process for the current workspace.
- If sandbox restrictions prevent binding a port or making required network requests, ask for the necessary approval instead of mutating project config just to satisfy the environment.
- Capture the real URL, port, and any compile or runtime diagnostics.

### 4. Verify

- Wait for the first successful compile or ready signal.
- Run a lightweight verification step when possible, such as `curl -I`, a health endpoint, or a direct readiness message from the process output.
- Distinguish clearly between these outcomes:
  - the project is running successfully
  - the frontend is running but upstream APIs or intranet services are unavailable
  - dependency installation failed
  - the project started but compilation failed

### 5. Report

- Report the exact install command and start command used. If installation was skipped, explicitly say it was skipped and cite the dependency-state evidence.
- Report the verified local URL and port.
- Describe the project overall, including its purpose when inferable from docs/code, stack, key scripts, key config files, main business modules, and important runtime dependencies such as proxies or env-based endpoints.
- Call out blockers, caveats, and next actions without padding.
- End with a short final summary of the current run state and the most important next action, if any.

## Guardrails

- Treat `/kc-pi` as the user's explicit shortcut for this workflow.
- Modify as little as possible. Default to no application source edits during initialization.
- Treat this as a bootstrap and runtime-verification workflow, not as a refactor or cleanup pass.
- Do not touch databases, migrations, shared packages, or unrelated config unless the user explicitly asks.
- If the project relies on private networks, local services, or company intranet endpoints, state that clearly in the final output.
