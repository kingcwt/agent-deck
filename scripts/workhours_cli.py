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


WEEKDAY_LABELS = {
    1: "周一",
    2: "周二",
    3: "周三",
    4: "周四",
    5: "周五",
    6: "周六",
    7: "周日",
}


def build_help_text() -> str:
    """Return the supported CLI usage text."""
    return "\n".join(
        [
            "Usage:",
            "  kc-wh",
            "  kc-wh '[<project>,<project>]'",
            "  kc-wh add <project> -m\"<message>\" [-am|-pm]",
            "",
            "Examples:",
            "  kc-wh",
            "  kc-wh '[cmc-ai,nice]'",
            "  kc-wh add 其他 -m\"开会1小时\"",
            "  kc-wh add 其他 -m\"开会1小时\" -am",
            "  kc-wh add 其他 -m\"需求评审\" -pm",
        ]
    )


def parse_project_filter(raw_filter: str) -> list[str]:
    """Parse the bracket project filter while keeping project names exact."""
    if not (raw_filter.startswith("[") and raw_filter.endswith("]")):
        raise SystemExit(f"Unsupported arguments: {shlex.quote(raw_filter)}")

    projects = [item.strip() for item in raw_filter[1:-1].split(",") if item.strip()]
    if not projects:
        raise SystemExit("Project filter cannot be empty.")
    return projects


def parse_cli(argv: list[str]) -> tuple[str, argparse.Namespace]:
    """Parse the small command surface without adding unrelated subcommands."""
    if not argv:
        return "export", argparse.Namespace(project_filter=None)

    if argv[0] in {"-h", "--help", "help"}:
        print(build_help_text())
        raise SystemExit(0)

    if len(argv) == 1 and argv[0].startswith("["):
        return "export", argparse.Namespace(project_filter=parse_project_filter(argv[0]))

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


def weekday_label(value: datetime.date) -> str:
    """Return the Chinese weekday label used by the legacy work-hours template."""
    return WEEKDAY_LABELS[value.isoweekday()]


def escape_markdown_cell(value: str) -> str:
    """Keep Markdown table cells stable when messages contain pipe characters."""
    return value.replace("|", "\\|").strip()


def render_halfday_table(entries: list[WorkRecord]) -> list[str]:
    """Render one half-day block using the legacy table layout."""
    lines = [
        "| 时间 | 项目 | 工作描述 |",
        "|------|------|----------|",
    ]
    for entry in sorted(entries, key=lambda item: item.commit_time):
        entry_time = entry.commit_time.strftime("%H:%M")
        for message_line in entry.message_lines:
            lines.append(
                "| "
                f"{entry_time} | "
                f"{escape_markdown_cell(entry.project)} | "
                f"{escape_markdown_cell(message_line)} |"
            )
    return lines


def iter_halfday_message_lines(entries: list[WorkRecord]) -> list[str]:
    """Return copy-friendly message lines in the same order as the table rows."""
    lines: list[str] = []
    for entry in sorted(entries, key=lambda item: item.commit_time):
        lines.extend(entry.message_lines)
    return lines


def render_halfday_copy_block(entries: list[WorkRecord]) -> list[str]:
    """Render plain message lines below each table so users can copy quickly."""
    return ["#### 复制文本", "", "```text", *iter_halfday_message_lines(entries), "```"]


def build_export_markdown(project_filter: list[str] | None = None) -> tuple[str, Path]:
    """Render the last 7 days and return both markdown and the Desktop file path."""
    ensure_storage_exists()

    now = datetime.now().astimezone()
    end_date = now.date()
    start_date = end_date - timedelta(days=6)
    records = parse_log_file()
    project_filter_set = set(project_filter or [])

    buckets: dict[tuple[str, str], list[WorkRecord]] = {}
    for record in records:
        local_time = record.commit_time.astimezone(now.tzinfo)
        record_date = local_time.date()
        if not (start_date <= record_date <= end_date):
            continue
        # Project filters are explicit opt-ins for export only; manual-add records
        # still preserve whatever project name the user typed.
        if project_filter_set and record.project not in project_filter_set:
            continue
        half = "上午" if local_time.hour < 12 else "下午"
        buckets.setdefault((record_date.isoformat(), half), []).append(
            WorkRecord(
                commit_time=local_time,
                project=record.project,
                message_lines=record.message_lines,
            )
        )

    included_dates = sorted(
        {
            record.commit_time.date()
            for entries in buckets.values()
            for record in entries
        }
    )
    unique_projects = sorted(
        {
            record.project
            for entries in buckets.values()
            for record in entries
        }
    )
    total_rows = sum(
        len(record.message_lines)
        for entries in buckets.values()
        for record in entries
    )

    lines = [
        "# 工时记录",
        "",
        f"**统计周期**：{start_date.isoformat()}（{weekday_label(start_date)}）～ {end_date.isoformat()}（{weekday_label(end_date)}）",
        f"**导出时间**：{now.strftime('%Y-%m-%d %H:%M')}",
    ]
    if project_filter:
        lines.append(f"**筛选项目**：{'、'.join(project_filter)}")
    lines.extend(["", "---", ""])
    if not included_dates:
        lines.append("暂无工时记录")
    else:
        for current_date in included_dates:
            date_key = current_date.isoformat()
            lines.append(f"## {date_key} {weekday_label(current_date)}")
            lines.append("")
            for half in ("上午", "下午"):
                entries = buckets.get((date_key, half), [])
                if not entries:
                    continue
                lines.append(f"### {half}")
                lines.append("")
                lines.extend(render_halfday_table(entries))
                lines.append("")
                lines.extend(render_halfday_copy_block(entries))
                lines.append("")

        lines.extend(
            [
                "---",
                "",
                f"**合计记录**：{total_rows} 条",
                f"**涉及项目**：{'、'.join(unique_projects)}",
            ]
        )

    markdown = "\n".join(lines).rstrip() + "\n"
    # Include filtered project names in the file name so a partial export does
    # not overwrite the all-project export for the same 7-day window.
    project_suffix = ""
    if project_filter:
        safe_projects = "_".join(project.replace("/", "-") for project in project_filter)
        project_suffix = f"_{safe_projects}"
    export_path = Path.home() / "Desktop" / f"工时记录_近7天{project_suffix}_{start_date.isoformat()}_{end_date.isoformat()}.md"
    return markdown, export_path


def export_markdown(project_filter: list[str] | None = None) -> str:
    """Write the markdown export file and return a user-facing result summary."""
    markdown, export_path = build_export_markdown(project_filter)
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
        print(export_markdown(args.project_filter), end="")
        return

    print(append_manual_record(args))


if __name__ == "__main__":
    main()
