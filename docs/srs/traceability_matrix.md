# FleetSync · Requirements Traceability Matrix

| | |
|---|---|
| **Owner** | Ahmet Can Vurmaz (Product Owner & Requirements Engineer) |
| **Version** | 1.0 · Sprint 2 |
| **Sources** | `docs/product_backlog.md`, `docs/openapi.yaml`, `docs/test_plans_and_coverage.md` |

| Story ID | Priority | Target | SRS Req | OpenAPI Endpoint(s) | Test Case ID(s) | Issue / PR |
|---|---|---|---|---|---|---|
| **US-01** | Must | Sprint 3 | REQ-ID-01 | `POST /auth/login`, `GET /me` | TC-AUTH-01, TC-AUTH-02, TC-AUTH-03 | #153 (F1.1) |
| **US-02** | Must | Sprint 3 | REQ-ID-02 | `GET /users`, `POST /users` | TC-AUTH-04 | #153 (F1.1) |
| **US-03** | Must | Sprint 3 | REQ-ID-03 | `POST /drivers/{id}/licenses`, `GET /drivers/{id}/licenses`, `GET /drivers/{id}` | *Sprint 2 QA (pending)* | #154 (F1.2) |
| **US-04** | Must | Sprint 3 | REQ-ID-04 | `POST /drivers/{id}/licenses/{licenseId}/verify` | TC-ELG-05 | #154 (F1.2) |
| **US-05** | Must | Sprint 3 | REQ-ID-05 | `GET /drivers/{id}/eligibility` | TC-ELG-01 – TC-ELG-04 | #155 (F1.3) |
| **US-06** | Could | Final | REQ-ID-06 | `PUT /drivers/{id}` | *Final* | #153 (F1.1) |
| **US-07** | Must | Sprint 3 | REQ-VEH-01 | `POST /vehicles` | *Sprint 2 QA (pending)* | #156 (F2.1) |
| **US-08** | Must | Sprint 3 | REQ-VEH-02 | `GET /vehicles`, `GET /vehicles/{id}` | *Sprint 2 QA (pending)* | #156 (F2.1) |
| **US-09** | Should | Final | REQ-VEH-03 | `PATCH /vehicles/{id}`, `POST /vehicles/{id}/status` | TC-MNT-10 | #156 (F2.1) |
| **US-10** | Should | Final | REQ-MNT-01 | `GET /maintenance/rules`, `PUT /maintenance/rules/{ruleId}` | *Final* | #157 (F3.1) |
| **US-11** | Must | Sprint 3 | REQ-MNT-01 | `GET /vehicles/{id}/maintenance-status` | TC-MNT-01 – TC-MNT-04 | #157 (F3.1) |
| **US-12** | Must | Sprint 3 | REQ-MNT-02 | `GET /vehicles/recommendations` | TC-REC-01 – TC-REC-03, TC-E2E-01 | #157 (F3.1) |
| **US-13** | Must | Sprint 3 | REQ-MNT-03 | `POST /reservations/{id}/return` | TC-MNT-05 – TC-MNT-07, TC-E2E-03 | #158 (F3.2) |
| **US-14** | Must | Sprint 3 | REQ-MNT-03 | `GET /maintenance/alerts` | *Sprint 2 QA (pending)* | #158 (F3.2) |
| **US-15** | Must | Sprint 3 | REQ-MNT-03 | `POST /maintenance/records` | TC-MNT-08, TC-MNT-09, TC-E2E-04 | #158 (F3.2) |
| **US-16** | Should | Final | REQ-MNT-03 | `GET /maintenance/calendar` | *Final* | #159 (F3.3) |
| **US-17** | Could | Final | REQ-MNT-03 | `GET /vehicles/{id}/maintenance-records` | *Final* | #159 (F3.3) |
| **US-18** | Must | Sprint 3 | REQ-RES-01 | `GET /locations` | *Sprint 2 QA (pending)* | #160 (F4.1) |
| **US-19** | Must | Sprint 3 | REQ-RES-01 | `GET /vehicles/recommendations` | TC-REC-04 – TC-REC-06, TC-E2E-01 | #160 (F4.1) |
| **US-20** | Must | Sprint 3 | REQ-RES-02 | `POST /reservations` | TC-RES-01 – TC-RES-05, TC-RES-08 – TC-RES-10, TC-E2E-01 | #161 (F4.2) |
| **US-21** | Must | Sprint 3 | REQ-RES-02 | `GET /reservations`, `GET /reservations/{id}` | TC-RES-07 | #161 (F4.2) |
| **US-22** | Should | Final | REQ-RES-02 | `POST /reservations/{id}/cancel` | TC-RES-06 | #161 (F4.2) |
| **US-23** | Must | Sprint 3 | REQ-CRP-01 | `GET /rides/matches` | TC-POOL-01 – TC-POOL-03 | #162 (F5.1) |
| **US-24** | Must | Sprint 3 | REQ-CRP-02 | `POST /reservations/{id}/passengers` | TC-POOL-04 – TC-POOL-06, TC-E2E-02 | #162 (F5.1) |
| **US-25** | Could | Final | REQ-CRP-02 | `DELETE /reservations/{id}/passengers/{userId}` | *Final* | #162 (F5.1) |
| **US-26** | Must | Sprint 3 | REQ-HND-01 | `GET /checklist-templates`, `POST /reservations/{id}/pickup` | TC-HND-01, TC-HND-02, TC-E2E-03 | #163 (F6.1) |
| **US-27** | Must | Sprint 3 | REQ-HND-02 | `POST /reservations/{id}/return` | TC-HND-03 – TC-HND-06, TC-E2E-03 | #163 (F6.1) |
| **US-28** | Should | Final | REQ-HND-03 | `POST /damage-reports`, `GET /vehicles/{id}/damage-reports` | *Final* | #164 (F6.2) |
| **US-29** | Must | Sprint 3 | REQ-FUE-01 | `POST /fuel-receipts` | TC-FUEL-01 – TC-FUEL-04 | #165 (F7.1) |
| **US-30** | Should | Final | REQ-FUE-01 | `GET /vehicles/{id}/fuel-receipts`, `GET /vehicles/{id}/consumption` | TC-FUEL-05 | #165 (F7.1) |
| **US-31** | Should | Final | REQ-FUE-02 | `POST /fuel-receipts`, `GET /fuel/anomalies` | TC-FUEL-06 – TC-FUEL-09 | #165 (F7.1) |
| **US-32** | Could | Final | REQ-FUE-03 | `POST /expenses`, `GET /expenses` | *Final* | #166 (F7.2) |
| **US-33** | Should | Final | REQ-REP-01 | `GET /reports/summary` | *Final* | #167 (F8.1) |
| **US-34** | Must | Final | REQ-REP-01 | `GET /reports/cost` | TC-E2E-05 | #167 (F8.1) |
| **US-35** | Must | Final | REQ-REP-02 | `GET /reports/carbon` | TC-E2E-05 | #168 (F8.2) |
| **US-36** | Must | Final | REQ-REP-03 | `GET /reports/utilization` | TC-E2E-05 | #167 (F8.1) |
| **US-37** | Could | Final | REQ-REP-04 | `GET /reports/cost` (`Accept: text/csv`) | *Final* | #167 (F8.1) |
| **US-38** | Must | Sprint 3 | UI (§4) | `POST /auth/login`, `GET /me` | TC-E2E-01 – TC-E2E-05 | #169 (F9.1) |
| **US-39** | Must | Sprint 3 | UI (§4) | `GET /vehicles` | TC-E2E-01 – TC-E2E-05 | #169 (F9.1) |
| **US-40** | Must | Sprint 3 | UI (§4) | `GET /vehicles/recommendations`, `POST /reservations` | TC-E2E-01 | #170 (F9.2) |
| **US-41** | Must | Sprint 3 | UI (§4) | `GET /rides/matches`, `POST /reservations/{id}/passengers` | TC-E2E-02 | #170 (F9.2) |
| **US-42** | Must | Sprint 3 | UI (§4) | `GET /checklist-templates`, `POST .../pickup`, `POST .../return` | TC-E2E-03 | #171 (F9.3) |
| **US-43** | Must | Sprint 3 | UI (§4) | `GET /maintenance/alerts`, `GET /maintenance/calendar`, `POST /maintenance/records` | TC-E2E-04 | #171 (F9.3) |
| **US-44** | Should | Final | UI (§4) | `POST /fuel-receipts`, `GET /vehicles/{id}/fuel-receipts` | *Final* | #172 (F9.4) |
| **US-45** | Should | Final | UI (§4) | `GET /reports/*` | TC-E2E-05 | #172 (F9.4) |
| **US-46** | Must | Sprint 3 | NFR (§5) | — (Docker Compose) | CI Pipeline | #173 (F10.1) |
| **US-47** | Must | Sprint 3 | NFR (§5) | — (Seed Data) | CI Pipeline / TC-E2E-01 | #173 (F10.1) |
| **US-48** | Must | Sprint 3 | NFR (§5) | — (GitHub Actions CI) | CI Pipeline | #173 (F10.1) |
| **US-49** | Must | Sprint 3 | NFR (§5) | — (pytest-cov ≥ 50%) | CI Pipeline | #174 (F10.2) |
| **US-50** | Must | Final | NFR (§5) | — (Playwright E2E) | TC-E2E-01 – TC-E2E-05 | #174 (F10.2) |
| **US-51** | Must | Final | NFR (§5) | — (PostgreSQL Integration) | CI Pipeline | #174 (F10.2) |
| **US-52** | Should | Final | NFR (§5) | — (SonarQube) | CI Pipeline | #174 (F10.2) |
