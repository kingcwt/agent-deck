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

`git-diff-description-push`

技能名，保持英文短名，不翻译。

### `display_name`

`Git Diff Description Push`

显示名称，表示“Git 改动描述并推送”。

### `description`

含义：

先逐个为当前仓库的改动文件生成简短、具体的描述，只对这些改动执行文件级 lint 和定向测试，再仅在所有适用的改动文件检查均通过后提交并推送当前分支。适用于用户输入 `/kc-gdp`、`$kc-gdp`、`kc-gdp`，或者明确要求“一边生成改动描述一边提交推送”的场景。

### `short_description`

`Describe, validate, commit, and push`

含义：

先描述并检查当前改动，再提交并推送。

### `default_prompt`

`Immediately inspect the current repository state for this turn, ignore stale conclusions, summarize every current changed file, run repository-defined file-scoped lint and targeted tests only for the final changed files, and create and push one commit only if every applicable changed-file check passes.`

含义：

在这一轮里立即检查当前仓库状态，忽略过期结论，汇总当前所有改动文件，只对最终改动文件执行仓库定义的文件级 lint 和定向测试，并且仅在所有适用的改动文件检查均通过后创建并推送一次提交。

### `codex_names`

`kc-gdp`

表示 Codex 侧生成一个技能别名：`kc-gdp`。

### `claude_skill_names`

`kc-gdp`

表示 Claude skill 侧生成一个技能别名：`kc-gdp`。

### `claude_commands`

`kc-gdp`

表示 Claude command 侧生成一个命令别名：`/kc-gdp`。

### `allow_implicit_invocation`

`false`

表示默认不允许隐式注入，优先要求显式调用。

---

# Git Diff Description Push

## Description

读取当前仓库改动；如果没有提供自定义提交描述，则为每个改动文件生成一句简短描述，并整理成 commit message；随后只对这些改动执行文件级 lint 和定向测试，仅在所有适用的改动文件检查均通过后提交并推送当前分支。默认生成中文描述，只有传入 `-e` 时才切换成英文。

## Parameters

- 必填：无。
- 可选 `-e`：把生成描述和总标题切换成英文。
- 可选 `[commit message]`：只要快捷词后面跟了任何非空文本，就把所有剩余文本作为完整 commit message。
- 支持格式：`[-e] [commit message]`。

## Shortcuts And Commands

- Codex 快捷键：`$kc-gdp`
- Codex 完整命令：`$kc-gdp [-e] [commit message]`
- Claude Code 快捷键：`/kc-gdp`
- Claude Code 完整命令：`/kc-gdp [-e] [commit message]`

## Examples

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

## Workflow

### 1. 先检查仓库状态

- 把 `/kc-gdp` 和 `$kc-gdp` 视为这个工作流的显式快捷触发词。
- 把这次命令触发本身视为这一轮的完整任务。不要沿用上一轮话题，也不要复用诸如“刚提交过”“没有改动”“仓库已经干净”这类旧结论；必须先重新检查当前仓库状态。
- 只支持一个可选语言参数，并且必须紧跟在快捷词后面：`-e` 表示把生成描述切换成英文。
- 在执行任何修改前，先读取 `git status --short`、当前分支名和已配置的远程信息。
- 在决定执行哪些检查前，先读取仓库本地规则文件，以及定义了必要验证命令的项目清单、任务配置和 CI 配置。
- 这次命令里新读取到的 `git status --short` 结果，就是判断本地是否有改动的唯一事实来源。只要 worktree 或 index 不为空，就不能再说“没有改动”。
- 先识别所有改动文件，包含 staged、unstaged 和 untracked 文件。
- 如果本地没有任何改动，直接说明并停止。
- 如果没有可用远程，或者当前分支暂时不能推送，必须先说明阻塞原因，再停止，不能先创建提交。

### 2. 确定 commit message 模式

- 快捷词后面的内容要作为一个原始参数整体保留，包括内部换行、空行、标点，以及属于描述内容的空格。
- 只支持一个可选语言参数，并且必须紧跟在快捷词后面：如果原始参数以精确的 `-e` token 开头，就移除这个 token 以及它后面紧邻的分隔空白，再判断是否还有自定义描述。
- 如果移除可选 `-e` 后还剩任何非空自定义描述，就把这段文本作为完整 commit message；不要再生成总标题，也不要追加自动生成的逐文件描述行。
- 自定义 commit message 可以跨多行。不要把它压成一行、不要按换行拆掉，也不要丢弃后续行。
- 如果没有剩余的非空自定义描述，才继续走下面默认的自动生成描述流程。

### 3. 为每个改动文件生成一句简短描述

- 先检查每个改动文件自己的 diff。
- 只有在仅看 diff 还不足以判断改动内容时，才继续阅读该文件当前内容。
- 默认用中文生成这些逐文件描述；只有当用户显式传了 `-e` 时，才改为英文。
- 每条描述都要短、具体、以动作表达为主。
- 不要退化成 `优化代码`、`修复一些问题`、`更新逻辑` 这类空泛说法。

### 4. 生成一条多行 commit message

- 以逐文件描述作为 commit message 的来源材料。
- 第一行必须是整个改动集的简短总标题。
- 后续每一行必须放一条逐文件描述，每行一条。
- 只有当用户没有在快捷词后面提供自定义 commit message 时，才执行这个自动生成消息步骤。
- 这些描述行默认只写描述内容本身；只有确实需要消歧义时，才允许提到文件路径。
- 如果这些改动文件看起来彼此不相关，要在提交前先指出这一点，让用户决定是否继续。

### 5. 通过强制质量门禁

- 只把准备提交的完整、最终改动文件作为强制验证范围。未改动文件和整个仓库的健康状态不属于本工作流。
- 从仓库本地规则（例如 `AGENTS.md` 或 `CLAUDE.md`）、package scripts、Makefile 或任务运行器、CI 配置中确认文件级命令。必须使用仓库真实工具及其参数，不能自行臆造一个通用命令。
- lint 只传入本次有改动且可 lint 的文件，或使用工具支持的最窄改动文件选择器。不能仅仅因为文件属于某个应用或包，就执行应用级、包级、工作区级或仓库级 lint、build、typecheck。
- 执行本次改动的测试文件，以及与改动生产代码直接相关的定向测试。除非用户明确要求扩大验证范围，否则不能运行整个应用、包或仓库的全量测试。
- 遵守仓库对命令的明确限制。相关命令被禁止，或现有工具不支持文件级执行时，要报告该项无法运行，并继续执行其他适用的改动文件检查；禁止用扩大到整个应用或仓库的命令代替。
- 除仓库规定的检查外，还要执行 `git diff --check`，在暂存前发现空白符错误。
- 每一条实际执行且适用于改动文件的命令都必须成功退出。任何这类检查失败时，必须在暂存、提交、推送之前停止，并报告准确阻塞原因。因为超出改动文件范围而明确不运行的更广检查不算失败。
- 不得使用 `--no-verify`、关闭或降低 lint 规则、仅为掩盖失败而添加忽略项，或者因为用户要求跳过验证而绕过本门禁。
- 不要在这个提交推送工作流中修复业务代码。报告失败并等待单独的修复请求。
- 验证后只要任意文件发生变化，就必须重跑受影响的全部检查。只能暂存和提交与成功验证结果完全一致的状态。

### 6. 创建一次提交

- 使用非交互式 git 命令暂存当前仓库改动。
- 使用完整的自定义 commit message，或自动推导出的多行 commit message，创建且只创建一个提交。
- 提交时必须使用能保留换行的非交互式 git 命令，例如把 message 写入临时文件后用 `git commit -F <file>` 提交。
- 如果 commit hooks 失败，必须报告失败并停止。
- 如果因为 git 身份未配置或 index 为空导致提交失败，必须精确说明阻塞点并停止。

### 7. 安全推送

- 如果当前分支已有 upstream，就推到该 upstream。
- 如果当前分支还没有 upstream，但存在 `origin`，则按当前分支名建立 upstream 并推送。
- 如果 push 因远程已有新提交而被拒绝，必须明确说明并停止，不能强推。
- 如果当前环境对网络或权限有额外限制，应申请必要授权，而不是假装推送成功。

### 8. 报告结果

- 报告生成出的逐文件描述；如果因为使用了自定义 commit message 而跳过自动生成，则说明这一点。
- 报告实际使用的 commit message。
- 报告推送的分支和远程目标。
- 如果能拿到结果，报告最终提交 hash。
- 如果任何一步失败，直接说明失败步骤和阻塞错误，不要堆砌废话。

## Guardrails

- 这是一个把“简短描述 diff”和“提交并推送”组合在一起的执行工作流。
- 除非用户另外要求修复，否则不要在这个流程里改业务代码。
- 不要静默遗漏改动文件。
- 一次调用只创建一个提交。
- 除非用户明确要求，否则不要改历史、amend、force push 或切换分支。
- 适用于改动文件的验证失败，或者验证结果已经不再对应当前文件状态时，绝对不能提交或推送。
- 绝对不能绕过 commit hooks 或强制质量门禁。
- 不要伪造成功结果；是否成功必须以真实 git 命令结果为准。
