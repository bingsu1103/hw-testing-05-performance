# HW05 - Performance Testing

Student: **Ngô Gia An**

Student ID: **23120205**

Assigned workflow: **Flow 2 - Tìm kiếm + Mã giảm giá**

System under test: [ttbhanh/eshop-sut](https://github.com/ttbhanh/eshop-sut)

Public homework repository: [bingsu1103/hw-testing-05-performance](https://github.com/bingsu1103/hw-testing-05-performance)

Backend base URL: `http://localhost:3000`

Every scenario executes the same CSV-driven journey:

1. register a unique user;
2. log in and extract the JWT;
3. search for a product;
4. view its detail;
5. add it to the cart;
6. apply a discount code and extract the final amount;
7. checkout with that amount;
8. record coupon usage, completing the SUT-side coupon flow.

The same Flow 2 workflow is used by Load, Stress, Spike, and a separate 12-minute Soak plan. The measured workload uses the deterministic fixed-value `BIGBUY` coupon; the defective percentage coupon `SAVE10` is reproduced separately in Issue #3.

## Repository status

| Deliverable | Status | Location |
|---|---|---|
| Flow assignment | Recorded; the group table is internal coordination and is not a submission artifact | `docs/FLOW_ASSIGNMENT.md` |
| Requirement traceability | Ready | `docs/REQUIREMENTS_TRACEABILITY.md` |
| Load/Stress/Spike/Soak plans | Complete and executed | `test-plans/` |
| CSV test data | Complete and used in measured execution | `data/` |
| Run and validation scripts | Ready | `scripts/` |
| JTL analyzer and performance gates | Ready | `scripts/analyze_jtl.py` |
| Continuous performance proposal | Ready | `docs/CONTINUOUS_PERFORMANCE_TESTING.md` |
| Main performance report | Complete with raw-JTL values | `docs/REPORT.md` |
| Static and bounded contract validation | Passed | `docs/VALIDATION.md` |
| Raw JTL and HTML reports | Complete for four measured runs | `results/`, `reports/` |
| Resource/hardware evidence | Time series, summaries, live screenshots, and hardware evidence complete | `evidence/` |
| Reproduced Flow 2 GitHub issue | Published | [Issue #3](https://github.com/bingsu1103/hw-testing-05-performance/issues/3) |
| Agent Skill | Implemented and validated; own-voice demonstration pending | `agent-skill/jmeter-performance-evidence/` |
| Vietnamese narrated video | Script ready; own-voice recording pending | `docs/VIDEO_SCRIPT_VI.md` |
| AI audit/report/prompts | Intentionally excluded per student instruction | not stored here |

Rendered summary images are derived from the raw data. Separate live JMeter and
Activity Monitor screenshots for all four scenarios are stored under
`evidence/screenshots/`; the student's narrated video remains a separate item.

Video URL (YouTube Unlisted): **TO BE ADDED BY STUDENT**

## Test summary

- Load: 800 samples, 0 errors, 7.56 req/s, p95 8 ms.
- Stress: 6,400 samples, 0 errors, 28.84 req/s, p95 6 ms.
- Spike: 3,600 samples, 0 errors, 94.22 req/s, p95 39 ms.
- Soak: 13,696 samples, 0 errors, 19.06 req/s for 12 minutes, p95 7 ms, p99 22 ms, backend RSS peak 59.36 MiB.
- Genuine Flow 2 bug: [SAVE10 percentage coupon inflates checkout total tenfold](https://github.com/bingsu1103/hw-testing-05-performance/issues/3).
- Demonstrated endurance point: at least 19.06 req/s at 25 users for 12 minutes; this is not an absolute maximum.

## Self-assessment

| Criterion | Maximum | Current score |
|---|---:|---:|
| Load testing | 30 | 30 |
| Stress testing | 20 | 20 |
| Spike testing | 20 | 20 |
| AI analysis and misinterpretation hunt | 10 | 0 |
| Continuous Performance Testing proposal | 10 | 10 |
| Agent Skill | 10 | 5 |
| **Total** | **100** | **85** |

## Quick start

Prerequisites: Java 17+ and Apache JMeter 5.6.x.

```bash
./scripts/validate.sh
./scripts/run-scenario.sh load
./scripts/run-scenario.sh stress
./scripts/run-scenario.sh spike
./scripts/run-scenario.sh soak
```

Detailed setup, safe execution order, evidence checklist, and interpretation guidance are in `docs/RUNBOOK.md`.

## Submission checklist

- [x] Implement and validate the assigned Flow 2 sequence.
- [x] Run Load, Stress, Spike, and Soak against a clean/restarted SUT.
- [x] Preserve complete raw JTLs, logs, HTML reports, and resource samples.
- [x] Publish only the Flow 2 issue reproduced through real execution.
- [x] Record Flow 2 ownership for internal coordination; no table screenshot is required in the submission.
- [x] Capture JMeter and Activity Monitor in the same frame for each scenario.
- [x] Add the matching hardware-spec screenshot.
- [ ] Record at least six minutes of the student's own Vietnamese narration and add the unlisted YouTube URL.
- [ ] Add the manually prepared AI audit/report/prompt material outside this implementation scope.
- [ ] Regenerate `git-commit-log.txt` and the final archive after adding all manual items.
