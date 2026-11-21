# ADR-006: In-app notifications through open alerts; CSV export by content negotiation

- Status: Accepted
- Date: 2026-11-21
- Decider: Ali Eren Kurt (Lead Software Architect)
- Consulted: Ahmet Can Vurmaz (Product Owner), Abdullah Tecimen (QA), Deniz Alp Oniki (reporting owner), Mustafa Düşünceli (Frontend & UI)
- Resolves: findings F1 and F2 in `docs/test_plans_and_coverage.md` §8

## Context

**F1.** Demo step 5 (`docs/system_vision.md` §11) says the maintenance officer is
*notified* when a returned vehicle needs service, but `openapi.yaml` has no notification
endpoint. Email notifications were deferred to keep the demo and the documentation
consistent (§7.3). US-13 criterion 4 and US-43 criterion 1 only require that the new
alert is *visible* when the officer opens the application.

**F2.** CSV export is in scope (§7.1 Reporting, US-37, priority Could) but only
`GET /reports/cost` mentioned `text/csv`; carbon and utilisation had no CSV variant.

## Decision

### F1: notifications

1. A notification **is** an `OPEN` maintenance alert. No `notifications` resource, table or
   endpoint is added in release 1.
2. The web application polls `GET /maintenance/alerts?status=OPEN&size=1` every
   **60 seconds** while a `MAINTENANCE_OFFICER` or `FLEET_MANAGER` is signed in, and on
   every page load. `page.totalElements` is shown as a badge in the header; the
   maintenance screen lists the alerts.
3. The return response already contains the generated alerts
   (`ReturnResult.maintenanceAlerts`), so the driver sees the message immediately.
4. The `listMaintenanceAlerts` description in `openapi.yaml` states this behaviour.

### F2: CSV export

1. CSV is a second representation of the existing report resources, chosen with
   `Accept: text/csv` on `GET /reports/cost`, `GET /reports/carbon` and
   `GET /reports/utilization`. No new paths are added.
2. The CSV has one header row and one row per vehicle, with the same values as the JSON
   `items` (US-37: "the same values as the screen"). Encoding UTF-8, separator `,`,
   decimal point `.`.
3. The response carries `Content-Disposition: attachment; filename="fleetsync-<report>-<from>_<to>.csv"`
   so the browser downloads it.
4. Role and query parameters are the same as for JSON (`FLEET_MANAGER`, `from`, `to`,
   optional `vehicleId`). `GET /reports/summary` has no CSV form.

## Alternatives considered

| Option | Why not |
|---|---|
| F1: `GET /notifications` with read/unread state | New table and endpoints for a Could-level need; the open alert list already carries the same information |
| F1: server push (WebSocket or Server-Sent Events) | Extra infrastructure in Nginx and FastAPI; a 60 s delay is acceptable for maintenance planning |
| F1: email | Deferred in `system_vision.md` §7.3; needs an SMTP service |
| F2: separate paths (`/reports/cost.csv`, `/reports/cost/export`) | Duplicates every report operation in the contract |
| F2: `?format=csv` query parameter | Works, but HTTP content negotiation is the standard way and the cost report already used it |
| F2: CSV generated in the browser | Values could differ from the server's rounding; US-37 asks for a file with the same values |

## Consequences

- Positive: no new endpoints; the contract stays small before it is frozen as `v1.0.0`.
- Positive: QA can test F1 with US-13 criterion 4 and US-43 criterion 1 (alert visible
  after at most one polling interval) and F2 with a request using `Accept: text/csv`.
- Negative: polling sends one small request per minute per signed-in officer or manager;
  negligible for tens of users (`system_vision.md` assumption A6).
- Negative: there is no read/unread state; the badge counts open alerts, not unseen ones.
- Follow-up: QA updates F1 and F2 in `docs/test_plans_and_coverage.md` §8 to "Closed –
  ADR-006"; the Product Owner replaces "to be added to openapi.yaml" in US-37 with the three
  report operations.

## Related

- `docs/openapi.yaml` `listMaintenanceAlerts`, `getCostReport`, `getCarbonReport`, `getUtilizationReport`, `components/headers/CsvContentDisposition`
- `docs/product_backlog.md` US-13, US-37, US-43
- `docs/uml/sequence_diagrams.md` SD-6
- Issue #243
