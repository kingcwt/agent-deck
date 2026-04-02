#!/usr/bin/env python3
"""Render single-source skill files into Codex and Claude artifacts."""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
DIST_DIR = ROOT / "dist"


def split_frontmatter(raw_text: str) -> tuple[dict[str, str], str]:
    """Parse a minimal frontmatter block with single-line key/value pairs."""
    if not raw_text.startswith("---\n"):
        raise ValueError("source file must start with frontmatter")

    _, frontmatter, body = raw_text.split("---", 2)
    metadata: dict[str, str] = {}

    for raw_line in frontmatter.strip().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {raw_line}")
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")

    return metadata, body.lstrip()


def require(metadata: dict[str, str], key: str) -> str:
    """Fail early if a required metadata field is missing."""
    value = metadata.get(key, "").strip()
    if not value:
        raise ValueError(f"missing required metadata field: {key}")
    return value


def split_csv(metadata: dict[str, str], key: str) -> list[str]:
    """Parse a comma-separated metadata field into a cleaned list."""
    raw = require(metadata, key)
    return [item.strip() for item in raw.split(",") if item.strip()]


def render_codex_alias(alias: str, metadata: dict[str, str], body: str) -> None:
    """Render Codex SKILL.md and UI metadata from the shared source file."""
    target_dir = DIST_DIR / "codex" / alias
    agents_dir = target_dir / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)

    skill_md = "\n".join(
        [
            "---",
            f"name: {alias}",
            f"description: {require(metadata, 'description')}",
            "---",
            "",
            body.rstrip(),
            "",
        ]
    )
    (target_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

    openai_yaml = "\n".join(
        [
            "interface:",
            f'  display_name: "{require(metadata, "display_name")}"',
            f'  short_description: "{require(metadata, "short_description")}"',
            f'  default_prompt: "{require(metadata, "default_prompt")}"',
            "policy:",
            f'  allow_implicit_invocation: {metadata.get("allow_implicit_invocation", "false").lower()}',
            "",
        ]
    )
    (agents_dir / "openai.yaml").write_text(openai_yaml, encoding="utf-8")


def render_codex(metadata: dict[str, str], body: str) -> None:
    """Render all configured Codex aliases from one source skill."""
    for alias in split_csv(metadata, "codex_names"):
        render_codex_alias(alias, metadata, body)


def render_claude_skill_alias(alias: str, metadata: dict[str, str], body: str) -> None:
    """Render a Claude-compatible skill folder from the shared source file."""
    target_dir = DIST_DIR / "claude" / "skills" / alias
    target_dir.mkdir(parents=True, exist_ok=True)

    skill_md = "\n".join(
        [
            "---",
            f"name: {alias}",
            f"description: {require(metadata, 'description')}",
            "---",
            "",
            body.rstrip(),
            "",
        ]
    )
    (target_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")


def render_claude_skills(metadata: dict[str, str], body: str) -> None:
    """Render all configured Claude skill aliases from one source skill."""
    for alias in split_csv(metadata, "claude_skill_names"):
        render_claude_skill_alias(alias, metadata, body)


def render_claude_alias(alias: str, metadata: dict[str, str], body: str) -> None:
    """Render a Claude Code custom command prompt from the same source file."""
    target_dir = DIST_DIR / "claude" / "commands"
    target_dir.mkdir(parents=True, exist_ok=True)

    command_md = "\n".join(
        [
            f"# /{alias}",
            "",
            "<!-- This file is generated from skills/*/source.md. Edit the source file instead. -->",
            "",
            "Execute the following workflow in the current working directory.",
            "Treat this command as the user's personal project bootstrap shortcut.",
            "",
            body.rstrip(),
            "",
        ]
    )
    (target_dir / f"{alias}.md").write_text(command_md, encoding="utf-8")


def render_claude(metadata: dict[str, str], body: str) -> None:
    """Render all configured Claude command aliases from one source skill."""
    for alias in split_csv(metadata, "claude_commands"):
        render_claude_alias(alias, metadata, body)


def main() -> None:
    """Rebuild dist/ from the source skill definitions."""
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    for source_path in sorted(SKILLS_DIR.glob("*/source.md")):
        raw_text = source_path.read_text(encoding="utf-8")
        metadata, body = split_frontmatter(raw_text)
        render_codex(metadata, body)
        render_claude_skills(metadata, body)
        render_claude(metadata, body)
        print(f"Rendered {require(metadata, 'name')}")


if __name__ == "__main__":
    main()
