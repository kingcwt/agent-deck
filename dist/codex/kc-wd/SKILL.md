---
name: kc-wd
description: Teach one English word or code identifier with Chinese meaning, part of speech, accurate Chinese pronunciation guide, IPA breakdown, memory analysis, and related extensions. Use when the user types /kc-wd, $kc-wd, kc-wd, asks how to read or remember a word, or sends a single standalone English word with no other intent.
---

> Canonical source for this skill. Keep this file as the only executable source of truth.
> See `source.zh-CN.md` for the one-to-one Chinese translation used only for reading and understanding.

# Word Drill

## Description

Teach one English word, phrase, or code identifier so a Chinese-speaking learner can understand its meaning, pronounce it, and remember it. This workflow is especially for unfamiliar vocabulary in code, documentation, terminal output, API names, and ordinary English.

## Parameters

- Required: one English word, phrase, or identifier.
- Optional context: surrounding code, sentence, or domain that affects meaning.
- If the user sends only one standalone English word and no other intent, treat it as an implicit request to run this workflow.
- If the input is a code identifier such as `drain_notifications`, split it into component words and teach the selected word first, then explain the whole identifier.

## Shortcuts And Commands

- Codex shortcut: `$kc-wd`
- Codex full command: `$kc-wd <word-or-identifier>`
- Claude Code shortcut: `/kc-wd`
- Claude Code full command: `/kc-wd <word-or-identifier>`
- Implicit mode: `<single English word>`

## Examples

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

## Workflow

### 1. Identify the target word

- Determine the exact target word from the user's message.
- For snake_case, camelCase, kebab-case, or API identifiers, split the identifier into words.
- If multiple words are present and the user did not specify one, explain the main unfamiliar word first and briefly connect the full phrase.
- If pronunciation or meaning depends on domain context, state the likely context and keep uncertainty explicit.

### 2. Start with Chinese meaning and part of speech

- Always put the Chinese translation first.
- Always state the part of speech immediately after the translation.
- Use beginner-friendly labels such as noun, verb, adjective, adverb, preposition, plural noun, past tense verb, or gerund.
- If the word has multiple common meanings, list only the meanings relevant to the user's context first, then add common secondary meanings.

Required shape:

```text
<word> = <Chinese meaning>
词性：<part of speech>
```

### 3. Provide accurate Chinese pronunciation guide

- Always include a Chinese homophonic pronunciation guide. Do not omit it.
- Make the guide practical for reading IPA, not a loose joke translation.
- Mark the stressed syllable clearly with uppercase letters, bold text, or `↑ 重读`.
- If British and American pronunciations differ meaningfully, give both.
- For plural, past tense, or derived forms, explain the ending sound separately.

Required shape:

```text
中文谐音：...
重音位置：...
```

### 4. Break down IPA

- Always provide IPA if the word is pronounceable English.
- Break IPA into syllables or sound groups.
- Explain each sound group in Chinese, including how the mouth/tongue roughly moves when helpful.
- Point out sounds that Chinese speakers often misread, such as /θ/, /ð/, /v/, /r/, /æ/, /ə/, /ʃ/, /tʃ/, /dʒ/, and plural endings /s/, /z/, /ɪz/.
- For code identifiers that are not a single pronounceable word, provide IPA for each component word.

Required shape:

```text
音标：/ ... /
拆解：
- /.../：...
- /.../：...
```

### 5. Analyze and extend the word

- Explain the word's structure: root, prefix, suffix, plural ending, tense ending, or compound parts when useful.
- Give memory hooks that connect sound, spelling, and meaning.
- Provide related words or common collocations.
- For every extension word, also include Chinese meaning, part of speech, and Chinese pronunciation guide.
- Keep extensions focused. Prefer 3 to 6 useful items, not a long vocabulary dump.

### 6. Explain usage in the current context

- If the word appears in code, explain why that word is used in the identifier or comment.
- If it appears in a sentence, translate the sentence naturally.
- For identifiers, explain the full identifier in plain Chinese after teaching component words.

### 7. Keep the answer clear and teachable

- Default to Chinese explanation.
- Be concise but do not skip the four required parts: translation and part of speech, Chinese pronunciation guide, IPA breakdown, and word analysis with extensions.
- If exact pronunciation cannot be confirmed, say it is the common pronunciation rather than presenting a guess as certain.

## Output Template

Use this shape unless the user's request clearly needs a shorter answer:

```text
<word> = <中文翻译>
词性：<词性>

读音
音标：/ ... /
中文谐音：...
重音位置：...

音标拆解
- /.../：...
- /.../：...

词义和记忆
- ...

延伸
- <related word> = <中文>；词性：<词性>；中文谐音：...

当前上下文
- ...
```

## Guardrails

- Do not answer a word-pronunciation request with only translation.
- Do not omit Chinese homophonic pronunciation.
- Do not omit part of speech.
- Do not omit IPA breakdown.
- Do not give extensions without pronunciation guides.
- Do not invent certainty when pronunciation or context is unclear.
