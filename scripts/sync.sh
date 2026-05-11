#!/usr/bin/env bash
set -euo pipefail

# Resolve repository root so the script works from any current directory.
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Re-render generated artifacts from the single-source skill files.
python3 "$ROOT_DIR/scripts/render_skills.py"

# Install the global kc-wh storage, CLI, and chained post-commit hook.
bash "$ROOT_DIR/scripts/install_workhours.sh"

# Remove retired bootstrap aliases so old entries do not linger in user installs.
rm -rf "$HOME/.codex/skills/init"
rm -rf "$HOME/.codex/skills/pi"
rm -rf "$HOME/.codex/skills/project-init"
rm -f "$HOME/.claude/commands/init.md"
rm -f "$HOME/.claude/commands/pi.md"
rm -f "$HOME/.claude/commands/project-init.md"
rm -rf "$HOME/.claude/skills/init"
rm -rf "$HOME/.claude/skills/pi"
rm -rf "$HOME/.claude/skills/project-init"

# Install Codex skills into the auto-discovered local skills directory.
mkdir -p "$HOME/.codex/skills"
for skill_dir in "$ROOT_DIR"/dist/codex/*; do
  [ -d "$skill_dir" ] || continue
  skill_name="$(basename "$skill_dir")"
  rm -rf "$HOME/.codex/skills/$skill_name"
  cp -R "$skill_dir" "$HOME/.codex/skills/$skill_name"
done

# Install Claude custom commands into the user's global commands directory.
mkdir -p "$HOME/.claude/commands"
for command_file in "$ROOT_DIR"/dist/claude/commands/*.md; do
  [ -f "$command_file" ] || continue
  cp "$command_file" "$HOME/.claude/commands/"
done

# Install Claude skills into the user's global Claude skills directory.
mkdir -p "$HOME/.claude/skills"
for skill_dir in "$ROOT_DIR"/dist/claude/skills/*; do
  [ -d "$skill_dir" ] || continue
  skill_name="$(basename "$skill_dir")"
  rm -rf "$HOME/.claude/skills/$skill_name"
  cp -R "$skill_dir" "$HOME/.claude/skills/$skill_name"
done

echo "Synced skills, commands, and kc-wh global workhours storage"
