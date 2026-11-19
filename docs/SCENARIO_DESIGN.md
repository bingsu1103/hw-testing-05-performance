# Scenario design

## Shared workflow

Every virtual-user iteration executes the same business journey:

1. `POST /api/register` - create a unique account and extract its user ID.
2. `POST /api/login` - authentication-heavy step; extract and assert the JWT.
3. `GET /api/products?search=...` - read-heavy product search.
4. `GET /api/products/:id` - read-heavy product detail.
5. `POST /api/cart` - authenticated transactional mutation.
6. `POST /api/apply-coupon` - apply `BIGBUY`, extract the coupon/final amount, and assert the CSV oracle.
7. `POST /api/checkout` - authenticated SQLite order write using the discounted amount.
8. `POST /api/coupon-usage` - persist coupon use as the final backend call made by the Checkout UI action.

This is the assigned Flow 2 (“Tìm kiếm + Mã giảm giá”). CSV rows parameterize the password, search term, product values, quantity, original total, coupon, expected discounted total, and shipping address. The plan generates a unique email from the scenario-run ID, thread number, and iteration so registration is repeatable without account collisions. A uniform 0.5-2.0 second timer applies between requests to avoid an unrealistically tight loop.

The CSV variable list is declared explicitly while `ignoreFirstLine=true`, and the data file must contain no blank record. A trailing empty record was found during measured execution because it produced periodic empty credentials and unresolved product IDs when JMeter recycled the file; it was removed before the final runs.

## Default load models

| Scenario | Users | Ramp-up | Iterations/duration | Intended observation | Listener/report view |
|---|---:|---:|---:|---|---|
| Load | 20 | 60 s | 5 iterations/user | Normal sustained concurrency and baseline p95 | View Results Tree |
| Stress | 80 | 120 s | 10 iterations/user | Saturation, SQLite write contention, error onset | Summary Report |
| Spike | 150 | 5 s | 3 iterations/user | Recovery and error behavior after a sudden surge | Aggregate Report |
| Soak | 25 | 60 s | 720 s | Memory growth, throughput stability, practical endurance threshold | Summary Report |

The values are starting hypotheses, not measured limits. Before the final evidence run, use a small smoke override and then tune the full values to the actual hardware while documenting every change.

## Safe overrides

JMeter properties make bounded validation possible without changing the plans:

```bash
jmeter -n -t test-plans/23120205_Load_20261119.jmx \
  -Jthreads=1 -Jramp_seconds=1 -Jloops=1 \
  -Jcsv_file="$PWD/data/users.csv" \
  -l results/smoke.jtl
```

For a different SUT location, add `-Jhost`, `-Jport`, and `-Jprotocol`.

## Assertions and known hazards

- Each request asserts HTTP 200. Registration, login, coupon application, and checkout also assert the extracted user ID, JWT, discounted final amount, and order ID respectively.
- The runner checks `/api/products` before starting, avoiding a meaningless full run against a stopped backend.
- Never use invalid credentials in the performance CSV. Each loop logs in with the account it has just registered, avoiding shared-account lockout contamination.
- Registration, checkout, and coupon usage write to SQLite on every iteration. Restore the tracked demo database between scenarios so one run does not contaminate the next.
- Measured runs use the valid fixed-value `BIGBUY` coupon. `SAVE10` is reserved for a separate functional reproduction because the SUT's percentage calculation is suspected to be defective.
- View Results Tree is required as one distinct view but is memory-heavy. Use it for GUI inspection/screenshot only; authoritative measurements come from non-GUI execution and the raw JTL.

