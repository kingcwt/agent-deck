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
echo "Installed kc-wh storage to ${WORKHOURS_DIR}"
