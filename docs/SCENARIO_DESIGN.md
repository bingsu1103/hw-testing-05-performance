# Scenario design

## Shared workflow

Every virtual-user iteration executes the same business journey:

1. `POST /api/login` - authentication-heavy step; extract and assert the JWT.
2. `GET /api/products?search=...` - read-heavy product search.
3. `GET /api/products/:id` - read-heavy product detail.
4. `POST /api/cart` - authenticated transactional mutation.
5. `POST /api/checkout` - authenticated SQLite order write.

CSV rows parameterize credentials, search terms, product values, quantities, totals, and shipping addresses. A uniform 0.5-2.0 second timer applies between requests to avoid an unrealistically tight loop.

The CSV variable list is declared explicitly while `ignoreFirstLine=true`. This is required because a blank variable list can make JMeter infer names from the first row but later recycle that header as data, producing periodic invalid credentials and unresolved product IDs.

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
jmeter -n -t test-plans/23120205_Load_20261117.jmx \
  -Jthreads=1 -Jramp_seconds=1 -Jloops=1 \
  -Jcsv_file="$PWD/data/users.csv" \
  -l results/smoke.jtl
```

For a different SUT location, add `-Jhost`, `-Jport`, and `-Jprotocol`.

## Assertions and known hazards

- Each request asserts HTTP 200; login additionally asserts that a JWT was extracted.
- The runner checks `/api/products` before starting, avoiding a meaningless full run against a stopped backend.
- Never use invalid credentials in the performance CSV. Three failed logins can lock an account; if this happens, stop the run, wait for/reset the lock, verify one manual login, and restart with a clean result file.
- Checkout writes an order on every iteration. Back up or reset the demo database between scenarios so one run does not contaminate the next.
- View Results Tree is required as one distinct view but is memory-heavy. Use it for GUI inspection/screenshot only; authoritative measurements come from non-GUI execution and the raw JTL.

