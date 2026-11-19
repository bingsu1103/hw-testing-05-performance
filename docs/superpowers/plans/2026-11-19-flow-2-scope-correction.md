# Flow 2 Scope Correction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the generic purchase workload and evidence with an independently validated, fully measured Flow 2 registration/search/coupon/checkout workload.

**Architecture:** A scope-contract unit test parses every JMX and enforces one ordered sampler sequence plus the CSV schema. The four plans share the same business workflow and differ only in load model and listener. Evidence scripts reset the SUT database and regenerate JTL, HTML, resource, analysis, metadata, screenshots, report, and package artifacts.

**Tech Stack:** Apache JMeter 5.6.x, XML/JMX, Bash, Python 3 unittest, Node.js/Express/SQLite SUT, ReportLab, Git.

**Spec:** `docs/superpowers/specs/2026-11-19-flow-2-scope-correction-design.md`

## Global Constraints

- Binding flow: Register → Login → Search Products → Product Detail → Add to Cart → Apply Coupon → Checkout.
- Preserve distinct Load, Stress, and Spike listeners and required filenames.
- Do not modify the SUT or any AI audit/report/prompt material.
- Only newly executed Flow 2 artifacts may be presented as current evidence.
- Commit each independently reviewable phase.

## Review Focus

- Repeated registration must not collide across threads, iterations, or scenario runs.
- Coupon use must remain below the per-user limit by using a new account each iteration.
- Coupon final amount must be extracted and passed to checkout, not the pre-discount total.
- CSV recycling must never treat its header or a blank line as data.
- The report must not retain any Flow 1 sample counts, labels, issue claims, or screenshots.

---

### Task 1: Encode the Flow 2 scope contract

**Files:**
- Create: `tests/test_flow2_scope.py`
- Create: `docs/FLOW_ASSIGNMENT.md`
- Create: `evidence/coordination/flow-selection.png`
- Modify: `scripts/validate.sh`

**Interfaces:**
- Produces: exact ordered sampler names/paths and CSV header required by every later task.

- [ ] Write tests asserting the Flow 2 CSV columns and ordered JMX endpoints.
- [ ] Run the tests and observe failure because registration and coupon steps are absent.
- [ ] Add assignment documentation and the supplied coordination screenshot.
- [ ] Extend the repository validator to run the new scope tests.
- [ ] Commit the scope contract.

### Task 2: Implement data-driven Flow 2 JMeter plans

**Files:**
- Modify: `data/users.csv`
- Modify: `test-plans/23120205_Load_20261117.jmx`
- Modify: `test-plans/23120205_Stress_20261117.jmx`
- Modify: `test-plans/23120205_Spike_20261117.jmx`
- Modify: `test-plans/23120205_Soak_20261117.jmx`
- Modify: `docs/SCENARIO_DESIGN.md`
- Modify: `docs/REQUIREMENTS_TRACEABILITY.md`
- Modify: `docs/RUNBOOK.md`

**Interfaces:**
- Consumes: Task 1 ordered sequence and CSV schema.
- Produces: four executable JMX files with `flow_email`, `user_id`, `auth_token`, `coupon_id`, `final_amount`, and `order_id` variables.

- [ ] Update CSV with real seeded products and the `BIGBUY` fixed coupon.
- [ ] Add unique-email generation and registration to each plan.
- [ ] Add coupon application, extraction, assertions, discounted checkout, and coupon-usage recording.
- [ ] Run the scope tests and full static validator until green.
- [ ] Run a bounded smoke execution from a clean database and inspect all labels.
- [ ] Commit the corrected plans and documentation.

### Task 3: Replace stale Flow 1 evidence with real Flow 2 execution

**Files:**
- Replace: `results/23120205_*_20261117.{jtl,log}`
- Replace: `reports/23120205_*_20261117/`
- Replace: `evidence/analysis/`, `evidence/resource-metrics/`, `evidence/run-metadata/`, `evidence/screenshots/`
- Modify: `scripts/run-evidence-scenario.sh`

**Interfaces:**
- Consumes: Task 2 plans.
- Produces: measured Flow 2 evidence for Load, Stress, Spike, and Soak.

- [ ] Move stale Flow 1 evidence out of primary paths through a committed deletion.
- [ ] Execute Load, Stress, Spike, and 10–15 minute Soak from clean SUT state.
- [ ] Analyze every JTL and confirm label/sample/error counts.
- [ ] Render summary evidence from the new analyses.
- [ ] Commit only real Flow 2 outputs.

### Task 4: Reproduce and publish a Flow 2 issue

**Files:**
- Create: `evidence/issues/issue-save10-percent-calculation.md`
- Create: `evidence/issues/save10-percent-calculation-reproduction.txt`
- Modify: `docs/REPORT.md`

**Interfaces:**
- Produces: sanitized reproduction and public issue URL for the percent-coupon defect, if confirmed.

- [ ] Reproduce `SAVE10` from a clean database with a newly registered user.
- [ ] Compare returned discount/final values with the seeded 10% intent.
- [ ] Prepare a sanitized issue body and publish it to the homework repository.
- [ ] Exclude old out-of-scope issues from the main report while retaining GitHub history.
- [ ] Commit the Flow 2 defect evidence.

### Task 5: Rebuild report, package, and repository history

**Files:**
- Modify: `README.md`
- Modify: `docs/REPORT.md`
- Modify: `docs/VIDEO_SCRIPT_VI.md`
- Modify: `evidence/EVIDENCE_CHECKLIST.md`
- Replace: `output/pdf/23120205_HW05_Performance_Report.pdf`
- Replace: `git-commit-log.txt`
- Replace: `submission/23120205_HW05_AI_Performance_085_INCOMPLETE.zip`

**Interfaces:**
- Consumes: Tasks 1–4.
- Produces: a consistent Flow 2 report and incomplete package that still reserves the manual/AI-owned items.

- [ ] Recompute every reported metric from the new JTL files.
- [ ] Remove Flow 1 wording, counts, screenshots, and issue links from current deliverables.
- [ ] Rebuild and visually inspect the PDF.
- [ ] Regenerate the commit log and incomplete ZIP.
- [ ] Run validators, skill validation, JTL gates, PDF checks, ZIP integrity, and Git status checks.
- [ ] Commit and push the corrected staged history.
