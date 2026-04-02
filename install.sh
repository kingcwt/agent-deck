#!/usr/bin/env bash
set -euo pipefail

# Install or update this skills repository into Codex and Claude directories.
# This script supports two modes:
# 1. Run inside a local checkout: ./install.sh
# 2. Run remotely: curl -fsSL <raw-install-url> | bash -s -- --repo owner/repo --ref main

REPO="${REPO:-}"
REF="${REF:-main}"
SOURCE_DIR=""
TMP_DIR=""

cleanup() {
  if [ -n "${TMP_DIR:-}" ] && [ -d "$TMP_DIR" ]; then
    rm -rf "$TMP_DIR"
  fi
}
trap cleanup EXIT

while [ "$#" -gt 0 ]; do
  case "$1" in
    --repo)
      REPO="$2"
      shift 2
      ;;
    --ref)
      REF="$2"
      shift 2
      ;;
    --source)
      SOURCE_DIR="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if [ -z "$SOURCE_DIR" ]; then
  if [ -f "./scripts/sync.sh" ] && [ -d "./skills" ]; then
    SOURCE_DIR="$(pwd)"
  elif [ -n "$REPO" ]; then
    TMP_DIR="$(mktemp -d)"
    ARCHIVE_URL="https://codeload.github.com/${REPO}/tar.gz/refs/heads/${REF}"
    curl -fsSL "$ARCHIVE_URL" | tar -xz -C "$TMP_DIR"
    SOURCE_DIR="$(find "$TMP_DIR" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
  else
    echo "Provide --repo owner/name when running remotely, or run inside a local checkout." >&2
    exit 1
  fi
fi

if [ ! -f "$SOURCE_DIR/scripts/sync.sh" ]; then
  echo "sync.sh not found in source directory: $SOURCE_DIR" >&2
  exit 1
fi

bash "$SOURCE_DIR/scripts/sync.sh"
