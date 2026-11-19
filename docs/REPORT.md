# HW05 - Performance Testing Report

**Student:** Ngô Gia An - 23120205

**Assigned workflow:** Flow 2 - Tìm kiếm + Mã giảm giá

**SUT:** EShop (`ttbhanh/eshop-sut`) at `85af3ba875c88283615e22cb108f13e2fccaf0e9`

**Execution:** 2026-11-19, Asia/Ho_Chi_Minh, hostname `my-mac`

> AI Audit, AI prompt log, and the separately required AI-focused report are intentionally excluded. Every performance value below was calculated from preserved raw JTL files.

## 1. Scope and workflow

The supplied group table assigns the student **Flow 2 - Tìm kiếm + Mã giảm giá**:

1. `POST /api/register` - register a unique account for the current thread and iteration.
2. `POST /api/login` - authenticate and extract the JWT.
3. `GET /api/products?search=...` - search for a product.
4. `GET /api/products/:id` - view product detail.
5. `POST /api/cart` - add the product to the authenticated user's cart.
6. `POST /api/apply-coupon` - apply a coupon and extract `coupon_id` and `final_amount`.
7. `POST /api/checkout` - checkout using the extracted discounted amount.
8. `POST /api/coupon-usage` - record coupon usage after successful checkout.

Step 8 is the SUT-side completion of coupon application; it does not add a separate user-facing flow. The plans use unique accounts so repeated loops do not collide with existing registrations. Search, product ID, quantity, address, coupon, and expected final amount are CSV-driven. Every request asserts HTTP 200, while extractors/assertions also verify the IDs, token, discounted total, and order ID needed by later steps.

The flow-selection screenshot and its SHA-256 are recorded in `docs/FLOW_ASSIGNMENT.md`. The visible name column in that screenshot is blank, so a completed shared-table screenshot or group confirmation remains a manual submission item.

## 2. Environment and reproducibility

| Item | Recorded value |
|---|---|
| Machine | MacBook Air, Apple M2 |
| CPU / RAM | 8 cores (4 performance + 4 efficiency) / 8 GB |
| OS | macOS 26.6, build 25G72 |
| Java / JMeter | OpenJDK 25.0.5 / Apache JMeter 5.6.3 |
| Backend | Node.js/Express + SQLite, `localhost:3000` |
| Resource evidence | Backend and JMeter CPU/RSS sampled every 2 seconds |
| Percentile method | Nearest-rank over raw JTL `elapsed` |

Before every measured run, the tracked database was restored, the backend restarted and health-checked, and fresh JTL/log/HTML locations created. Plan hash, repository commits, hostname, timezone, timestamps, commands, and reset procedure are preserved under `evidence/run-metadata/`.

## 3. Human review and correction

The repository originally exercised a generic login-first purchase path. Comparing it with the supplied flow table found two scope gaps: it omitted registration and coupon application. That out-of-scope evidence was retired from the current branch, and the contract tests were written first to require the assigned Flow 2 API sequence.

A one-user smoke run then verified all eight backend calls before the measured scenarios. The measured workload uses the seeded `BIGBUY` fixed-value coupon because its expected total is deterministic. The seeded `SAVE10` percentage coupon was tested separately and revealed a real calculation defect; that defect is reported in Section 11 rather than allowing a known-invalid total into performance measurements.

## 4. Scenario design

| Scenario | Users | Ramp-up | Iterations/duration | Distinct view |
|---|---:|---:|---:|---|
| Load | 20 | 60 s | 5 iterations/user | View Results Tree |
| Stress | 80 | 120 s | 10 iterations/user | Summary Report |
| Spike | 150 | 5 s | 3 iterations/user | Aggregate Report |
| Soak | 25 | 60 s | 720 seconds | Summary Report |

A random 0.5-2.0 second think time separates requests. Load models normal concurrency; Stress raises sustained database work; Spike starts 150 users rapidly; Soak holds 25 users for 12 minutes. Thread count, ramp-up, loop count/duration, host, port, and CSV path remain overrideable for bounded validation.

## 5. Consolidated results

| Scenario | Samples | Errors | Throughput | Mean | p95 | p99 | Max |
|---|---:|---:|---:|---:|---:|---:|---:|
| Load | 800 | 0 (0.00%) | 7.56 req/s | 4.09 ms | 8 ms | 15 ms | 82 ms |
| Stress | 6,400 | 0 (0.00%) | 28.84 req/s | 2.61 ms | 6 ms | 18 ms | 215 ms |
| Spike | 3,600 | 0 (0.00%) | 94.22 req/s | 10.39 ms | 39 ms | 228 ms | 449 ms |
| Soak | 13,696 | 0 (0.00%) | 19.06 req/s | 5.92 ms | 7 ms | 22 ms | 2,285 ms |

The non-monotonic latency is not interpreted as higher load making the SUT faster. Each scenario has a different ramp/timing profile, and short localhost calls are sensitive to scheduling, garbage collection, and JIT outliers. Conclusions therefore combine p95, p99, per-label values, errors, throughput, and resource evidence.

## 6. Load

All 800 samples succeeded; each of the eight API labels contributed exactly 100 samples. Overall p95 was 8 ms and p99 15 ms. Coupon usage had the highest label p95 at 10 ms, while registration reached the 82 ms maximum. Backend CPU averaged 1.88% and peaked at 5.30%; backend RSS averaged 31.97 MiB and peaked at 40.45 MiB. JMeter RSS peaked at 168.91 MiB.

## 7. Stress

All 6,400 samples succeeded at 28.84 req/s whole-run throughput; each label contributed 800 samples. Overall p95 was 6 ms and p99 18 ms. Registration had the highest label p95 at 8 ms; coupon application reached the 215 ms maximum. Backend CPU averaged 4.33%, peaked at 14.90%, and backend RSS peaked at 59.64 MiB. JMeter RSS peaked at 260.78 MiB.

No saturation point was reached: error rate stayed 0%, tail latency stayed bounded, and CPU/RAM were not exhausted. This is a verified error-free operating point, not an absolute capacity ceiling.

## 8. Spike

The plan started 150 users over five seconds and completed 3,600 samples, 450 for each API label. It achieved 94.22 req/s with zero errors. Overall p95 was 39 ms, p99 228 ms, and max 449 ms. Checkout was the most affected operation, with label p95 172 ms and the overall maximum.

Backend CPU peaked at 22.90% and RSS at 66.56 MiB. JMeter CPU peaked at 94.90% and RSS at 240.20 MiB. All threads finished without an error tail, demonstrating recovery after the burst.

## 9. Soak and endurance threshold

The Soak ran for 12 minutes and produced 13,696 successful samples at 19.06 req/s. Overall p95 was 7 ms and p99 22 ms. Because the duration scheduler stops active threads at the deadline, per-label counts decrease slightly from registration (1,723) to coupon usage (1,700); this is expected and not missing evidence.

A short latency excursion around minute 7-8 produced the 2,285 ms maximum. Subsequent 30-second windows immediately returned to roughly 20 req/s with maximum latency between 27 and 71 ms, and no errors occurred. It is therefore treated as a recovered transient, not sustained degradation.

Backend CPU averaged 3.34% and peaked at 13.40%; backend RSS averaged 35.96 MiB and peaked at 59.36 MiB. The first 20 backend RSS samples averaged 34.29 MiB and the last 20 averaged 27.74 MiB (-6.55 MiB). JMeter changed from 81.48 MiB to 68.57 MiB (-12.91 MiB). No upward memory trend was observed during this 12-minute window.

The verified endurance threshold is **at least 19.06 req/s at 25 concurrent users for 12 minutes, with 0% errors, p95 7 ms, p99 22 ms, and backend RSS no higher than 59.36 MiB**. The 94.22 req/s Spike result is an error-free burst, not a sustainable threshold or absolute maximum.

## 10. Ten raw-log cross-check values

1. Load samples: 800.
2. Load errors: 0.
3. Load p95: 8 ms.
4. Stress samples: 6,400.
5. Stress throughput: 28.84 req/s.
6. Stress checkout p95: 7 ms.
7. Spike throughput: 94.22 req/s.
8. Spike checkout p95: 172 ms.
9. Soak samples: 13,696.
10. Soak p95 / error rate: 7 ms / 0.00%.

## 11. Reproduced Flow 2 issue

### SAVE10 percentage coupon inflates checkout total tenfold

From a clean database, the seeded `SAVE10` coupon was confirmed as `type=percent` with `discount_value=10`. Applying it to a 30,000,000 VND cart should produce a 3,000,000 VND discount and a 27,000,000 VND final amount. The API instead returned a -270,000,000 VND discount and a 300,000,000 VND final amount.

The observed calculation is consistent with treating the integer percentage `10` as a fraction in `total * (1 - discount_value)`. This finding was reproduced separately through public APIs and was not inferred from a performance failure. Sanitized requests/responses and the reproduction procedure are under `evidence/issues/`.

GitHub Issue: [#3 - SAVE10 percentage coupon inflates checkout total tenfold](https://github.com/bingsu1103/hw-testing-05-performance/issues/3)

## 12. Continuous Performance Testing

Performance-sensitive changes should trigger functional smoke checks and a bounded Load test on a fixed self-hosted runner. The gate parses raw JTL and checks error rate, absolute p95, and regression against a comparable accepted baseline. A regression is repeated once on the same runner; both attempts are retained.

Docs-only changes are skipped with a recorded reason. Stress runs nightly; Spike and Soak run weekly or before release. Each baseline stores JTL, plan, CSV identity, commits, machine, tool versions, and reset procedure. Path filters, clean resets, one controlled rerun, and per-label metrics reduce noise from OS scheduling, JIT warm-up, SQLite state, and contention. The complete flow chart is in `docs/CONTINUOUS_PERFORMANCE_TESTING.md`.

## 13. Conclusion

All final Flow 2 workloads completed with 0% errors. Spike delivered the highest burst throughput at 94.22 req/s, while Soak verified at least 19.06 req/s for 12 minutes. Checkout was the most latency-sensitive label during Spike, but recovered without an error tail. CPU and memory remained below host limits in all measured runs.

The first implementation priority is correcting percentage-coupon arithmetic and adding unit/API coverage for both percentage and fixed-value coupons. A longer soak and stepwise increasing-load experiment should then locate absolute capacity; current results intentionally make no maximum-capacity claim.

## 14. Self-assessment

| Criterion | Maximum | Current score | Evidence |
|---|---:|---:|---|
| Load | 30 | 30 | JMX, JTL, HTML, resource series |
| Stress | 20 | 20 | JMX, JTL, HTML, resource series |
| Spike | 20 | 20 | JMX, JTL, HTML, resource series |
| AI analysis/review | 10 | 0 | Intentionally left for student |
| Continuous proposal | 10 | 10 | Proposal and workflow |
| Agent Skill | 10 | 5 | Skill ready; own-voice demo remains manual |
| **Total** | **100** | **85** | |
