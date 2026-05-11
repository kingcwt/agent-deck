#!/usr/bin/env bash
set -euo pipefail

# This hook writes commit records into the agent-deck work-hour log, then
# delegates to the previously configured post-commit hook when one existed.

WORKHOURS_DIR="${HOME}/.agent-deck/workhours"
LOG_FILE="${WORKHOURS_DIR}/git-commit-log.txt"
PREVIOUS_HOOKS_PATH_FILE="${WORKHOURS_DIR}/previous-hooks-path"

repo="$(git rev-parse --show-toplevel 2>/dev/null || true)"
project_name="$(basename "${repo:-}")"
branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
hash="$(git rev-parse HEAD 2>/dev/null || true)"
author_name="$(git log -1 --pretty=format:%an 2>/dev/null || true)"
author_email="$(git log -1 --pretty=format:%ae 2>/dev/null || true)"
commit_time="$(git log -1 --pretty=format:%cI 2>/dev/null || true)"
subject="$(git log -1 --pretty=format:%s 2>/dev/null || true)"
body="$(git log -1 --pretty=format:%b 2>/dev/null || true)"
parents="$(git log -1 --pretty=format:%P 2>/dev/null || true)"
changed_files="$(git show --name-only --pretty=format: HEAD 2>/dev/null | sed '/^$/d')"
changed_stats="$(git show --shortstat --pretty=format: HEAD 2>/dev/null | tail -n 1)"

if [ -n "${hash}" ] && [ -n "${repo}" ]; then
  # Merge commits are skipped so the work-hour log stays closer to user-authored
  # task records instead of transport noise.
  if ! printf '%s' "${parents}" | grep -q ' '; then
    message="${subject}"
    if [ -n "${body}" ]; then
      message="${subject}
${body}"
    fi

    mkdir -p "${WORKHOURS_DIR}"
    {
      printf '%s\n' '-----'
      printf 'captured_at=%s\n' "$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
      printf 'commit_time=%s\n' "${commit_time}"
      printf 'project=%s\n' "${project_name}"
      printf 'repo=%s\n' "${repo}"
      printf 'branch=%s\n' "${branch}"
      printf 'hash=%s\n' "${hash}"
      printf 'author=%s <%s>\n' "${author_name}" "${author_email}"
      printf 'message<<EOF\n'
      printf '%s\n' "${message}"
      printf 'EOF\n'
      printf 'changed_files<<EOF\n'
      printf '%s\n' "${changed_files}"
      printf 'EOF\n'
      printf 'stats=%s\n' "${changed_stats}"
    } >> "${LOG_FILE}" 2>/dev/null || true
  fi
fi

# Chaining preserves the user's previous global post-commit behavior after the
# agent-deck hook has recorded the current commit.
if [ -f "${PREVIOUS_HOOKS_PATH_FILE}" ]; then
  previous_hooks_path="$(cat "${PREVIOUS_HOOKS_PATH_FILE}")"
  previous_hook="${previous_hooks_path}/post-commit"
  if [ -n "${previous_hooks_path}" ] && [ "${previous_hook}" != "$0" ] && [ -x "${previous_hook}" ]; then
    "${previous_hook}" || true
  fi
fi
