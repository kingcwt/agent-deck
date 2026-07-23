# Agent Deck

[English README](./README.en.md)

`agent-deck` 是一个面向 Codex 和 Claude Code 的单一源技能仓库。

你只维护一次工作流定义，然后生成并安装到多个目标：

- Codex skills
- Claude Code skills
- Claude Code slash commands

当前仓库地址：`https://github.com/kingcwt/agent-deck`

## 这个仓库解决什么问题

你不需要反复输入很长的提示词，比如“分析当前项目、验证依赖、必要时安装、启动、验证并输出项目说明”。

你只需要维护一组短指令，例如：

- Codex：`$kc-pi`
- Claude Code：`/kc-pi`

真正的工作流只写在一个源文件里，然后自动渲染成各个平台所需的格式。

## 当前已有技能

下面这段由 `scripts/render_skills.py` 根据 `skills/*/source.md` 和 `skills/*/source.zh-CN.md` 自动同步。

<!-- BEGIN GENERATED SKILLS -->
### `active-memory`

技能描述：

把最近一轮已经完成的用户-助手对话写入当前项目的 `active-memory.md`，形成一条结构化记忆。

参数：

- 必填：无。
- 来源范围：当前快捷调用之前最近一轮已经完成的用户-助手对话。
- 输出文件：项目根目录下的 `active-memory.md`。
- 可选参数：无。

快捷键和完整命令：

- Codex 快捷键：`$kc-am`
- Codex 完整命令：`$kc-am`
- Claude Code 快捷键：`/kc-am`
- Claude Code 完整命令：`/kc-am`

示例：

### Codex

```text
$kc-am
```

### Claude Code

```text
/kc-am
```

### `diff-review`

技能描述：

只审查当前文件的 git 改动，解释每个改动在做什么，并判断这次修改是否必要、是否足够克制。

参数：

- 必填：无。
- 审查目标：必须且只能是一个带有 git 改动的当前文件。
- 可选参数：无。
- 默认不支持：全仓 diff 审查、多文件批量审查、自动修代码。

快捷键和完整命令：

- Codex 快捷键：`$df`、`$diff-review`
- Codex 完整命令：`$df`、`$diff-review`
- Claude Code 快捷键：`/df`、`/diff-review`
- Claude Code 完整命令：`/df`、`/diff-review`

示例：

### Codex

```text
$df
$diff-review
```

### Claude Code

```text
/df
/diff-review
```

### `git-diff-description`

技能描述：

读取当前仓库改动，并输出简洁中文审查：说明每个文件改了什么、实现是否还能更小、是否可能影响其他模块或逻辑。

参数：

- 必填：无。
- 可选语言：默认中文；只有用户明确要求英文时才输出英文。
- 输出：逐文件改动说明，加审查结论、最小化实现建议和影响范围说明。

快捷键和完整命令：

- Codex 快捷键：`$kc-gdd`
- Codex 完整命令：`$kc-gdd`
- Claude Code 快捷键：`/kc-gdd`
- Claude Code 完整命令：`/kc-gdd`

示例：

### Codex

```text
$kc-gdd
```

### Claude Code

```text
/kc-gdd
```

### `git-diff-description-push`

技能描述：

读取当前仓库改动；如果没有提供自定义提交描述，则为每个改动文件生成一句简短描述，并整理成 commit message；随后只对这些改动执行文件级 lint 和定向测试，仅在所有适用的改动文件检查均通过后提交并推送当前分支。默认生成中文描述，只有传入 `-e` 时才切换成英文。

参数：

- 必填：无。
- 可选 `-e`：把生成描述和总标题切换成英文。
- 可选 `[commit message]`：只要快捷词后面跟了任何非空文本，就把所有剩余文本作为完整 commit message。
- 支持格式：`[-e] [commit message]`。

快捷键和完整命令：

- Codex 快捷键：`$kc-gdp`
- Codex 完整命令：`$kc-gdp [-e] [commit message]`
- Claude Code 快捷键：`/kc-gdp`
- Claude Code 完整命令：`/kc-gdp [-e] [commit message]`

示例：

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

### `git-push`

技能描述：

执行仓库规定的 lint 和质量检查，再仅在所有规定检查均通过后，用必填描述创建一次提交并把当前分支推送到已配置远程。

参数：

- 必填：`<description>`，作为 commit message 使用。
- 可选参数：无。
- 默认不支持：`--amend`、强推、切分支、把改动拆成多个提交。

快捷键和完整命令：

- Codex 快捷键：`$kc-gp`
- Codex 完整命令：`$kc-gp <description>`
- Claude Code 快捷键：`/kc-gp`
- Claude Code 完整命令：`/kc-gp <description>`

示例：

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

### `init`

技能描述：

检查当前项目、验证依赖、仅在需要时安装、启动主进程、完成验证，并总结这个项目如何运行。

参数：

- 必填：无。
- 可选参数：无。
- 工作范围：仅限当前仓库或当前工作区。

快捷键和完整命令：

- Codex 快捷键：`$kc-pi`
- Codex 完整命令：`$kc-pi`
- Claude Code 快捷键：`/kc-pi`
- Claude Code 完整命令：`/kc-pi`

示例：

### Codex

```text
$kc-pi
```

### Claude Code

```text
/kc-pi
```

### `kc-slim-review`

技能描述：

审查代码、git diff 或拟议实现，找出在满足当前需求前提下最小且安全的实现路径。

这个工作流默认是只读复杂度审查。它寻找哪些代码可以删除、复用、局部化或推迟，但不能削弱安全、数据保护、注释、测试或共享代码确认规则。

参数：

- 必填：无。
- 可选目标：文件路径、选中的代码、当前 diff、暂存 diff、PR diff 或设计方案。
- 可选意图：用户可以要求只审查、输出最小重构计划，或在审查后应用修复。
- 默认范围：只审查提供的目标或当前工作区 diff；除非用户明确要求，不扩展到整个仓库。
- 默认不支持：自动重构、公共 API 重设计、数据库/schema 修改、依赖变更、共享 package 修改。

快捷键和完整命令：

- Codex 快捷键：`$kc-sr`、`$kc-slim-review`
- Codex 完整命令：`$kc-sr [target-or-intent]`、`$kc-slim-review [target-or-intent]`
- Claude Code 快捷键：`/kc-sr`、`/kc-slim-review`
- Claude Code 完整命令：`/kc-sr [target-or-intent]`、`/kc-slim-review [target-or-intent]`

示例：

### Codex

```text
$kc-sr
$kc-sr review current diff for over-engineering
$kc-slim-review this file
```

### Claude Code

```text
/kc-sr
/kc-sr review current diff for over-engineering
/kc-slim-review this file
```

### `kc-ui`

技能描述：

列出、查看并应用沉淀好的 UI 风格预设到当前项目。这个技能是面向 Web、桌面端和移动端界面的风格库与执行工作流，不是某一个固定端的模板。

参数：

- 应用 UI 修改时必填：一个明确的内置风格 id 和一个 UI 任务。
- 列表命令可选：不需要参数。
- 查看命令可选：一个内置风格 id。
- 当前内置风格 id：`agency-compact`。
- 如果用户只说暗色、极简、苹果风、紧凑、原生感等泛化风格，但没有命名风格 id，不要修改代码。列出可用风格 id 和一句话描述，让用户用明确风格 id 重新执行。
- 如果风格 id 未知，不要修改代码。列出可用风格 id，并展示期望的命令格式。

快捷键和完整命令：

- Codex 列表命令：`$kc-ui list`
- Codex 查看命令：`$kc-ui look <style-id>`
- Codex 应用命令：`$kc-ui use <style-id> <task>`
- Codex 简写应用命令：`$kc-ui <style-id> <task>`
- Claude Code 列表命令：`/kc-ui list`
- Claude Code 查看命令：`/kc-ui look <style-id>`
- Claude Code 应用命令：`/kc-ui use <style-id> <task>`
- Claude Code 简写应用命令：`/kc-ui <style-id> <task>`

示例：

### Codex

```text
$kc-ui list
$kc-ui look agency-compact
$kc-ui use agency-compact redesign the settings page
$kc-ui agency-compact adjust the whole project UI
```

### Claude Code

```text
/kc-ui list
/kc-ui look agency-compact
/kc-ui use agency-compact redesign the settings page
/kc-ui agency-compact adjust the whole project UI
```

### 模糊请求

```text
$kc-ui make the settings page dark and minimal
```

期望行为：不要修改代码。展示可用风格 id，并让用户明确选择，例如 `$kc-ui use agency-compact make the settings page dark and minimal`。

### `kc-wd`

技能描述：

讲解一个英文单词、短语或代码标识符，让中文学习者能理解意思、读准读音并记住它。这个工作流尤其适合代码、文档、终端输出、API 名称和普通英文里的陌生词。

参数：

- 必填：一个英文单词、短语或标识符。
- 可选上下文：会影响含义的代码片段、句子或领域背景。
- 如果用户只发送一个独立英文单词且没有其他意图，默认按这个工作流处理。
- 如果输入是 `drain_notifications` 这样的代码标识符，先拆成组成单词，优先讲用户选中的词，再解释整个标识符。

快捷键和完整命令：

- Codex 快捷键：`$kc-wd`
- Codex 完整命令：`$kc-wd <word-or-identifier>`
- Claude Code 快捷键：`/kc-wd`
- Claude Code 完整命令：`/kc-wd <word-or-identifier>`
- 隐式模式：`<单个英文单词>`

示例：

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

### `work-hours`

技能描述：

导出最近 7 天的工时记录，并按天和上午/下午分组写入桌面 markdown 文件，可选只导出指定项目；或者向 agent-deck 的全局工时日志里补记一条今天的手动工时记录。

参数：

- 默认模式：不带额外参数，导出包含今天在内的最近 7 天。
- 筛选模式：传一个方括号参数，`"[<project>,<project>]"`，只导出最近 7 天里匹配的项目。
- 补记模式：`add <project> -m"<message>" [-am|-pm]`。
- 可选 `-am`：强制把手动记录写到今天上午。
- 可选 `-pm`：强制把手动记录写到今天下午。

快捷键和完整命令：

- Codex 快捷键：`$kc-wh`
- Codex 完整命令：`$kc-wh`、`$kc-wh '[<project>,<project>]'`、`$kc-wh add <project> -m"<message>" [-am|-pm]`
- Claude Code 快捷键：`/kc-wh`
- Claude Code 完整命令：`/kc-wh`、`/kc-wh '[<project>,<project>]'`、`/kc-wh add <project> -m"<message>" [-am|-pm]`

示例：

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
<!-- END GENERATED SKILLS -->

## 仓库结构

```text
agent-deck/
├── skills/
│   └── <skill-name>/
│       ├── source.md
│       └── source.zh-CN.md
├── scripts/
│   ├── render_skills.py
│   └── sync.sh
├── dist/
│   ├── codex/
│   └── claude/
├── install.sh
├── README.md
└── README.en.md
```

各目录含义：

- `skills/*/source.md`：技能唯一执行源文件
- `skills/*/source.zh-CN.md`：和执行源一一对应的中文阅读说明
- `scripts/render_skills.py`：把源文件渲染成发布产物
- `scripts/sync.sh`：本地重新生成并安装到 Codex / Claude 目录
- `dist/`：生成产物；为了远程安装和公开发布，应该提交到 GitHub
- `install.sh`：本地或远程一键安装/更新入口
- `README.md`：默认中文说明
- `README.en.md`：英文说明

## 编写模型

每个技能只定义一次，执行源写在 `source.md` 中；中文对照说明写在 `source.zh-CN.md` 中。

元数据示例：

```md
---
name: init
display_name: Project Init
description: ...
short_description: ...
default_prompt: ...
codex_names: kc-pi
claude_skill_names: kc-pi
claude_commands: kc-pi
allow_implicit_invocation: false
---
```

这样一个工作流就可以展开成多个别名，不需要复制正文。

README 里的“当前已有技能”目录不会再手写维护，而是从技能源说明自动同步。

## 本地开发

本地渲染并安装：

```bash
cd ~/Desktop/kingcwt/work/agent-deck
./scripts/sync.sh
```

这个命令会：

- 重建 `dist/`
- 刷新 `README.md` 和 `README.en.md` 里的技能目录
- 安装 Codex skills 到 `~/.codex/skills`
- 安装 Claude skills 到 `~/.claude/skills`
- 安装 Claude commands 到 `~/.claude/commands`

如果你只想生成产物，不想安装：

```bash
python3 ./scripts/render_skills.py
```

## 安装

### 本地仓库安装

```bash
git clone https://github.com/kingcwt/agent-deck.git
cd agent-deck
./install.sh
```

### 直接从 GitHub 安装

```bash
curl -fsSL https://raw.githubusercontent.com/kingcwt/agent-deck/main/install.sh | bash -s -- --repo kingcwt/agent-deck --ref main
```

`install.sh` 是幂等的：

- 第一次执行：安装
- 之后再次执行：更新并覆盖到最新版本

## 更新

如果你已经有本地仓库：

```bash
cd ~/Desktop/kingcwt/work/agent-deck
git pull
./install.sh
```

如果你用的是远程安装方式，重复执行同一个 `curl ... | bash` 命令即可。

## 发布工作流

当你修改某个技能时：

1. 编辑 `skills/*/source.md`
2. 同步更新对应的 `skills/*/source.zh-CN.md`
3. 运行 `./scripts/sync.sh`
4. 在 Codex 和 Claude Code 中测试
5. 提交源文件、更新后的 README 和生成后的 `dist/`
6. 推送到 GitHub

之所以提交 `dist/`，是因为：

- 远程安装更稳定
- 其他用户可以直接检查生成产物
- 更容易被技能目录或安装工具消费

## 新增一个技能

1. 新建 `skills/<new-skill>/source.md`
2. 新建对应的 `skills/<new-skill>/source.zh-CN.md`
3. 复制现有技能作为模板
4. 修改元数据和正文
5. 配置别名：
   - `codex_names: foo,bar`
   - `claude_skill_names: foo,bar`
   - `claude_commands: foo,bar`
6. 运行 `./scripts/sync.sh`
7. 提交源文件、README 更新和新的 `dist/`

## 为什么 Claude 同时有 skills 和 commands

Claude Code 同时支持可复用技能和 slash commands，两者用途不同：

- Claude skills 用于能力复用和技能分发
- Claude commands 用于最短路径调用体验，例如 `/kc-pi`

这个仓库会从同一个源文件同时生成两种产物，避免你维护两套重复逻辑。

## 备注

- Codex 更适合显式调用 skill，例如 `$kc-pi`
- Claude 使用 `/kc-pi`
- Claude 侧故意不使用 `/init`，因为它容易与内置命令语义冲突
- 这个仓库的结构可以继续扩展到很多技能，不需要重构整体架构
