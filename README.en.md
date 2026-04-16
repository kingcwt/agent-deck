# Agent Deck

[阅读中文说明 / Read the Chinese version](./README.md)

`agent-deck` is a single-source skill repository for Codex and Claude Code.

You define a workflow once and generate installable targets for:

- Codex skills
- Claude Code skills
- Claude Code slash commands

Repository: `https://github.com/kingcwt/agent-deck`

## What This Repository Solves

You do not need to repeatedly type long prompts such as “analyze the current project, install dependencies, start it, verify it, and summarize it.”

Instead, you keep a short command set such as:

- Codex: `$pi` or `$project-init`
- Claude Code: `/pi` or `/project-init`

The workflow is authored once in a source file and rendered into the formats required by each tool.

## Current Skill Set

### `init`

Project bootstrap and baseline analysis.

Aliases generated from one source:

- Codex skills: `pi`, `project-init`
- Claude skills: `pi`, `project-init`
- Claude commands: `/pi`, `/project-init`

Purpose:

- inspect the current project
- detect the package manager and runtime shape
- install dependencies
- start the main local app or dev server
- verify readiness
- summarize the project structure, stack, and blockers

## Repository Structure

```text
agent-deck/
├── skills/
│   └── init/
│       └── source.md
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

- `skills/*/source.md`: the only manually maintained source file for a skill
- `scripts/render_skills.py`: renders source files into publishable artifacts
- `scripts/sync.sh`: regenerates and installs artifacts into local Codex / Claude directories
- `dist/`: generated output; commit it for remote installs and public distribution
- `install.sh`: one-command installer/updater for local or remote use
- `README.md`: default Chinese documentation
- `README.en.md`: English documentation

## Authoring Model

Each skill is defined exactly once in `source.md`.

Metadata example:

```md
---
name: init
display_name: Project Init
description: ...
short_description: ...
default_prompt: ...
codex_names: pi,project-init
claude_skill_names: pi,project-init
claude_commands: pi,project-init
allow_implicit_invocation: false
---
```

This lets one workflow expand into multiple aliases without duplicating the body.

## Local Development

Render and install locally:

```bash
cd ~/Desktop/kingcwt/work/agent-deck
./scripts/sync.sh
```

This command will:

- rebuild `dist/`
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
2. run `./scripts/sync.sh`
3. test in Codex and Claude Code
4. commit both the source files and generated `dist/`
5. push to GitHub

`dist/` is committed on purpose because:

- remote installs are more reliable
- other users can inspect the generated outputs directly
- skill catalogs and install tooling can consume the repository more easily

## Add a New Skill

1. create `skills/<new-skill>/source.md`
2. copy an existing skill as a template
3. update metadata and body
4. choose aliases:
   - `codex_names: foo,bar`
   - `claude_skill_names: foo,bar`
   - `claude_commands: foo,bar`
5. run `./scripts/sync.sh`
6. commit source and regenerated `dist/`

## Why Claude Has Both Skills And Commands

Claude Code supports both reusable skills and slash commands, and they serve different purposes:

- Claude skills are for reusable packaged capability
- Claude commands provide the shortest invocation path, such as `/pi`

This repository generates both from the same source file, so you do not maintain duplicate logic.

## Notes

- Codex works best with explicit skill invocation such as `$pi`
- Claude uses `/pi` and `/project-init`
- `/init` is intentionally avoided on the Claude command side because it can conflict with built-in command semantics
- the repository structure is designed to scale to many skills without structural changes
