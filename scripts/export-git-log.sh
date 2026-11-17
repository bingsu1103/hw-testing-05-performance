#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
git -C "$repo_dir" log --date=iso-strict --pretty=format:'%h | %ad | %an | %s' > "${repo_dir}/git-commit-log.txt"
echo >> "${repo_dir}/git-commit-log.txt"
echo "Git commit log exported to ${repo_dir}/git-commit-log.txt"

