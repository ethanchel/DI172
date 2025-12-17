#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"

# Remove tracked macOS Finder files
find "$repo_root" -name '.DS_Store' -print0 | xargs -0 git -C "$repo_root" rm --cached --ignore-unmatch || true

# Remove tracked Python bytecode files
find "$repo_root" -name '*.pyc' -print0 | xargs -0 git -C "$repo_root" rm --cached --ignore-unmatch || true

echo "Index cleaned of .DS_Store and .pyc if present."
