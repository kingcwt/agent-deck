#!/usr/bin/env python3
"""Export recent work-hour records or append one manual work-hour record."""

from __future__ import annotations

import argparse
import shlex
import sys
from dataclasses import dataclass
from datetime import UTC, datetime, time, timedelta
from pathlib import Path


STORAGE_DIR = Path.home() / ".agent-deck" / "workhours"
LOG_FILE = STORAGE_DIR / "git-commit-log.txt"


@dataclass
class WorkRecord:
    """One parsed work-hour record from the shared log."""

    commit_time: datetime
    project: str
    message_lines: list[str]


def build_help_text() -> str:
    """Return the supported CLI usage text."""
    return "\n".join(
        [
            "Usage:",
            "  kc-wh",
            "  kc-wh add <project> -m\"<message>\" [-am|-pm]",
            "",
            "Examples:",
            "  kc-wh",
            "  kc-wh add 其他 -m\"开会1小时\"",
            "  kc-wh add 其他 -m\"开会1小时\" -am",
            "  kc-wh add 其他 -m\"需求评审\" -pm",
        ]
    )


def parse_cli(argv: list[str]) -> tuple[str, argparse.Namespace]:
    """Parse the small command surface without adding unrelated subcommands."""
    if not argv:
        return "export", argparse.Namespace()

    if argv[0] in {"-h", "--help", "help"}:
        print(build_help_text())
        raise SystemExit(0)

    if argv[0] != "add":
        raise SystemExit(f"Unsupported arguments: {' '.join(shlex.quote(arg) for arg in argv)}")

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("project")
    parser.add_argument("-m", "--message", required=True)
    parser.add_argument("-am", action="store_true", dest="is_am")
    parser.add_argument("-pm", action="store_true", dest="is_pm")
    args = parser.parse_args(argv[1:])
    if args.is_am and args.is_pm:
        raise SystemExit("Use only one of -am or -pm.")
    return "add", args


def ensure_storage_exists() -> None:
    """Fail fast when the global storage is missing instead of inventing data."""
    if not LOG_FILE.exists():
        raise SystemExit(
            "Work-hour log not found. Rerun ./scripts/sync.sh or ./install.sh to install kc-wh storage."
        )


def parse_log_file() -> list[WorkRecord]:
    """Parse the shared log file and ignore incomplete legacy blocks safely."""
    records: list[WorkRecord] = []
    if not LOG_FILE.exists():
        return records

    lines = LOG_FILE.read_text(encoding="utf-8", errors="replace").splitlines()
    index = 0
    while index < len(lines):
        if lines[index].strip() != "-----":
            index += 1
            continue

        index += 1
        block: dict[str, str] = {}
        message: str | None = None

        while index < len(lines) and lines[index].strip() != "-----":
            line = lines[index]
            if line == "message<<EOF":
                index += 1
                message_lines: list[str] = []
                while index < len(lines) and lines[index] != "EOF":
                    if lines[index].strip() == "-----":
                        message = None
                        break
                    message_lines.append(lines[index])
                    index += 1
                if index >= len(lines) or lines[index] != "EOF":
                    message = None
                    break
                message = "\n".join(message_lines).strip()
                index += 1
                continue

            if line == "changed_files<<EOF":
                index += 1
                while index < len(lines) and lines[index] != "EOF":
                    if lines[index].strip() == "-----":
                        break
                    index += 1
                if index < len(lines) and lines[index] == "EOF":
                    index += 1
                continue

            if "=" in line:
                key, value = line.split("=", 1)
                block[key.strip()] = value.strip()
            index += 1

        commit_time = block.get("commit_time")
        project = block.get("project")
        if not commit_time or not project or message is None:
            continue

        try:
            parsed_time = datetime.fromisoformat(commit_time)
        except ValueError:
            continue

        cleaned_lines = clean_message_lines(message)
        if not cleaned_lines:
            continue

        records.append(WorkRecord(commit_time=parsed_time, project=project, message_lines=cleaned_lines))

    return records


def clean_message_lines(message: str) -> list[str]:
    """Keep each meaningful message line so export can preserve multi-line notes."""
    return [line.strip() for line in message.splitlines() if line.strip()]


def render_entry_lines(entry: WorkRecord) -> list[str]:
    """Render one entry, preserving multiple message lines when they exist."""
    if len(entry.message_lines) == 1:
        return [f"- `{entry.project}` {entry.message_lines[0]}"]

    lines = [f"- `{entry.project}`"]
    for message_line in entry.message_lines:
        # Indented sub-lines keep one commit's detailed notes readable in the file.
        lines.append(f"  - {message_line}")
    return lines


def build_export_markdown() -> tuple[str, Path]:
    """Render the last 7 days and return both markdown and the Desktop file path."""
    ensure_storage_exists()

    now = datetime.now().astimezone()
    end_date = now.date()
    start_date = end_date - timedelta(days=6)
    records = parse_log_file()

    buckets: dict[tuple[str, str], list[WorkRecord]] = {}
    for record in records:
        local_time = record.commit_time.astimezone(now.tzinfo)
        record_date = local_time.date()
        if not (start_date <= record_date <= end_date):
            continue
        half = "上午" if local_time.hour < 12 else "下午"
        buckets.setdefault((record_date.isoformat(), half), []).append(
            WorkRecord(
                commit_time=local_time,
                project=record.project,
                message_lines=record.message_lines,
            )
        )

    lines = [f"# 近7天工时记录（{start_date.isoformat()} ~ {end_date.isoformat()}）", ""]
    current_date = end_date
    while current_date >= start_date:
        date_key = current_date.isoformat()
        lines.append(f"## {date_key}")
        lines.append("")
        for half in ("上午", "下午"):
            lines.append(f"### {half}")
            entries = sorted(
                buckets.get((date_key, half), []),
                key=lambda item: item.commit_time,
            )
            if not entries:
                lines.append("- 无")
            else:
                for entry in entries:
                    lines.extend(render_entry_lines(entry))
            lines.append("")
        current_date -= timedelta(days=1)

    markdown = "\n".join(lines).rstrip() + "\n"
    export_path = Path.home() / "Desktop" / f"工时记录_近7天_{start_date.isoformat()}_{end_date.isoformat()}.md"
    return markdown, export_path


def export_markdown() -> str:
    """Write the markdown export file and return a user-facing result summary."""
    markdown, export_path = build_export_markdown()
    export_path.write_text(markdown, encoding="utf-8")
    return f"已导出到：{export_path}\n\n{markdown}"


def append_manual_record(args: argparse.Namespace) -> str:
    """Append one manual record into the same log format used by git commits."""
    ensure_storage_exists()

    now = datetime.now().astimezone()
    if args.is_am:
        record_time = datetime.combine(now.date(), time(9, 0), tzinfo=now.tzinfo)
        half = "上午"
    elif args.is_pm:
        record_time = datetime.combine(now.date(), time(14, 0), tzinfo=now.tzinfo)
        half = "下午"
    else:
        record_time = now
        half = "上午" if now.hour < 12 else "下午"

    captured_at = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    manual_hash = f"manual-{record_time.strftime('%Y%m%d%H%M%S')}"
    block = "\n".join(
        [
            "-----",
            f"captured_at={captured_at}",
            f"commit_time={record_time.isoformat()}",
            f"project={args.project}",
            "repo=manual",
            "branch=manual",
            f"hash={manual_hash}",
            "author=manual <manual>",
            "message<<EOF",
            args.message,
            "EOF",
            "changed_files<<EOF",
            "EOF",
            "stats=",
            "",
        ]
    )
    with LOG_FILE.open("a", encoding="utf-8") as handle:
        handle.write(block)

    return f"已添加：[{args.project}] {args.message} -> 今天{half}"


def main() -> None:
    """Dispatch the CLI to export mode or manual-add mode."""
    mode, args = parse_cli(sys.argv[1:])
    if mode == "export":
        print(export_markdown(), end="")
        return

    print(append_manual_record(args))


if __name__ == "__main__":
    main()
