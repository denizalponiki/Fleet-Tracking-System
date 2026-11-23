# CI/CD and Cost Reporting API

Owner: Deniz Alp Oniki — DevOps & CI/CD Infrastructure Engineer

## 1. Current CI/CD

The existing GitHub Actions workflow is defined in `.github/workflows/openapi-lint.yml`.

It runs on:
- Pull requests targeting `develop` or `main`.
- Pushes to `develop` or `main`.
- Manual execution through `workflow_dispatch`.

The workflow uses Ubuntu, Node.js 22 and Redocly CLI v1 to validate `docs/openapi.yaml`:

```bash
npx --yes @redocly/cli@1 lint docs/openapi.yaml --config redocly.yaml
```

`redocly.yaml` extends the recommended rules and treats the following as errors:
- `operation-operationId`: operations must have an operation ID.
- `operation-2xx-response`: operations must define a successful response.
- `no-unresolved-refs`: references must resolve.

This workflow checks the API contract. Build, automated tests, coverage and deployment are planned work.

## 2. Branch Protection and Review

`docs/git_flow.md` specifies these requirements for `main` and `develop`:
- Changes through pull requests; no direct pushes.
- At least one approving review.
- Code owner approval.
- Passing CI checks.
- Branch up to date with its target.
- Force pushes and protected branch deletion disabled.

These are the documented requirements. Their actual GitHub configuration must be verified in repository Settings; this document does not claim that all settings have been confirmed.

## 3. Delivery Plan

### Sprint 3
- US-46: Run frontend, FastAPI backend and PostgreSQL using `docker compose up`.
- US-47: Provide fictional demo seed data.
- US-48: Build the project and run automated tests on every PR to `develop`.
- US-49: Publish backend coverage using pytest-cov and fail CI below 50%, in coordination with QA.
- Retain OpenAPI lint as a required check and require the new checks before merging.

### Final
- US-52: Integrate SonarQube analysis and produce a report for `develop`.
- Meet the final quality target of no open critical issues.

SonarQube integration can be prepared during Sprint 3; its backlog target is Final.

## 4. Reporting API

**Sprint 2 scope:** the following documents specify future reporting behavior only; reporting backend code and CSV export implementation are not part of this documentation PR.

The reporting endpoints are defined in `docs/openapi.yaml`. Implementation targets below follow `docs/product_backlog.md`.

| Story | Endpoint / feature | Purpose | Target |
|---|---|---|---|
| US-33 | `GET /reports/summary` | Vehicle counts by status, open alerts and total cost for the selected period | Final |
| US-34 | `GET /reports/cost` | Fuel, expense and maintenance costs per vehicle | Final |
| US-35 | `GET /reports/carbon` | Vehicle CO₂ emissions and ride-sharing savings | Final |
| US-36 | `GET /reports/utilization` | Vehicle utilisation for the selected period | Final |
| US-37 | CSV export | Export cost, carbon and utilisation reports | Final |

**Sprint 2 decision (ADR-006):** US-37 uses existing `GET /reports/cost`, `GET /reports/carbon`, and `GET /reports/utilization` operations with `Accept: text/csv`. No separate CSV endpoint is required, and summary remains JSON-only. This is a contract decision, not implemented functionality.

Request parameters, response schemas and security requirements must follow `docs/openapi.yaml`. A `STAFF` user requesting reports must receive `403 FORBIDDEN`.

## 5. Calculation Rules

### Cost — US-34

Total cost = fuel cost + expenses + maintenance cost.

Use source records belonging to the selected vehicle and period. Totals must match those records. A period without records returns zero costs without error.

### Carbon — US-35

CO₂ emissions = fuel consumed in litres × emission factor for the fuel type.

**Agreed Sprint 2 factors from SRS §3.8 / OpenAPI (kg CO₂ per litre):** GASOLINE 2.31; DIESEL 2.68; HYBRID 2.31 (same per-litre factor as gasoline); ELECTRIC 0.00 (no fuel combusted, not full life-cycle emissions). LPG is not a valid fuel type in the current API schema. These are project assumptions documented in the contract.

The `rideSharingSavedKgCo2` field estimates emissions avoided by separate passenger trips not taken. Review the estimation assumptions against SRS and API acceptance criteria before implementation; do not invent unsupported constants.

### Utilisation — US-36

Utilisation (%) = reserved hours / available working hours × 100.

Example: 22.5 reserved hours / 45 working hours (5 weekdays × 9 hours/day) × 100 = 50%.

**Sprint 2 working calendar (SRS §3.8):** Monday–Friday, 08:00–17:00 (9 hours per day) in the Europe/Istanbul time zone, excluding `IN_MAINTENANCE` and `OUT_OF_SERVICE` periods from available hours. Invalid periods return `400 VALIDATION_ERROR`; verify the zero-available-hours behavior against the contract before implementation.

### CSV Export — US-37

ADR-006 defines CSV on the three cost, carbon and utilisation GET operations via `Accept: text/csv` (not on summary). UTF-8 CSV uses a header row, comma delimiter, period decimal separator, and one row per vehicle; values must match JSON under identical filters. The response sets `Content-Disposition: attachment` with a generated filename and keeps the same `FLEET_MANAGER` access control.

## 6. References

- [Documentation ownership](README.md)
- [Git-Flow and contribution rules](git_flow.md)
- [Product backlog](product_backlog.md)
- [OpenAPI contract](openapi.yaml)
- [Sprint 2 SRS](srs/srs.md)
- [Requirements traceability matrix](srs/traceability_matrix.md)
- [ADR-006 CSV export decision](adr/ADR-006-notifications-and-csv-export.md)
- [Test plan and coverage](test_plans_and_coverage.md)
- [OpenAPI lint workflow](../.github/workflows/openapi-lint.yml)
- [Redocly configuration](../redocly.yaml)
