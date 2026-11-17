#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
output="${repo_dir}/evidence/hardware-spec.txt"

{
  echo "Captured at: $(date -Iseconds)"
  echo "Hostname: $(hostname)"
  echo
  sw_vers
  echo
  system_profiler SPHardwareDataType
} > "$output"

echo "Hardware specification saved to $output"
echo "Also capture a screenshot showing the hostname and Activity Monitor for attributable evidence."

