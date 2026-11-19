# Requirements traceability

Source: `2026.HW05.Performance Testing_En.pdf` and the SUT's public API specification.

| Requirement | Planned evidence | Repository location |
|---|---|---|
| Assigned Flow 2 spanning auth, reads, coupon, and transactions | Register, login, search/detail, cart, apply coupon, checkout samplers | `docs/FLOW_ASSIGNMENT.md`, `test-plans/*.jmx` |
| Three plans: Load, Stress, Spike | Filename-compliant plans | `test-plans/23120205_*_20261119.jmx` |
| CSV-driven workflow | Password, search/product/order values, coupon, expected final amount | `data/users.csv` |
| Three distinct report/listener views | View Results Tree, Summary Report, Aggregate Report | Load, Stress, Spike plans respectively |
| Realistic think time, ramp-up, and thread counts | Defaults documented with override support | JMX properties and `docs/SCENARIO_DESIGN.md` |
| Assertions and account-lockout awareness | HTTP status/token assertions and runbook reset steps | JMX plans and `docs/RUNBOOK.md` |
| Raw logs and HTML reports | Generated only by real non-GUI runs | `results/`, `reports/` (ignored until execution) |
| Resource and hardware evidence | Manual checklist and naming convention | `evidence/EVIDENCE_CHECKLIST.md` |
| 10-15 minute endurance test | 12-minute sustained-load plan | `test-plans/23120205_Soak_20261119.jmx` |
| Correct metrics from raw logs | Deterministic JTL analyzer | `scripts/analyze-jtl.py` |
| Continuous performance model and p95 regression gate | Proposal, flow chart, CI workflow | `docs/CONTINUOUS_PERFORMANCE_TESTING.md`, `.github/workflows/` |
| Git commit per procedure stage | Staged conventional commits and export script | Git history, `scripts/export-git-log.sh` |
| Main report and self-assessment | Evidence-driven skeleton; no fabricated values | `docs/REPORT.md` |
| AI audit/report/prompts | Explicitly excluded per student instruction | completed manually by student |

## SUT API contract used

| Step | Method and path | Expected successful response |
|---|---|---|
| Registration | `POST /api/register` | HTTP 200 and JSON `id` |
| Login | `POST /api/login` | HTTP 200 and JSON `token` |
| Product search | `GET /api/products?search=...` | HTTP 200 and JSON array |
| Product detail | `GET /api/products/:id` | HTTP 200 and non-empty object for a valid ID |
| Add to cart | `POST /api/cart` | HTTP 200 |
| Apply coupon | `POST /api/apply-coupon` | HTTP 200; JSON `coupon_id` and expected `final_amount` |
| Checkout | `POST /api/checkout` | HTTP 200 and JSON `orderId`, using extracted discounted total |
| Record coupon use | `POST /api/coupon-usage` | HTTP 200 |

