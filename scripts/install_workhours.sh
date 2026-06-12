#!/usr/bin/env bash
set -euo pipefail

# Install the global kc-wh storage, CLI, and post-commit hook under ~/.agent-deck.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORKHOURS_DIR="${HOME}/.agent-deck/workhours"
HOOKS_DIR="${WORKHOURS_DIR}/hooks"
CLI_TARGET="${WORKHOURS_DIR}/workhours_cli.py"
HOOK_TARGET="${HOOKS_DIR}/post-commit"
PREVIOUS_HOOKS_PATH_FILE="${WORKHOURS_DIR}/previous-hooks-path"
NEW_HOOKS_PATH="${HOOKS_DIR}"

mkdir -p "${HOOKS_DIR}"
cp "${ROOT_DIR}/scripts/workhours_cli.py" "${CLI_TARGET}"
cp "${ROOT_DIR}/scripts/workhours_post_commit.sh" "${HOOK_TARGET}"
chmod +x "${CLI_TARGET}" "${HOOK_TARGET}"

# The log file is created lazily only when missing so installs do not destroy
# existing work-hour history.
touch "${WORKHOURS_DIR}/git-commit-log.txt"

current_hooks_path="$(git config --global --get core.hooksPath || true)"
if [ -n "${current_hooks_path}" ] && [ "${current_hooks_path}" != "${NEW_HOOKS_PATH}" ]; then
  printf '%s\n' "${current_hooks_path}" > "${PREVIOUS_HOOKS_PATH_FILE}"
fi

git config --global core.hooksPath "${NEW_HOOKS_PATH}"

# Fix local overrides: unset per-repo core.hooksPath so the global agent-deck
# hooks take effect. A local hooksPath pointing at a non-existent directory
# silently disables all hooks without warning.
local_hooks_path="$(git config --local --get core.hooksPath 2>/dev/null || true)"
if [ -n "${local_hooks_path}" ] && [ "${local_hooks_path}" != "${NEW_HOOKS_PATH}" ]; then
  echo "Found local core.hooksPath='${local_hooks_path}' in $(git rev-parse --show-toplevel), unsetting to use global agent-deck hooks"
  git config --local --unset core.hooksPath
fi

echo "Installed kc-wh storage to ${WORKHOURS_DIR}"
