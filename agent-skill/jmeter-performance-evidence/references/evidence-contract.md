# Evidence contract

## Required run identity

Record these together for every measured scenario:

- scenario and exact JMX filename;
- exact command and effective threads/ramp/loops/duration;
- test-assets commit and SUT commit;
- CSV/data-set identity without exposing secrets;
- start/end timestamps and timezone;
- hostname, CPU, RAM, OS, Java, and JMeter versions;
- database/process reset and warm-up procedure.

## Required artifacts

- unmodified CSV JTL with header;
- JMeter log;
- HTML report generated from the same JTL;
- time-series backend and JMeter CPU/memory samples;
- required resource-monitor screenshot/video;
- analysis derived from the raw JTL;
- reproduction evidence for each reported defect.

## Metric rules

- Latency percentiles come from JTL `elapsed` values. State the percentile method.
- Error rate is unsuccessful samples divided by all samples; do not silently exclude assertion failures.
- Throughput uses the whole measured wall interval, not the sum of endpoint-specific rates.
- Report per-label metrics so a fast read endpoint cannot hide a slow transactional endpoint.
- Compare baselines only when workload, data, software versions, and machine are comparable.

## Integrity rules

- Do not edit, concatenate, or hand-correct raw JTLs.
- Do not use a failed sandbox/network attempt as evidence of a SUT defect.
- Do not publish credentials, JWTs, private addresses, hardware serial numbers, or UUIDs.
- Do not claim a defect from source inspection alone; reproduce it through the public behavior.
- Do not fill missing screenshots, narration, or measured values with generated substitutes.
