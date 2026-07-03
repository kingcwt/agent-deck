# /kc-slim-review

<!-- This file is generated from skills/*/source.md. Edit the source file instead. -->

Execute the following workflow in the current working directory.
Treat this command as the user's explicit shortcut for the workflow below.

> Canonical source for this skill. Keep this file as the only executable source of truth.
> See `source.zh-CN.md` for the one-to-one Chinese translation used only for reading and understanding.

# Slim Review

## Description

Review code, git diffs, or a proposed implementation and identify the smallest safe path that still satisfies the current requirement.

This workflow is a read-only complexity review by default. It finds what can be deleted, reused, localized, or postponed. It does not weaken safety, data protection, comments, tests, or shared-code review rules.

## Parameters

- Required: none.
- Optional target: a file path, selected code, current diff, staged diff, pull request diff, or proposed design.
- Optional intent: the user may ask for review only, a minimal refactor plan, or applying fixes after the review.
- Default scope: review only the provided or current working diff. Do not expand to the whole repository unless explicitly requested.
- Not supported by default: automatic refactoring, public API redesign, database/schema changes, dependency changes, or shared package edits.

## Shortcuts And Commands

- Codex shortcuts: `$kc-sr`, `$kc-slim-review`
- Codex full commands: `$kc-sr [target-or-intent]`, `$kc-slim-review [target-or-intent]`
- Claude Code shortcuts: `/kc-sr`, `/kc-slim-review`
- Claude Code full commands: `/kc-sr [target-or-intent]`, `/kc-slim-review [target-or-intent]`

## Examples

### Codex

```text
$kc-sr
$kc-sr review current diff for over-engineering
$kc-slim-review this file
```

### Claude Code

```text
/kc-sr
/kc-sr review current diff for over-engineering
/kc-slim-review this file
```

## Workflow

### 1. Confirm scope and mode

- Treat `$kc-sr`, `$kc-slim-review`, `/kc-sr`, and `/kc-slim-review` as explicit triggers for this workflow.
- Default to read-only review. Do not edit files unless the user explicitly says to apply fixes.
- Identify the exact review target before judging. Use the current diff or provided file/code when available.
- If the target is unclear, ask for the path or diff instead of scanning unrelated files.
- If the user asks for a refactor, first produce a minimal refactor plan; only implement after explicit confirmation.

### 2. Read enough context

- Inspect the relevant diff or code first.
- Read nearby code and directly related helpers, types, components, imports, and call sites needed to judge reuse and scope.
- Search for existing utilities or patterns before claiming something is duplicated.
- Treat repo instructions, comments, and local conventions as binding evidence.
- Mark uncertainty clearly when intent or requirements are not proven by code, logs, tests, screenshots, or user-provided context.

### 3. Apply the minimal implementation ladder

For each change or proposed implementation, check this ladder in order:

1. Does this code need to exist for the current requirement?
2. Does the project already have a helper, component, type, pattern, or workflow that covers it?
3. Does the language standard library cover it?
4. Does the platform, browser, framework, database constraint, or native feature cover it?
5. Does an already-installed dependency cover it without adding a new dependency?
6. Can the same behavior be achieved with a smaller local change?
7. Only then accept the new abstraction, wrapper, config, dependency, or broader refactor.

### 4. Flag complexity smells

Look specifically for:

- Unrequested abstractions: one-implementation interfaces, factories, strategies, adapters, or generic layers.
- Speculative flexibility: options, config fields, extension points, feature flags, or callbacks nobody sets.
- Duplicate logic: code that should reuse an existing helper, component, type, or project pattern.
- Avoidable dependencies: new or heavy dependencies for behavior covered by stdlib, platform features, or existing packages.
- Shared-code overreach: edits to public helpers, packages, common types, configs, or shared components for a local requirement.
- Opportunistic churn: formatting-only changes, cleanup, renames, broad rewrites, or performance changes unrelated to the task.
- Large surface area: many files touched when a local change would satisfy the requirement.

### 5. Protect non-negotiables

Never recommend removing or weakening:

- Authorization, authentication, permission checks, or trust-boundary validation.
- Data-loss prevention, idempotency, transaction safety, migration safety, or rollback behavior.
- Error handling that preserves data integrity or gives required user feedback.
- Accessibility basics and platform compatibility required by the product.
- Existing tests or a small necessary test for non-trivial logic.
- Required comments that explain business intent, compatibility constraints, or key implementation reasons.
- Explicit user requirements, even if they are more complex than the minimal alternative.
- Project rules requiring confirmation before modifying shared code, packages, public types, database files, or config.

### 6. Decide review outcome

Classify each finding:

- `delete`: remove dead, speculative, or unrelated code.
- `reuse`: replace duplicate logic with an existing local helper, component, type, or pattern.
- `stdlib`: replace custom code with a standard-library feature.
- `native`: replace code or dependency with a platform, browser, framework, database, or built-in feature.
- `localize`: avoid changing shared/public code by adapting only the current module.
- `defer`: postpone speculative flexibility until a real second use case appears.
- `keep`: complexity is justified by evidence, safety, compatibility, or explicit requirements.

### 7. Report clearly

Use this output order:

1. `Scope`: what was reviewed and whether this is review-only or apply-fixes mode.
2. `Findings`: actionable items first, ordered by severity and confidence.
3. `Keep`: complexity that should stay because it protects safety, data, accessibility, compatibility, or explicit requirements.
4. `Minimal path`: the smallest safe implementation or refactor plan.
5. `Blocked or needs confirmation`: shared-code edits, database/config changes, or uncertain requirements that need user approval.

Each finding should include:

- file or code location when available
- current complexity
- smaller replacement
- why the replacement is safe
- what must not be removed

## Output Template

```text
Scope
- Reviewed: <target>
- Mode: review-only | apply-fixes requested

Findings
- <severity>: <location> <tag> <current complexity>. Smaller path: <replacement>. Keep: <non-negotiable guardrail>.

Keep
- <location or behavior>: keep because <evidence>.

Minimal path
- <smallest safe plan>

Blocked or needs confirmation
- <only if needed>
```

## Guardrails

- Do not edit code during the first pass unless the user explicitly requested implementation.
- Do not recommend modifying shared packages, public helpers, database schema, migrations, or shared config without calling out that confirmation is required.
- Do not claim a smaller path is safe without reading the relevant existing code or stating the uncertainty.
- Do not remove comments required by local project rules; improve stale comments instead.
- Do not turn this into a general correctness review. Mention correctness or security only when a proposed simplification would affect them.
- Do not prefer fewer lines over clearer necessary business logic.
