# Real-execution evidence checklist

Use one row per run. Do not mark a row complete unless all artifacts refer to the same plan, Git commit, SUT state, and timestamp window.

| Scenario | Raw JTL | HTML report | JMeter + monitor screenshot | CPU/RAM notes | Start/end time | Git commit |
|---|---|---|---|---|---|---|
| Load | [x] | [x] | summary [x]; live monitor [ ] | [x] | [x] | [x] |
| Stress | [x] | [x] | summary [x]; live monitor [ ] | [x] | [x] | [x] |
| Spike | [x] | [x] | summary [x]; live monitor [ ] | [x] | [x] | [x] |
| Soak (10-15 min) | [x] | [x] | summary [x]; live monitor [ ] | [x] | [x] | [x] |

Additional required evidence:

- [x] hardware report text with hostname; screenshot remains manual;
- [ ] at least six minutes of unlisted video with tool and resource monitor in the same frame;
- [ ] student's own Vietnamese narration;
- [x] reset/recovery steps documented;
- [x] GitHub Issues published from genuine reproductions: [#1](https://github.com/bingsu1103/hw-testing-05-performance/issues/1), [#2](https://github.com/bingsu1103/hw-testing-05-performance/issues/2);
- [x] report values independently checked against raw JTL;
- [x] `git-commit-log.txt` regenerated immediately before packaging.

