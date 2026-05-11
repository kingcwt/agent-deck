#!/usr/bin/env python3
"""Render single-source skill files into Codex, Claude, and README artifacts."""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
DIST_DIR = ROOT / "dist"
README_CN = ROOT / "README.md"
README_EN = ROOT / "README.en.md"
GENERATED_SKILLS_BEGIN = "<!-- BEGIN GENERATED SKILLS -->"
GENERATED_SKILLS_END = "<!-- END GENERATED SKILLS -->"


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


def extract_section(markdown: str, heading: str) -> str:
    """Return the content of one level-2 markdown section."""
    lines = markdown.splitlines()
    collected: list[str] = []
    in_section = False

    for line in lines:
        if in_section and line.startswith("## "):
            break
        if in_section:
            collected.append(line)
            continue
        if line.strip() == f"## {heading}":
            in_section = True

    if not in_section:
        raise ValueError(f"missing section: {heading}")

    return "\n".join(collected).strip()


def format_aliases(items: list[str], command_prefix: str = "") -> str:
    """Render one alias list as comma-separated inline code tokens."""
    return ", ".join(f"`{command_prefix}{item}`" for item in items)


def render_skill_entry(metadata: dict[str, str], body: str, is_chinese: bool) -> str:
    """Render one README skill entry from a skill source body."""
    description = extract_section(body, "Description")
    parameters = extract_section(body, "Parameters")
    shortcuts = extract_section(body, "Shortcuts And Commands")
    examples = extract_section(body, "Examples")

    description_label = "技能描述：" if is_chinese else "Description:"
    parameters_label = "参数：" if is_chinese else "Parameters:"
    shortcuts_label = "快捷键和完整命令：" if is_chinese else "Shortcuts And Commands:"
    examples_label = "示例：" if is_chinese else "Examples:"

    return "\n".join(
        [
            f"### `{require(metadata, 'name')}`",
            "",
            description_label,
            "",
            description,
            "",
            parameters_label,
            "",
            parameters,
            "",
            shortcuts_label,
            "",
            shortcuts,
            "",
            examples_label,
            "",
            examples,
        ]
    ).rstrip()


def replace_generated_block(readme_path: Path, content: str) -> None:
    """Replace the generated skill block inside one README file."""
    raw = readme_path.read_text(encoding="utf-8")
    start = raw.find(GENERATED_SKILLS_BEGIN)
    end = raw.find(GENERATED_SKILLS_END)
    if start == -1 or end == -1 or end < start:
        raise ValueError(f"missing README markers in {readme_path}")

    updated = (
        raw[: start + len(GENERATED_SKILLS_BEGIN)]
        + "\n"
        + content.rstrip()
        + "\n"
        + raw[end:]
    )
    readme_path.write_text(updated, encoding="utf-8")


def render_readmes(skill_docs: list[tuple[dict[str, str], str, str]]) -> None:
    """Refresh the generated skill catalog blocks inside both READMEs."""
    cn_content = "\n\n".join(
        render_skill_entry(metadata, zh_body, is_chinese=True)
        for metadata, _, zh_body in skill_docs
    )
    en_content = "\n\n".join(
        render_skill_entry(metadata, en_body, is_chinese=False)
        for metadata, en_body, _ in skill_docs
    )
    replace_generated_block(README_CN, cn_content)
    replace_generated_block(README_EN, en_content)


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
            "Treat this command as the user's explicit shortcut for the workflow below.",
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
    """Rebuild dist/ and generated README sections from the source skills."""
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    skill_docs: list[tuple[dict[str, str], str, str]] = []
    for source_path in sorted(SKILLS_DIR.glob("*/source.md")):
        raw_text = source_path.read_text(encoding="utf-8")
        metadata, body = split_frontmatter(raw_text)
        zh_path = source_path.with_name("source.zh-CN.md")
        zh_body = zh_path.read_text(encoding="utf-8")
        render_codex(metadata, body)
        render_claude_skills(metadata, body)
        render_claude(metadata, body)
        skill_docs.append((metadata, body, zh_body))
        print(f"Rendered {require(metadata, 'name')}")

    render_readmes(skill_docs)
    print("Updated README skill catalogs")


if __name__ == "__main__":
    main()
