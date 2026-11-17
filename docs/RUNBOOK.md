# Execution runbook

## 1. Install prerequisites

- Java 17 or newer.
- Apache JMeter 5.6.x on `PATH`.
- Node.js/npm for the SUT.
- Activity Monitor (macOS) visible during evidence capture.

Prepare the SUT with `./scripts/setup-sut.sh`, then start its backend in a separate terminal:

```bash
npm start --prefix sut/eshop-sut/backend
```

Confirm `http://localhost:3000/api/products` returns JSON.

## 2. Validate and smoke test

```bash
./scripts/validate.sh
jmeter -n -t test-plans/23120205_Load_20261117.jmx \
  -Jthreads=1 -Jramp_seconds=1 -Jloops=1 \
  -Jcsv_file="$PWD/data/users.csv" \
  -l results/smoke.jtl
```

Inspect the smoke JTL. Do not proceed if login or assertions fail.

## 3. Establish clean starting state

1. Stop the backend.
2. Restore a known-good copy of the demo SQLite database or reclone the SUT.
3. Start the backend and verify a successful login with the CSV credentials.
4. Close unrelated high-resource applications.
5. Record the hostname and hardware with `./scripts/capture-hardware.sh`; capture the corresponding screenshot.

Use the same starting-state procedure before every scenario. The backend keeps carts in memory and writes checkout orders to SQLite, so restarting only the test tool is not sufficient for comparable runs.

## 4. Run scenarios

Run in this order and allow the machine/backend to return to idle between runs:

```bash
./scripts/run-scenario.sh load
./scripts/run-scenario.sh stress
./scripts/run-scenario.sh spike
./scripts/run-scenario.sh soak
```

During each run, capture JMeter/terminal and Activity Monitor in the same frame. Record CPU, memory, start/end time, and any visible recovery period. Do not reuse a JTL filename.

## 5. Lockout recovery

If login returns 401/403 repeatedly:

1. stop JMeter immediately;
2. confirm that credentials were not changed;
3. wait at least the configured lock interval or restore the clean database;
4. prove one successful manual login;
5. start a new run with a new JTL filename and document the reset.

Never merge partial and restarted JTL files as if they were one uninterrupted run.

## 6. Analyze and preserve evidence

For each completed JTL, run the analyzer added in the reporting stage. Preserve:

- unmodified JTL;
- JMeter log;
- generated HTML report folder;
- monitor/hardware screenshot;
- execution notes with plan name, Git commit, exact command, timestamps, and observed anomalies.

Open a GitHub Issue only after reproducing a genuine defect or performance issue and attach the relevant screenshot and non-sensitive excerpt. Do not upload credentials or JWTs.

