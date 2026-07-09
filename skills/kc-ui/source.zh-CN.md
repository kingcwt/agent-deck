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

`kc-ui`

技能名，保持 `kc-` 短名，不翻译。

### `display_name`

`UI Style`

显示名称，表示“UI 风格”。

### `description`

含义：

选择并应用沉淀好的 UI 风格预设，适用于 Web、桌面端和移动端界面。用户输入 `/kc-ui`、`$kc-ui`、`kc-ui`，要求列出 UI 风格、查看某个 UI 风格，或把明确命名的 UI 风格应用到页面、组件或项目 UI 时使用。

### `short_description`

`List, inspect, and apply UI styles [UI风格库]`

含义：

列出、查看和应用 UI 风格库。

### `default_prompt`

`Use $kc-ui to list curated UI styles, inspect one style, or apply an explicitly named style to the current UI.`

含义：

使用 `$kc-ui` 列出沉淀好的 UI 风格、查看某个风格，或把明确命名的风格应用到当前 UI。

### `codex_names`

`kc-ui`

表示 Codex 侧生成一个技能别名：`kc-ui`。

### `claude_skill_names`

`kc-ui`

表示 Claude skill 侧生成一个技能别名：`kc-ui`。

### `claude_commands`

`kc-ui`

表示 Claude command 侧生成一个命令别名：`/kc-ui`。

### `allow_implicit_invocation`

`false`

表示不允许隐式触发。必须通过 `$kc-ui`、`/kc-ui` 或明确的 `kc-ui` 意图触发。

---

# UI Style

## Description

列出、查看并应用沉淀好的 UI 风格预设到当前项目。这个技能是面向 Web、桌面端和移动端界面的风格库与执行工作流，不是某一个固定端的模板。

## Parameters

- 应用 UI 修改时必填：一个明确的内置风格 id 和一个 UI 任务。
- 列表命令可选：不需要参数。
- 查看命令可选：一个内置风格 id。
- 当前内置风格 id：`agency-compact`。
- 如果用户只说暗色、极简、苹果风、紧凑、原生感等泛化风格，但没有命名风格 id，不要修改代码。列出可用风格 id 和一句话描述，让用户用明确风格 id 重新执行。
- 如果风格 id 未知，不要修改代码。列出可用风格 id，并展示期望的命令格式。

## Shortcuts And Commands

- Codex 列表命令：`$kc-ui list`
- Codex 查看命令：`$kc-ui look <style-id>`
- Codex 应用命令：`$kc-ui use <style-id> <task>`
- Codex 简写应用命令：`$kc-ui <style-id> <task>`
- Claude Code 列表命令：`/kc-ui list`
- Claude Code 查看命令：`/kc-ui look <style-id>`
- Claude Code 应用命令：`/kc-ui use <style-id> <task>`
- Claude Code 简写应用命令：`/kc-ui <style-id> <task>`

## Examples

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

## Workflow

### 1. 解析命令

- `list`：输出所有可用风格 id 和一句话描述。
- `look <style-id>`：输出所选风格的完整规格。
- `use <style-id> <task>` 或 `<style-id> <task>`：把该风格应用到当前项目 UI。
- 缺少风格 id、未知风格 id，或只有泛化自然语言风格描述：不要修改文件；列出可用风格和期望用法。

### 2. 修改前检查目标项目

- 阅读相关 UI 文件、主题 token、组件库、设计系统和现有布局结构。
- 优先复用项目已有 token、组件、框架约定和工具类。
- 判断目标是 Web、桌面端还是移动端，然后把所选风格翻译到该平台，不要把桌面布局复制到所有端。
- 修改前说明会改哪些文件以及为什么要改。

### 3. 应用所选风格

- 以风格规格作为字体、密度、颜色、圆角、组件状态和布局节奏的事实来源。
- 除非用户明确要求行为改动，否则保持产品功能不变。
- 当任务是风格转换时，不要发明新页面、假数据或只为截图存在的内容。
- 修改范围限制在用户要求的页面、组件或 UI 表面。

### 4. 验证

- 可行时运行项目已有的 typecheck、lint、build 或聚焦 UI 验证。
- 如果工具可用，按相关视口或应用窗口检查视觉结果。
- 特别检查比例：正文字号、控件高度、侧栏宽度、padding、margin、卡片大小和 titlebar 对齐都必须符合所选风格密度。

## Built-in Styles

### `agency-compact`

一句话描述：暗色、紧凑、macOS 原生工具应用风格，使用克制橙色强调、紧密间距、source-list 导航和细微层级表面。

#### 定位

- 适用：设置页、账号/Profile 管理器、控制面板、仪表盘、source-list 应用、开发者工具、工具类应用、Web 管理后台、桌面应用和移动端工具页。
- 不适用：营销落地页、图片很重的活动页、游戏 UI、品牌叙事页和大屏展示界面。
- 关键词：暗色、紧凑、macOS 原生、Apple 原生、source-list、工具应用、极简、高密度、克制、专业。

#### 字体

- Web 和桌面端根字号/基础字号：`13px`。
- 正文、导航项、控件、表格单元格：`13px`。
- 次级文本和元信息：`12px`。
- 徽标、标签和小型提示文本：`10px` 到 `11px`。
- 列表标题和 titlebar 标签：`14px`。
- 页面、弹窗或对话框标题：`18px`。
- 除非目标平台有无障碍要求，否则避免默认 `16px` 偏大的布局；如果必须使用，也要通过间距和层级保持紧凑视觉密度。

#### 颜色

- 画布：`#151516`。
- Titlebar 或 topbar：`#202023`。
- 侧栏或导航表面：`#222224`。
- 主表面：`#1b1b1d`。
- 浮起表面：`#242427`。
- 按下表面：`#101011`。
- 控件表面：`#1a1a1c`。
- 悬停表面：`#29292d`。
- 边框：`rgba(255,255,255,0.09)`。
- 强边框：`rgba(255,255,255,0.15)`。
- 主文本：`#e6e6e9`。
- 次级文本：`#aaaab1`。
- 弱化文本：`#85858d`。
- 橙色强调：`#ff7a2f`。
- 成功：`#48d17a`。
- 危险：`#ff6b68`。
- 警告：`#f5b85f`。

#### 尺寸和间距

- 桌面 titlebar，如果应用自己绘制：约 `38px`。
- Toolbar：`48px` 到 `54px`。
- Sidebar：`220px` 到 `236px`，通常不超过 `980px` 宽窗口的 `28%`。
- 列表行：`56px` 到 `64px`。
- 按钮：`28px` 到 `34px`。
- 输入框和选择器：`32px` 到 `36px`。
- 卡片和面板内边距：`10px` 到 `16px`。
- 页面内边距：`16px` 到 `24px`。
- 优先使用 `4px`、`6px`、`8px`、`10px`、`12px`、`16px`、`20px` 间距阶梯。

#### 圆角

- 小控件：`8px`。
- 中等控件和列表行：`11px`。
- 大面板：`16px`。
- 胶囊：`999px`。

#### 组件规则

- 使用细边框和克制表面反差，不使用大阴影。
- 背景、边框、透明度和 transform 的悬停过渡约 `140ms`。
- 活动交互使用更暗的 pressed 表面。
- 橙色强调只克制用于主操作、选中指示、焦点环和重要状态标记。
- 选中的导航项或列表行应使用细微 pressed 背景，再配合克制强调色或 `2px` 橙色指示条。
- 避免超大卡片、重阴影、大留白和装饰性渐变，除非现有产品已经依赖这些语言。

#### 平台翻译

- Web：使用完整视口。不要把整个页面包成假的小桌面窗口。把风格翻译为全宽 app shell，使用侧栏、topbar、内容区域或响应式等价结构。
- 桌面端：titlebar、侧栏、分栏和内容面板是合适的。可用时优先使用原生平台控件。如果 shell 已经提供原生窗口控制，不要重复渲染交通灯按钮。
- 移动端：翻译成紧凑 header、tab 或底部导航、sheet、紧凑卡片和高密度列表。不要把桌面侧栏直接复制到移动端。

#### UI 比例防护

- 不要从截图像素直接反推 CSS 尺寸。必须考虑 Retina 截图、浏览器缩放和设备像素比。
- 优先使用源码 token、设计系统数值、DevTools computed value，或本技能里的明确规格。
- 紧凑工具 UI 不要默认使用 `16px` 正文和 `20px+` 控件。
- 如果结果整体显得偏大，优先按本风格规格回调根字号、toolbar 高度、列表行高、padding 和侧栏宽度。

## Guardrails

- 命令里没有明确已知风格 id 时，绝不应用风格。
- 绝不把“暗色主题”这类泛化请求当成自动选择风格的许可。
- 除非用户明确要求，不要在样式调整时改变产品行为。
- 不要手改 `agent-deck` 里的生成产物 `dist`；应修改 `skills/<name>/source.md` 后重新渲染。
- 每个风格都要跨平台。风格可以有平台专属翻译规则，但不能只是桌面、Web 或移动端的单端模板。

## Output Templates

### `list`

```text
Available UI styles:
- agency-compact: dark, compact, macOS-native utility-app style with restrained orange accents.

Use:
- $kc-ui look agency-compact
- $kc-ui use agency-compact <task>
```

### 缺少或模糊风格 id

```text
I need an explicit UI style id before changing code.

Available UI styles:
- agency-compact: dark, compact, macOS-native utility-app style with restrained orange accents.

Rerun with:
$kc-ui use agency-compact <task>
```

### `look agency-compact`

返回 Built-in Styles 里的完整 `agency-compact` 规格，包括定位、字体、颜色、尺寸、圆角、组件规则、平台翻译和比例防护。
