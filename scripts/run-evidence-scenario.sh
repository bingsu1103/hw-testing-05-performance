#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
sut_dir="${SUT_DIR:-${repo_dir}/sut/eshop-sut}"
scenario="${1:-}"

case "$scenario" in
  load) label="Load" ;;
  stress) label="Stress" ;;
  spike) label="Spike" ;;
  soak) label="Soak" ;;
  *) echo "Usage: $0 {load|stress|spike|soak}" >&2; exit 64 ;;
esac

plan="${repo_dir}/test-plans/23120205_${label}_20261117.jmx"
stem="23120205_${label}_20261117"
jtl="${repo_dir}/results/${stem}.jtl"
jmeter_log="${repo_dir}/results/${stem}.log"
backend_log="${repo_dir}/results/${stem}_backend.log"
report_dir="${repo_dir}/reports/${stem}"
metrics="${repo_dir}/evidence/resource-metrics/${stem}.csv"
analysis="${repo_dir}/evidence/analysis/${stem}.md"
metadata="${repo_dir}/evidence/run-metadata/${stem}.txt"

for path in "$jtl" "$jmeter_log" "$backend_log" "$report_dir" "$metrics" "$analysis" "$metadata"; do
  if [[ -e "$path" ]]; then
    echo "Refusing to overwrite existing evidence: $path" >&2
    exit 73
  fi
done

if [[ ! -d "${sut_dir}/.git" ]]; then
  echo "SUT clone not found at ${sut_dir}; run ./scripts/setup-sut.sh first." >&2
  exit 69
fi
command -v jmeter >/dev/null
command -v node >/dev/null

mkdir -p "${repo_dir}/results" "$report_dir" \
  "${repo_dir}/evidence/resource-metrics" \
  "${repo_dir}/evidence/analysis" \
  "${repo_dir}/evidence/run-metadata"

# Restore the tracked demo database so every scenario starts comparably.
git -C "$sut_dir" restore backend/database.sqlite

cleanup() {
  if [[ -n "${sampler_pid:-}" ]]; then kill "$sampler_pid" 2>/dev/null || true; fi
  if [[ -n "${backend_pid:-}" ]]; then kill "$backend_pid" 2>/dev/null || true; fi
}
trap cleanup EXIT INT TERM

node "${sut_dir}/backend/server.js" > "$backend_log" 2>&1 &
backend_pid=$!

for _ in {1..30}; do
  if curl --fail --silent --max-time 2 http://localhost:3000/api/products >/dev/null; then break; fi
  sleep 1
done
curl --fail --silent --max-time 2 http://localhost:3000/api/products >/dev/null

{
  echo "scenario=${label}"
  echo "plan=${plan}"
  echo "plan_sha256=$(shasum -a 256 "$plan" | awk '{print $1}')"
  echo "test_assets_commit=$(git -C "$repo_dir" rev-parse HEAD)"
  echo "sut_commit=$(git -C "$sut_dir" rev-parse HEAD)"
  echo "hostname=$(hostname)"
  echo "timezone=$(date +%Z)"
  echo "started_at=$(date -Iseconds)"
  echo "jmeter_version=$(jmeter --version 2>&1 | tail -1)"
  echo "java_version=$(java -version 2>&1 | head -1)"
  echo "database_reset=git restore backend/database.sqlite"
} > "$metadata"

echo "timestamp,backend_cpu_pct,backend_mem_pct,backend_rss_kb,jmeter_cpu_pct,jmeter_mem_pct,jmeter_rss_kb" > "$metrics"
(
  while true; do
    backend_stats="$(ps -p "$backend_pid" -o %cpu=,%mem=,rss= 2>/dev/null | xargs || true)"
    jmeter_pid="$(pgrep -n -f 'ApacheJMeter.jar' || true)"
    jmeter_stats=""
    if [[ -n "$jmeter_pid" ]]; then
      jmeter_stats="$(ps -p "$jmeter_pid" -o %cpu=,%mem=,rss= 2>/dev/null | xargs || true)"
    fi
    read -r backend_cpu backend_mem backend_rss <<< "${backend_stats:-0 0 0}"
    read -r jmeter_cpu jmeter_mem jmeter_rss <<< "${jmeter_stats:-0 0 0}"
    printf '%s,%s,%s,%s,%s,%s,%s\n' "$(date -Iseconds)" \
      "${backend_cpu:-0}" "${backend_mem:-0}" "${backend_rss:-0}" \
      "${jmeter_cpu:-0}" "${jmeter_mem:-0}" "${jmeter_rss:-0}" >> "$metrics"
    sleep 2
  done
) &
sampler_pid=$!

cd "$repo_dir"
jmeter -n -t "$plan" \
  -Jcsv_file="${repo_dir}/data/users.csv" \
  -l "$jtl" -j "$jmeter_log" -e -o "$report_dir"

kill "$sampler_pid" 2>/dev/null || true
wait "$sampler_pid" 2>/dev/null || true
sampler_pid=""

echo "finished_at=$(date -Iseconds)" >> "$metadata"
python3 "${repo_dir}/scripts/analyze_jtl.py" "$jtl" > "$analysis"
python3 "${repo_dir}/scripts/analyze_resources.py" "$metrics" >> "$analysis"

echo "Completed ${label}."
echo "Raw JTL: ${jtl}"
echo "HTML report: ${report_dir}"
echo "Analysis: ${analysis}"

