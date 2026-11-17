# Real-execution evidence checklist

Use one row per run. Do not mark a row complete unless all artifacts refer to the same plan, Git commit, SUT state, and timestamp window.

| Scenario | Raw JTL | HTML report | JMeter + monitor screenshot | CPU/RAM notes | Start/end time | Git commit |
|---|---|---|---|---|---|---|
| Load | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Stress | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Spike | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| Soak (10-15 min) | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |

Additional required evidence:

- [ ] hardware report text plus screenshot with matching hostname;
- [ ] at least six minutes of unlisted video with tool and resource monitor in the same frame;
- [ ] student's own Vietnamese narration;
- [ ] reset/recovery steps documented if login lockout occurred;
- [ ] GitHub Issues contain only genuinely reproduced issues and screenshots;
- [ ] report values independently checked against raw JTL;
- [ ] `git-commit-log.txt` regenerated immediately before packaging.

