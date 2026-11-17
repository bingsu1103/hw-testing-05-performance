#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
scenario="${1:-}"

case "$scenario" in
  load) plan="23120205_Load_20261117.jmx" ;;
  stress) plan="23120205_Stress_20261117.jmx" ;;
  spike) plan="23120205_Spike_20261117.jmx" ;;
  soak) plan="23120205_Soak_20261117.jmx" ;;
  *)
    echo "Usage: $0 {load|stress|spike|soak}" >&2
    exit 64
    ;;
esac

if ! command -v jmeter >/dev/null 2>&1; then
  echo "Apache JMeter is not installed or is not on PATH." >&2
  echo "Install JMeter 5.6.x, then rerun this command." >&2
  exit 69
fi

host="${JMETER_HOST:-localhost}"
port="${JMETER_PORT:-3000}"
protocol="${JMETER_PROTOCOL:-http}"
base_url="${protocol}://${host}:${port}"

if ! curl --fail --silent --show-error --max-time 5 "${base_url}/api/products" >/dev/null; then
  echo "SUT health check failed at ${base_url}/api/products." >&2
  echo "Start the backend and confirm that the API responds before generating evidence." >&2
  exit 69
fi

timestamp="$(date +%Y%m%d_%H%M%S)"
jtl_file="${repo_dir}/results/23120205_${scenario}_${timestamp}.jtl"
report_dir="${repo_dir}/reports/23120205_${scenario}_${timestamp}"
jmeter_log="${repo_dir}/results/23120205_${scenario}_${timestamp}.log"

mkdir -p "${repo_dir}/results" "${report_dir}"
cd "$repo_dir"

echo "Running ${scenario} against ${base_url}"
echo "JTL: ${jtl_file}"
echo "HTML report: ${report_dir}"

jmeter -n \
  -t "${repo_dir}/test-plans/${plan}" \
  -Jhost="$host" \
  -Jport="$port" \
  -Jprotocol="$protocol" \
  -Jcsv_file="${repo_dir}/data/users.csv" \
  -l "$jtl_file" \
  -j "$jmeter_log" \
  -e -o "$report_dir"

echo "Run finished. Keep the terminal, JMeter report, and resource monitor visible when capturing evidence."

