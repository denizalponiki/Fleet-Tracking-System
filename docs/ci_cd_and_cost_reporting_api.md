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

The reporting endpoints are defined in `docs/openapi.yaml`. Implementation targets below follow `docs/product_backlog.md`.

| Story | Endpoint / feature | Purpose | Target |
|---|---|---|---|
| US-33 | `GET /reports/summary` | Vehicle counts by status, open alerts and total cost for the selected period | Final |
| US-34 | `GET /reports/cost` | Fuel, expense and maintenance costs per vehicle | Final |
| US-35 | `GET /reports/carbon` | Vehicle CO₂ emissions and ride-sharing savings | Final |
| US-36 | `GET /reports/utilization` | Vehicle utilisation for the selected period | Final |
| US-37 | CSV export | Export cost, carbon and utilisation reports | Final |

US-37 has no endpoint defined yet. Its API design must be agreed and added to `docs/openapi.yaml` before implementation.

Request parameters, response schemas and security requirements must follow `docs/openapi.yaml`. A `STAFF` user requesting reports must receive `403 FORBIDDEN`.

## 5. Calculation Rules

### Cost — US-34

Total cost = fuel cost + expenses + maintenance cost.

Use source records belonging to the selected vehicle and period. Totals must match those records. A period without records returns zero costs without error.

### Carbon — US-35

CO₂ emissions = fuel consumed in litres × emission factor for the fuel type.

Factors for petrol, diesel and LPG, their units and authoritative sources remain to be agreed with the Product Owner. No numerical factor is assumed here.

Ride-sharing savings must represent emissions avoided by passenger trips not taken separately. The calculation assumptions remain to be agreed and documented before implementation.

### Utilisation — US-36

Utilisation (%) = reserved hours / available working hours × 100.

Example: 20 reserved hours / 40 working hours × 100 = 50%.

The working calendar, working hours and handling of zero available hours remain to be agreed with the Product Owner. Invalid periods return `400 VALIDATION_ERROR`.

### CSV Export — US-37

Exported values must match the corresponding report for the same period and filters.

## 6. References

- [Documentation ownership](README.md)
- [Git-Flow and contribution rules](git_flow.md)
- [Product backlog](product_backlog.md)
- [OpenAPI contract](openapi.yaml)
- [Test plan and coverage](test_plans_and_coverage.md)
- [OpenAPI lint workflow](../.github/workflows/openapi-lint.yml)
- [Redocly configuration](../redocly.yaml)
