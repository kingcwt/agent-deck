---
name: active-memory
display_name: Active Memory
description: Summarize the most recent completed user-assistant exchange into a structured memory entry and append it to the current project's root active-memory.md file. Use when the user types /kc-am, $kc-am, kc-am, or asks to organize the last conversation into a persistent project memory note.
short_description: Write the last Q&A into project memory [把上一轮问答写入项目记忆]
default_prompt: Use $kc-am to summarize the most recent completed user-assistant exchange and append it as a structured entry in the project's root active-memory.md file.
codex_names: kc-am
claude_skill_names: kc-am
claude_commands: kc-am
allow_implicit_invocation: false
---

> Canonical source for this skill. Keep this file as the only executable source of truth.
> See `source.zh-CN.md` for the one-to-one Chinese translation used only for reading and understanding.

# Active Memory

## Overview

Take the most recent completed user-assistant exchange, convert it into one structured memory entry, then write that entry into `active-memory.md` at the current project root. If the file does not exist, create it. If it already exists, append a new entry at the end.

## Workflow

### 1. Locate the memory file

- Treat `/kc-am` and `$kc-am` as explicit shortcuts for this workflow.
- Resolve the current project root first.
- Use `active-memory.md` in that root as the canonical memory file.
- If `active-memory.md` does not exist, create it in the project root.
- If it already exists, read enough of the file to determine the next sequence number before appending.

### 2. Choose the source exchange

- Use the most recent completed user-assistant exchange before the current shortcut invocation as the source material.
- The `original question` must preserve the user's source question as written, except for trimming obvious surrounding noise like the current shortcut invocation.
- The `question` field must be a shorter, cleaned-up restatement of the user's real question or intent.
- The `description` field must summarize the assistant's answer in a structured and easy-to-scan form.
- If there is no clear prior exchange to summarize, say so plainly and stop instead of inventing one.

### 3. Build one structured entry

- Write one entry per invocation.
- Use the local current time at write time.
- Number entries sequentially as `1`, `2`, `3`, and so on based on existing content in `active-memory.md`.
- Use this exact markdown structure and field order:

```md
## 时间：YYYY-MM-DD HH:mm:ss

> 原始问题：...

## N. ...

## 描述：

### 1. ...

### 2. ...

### 3. ...
```

- Render the time line as an H2 heading using `## `.
- Render the original question line as a blockquote using `> `.
- Render the cleaned question line as an H2 heading using `## `, followed by the sequence number and question title only.
- Do not include the literal label `序号 问题：` in the written entry.
- Render the `描述：` line as an H2 heading using `## `.
- Render each description point as an H3 heading using `### `.
- Keep the cleaned `question` short and focused.
- In `description`, break the answer into clear numbered points instead of one long paragraph.
- Preserve concrete technical nouns, commands, file names, decisions, constraints, and next steps when they are part of the answer.
- Do not pad the entry with generic commentary.

### 4. Append safely

- If the file is empty, write the entry directly.
- If the file already contains entries, first append a separator line `-----`, then add one blank line, then write the new entry.
- Keep the separator on its own line so adjacent records do not visually blend together.
- Do not rewrite or reorder prior entries unless the user explicitly asks.
- Do not create additional memory files or move the canonical file elsewhere.

### 5. Report the result

- Report which file was written.
- Report the sequence number used.
- Report the cleaned question title that was recorded.
- If writing fails, report the exact blocking error.

## Guardrails

- This workflow is for recording project memory, not for answering a new question from scratch.
- Do not summarize the current shortcut invocation itself unless the user explicitly says that is the exchange to record.
- Do not invent missing user intent or assistant conclusions.
- Do not silently skip the file existence check or the sequence-number check.
- Keep the memory entry concise, structured, and useful for later retrieval.
