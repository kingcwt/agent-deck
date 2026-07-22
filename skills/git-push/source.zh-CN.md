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

执行仓库规定的 lint 和质量检查，再使用用户提供且必填的描述信息，仅在所有规定检查均通过后把当前仓库改动提交并推送到远程仓库。适用于用户输入带有非空描述的 `/kc-gp`、带有非空描述的 `$kc-gp`、带有非空描述的 `kc-gp`，或者明确要求“检查、提交并推送当前仓库改动”的场景。

### `short_description`

`Validate, commit, and push`

含义：

检查通过后，带描述地提交并推送当前仓库改动。

### `default_prompt`

`Use $kc-gp <description> to inspect the current changes, run all repository-required lint and quality checks against the final state, and create and push one commit only if every required check passes.`

含义：

使用 `$kc-gp <description>` 检查当前改动，对最终状态执行仓库规定的全部 lint 和质量检查，并且仅在所有规定检查均通过后创建并推送一次提交。

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

执行仓库规定的 lint 和质量检查，再仅在所有规定检查均通过后，用必填描述创建一次提交并把当前分支推送到已配置远程。

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
- 在决定执行哪些检查前，先读取仓库本地规则文件，以及定义了必要验证命令的项目清单、任务配置和 CI 配置。
- 简洁说明哪些文件有改动、是否已经存在 staged 改动，以及接下来准备推哪个分支。
- 如果本地没有任何改动，直接说明并停止。
- 如果没有可用远程，或者当前分支暂时不能推送，必须先说明阻塞原因，再停止，不能先创建提交。

### 3. Protect scope before committing

- 把这个工作流视为用户显式发起的“提交并推送当前仓库现有改动”动作。
- 默认将当前仓库改动作为一次提交进行暂存，不要静默遗漏文件。
- 如果工作区里存在看起来与用户意图不一致的改动，要先指出这一点，再继续提交，避免误推。
- 除非用户明确要求，否则不要改历史、不要 amend、不要 force push、不要切分支。

### 4. Pass the mandatory quality gate

- 把准备提交的完整、最终工作区内容作为验证对象。
- 从仓库本地规则（例如 `AGENTS.md` 或 `CLAUDE.md`）、package scripts、Makefile 或任务运行器、CI 配置中确认适用命令。必须使用仓库真实命令，不能自行臆造一个通用命令。
- 对每个提供 lint 命令的受影响应用或包执行 lint。如果仓库把 build、typecheck 或其他命令定义为 lint 验证，必须执行该实际命令。
- 同时执行仓库规则针对当前改动范围要求的全部 typecheck、test、build 或其他质量检查。不能用 diff 审查替代可执行验证。
- 遵守仓库对命令的明确限制。某个必要命令被禁止时，只能使用规则中明确写出的等价检查；如果不存在允许的等价检查，必须在暂存前停止并报告验证阻塞。
- 除仓库规定的检查外，还要执行 `git diff --check`，在暂存前发现空白符错误。
- 每一条必要命令都必须成功退出。任何检查失败、无法执行或无法可靠识别时，必须在暂存、提交、推送之前停止，并报告准确阻塞原因。
- 不得使用 `--no-verify`、关闭或降低 lint 规则、仅为掩盖失败而添加忽略项，或者因为用户要求跳过验证而绕过本门禁。
- 不要在这个提交推送工作流中修复业务代码。报告失败并等待单独的修复请求。
- 验证后只要任意文件发生变化，就必须重跑受影响的全部检查。只能暂存和提交与成功验证结果完全一致的状态。

### 5. Create the commit

- 使用非交互式 git 命令暂存仓库改动。
- 使用提供的描述创建且只创建一个提交。
- 如果 commit hook 失败，必须报告失败并停止；绝对不能绕过 hook。
- 如果因为 git 身份未配置或 index 为空导致提交失败，必须精确说明阻塞点并停止。

### 6. Push safely

- 如果当前分支已有 upstream，就推到该 upstream。
- 如果当前分支还没有 upstream，但存在 `origin`，则按当前分支名建立 upstream 并推送。
- 如果 push 因远程已有新提交而被拒绝，必须明确说明并停止，不能强推。
- 如果当前环境对网络或权限有额外限制，应申请必要授权，而不是假装推送成功。

### 7. Report the result

- 报告实际使用的 commit message。
- 报告推送的分支和远程目标。
- 如果能拿到结果，报告最终提交 hash。
- 如果任何一步失败，直接说明失败步骤和阻塞错误，不要堆砌废话。

## Guardrails

- 这是一个显式的“提交并推送”执行工作流，不是代码审阅或顺手清理工作流。
- 除非用户另外要求修复，否则不要在这个流程里改业务代码。
- 一次调用只创建一个提交。
- 除非用户明确要求，否则不要推到当前分支之外的分支。
- 必要验证失败、被跳过、无法执行，或者已经不再对应当前文件状态时，绝对不能提交或推送。
- 绝对不能绕过 commit hooks 或强制质量门禁。
- 不要伪造成功结果；是否成功必须以真实 git 命令结果为准。
