# FleetSync · Problem Definition and Project Proposal

| | |
|---|---|
| Course | SENG 321 Software Engineering · Sprint 1, deliverable 1 |
| Author (Product Owner) | Ahmet Can Vurmaz |
| Date | 2026-10-25 · revised 2026-10-31 |
| Related documents | [`system_vision.md`](system_vision.md) (system boundary), [`openapi.yaml`](openapi.yaml) (API contract), [`product_backlog.md`](product_backlog.md) (initial backlog), [`raci_matrix.md`](raci_matrix.md) (roles) |

## 1. Introduction and Background

Many institutions and campuses operate a shared vehicle fleet to support their staff's official travel needs. However, the management of these fleets is often decentralized and handled through informal channels such as phone calls, emails, and manual spreadsheets. This unstructured approach creates a lack of visibility, leading to significant administrative overhead, safety risks, and unnecessary expenses.

## 2. Problem Statement

The current manual approach to fleet management presents four critical issues:

1. **Scheduling Conflicts and Inefficiency:** Vehicles are requested informally without a unified calendar. As a result, the same vehicle can easily be promised to two different people, leading to double bookings and last-minute confusion.
2. **Safety and Maintenance Risks:** Maintenance schedules (oil changes, tire replacements, routine inspections) are tracked manually, relying on human memory or outdated logs. Consequently, vehicles that are due for service often continue to be assigned for trips, posing significant safety risks to drivers.
3. **Redundant Trips:** Because staff members cannot see who else is travelling, it is common for multiple individuals to drive separate vehicles to the exact same destination on the same day. This wastes fuel and limits vehicle availability for others.
4. **Lack of Financial and Environmental Visibility:** Crucial data such as trip mileage, fuel receipts, and vehicle damage are recorded on loose paper or ignored entirely. This makes it impossible to accurately track overall fleet costs, detect anomalies in fuel consumption, or calculate the institution's carbon footprint.

### 2.1 Supporting Evidence

| Problem | Evidence | What it shows |
|---|---|---|
| 1. Scheduling conflicts | A spreadsheet or a shared calendar does not reject a second booking of the same vehicle for an overlapping period; the conflict is only noticed when two people arrive for the same car. | Conflict prevention needs a rule enforced by the system, not a shared document. |
| 2. Maintenance risk | Service intervals depend on two variables that change every trip (odometer and date). In Turkey, periodic vehicle inspection is also a legal obligation under the Highway Traffic Act (Law No. 2918). With manual tracking nobody recalculates the remaining distance after each trip, so a vehicle can pass its service interval between two checks. | Mileage must be captured at every return and evaluated automatically. |
| 3. Redundant trips | Trip requests arrive by phone or email to different people, so there is no single place where two requests to the same destination at the same time can be compared. | Ride sharing requires a shared, searchable list of trips. |
| 4. No cost or emission visibility | Fuel receipts, tolls and odometer readings are kept on paper or not kept. Consumption per 100 km, cost per vehicle and CO₂ emissions cannot be calculated without this data. | Fuel, expense and mileage data must be recorded digitally per vehicle and trip. |

These problems were identified from the project brief and from analysing how a shared campus fleet is typically managed with phone, email and spreadsheets. They are measured by the success criteria in section 6, which become the goals G1–G6 in `system_vision.md`.

## 3. Stakeholder Identification and Analysis

### 3.1 Stakeholders

* **Staff Members / Drivers:** Need a reliable, fast way to book vehicles and share rides for official duties.
* **Fleet Managers:** Need to ensure fleet availability, enforce safety rules, verify driving licences, and monitor budgets and emissions.
* **Maintenance Officers:** Need accurate, timely alerts for vehicle servicing to prevent breakdowns.
* **Institution Management (Sponsor):** Interested in fair usage, cost savings, and sustainability metrics.
* **Passengers in shared rides:** Staff members who join an existing trip; they need a seat at the right time.
* **Vehicle workshop:** Outside the system; receives vehicles for service when FleetSync raises an alert.
* **Course instructor and jury:** Assess the product, the process and the individual contributions.

### 3.2 Stakeholder Analysis

| Stakeholder | Interest | Influence | Main need | Engagement |
|---|---|---|---|---|
| Staff members / drivers | High | Medium | Book a safe vehicle in under 2 minutes | Primary users; usability test with the Figma prototype |
| Fleet managers | High | High | Safe, available and affordable fleet; reports | Primary users and source of business rules; acceptance of rules and reports |
| Maintenance officers | High | Medium | Timely, data-based service alerts | Primary users of alerts and the maintenance calendar |
| Institution management | Medium | High | Cost savings, fair use, sustainability | Keep satisfied: cost, carbon and utilisation reports |
| Passengers | Medium | Low | A seat on a trip they need | Covered through the staff role |
| Vehicle workshop | Low | Low | Clear service requests | Keep informed; outside the system |
| Instructor and jury | High | High | A working demo, traceable process and documentation | Sprint deliveries, GitHub evidence and the live demo |

## 4. Proposed Solution: FleetSync

**FleetSync** is a centralized, web-based fleet management platform designed to automate and optimize the reservation, maintenance, and monitoring of shared vehicles. It replaces spreadsheets and disjointed communication with a unified system that enforces business rules and ensures safety.

By acting as the single source of truth for the fleet, FleetSync applies consistent reservation, driver licence, and maintenance rules to every request, while maintaining a complete history of vehicle usage and condition.

## 5. Key Capabilities

* **Smart Reservations & Ride Sharing:** Users can view vehicle availability, make reservations, and see existing trips to their destination. This encourages carpooling, reducing the number of vehicles on the road.
* **Predictive Maintenance & Safety Blocks:** The system tracks mileage and dates automatically. It proactively blocks unsafe vehicles (those close to needing maintenance) from being reserved and generates alerts for the maintenance staff.
* **Digital Handovers:** Drivers complete digital pickup and return checklists, ensuring accurate logging of odometer readings, fuel levels, and any new damage.
* **Fuel & Expense Tracking:** Drivers record fuel receipts and trip expenses; the system calculates consumption and flags anomalies.
* **Reporting & Analytics:** Fleet managers gain access to detailed reports on vehicle utilization, financial costs, fuel anomalies, and carbon emissions.

## 6. Expected Outcomes and Success Criteria for Initial Release

The implementation of FleetSync will be considered successful if it achieves the following measurable targets:

* **Zero Safety Breaches:** No trip starts with a vehicle whose remaining service distance is dangerously low.
* **Zero Double Bookings:** The system prevents any overlapping confirmed reservations for the same vehicle.
* **Data-Driven Maintenance:** 100% of maintenance alerts are triggered automatically by system data (odometer readings and dates) rather than manual memory.
* **Fast Usability:** A staff member can complete a valid vehicle request in under 2 minutes.
* **Increased Efficiency:** Measurable reduction in vehicles used for identical trips via the ride-sharing feature.
* **Complete Visibility:** Reports on cost, carbon emissions, and fleet utilization are readily available.

These targets correspond to goals G1–G6 in `system_vision.md` and are verified by the acceptance criteria in `product_backlog.md`.

## 7. Feasibility Assessment

| Dimension | Assessment | Result |
|---|---|---|
| Technical | The product is a web front end, a REST API and a relational database. The chosen stack is widely documented and free: React (Vite, Tailwind CSS), Python with FastAPI, PostgreSQL, Docker Compose and GitHub Actions. FastAPI and the API-first OpenAPI contract let front end and back end work in parallel. The business rules (maintenance thresholds, conflict checks, ride matching) are deterministic and do not need external services. | Feasible |
| Schedule | 10 weeks with four assessed deliveries (weeks 2, 5, 8, 10). The backlog separates Must stories for the Sprint 3 MVP from Should and Could stories for the final release, so lower-priority work can be dropped without affecting the demo. | Feasible with prioritisation |
| Team and operational | Seven members, each with a defined role and a module (see `raci_matrix.md`). All users reach the system through a browser, and the whole product starts with one `docker compose up` command. | Feasible |
| Economic | All tools and libraries are open source or free for students; development and demo run locally in Docker. No paid API is needed in release 1 (maps, GPS and SMS are deferred). | Feasible, zero cost |
| Legal and ethical | Names, emails, phone numbers and licence numbers are personal data under KVKK (Law No. 6698). FleetSync stores only the data the rules need, restricts licence data to the owner and fleet managers, and uses invented data in the demo. | Feasible with the listed measures |

## 8. Initial Project Scope

**In scope for release 1:** accounts and the three roles, driver licence verification and eligibility, the vehicle inventory, mileage- and date-based predictive maintenance with alerts and trip blocking, vehicle recommendation, reservations with conflict prevention, ride sharing, digital pickup and return checklists with damage reports, fuel receipts and expenses with anomaly detection, and cost, carbon and utilisation reports.

**Out of scope for release 1:** single sign-on, live GPS tracking and map routing, a mobile application, a reservation approval workflow, OCR reading of receipts, email notifications, payments, fines, fuel cards, insurance, payroll and vehicle purchasing.

The detailed boundary is defined in `system_vision.md` §7, and the scope is broken down into epics and user stories in `product_backlog.md`.

## 9. Assumptions

| # | Assumption |
|---|---|
| A1 | Drivers enter the odometer reading honestly at pickup and return. |
| A2 | Trip destinations come from a predefined list with known road distances. |
| A3 | Each vehicle has one active reservation at a time; passengers join it instead of booking separately. |
| A4 | The fleet manager verifies licences from the physical document. |
| A5 | Users have a modern web browser and network access on campus. |
| A6 | Fleet size is in the tens of vehicles and hundreds of users. |

The consequences of each assumption turning out false are described in `system_vision.md` §9.

## 10. Potential Risks

| # | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| R1 | Scope is too large for 10 weeks | Medium | High | MoSCoW priorities; Must stories first; Should and Could stories can be dropped | Product Owner |
| R2 | Modules work alone but fail when integrated | Medium | High | API-first contract in `openapi.yaml`; integration tests against PostgreSQL; early end-to-end integration in Sprint 3 | Lead Architect, QA |
| R3 | Unit test coverage stays below the required 50% | Medium | High | Tests required in the pull request checklist; coverage measured in CI | QA, DevOps |
| R4 | The demo flow breaks in front of the jury | Low | High | Automated end-to-end test of the demo journey; fixed seed data; rehearsal before the demo | QA |
| R5 | Uneven individual contributions or a member becomes unavailable | Medium | Medium | Every task is a GitHub Issue with an owner; contributions tracked through commits and pull requests; dependencies visible in the backlog | Scrum Master |
| R6 | Team members are new to the stack (FastAPI, React, Docker) | Medium | Medium | Shared project template, pair work, short knowledge sessions in Sprint 2 | Lead Architect |
| R7 | Personal data is mishandled | Low | High | Only invented data in the demo; data minimisation and role checks on the server (KVKK) | Product Owner, Lead Architect |
| R8 | Merge conflicts or broken `develop` branch | Medium | Medium | Git-Flow with protected branches, small pull requests and mandatory review | DevOps, Scrum Master |

## 11. Open-Source License Selection

FleetSync is released under the **MIT License** (see `LICENSE` in the repository root).

| Reason | Explanation |
|---|---|
| Simple and permissive | Anyone may use, copy, modify and distribute the code, provided the copyright notice is kept. This suits a course project that other students and the institution may reuse. |
| Compatible with the stack | React, Vite, Tailwind CSS (MIT), FastAPI (MIT), PostgreSQL (PostgreSQL License) and pytest (MIT) are all permissive licenses that are compatible with MIT. |
| Low administrative effort | Unlike GPL, MIT does not require derived works to be released under the same license, so no license review is needed for internal reuse. |

Every new dependency must have an MIT-compatible open-source license; this is checked during pull request review.
