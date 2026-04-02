# Agent Deck

`agent-deck` is a single-source shortcut and skill repository for Codex and Claude Code.

You author each workflow once, then generate and install all required targets:

- Codex skills
- Claude Code skills
- Claude Code slash commands

Current repository: `https://github.com/kingcwt/agent-deck`

## What This Solves

Instead of repeatedly typing long prompts like “analyze the current project, install dependencies, start it, verify it, and summarize it,” you keep a short reusable command set such as:

- Codex: `$pi` or `$project-init`
- Claude Code: `/pi` or `/project-init`

The workflow itself lives in one source file and is rendered into the formats required by each tool.

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
- summarize the project structure and blockers

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
└── README.md
```

Meaning of each part:

- `skills/*/source.md`: the only file you manually maintain for a skill
- `scripts/render_skills.py`: generates publishable artifacts
- `scripts/sync.sh`: regenerates and installs locally
- `dist/`: generated output; commit this for public installs
- `install.sh`: one-command installer/updater for local or remote use

## Authoring Model

Each skill is defined once in `source.md`.

Example metadata:

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

This lets one workflow fan out into multiple aliases without duplicating the body.

## Local Development

Render and install locally:

```bash
cd ~/Desktop/agent-deck
./scripts/sync.sh
```

This will:

- rebuild `dist/`
- install Codex skills to `~/.codex/skills`
- install Claude skills to `~/.claude/skills`
- install Claude commands to `~/.claude/commands`

If you only want to regenerate artifacts without installing:

```bash
python3 ./scripts/render_skills.py
```

## Install

### Local checkout

Clone the repository and install/update:

```bash
git clone https://github.com/kingcwt/agent-deck.git
cd agent-deck
./install.sh
```

### Direct from GitHub

Install or update without manually cloning:

```bash
curl -fsSL https://raw.githubusercontent.com/kingcwt/agent-deck/main/install.sh | bash -s -- --repo kingcwt/agent-deck --ref main
```

`install.sh` is intentionally idempotent:

- first run = install
- later runs = update/overwrite with the latest repo state

## Update

If you already have a local checkout:

```bash
cd ~/Desktop/agent-deck
git pull
./install.sh
```

If you prefer the remote installer path, just run the same curl command again.

## Publish Workflow

When you change a skill:

1. edit `skills/*/source.md`
2. run `./scripts/sync.sh`
3. test in Codex and Claude Code
4. commit both the source files and the generated `dist/` files
5. push to GitHub

`dist/` is committed on purpose so:

- remote installs work consistently
- other users can inspect generated outputs
- skill catalogs and install tooling can consume the repository more easily

## Add a New Skill

1. create `skills/<new-skill>/source.md`
2. copy an existing source file as a base
3. update the metadata and workflow body
4. choose aliases:
   - `codex_names: foo,bar`
   - `claude_skill_names: foo,bar`
   - `claude_commands: foo,bar`
5. run `./scripts/sync.sh`
6. commit source and regenerated `dist/`

## Why Claude Has Both Skills And Commands

Claude Code supports reusable skills and slash commands, and they solve different problems:

- Claude skills help with reusable packaged capability
- Claude commands provide the shortest possible invocation UX, such as `/pi`

This repository emits both from the same source file so you do not maintain duplicate logic.

## Notes

- Codex works best with explicit skill invocation such as `$pi`
- Claude uses `/pi` and `/project-init`
- `/init` is intentionally avoided for Claude commands because it conflicts with Claude’s built-in command naming
- the repository is designed to scale to many skills without changing the overall structure
