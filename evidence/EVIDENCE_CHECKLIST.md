# Real-execution evidence checklist

Use one row per run. Do not mark a row complete unless all artifacts refer to the same Flow 2 plan, Git commit, SUT state, and timestamp window.

| Scenario | Raw JTL | HTML report | Rendered summary | Live JMeter + monitor | CPU/RAM series | Run metadata |
|---|---|---|---|---|---|---|
| Load | [x] | [x] | [x] | [x] | [x] | [x] |
| Stress | [x] | [x] | [x] | [x] | [x] | [x] |
| Spike | [x] | [x] | [x] | [x] | [x] | [x] |
| Soak (12 min) | [x] | [x] | [x] | [x] | [x] | [x] |

Additional evidence:

- [x] assigned Flow 2 recorded with supplied source screenshot and SHA-256;
- [x] hardware report text with hostname;
- [x] matching hardware screenshot (`screenshots/23120205_hardware_20261120.png`);
- [x] live Load screenshot (`screenshots/23120205_Load_20261120_live.png`);
- [x] live Stress screenshot (`screenshots/23120205_Stress_20261120_live.png`);
- [x] live Spike screenshot (`screenshots/23120205_Spike_20261120_live.png`);
- [x] live Soak screenshot (`screenshots/23120205_Soak_20261120_live.png`);
- [ ] at least six minutes of unlisted video with JMeter and Activity Monitor in the same frame;
- [ ] student's own Vietnamese narration and Agent Skill demonstration;
- [x] reset/recovery steps documented;
- [x] genuine Flow 2 defect reproduced and published as [Issue #3](https://github.com/bingsu1103/hw-testing-05-performance/issues/3);
- [x] report values independently checked against raw JTL;
- [ ] AI audit, AI report, and prompt log completed by the student;
- [ ] `git-commit-log.txt` regenerated immediately before the final package.

The group uses the assignment table only for internal coordination; no name/MSSV
table screenshot is required in the submitted evidence.
