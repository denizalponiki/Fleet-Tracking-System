# FleetSync · UML Sequence Diagrams

| | |
|---|---|
| Responsible / Accountable | Ali Eren Kurt, Lead Software Architect & Technical Lead |
| Consulted | Ahmet Tarık Orhan (reservation, carpool), Mehmet Umut Oğuzcan (handover) |
| Version | 1.0 · Sprint 2 · 2026-11-21 |
| Sources | [`openapi.yaml`](../openapi.yaml), [`carpool_reservation_api.md`](../carpool_reservation_api.md), [`system_vision.md`](../system_vision.md) §8 and §11, [`../c4/README.md`](../c4/README.md) §3 |
| Issue | #237 |

The diagrams follow the jury demo flow (`system_vision.md` §11). Participants are the containers and backend modules from the C4 Level 3 diagram. Every call from the SPA carries `Authorization: Bearer <JWT>`; the security check is drawn once in SD-1 and omitted afterwards.

| # | Scenario | Demo step | User stories |
|---|---|---|---|
| SD-1 | Log in | – | US-01 |
| SD-2 | Get recommendations (a vehicle is blocked) | 1–2 | US-19 |
| SD-3 | Create a reservation (conflict prevention) | 2 | US-20 |
| SD-4 | Find and join a shared ride | 3 | US-23, US-24 |
| SD-5 | Pick up the vehicle | 4 | handover |
| SD-6 | Return the vehicle and run the maintenance rule engine | 5 | US-13, handover |
| SD-7 | Record a service and release the vehicle | 6 | US-15 |

## SD-1 · Log in

```mermaid
sequenceDiagram
    autonumber
    actor U as Staff member
    participant SPA as Web application
    participant API as Backend API (router)
    participant ID as identity
    participant DB as PostgreSQL

    U->>SPA: Enter email and password
    SPA->>API: POST /auth/login {email, password}
    API->>ID: login(email, password)
    ID->>DB: SELECT user BY email
    DB-->>ID: user row (passwordHash, role)
    alt password matches
        ID->>ID: issue JWT (sub=userId, role, exp=3600 s)
        ID-->>API: TokenResponse
        API-->>SPA: 200 {accessToken, expiresIn, user}
        SPA->>SPA: keep token in memory
    else unknown email or wrong password
        ID-->>API: InvalidCredentials
        API-->>SPA: 401 problem+json code=INVALID_CREDENTIALS
    end

    Note over SPA,API: Every later request: Authorization Bearer token.<br/>The security dependency verifies signature and expiry,<br/>then checks the role required by the operation (401 / 403).
```

## SD-2 · Get recommendations

The staff member asks for a 9-seat vehicle to Konya. One minibus has only 550 km left before its oil service, so it is blocked with a reason (demo step 2).

```mermaid
sequenceDiagram
    autonumber
    actor U as Staff member
    participant SPA as Web application
    participant RES as reservation
    participant ID as identity
    participant VEH as vehicle
    participant MNT as maintenance
    participant DB as PostgreSQL

    U->>SPA: Destination, period, seats, purpose
    SPA->>SPA: propose estimatedKm from the destination distance (user may edit)
    SPA->>RES: GET /vehicles/recommendations?startAt&endAt&seats&estimatedKm&destinationId
    RES->>VEH: listVehicles(status=AVAILABLE)
    VEH-->>RES: candidate vehicles
    RES->>ID: eligibility(driver, requiredLicenseClass, until=endAt)
    ID-->>RES: eligible or LICENSE_EXPIRED / LICENSE_CLASS_MISMATCH
    loop each candidate vehicle
        RES->>RES: seatCount >= seats? else INSUFFICIENT_SEATS
        RES->>DB: overlapping CONFIRMED/ACTIVE reservation?
        DB-->>RES: none or conflict (CALENDAR_CONFLICT)
        RES->>MNT: isBlockedForTrip(vehicle, estimatedKm, endAt)
        MNT->>DB: maintenance plans of vehicle
        MNT->>MNT: remainingKm < estimatedKm + 100<br/>or nextDueDate < endAt ?
        MNT-->>RES: [] or [MAINTENANCE_DUE / MAINTENANCE_DUE_SOON]
        alt no blocking reason
            RES->>RES: score(vehicle) and add to recommended
        else at least one reason
            RES->>RES: add to blocked with reasons
        end
    end
    RES-->>SPA: 200 {recommended (score desc), blocked}
    SPA-->>U: Vehicle cards, blocked ones greyed out with the reason
```

## SD-3 · Create a reservation

The server repeats every check, because the client may be stale. The no-overlap rule is enforced by the database constraint as well (see [`er_diagram.md`](er_diagram.md)), so two concurrent requests cannot both succeed.

```mermaid
sequenceDiagram
    autonumber
    actor U as Staff member
    participant SPA as Web application
    participant RES as reservation
    participant ID as identity
    participant MNT as maintenance
    participant DB as PostgreSQL

    U->>SPA: Choose recommended vehicle, confirm
    SPA->>RES: POST /reservations {vehicleId, destinationId, startAt, endAt, estimatedKm, seatsNeeded}
    RES->>RES: validate (endAt > startAt, <= 14 days, ranges)
    alt invalid fields
        RES-->>SPA: 400 VALIDATION_ERROR {errors[]}
    end
    RES->>ID: eligibility(driver, vehicle, endAt)
    alt not eligible
        RES-->>SPA: 422 LICENSE_EXPIRED / LICENSE_CLASS_MISMATCH
    end
    RES->>MNT: isBlockedForTrip(vehicle, estimatedKm, endAt)
    alt blocked by maintenance
        RES-->>SPA: 409 VEHICLE_MAINTENANCE_DUE {suggestedVehicleIds}
    end
    RES->>DB: BEGIN, SELECT vehicle FOR UPDATE
    alt vehicle IN_MAINTENANCE or OUT_OF_SERVICE
        RES-->>SPA: 409 VEHICLE_UNAVAILABLE
    end
    RES->>DB: INSERT reservation (status=CONFIRMED)
    alt exclusion constraint violated (overlap)
        DB-->>RES: 23P01 exclusion_violation
        RES->>DB: ROLLBACK
        RES-->>SPA: 409 RESERVATION_CONFLICT {suggestedVehicleIds}
    else inserted
        RES->>DB: COMMIT
        RES-->>SPA: 201 Reservation (CONFIRMED, seatsAvailable)
        SPA-->>U: Reservation confirmed
    end
```

## SD-4 · Find and join a shared ride

```mermaid
sequenceDiagram
    autonumber
    actor C as Colleague (staff)
    participant SPA as Web application
    participant CP as carpool
    participant RES as reservation
    participant DB as PostgreSQL

    C->>SPA: Same destination and departure time
    SPA->>CP: GET /rides/matches?destinationId&departAt&seats
    CP->>RES: CONFIRMED reservations to destination
    RES->>DB: query by destination and day
    DB-->>RES: reservations
    RES-->>CP: reservations with seatsAvailable
    CP->>CP: keep allowRideSharing,<br/>|startAt - departAt| <= 30 min,<br/>seatsAvailable >= seats
    CP-->>SPA: 200 [RideMatch]
    C->>SPA: Join ride
    SPA->>CP: POST /reservations/{id}/passengers
    CP->>DB: BEGIN, SELECT reservation FOR UPDATE
    alt already a passenger
        CP-->>SPA: 409 ALREADY_JOINED
    else no free seat
        CP-->>SPA: 422 SEAT_CAPACITY_EXCEEDED
    else reservation not CONFIRMED
        CP-->>SPA: 409 INVALID_RESERVATION_STATE
    else seat free
        CP->>DB: INSERT passenger, COMMIT
        CP-->>SPA: 201 Reservation (seatsAvailable - 1)
        SPA-->>C: Joined the ride
    end
```

## SD-5 · Pick up the vehicle

```mermaid
sequenceDiagram
    autonumber
    actor D as Driver (staff)
    participant SPA as Web application
    participant HO as handover
    participant RES as reservation
    participant VEH as vehicle
    participant DB as PostgreSQL

    D->>SPA: Open reservation, fill pickup checklist
    SPA->>HO: GET /checklist-templates?type=PICKUP
    HO-->>SPA: template items
    D->>SPA: Odometer, fuel level, item results
    SPA->>HO: POST /reservations/{id}/pickup
    HO->>RES: get(reservation) — owner and status CONFIRMED?
    alt not CONFIRMED
        HO-->>SPA: 409 INVALID_RESERVATION_STATE
    end
    HO->>HO: required items present? else 422 CHECKLIST_INCOMPLETE
    HO->>VEH: odometer >= vehicle.odometerKm? else 422 ODOMETER_DECREASED
    HO->>DB: BEGIN
    HO->>DB: INSERT handover_record (PICKUP) and items
    HO->>RES: activate(reservation) — CONFIRMED to ACTIVE
    HO->>VEH: changeStatus(IN_USE), updateOdometer(km)
    HO->>DB: COMMIT
    HO-->>SPA: 201 HandoverRecord
```

## SD-6 · Return the vehicle and run the maintenance rule engine

This is the core of demo step 5. The return and the maintenance evaluation run in the same transaction (`openapi.yaml` `recordReturn`). The event payload and the rule for the final vehicle status are defined in [`domain_events.md`](../domain_events.md).

```mermaid
sequenceDiagram
    autonumber
    actor D as Driver (staff)
    participant SPA as Web application
    participant HO as handover
    participant RES as reservation
    participant VEH as vehicle
    participant BUS as event bus
    participant MNT as maintenance
    participant DB as PostgreSQL
    actor O as Maintenance officer

    D->>SPA: Return checklist, odometer 60,020 km, fuel 35%
    SPA->>HO: POST /reservations/{id}/return
    HO->>RES: get(reservation) — status ACTIVE?
    HO->>HO: returnKm >= pickupKm? else 422 ODOMETER_DECREASED
    HO->>DB: BEGIN
    HO->>DB: INSERT handover_record (RETURN), items, damages
    HO->>HO: tripKm = 570, kmLimitExceeded = tripKm > estimatedKm x 1.3
    HO->>VEH: updateOdometer(60,020)
    HO->>RES: complete(reservation) — ACTIVE to COMPLETED
    HO->>BUS: publish TripCompletedEvent(vehicleId, odometerKm, tripKm, ...)
    BUS->>MNT: onTripCompleted(event)
    MNT->>DB: maintenance plans and active rules
    loop each active rule
        MNT->>MNT: evaluate: remainingKm, remainingDays
    end
    alt any rule DUE (oil change at 60,000 km)
        MNT->>DB: INSERT maintenance_alert (DUE, OPEN)
    else only DUE_SOON or OK
        MNT->>DB: INSERT alert for DUE_SOON (if not already open)
    end
    MNT-->>BUS: TripEvaluationResult {anyRuleDue, alerts}
    BUS-->>HO: [TripEvaluationResult]
    alt SEVERE damage reported
        HO->>VEH: changeStatus(OUT_OF_SERVICE)
    else anyRuleDue
        HO->>VEH: changeStatus(IN_MAINTENANCE)
    else
        HO->>VEH: changeStatus(AVAILABLE)
    end
    HO->>DB: COMMIT
    HO-->>SPA: 201 ReturnResult {tripKm, kmLimitExceeded, vehicleStatus=IN_MAINTENANCE, maintenanceAlerts}
    SPA-->>D: "10,000 km service is due. Vehicle moved to maintenance."

    O->>SPA: Open dashboard
    SPA->>MNT: GET /maintenance/alerts?status=OPEN
    MNT-->>SPA: 200 [alert OIL_CHANGE DUE]
    SPA-->>O: Alert badge and list (in-app notification, finding F1)
```

## SD-7 · Record a service and release the vehicle

```mermaid
sequenceDiagram
    autonumber
    actor O as Maintenance officer
    participant SPA as Web application
    participant MNT as maintenance
    participant VEH as vehicle
    participant DB as PostgreSQL

    O->>SPA: Record service (rules OIL_CHANGE, odometer, date, cost, workshop)
    SPA->>MNT: POST /maintenance/records
    MNT->>VEH: odometer >= vehicle.odometerKm? else 422 ODOMETER_DECREASED
    MNT->>DB: BEGIN
    MNT->>DB: INSERT maintenance_record and record_rules
    MNT->>DB: UPDATE maintenance_plan SET lastServiceKm, lastServiceDate
    MNT->>DB: UPDATE alerts SET RESOLVED for these rules
    MNT->>MNT: re-evaluate all rules of the vehicle
    alt no rule DUE any more
        MNT->>VEH: changeStatus(AVAILABLE)
    else another rule still DUE
        MNT->>MNT: vehicle stays IN_MAINTENANCE
    end
    MNT->>DB: COMMIT
    MNT-->>SPA: 201 MaintenanceRecord {resolvedAlertIds, vehicleStatus}
    SPA-->>O: Vehicle is AVAILABLE again
```
