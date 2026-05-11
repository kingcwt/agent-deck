---
name: kc-wh
description: Export recent work-hour records from the global agent-deck git commit log, or add a manual work-hour record for today. Use when the user types /kc-wh, /kc-work-hours, $kc-wh, $kc-work-hours, kc-wh, or asks to export recent work hours or append a manual work-hour note such as a meeting entry.
---

> Canonical source for this skill. Keep this file as the only executable source of truth.
> See `source.zh-CN.md` for the one-to-one Chinese translation used only for reading and understanding.

# Work Hours

## Description

Export the last 7 days of work-hour records grouped by day and by AM/PM into a Desktop markdown file, or add one manual work-hour record for today into the global agent-deck work-hour log.

## Parameters

- Default mode: no extra arguments, export the last 7 days including today.
- Add mode: `add <project> -m"<message>" [-am|-pm]`.
- Optional `-am`: force the manual record into today's AM bucket.
- Optional `-pm`: force the manual record into today's PM bucket.

## Shortcuts And Commands

- Codex shortcut: `$kc-wh`
- Codex full commands: `$kc-wh`, `$kc-wh add <project> -m"<message>" [-am|-pm]`
- Claude Code shortcut: `/kc-wh`
- Claude Code full commands: `/kc-wh`, `/kc-wh add <project> -m"<message>" [-am|-pm]`

## Examples

### Codex

```text
$kc-wh
$kc-wh add 其他 -m"开会1小时"
$kc-wh add 其他 -m"开会1小时" -am
$kc-wh add 其他 -m"需求评审" -pm
```

### Claude Code

```text
/kc-wh
/kc-wh add 其他 -m"开会1小时"
/kc-wh add 其他 -m"开会1小时" -am
/kc-wh add 其他 -m"需求评审" -pm
```

## Workflow

### 1. Parse the invocation

- Treat `/kc-wh` and `$kc-wh` as explicit shortcuts for this workflow.
- If there is no trailing text after the shortcut, run export mode for the last 7 days including today.
- If the trailing text starts with `add `, parse it as manual-add mode using `add <project> -m"<message>" [-am|-pm]`.
- If the arguments do not match either supported form, stop and report the supported command formats instead of guessing.

### 2. Use the global agent-deck work-hour installation

- The global storage root for this skill is `~/.agent-deck/workhours`.
- The executable CLI is `~/.agent-deck/workhours/workhours_cli.py`.
- The shared work-hour log is `~/.agent-deck/workhours/git-commit-log.txt`.
- If the CLI or log path is missing, tell the user to rerun this repository's `./scripts/sync.sh` or `./install.sh` so the global installation is recreated.

### 3. Run export mode

- In export mode, execute the global CLI with no extra arguments.
- Export exactly the last 7 days including today: today plus the previous 6 calendar days in the local timezone.
- The exported markdown must show the date range in the title.
- The export must always be written to a Desktop markdown file, not only printed into the chat reply.
- Group the output by day, and inside each day split records into `上午` and `下午`.
- For each record, show the project name plus the commit or manual message content.
- If one record contains multiple message lines, preserve those lines in the exported file instead of collapsing them into one flat line.

### 4. Run manual-add mode

- In add mode, execute the global CLI with the parsed `add` arguments.
- Preserve the user-provided project and message exactly, except for normal shell-safe quoting when running the command.
- If `-am` is passed, write the record into today's AM bucket.
- If `-pm` is passed, write the record into today's PM bucket.
- If neither `-am` nor `-pm` is passed, let the CLI decide AM or PM from the current local time.

### 5. Report the result

- For export mode, report the Desktop file path and return the generated markdown content.
- For add mode, report the project, message, and whether the record was written into today's AM or PM bucket.
- If execution fails, report the exact blocking error without padding.

## Guardrails

- This workflow is only for exporting recent work-hour records or appending one manual record.
- Do not modify application source code as part of this workflow.
- Do not read or write the old `~/.workhours` storage used by unrelated legacy tools.
- Do not invent records when the global log is empty or missing.
- Do not broaden the date range unless the skill definition is explicitly changed.
