# HW05 Performance Testing report

Student: **Ngô Gia An - 23120205**  
SUT commit: `[fill after real execution]`  
Test-assets commit: `[fill after real execution]`  
Execution date/time: `[fill]`  
Hostname/hardware: `[fill from attributable evidence]`

> This report skeleton intentionally contains no invented performance values. Replace every bracketed field from the raw JTL, generated report, and hardware/resource evidence.

## 1. Scope and workflow

The selected end-to-end workflow covers authentication (`POST /api/login`), read-heavy product search/detail (`GET /api/products`, `GET /api/products/:id`), and transactions (`POST /api/cart`, `POST /api/checkout`). Explain why this workflow is unique within the student group: `[fill]`.

CSV inputs vary credentials, searches, products, quantities, totals, and addresses. All plans assert HTTP 200; login also requires a JWT. The final parameter choices and any changes from `docs/SCENARIO_DESIGN.md` were: `[fill with reasons]`.

## 2. Environment and method

| Item | Recorded value |
|---|---|
| CPU / cores | `[fill]` |
| RAM | `[fill]` |
| OS | `[fill]` |
| Java / JMeter | `[fill]` |
| SUT/backend commit | `[fill]` |
| Database starting state/reset method | `[fill]` |
| Resource monitor | Activity Monitor / `[fill]` |

Describe warm-up, isolation, database reset, test order, and how the login lockout was avoided/reset: `[fill]`.

## 3. Load test

- Plan: `23120205_Load_20261117.jmx`
- Actual users/ramp/loops: `[fill]`
- Raw JTL and HTML report: `[link/path]`
- Resource evidence: `[link/path]`

Paste the analyzer table, then interpret throughput, error rate, per-endpoint p95/p99, and resource usage: `[fill]`.

## 4. Stress test

- Plan: `23120205_Stress_20261117.jmx`
- Actual users/ramp/loops: `[fill]`
- Raw JTL and HTML report: `[link/path]`
- Resource evidence: `[link/path]`

Identify saturation onset with concrete timestamp/load/error/resource evidence: `[fill]`.

## 5. Spike test

- Plan: `23120205_Spike_20261117.jmx`
- Actual users/ramp/loops: `[fill]`
- Raw JTL and HTML report: `[link/path]`
- Resource evidence: `[link/path]`

Report peak latency/error rate and recovery time after the surge: `[fill]`.

## 6. Soak test and endurance threshold

- Plan: `23120205_Soak_20261117.jmx`
- Actual users/ramp/duration: `[fill]`
- Raw JTL and HTML report: `[link/path]`
- Resource evidence: `[link/path]`

State the maximum stable request rate, p95, error-rate ceiling, memory ceiling/growth, and empirical definition of “stable”: `[fill only from the 10-15 minute run]`.

## 7. Observed issues

| Issue | Reproduction/evidence | GitHub Issue URL | Status |
|---|---|---|---|
| `[none until genuinely observed]` | `[fill]` | `[fill]` | `[fill]` |

Distinguish assertion failures, performance degradation, functional defects, and test-infrastructure failures.

## 8. Continuous performance testing proposal

Summarize the decision flow, p95 gate, fixed-runner strategy, cost, and false-alarm trade-offs from `docs/CONTINUOUS_PERFORMANCE_TESTING.md`. Add any course-specific conclusion: `[fill]`.

## 9. Conclusion

Answer with measured evidence: Which scenario first became unstable? Which endpoint dominated p95? What was the hardware threshold? Which recommendation should be implemented first, and why? `[fill]`.

## 10. Self-assessment

| Criterion | Maximum | Self-assessed | Evidence |
|---|---:|---:|---|
| Load testing | 30 | `[fill]` | `[link]` |
| Stress testing | 20 | `[fill]` | `[link]` |
| Spike testing | 20 | `[fill]` | `[link]` |
| Result analysis/review | 10 | `[fill manually]` | `[link]` |
| Continuous performance proposal | 10 | `[fill]` | `docs/CONTINUOUS_PERFORMANCE_TESTING.md` |
| Reusable skill | 10 | `[fill manually]` | `[link]` |
| **Total** | **100** | **[fill]** | |

The student will append the separately prepared AI-related mandatory material before submission.

