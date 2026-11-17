# HW05 - Performance Testing Report

**Student:** Ngô Gia An - 23120205
**SUT:** EShop (`ttbhanh/eshop-sut`) at `85af3ba875c88283615e22cb108f13e2fccaf0e9`
**Execution:** 2026-11-17, Asia/Ho_Chi_Minh, hostname `my-mac`

> AI Audit, AI prompt log, and the separately required AI-focused report are intentionally excluded. Every performance value below was calculated from preserved raw JTL files.

## 1. Scope and workflow

All scenarios execute the same CSV-driven journey:

1. `POST /api/login` - authentication-heavy; extract and assert JWT.
2. `GET /api/products?search=...` - read-heavy search.
3. `GET /api/products/:id` - read-heavy detail.
4. `POST /api/cart` - authenticated transaction.
5. `POST /api/checkout` - authenticated SQLite order write.

CSV rows parameterize credentials, searches, products, quantities, totals, and addresses. Every request asserts HTTP 200; login additionally requires a non-empty JWT. The student must still confirm this workflow is not duplicated by another group member.

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

Before each run, the tracked SUT database was restored, the backend restarted and health-checked, and a new JTL/report directory created. Plan hash, commits, hostname, timezone, timestamps, and reset procedure are under `evidence/run-metadata/`.

## 3. Human review and correction

The first measured Load execution reported 15.8% errors. Raw-log inspection showed periodic invalid credentials and unresolved `${product_id}`. Declaring CSV variable names explicitly did not remove the pattern. A line-count check then found a trailing empty CSV record; every fourth read returned empty variables, explaining the exact 25% login failures and downstream errors.

Both invalid executions were preserved under the Git-ignored `evidence/discarded/` directory and excluded from final results. The empty record was removed, then an eight-iteration recycle smoke test produced 40/40 successful samples before the final Load run. This demonstrates why errors must be classified from raw evidence before attributing them to the SUT.

Thread Group names were also changed to display effective property values, preventing overridden smoke runs from misleadingly showing default concurrency.

## 4. Scenario design

| Scenario | Users | Ramp-up | Iterations/duration | Distinct view |
|---|---:|---:|---:|---|
| Load | 20 | 60 s | 5 iterations/user | View Results Tree |
| Stress | 80 | 120 s | 10 iterations/user | Summary Report |
| Spike | 150 | 5 s | 3 iterations/user | Aggregate Report |
| Soak | 25 | 60 s | 720 seconds | Summary Report |

A random 0.5-2.0 second think time separates requests. Load models normal concurrency; Stress raises sustained writes; Spike starts 150 users rapidly; Soak holds 25 users for 12 minutes.

## 5. Consolidated results

| Scenario | Samples | Errors | Throughput | Mean | p95 | p99 | Max |
|---|---:|---:|---:|---:|---:|---:|---:|
| Load | 500 | 0 (0.00%) | 5.79 req/s | 12.37 ms | 19 ms | 307 ms | 522 ms |
| Stress | 4,000 | 0 (0.00%) | 22.06 req/s | 5.23 ms | 11 ms | 70 ms | 441 ms |
| Spike | 2,250 | 0 (0.00%) | 84.82 req/s | 4.69 ms | 15 ms | 90 ms | 176 ms |
| Soak | 13,701 | 0 (0.00%) | 19.08 req/s | 4.68 ms | 7 ms | 26 ms | 1,320 ms |

The non-monotonic latency is not interpreted as higher load making the SUT faster. Scenarios have different timing, and short localhost calls are sensitive to scheduling/JIT outliers. Therefore p95, p99, per-label results, errors, and resources are considered together.

## 6. Load

All 500 samples succeeded. Overall p95 was 19 ms and p99 307 ms. Checkout had the highest label p95 (59 ms); product search reached the 522 ms maximum. Backend CPU averaged 1.33% and peaked at 4.20%; backend RSS averaged 28.57 MiB and peaked at 51.75 MiB. JMeter RSS peaked at 212.11 MiB. With 0% errors and p95 below 20 ms, this profile was stable.

## 7. Stress

All 4,000 samples succeeded at 22.06 req/s whole-run throughput. Overall p95 was 11 ms and p99 70 ms. Checkout was slowest by label p95 (15 ms) and reached the 441 ms maximum. Backend CPU averaged 4.21%, peaked at 14.10%, and backend RSS peaked at 60.33 MiB. JMeter RSS peaked at 260.28 MiB.

No saturation point was reached: error rate stayed 0%, tail latency stayed bounded, and CPU/RAM were not exhausted. This is a verified error-free operating point, not an absolute capacity ceiling.

## 8. Spike

The plan started 150 users over five seconds and completed 2,250 samples in about 27 seconds. It achieved 84.82 req/s with zero errors. Overall p95 was 15 ms, p99 90 ms, and max 176 ms. Checkout had the highest label p95 (24 ms).

Backend CPU peaked at 17.50% and RSS at 74.97 MiB. JMeter CPU reached 167.80% under macOS multi-core accounting and RSS peaked at 259.50 MiB. All threads finished, so the SUT recovered without an error tail.

## 9. Soak and endurance threshold

The Soak ran the full 720 seconds and produced 13,701 successful samples. Whole-run throughput was 19.08 req/s; after ramp-up, 30-second windows stayed near 19-20 req/s. Overall p95 was 7 ms and p99 26 ms. Two isolated excursions occurred (max 1,320 ms), but later windows returned to normal without errors or throughput loss.

Backend CPU averaged 3.72% and peaked at 23.60%; backend RSS peaked at 51.53 MiB. First-20-sample backend RSS averaged 24.63 MiB and last-20 averaged 34.81 MiB (+10.18 MiB). JMeter changed +1.05 MiB. The backend change includes ramp-up/cache/cart state and did not correlate with rising p95, but a multi-hour run would be required to rule out slow growth.

The verified endurance threshold is **at least 19.08 req/s at 25 concurrent users for 12 minutes, with 0% errors, p95 7 ms, p99 26 ms, and backend RSS no higher than 51.53 MiB**. The 84.82 req/s Spike result is an error-free burst, not a sustainable threshold.

## 10. Ten raw-log cross-check values

1. Load samples: 500.
2. Load errors: 0.
3. Load p95: 19 ms.
4. Stress samples: 4,000.
5. Stress throughput: 22.06 req/s.
6. Stress checkout p95: 15 ms.
7. Spike throughput: 84.82 req/s.
8. Spike p99: 90 ms.
9. Soak samples: 13,701.
10. Soak p95 / error rate: 7 ms / 0.00%.

## 11. Reproduced issues

### Checkout trusts client total

From a clean database, an item priced 25,000,000 VND was added, checkout submitted `total_amount=1`, and the persisted order was read. The server returned success and stored `total_amount=1`, violating FR-08 and compromising integrity. Sanitized evidence is in `evidence/issues/checkout-client-total-reproduction.txt`.

GitHub Issue: `[insert after publication]`

### Lockout triggers early and lasts too long

From a clean database, two incorrect passwords were followed by a correct password. The valid attempt returned HTTP 403 immediately and again after 35 seconds. FR-02 requires three failures and 30 seconds. Evidence is in `evidence/issues/login-lockout-reproduction.txt`.

GitHub Issue: `[insert after publication]`

Both issues were reproduced separately through public APIs; neither was inferred from a performance failure.

## 12. Continuous Performance Testing

Performance-sensitive changes should trigger functional smoke checks and a bounded Load test on a fixed self-hosted runner. The gate parses raw JTL and checks error rate, absolute p95, and regression against a comparable accepted baseline. A regression is repeated once on the same runner; both attempts are retained.

Docs-only changes are skipped with a recorded reason. Stress runs nightly; Spike and Soak run weekly or before release. Each baseline stores JTL, plan, CSV identity, commits, machine, tool versions, and reset procedure.

This balances feedback speed against runner cost and false alarms caused by OS scheduling, JIT warm-up, SQLite state, or contention. Path filters, clean resets, one controlled rerun, and per-label metrics reduce noise. The complete flow chart is in `docs/CONTINUOUS_PERFORMANCE_TESTING.md`.

## 13. Conclusion

All final workloads completed with 0% errors. Spike delivered the highest burst throughput (84.82 req/s), while Soak verified 19.08 req/s sustained for 12 minutes. Checkout was the slowest p95 label in Stress, Spike, and Soak, although absolute localhost values remained low.

The first implementation priority is server-side total recalculation because it is a direct order-integrity defect. The second is correcting lockout counting and duration. A longer soak and stepwise increasing-load experiment should follow to locate absolute capacity and evaluate backend RSS growth.

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
