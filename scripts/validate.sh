#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_dir"

expected_plans=(
  "test-plans/23120205_Load_20261119.jmx"
  "test-plans/23120205_Stress_20261119.jmx"
  "test-plans/23120205_Spike_20261119.jmx"
  "test-plans/23120205_Soak_20261119.jmx"
)

for plan in "${expected_plans[@]}"; do
  test -f "$plan"
  xmllint --noout "$plan"
done

header="$(head -n 1 data/users.csv)"
expected_header="name_prefix,password,search,product_id,product_name,product_price,quantity,total_amount,coupon_code,expected_final_amount,shipping_address"
if [[ "$header" != "$expected_header" ]]; then
  echo "Unexpected CSV header: $header" >&2
  exit 65
fi

assert_listener() {
  local plan="$1"
  local guiclass="$2"
  local testname="$3"
  local found

  found="$(xmllint --xpath "boolean(//*[@guiclass='${guiclass}' and @testname='${testname}'])" "$plan")"
  if [[ "$found" != "true" ]]; then
    echo "Missing listener ${guiclass} / ${testname} in ${plan}" >&2
    exit 66
  fi
}

assert_listener test-plans/23120205_Load_20261119.jmx ViewResultsFullVisualizer "Load View - View Results Tree"
assert_listener test-plans/23120205_Stress_20261119.jmx SummaryReport "Stress View - Summary Report"
assert_listener test-plans/23120205_Spike_20261119.jmx StatVisualizer "Spike View - Aggregate Report"

endpoints=(
  "/api/register"
  "/api/login"
  "/api/products"
  "/api/products/\${product_id}"
  "/api/cart"
  "/api/apply-coupon"
  "/api/checkout"
  "/api/coupon-usage"
)
for endpoint in "${endpoints[@]}"; do
  for plan in "${expected_plans[@]}"; do
    grep -Fq "$endpoint" "$plan"
  done
done

shellcheck scripts/*.sh
python3 -m py_compile scripts/analyze_jtl.py scripts/analyze_resources.py tests/test_analyze_jtl.py tests/test_flow2_scope.py
python3 -m unittest discover -s tests -v
echo "Static validation passed for 4 JMeter plans, CSV data, endpoint coverage, scripts, and analyzer tests."

