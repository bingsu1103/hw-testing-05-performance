# Implementation plan

## Scope decisions

- Use Apache JMeter because the assignment explicitly names three distinct JMeter listener/report views.
- Exercise one end-to-end workflow across authentication-heavy, read-heavy, and transactional endpoint groups.
- Keep all scenario parameters overrideable so smoke validation does not require running the full workload.
- Never commit invented performance numbers, screenshots, logs, or issue reports.
- Exclude AI audit, AI report, and AI prompts as requested by the student.

## Delivery stages

1. Establish repository baseline, requirements traceability, and evidence policy.
2. Implement CSV-driven Load, Stress, Spike, and Soak test plans plus safe runner/validator tooling.
3. Add raw-log analysis, p95 quality gates, CI proposal/workflow, report skeleton, and evidence checklists.
4. Validate XML/scripts, perform a bounded smoke run when the SUT and JMeter are available, and export the commit history.

Each stage is committed separately so the history can be submitted as process evidence.

## Execution boundary

Automated implementation can create and statically validate plans. The following must be completed through attributable, real execution by the student:

- load/stress/spike/soak runs on the student's hardware;
- `.jtl` and generated HTML reports;
- resource and hardware screenshots;
- Vietnamese voice-narrated demo video;
- bug/performance GitHub Issues based on observed behavior;
- measured threshold values and conclusions.

