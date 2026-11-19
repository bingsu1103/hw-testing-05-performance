# Implementation validation

Validation date: **2026-11-19 (Asia/Ho_Chi_Minh)**

## Static validation

`./scripts/validate.sh` passed with:

- four well-formed JMX files dated `20261119`;
- the exact eight-call Flow 2 sequence in every plan;
- state extraction/reuse for user ID, JWT, coupon ID, final amount, and order ID;
- distinct Load/Stress/Spike listener types;
- the expected Flow 2 CSV schema;
- ShellCheck and Python compilation;
- seven passing unit/contract tests.

The negative gate unit test intentionally prints a p95 failure while the test itself passes by confirming that the analyzer rejects the threshold violation.

## Contract smoke test

Apache JMeter 5.6.3 and the checked-out `ttbhanh/eshop-sut` backend were used for a bounded one-user, one-iteration smoke execution before measured load. The run produced eight samples and zero request/assertion errors, covering:

1. registration and user ID extraction;
2. login and JWT extraction;
3. product search and detail;
4. authenticated cart mutation;
5. coupon application and final-amount assertion;
6. checkout with the extracted final amount;
7. coupon-usage recording.

This was only a contract check; its latency and throughput are not reported as Load/Stress/Spike/Soak findings.

## Measured-run validation

All four final runs were generated from a restored database and preserved with JTL, JMeter log, HTML report, run metadata, and two-second resource samples.

| Plan | Samples | Errors | p95 | Result |
|---|---:|---:|---:|---|
| Load | 800 | 0 | 8 ms | Pass |
| Stress | 6,400 | 0 | 6 ms | Pass |
| Spike | 3,600 | 0 | 39 ms | Pass |
| Soak | 13,696 | 0 | 7 ms | Pass |

For every JTL, `scripts/analyze_jtl.py` passed an error-rate gate of 0% and a p95 ceiling of 2,500 ms. Raw line counts match the reported sample counts plus one CSV header. Each corresponding HTML report contains `index.html`.

## Honest evidence boundary

Rendered summary images are derived from raw JTL/resource CSV files and are labeled as such. They do not replace the live JMeter/Activity Monitor screenshots or the student's own narrated Agent Skill demonstration. The AI audit, AI report, and prompt log also remain outside this implementation scope.
