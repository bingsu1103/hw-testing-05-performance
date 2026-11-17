---
name: jmeter-performance-evidence
description: Design, execute, validate, and report reproducible JMeter API performance tests with raw JTL, resource evidence, percentile checks, and honest separation of smoke checks from measured Load, Stress, Spike, or Soak findings. Use for performance-test planning, execution, evidence collection, regression analysis, or report preparation; not for fabricating runs, screenshots, hardware data, or defects.
---

# JMeter Performance Evidence

Produce an auditable performance-test result whose report can be traced to the exact plan, command, SUT commit, raw JTL, machine, and resource observations.

## Workflow

1. Read the assignment/SLO and the SUT's actual API contract. Resolve endpoints, authentication, data mutation, lockout/rate-limit behavior, and required evidence before choosing load parameters.
2. Define one realistic workflow and a distinct load model for each requested scenario. Keep thread count, ramp, loops/duration, host, port, and CSV path overrideable.
3. Validate plans statically and run a one-user/one-iteration contract smoke test. Treat connection/sandbox failures as infrastructure failures, not SUT defects.
4. Establish a clean starting state for every measured run. Record plan hash/commit, SUT commit, command, timestamps, hostname, hardware, Java/JMeter versions, database reset, and warm-up.
5. Execute JMeter non-GUI. Preserve the raw CSV JTL and JMeter log without merging or editing them. Generate the HTML report from that JTL.
6. Sample backend/JMeter CPU and memory throughout the run. Capture any required screenshots/video while the run is active.
7. Analyze raw `elapsed` and `success` values with `scripts/analyze_jtl.py`; report sample count, errors, error rate, throughput, and p50/p90/p95/p99 overall and by label.
8. Reproduce any suspected issue from a clean state before creating an external issue. State observations separately from hypotheses and remove tokens/passwords.
9. Fill the report only from attributable artifacts. Explicitly mark missing evidence or manual steps rather than inventing values.

Read [references/evidence-contract.md](references/evidence-contract.md) before measured execution or final reporting.

## Stopping conditions

- Stop a run when invalid credentials cause repeated 401/403 responses, the target is not the explicitly authorized SUT, or resource exhaustion threatens the host.
- Do not automatically retry more than once solely to make a gate pass. Preserve both attempts and explain the rerun.
- Do not publish repositories, issues, or files unless the user authorized those external changes.
- Never characterize smoke-test latency as Load/Stress/Spike/Soak performance.
