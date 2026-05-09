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

先逐个为当前仓库的改动文件生成简短、具体的描述，再把这些描述整理成一条“多行”的 commit message，最后提交并推送当前分支。适用于用户输入 `/kc-gdp`、`$kc-gdp`、`kc-gdp`，或者明确要求“一边生成改动描述一边提交推送”的场景。

### `short_description`

`Describe current changes, commit, and push`

含义：

先描述当前改动，再提交并推送。

### `default_prompt`

`Use $kc-gdp to summarize the current changed files, derive a multi-line commit message from those descriptions, create one commit, and push the current branch.`

含义：

使用 `$kc-gdp` 汇总当前改动文件，为这些描述生成一条多行 commit message，创建一次提交，并推送当前分支。

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

## Overview

检查当前仓库里的所有改动文件，基于 diff 和必要上下文为每个文件生成一句简短、具体的描述，再把这些描述整理成一条多行 commit message，然后暂存当前仓库改动、创建一次提交，并推送当前分支。

## Workflow

### 1. 先检查仓库状态

- 把 `/kc-gdp` 和 `$kc-gdp` 视为这个工作流的显式快捷触发词。
- 在执行任何修改前，先读取 `git status --short`、当前分支名和已配置的远程信息。
- 先识别所有改动文件，包含 staged 和 unstaged 的已跟踪改动，也包含当前工作区里的 untracked 文件。
- 如果本地没有任何改动，直接说明并停止。
- 如果没有可用远程，或者当前分支暂时不能推送，必须先说明阻塞原因，再停止，不能先创建提交。

### 2. 为每个文件生成简短描述

- 对每个改动文件，先检查它自己的 git diff。
- 如果仅看 diff 还不足以判断改动内容，就继续阅读该文件当前内容。
- 只补充理解这个改动所必需的最近邻代码或引用。
- 对于 untracked 文件，直接读取文件内容，并结合文件名和内容推断它的用途。
- 对于被删除的文件，结合删除 diff 和周边引用说明删掉了什么。
- 为每个改动文件输出一条简短、具体的描述。
- 优先使用类似 `新增登录按钮`、`补充 UserSession 类型`、`调整订单列表请求参数`、`删除废弃支付回调` 这样的表述。
- 避免 `优化代码`、`修复一些问题`、`更新逻辑` 这类空泛说法。

### 3. 把这些描述整理成一条多行 commit message

- 以逐文件描述作为 commit message 的来源材料。
- 不能把所有改动压成一句话提交信息。
- 必须生成一条多行 commit message：
  - 第一行：整个改动集的简短总标题
  - 后续每一行：写一条逐文件改动描述，每个文件一行
- 后续这些逐文件描述要尽量具体、可读；除非需要消歧义，否则不要机械地在每行前都带完整文件路径。
- 如果用户在 `/kc-gdp` 或 `$kc-gdp` 后面追加了文本，就把这段文本视为显式指定的第一行标题，但后面仍然必须逐行追加生成出的逐文件描述。
- 如果这些改动文件看起来彼此不相关，要在提交前先指出这一点，让用户决定是否继续。

结构示例：

```text
feat: add region-manager entry selection flow
新增首页头像菜单里的切换版本入口
新增登录后的入口选择页
调整登录后默认跳转到 /entry
新增地区经理首页路由和权限判断
```

### 4. 创建一次提交

- 使用非交互式 git 命令暂存当前仓库改动。
- 使用推导出的多行 commit message，或“用户显式指定的第一行 + 自动生成的逐文件描述行”，创建且只创建一个提交。
- 提交时必须使用能保留换行的非交互式 git 命令。
- 如果 commit hooks 失败，必须报告失败并停止；除非用户明确要求，否则不要绕过 hook。
- 如果因为 git 身份未配置或 index 为空导致提交失败，必须精确说明阻塞点并停止。

### 5. 安全推送

- 如果当前分支已有 upstream，就推到该 upstream。
- 如果当前分支还没有 upstream，但存在 `origin`，则按当前分支名建立 upstream 并推送。
- 如果 push 因远程已有新提交而被拒绝，必须明确说明并停止，不能强推。
- 如果当前环境对网络或权限有额外限制，应申请必要授权，而不是假装推送成功。

### 6. 报告结果

- 报告生成出的逐文件描述。
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
- 不要伪造成功结果；是否成功必须以真实 git 命令结果为准。
