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

`git-push`

技能名，保持英文短名，不翻译。

### `display_name`

`Git Push`

显示名称，表示“提交并推送 Git 改动”。

### `description`

含义：

使用用户提供且必填的描述信息，把当前仓库改动提交并推送到远程仓库。适用于用户输入带有非空描述的 `/kc-gp`、带有非空描述的 `$kc-gp`、带有非空描述的 `kc-gp`，或者明确要求“暂存当前仓库改动、创建一次 git 提交、并把当前分支推送到远程”的场景。

### `short_description`

`Stage, commit, and push the current repo changes with a required description`

含义：

必须带描述地暂存、提交并推送当前仓库改动。

### `default_prompt`

`Use $kc-gp <description> to stage the current repository changes, create one commit from the provided description, and push the current branch to its remote.`

含义：

使用 `$kc-gp <description>` 暂存当前仓库改动，用提供的描述创建一次提交，并把当前分支推送到远程。

### `codex_names`

`kc-gp`

表示 Codex 侧生成一个技能别名：`kc-gp`。

### `claude_skill_names`

`kc-gp`

表示 Claude skill 侧生成一个技能别名：`kc-gp`。

### `claude_commands`

`kc-gp`

表示 Claude command 侧生成一个命令别名：`/kc-gp`。

### `allow_implicit_invocation`

`false`

表示默认不允许隐式注入，优先要求显式调用。

---

# Git Push

## Description

把当前仓库改动用必填描述创建一次提交，然后把当前分支推送到已配置远程。

## Parameters

- 必填：`<description>`，作为 commit message 使用。
- 可选参数：无。
- 默认不支持：`--amend`、强推、切分支、把改动拆成多个提交。

## Shortcuts And Commands

- Codex 快捷键：`$kc-gp`
- Codex 完整命令：`$kc-gp <description>`
- Claude Code 快捷键：`/kc-gp`
- Claude Code 完整命令：`/kc-gp <description>`

## Examples

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

## Workflow

### 1. Require a commit description

- 把 `/kc-gp` 和 `$kc-gp` 视为这个工作流的显式快捷触发词。
- 要求快捷词后面必须跟非空文本，并把这段文本视为提交说明和默认的 commit message 来源。
- 如果用户没有提供描述，必须停止并要求补充，不能自己编造。
- 提交信息要尽量保留用户原意。只有当原文过于含糊、不能作为 commit message 使用时，才允许做收紧处理，并且要明确说明。

### 2. Inspect the repository state

- 在执行任何修改前，先读取 `git status --short`、当前分支名和已配置的远程信息。
- 简洁说明哪些文件有改动、是否已经存在 staged 改动，以及接下来准备推哪个分支。
- 如果本地没有任何改动，直接说明并停止。
- 如果没有可用远程，或者当前分支暂时不能推送，必须先说明阻塞原因，再停止，不能先创建提交。

### 3. Protect scope before committing

- 把这个工作流视为用户显式发起的“提交并推送当前仓库现有改动”动作。
- 默认将当前仓库改动作为一次提交进行暂存，不要静默遗漏文件。
- 如果工作区里存在看起来与用户意图不一致的改动，要先指出这一点，再继续提交，避免误推。
- 除非用户明确要求，否则不要改历史、不要 amend、不要 force push、不要切分支。

### 4. Create the commit

- 使用非交互式 git 命令暂存仓库改动。
- 使用提供的描述创建且只创建一个提交。
- 如果 commit hook 失败，必须报告失败并停止；除非用户明确要求，否则不要绕过 hook。
- 如果因为 git 身份未配置或 index 为空导致提交失败，必须精确说明阻塞点并停止。

### 5. Push safely

- 如果当前分支已有 upstream，就推到该 upstream。
- 如果当前分支还没有 upstream，但存在 `origin`，则按当前分支名建立 upstream 并推送。
- 如果 push 因远程已有新提交而被拒绝，必须明确说明并停止，不能强推。
- 如果当前环境对网络或权限有额外限制，应申请必要授权，而不是假装推送成功。

### 6. Report the result

- 报告实际使用的 commit message。
- 报告推送的分支和远程目标。
- 如果能拿到结果，报告最终提交 hash。
- 如果任何一步失败，直接说明失败步骤和阻塞错误，不要堆砌废话。

## Guardrails

- 这是一个显式的“提交并推送”执行工作流，不是代码审阅或顺手清理工作流。
- 除非用户另外要求修复，否则不要在这个流程里改业务代码。
- 一次调用只创建一个提交。
- 除非用户明确要求，否则不要推到当前分支之外的分支。
- 不要伪造成功结果；是否成功必须以真实 git 命令结果为准。
