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

`init`

技能名，保持英文短名，不翻译。

### `display_name`

`Project Init`

显示名称，表示“项目初始化”。

### `description`

含义：

初始化并建立当前代码项目的基线。适用于用户输入 `/pi`、`/project-init`、`$pi`、`$project-init`、`pi`，或者表达“检查当前仓库、识别技术栈和包管理器、安装依赖、启动主应用或开发服务、验证服务可达、并输出包含启动说明、配置依赖和阻塞项的项目描述”这类意图的场景。

### `short_description`

`Inspect, install, run, and summarize a codebase`

含义：

检查、安装、运行并总结一个代码仓库。

### `default_prompt`

`Use $pi to inspect the current project, install dependencies, start it, and summarize how it works.`

含义：

使用 `$pi` 检查当前项目、安装依赖、启动它，并总结它的工作方式。

### `codex_names`

`pi,project-init`

表示 Codex 侧生成两个技能别名：`pi` 和 `project-init`。

### `claude_skill_names`

`pi,project-init`

表示 Claude skill 侧生成两个技能别名：`pi` 和 `project-init`。

### `claude_commands`

`pi,project-init`

表示 Claude command 侧生成两个命令别名：`/pi` 和 `/project-init`。

### `allow_implicit_invocation`

`false`

表示默认不允许隐式注入，优先要求显式调用。

---

# Init

## Overview

从项目检查开始，一直到本地成功运行并完成验证，建立当前项目的初始化基线。先阅读仓库，再安装依赖、启动主进程、验证结果，最后总结项目是什么以及它如何工作。

## Workflow

### 1. Inspect

- 在执行明显有副作用的动作之前，先读取顶层清单文件、锁文件、README、环境变量文件和主要配置文件。
- 确定项目类型、包管理器、主要脚本、可能的入口、默认端口，以及是否依赖私有源、本地 tarball 或 workspace 包。
- 即使仓库里已经有安装产物或生成文件，也不要直接假定它们是有效的，必须以后续验证结果为准。

### 2. Install

- 使用锁文件或项目脚本所对应的包管理器。
- 优先使用尊重锁文件的安装命令，例如 `pnpm install --frozen-lockfile`、`npm ci` 或最接近的等价命令。
- 默认保留现有 registry 配置。如果安装因为 registry 不可达而失败，先明确报告具体错误，再尝试用单次命令覆盖 registry，而不是直接改项目配置。
- 允许正常的 setup hook 运行，除非某个 hook 明显不是必需且会阻塞流程。

### 3. Start

- 从项目脚本和文档中选择最标准的本地启动命令。
- 启动当前 workspace 最主要的开发服务，或者对当前任务最有价值的验证进程。
- 如果沙箱限制导致无法绑定端口或访问所需网络，应申请必要权限，而不是为了适配环境去改项目配置。
- 记录真实的 URL、端口以及任何编译或运行时诊断信息。

### 4. Verify

- 等待第一次成功编译或 ready 信号。
- 在可能的情况下执行轻量级验证，比如 `curl -I`、健康检查接口，或者直接依据进程输出中的 ready 信息。
- 明确区分以下结果：
  - 项目已经成功运行
  - 前端已运行，但上游 API 或内网服务不可达
  - 依赖安装失败
  - 项目已启动，但编译失败

### 5. Report

- 报告实际使用的安装命令和启动命令。
- 报告已验证的本地 URL 和端口。
- 总结技术栈、关键脚本、关键配置文件、主要业务模块，以及代理或环境变量地址这类重要运行时依赖。
- 简洁指出阻塞项、注意事项和下一步，不要堆砌废话。

## Guardrails

- 把 `/pi` 和 `/project-init` 视为这个工作流的显式快捷触发词。
- 尽量少改动，默认不修改应用业务源码。
- 这是一个“启动与验证”工作流，不是重构或清理工作流。
- 不要碰数据库、迁移、共享包或无关配置，除非用户明确要求。
- 如果项目依赖私有网络、本地服务或公司内网资源，必须在最终输出中明确说明。
