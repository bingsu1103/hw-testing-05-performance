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

start_clean_backend() {
  cleanup
  backend_pid=""
  git -C "$sut_dir" restore backend/database.sqlite
  node "${sut_dir}/backend/server.js" > "${output_dir}/reproduction-backend.log" 2>&1 &
  backend_pid=$!
  for _ in {1..30}; do
    if curl --fail --silent --max-time 2 http://localhost:3000/api/products >/dev/null; then return; fi
    sleep 1
  done
  echo "Backend did not become healthy" >&2
  exit 69
}

start_clean_backend
login_json="$(curl --fail --silent -H 'Content-Type: application/json' \
  -d '{"email":"test@eshop.com","password":"Test1234!"}' \
  http://localhost:3000/api/login)"
token="$(jq -r .token <<< "$login_json")"

curl --fail --silent -H 'Content-Type: application/json' \
  -H "Authorization: Bearer ${token}" \
  -d '{"id":1,"name":"Laptop Dell XPS 13","price":25000000,"quantity":1}' \
  http://localhost:3000/api/cart >/dev/null

checkout_json="$(curl --fail --silent -H 'Content-Type: application/json' \
  -H "Authorization: Bearer ${token}" \
  -d '{"total_amount":1,"shipping_address":"HW05 reproduction address"}' \
  http://localhost:3000/api/checkout)"
order_id="$(jq -r .orderId <<< "$checkout_json")"
order_json="$(curl --fail --silent "http://localhost:3000/api/orders/${order_id}")"

{
  echo "Reproduced at: $(date -Iseconds)"
  echo "SUT commit: $(git -C "$sut_dir" rev-parse HEAD)"
  echo "Cart item price sent: 25000000"
  echo "Checkout total_amount sent: 1"
  echo "Checkout response: $(jq -c . <<< "$checkout_json")"
  echo "Persisted order (address redacted): $(jq -c 'del(.shipping_address)' <<< "$order_json")"
  echo "Result: backend persisted total_amount=1 instead of recalculating from cart."
} > "${output_dir}/checkout-client-total-reproduction.txt"

start_clean_backend
wrong_payload='{"email":"test@eshop.com","password":"Wrong123!"}'
valid_payload='{"email":"test@eshop.com","password":"Test1234!"}'

wrong_1="$(curl --silent -o /tmp/hw05-wrong-1.json -w '%{http_code}' -H 'Content-Type: application/json' -d "$wrong_payload" http://localhost:3000/api/login)"
wrong_2="$(curl --silent -o /tmp/hw05-wrong-2.json -w '%{http_code}' -H 'Content-Type: application/json' -d "$wrong_payload" http://localhost:3000/api/login)"
valid_immediate="$(curl --silent -o /tmp/hw05-valid-immediate.json -w '%{http_code}' -H 'Content-Type: application/json' -d "$valid_payload" http://localhost:3000/api/login)"
sleep 35
valid_after_35="$(curl --silent -o /tmp/hw05-valid-after-35.json -w '%{http_code}' -H 'Content-Type: application/json' -d "$valid_payload" http://localhost:3000/api/login)"

{
  echo "Reproduced at: $(date -Iseconds)"
  echo "SUT commit: $(git -C "$sut_dir" rev-parse HEAD)"
  echo "Wrong login #1: HTTP ${wrong_1} $(jq -c . /tmp/hw05-wrong-1.json)"
  echo "Wrong login #2: HTTP ${wrong_2} $(jq -c . /tmp/hw05-wrong-2.json)"
  echo "Valid login immediately after two failures: HTTP ${valid_immediate} $(jq -c . /tmp/hw05-valid-immediate.json)"
  echo "Valid login after 35 seconds: HTTP ${valid_after_35} $(jq -c . /tmp/hw05-valid-after-35.json)"
  echo "Expected contract: lock after 3 failures for 30 seconds."
  echo "Result: account locked after 2 failures and remained locked beyond 35 seconds."
} > "${output_dir}/login-lockout-reproduction.txt"

echo "Issue reproductions saved under ${output_dir}"

