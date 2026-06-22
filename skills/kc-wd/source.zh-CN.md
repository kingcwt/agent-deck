# `source.md` 中文对照说明

本文件与 [source.md](./source.md) 一一对应。

约束说明：

- `source.md` 是唯一正式源文件，也是分发、渲染、安装时使用的英文源文件。
- 本文件只用于中文理解、学习和阅读，不用于渲染或安装。
- 不允许在本文件里单独新增一套逻辑。
- 如果 `source.md` 更新，本文件必须同步做对应翻译更新。
- 如果中文内容与英文源文件冲突，以 `source.md` 为准。

---

## Frontmatter 对照

### `name`

`kc-wd`

技能名，保持 `kc-` 短名，不翻译。

### `display_name`

`Word Drill`

显示名称，表示“单词训练”。

### `description`

含义：

讲解一个英文单词或代码标识符，必须包含中文释义、词性、准确中文谐音、音标拆解、记忆分析和相关延伸。适用于用户输入 `/kc-wd`、`$kc-wd`、`kc-wd`，询问某个单词怎么读/怎么记，或者只发送一个独立英文单词且没有其他意图的场景。

### `short_description`

`Learn a word's meaning and pronunciation [单词读音记忆]`

含义：

学习单词含义和读音，重点服务中文用户记忆。

### `default_prompt`

`Use $kc-wd to explain one English word with Chinese meaning, part of speech, IPA, pronunciation, and memory hooks.`

含义：

使用 `$kc-wd` 讲解一个英文单词，包含中文含义、词性、音标、读音和记忆方法。

### `codex_names`

`kc-wd`

表示 Codex 侧生成一个技能别名：`kc-wd`。

### `claude_skill_names`

`kc-wd`

表示 Claude skill 侧生成一个技能别名：`kc-wd`。

### `claude_commands`

`kc-wd`

表示 Claude command 侧生成一个命令别名：`/kc-wd`。

### `allow_implicit_invocation`

`true`

表示允许隐式触发：当用户只输入一个英文单词且没有其他意图时，也按这个技能处理。

---

# Word Drill

## Description

讲解一个英文单词、短语或代码标识符，让中文学习者能理解意思、读准读音并记住它。这个工作流尤其适合代码、文档、终端输出、API 名称和普通英文里的陌生词。

## Parameters

- 必填：一个英文单词、短语或标识符。
- 可选上下文：会影响含义的代码片段、句子或领域背景。
- 如果用户只发送一个独立英文单词且没有其他意图，默认按这个工作流处理。
- 如果输入是 `drain_notifications` 这样的代码标识符，先拆成组成单词，优先讲用户选中的词，再解释整个标识符。

## Shortcuts And Commands

- Codex 快捷键：`$kc-wd`
- Codex 完整命令：`$kc-wd <word-or-identifier>`
- Claude Code 快捷键：`/kc-wd`
- Claude Code 完整命令：`/kc-wd <word-or-identifier>`
- 隐式模式：`<单个英文单词>`

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

- 判断用户消息里的准确目标词。
- 对 snake_case、camelCase、kebab-case 或 API 标识符，先拆成单词。
- 如果有多个词而用户没有指定，先讲最可能陌生的核心词，再简单串起完整短语。
- 如果读音或意思依赖领域上下文，说明当前判断的上下文，并明确保留不确定性。

### 2. Start with Chinese meaning and part of speech

- 必须先给中文翻译。
- 翻译后必须立即标出词性。
- 使用适合初学者的词性标签，例如名词、动词、形容词、副词、介词、复数名词、过去式动词、动名词。
- 如果这个词有多个常见意思，先列和用户上下文相关的意思，再补充常见次要意思。

固定格式：

```text
<word> = <Chinese meaning>
词性：<part of speech>
```

### 3. Provide accurate Chinese pronunciation guide

- 必须提供中文谐音读法，不能省略。
- 谐音要服务于读音标，不能写成随意玩笑式翻译。
- 必须用大写、加粗或 `↑ 重读` 明确标出重读音节。
- 如果英式和美式读音有明显差异，两个都给。
- 如果是复数、过去式或派生形式，要单独解释结尾音。

固定格式：

```text
中文谐音：...
重音位置：...
```

### 4. Break down IPA

- 只要是可读的英文词，必须提供 IPA 音标。
- 按音节或发音组拆解 IPA。
- 用中文解释每个发音组，必要时说明嘴型、舌位或发音方式。
- 提醒中文用户容易读错的音，例如 /θ/、/ð/、/v/、/r/、/æ/、/ə/、/ʃ/、/tʃ/、/dʒ/，以及复数结尾 /s/、/z/、/ɪz/。
- 如果是代码标识符而不是单个可读单词，分别给每个组成单词的 IPA。

固定格式：

```text
音标：/ ... /
拆解：
- /.../：...
- /.../：...
```

### 5. Analyze and extend the word

- 在有帮助时解释词根、前缀、后缀、复数结尾、时态结尾或复合词结构。
- 给出能把声音、拼写和意思连起来的记忆方法。
- 提供相关词或常见搭配。
- 每个延伸词也必须包含中文意思、词性和中文谐音。
- 延伸要克制，优先给 3 到 6 个有用项，不要堆成长词表。

### 6. Explain usage in the current context

- 如果词出现在代码里，解释为什么这个词会用于该标识符或注释。
- 如果词出现在句子里，自然翻译整句。
- 对标识符，讲完组成词后，用中文解释整个标识符。

### 7. Keep the answer clear and teachable

- 默认用中文讲解。
- 保持精简，但不能跳过四个必选部分：翻译和词性、中文谐音、音标拆解、词义分析和带谐音的延伸。
- 如果无法确认精确读音，要说这是常见读法，不能把猜测说成确定事实。

## Output Template

除非用户明确要求更短，否则使用这个结构：

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

- 不要只给翻译就结束单词读音请求。
- 不要省略中文谐音。
- 不要省略词性。
- 不要省略音标拆解。
- 不要给没有谐音的延伸词。
- 在读音或上下文不明确时，不要伪装成已经确定。
