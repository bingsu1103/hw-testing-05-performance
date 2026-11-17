## Environment

- SUT commit: `85af3ba875c88283615e22cb108f13e2fccaf0e9`
- Backend: Node.js/Express + SQLite on macOS 26.6, Apple M2, 8 GB RAM
- Reproduced: 2026-11-17 15:48 ICT

## Observed behavior

The default test account becomes locked after two consecutive invalid passwords and remains locked more than 35 seconds.

## Expected behavior

FR-02 requires lockout after three failed attempts and a 30-second lock duration in the demo environment.

## Reproduction

1. Start from the tracked clean `database.sqlite`.
2. Submit the wrong password twice for `test@eshop.com`.
3. Immediately submit the correct password.
4. Wait 35 seconds and submit the correct password again.

## Evidence

```text
Wrong login #1: HTTP 401
Wrong login #2: HTTP 401
Valid login immediately after two failures: HTTP 403 (account locked)
Valid login after 35 seconds: HTTP 403 (account still locked)
```

## Impact

Accounts are locked one attempt earlier than specified and for substantially longer than the documented demo interval, increasing denial-of-service and usability risk. It can also contaminate authentication-heavy performance runs unless the database is reset between scenarios.

## Data-safety check

- [x] No password, JWT, serial number, or UUID is attached.
- [x] The behavior was reproduced from a clean database.

