#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
sut_dir="${SUT_DIR:-${repo_dir}/sut/eshop-sut}"
output_dir="${repo_dir}/evidence/issues"
mkdir -p "$output_dir"

backend_pid=""
cleanup() {
  if [[ -n "$backend_pid" ]]; then kill "$backend_pid" 2>/dev/null || true; fi
}
trap cleanup EXIT INT TERM

git -C "$sut_dir" restore backend/database.sqlite
node "${sut_dir}/backend/server.js" > "${output_dir}/reproduction-backend.log" 2>&1 &
backend_pid=$!
for _ in {1..30}; do
  if curl --fail --silent --max-time 2 http://localhost:3000/api/products >/dev/null; then break; fi
  sleep 1
done
curl --fail --silent --max-time 2 http://localhost:3000/api/products >/dev/null

email="flow2-coupon-repro-$(date +%s)@example.test"
password="Flow2Pass123!"
register_json="$(curl --fail --silent -H 'Content-Type: application/json' \
  -d "{\"name\":\"Flow 2 Coupon Reproduction\",\"email\":\"${email}\",\"password\":\"${password}\"}" \
  http://localhost:3000/api/register)"
user_id="$(jq -r .id <<< "$register_json")"

login_json="$(curl --fail --silent -H 'Content-Type: application/json' \
  -d "{\"email\":\"${email}\",\"password\":\"${password}\"}" \
  http://localhost:3000/api/login)"
token="$(jq -r .token <<< "$login_json")"

search_json="$(curl --fail --silent --get --data-urlencode 'search=iPhone' http://localhost:3000/api/products)"
detail_json="$(curl --fail --silent http://localhost:3000/api/products/1)"
curl --fail --silent -H 'Content-Type: application/json' \
  -H "Authorization: Bearer ${token}" \
  -d '{"id":1,"name":"iPhone 15 Pro Max","price":30000000,"quantity":1}' \
  http://localhost:3000/api/cart >/dev/null

total_amount=30000000
expected_discount=3000000
expected_final=27000000
coupon_json="$(curl --fail --silent -H 'Content-Type: application/json' \
  -d "{\"code\":\"SAVE10\",\"total_amount\":${total_amount},\"user_id\":${user_id}}" \
  http://localhost:3000/api/apply-coupon)"
actual_discount="$(jq -r .discount_amount <<< "$coupon_json")"
actual_final="$(jq -r .final_amount <<< "$coupon_json")"

if [[ "$actual_discount" == "$expected_discount" && "$actual_final" == "$expected_final" ]]; then
  echo "SAVE10 behaved correctly; refusing to create false bug evidence." >&2
  exit 1
fi

{
  echo "Reproduced at: $(date -Iseconds)"
  echo "SUT commit: $(git -C "$sut_dir" rev-parse HEAD)"
  echo "Flow 2 steps exercised: register -> login -> search -> detail -> cart -> apply coupon"
  echo "Registered user ID: ${user_id} (email and token omitted)"
  echo "Search result count: $(jq 'length' <<< "$search_json")"
  echo "Product detail ID/price: $(jq -c '{id,price}' <<< "$detail_json")"
  echo "Coupon seed: SAVE10, type=percent, discount_value=10"
  echo "Original total: ${total_amount}"
  echo "Expected 10% discount: ${expected_discount}"
  echo "Expected final amount: ${expected_final}"
  echo "Actual response: $(jq -c . <<< "$coupon_json")"
  echo "Actual discount: ${actual_discount}"
  echo "Actual final amount: ${actual_final}"
  echo "Result: percentage coupon is calculated as total * (1 - 10), producing a negative discount and inflated final amount."
} > "${output_dir}/save10-percent-calculation-reproduction.txt"

echo "Flow 2 coupon issue reproduction saved under ${output_dir}"
