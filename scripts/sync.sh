#!/usr/bin/env bash
set -euo pipefail

# Resolve repository root so the script works from any current directory.
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Re-render generated artifacts from the single-source skill files.
python3 "$ROOT_DIR/scripts/render_skills.py"

# Remove the old bootstrap command names that existed before alias support.
rm -rf "$HOME/.codex/skills/init"
rm -f "$HOME/.claude/commands/init.md"
rm -rf "$HOME/.claude/skills/init"

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

echo "Synced skills to ~/.codex/skills, ~/.claude/skills, and ~/.claude/commands"
