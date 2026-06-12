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

`work-hours`

技能名，保持英文短名，不翻译。

### `display_name`

`Work Hours`

显示名称，表示“工时导出与补记”。

### `description`

含义：

从 agent-deck 的全局 git 提交日志里导出最近工时记录，可选只导出指定项目，或者为今天补记一条手动工时记录。适用于用户输入 `/kc-wh`、`/kc-work-hours`、`$kc-wh`、`$kc-work-hours`、`kc-wh`，或者明确要求导出近 7 天工时、补记会议等手动工时记录的场景。

### `short_description`

`Export 7-day work hours or add a manual record`

含义：

导出近 7 天工时，或补记一条手动工时。

### `default_prompt`

`Use $kc-wh to export the last 7 days of work-hour records, use $kc-wh '[project-a,project-b]' to export only selected projects, or use $kc-wh add <project> -m"<message>" [-am|-pm] to append a manual work-hour record for today.`

含义：

使用 `$kc-wh` 导出最近 7 天工时，使用 `$kc-wh '[project-a,project-b]'` 只导出指定项目，或使用 `$kc-wh add <project> -m"<message>" [-am|-pm]` 为今天追加一条手动工时记录。

### `codex_names`

`kc-wh`

表示 Codex 侧只生成一个技能别名：`kc-wh`。

### `claude_skill_names`

`kc-wh`

表示 Claude skill 侧只生成一个技能别名：`kc-wh`。

### `claude_commands`

`kc-wh`

表示 Claude command 侧只生成一个命令别名：`/kc-wh`。

### `allow_implicit_invocation`

`false`

表示默认不允许隐式注入，优先要求显式调用。

---

# Work Hours

## Description

导出最近 7 天的工时记录，并按天和上午/下午分组写入桌面 markdown 文件，可选只导出指定项目；或者向 agent-deck 的全局工时日志里补记一条今天的手动工时记录。

## Parameters

- 默认模式：不带额外参数，导出包含今天在内的最近 7 天。
- 筛选模式：传一个方括号参数，`"[<project>,<project>]"`，只导出最近 7 天里匹配的项目。
- 补记模式：`add <project> -m"<message>" [-am|-pm]`。
- 可选 `-am`：强制把手动记录写到今天上午。
- 可选 `-pm`：强制把手动记录写到今天下午。

## Shortcuts And Commands

- Codex 快捷键：`$kc-wh`
- Codex 完整命令：`$kc-wh`、`$kc-wh '[<project>,<project>]'`、`$kc-wh add <project> -m"<message>" [-am|-pm]`
- Claude Code 快捷键：`/kc-wh`
- Claude Code 完整命令：`/kc-wh`、`/kc-wh '[<project>,<project>]'`、`/kc-wh add <project> -m"<message>" [-am|-pm]`

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

### 1. 解析调用形式

- 把 `/kc-wh` 和 `$kc-wh` 视为这个工作流的显式快捷触发词。
- 如果快捷词后面没有额外文本，就进入默认导出模式，导出包含今天在内的最近 7 天。
- 如果尾随文本是一个方括号参数，例如 `"[cmc-ai,nice]"`，就按导出筛选模式解析，只保留项目名精确匹配列表中任一名称的记录。
- 如果尾随文本以 `add ` 开头，就按 `add <project> -m"<message>" [-am|-pm]` 解析成手动补记模式。
- 如果参数不符合任何支持格式，就直接报出支持的命令格式，不要自行猜测。

### 2. 使用全局 agent-deck 工时安装目录

- 这个技能的全局存储根目录固定为 `~/.agent-deck/workhours`。
- 可执行 CLI 固定为 `~/.agent-deck/workhours/workhours_cli.py`。
- 共享工时日志固定为 `~/.agent-deck/workhours/git-commit-log.txt`。
- 如果 CLI 或日志路径缺失，要明确提示用户重新执行本仓库的 `./scripts/sync.sh` 或 `./install.sh`，让全局安装被重新创建。

### 3. 执行导出模式

- 导出模式下，直接执行全局 CLI，不传额外参数。
- 导出筛选模式下，执行全局 CLI 时传入单个带引号的方括号参数，例如 `"[cmc-ai,nice]"`。
- 导出的时间范围必须严格是包含今天在内的最近 7 天，也就是今天加往前 6 个自然日，使用本地时区。
- 项目筛选必须用工时日志里的 `project` 值做精确项目名匹配。
- 导出的 markdown 标题里必须显示时间范围。
- 使用项目筛选时，导出的 markdown 必须显示选中的项目名，并且桌面文件名必须包含这些项目名。
- 导出结果必须始终落到桌面 markdown 文件里，不能只在对话里输出文本。
- 输出按天分组，每天内部再拆成 `上午` 和 `下午`。
- 每条记录要显示项目名和提交描述或手动描述。
- 如果一条记录本身包含多行描述，导出文件里必须保留这些描述行，不能压成一行。

### 4. 执行手动补记模式

- 补记模式下，把解析后的 `add` 参数传给全局 CLI 执行。
- 用户提供的项目名和描述内容要尽量原样保留，只有在执行命令时做必要的安全转义。
- 如果传了 `-am`，就写入今天上午。
- 如果传了 `-pm`，就写入今天下午。
- 如果两者都没传，就让 CLI 根据当前本地时间决定写上午还是下午。

### 5. 报告结果

- 导出模式下，返回桌面文件路径，并给出生成的 markdown 内容。
- 补记模式下，报告项目名、描述内容，以及这条记录写入的是今天上午还是下午。
- 如果执行失败，直接说明阻塞错误，不要堆砌废话。

## Guardrails

- 这个工作流只负责导出最近工时记录，或者补记一条手动工时。
- 不要在这个流程里修改业务代码。
- 不要读写旧的 `~/.workhours` 目录，那是其他历史工具的存储位置。
- 如果全局日志为空或不存在，就直接说明，不要编造记录。
- 除非技能定义被明确修改，否则不要擅自扩大导出时间范围。
