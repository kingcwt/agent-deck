# /kc-wh

<!-- This file is generated from skills/*/source.md. Edit the source file instead. -->

Execute the following workflow in the current working directory.
Treat this command as the user's explicit shortcut for the workflow below.

> Canonical source for this skill. Keep this file as the only executable source of truth.
> See `source.zh-CN.md` for the one-to-one Chinese translation used only for reading and understanding.

# Work Hours

## Description

Export the last 7 days of work-hour records grouped by day and by AM/PM into a Desktop markdown file, optionally filtered to selected projects, or add one manual work-hour record for today into the global agent-deck work-hour log.

## Parameters

- Default mode: no extra arguments, export the last 7 days including today.
- Filter mode: one bracket argument, `"[<project>,<project>]"`, export only matching projects from the last 7 days.
- Add mode: `add <project> -m"<message>" [-am|-pm]`.
- Optional `-am`: force the manual record into today's AM bucket.
- Optional `-pm`: force the manual record into today's PM bucket.

## Shortcuts And Commands

- Codex shortcut: `$kc-wh`
- Codex full commands: `$kc-wh`, `$kc-wh '[<project>,<project>]'`, `$kc-wh add <project> -m"<message>" [-am|-pm]`
- Claude Code shortcut: `/kc-wh`
- Claude Code full commands: `/kc-wh`, `/kc-wh '[<project>,<project>]'`, `/kc-wh add <project> -m"<message>" [-am|-pm]`

## Examples

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

## Workflow

### 1. Parse the invocation

- Treat `/kc-wh` and `$kc-wh` as explicit shortcuts for this workflow.
- If there is no trailing text after the shortcut, run export mode for the last 7 days including today.
- If the trailing text is one bracket argument such as `"[cmc-ai,nice]"`, parse it as export-filter mode and keep only records whose project exactly matches one of the listed names.
- If the trailing text starts with `add `, parse it as manual-add mode using `add <project> -m"<message>" [-am|-pm]`.
- If the arguments do not match any supported form, stop and report the supported command formats instead of guessing.

### 2. Use the global agent-deck work-hour installation

- The global storage root for this skill is `~/.agent-deck/workhours`.
- The executable CLI is `~/.agent-deck/workhours/workhours_cli.py`.
- The shared work-hour log is `~/.agent-deck/workhours/git-commit-log.txt`.
- If the CLI or log path is missing, tell the user to rerun this repository's `./scripts/sync.sh` or `./install.sh` so the global installation is recreated.

### 3. Run export mode

- In export mode, execute the global CLI with no extra arguments.
- In export-filter mode, execute the global CLI with the single quoted bracket argument, for example `"[cmc-ai,nice]"`.
- Export exactly the last 7 days including today: today plus the previous 6 calendar days in the local timezone.
- Project filtering must use exact project-name matching against the `project` value stored in the work-hour log.
- The exported markdown must show the date range in the title.
- When project filtering is used, the exported markdown must show the selected project names and the Desktop file name must include those project names.
- The export must always be written to a Desktop markdown file, not only printed into the chat reply.
- Group the output by day, and inside each day split records into `上午` and `下午`.
- For each record, show the project name plus the commit or manual message content.
- Under each `上午` or `下午` table, also render a `复制文本` plain text block that repeats each work-description line on its own line for quick copying.
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
