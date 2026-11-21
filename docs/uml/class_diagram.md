# FleetSync · UML Class Diagram (Domain Model)

| | |
|---|---|
| Responsible / Accountable | Ali Eren Kurt, Lead Software Architect & Technical Lead |
| Version | 1.0 · Sprint 2 · 2026-11-21 |
| Sources | [`openapi.yaml`](../openapi.yaml) `components/schemas`, [`system_vision.md`](../system_vision.md) §8, [`../c4/README.md`](../c4/README.md) §3 |
| Issue | #237 |

The diagram shows the domain classes of each backend module, their key attributes and the operations that carry business rules. API-only shapes (pages, request bodies, report rows) are left out; they are the Pydantic schemas generated from `openapi.yaml`. The tables behind these classes are in [`er_diagram.md`](er_diagram.md).

## 1. Domain model

```mermaid
classDiagram
    direction LR

    %% ---------------- identity
    class User {
        +UUID id
        +String email
        +String fullName
        +Role role
        +String department
        -String passwordHash
        +verifyPassword(raw) bool
    }
    class DriverProfile {
        +UUID userId
        +String phone
        +String employeeNo
        +canDrive(on: date) bool
    }
    class License {
        +UUID id
        +LicenseClass licenseClass
        +String licenseNumber
        +Date issuedAt
        +Date expiresAt
        +bool verified
        +UUID verifiedBy
        +allows(required: LicenseClass) bool
        +isValidUntil(date) bool
    }
    class Role {
        <<enumeration>>
        STAFF
        FLEET_MANAGER
        MAINTENANCE_OFFICER
    }
    class LicenseClass {
        <<enumeration>>
        B
        BE
        C1
        C
        D1
        D
    }

    %% ---------------- vehicle
    class Vehicle {
        +UUID id
        +Plate plate
        +String brandModel
        +VehicleType type
        +int seatCount
        +FuelType fuelType
        +decimal tankCapacityLiters
        +LicenseClass requiredLicenseClass
        +int odometerKm
        +int modelYear
        +VehicleStatus status
        +changeStatus(to, reason) void
        +updateOdometer(km) void
    }
    class VehicleStatus {
        <<enumeration>>
        AVAILABLE
        IN_USE
        IN_MAINTENANCE
        OUT_OF_SERVICE
    }

    %% ---------------- maintenance
    class MaintenanceRule {
        +UUID id
        +String code
        +String name
        +int intervalKm
        +int intervalMonths
        +int warnKm
        +int warnDays
        +bool active
    }
    class MaintenancePlan {
        +UUID vehicleId
        +UUID ruleId
        +int lastServiceKm
        +Date lastServiceDate
        +nextDueKm() int
        +nextDueDate() Date
        +evaluate(odometerKm, today) RuleEvaluation
    }
    class RuleEvaluation {
        <<value object>>
        +String ruleCode
        +int remainingKm
        +int remainingDays
        +EvaluationStatus status
    }
    class MaintenanceAlert {
        +UUID id
        +AlertLevel level
        +AlertStatus status
        +String message
        +int odometerKmAtAlert
        +DateTime createdAt
        +DateTime resolvedAt
        +resolve(record) void
    }
    class MaintenanceRecord {
        +UUID id
        +int odometerKm
        +Date performedAt
        +decimal cost
        +String workshop
        +String notes
    }
    class MaintenanceRuleEngine {
        <<service>>
        +evaluateVehicle(vehicle) VehicleMaintenanceStatus
        +isBlockedForTrip(vehicle, estimatedKm, endAt) List~Reason~
        +onTripCompleted(event) List~MaintenanceAlert~
        +recordService(record) void
    }
    class EvaluationStatus {
        <<enumeration>>
        OK
        DUE_SOON
        DUE
    }

    %% ---------------- reservation and carpool
    class Location {
        +UUID id
        +String name
        +String city
        +int distanceKmFromBase
    }
    class Reservation {
        +UUID id
        +String purpose
        +DateTime startAt
        +DateTime endAt
        +int estimatedKm
        +int seatsNeeded
        +bool allowRideSharing
        +ReservationStatus status
        +String cancelReason
        +DateTime createdAt
        +seatsAvailable() int
        +overlaps(start, end) bool
        +cancel(by, reason) void
        +activate() void
        +complete() void
    }
    class Passenger {
        +UUID userId
        +DateTime joinedAt
    }
    class ReservationStatus {
        <<enumeration>>
        CONFIRMED
        ACTIVE
        COMPLETED
        CANCELLED
    }
    class RecommendationService {
        <<service>>
        +recommend(query) RecommendationResult
        -score(vehicle, query) float
    }
    class RideMatcher {
        <<service>>
        +findMatches(destination, departAt, seats, tolerance) List~RideMatch~
        +join(reservation, user) Passenger
        +leave(reservation, user) void
    }

    %% ---------------- handover
    class HandoverRecord {
        +UUID id
        +HandoverType type
        +int odometerKm
        +int fuelLevelPercent
        +String notes
        +DateTime recordedAt
    }
    class ChecklistItemResult {
        +String code
        +bool ok
        +String note
    }
    class ChecklistTemplate {
        +HandoverType type
        +List items
        +missingRequired(results) List~String~
    }
    class DamageReport {
        +UUID id
        +DamageArea area
        +DamageSeverity severity
        +String description
        +URI photoUrl
        +DateTime reportedAt
    }

    %% ---------------- fuel
    class FuelReceipt {
        +UUID id
        +decimal liters
        +decimal totalPrice
        +int odometerKm
        +bool fullTank
        +String station
        +DateTime filledAt
        +unitPrice() decimal
    }
    class FuelAnomaly {
        +FuelAnomalyType type
        +decimal measuredLPer100Km
        +decimal baselineLPer100Km
        +decimal deviationPercent
        +DateTime detectedAt
    }
    class Expense {
        +UUID id
        +ExpenseCategory category
        +decimal amount
        +DateTime spentAt
        +String description
    }

    %% ---------------- relationships
    User "1" -- "0..1" DriverProfile
    DriverProfile "1" *-- "0..*" License
    User ..> Role
    License ..> LicenseClass
    Vehicle ..> VehicleStatus
    Vehicle ..> LicenseClass : requires

    Vehicle "1" *-- "0..*" MaintenancePlan
    MaintenanceRule "1" -- "0..*" MaintenancePlan
    MaintenancePlan ..> RuleEvaluation : creates
    RuleEvaluation ..> EvaluationStatus
    Vehicle "1" -- "0..*" MaintenanceAlert
    MaintenanceRule "1" -- "0..*" MaintenanceAlert
    Vehicle "1" -- "0..*" MaintenanceRecord
    MaintenanceRecord "0..1" -- "0..*" MaintenanceAlert : resolves
    MaintenanceRecord "0..*" -- "1..*" MaintenanceRule : covers
    MaintenanceRuleEngine ..> MaintenancePlan
    MaintenanceRuleEngine ..> MaintenanceAlert

    User "1" -- "0..*" Reservation : requests
    Vehicle "1" -- "0..*" Reservation
    Location "1" -- "0..*" Reservation : destination
    Reservation "1" *-- "0..*" Passenger
    Passenger "0..*" -- "1" User
    Reservation ..> ReservationStatus
    RecommendationService ..> Vehicle
    RecommendationService ..> MaintenanceRuleEngine : trip block check
    RideMatcher ..> Reservation

    Reservation "1" *-- "0..2" HandoverRecord : pickup, return
    HandoverRecord "1" *-- "1..*" ChecklistItemResult
    ChecklistTemplate ..> ChecklistItemResult : validates
    HandoverRecord "0..1" -- "0..*" DamageReport
    Vehicle "1" -- "0..*" DamageReport

    Vehicle "1" -- "0..*" FuelReceipt
    Reservation "0..1" -- "0..*" FuelReceipt
    FuelReceipt "1" -- "0..1" FuelAnomaly
    Vehicle "1" -- "0..*" Expense
    Reservation "0..1" -- "0..*" Expense
```

## 2. Notes on the model

| Class | Rule it owns | Source |
|---|---|---|
| `License` | `allows()` uses the licence class hierarchy; `isValidUntil()` must hold for the trip end date. Only `verified` licences count. | `system_vision.md` §8 Driver eligibility |
| `Vehicle` | `updateOdometer()` rejects lower values (`ODOMETER_DECREASED`). `changeStatus()` allows only the manual transitions in [`state_diagrams.md`](state_diagrams.md) (`INVALID_STATUS_TRANSITION`). | `openapi.yaml` `changeVehicleStatus` |
| `MaintenancePlan` | Holds the last service km and date of one rule on one vehicle. `nextDueKm = lastServiceKm + intervalKm`, `nextDueDate = lastServiceDate + intervalMonths`. `evaluate()` returns `DUE` at the interval and `DUE_SOON` inside `warnKm` / `warnDays`. | `system_vision.md` §8, §12 |
| `MaintenanceRuleEngine` | `isBlockedForTrip()` blocks when `remainingKm < estimatedKm + 100` or `nextDueDate < endAt`. `onTripCompleted()` opens alerts and moves the vehicle to `IN_MAINTENANCE` when any rule is `DUE`. | `system_vision.md` §8 Trip blocking, Automatic maintenance status |
| `Reservation` | `overlaps()` uses half-open periods `[startAt, endAt)`, so back-to-back trips are allowed. `seatsAvailable() = vehicle.seatCount − seatsNeeded − passengers`. Only `CONFIRMED` can be cancelled. | `carpool_reservation_api.md` |
| `RideMatcher` | Same destination, departure within tolerance (default 30 min), `allowRideSharing`, at least one free seat. | `system_vision.md` §8 Ride sharing |
| `FuelReceipt` / `FuelAnomaly` | Litres above tank capacity rejected (`FUEL_EXCEEDS_TANK`); consumption > 25% above baseline flagged. | `system_vision.md` §8 Fuel anomaly |

`Plate`, `VehicleType`, `FuelType`, `HandoverType`, `DamageArea`, `DamageSeverity`, `AlertLevel`, `AlertStatus`, `FuelAnomalyType` and `ExpenseCategory` are enumerations or value types with the values listed in `openapi.yaml`; they are not drawn to keep the diagram readable.
