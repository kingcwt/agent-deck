# Agent Deck

[English README](./README.en.md)

`agent-deck` 是一个面向 Codex 和 Claude Code 的单一源技能仓库。

你只维护一次工作流定义，然后生成并安装到多个目标：

- Codex skills
- Claude Code skills
- Claude Code slash commands

当前仓库地址：`https://github.com/kingcwt/agent-deck`

## 这个仓库解决什么问题

你不需要反复输入很长的提示词，比如“分析当前项目、安装依赖、启动、验证并输出项目说明”。

你只需要维护一组短指令，例如：

- Codex：`$pi` 或 `$project-init`
- Claude Code：`/pi` 或 `/project-init`

真正的工作流只写在一个源文件里，然后自动渲染成各个平台所需的格式。

## 当前已有技能

### `init`

用于项目初始化和基线分析。

同一个源文件会生成这些别名：

- Codex skills：`pi`、`project-init`
- Claude skills：`pi`、`project-init`
- Claude commands：`/pi`、`/project-init`

用途：

- 检查当前项目结构
- 识别包管理器和运行方式
- 安装依赖
- 启动主应用或开发服务
- 验证是否可访问
- 输出项目结构、技术栈和阻塞项说明

## 仓库结构

```text
agent-deck/
├── skills/
│   └── init/
│       └── source.md
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

- `skills/*/source.md`：技能唯一人工维护源文件
- `scripts/render_skills.py`：把源文件渲染成发布产物
- `scripts/sync.sh`：本地重新生成并安装到 Codex / Claude 目录
- `dist/`：生成产物；为了远程安装和公开发布，应该提交到 GitHub
- `install.sh`：本地或远程一键安装/更新入口
- `README.md`：默认中文说明
- `README.en.md`：英文说明

## 编写模型

每个技能只定义一次，写在 `source.md` 中。

元数据示例：

```md
---
name: init
display_name: Project Init
description: ...
short_description: ...
default_prompt: ...
codex_names: pi,project-init
claude_skill_names: pi,project-init
claude_commands: pi,project-init
allow_implicit_invocation: false
---
```

这样一个工作流就可以展开成多个别名，不需要复制正文。

## 本地开发

本地渲染并安装：

```bash
cd ~/Desktop/kingcwt/work/agent-deck
./scripts/sync.sh
```

这个命令会：

- 重建 `dist/`
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
2. 运行 `./scripts/sync.sh`
3. 在 Codex 和 Claude Code 中测试
4. 提交源文件和生成后的 `dist/`
5. 推送到 GitHub

之所以提交 `dist/`，是因为：

- 远程安装更稳定
- 其他用户可以直接检查生成产物
- 更容易被技能目录或安装工具消费

## 新增一个技能

1. 新建 `skills/<new-skill>/source.md`
2. 复制现有技能作为模板
3. 修改元数据和正文
4. 配置别名：
   - `codex_names: foo,bar`
   - `claude_skill_names: foo,bar`
   - `claude_commands: foo,bar`
5. 运行 `./scripts/sync.sh`
6. 提交源文件和新的 `dist/`

## 为什么 Claude 同时有 skills 和 commands

Claude Code 同时支持可复用技能和 slash commands，两者用途不同：

- Claude skills 用于能力复用和技能分发
- Claude commands 用于最短路径调用体验，例如 `/pi`

这个仓库会从同一个源文件同时生成两种产物，避免你维护两套重复逻辑。

## 备注

- Codex 更适合显式调用 skill，例如 `$pi`
- Claude 使用 `/pi` 和 `/project-init`
- Claude 侧故意不使用 `/init`，因为它容易与内置命令语义冲突
- 这个仓库的结构可以继续扩展到很多技能，不需要重构整体架构
