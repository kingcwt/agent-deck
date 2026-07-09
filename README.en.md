# Agent Deck

[阅读中文说明 / Read the Chinese version](./README.md)

`agent-deck` is a single-source skill repository for Codex and Claude Code.

You define a workflow once and generate installable targets for:

- Codex skills
- Claude Code skills
- Claude Code slash commands

Repository: `https://github.com/kingcwt/agent-deck`

## What This Repository Solves

You do not need to repeatedly type long prompts such as “analyze the current project, verify dependencies, install only if needed, start it, verify it, and summarize it.”

Instead, you keep a short command set such as:

- Codex: `$kc-pi`
- Claude Code: `/kc-pi`

The workflow is authored once in a source file and rendered into the formats required by each tool.

## Current Skill Set

This block is auto-synced by `scripts/render_skills.py` from `skills/*/source.md` and `skills/*/source.zh-CN.md`.

<!-- BEGIN GENERATED SKILLS -->
### `active-memory`

Description:

Write the most recent completed user-assistant exchange into the current project's `active-memory.md` as one structured memory entry.

Parameters:

- Required: none.
- Source scope: the most recent completed user-assistant exchange before the shortcut invocation.
- Output file: the project root `active-memory.md`.
- Optional flags: none.

Shortcuts And Commands:

- Codex shortcut: `$kc-am`
- Codex full command: `$kc-am`
- Claude Code shortcut: `/kc-am`
- Claude Code full command: `/kc-am`

Examples:

### Codex

```text
$kc-am
```

### Claude Code

```text
/kc-am
```

### `diff-review`

Description:

Review only the current file's git changes, explain what each change is doing, and judge whether the change is necessary and minimal.

Parameters:

- Required: none.
- Review target: exactly one current file with git changes.
- Optional flags: none.
- Not supported by default: repository-wide diff review, multi-file batching, or automatic code fixes.

Shortcuts And Commands:

- Codex shortcuts: `$df`, `$diff-review`
- Codex full commands: `$df`, `$diff-review`
- Claude Code shortcuts: `/df`, `/diff-review`
- Claude Code full commands: `/df`, `/diff-review`

Examples:

### Codex

```text
$df
$diff-review
```

### Claude Code

```text
/df
/diff-review
```

### `git-diff-description`

Description:

Read the current repository diff and output a concise Chinese review of the changed files: what each file changed, whether the implementation can be smaller, and whether the changes may affect other modules or logic.

Parameters:

- Required: none.
- Optional language: Chinese by default; use English only when the user explicitly asks for English.
- Output: concise per-file change summaries plus review findings, minimal-implementation suggestions, and impact notes.

Shortcuts And Commands:

- Codex shortcut: `$kc-gdd`
- Codex full command: `$kc-gdd`
- Claude Code shortcut: `/kc-gdd`
- Claude Code full command: `/kc-gdd`

Examples:

### Codex

```text
$kc-gdd
```

### Claude Code

```text
/kc-gdd
```

### `git-diff-description-push`

Description:

Read the current repository diff, generate one short description per changed file when no custom message is provided, build a commit message, then commit and push the current branch. Generated descriptions default to Chinese, and switch to English only when `-e` is passed.

Parameters:

- Required: none.
- Optional `-e`: switch generated descriptions and summary line to English.
- Optional `[commit message]`: when any non-empty text follows the shortcut, use all remaining text as the complete commit message.
- Supported format: `[-e] [commit message]`.

Shortcuts And Commands:

- Codex shortcut: `$kc-gdp`
- Codex full command: `$kc-gdp [-e] [commit message]`
- Claude Code shortcut: `/kc-gdp`
- Claude Code full command: `/kc-gdp [-e] [commit message]`

Examples:

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

### `git-push`

Description:

Commit the current repository changes with a required description, then push the current branch to the configured remote.

Parameters:

- Required: `<description>`, used as the commit message.
- Optional flags: none.
- Not supported by default: `--amend`, force-push, branch switching, or splitting into multiple commits.

Shortcuts And Commands:

- Codex shortcut: `$kc-gp`
- Codex full command: `$kc-gp <description>`
- Claude Code shortcut: `/kc-gp`
- Claude Code full command: `/kc-gp <description>`

Examples:

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

### `init`

Description:

Inspect the current project, verify dependencies, install only when needed, start the main local process, verify it, and summarize how the project runs.

Parameters:

- Required: none.
- Optional flags: none.
- Working scope: the current repository or workspace only.

Shortcuts And Commands:

- Codex shortcut: `$kc-pi`
- Codex full command: `$kc-pi`
- Claude Code shortcut: `/kc-pi`
- Claude Code full command: `/kc-pi`

Examples:

### Codex

```text
$kc-pi
```

### Claude Code

```text
/kc-pi
```

### `kc-slim-review`

Description:

Review code, git diffs, or a proposed implementation and identify the smallest safe path that still satisfies the current requirement.

This workflow is a read-only complexity review by default. It finds what can be deleted, reused, localized, or postponed. It does not weaken safety, data protection, comments, tests, or shared-code review rules.

Parameters:

- Required: none.
- Optional target: a file path, selected code, current diff, staged diff, pull request diff, or proposed design.
- Optional intent: the user may ask for review only, a minimal refactor plan, or applying fixes after the review.
- Default scope: review only the provided or current working diff. Do not expand to the whole repository unless explicitly requested.
- Not supported by default: automatic refactoring, public API redesign, database/schema changes, dependency changes, or shared package edits.

Shortcuts And Commands:

- Codex shortcuts: `$kc-sr`, `$kc-slim-review`
- Codex full commands: `$kc-sr [target-or-intent]`, `$kc-slim-review [target-or-intent]`
- Claude Code shortcuts: `/kc-sr`, `/kc-slim-review`
- Claude Code full commands: `/kc-sr [target-or-intent]`, `/kc-slim-review [target-or-intent]`

Examples:

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

### `kc-ui`

Description:

List, inspect, and apply curated UI style presets to the current project. This skill is a style library and execution workflow for web, desktop, and mobile interfaces, not a single fixed template.

Parameters:

- Required for applying UI changes: an explicit built-in style id and a UI task.
- Optional for listing: no parameters.
- Optional for inspection: one built-in style id.
- Current built-in style id: `agency-compact`.
- If the user asks for a generic style such as dark, minimal, Apple-like, compact, or native without naming a style id, do not edit code. List available style ids with one-line descriptions and ask the user to rerun with an explicit style id.
- If the style id is unknown, do not edit code. List available style ids and show the expected command shape.

Shortcuts And Commands:

- Codex list command: `$kc-ui list`
- Codex inspect command: `$kc-ui look <style-id>`
- Codex apply command: `$kc-ui use <style-id> <task>`
- Codex shorthand apply command: `$kc-ui <style-id> <task>`
- Claude Code list command: `/kc-ui list`
- Claude Code inspect command: `/kc-ui look <style-id>`
- Claude Code apply command: `/kc-ui use <style-id> <task>`
- Claude Code shorthand apply command: `/kc-ui <style-id> <task>`

Examples:

### Codex

```text
$kc-ui list
$kc-ui look agency-compact
$kc-ui use agency-compact redesign the settings page
$kc-ui agency-compact adjust the whole project UI
```

### Claude Code

```text
/kc-ui list
/kc-ui look agency-compact
/kc-ui use agency-compact redesign the settings page
/kc-ui agency-compact adjust the whole project UI
```

### Ambiguous request

```text
$kc-ui make the settings page dark and minimal
```

Expected behavior: do not edit code. Show the available style ids and ask the user to choose one explicitly, for example `$kc-ui use agency-compact make the settings page dark and minimal`.

### `kc-wd`

Description:

Teach one English word, phrase, or code identifier so a Chinese-speaking learner can understand its meaning, pronounce it, and remember it. This workflow is especially for unfamiliar vocabulary in code, documentation, terminal output, API names, and ordinary English.

Parameters:

- Required: one English word, phrase, or identifier.
- Optional context: surrounding code, sentence, or domain that affects meaning.
- If the user sends only one standalone English word and no other intent, treat it as an implicit request to run this workflow.
- If the input is a code identifier such as `drain_notifications`, split it into component words and teach the selected word first, then explain the whole identifier.

Shortcuts And Commands:

- Codex shortcut: `$kc-wd`
- Codex full command: `$kc-wd <word-or-identifier>`
- Claude Code shortcut: `/kc-wd`
- Claude Code full command: `/kc-wd <word-or-identifier>`
- Implicit mode: `<single English word>`

Examples:

### Codex

```text
$kc-wd notifications
$kc-wd drain_notifications
notifications
```

### Claude Code

```text
/kc-wd notifications
/kc-wd drain_notifications
notifications
```

### `work-hours`

Description:

Export the last 7 days of work-hour records grouped by day and by AM/PM into a Desktop markdown file, optionally filtered to selected projects, or add one manual work-hour record for today into the global agent-deck work-hour log.

Parameters:

- Default mode: no extra arguments, export the last 7 days including today.
- Filter mode: one bracket argument, `"[<project>,<project>]"`, export only matching projects from the last 7 days.
- Add mode: `add <project> -m"<message>" [-am|-pm]`.
- Optional `-am`: force the manual record into today's AM bucket.
- Optional `-pm`: force the manual record into today's PM bucket.

Shortcuts And Commands:

- Codex shortcut: `$kc-wh`
- Codex full commands: `$kc-wh`, `$kc-wh '[<project>,<project>]'`, `$kc-wh add <project> -m"<message>" [-am|-pm]`
- Claude Code shortcut: `/kc-wh`
- Claude Code full commands: `/kc-wh`, `/kc-wh '[<project>,<project>]'`, `/kc-wh add <project> -m"<message>" [-am|-pm]`

Examples:

### Codex

```text
$kc-wh
$kc-wh '[cmc-ai,nice]'
$kc-wh add 其他 -m"开会1小时"
$kc-wh add 其他 -m"开会1小时" -am
$kc-wh add 其他 -m"需求评审" -pm
```

### Claude Code

```text
/kc-wh
/kc-wh '[cmc-ai,nice]'
/kc-wh add 其他 -m"开会1小时"
/kc-wh add 其他 -m"开会1小时" -am
/kc-wh add 其他 -m"需求评审" -pm
```
<!-- END GENERATED SKILLS -->

## Repository Structure

```text
agent-deck/
├── skills/
│   └── <skill-name>/
│       ├── source.md
│       └── source.zh-CN.md
├── scripts/
│   ├── render_skills.py
│   └── sync.sh
├── dist/
│   ├── codex/
│   └── claude/
├── install.sh
├── README.md
└── README.en.md
```

Directory meanings:

- `skills/*/source.md`: the executable source of truth for a skill
- `skills/*/source.zh-CN.md`: the paired Chinese reading translation
- `scripts/render_skills.py`: renders source files into publishable artifacts
- `scripts/sync.sh`: regenerates and installs artifacts into local Codex / Claude directories
- `dist/`: generated output; commit it for remote installs and public distribution
- `install.sh`: one-command installer/updater for local or remote use
- `README.md`: default Chinese documentation
- `README.en.md`: English documentation

## Authoring Model

Each skill is defined exactly once for execution in `source.md`, with a paired reading translation in `source.zh-CN.md`.

Metadata example:

```md
---
name: init
display_name: Project Init
description: ...
short_description: ...
default_prompt: ...
codex_names: kc-pi
claude_skill_names: kc-pi
claude_commands: kc-pi
allow_implicit_invocation: false
---
```

This lets one workflow expand into multiple aliases without duplicating the body.

The README skill catalog is generated from those source documents instead of being maintained by hand.

## Local Development

Render and install locally:

```bash
cd ~/Desktop/kingcwt/work/agent-deck
./scripts/sync.sh
```

This command will:

- rebuild `dist/`
- refresh the skill catalogs inside `README.md` and `README.en.md`
- install Codex skills to `~/.codex/skills`
- install Claude skills to `~/.claude/skills`
- install Claude commands to `~/.claude/commands`

If you only want to regenerate artifacts without installing:

```bash
python3 ./scripts/render_skills.py
```

## Install

### Install from a local checkout

```bash
git clone https://github.com/kingcwt/agent-deck.git
cd agent-deck
./install.sh
```

### Install directly from GitHub

```bash
curl -fsSL https://raw.githubusercontent.com/kingcwt/agent-deck/main/install.sh | bash -s -- --repo kingcwt/agent-deck --ref main
```

`install.sh` is intentionally idempotent:

- first run = install
- later runs = update and overwrite with the latest version

## Update

If you already have a local checkout:

```bash
cd ~/Desktop/kingcwt/work/agent-deck
git pull
./install.sh
```

If you use the remote installer path, simply run the same `curl ... | bash` command again.

## Publish Workflow

When you change a skill:

1. edit `skills/*/source.md`
2. update the matching `skills/*/source.zh-CN.md`
3. run `./scripts/sync.sh`
4. test in Codex and Claude Code
5. commit the source files, refreshed README files, and generated `dist/`
6. push to GitHub

`dist/` is committed on purpose because:

- remote installs are more reliable
- other users can inspect the generated outputs directly
- skill catalogs and install tooling can consume the repository more easily

## Add a New Skill

1. create `skills/<new-skill>/source.md`
2. create the matching `skills/<new-skill>/source.zh-CN.md`
3. copy an existing skill as a template
4. update metadata and body
5. choose aliases:
   - `codex_names: foo,bar`
   - `claude_skill_names: foo,bar`
   - `claude_commands: foo,bar`
6. run `./scripts/sync.sh`
7. commit source, refreshed README files, and regenerated `dist/`

## Why Claude Has Both Skills And Commands

Claude Code supports both reusable skills and slash commands, and they serve different purposes:

- Claude skills are for reusable packaged capability
- Claude commands provide the shortest invocation path, such as `/kc-pi`

This repository generates both from the same source file, so you do not maintain duplicate logic.

## Notes

- Codex works best with explicit skill invocation such as `$kc-pi`
- Claude uses `/kc-pi`
- `/init` is intentionally avoided on the Claude command side because it can conflict with built-in command semantics
- the repository structure is designed to scale to many skills without structural changes
