# HW05 - Performance Testing

Student: **Ngô Gia An**  
Student ID: **23120205**  
System under test: [ttbhanh/eshop-sut](https://github.com/ttbhanh/eshop-sut)  
Backend base URL: `http://localhost:3000`

This repository contains reproducible JMeter assets for an end-to-end workflow:

1. authenticate with `POST /api/login`;
2. list/search and inspect products with `GET /api/products` and `GET /api/products/:id`;
3. add an item with `POST /api/cart`;
4. create an order with `POST /api/checkout`.

The same workflow is used by Load, Stress, and Spike scenarios. Inputs are read from CSV. A separate 12-minute soak plan is included to determine the local machine's endurance threshold.

## Repository status

| Deliverable | Status | Location |
|---|---|---|
| Requirement traceability | Ready | `docs/REQUIREMENTS_TRACEABILITY.md` |
| Load/Stress/Spike plans | Complete and executed | `test-plans/` |
| CSV test data | Complete and reviewed during measured execution | `data/` |
| Run and validation scripts | Ready | `scripts/` |
| JTL analyzer and performance gates | Ready | `scripts/analyze_jtl.py` |
| Continuous performance proposal | Ready | `docs/CONTINUOUS_PERFORMANCE_TESTING.md` |
| Main performance report | Complete with raw-JTL values | `docs/REPORT.md` |
| Static and bounded contract validation | Passed | `docs/VALIDATION.md` |
| Raw JTL and HTML reports | Complete for four measured runs | `results/`, `reports/` |
| Resource/hardware evidence | Time series, summary images, hardware text complete; live screenshot pending | `evidence/` |
| Vietnamese narrated video | Script ready; own-voice recording pending | `docs/VIDEO_SCRIPT_VI.md` |
| AI audit/report/prompts | Intentionally excluded per student instruction | not stored here |

Final metrics are derived from raw JTLs produced on the recorded student machine. Rendered summary images are clearly labeled and do not replace the manually required live Activity Monitor screenshot/video.

## Quick start

Prerequisites: Java 17+ and Apache JMeter 5.6.x.

```bash
./scripts/validate.sh
./scripts/run-scenario.sh load
./scripts/run-scenario.sh stress
./scripts/run-scenario.sh spike
./scripts/run-scenario.sh soak
```

Detailed setup, safe execution order, evidence checklist, and result interpretation are in `docs/RUNBOOK.md`.

## Submission checklist

- [ ] Run all three scenarios and the soak test against a clean/restarted SUT.
- [ ] Keep the complete raw `.jtl` files and HTML report folders.
- [ ] Capture JMeter and Activity Monitor in the same frame for each scenario.
- [ ] Capture the hardware specification and matching hostname.
- [ ] Reset/wait out the login lockout if an invalid-credential test triggers it.
- [ ] Record at least six minutes of Vietnamese narration and add the unlisted YouTube URL.
- [ ] Create GitHub Issues only for issues reproduced by real execution.
- [ ] Fill the measured values and self-assessment in the final report.
- [ ] Generate `git-commit-log.txt` with `./scripts/export-git-log.sh` immediately before packaging.
- [ ] Add the manually prepared AI audit/report/prompt material outside this implementation scope.

