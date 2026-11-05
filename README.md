# FleetSync - Smart Fleet Management, Periodic Maintenance & Carpooling Platform

SENG 321 Software Engineering Term Project

## Team Roles & RACI Assignments
- **Product Owner & Requirements Engineer:** Ahmet Can Vurmaz
- **Scrum Master & Agile Process Coach:** Mehmet Umut Oğuzcan
- **Lead Software Architect & Technical Lead:** Ali Eren Kurt
- **DevOps & CI/CD Infrastructure Engineer:** Deniz Alp Oniki
- **Quality Assurance & Test Automation Engineer:** Abdullah Tecimen
- **Implementation & Integration Engineer (Backend & API):** Ahmet Tarık Orhan
- **Implementation & Integration Engineer (Frontend & UI):** Mustafa Düşünceli

## Project Structure
- `docs/`: System documentation, SRS, and OpenAPI specifications
- `src/`: Application source code


## Local PostgreSQL setup

With Docker running, open PowerShell in the repository root and run:

```powershell
Copy-Item .env.example .env
docker compose config --quiet
docker compose up -d db
docker compose exec db pg_isready -U fleet -d fleet
```

If the database is still starting, wait a few seconds and repeat the last command. When it prints `accepting connections`, PostgreSQL is ready.

To stop the database, run `docker compose down`. The named volume keeps the data between runs.

This Sprint 1 setup starts PostgreSQL. Frontend and backend integration is tracked in #103.
