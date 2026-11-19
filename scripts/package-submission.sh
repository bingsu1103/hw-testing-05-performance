#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
student_id="23120205"
grade="085"
archive_name="${student_id}_HW05_AI_Performance_${grade}_INCOMPLETE.zip"
stage_dir="$(mktemp -d)"
package_root="${stage_dir}/${student_id}_HW05_AI_Performance_${grade}_INCOMPLETE"

cleanup() {
  rm -rf "${stage_dir}"
}
trap cleanup EXIT

mkdir -p "${repo_root}/submission" "${package_root}"

copy_items=(
  README.md
  git-commit-log.txt
  docs
  test-plans
  data
  results
  reports
  evidence
  agent-skill
  scripts
  output/pdf/23120205_HW05_Performance_Report.pdf
  submission/MISSING_MANUAL_ITEMS.md
)

for item in "${copy_items[@]}"; do
  if [[ ! -e "${repo_root}/${item}" ]]; then
    printf 'Missing required package item: %s\n' "${item}" >&2
    exit 1
  fi
  mkdir -p "${package_root}/$(dirname "${item}")"
  cp -R "${repo_root}/${item}" "${package_root}/${item}"
done

find "${package_root}" -name '.DS_Store' -delete
find "${package_root}" -type d -name '__pycache__' -prune -exec rm -rf {} +
rm -rf "${package_root}/evidence/discarded"
rm -rf "${package_root}/docs/superpowers"
find "${package_root}/results" -type f ! -name '23120205_*_20261119.jtl' ! -name '23120205_*_20261119.log' -delete

rm -f "${repo_root}/submission/${archive_name}"
(
  cd "${stage_dir}"
  zip -qr "${repo_root}/submission/${archive_name}" "$(basename "${package_root}")"
)

printf '%s\n' "${repo_root}/submission/${archive_name}"
