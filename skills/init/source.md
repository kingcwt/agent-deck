---
name: init
display_name: Project Init
description: Initialize and baseline the current code project. Use when the user types /pi, /project-init, $pi, $project-init, pi, or asks to inspect the current repository, detect the stack and package manager, install dependencies, start the main local app or dev server, verify it is reachable, and output a detailed project description with startup notes, config dependencies, and blockers.
short_description: Inspect, install, run, and summarize a codebase
default_prompt: Use $pi to inspect the current project, install dependencies, start it, and summarize how it works.
codex_names: pi,project-init
claude_skill_names: pi,project-init
claude_commands: pi,project-init
allow_implicit_invocation: false
---

> Canonical source for this skill. Keep this file as the only executable source of truth.
> See `source.zh-CN.md` for the one-to-one Chinese translation used only for reading and understanding.

# Init

## Overview

Initialize the current project from inspection to a verified local run. Read the repo first, then install dependencies, start the primary local process, verify the result, and summarize what the project is and how it works.

## Workflow

### 1. Inspect

- Read the top-level manifests, lockfiles, README files, env files, and primary config files before running anything substantial.
- Determine the project type, package manager, main scripts, likely entrypoint, default port, and whether private registries, local tarballs, or workspace packages are involved.
- Identify whether the repository already has install artifacts or generated files, but do not assume they are valid until verification succeeds.

### 2. Install

- Use the package manager implied by the lockfile or project scripts.
- Prefer lockfile-respecting commands such as `pnpm install --frozen-lockfile`, `npm ci`, or the closest equivalent.
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

- Report the exact install command and start command used.
- Report the verified local URL and port.
- Summarize the stack, key scripts, key config files, main business modules, and important runtime dependencies such as proxies or env-based endpoints.
- Call out blockers, caveats, and next actions without padding.

## Guardrails

- Treat `/pi` and `/project-init` as the user's explicit shortcuts for this workflow.
- Modify as little as possible. Default to no application source edits during initialization.
- Treat this as a bootstrap and runtime-verification workflow, not as a refactor or cleanup pass.
- Do not touch databases, migrations, shared packages, or unrelated config unless the user explicitly asks.
- If the project relies on private networks, local services, or company intranet endpoints, state that clearly in the final output.
