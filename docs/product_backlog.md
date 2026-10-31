# FleetSync · Initial Product Backlog

| | |
|---|---|
| Course | SENG 321 Software Engineering · Sprint 1, deliverable 6 |
| Accountable (A) | Ahmet Can Vurmaz, Product Owner & Requirements Engineer |
| Responsible (R) | Ahmet Can Vurmaz (backlog), Abdullah Tecimen (acceptance criteria review for testability) |
| Consulted (C) | All epic owners |
| Version | 0.1 · Sprint 1 |
| Related documents | [`problem_definition.md`](problem_definition.md), [`system_vision.md`](system_vision.md), [`openapi.yaml`](openapi.yaml), [`test_plans_and_coverage.md`](test_plans_and_coverage.md) |

## 1. How to read this backlog

- **Epic (E1–E10)** is a large capability. Epics follow the modules in `system_vision.md` §7.1, and each has one owner.
- **User story (US-xx)** is one small, testable feature written as *As a … I want … so that …*. Each story is also opened as a GitHub Issue with the same ID in its title, for example `[US-20] Reserve a vehicle for a trip`.
- **Acceptance criteria** use *Given / When / Then*. Each criterion becomes at least one test case in `test_plans_and_coverage.md`.
- **Story points (SP)** are relative effort on the Fibonacci scale 1, 2, 3, 5, 8, 13. A story above 8 SP is split before a sprint starts.
- **Priority** uses MoSCoW: **Must** (needed for the jury demo or a course requirement), **Should** (important, planned for release 1), **Could** (if time allows), **Won't** (out of release 1, see `system_vision.md` §7.3).
- **Target** is the sprint in which the story should be done: *Sprint 3* (MVP, week 8) or *Final* (week 10). Sprint 2 is used for SRS, design and test design of the Sprint 3 stories.
- **Trace** links the story to a rule, goal (G1–G6), assumption (A1–A6) or demo step in `system_vision.md`.

## 2. Definition of Ready and Definition of Done

**A story is ready for a sprint when** it has an owner, an estimate, testable acceptance criteria, its dependencies are done or planned in the same sprint, and its endpoints exist in `openapi.yaml`.

**A story is done when** its code is merged into `develop` through a reviewed pull request, its unit tests pass in CI, every acceptance criterion has been verified by a test, the OpenAPI contract still matches the implementation, and it has no open critical or major bugs.

## 3. Backlog summary

| Epic | Name | Owner | Stories | SP | Must | Should | Could |
|---|---|---|---|---|---|---|---|
| E1 | Identity, Access and Driver Eligibility | Ahmet Can Vurmaz | 6 | 17 | 5 | 0 | 1 |
| E2 | Fleet Inventory | Ali Eren Kurt | 3 | 8 | 2 | 1 | 0 |
| E3 | Predictive Maintenance | Ali Eren Kurt | 8 | 26 | 5 | 2 | 1 |
| E4 | Reservations and Vehicle Recommendation | Ahmet Tarık Orhan | 5 | 18 | 4 | 1 | 0 |
| E5 | Ride Sharing | Ahmet Tarık Orhan | 3 | 10 | 2 | 0 | 1 |
| E6 | Vehicle Handover | Mehmet Umut Oğuzcan | 3 | 13 | 2 | 1 | 0 |
| E7 | Fuel and Expenses | Abdullah Tecimen | 4 | 13 | 1 | 2 | 1 |
| E8 | Reporting | Deniz Alp Oniki | 5 | 13 | 3 | 1 | 1 |
| E9 | User Interface | Mustafa Düşünceli | 8 | 32 | 6 | 2 | 0 |
| E10 | Platform, Quality and Delivery | Deniz Alp Oniki | 7 | 27 | 6 | 1 | 0 |
| **Total** | | | **52** | **177** | **36** | **11** | **5** |

Sprint 3 (MVP) holds 31 stories / 116 SP; Final holds 21 stories / 61 SP.

## 4. Jury demo journey and the stories behind it

All of these stories are **Must**. The demo is the order in which they are integrated and tested end to end (US-50).

| Demo step (`system_vision.md` §11) | Stories |
|---|---|
| 1. A staff member requests a vehicle for a trip | US-01, US-18, US-40 |
| 2. FleetSync blocks the vehicle whose service is close, explains why, and recommends a suitable one | US-05, US-11, US-12, US-19, US-20 |
| 3. A colleague travelling to the same destination joins the ride | US-23, US-24, US-41 |
| 4. The driver picks up the vehicle with the checklist | US-26, US-42 |
| 5. On return the driver enters the mileage; FleetSync raises "10,000 km service is due", moves the vehicle to maintenance and notifies the maintenance officer | US-27, US-13, US-14, US-42, US-43 |
| 6. The maintenance officer records the service and the vehicle becomes available again | US-15, US-43 |
| 7. The fleet manager sees cost, carbon and utilisation for the period | US-34, US-35, US-36 |
| Runs with one command and seed data | US-46, US-47 |

## 5. Epics and user stories

### E1 · Identity, Access and Driver Eligibility

*Accounts, JWT login, the three roles, driving licences and the eligibility check for each trip.* Module: `identity` · Owner: Ahmet Can Vurmaz · 6 stories · 17 SP

| ID | Story | SP | Priority | Depends on | Owner | Target |
|---|---|---|---|---|---|---|
| US-01 | Log in with email and password | 3 | Must | — | Ahmet Can Vurmaz | Sprint 3 |
| US-02 | Manage user accounts and roles | 3 | Must | US-01 | Ahmet Can Vurmaz | Sprint 3 |
| US-03 | Register a driving licence | 3 | Must | US-02 | Ahmet Can Vurmaz | Sprint 3 |
| US-04 | Verify a driving licence | 2 | Must | US-03 | Ahmet Can Vurmaz | Sprint 3 |
| US-05 | Check driver eligibility for a vehicle and trip | 5 | Must | US-04, US-07 | Ahmet Can Vurmaz | Sprint 3 |
| US-06 | Update driver profile | 1 | Could | US-02 | Ahmet Can Vurmaz | Final |

#### US-01 · Log in with email and password

**As a** user of any role, **I want to** log in with my email and password, **so that** I can use the functions allowed for my role.

Acceptance criteria:

1. **Given** a registered user, **when** they log in with a correct email and password, **then** a JWT and their role are returned.
2. **Given** a registered user, **when** they log in with a wrong password, **then** the request is rejected with 401 `INVALID_CREDENTIALS`.
3. **Given** no token, **when** any endpoint other than login is called, **then** the request is rejected with 401 `UNAUTHORIZED`.

SP: 3 · Priority: Must · Depends on: — · Owner: Ahmet Can Vurmaz · Target: Sprint 3  
API: `POST /auth/login`, `GET /me`  
Trace: §10 Security

#### US-02 · Manage user accounts and roles

**As a** fleet manager, **I want to** create user accounts with one of the three roles, **so that** every staff member, manager and maintenance officer can use the system.

Acceptance criteria:

1. **Given** a fleet manager, **when** they create a user with a new email and a role, **then** the user is created (201) and can log in.
2. **Given** an existing email, **when** a user is created with that email, **then** the request is rejected with 409 `DUPLICATE_EMAIL`.
3. **Given** a `STAFF` user, **when** they try to create a user, **then** the request is rejected with 403 `FORBIDDEN`.

SP: 3 · Priority: Must · Depends on: US-01 · Owner: Ahmet Can Vurmaz · Target: Sprint 3  
API: `GET /users`, `POST /users`  
Trace: §5.1 Actors

#### US-03 · Register a driving licence

**As a** staff member, **I want to** add my driving licence to my profile, **so that** I can be allowed to drive fleet vehicles.

Acceptance criteria:

1. **Given** a staff member, **when** they add a licence with class, number and expiry date, **then** the licence is saved with status *not verified*.
2. **Given** a licence number already registered, **when** it is added again, **then** the request is rejected with 409 `DUPLICATE_LICENSE`.
3. **Given** an expiry date in the past, **when** the licence is added, **then** the request is rejected with 400 `VALIDATION_ERROR`.

SP: 3 · Priority: Must · Depends on: US-02 · Owner: Ahmet Can Vurmaz · Target: Sprint 3  
API: `POST /drivers/{driverId}/licenses`, `GET /drivers/{driverId}/licenses`, `GET /drivers/{driverId}`  
Trace: §8 Driver eligibility

#### US-04 · Verify a driving licence

**As a** fleet manager, **I want to** mark a licence as verified after checking the physical document, **so that** only drivers with a checked licence can take vehicles.

Acceptance criteria:

1. **Given** an unverified licence, **when** a fleet manager verifies it, **then** the licence becomes verified.
2. **Given** a `STAFF` user, **when** they try to verify a licence, **then** the request is rejected with 403 `FORBIDDEN`.

SP: 2 · Priority: Must · Depends on: US-03 · Owner: Ahmet Can Vurmaz · Target: Sprint 3  
API: `POST /drivers/{driverId}/licenses/{licenseId}/verify`  
Trace: §8 Driver eligibility, A4

#### US-05 · Check driver eligibility for a vehicle and trip

**As a** system, **I want to** check whether a driver may drive a vehicle until the trip ends, **so that** no trip starts with an unqualified driver.

Acceptance criteria:

1. **Given** a verified licence of the required class, valid after the trip ends, **when** eligibility is checked, **then** the driver is eligible.
2. **Given** a licence that expires before the trip ends, **when** eligibility is checked, **then** the driver is not eligible, reason `LICENSE_EXPIRED`.
3. **Given** a licence class that does not allow the vehicle, **when** eligibility is checked, **then** the driver is not eligible, reason `LICENSE_CLASS_MISMATCH`.
4. **Given** an unverified licence, **when** eligibility is checked, **then** the driver is not eligible.

SP: 5 · Priority: Must · Depends on: US-04, US-07 · Owner: Ahmet Can Vurmaz · Target: Sprint 3  
API: `GET /drivers/{driverId}/eligibility`  
Trace: §8 Driver eligibility

#### US-06 · Update driver profile

**As a** staff member, **I want to** update my contact details, **so that** the fleet manager can reach me.

Acceptance criteria:

1. **Given** a staff member, **when** they update their own phone number, **then** the profile is updated.
2. **Given** a staff member, **when** they try to update another user's profile, **then** the request is rejected with 403 `FORBIDDEN`.

SP: 1 · Priority: Could · Depends on: US-02 · Owner: Ahmet Can Vurmaz · Target: Final  
API: `PUT /drivers/{driverId}`  
Trace: §10 Legal / ethical (KVKK)

### E2 · Fleet Inventory

*Vehicles, their attributes and the vehicle status state machine.* Module: `vehicle` · Owner: Ali Eren Kurt · 3 stories · 8 SP

| ID | Story | SP | Priority | Depends on | Owner | Target |
|---|---|---|---|---|---|---|
| US-07 | Add a vehicle to the fleet | 3 | Must | US-01 | Ali Eren Kurt | Sprint 3 |
| US-08 | List vehicles with their current status | 2 | Must | US-07 | Ali Eren Kurt | Sprint 3 |
| US-09 | Update vehicle data and status | 3 | Should | US-07 | Ali Eren Kurt | Final |

#### US-07 · Add a vehicle to the fleet

**As a** fleet manager, **I want to** add a vehicle with plate, seats, fuel type, tank capacity, required licence class and odometer, **so that** it can be recommended and reserved.

Acceptance criteria:

1. **Given** a fleet manager, **when** they add a vehicle with valid data, **then** the vehicle is created with status `AVAILABLE`.
2. **Given** an existing plate, **when** a vehicle is added with the same plate, **then** the request is rejected with 409 `DUPLICATE_PLATE`.
3. **Given** a negative odometer or zero seats, **when** the vehicle is added, **then** the request is rejected with 400 `VALIDATION_ERROR`.

SP: 3 · Priority: Must · Depends on: US-01 · Owner: Ali Eren Kurt · Target: Sprint 3  
API: `POST /vehicles`  
Trace: §7.1 Fleet inventory

#### US-08 · List vehicles with their current status

**As a** user of any role, **I want to** see all vehicles with their status and maintenance summary, **so that** I know which vehicles are available.

Acceptance criteria:

1. **Given** vehicles in different statuses, **when** the list is filtered by `AVAILABLE`, **then** only available vehicles are returned.
2. **Given** a vehicle ID that does not exist, **when** its details are requested, **then** the request is rejected with 404 `NOT_FOUND`.

SP: 2 · Priority: Must · Depends on: US-07 · Owner: Ali Eren Kurt · Target: Sprint 3  
API: `GET /vehicles`, `GET /vehicles/{vehicleId}`  
Trace: §7.1 Fleet inventory

#### US-09 · Update vehicle data and status

**As a** fleet manager, **I want to** edit vehicle details and take a vehicle out of service, **so that** the fleet data stays correct.

Acceptance criteria:

1. **Given** an `AVAILABLE` vehicle, **when** the manager sets it to `OUT_OF_SERVICE`, **then** the status changes.
2. **Given** an `IN_MAINTENANCE` vehicle, **when** the manager sets it to `AVAILABLE` manually, **then** the request is rejected with 409 `INVALID_STATUS_TRANSITION` (only a service record releases it).

SP: 3 · Priority: Should · Depends on: US-07 · Owner: Ali Eren Kurt · Target: Final  
API: `PATCH /vehicles/{vehicleId}`, `POST /vehicles/{vehicleId}/status`  
Trace: §8 Automatic maintenance status

### E3 · Predictive Maintenance

*Mileage- and date-based maintenance rules, alerts, trip blocking, service records and the maintenance calendar.* Module: `maintenance` · Owner: Ali Eren Kurt · 8 stories · 26 SP

| ID | Story | SP | Priority | Depends on | Owner | Target |
|---|---|---|---|---|---|---|
| US-10 | Configure maintenance rule intervals | 2 | Should | US-07 | Ali Eren Kurt | Final |
| US-11 | Calculate remaining km and days for each rule | 5 | Must | US-10 | Ali Eren Kurt | Sprint 3 |
| US-12 | Block vehicles whose maintenance is too close for a trip | 5 | Must | US-11 | Ali Eren Kurt | Sprint 3 |
| US-13 | Move a vehicle to maintenance automatically on return | 5 | Must | US-11, US-27 | Ali Eren Kurt | Sprint 3 |
| US-14 | List maintenance alerts | 2 | Must | US-13 | Ali Eren Kurt | Sprint 3 |
| US-15 | Record completed maintenance and release the vehicle | 3 | Must | US-13 | Ali Eren Kurt | Sprint 3 |
| US-16 | View the maintenance calendar | 3 | Should | US-11 | Ali Eren Kurt | Final |
| US-17 | View maintenance history of a vehicle | 1 | Could | US-15 | Ali Eren Kurt | Final |

#### US-10 · Configure maintenance rule intervals

**As a** fleet manager, **I want to** view and change the km and month intervals of maintenance rules, **so that** the rules match the institution's service policy.

Acceptance criteria:

1. **Given** the default rules, **when** they are listed, **then** oil change 10,000 km / 12 months, tyres 40,000 km / 48 months and inspection 24 months are returned.
2. **Given** a fleet manager, **when** they change the oil change interval to 15,000 km, **then** the new interval is used in all later evaluations.
3. **Given** an interval of 0 or below, **when** it is saved, **then** the request is rejected with 400 `VALIDATION_ERROR`.

SP: 2 · Priority: Should · Depends on: US-07 · Owner: Ali Eren Kurt · Target: Final  
API: `GET /maintenance/rules`, `PUT /maintenance/rules/{ruleId}`  
Trace: §8 Maintenance intervals

#### US-11 · Calculate remaining km and days for each rule

**As a** fleet manager, **I want to** see how many km and days are left before each service of a vehicle, **so that** I can plan maintenance before it is needed.

Acceptance criteria:

1. **Given** last oil change at 0 km and odometer 8,999 km, **when** maintenance status is calculated, **then** oil change is `OK` with 1,001 km remaining.
2. **Given** last oil change at 0 km and odometer 9,000 km, **when** maintenance status is calculated, **then** oil change is `DUE_SOON`.
3. **Given** last oil change at 0 km and odometer 10,000 km, **when** maintenance status is calculated, **then** oil change is `DUE`.
4. **Given** a due date 30 days away, **when** maintenance status is calculated, **then** the rule is `DUE_SOON` (tyres: 60 days).

SP: 5 · Priority: Must · Depends on: US-10 · Owner: Ali Eren Kurt · Target: Sprint 3  
API: `GET /vehicles/{vehicleId}/maintenance-status`  
Trace: §8 Warning threshold

#### US-12 · Block vehicles whose maintenance is too close for a trip

**As a** staff member, **I want to** never be offered a vehicle that will need service during my trip, **so that** I travel safely.

Acceptance criteria:

1. **Given** a vehicle with 350 km left and a 300 km trip, **when** it is evaluated for the trip, **then** it is blocked, because 350 < 300 + 100.
2. **Given** a vehicle with 400 km left and a 300 km trip, **when** it is evaluated for the trip, **then** it is not blocked (400 is not below 400).
3. **Given** a rule whose due date falls before the trip ends, **when** the vehicle is evaluated, **then** it is blocked with reason `MAINTENANCE_DUE_SOON`.

SP: 5 · Priority: Must · Depends on: US-11 · Owner: Ali Eren Kurt · Target: Sprint 3  
API: `GET /vehicles/recommendations (used by)`  
Trace: §8 Trip blocking, G1, Demo step 2

#### US-13 · Move a vehicle to maintenance automatically on return

**As a** maintenance officer, **I want to** the system to raise an alert and take the vehicle out of use when a service becomes due, **so that** no vehicle is used past its service interval.

Acceptance criteria:

1. **Given** oil change last at 0 km, **when** the vehicle is returned with odometer 9,999 km, **then** no `DUE` alert is raised and the vehicle becomes `AVAILABLE`.
2. **Given** oil change last at 0 km, **when** the vehicle is returned with odometer 10,000 km, **then** a "10,000 km service is due" alert is raised and the vehicle becomes `IN_MAINTENANCE`.
3. **Given** oil change last at 0 km, **when** the vehicle is returned with odometer 10,050 km, **then** the alert is raised and the vehicle becomes `IN_MAINTENANCE`.
4. **Given** an alert raised on return, **when** the maintenance officer opens the application, **then** the new alert is visible to them.

SP: 5 · Priority: Must · Depends on: US-11, US-27 · Owner: Ali Eren Kurt · Target: Sprint 3  
API: `POST /reservations/{reservationId}/return (triggers)`  
Trace: §8 Automatic maintenance status, G3, Demo step 5

#### US-14 · List maintenance alerts

**As a** maintenance officer, **I want to** see all open maintenance alerts, **so that** I know which vehicles to send to service.

Acceptance criteria:

1. **Given** open and resolved alerts, **when** the list is filtered by open status, **then** only open alerts are returned, newest first.
2. **Given** alerts for several vehicles, **when** the list is filtered by vehicle, **then** only that vehicle's alerts are returned.

SP: 2 · Priority: Must · Depends on: US-13 · Owner: Ali Eren Kurt · Target: Sprint 3  
API: `GET /maintenance/alerts`  
Trace: §6 System context

#### US-15 · Record completed maintenance and release the vehicle

**As a** maintenance officer, **I want to** record a completed service, **so that** the service interval restarts and the vehicle can be used again.

Acceptance criteria:

1. **Given** an `IN_MAINTENANCE` vehicle with an open oil change alert, **when** the officer records an oil change at the current odometer, **then** the alert is resolved, the interval restarts and the vehicle becomes `AVAILABLE`.
2. **Given** a vehicle with another rule still `DUE`, **when** only one service is recorded, **then** the vehicle stays `IN_MAINTENANCE`.
3. **Given** a service odometer lower than the vehicle's odometer, **when** the record is saved, **then** the request is rejected with 422 `ODOMETER_DECREASED`.

SP: 3 · Priority: Must · Depends on: US-13 · Owner: Ali Eren Kurt · Target: Sprint 3  
API: `POST /maintenance/records`  
Trace: §8 Automatic maintenance status, Demo step 6

#### US-16 · View the maintenance calendar

**As a** maintenance officer, **I want to** see expected services in a date range, **so that** I can plan workshop visits.

Acceptance criteria:

1. **Given** vehicles with services expected in the next month, **when** the calendar for that month is requested, **then** each expected service is listed with vehicle, rule and expected date.
2. **Given** a start date after the end date, **when** the calendar is requested, **then** the request is rejected with 400 `VALIDATION_ERROR`.

SP: 3 · Priority: Should · Depends on: US-11 · Owner: Ali Eren Kurt · Target: Final  
API: `GET /maintenance/calendar`  
Trace: §7.1 Predictive maintenance

#### US-17 · View maintenance history of a vehicle

**As a** fleet manager, **I want to** see past services of a vehicle, **so that** I can check its service record.

Acceptance criteria:

1. **Given** a vehicle with recorded services, **when** its history is requested, **then** all services are listed by date.
2. **Given** a vehicle with no services, **when** its history is requested, **then** an empty list is returned.

SP: 1 · Priority: Could · Depends on: US-15 · Owner: Ali Eren Kurt · Target: Final  
API: `GET /vehicles/{vehicleId}/maintenance-records`  
Trace: §2 Vision (complete history)

### E4 · Reservations and Vehicle Recommendation

*Destinations, safe vehicle recommendation, the reservation lifecycle and conflict prevention.* Module: `reservation` · Owner: Ahmet Tarık Orhan · 5 stories · 18 SP

| ID | Story | SP | Priority | Depends on | Owner | Target |
|---|---|---|---|---|---|---|
| US-18 | List trip destinations | 1 | Must | US-01 | Ahmet Tarık Orhan | Sprint 3 |
| US-19 | Recommend safe vehicles for a trip | 8 | Must | US-05, US-12, US-18 | Ahmet Tarık Orhan | Sprint 3 |
| US-20 | Reserve a vehicle for a trip | 5 | Must | US-19 | Ahmet Tarık Orhan | Sprint 3 |
| US-21 | View reservations | 2 | Must | US-20 | Ahmet Tarık Orhan | Sprint 3 |
| US-22 | Cancel a reservation | 2 | Should | US-20 | Ahmet Tarık Orhan | Final |

#### US-18 · List trip destinations

**As a** staff member, **I want to** choose my destination from a list with known distances, **so that** the system knows how long my trip is.

Acceptance criteria:

1. **Given** predefined destinations, **when** the list is requested, **then** each destination is returned with its distance from the main campus.

SP: 1 · Priority: Must · Depends on: US-01 · Owner: Ahmet Tarık Orhan · Target: Sprint 3  
API: `GET /locations`  
Trace: A2

#### US-19 · Recommend safe vehicles for a trip

**As a** staff member, **I want to** see the vehicles that are suitable for my trip, and why the others are not, **so that** I can choose quickly and safely.

Acceptance criteria:

1. **Given** a trip request with destination, period, seats and estimated km, **when** recommendations are requested, **then** only vehicles that pass every rule are recommended.
2. **Given** a vehicle whose maintenance is too close (US-12), **when** recommendations are requested, **then** it is listed as blocked with reason `MAINTENANCE_DUE` or `MAINTENANCE_DUE_SOON`.
3. **Given** a vehicle with fewer seats than requested, **when** recommendations are requested, **then** it is listed as blocked with reason `INSUFFICIENT_SEATS`.
4. **Given** a vehicle already reserved in that period, **when** recommendations are requested, **then** it is listed as blocked with reason `CALENDAR_CONFLICT`.

SP: 8 · Priority: Must · Depends on: US-05, US-12, US-18 · Owner: Ahmet Tarık Orhan · Target: Sprint 3  
API: `GET /vehicles/recommendations`  
Trace: §2 Vision, G1, Demo steps 1–2

#### US-20 · Reserve a vehicle for a trip

**As a** staff member, **I want to** reserve a recommended vehicle, **so that** the vehicle is held for my trip.

Acceptance criteria:

1. **Given** a free, safe vehicle and an eligible driver, **when** a reservation is made, **then** it is created with status `CONFIRMED`.
2. **Given** a reservation 10:00–12:00, **when** another reservation is made for 11:00–13:00 on the same vehicle, **then** the request is rejected with 409 `RESERVATION_CONFLICT`.
3. **Given** a reservation 10:00–12:00, **when** another reservation is made for 12:00–14:00 on the same vehicle, **then** it is accepted (no overlap).
4. **Given** a vehicle blocked for maintenance, **when** it is reserved directly via the API, **then** the request is rejected with 422 `VEHICLE_MAINTENANCE_DUE`.
5. **Given** an end time before the start time, or more than 14 days later, **when** a reservation is made, **then** the request is rejected with 400 `VALIDATION_ERROR`.

SP: 5 · Priority: Must · Depends on: US-19 · Owner: Ahmet Tarık Orhan · Target: Sprint 3  
API: `POST /reservations`  
Trace: §8 No double booking, G2

#### US-21 · View reservations

**As a** staff member, **I want to** see my reservations, and as a fleet manager all reservations, **so that** I know the vehicle calendar.

Acceptance criteria:

1. **Given** a staff member, **when** they list reservations, **then** only their own reservations and rides they joined are returned.
2. **Given** a fleet manager, **when** they list reservations, **then** all reservations are returned.
3. **Given** a staff member, **when** they open another user's reservation, **then** the request is rejected with 403 `FORBIDDEN`.

SP: 2 · Priority: Must · Depends on: US-20 · Owner: Ahmet Tarık Orhan · Target: Sprint 3  
API: `GET /reservations`, `GET /reservations/{reservationId}`  
Trace: §5.1 Actors

#### US-22 · Cancel a reservation

**As a** staff member, **I want to** cancel a reservation I no longer need, **so that** the vehicle becomes free for others.

Acceptance criteria:

1. **Given** a `CONFIRMED` reservation, **when** its owner cancels it, **then** it becomes `CANCELLED` and the period is free again.
2. **Given** an `ACTIVE` reservation, **when** it is cancelled, **then** the request is rejected with 409 `RESERVATION_NOT_CANCELLABLE`.

SP: 2 · Priority: Should · Depends on: US-20 · Owner: Ahmet Tarık Orhan · Target: Final  
API: `POST /reservations/{reservationId}/cancel`  
Trace: §7.1 Reservations

### E5 · Ride Sharing

*Matching requests with existing trips to the same destination and managing passengers.* Module: `carpool` · Owner: Ahmet Tarık Orhan · 3 stories · 10 SP

| ID | Story | SP | Priority | Depends on | Owner | Target |
|---|---|---|---|---|---|---|
| US-23 | Find rides to the same destination | 5 | Must | US-20 | Ahmet Tarık Orhan | Sprint 3 |
| US-24 | Join a ride as a passenger | 3 | Must | US-23 | Ahmet Tarık Orhan | Sprint 3 |
| US-25 | Leave a ride or remove a passenger | 2 | Could | US-24 | Ahmet Tarık Orhan | Final |

#### US-23 · Find rides to the same destination

**As a** staff member, **I want to** see existing trips to my destination at a similar time with free seats, **so that** I can share a vehicle instead of taking another one.

Acceptance criteria:

1. **Given** a ride to the same destination departing 30 minutes after my requested time, with a free seat, **when** matches are requested, **then** the ride is returned.
2. **Given** a ride to the same destination departing 31 minutes after my requested time, **when** matches are requested, **then** the ride is not returned.
3. **Given** a ride with no free seats, or whose driver disabled ride sharing, **when** matches are requested, **then** the ride is not returned.

SP: 5 · Priority: Must · Depends on: US-20 · Owner: Ahmet Tarık Orhan · Target: Sprint 3  
API: `GET /rides/matches`  
Trace: §8 Ride sharing, G5, Demo step 3

#### US-24 · Join a ride as a passenger

**As a** staff member, **I want to** join a matching ride, **so that** I travel without reserving another vehicle.

Acceptance criteria:

1. **Given** a ride with a free seat, **when** a staff member joins it, **then** they are added as a passenger and free seats decrease by one.
2. **Given** a ride with no free seats, **when** a staff member joins it, **then** the request is rejected with 422 `SEAT_CAPACITY_EXCEEDED`.
3. **Given** a staff member already in the ride, **when** they join again, **then** the request is rejected with 409 `ALREADY_JOINED`.

SP: 3 · Priority: Must · Depends on: US-23 · Owner: Ahmet Tarık Orhan · Target: Sprint 3  
API: `POST /reservations/{reservationId}/passengers`  
Trace: §8 Ride sharing, Demo step 3

#### US-25 · Leave a ride or remove a passenger

**As a** passenger, **I want to** leave a ride I no longer need, **so that** the seat becomes free for someone else.

Acceptance criteria:

1. **Given** a passenger in a `CONFIRMED` ride, **when** they leave it, **then** they are removed (204) and free seats increase by one.
2. **Given** an `ACTIVE` ride, **when** a passenger is removed, **then** the request is rejected with 409.

SP: 2 · Priority: Could · Depends on: US-24 · Owner: Ahmet Tarık Orhan · Target: Final  
API: `DELETE /reservations/{reservationId}/passengers/{userId}`  
Trace: §7.1 Ride sharing

### E6 · Vehicle Handover

*Digital pickup and return checklists, odometer and fuel level, damage reports and the mileage limit check.* Module: `handover` · Owner: Mehmet Umut Oğuzcan · 3 stories · 13 SP

| ID | Story | SP | Priority | Depends on | Owner | Target |
|---|---|---|---|---|---|---|
| US-26 | Pick up a vehicle with a digital checklist | 5 | Must | US-20 | Mehmet Umut Oğuzcan | Sprint 3 |
| US-27 | Return a vehicle and enter the current mileage | 5 | Must | US-26 | Mehmet Umut Oğuzcan | Sprint 3 |
| US-28 | Report vehicle damage | 3 | Should | US-26 | Mehmet Umut Oğuzcan | Final |

#### US-26 · Pick up a vehicle with a digital checklist

**As a** driver, **I want to** complete the pickup checklist with odometer and fuel level, **so that** the vehicle's condition at the start of the trip is recorded.

Acceptance criteria:

1. **Given** a `CONFIRMED` reservation and a complete checklist, **when** the driver picks up the vehicle, **then** the reservation becomes `ACTIVE` and the vehicle `IN_USE`.
2. **Given** a checklist with a missing required item, **when** pickup is submitted, **then** the request is rejected with 422 `CHECKLIST_INCOMPLETE`.
3. **Given** a pickup odometer lower than the vehicle's last odometer, **when** pickup is submitted, **then** the request is rejected with 422 `ODOMETER_DECREASED`.

SP: 5 · Priority: Must · Depends on: US-20 · Owner: Mehmet Umut Oğuzcan · Target: Sprint 3  
API: `GET /checklist-templates`, `POST /reservations/{reservationId}/pickup`  
Trace: §8 Mileage integrity, Demo step 4

#### US-27 · Return a vehicle and enter the current mileage

**As a** driver, **I want to** complete the return checklist and enter the odometer reading, **so that** the trip is closed and the vehicle's mileage is up to date.

Acceptance criteria:

1. **Given** an `ACTIVE` reservation, **when** the driver returns the vehicle with a valid odometer, **then** the reservation becomes `COMPLETED`, trip km is calculated and the maintenance rules are evaluated (US-13).
2. **Given** a return odometer lower than the pickup odometer, **when** return is submitted, **then** the request is rejected with 422 `ODOMETER_DECREASED`.
3. **Given** an estimated trip of 100 km, **when** the trip is 131 km, **then** the return is flagged `kmLimitExceeded` (more than 30% longer).
4. **Given** an estimated trip of 100 km, **when** the trip is 130 km, **then** the return is not flagged.

SP: 5 · Priority: Must · Depends on: US-26 · Owner: Mehmet Umut Oğuzcan · Target: Sprint 3  
API: `POST /reservations/{reservationId}/return`  
Trace: §8 Mileage integrity, Demo step 5

#### US-28 · Report vehicle damage

**As a** driver, **I want to** report damage with a description and severity, **so that** the vehicle's condition history is complete.

Acceptance criteria:

1. **Given** a handover or any time during use, **when** the driver reports damage, **then** the damage is saved to the vehicle's history.
2. **Given** a vehicle with damage reports, **when** its damage history is requested, **then** all reports are listed by date.

SP: 3 · Priority: Should · Depends on: US-26 · Owner: Mehmet Umut Oğuzcan · Target: Final  
API: `POST /damage-reports`, `GET /vehicles/{vehicleId}/damage-reports`  
Trace: §7.1 Handover

### E7 · Fuel and Expenses

*Fuel receipts, consumption per 100 km, fuel anomaly detection and trip expenses.* Module: `fuel` · Owner: Abdullah Tecimen · 4 stories · 13 SP

| ID | Story | SP | Priority | Depends on | Owner | Target |
|---|---|---|---|---|---|---|
| US-29 | Record a fuel receipt | 3 | Must | US-07 | Abdullah Tecimen | Sprint 3 |
| US-30 | View fuel receipts and consumption of a vehicle | 3 | Should | US-29 | Abdullah Tecimen | Final |
| US-31 | Detect fuel consumption anomalies | 5 | Should | US-30 | Abdullah Tecimen | Final |
| US-32 | Record trip expenses | 2 | Could | US-07 | Abdullah Tecimen | Final |

#### US-29 · Record a fuel receipt

**As a** driver, **I want to** enter my fuel receipt (litres, total price, odometer, full tank, date, station), **so that** the fleet's fuel use and cost are recorded.

Acceptance criteria:

1. **Given** an existing vehicle, **when** a valid receipt is submitted, **then** it is saved (201) and the unit price is calculated.
2. **Given** litres or total price of 0 or below, **when** the receipt is submitted, **then** the request is rejected with 400 `VALIDATION_ERROR`.
3. **Given** litres above the vehicle's tank capacity, **when** the receipt is submitted, **then** the request is rejected with 422 `FUEL_EXCEEDS_TANK`.
4. **Given** a vehicle ID that does not exist, **when** the receipt is submitted, **then** the request is rejected with 404 `NOT_FOUND`.

SP: 3 · Priority: Must · Depends on: US-07 · Owner: Abdullah Tecimen · Target: Sprint 3  
API: `POST /fuel-receipts`  
Trace: §7.1 Fuel and expenses, §8 Fuel anomaly

#### US-30 · View fuel receipts and consumption of a vehicle

**As a** fleet manager, **I want to** see a vehicle's fuel receipts and its consumption per 100 km, **so that** I can follow fuel cost.

Acceptance criteria:

1. **Given** a vehicle with receipts, **when** its receipts are requested, **then** they are listed by date.
2. **Given** two full-tank receipts 500 km apart with 40 litres filled at the second, **when** consumption is requested, **then** 8.0 L/100 km is returned.
3. **Given** a vehicle with no full-tank pair, **when** consumption is requested, **then** no consumption value is returned and no error occurs.

SP: 3 · Priority: Should · Depends on: US-29 · Owner: Abdullah Tecimen · Target: Final  
API: `GET /vehicles/{vehicleId}/fuel-receipts`, `GET /vehicles/{vehicleId}/consumption`  
Trace: §7.1 Fuel and expenses

#### US-31 · Detect fuel consumption anomalies

**As a** fleet manager, **I want to** the system to flag abnormal fuel consumption, **so that** I can detect fuel misuse or vehicle faults.

Acceptance criteria:

1. **Given** a vehicle averaging 8.0 L/100 km, **when** a receipt gives 10.1 L/100 km (more than 25% above), **then** the receipt is saved and flagged `CONSUMPTION_SPIKE`.
2. **Given** a vehicle averaging 8.0 L/100 km, **when** a receipt gives exactly 10.0 L/100 km (25% above), **then** it is not flagged.
3. **Given** a receipt dated outside any reservation of that vehicle, **when** it is saved, **then** it is flagged `OUTSIDE_RESERVATION`.
4. **Given** a `STAFF` user, **when** they request the anomaly list, **then** the request is rejected with 403 `FORBIDDEN`.

SP: 5 · Priority: Should · Depends on: US-30 · Owner: Abdullah Tecimen · Target: Final  
API: `POST /fuel-receipts (evaluates)`, `GET /fuel/anomalies`  
Trace: §8 Fuel anomaly

#### US-32 · Record trip expenses

**As a** driver, **I want to** record tolls, parking, bridge fees and car washes, **so that** all trip costs appear in the reports.

Acceptance criteria:

1. **Given** a valid category and an amount above 0, **when** an expense is recorded, **then** it is saved and appears in the vehicle's cost.
2. **Given** an amount of 0 or below, **when** an expense is recorded, **then** the request is rejected with 400 `VALIDATION_ERROR`.

SP: 2 · Priority: Could · Depends on: US-07 · Owner: Abdullah Tecimen · Target: Final  
API: `POST /expenses`, `GET /expenses`  
Trace: §7.1 Fuel and expenses

### E8 · Reporting

*Fleet cost, carbon footprint and utilisation reports.* Module: `reporting` · Owner: Deniz Alp Oniki · 5 stories · 13 SP

| ID | Story | SP | Priority | Depends on | Owner | Target |
|---|---|---|---|---|---|---|
| US-33 | See the fleet summary | 2 | Should | US-08 | Deniz Alp Oniki | Final |
| US-34 | Cost report per vehicle | 3 | Must | US-29, US-15 | Deniz Alp Oniki | Final |
| US-35 | Carbon footprint report with ride-sharing savings | 3 | Must | US-29, US-24 | Deniz Alp Oniki | Final |
| US-36 | Utilisation report | 3 | Must | US-20 | Deniz Alp Oniki | Final |
| US-37 | Export reports as CSV | 2 | Could | US-34 | Deniz Alp Oniki | Final |

#### US-33 · See the fleet summary

**As a** fleet manager, **I want to** see key fleet indicators for a period, **so that** I get a quick overview.

Acceptance criteria:

1. **Given** vehicles in different statuses, **when** the summary is requested, **then** counts per status, open alerts and total cost for the period are returned.
2. **Given** a `STAFF` user, **when** they request any report, **then** the request is rejected with 403 `FORBIDDEN`.

SP: 2 · Priority: Should · Depends on: US-08 · Owner: Deniz Alp Oniki · Target: Final  
API: `GET /reports/summary`  
Trace: G6

#### US-34 · Cost report per vehicle

**As a** fleet manager, **I want to** see fuel, expense and maintenance cost per vehicle for a period, **so that** I can control the fleet budget.

Acceptance criteria:

1. **Given** fuel receipts, expenses and service records in a period, **when** the cost report is requested, **then** each vehicle's cost is the sum of the three, and the totals match the source records.
2. **Given** a period with no records, **when** the report is requested, **then** zero costs are returned without error.

SP: 3 · Priority: Must · Depends on: US-29, US-15 · Owner: Deniz Alp Oniki · Target: Final  
API: `GET /reports/cost`  
Trace: G6, Demo step 7

#### US-35 · Carbon footprint report with ride-sharing savings

**As a** fleet manager, **I want to** see each vehicle's CO₂ emissions and the emissions saved by ride sharing, **so that** the institution can follow its sustainability goals.

Acceptance criteria:

1. **Given** fuel used by each vehicle in a period, **when** the carbon report is requested, **then** emissions are calculated from litres and fuel type with a documented factor.
2. **Given** rides with passengers, **when** the report is requested, **then** the saving from trips not taken by passengers is shown.

SP: 3 · Priority: Must · Depends on: US-29, US-24 · Owner: Deniz Alp Oniki · Target: Final  
API: `GET /reports/carbon`  
Trace: G5, G6, Demo step 7

#### US-36 · Utilisation report

**As a** fleet manager, **I want to** see the utilisation rate of each vehicle, **so that** I can decide whether the fleet size is right.

Acceptance criteria:

1. **Given** a vehicle reserved 20 of 40 working hours, **when** the utilisation report is requested, **then** 50% utilisation is returned.
2. **Given** an invalid period, **when** the report is requested, **then** the request is rejected with 400 `VALIDATION_ERROR`.

SP: 3 · Priority: Must · Depends on: US-20 · Owner: Deniz Alp Oniki · Target: Final  
API: `GET /reports/utilization`  
Trace: Glossary: Utilisation, G6, Demo step 7

#### US-37 · Export reports as CSV

**As a** fleet manager, **I want to** download a report as CSV, **so that** I can share it with institution management.

Acceptance criteria:

1. **Given** a cost, carbon or utilisation report, **when** CSV export is requested, **then** a CSV file with the same values as the screen is returned.

SP: 2 · Priority: Could · Depends on: US-34 · Owner: Deniz Alp Oniki · Target: Final  
API: `(to be added to openapi.yaml)`  
Trace: §7.1 Reporting (CSV export)

### E9 · User Interface

*Screens that connect every module end to end for the three roles.* Module: `frontend` · Owner: Mustafa Düşünceli · 8 stories · 32 SP

| ID | Story | SP | Priority | Depends on | Owner | Target |
|---|---|---|---|---|---|---|
| US-38 | Login screen and role-based navigation | 3 | Must | US-01 | Mustafa Düşünceli | Sprint 3 |
| US-39 | Vehicle status cards | 3 | Must | US-08, US-11 | Mustafa Düşünceli | Sprint 3 |
| US-40 | Trip request and recommendation screen | 5 | Must | US-19, US-20 | Mustafa Düşünceli | Sprint 3 |
| US-41 | Ride match and join screen | 3 | Must | US-23, US-24 | Mustafa Düşünceli | Sprint 3 |
| US-42 | Pickup and return checklist screens | 5 | Must | US-26, US-27 | Mustafa Düşünceli | Sprint 3 |
| US-43 | Maintenance alerts and calendar screen | 5 | Must | US-14, US-15 | Mustafa Düşünceli | Sprint 3 |
| US-44 | Fuel receipt form and history screen | 3 | Should | US-29, US-31 | Mustafa Düşünceli | Final |
| US-45 | Reports dashboard | 5 | Should | US-33, US-34, US-35, US-36 | Mustafa Düşünceli | Final |

#### US-38 · Login screen and role-based navigation

**As a** user of any role, **I want to** log in and see only the menus for my role, **so that** the application is simple to use.

Acceptance criteria:

1. **Given** a `STAFF` user, **when** they log in, **then** they see request, reservations, handover and fuel menus but not reports.
2. **Given** an expired or missing token, **when** a protected page is opened, **then** the user is sent to the login screen.

SP: 3 · Priority: Must · Depends on: US-01 · Owner: Mustafa Düşünceli · Target: Sprint 3  
API: `POST /auth/login`, `GET /me`  
Trace: §5.1 Actors

#### US-39 · Vehicle status cards

**As a** fleet manager, **I want to** see every vehicle as a card with status, odometer and next service, **so that** I see the fleet state at a glance.

Acceptance criteria:

1. **Given** vehicles in different statuses, **when** the vehicle page is opened, **then** each card shows plate, status, odometer and remaining km to next service.
2. **Given** a `DUE_SOON` or `DUE` vehicle, **when** the page is opened, **then** its card is visually highlighted.

SP: 3 · Priority: Must · Depends on: US-08, US-11 · Owner: Mustafa Düşünceli · Target: Sprint 3  
API: `GET /vehicles`  
Trace: §7.1 User interface

#### US-40 · Trip request and recommendation screen

**As a** staff member, **I want to** enter my trip and choose from recommended vehicles, **so that** I can complete a request in under 2 minutes.

Acceptance criteria:

1. **Given** a trip request, **when** it is submitted, **then** recommended vehicles and blocked vehicles with their reasons are shown.
2. **Given** a recommended vehicle, **when** the user reserves it, **then** a confirmation is shown.
3. **Given** a usability test with a new user, **when** they make a valid request, **then** it takes under 2 minutes.

SP: 5 · Priority: Must · Depends on: US-19, US-20 · Owner: Mustafa Düşünceli · Target: Sprint 3  
API: `GET /vehicles/recommendations`, `POST /reservations`  
Trace: G4, Demo steps 1–2

#### US-41 · Ride match and join screen

**As a** staff member, **I want to** see matching rides and join one, **so that** I can share a vehicle easily.

Acceptance criteria:

1. **Given** matching rides, **when** the user opens ride sharing for their trip, **then** rides are listed with driver, departure time and free seats.
2. **Given** a full ride, **when** the user tries to join it, **then** a clear error message is shown.

SP: 3 · Priority: Must · Depends on: US-23, US-24 · Owner: Mustafa Düşünceli · Target: Sprint 3  
API: `GET /rides/matches`, `POST /reservations/{reservationId}/passengers`  
Trace: Demo step 3

#### US-42 · Pickup and return checklist screens

**As a** driver, **I want to** fill in the checklists on screen, **so that** handover is quick and paperless.

Acceptance criteria:

1. **Given** a `CONFIRMED` reservation, **when** the driver opens pickup, **then** the checklist template items are shown and required items are marked.
2. **Given** a return that makes a service due, **when** the driver submits the return, **then** the "10,000 km service is due" message is shown.

SP: 5 · Priority: Must · Depends on: US-26, US-27 · Owner: Mustafa Düşünceli · Target: Sprint 3  
API: `GET /checklist-templates`, `POST .../pickup`, `POST .../return`  
Trace: Demo steps 4–5

#### US-43 · Maintenance alerts and calendar screen

**As a** maintenance officer, **I want to** see open alerts and the maintenance calendar, and record a service, **so that** I can manage maintenance from one screen.

Acceptance criteria:

1. **Given** a new alert, **when** the maintenance officer opens the application, **then** an alert indicator and the alert list are shown.
2. **Given** an open alert, **when** the officer records the service, **then** the alert disappears and the vehicle card shows `AVAILABLE`.

SP: 5 · Priority: Must · Depends on: US-14, US-15 · Owner: Mustafa Düşünceli · Target: Sprint 3  
API: `GET /maintenance/alerts`, `GET /maintenance/calendar`, `POST /maintenance/records`  
Trace: Demo steps 5–6

#### US-44 · Fuel receipt form and history screen

**As a** driver, **I want to** enter fuel receipts on a form and see a vehicle's fuel history, **so that** recording fuel is easy.

Acceptance criteria:

1. **Given** the fuel form, **when** invalid values are entered, **then** field errors are shown before sending.
2. **Given** a flagged receipt, **when** the manager opens fuel history, **then** the anomaly is marked.

SP: 3 · Priority: Should · Depends on: US-29, US-31 · Owner: Mustafa Düşünceli · Target: Final  
API: `POST /fuel-receipts`, `GET /vehicles/{vehicleId}/fuel-receipts`  
Trace: §7.1 Fuel and expenses

#### US-45 · Reports dashboard

**As a** fleet manager, **I want to** see cost, carbon and utilisation on one page for a selected period, **so that** I can make fleet decisions.

Acceptance criteria:

1. **Given** a selected period, **when** the dashboard is opened, **then** summary, cost, carbon and utilisation are shown for that period.
2. **Given** a `STAFF` user, **when** they open the dashboard URL, **then** access is denied.

SP: 5 · Priority: Should · Depends on: US-33, US-34, US-35, US-36 · Owner: Mustafa Düşünceli · Target: Final  
API: `GET /reports/*`  
Trace: Demo step 7

### E10 · Platform, Quality and Delivery

*Docker, seed data, CI pipeline, test coverage, end-to-end tests and static analysis.* Module: `platform` · Owner: Deniz Alp Oniki · 7 stories · 27 SP

| ID | Story | SP | Priority | Depends on | Owner | Target |
|---|---|---|---|---|---|---|
| US-46 | Start the whole product with one command | 5 | Must | — | Deniz Alp Oniki | Sprint 3 |
| US-47 | Seed data for the demo | 3 | Must | US-46 | Deniz Alp Oniki | Sprint 3 |
| US-48 | CI pipeline on every pull request | 3 | Must | US-46 | Deniz Alp Oniki | Sprint 3 |
| US-49 | Unit test coverage of at least 50% | 3 | Must | US-48 | Abdullah Tecimen | Sprint 3 |
| US-50 | Automated end-to-end test of the jury demo | 5 | Must | US-40, US-41, US-42, US-43, US-47 | Abdullah Tecimen | Final |
| US-51 | Integration tests for the API | 5 | Must | US-48 | Abdullah Tecimen | Final |
| US-52 | SonarQube static analysis | 3 | Should | US-48 | Deniz Alp Oniki | Final |

#### US-46 · Start the whole product with one command

**As a** team member, **I want to** start frontend, backend and database with `docker compose up`, **so that** anyone, including the jury, can run the product.

Acceptance criteria:

1. **Given** a clean machine with Docker, **when** `docker compose up` is run, **then** frontend, backend and PostgreSQL start and the login page opens.

SP: 5 · Priority: Must · Depends on: — · Owner: Deniz Alp Oniki · Target: Sprint 3  
API: —  
Trace: §10 Deployment

#### US-47 · Seed data for the demo

**As a** team member, **I want to** start with realistic, invented demo data, **so that** the jury demo can run without manual setup.

Acceptance criteria:

1. **Given** a fresh database, **when** the product starts, **then** users of all three roles, verified licences, destinations and vehicles are loaded.
2. **Given** the seed data, **when** the demo is run, **then** one vehicle is close to its oil change (blocked for the demo trip) and another is suitable.
3. **Given** the seed data, **when** it is reviewed, **then** it contains no real personal data (KVKK).

SP: 3 · Priority: Must · Depends on: US-46 · Owner: Deniz Alp Oniki · Target: Sprint 3  
API: —  
Trace: §10 Deployment, §10 Legal / ethical

#### US-48 · CI pipeline on every pull request

**As a** team member, **I want to** tests and the build to run automatically on every PR to `develop`, **so that** broken code is not merged.

Acceptance criteria:

1. **Given** a pull request to `develop`, **when** it is opened or updated, **then** GitHub Actions builds the project and runs all tests.
2. **Given** a failing test, **when** the PR is checked, **then** the PR cannot be merged.

SP: 3 · Priority: Must · Depends on: US-46 · Owner: Deniz Alp Oniki · Target: Sprint 3  
API: —  
Trace: §10 Process, §10 Quality

#### US-49 · Unit test coverage of at least 50%

**As a** team member, **I want to** unit test coverage to be measured and reported in CI, **so that** we meet the course quality target.

Acceptance criteria:

1. **Given** the CI pipeline, **when** it runs, **then** a pytest-cov coverage report is published.
2. **Given** total backend coverage below 50%, **when** the pipeline runs, **then** the coverage check fails.

SP: 3 · Priority: Must · Depends on: US-48 · Owner: Abdullah Tecimen · Target: Sprint 3  
API: —  
Trace: §10 Quality

#### US-50 · Automated end-to-end test of the jury demo

**As a** team member, **I want to** the full demo journey to be tested automatically, **so that** we know before the demo that it works.

Acceptance criteria:

1. **Given** the seeded product, **when** the Playwright E2E test runs, **then** it completes demo steps 1–7 of system_vision.md §11 without errors.
2. **Given** a change that breaks any demo step, **when** the E2E test runs, **then** the test fails and names the failing step.

SP: 5 · Priority: Must · Depends on: US-40, US-41, US-42, US-43, US-47 · Owner: Abdullah Tecimen · Target: Final  
API: —  
Trace: §11 Release 1, §10 Quality

#### US-51 · Integration tests for the API

**As a** team member, **I want to** API endpoints to be tested against a real PostgreSQL database, **so that** modules work together, not only alone.

Acceptance criteria:

1. **Given** the test database in Docker, **when** integration tests run, **then** reservation conflict, maintenance on return and fuel receipt flows are verified through the API.

SP: 5 · Priority: Must · Depends on: US-48 · Owner: Abdullah Tecimen · Target: Final  
API: —  
Trace: §10 Quality

#### US-52 · SonarQube static analysis

**As a** team member, **I want to** code quality to be analysed by SonarQube, **so that** we find bugs and code smells early.

Acceptance criteria:

1. **Given** the CI pipeline, **when** it runs on `develop`, **then** a SonarQube report is produced.
2. **Given** the final release, **when** the report is reviewed, **then** there are no open critical issues.

SP: 3 · Priority: Should · Depends on: US-48 · Owner: Deniz Alp Oniki · Target: Final  
API: —  
Trace: §10 Quality

## 6. Won't have in release 1

These items are recorded so that the scope is clear. They follow `system_vision.md` §7.3 and §7.4.

| Item | Reason |
|---|---|
| Single sign-on (LDAP / SAML / OAuth) | Needs institutional access; release 1 has its own accounts |
| Live GPS tracking and map-based routing | Paid external API; destinations are predefined |
| Mobile application | The responsive web interface covers the demo |
| Approval workflow for reservations | Valid reservations are confirmed immediately; rules block unsafe requests |
| OCR reading of fuel receipts | Receipts are entered manually |
| Email notifications | In-app alerts are used in release 1 |
| Payments, fines, fuel cards, insurance, payroll, vehicle purchasing | Explicitly outside the system boundary |

## 7. Workload per team member

| Team member | Stories | SP |
|---|---|---|
| Ahmet Can Vurmaz | US-01, US-02, US-03, US-04, US-05, US-06 | 17 |
| Mehmet Umut Oğuzcan | US-26, US-27, US-28 | 13 |
| Ali Eren Kurt | US-07, US-08, US-09, US-10, US-11, US-12, US-13, US-14, US-15, US-16, US-17 | 34 |
| Abdullah Tecimen | US-29, US-30, US-31, US-32, US-49, US-50, US-51 | 26 |
| Deniz Alp Oniki | US-33, US-34, US-35, US-36, US-37, US-46, US-47, US-48, US-52 | 27 |
| Ahmet Tarık Orhan | US-18, US-19, US-20, US-21, US-22, US-23, US-24, US-25 | 28 |
| Mustafa Düşünceli | US-38, US-39, US-40, US-41, US-42, US-43, US-44, US-45 | 32 |

SP measures relative effort, not hours. Role duties that are not stories (sprint planning, architecture documents, reviews, test planning) are tracked as separate GitHub Issues.

## 8. Open questions for the Product Owner

- **Notifications (demo step 5):** `openapi.yaml` has no notification endpoint. This backlog assumes the maintenance officer is notified through the open-alert list and an indicator in the UI (US-13, US-43). Confirm, or add an endpoint.
- **CSV export (US-37):** `system_vision.md` §7.1 lists CSV export, but `openapi.yaml` has no export endpoint yet.
- **Carbon factors (US-35):** which CO₂ factor per litre is used for petrol, diesel and LPG, and from which source?
- **Working hours (US-36):** what counts as available working hours for utilisation (for example weekdays 08:00–18:00)?
- **Fuel anomaly baseline (US-31):** how many earlier full-tank intervals are needed before a vehicle's average is trusted?
