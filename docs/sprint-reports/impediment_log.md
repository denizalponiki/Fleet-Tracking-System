# FleetSync · Impediment Log

> Owner: Mehmet Umut Oğuzcan (Scrum Master). Updated at every stand-up. Closed items stay in the table.
> An impediment is anything that blocks or slows the team and cannot be solved by the person alone.

| ID | Opened | Impediment | Impact | Owner | Action | Status | Resolved |
|---|---|---|---|---|---|---|---|
| IMP-01 | 2026-11-02 | `docs/raci_matrix.md` was deleted from `develop` (PR #19) and not restored. | Sprint 1 deliverable missing; `docs/README.md` links to a missing file. | Mehmet Umut Oğuzcan | Restore the revised file through a PR. | Closed | 2026-11-02 |
| IMP-02 | 2026-11-02 | GitHub usernames of 5 members are unknown (`@?` in RACI). | `CODEOWNERS` cannot be activated; required reviews do not work. | Mehmet Umut Oğuzcan | Collect usernames in the team group; fill RACI and CODEOWNERS. | Closed | 2026-11-02 |
| IMP-03 | 2026-11-02 | 3 members have no commit / PR / review yet. | Individual contribution (15 pts) at risk. | Mehmet Umut Oğuzcan | Each member opens at least one issue + PR and reviews one PR before the Sprint 1 submission. | Closed | 2026-11-04 |
| IMP-04 | 2026-11-02 | Files are added with "Add files via upload" and default `<user>-patch-N` branches; several PRs were merged within minutes without review. | Changes are hard to review; history does not show what changed. | Mehmet Umut Oğuzcan, Deniz Alp Oniki | Share `docs/git_flow.md`; enable branch protection (1 approval, no self-approval). | Closed | 2026-11-05 |
| IMP-05 | 2026-11-02 | No `sprint-1` tag yet; `main` contains only the initial commit. | Sprint 1 submission evidence incomplete. | Deniz Alp Oniki | Merge `develop` → `main` through a reviewed PR and tag `sprint-1` before submission. | Closed | 2026-11-05 |

<!-- Add a row:
| IMP-06 | YYYY-MM-DD | what blocks us | what it affects | who solves it | next step | Open / In progress / Closed | YYYY-MM-DD |
-->
