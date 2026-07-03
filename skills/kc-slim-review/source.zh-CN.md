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

`kc-slim-review`

技能名，保持 `kc-` 短名，不翻译。

### `display_name`

`Slim Review`

显示名称，表示“最小实现审查”。

### `description`

含义：

审查代码、diff 或拟议实现中是否存在过度设计和不必要的范围扩大。适用于用户输入 `/kc-sr`、`/kc-slim-review`、`$kc-sr`、`$kc-slim-review`、`kc-sr`，询问代码是否能更简单，要求做最小重构审查，或希望 AI agent 找出不必要抽象、依赖、重复逻辑、共享代码越界、投机配置、顺手清理等问题。默认只读审查；只有用户在审查后明确要求应用修复时才改代码。

### `short_description`

`Find smaller safe implementations [最小实现审查]`

含义：

寻找更小但安全的实现路径。

### `default_prompt`

`Use $kc-sr to review code or a diff for over-engineering, duplicated logic, avoidable dependencies, and unsafe scope expansion without changing code by default.`

含义：

使用 `$kc-sr` 审查代码或 diff 里是否存在过度设计、重复逻辑、可避免依赖和不安全的范围扩大；默认不修改代码。

### `codex_names`

`kc-sr,kc-slim-review`

表示 Codex 侧生成两个技能别名：`kc-sr` 和 `kc-slim-review`。

### `claude_skill_names`

`kc-sr,kc-slim-review`

表示 Claude skill 侧生成两个技能别名：`kc-sr` 和 `kc-slim-review`。

### `claude_commands`

`kc-sr,kc-slim-review`

表示 Claude command 侧生成两个命令别名：`/kc-sr` 和 `/kc-slim-review`。

### `allow_implicit_invocation`

`false`

表示默认不允许隐式触发，优先要求显式调用。

---

# Slim Review

## Description

审查代码、git diff 或拟议实现，找出在满足当前需求前提下最小且安全的实现路径。

这个工作流默认是只读复杂度审查。它寻找哪些代码可以删除、复用、局部化或推迟，但不能削弱安全、数据保护、注释、测试或共享代码确认规则。

## Parameters

- 必填：无。
- 可选目标：文件路径、选中的代码、当前 diff、暂存 diff、PR diff 或设计方案。
- 可选意图：用户可以要求只审查、输出最小重构计划，或在审查后应用修复。
- 默认范围：只审查提供的目标或当前工作区 diff；除非用户明确要求，不扩展到整个仓库。
- 默认不支持：自动重构、公共 API 重设计、数据库/schema 修改、依赖变更、共享 package 修改。

## Shortcuts And Commands

- Codex 快捷键：`$kc-sr`、`$kc-slim-review`
- Codex 完整命令：`$kc-sr [target-or-intent]`、`$kc-slim-review [target-or-intent]`
- Claude Code 快捷键：`/kc-sr`、`/kc-slim-review`
- Claude Code 完整命令：`/kc-sr [target-or-intent]`、`/kc-slim-review [target-or-intent]`

## Examples

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

## Workflow

### 1. Confirm scope and mode

- 把 `$kc-sr`、`$kc-slim-review`、`/kc-sr` 和 `/kc-slim-review` 视为这个工作流的显式触发词。
- 默认只读审查；除非用户明确说要应用修复，否则不要编辑文件。
- 判断前先确认准确审查目标；能拿到当前 diff 或用户提供的文件/代码时就使用它。
- 如果目标不明确，先询问路径或 diff，不要扫描无关文件。
- 如果用户要求重构，先输出最小重构计划；只有得到明确确认后才实现。

### 2. Read enough context

- 先检查相关 diff 或代码。
- 阅读判断复用和范围所需的邻近代码，包括直接相关的 helper、类型、组件、import 和调用点。
- 在判断“重复实现”之前，先搜索已有工具或模式。
- 把仓库规则、注释和本地约定当作有约束力的证据。
- 当意图或需求没有代码、日志、测试、截图或用户上下文支持时，要明确标注不确定性。

### 3. Apply the minimal implementation ladder

对每个改动或拟议实现，按顺序检查：

1. 这段代码是否确实是当前需求所必需的？
2. 项目里是否已经有 helper、组件、类型、模式或流程覆盖它？
3. 语言标准库是否已经覆盖它？
4. 平台、浏览器、框架、数据库约束或原生能力是否覆盖它？
5. 已安装依赖是否能覆盖它，而不需要新增依赖？
6. 同样行为是否能用更小的局部改动完成？
7. 只有以上都不满足时，才接受新增抽象、包装层、配置、依赖或更大范围重构。

### 4. Flag complexity smells

重点查找：

- 未请求的抽象：只有一个实现的接口、工厂、策略、适配器或泛型层。
- 投机灵活性：没人设置的 option、配置字段、扩展点、feature flag 或 callback。
- 重复逻辑：本应复用现有 helper、组件、类型或项目模式的代码。
- 可避免依赖：标准库、平台能力或现有包已覆盖，却新增或使用沉重依赖。
- 共享代码越界：为局部需求修改公共 helper、packages、通用类型、配置或共享组件。
- 顺手改动：与任务无关的格式化、清理、重命名、大范围重写或性能优化。
- 影响面过大：本可以局部修改，却触碰很多文件。

### 5. Protect non-negotiables

永远不要建议移除或削弱：

- 授权、认证、权限检查或信任边界校验。
- 防止数据丢失、幂等性、事务安全、migration 安全或回滚行为。
- 保护数据完整性或提供必要用户反馈的错误处理。
- 产品要求的可访问性基础和平台兼容性。
- 已有测试，或非平凡逻辑所需的小型必要测试。
- 说明业务意图、兼容性约束或关键实现原因的必要注释。
- 用户明确要求，即使它比最小替代方案更复杂。
- 项目中关于修改共享代码、packages、公共类型、数据库文件或配置前必须确认的规则。

### 6. Decide review outcome

对每条发现分类：

- `delete`：删除死代码、投机代码或无关代码。
- `reuse`：用现有本地 helper、组件、类型或模式替换重复逻辑。
- `stdlib`：用标准库功能替换自写代码。
- `native`：用平台、浏览器、框架、数据库或内建能力替换代码或依赖。
- `localize`：避免修改共享/公共代码，只在当前模块局部适配。
- `defer`：把投机灵活性推迟到真实第二个用例出现时。
- `keep`：复杂度有证据支持，来自安全、兼容性、可访问性或明确需求。

### 7. Report clearly

默认按这个顺序输出：

1. `Scope`：审查了什么，以及当前是只读审查还是应用修复模式。
2. `Findings`：先列可执行项，按严重程度和置信度排序。
3. `Keep`：哪些复杂度应该保留，因为它保护安全、数据、可访问性、兼容性或明确需求。
4. `Minimal path`：最小安全实现或重构计划。
5. `Blocked or needs confirmation`：需要用户确认的共享代码、数据库/配置改动或不确定需求。

每条发现都应包含：

- 可用时给出文件或代码位置
- 当前复杂度
- 更小替代方案
- 为什么替代方案安全
- 哪些保护项不能移除

## Output Template

```text
Scope
- Reviewed: <target>
- Mode: review-only | apply-fixes requested

Findings
- <severity>: <location> <tag> <current complexity>. Smaller path: <replacement>. Keep: <non-negotiable guardrail>.

Keep
- <location or behavior>: keep because <evidence>.

Minimal path
- <smallest safe plan>

Blocked or needs confirmation
- <only if needed>
```

## Guardrails

- 第一轮默认不编辑代码，除非用户明确要求实现。
- 不要建议修改共享 package、公共 helper、数据库 schema、migration 或共享配置，除非明确指出需要用户确认。
- 没有阅读相关现有代码或说明不确定性时，不要声称更小方案是安全的。
- 不要删除本地项目规则要求的注释；如果注释过期，应更新注释。
- 不要把它变成通用正确性审查；只有当简化建议影响正确性或安全时才提及。
- 不要为了更少代码牺牲必要业务逻辑的清晰性。
