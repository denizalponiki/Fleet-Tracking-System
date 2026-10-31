# FleetSync · Problem Definition and Project Proposal

| | |
|---|---|
| Course | SENG 321 Software Engineering · Sprint 1, deliverable 1 |
| Author (Product Owner) | Ahmet Can Vurmaz |
| Date | 2026-10-25 |
| Related documents | `system_vision.md` (System boundary) |

## 1. Introduction and Background

Many institutions and campuses operate a shared vehicle fleet to support their staff's official travel needs. However, the management of these fleets is often decentralized and handled through informal channels such as phone calls, emails, and manual spreadsheets. This unstructured approach creates a lack of visibility, leading to significant administrative overhead, safety risks, and unnecessary expenses. 

## 2. Problem Statement

The current manual approach to fleet management presents four critical issues:

1. **Scheduling Conflicts and Inefficiency:** Vehicles are requested informally without a unified calendar. As a result, the same vehicle can easily be promised to two different people, leading to double bookings and last-minute confusion. 
2. **Safety and Maintenance Risks:** Maintenance schedules (oil changes, tire replacements, routine inspections) are tracked manually, relying on human memory or outdated logs. Consequently, vehicles that are due for service often continue to be assigned for trips, posing significant safety risks to drivers.
3. **Redundant Trips:** Because staff members cannot see who else is travelling, it is common for multiple individuals to drive separate vehicles to the exact same destination on the same day. This wastes fuel and limits vehicle availability for others.
4. **Lack of Financial and Environmental Visibility:** Crucial data such as trip mileage, fuel receipts, and vehicle damage are recorded on loose paper or ignored entirely. This makes it impossible to accurately track overall fleet costs, detect anomalies in fuel consumption, or calculate the institution's carbon footprint.

## 3. Proposed Solution: FleetSync

**FleetSync** is a centralized, web-based fleet management platform designed to automate and optimize the reservation, maintenance, and monitoring of shared vehicles. It replaces spreadsheets and disjointed communication with a unified system that enforces business rules and ensures safety.

By acting as the single source of truth for the fleet, FleetSync applies consistent reservation, driver licence, and maintenance rules to every request, while maintaining a complete history of vehicle usage and condition.

## 4. Key Capabilities

* **Smart Reservations & Ride Sharing:** Users can view vehicle availability, make reservations, and see existing trips to their destination. This encourages carpooling, reducing the number of vehicles on the road.
* **Predictive Maintenance & Safety Blocks:** The system tracks mileage and dates automatically. It proactively blocks unsafe vehicles (those close to needing maintenance) from being reserved and generates alerts for the maintenance staff.
* **Digital Handovers:** Drivers complete digital pickup and return checklists, ensuring accurate logging of odometer readings, fuel levels, and any new damage.
* **Reporting & Analytics:** Fleet managers gain access to detailed reports on vehicle utilization, financial costs, fuel anomalies, and carbon emissions.

## 5. Target Users and Stakeholders

* **Staff Members / Drivers:** Need a reliable, fast way to book vehicles and share rides for official duties.
* **Fleet Managers:** Need to ensure fleet availability, enforce safety rules, verify driving licences, and monitor budgets and emissions.
* **Maintenance Officers:** Need accurate, timely alerts for vehicle servicing to prevent breakdowns.
* **Institution Management (Sponsor):** Interested in fair usage, cost savings, and sustainability metrics.

## 6. Success Criteria for Initial Release

The implementation of FleetSync will be considered successful if it achieves the following measurable targets:

* **Zero Safety Breaches:** No trip starts with a vehicle whose remaining service distance is dangerously low.
* **Zero Double Bookings:** The system prevents any overlapping confirmed reservations for the same vehicle.
* **Data-Driven Maintenance:** 100% of maintenance alerts are triggered automatically by system data (odometer readings and dates) rather than manual memory.
* **Fast Usability:** A staff member can complete a valid vehicle request in under 2 minutes.
* **Increased Efficiency:** Measurable reduction in vehicles used for identical trips via the ride-sharing feature.
* **Complete Visibility:** Reports on cost, carbon emissions, and fleet utilization are readily available.