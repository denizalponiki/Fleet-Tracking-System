# FleetSync · Git-Flow and Contribution Rules

> SENG 321 · Sprint 1 deliverable. Owner: Mehmet Umut Oğuzcan (Scrum Master). Branch protection is configured by Deniz Alp Oniki (DevOps).
> Related: [`raci_matrix.md`](raci_matrix.md) · [`.github/CODEOWNERS`](../.github/CODEOWNERS) · [`.github/pull_request_template.md`](../.github/pull_request_template.md)

These rules exist for two reasons: `develop` must always build, and every member's contribution must be visible in the history (individual contribution is graded from commits, PRs, reviews and issues).

## 1. Branches

| Branch | Purpose | Created from | Merges into | Lifetime |
|---|---|---|---|---|
| `main` | Only submitted releases. Every sprint submission is tagged here. | – | – | permanent |
| `develop` | Integration branch. Always builds, CI always green. | `main` | `main` (end of sprint only) | permanent |
| `feature/FS-<issue>-<short-name>` | One issue, one feature. | `develop` | `develop` | days, not weeks |
| `fix/FS-<issue>-<short-name>` | Bug fix found during the sprint. | `develop` | `develop` | short |
| `release/<version>` | Optional: final polishing before a submission. | `develop` | `main` and `develop` | until the tag |
| `hotfix/FS-<issue>-<short-name>` | Urgent fix on a submitted version. | `main` | `main` and `develop` | short |

**Naming examples**

```text
feature/FS-12-reservation-create
feature/FS-31-handover-pickup-checklist
fix/FS-40-odometer-validation
docs/FS-7-git-flow-rules        # documentation-only work may use docs/
```

- Lowercase, words separated by `-`, always the issue number.
- No personal branches (`ali-branch`, `patch-1`). GitHub's web editor creates `<user>-patch-N` by default: rename the branch in the "Propose changes" dialog before opening the PR.

## 2. Protected branches

Configured on GitHub for `main` and `develop`:

- No direct pushes; changes only through pull requests.
- At least **1 approving review**; the PR author cannot approve their own PR.
- Review from the code owner is required (`.github/CODEOWNERS`).
- CI status checks must pass before merging (OpenAPI lint now; build, tests and coverage ≥ 50% from Sprint 3).
- Branch must be up to date with the target before merging.
- Force pushes and branch deletion are disabled.

## 3. Issues come first

Every piece of work starts as a GitHub issue on the Projects board.

- The issue states the **goal**, the **owner** (assignee), and the **acceptance evidence** (what proves it is done).
- Use the templates in `.github/ISSUE_TEMPLATE/`; label with the module (`handover`, `fuel`, …) and type (`feature`, `bug`, `docs`, `test`).
- Issue numbers are referenced as `FS-<n>` in branch names and as `#<n>` in commits and PRs.

## 4. Commits

[Conventional Commits](https://www.conventionalcommits.org/) with the module as scope and the issue number at the end:

```text
<type>(<scope>): <short imperative summary> (#<issue>)
```

| Type | Use for |
|---|---|
| `feat` | new behaviour |
| `fix` | bug fix |
| `docs` | documentation, diagrams, ADRs |
| `test` | adding or changing tests |
| `refactor` | code change without behaviour change |
| `chore` / `ci` / `build` | tooling, CI, Docker, dependencies |

```text
feat(maintenance): add km-based rule strategy (#23)
fix(handover): reject return odometer lower than pickup (#41)
docs(process): add git-flow rules (#7)
```

- Small, focused commits. One commit should do one thing.
- Commit from your own Git identity (name and email linked to your GitHub account), so the contribution is attributed to you.
- Avoid "Add files via upload": it hides what changed. Use `git` locally or the web editor with a real commit message.

## 5. Pull requests

1. Branch from an up-to-date `develop`.
2. Open the PR against `develop` and fill in the PR template: linked issue (`Closes #<n>`), summary, how to test, test evidence or screenshot, OpenAPI impact.
3. Request a reviewer. Keep PRs small enough to review in about 15 minutes.
4. Address review comments with new commits (do not force-push over a review in progress).
5. Merge when: CI is green, at least 1 approval, code owner approved, conversations resolved.

**Extra approval rules**

- `docs/openapi.yaml`, `docs/adr/` and cross-module interfaces: Lead Architect approval required.
- Tests in the `fuel` module (owned by QA) are reviewed by another member.
- **Review rotation:** every member reviews at least one PR from someone else each week. The Scrum Master tracks this in the weekly contribution check.

## 6. Merge strategy

- Use **"Create a merge commit"**. Do **not** squash and do not rebase-merge on `develop` or `main`: squashing erases individual commits and authorship.
- Delete the feature branch after merging.
- `develop` → `main` happens **only at the end of a sprint**, through a PR approved by the Scrum Master and the Lead Architect.

## 7. Releases and tags

| Submission | Tag on `main` |
|---|---|
| Sprint 1 | `sprint-1` |
| Sprint 2 | `sprint-2` |
| Sprint 3 (MVP) | `v0.3.0-mvp` |
| Final | `v1.0.0` |

The tag is created by DevOps after the `develop` → `main` merge. The Scrum Master adds the tag link to the sprint's submission evidence list in `docs/sprint-reports/`.

## 8. Definition of Ready

A story can enter a sprint when:

- the user, capability and value are clear;
- acceptance criteria are testable (Given/When/Then);
- API impact and dependencies on other modules are known;
- it is small enough to finish within one sprint.

## 9. Definition of Done

A story is done when:

- code is reviewed and merged into `develop`;
- unit tests are written and CI is green;
- `docs/openapi.yaml` is updated if the API changed;
- the acceptance criteria are verified;
- diagrams are updated if the structure changed;
- the issue is closed and the board card is in **Done**.

## 10. Quick reference

```bash
git checkout develop && git pull
git checkout -b feature/FS-31-handover-pickup-checklist
# ... work ...
git add -p
git commit -m "feat(handover): add pickup checklist entity (#31)"
git push -u origin feature/FS-31-handover-pickup-checklist
# open a PR to develop on GitHub, fill in the template, request a reviewer
```
