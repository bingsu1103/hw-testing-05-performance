#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_dir"

expected_plans=(
  "test-plans/23120205_Load_20261117.jmx"
  "test-plans/23120205_Stress_20261117.jmx"
  "test-plans/23120205_Spike_20261117.jmx"
  "test-plans/23120205_Soak_20261117.jmx"
)

for plan in "${expected_plans[@]}"; do
  test -f "$plan"
  xmllint --noout "$plan"
done

header="$(head -n 1 data/users.csv)"
expected_header="email,password,search,product_id,product_name,product_price,quantity,total_amount,shipping_address"
if [[ "$header" != "$expected_header" ]]; then
  echo "Unexpected CSV header: $header" >&2
  exit 65
fi

grep -q 'ViewResultsFullVisualizer.*Load View - View Results Tree' test-plans/23120205_Load_20261117.jmx
grep -q 'SummaryReport.*Stress View - Summary Report' test-plans/23120205_Stress_20261117.jmx
grep -q 'StatVisualizer.*Spike View - Aggregate Report' test-plans/23120205_Spike_20261117.jmx

endpoints=(
  "/api/login"
  "/api/products"
  "/api/products/\${product_id}"
  "/api/cart"
  "/api/checkout"
)
for endpoint in "${endpoints[@]}"; do
  for plan in "${expected_plans[@]}"; do
    grep -Fq "$endpoint" "$plan"
  done
done

shellcheck scripts/*.sh
python3 -m py_compile scripts/analyze_jtl.py scripts/analyze_resources.py tests/test_analyze_jtl.py
python3 -m unittest discover -s tests -v
echo "Static validation passed for 4 JMeter plans, CSV data, endpoint coverage, scripts, and analyzer tests."

