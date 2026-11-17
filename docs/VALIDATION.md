# Implementation validation

Validation date: **2026-11-17 (Asia/Ho_Chi_Minh)**

## Static validation

`./scripts/validate.sh` passed with:

- four well-formed JMX files;
- required endpoint coverage in every plan;
- distinct Load/Stress/Spike listeners;
- expected CSV schema;
- ShellCheck for runner/setup/evidence scripts;
- Python compilation and four unit tests for the JTL analyzer.

## Contract smoke tests

Apache JMeter 5.6.3 and the public `ttbhanh/eshop-sut` backend were used for bounded smoke execution. Each plan was overridden to one virtual user and one iteration; the soak duration was also bounded. All four plans loaded successfully and each completed the five-request journey with zero assertion/request errors:

| Plan | Samples | Errors | Contract result |
|---|---:|---:|---|
| Load | 5 | 0 | Pass |
| Stress | 5 | 0 | Pass |
| Spike | 5 | 0 | Pass |
| Soak | 5 | 0 | Pass |

The first sandboxed attempt could not open a localhost socket and produced `Operation not permitted`; it was discarded as infrastructure failure. The repeated run with localhost permission passed. This distinction prevents an environment restriction from being reported as a SUT defect.

The smoke run also verified that login returned a token, product list/detail requests succeeded, the authenticated cart request succeeded, and checkout returned success. It led to one correction: Thread Group display names now interpolate effective property values so overridden runs do not misleadingly display default concurrency.

## Evidence limitation

These are contract smoke tests only. Their latency/throughput values are not valid Load/Stress/Spike/Soak findings because the plans were deliberately overridden to one user and one iteration. Full runs still require simultaneous resource monitoring, screenshots, clean database state, and the student's narrated video. Raw smoke artifacts remain Git-ignored to avoid mixing them with submission evidence.

