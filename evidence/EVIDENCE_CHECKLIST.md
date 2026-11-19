# Real-execution evidence checklist

Use one row per run. Do not mark a row complete unless all artifacts refer to the same Flow 2 plan, Git commit, SUT state, and timestamp window.

| Scenario | Raw JTL | HTML report | Rendered summary | Live JMeter + monitor | CPU/RAM series | Run metadata |
|---|---|---|---|---|---|---|
| Load | [x] | [x] | [x] | [ ] | [x] | [x] |
| Stress | [x] | [x] | [x] | [ ] | [x] | [x] |
| Spike | [x] | [x] | [x] | [ ] | [x] | [x] |
| Soak (12 min) | [x] | [x] | [x] | [ ] | [x] | [x] |

Additional evidence:

- [x] assigned Flow 2 recorded with supplied source screenshot and SHA-256;
- [ ] proof that name/MSSV was entered into the shared Flow 2 table;
- [x] hardware report text with hostname;
- [ ] matching hardware screenshot;
- [ ] at least six minutes of unlisted video with JMeter and Activity Monitor in the same frame;
- [ ] student's own Vietnamese narration and Agent Skill demonstration;
- [x] reset/recovery steps documented;
- [x] genuine Flow 2 defect reproduced and published as [Issue #3](https://github.com/bingsu1103/hw-testing-05-performance/issues/3);
- [x] report values independently checked against raw JTL;
- [ ] AI audit, AI report, and prompt log completed by the student;
- [ ] `git-commit-log.txt` regenerated immediately before the final package.
