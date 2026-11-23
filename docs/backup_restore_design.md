# FleetSync · PostgreSQL Backup and Restore Verification Design (DD-4)

| Field | Value |
|---|---|
| Phase | Sprint 2 — design and verification planning only |
| Author | Deniz Alp Oniki · DevOps & CI/CD Infrastructure Engineer |
| Date | 2026-11-23 |
| Status | **Proposed; review pending. Not implemented or tested.** |
| Related | [Issue #304](https://github.com/denizalponiki/Fleet-Tracking-System/issues/304), [NFR-OPS-04](nfr_quality_measures.md#nfr-ops-04--database-backup-and-restoration), [UML deployment DD-4](uml/deployment_diagram.md#3-open-points), [DevOps architecture review](deployment_architecture_review.md) |

## 1. Verified repository baseline and scope

- The current [`docker-compose.yml`](../docker-compose.yml) has exactly one service, `db`, using `postgres:16`, with `POSTGRES_DB`, `POSTGRES_USER` and `POSTGRES_PASSWORD` read from the environment.
- Database files are in the named Compose volume `postgres_data`, mounted at `/var/lib/postgresql/data`. The Compose file does **not** publish PostgreSQL port 5432 to the host.
- [`.env.example`](../.env.example) provides **example** PostgreSQL variables. It must not be treated as real credentials.
- The proposed `api`, `web`, migration and seed services in the [deployment diagram](uml/deployment_diagram.md) are **not in the current Compose file**. This plan is independent of those future services.
- There are no backup/restore scripts or executed restore-test results established by this document. DD-4 remains **execution pending**, to be validated before the final demonstration.

This plan implements the **design and acceptance-evidence definition** of [NFR-OPS-04](nfr_quality_measures.md). It does not mark its operational verification as passed.

## 2. Backup design

| Decision | Proposed approach | Reason |
|---|---|---|
| Backup type | PostgreSQL logical backup using `pg_dump --format=custom` | Supports `pg_restore` into a new database and inspection of the archive |
| Source | Existing Compose service `db`, using its `POSTGRES_DB` and `POSTGRES_USER` | Does not assume an application container or host-published database port |
| Destination | Timestamped `.dump` file in a **host-side, ignored** `backups/` folder outside the DB container and `postgres_data` volume | Survives DB-container removal and ordinary volume reuse; separate/off-host copy is needed for host-failure recovery |
| Data | Only synthetic demo/test records | Do not commit personal data or credentials |
| Credentials | Read configured environment within the DB container; never print credentials or put them in Git | Reduces accidental disclosure |
| Recovery target | A **new, disposable database** (not the original `POSTGRES_DB`) | Avoids overwriting the source when checking the logical restore |

The `backups/` folder must be ignored by Git **before** any archive is produced. A backup placed only on the same host does **not** protect against loss of that host; an independently secured/off-host copy should be specified for any real operational deployment. Do not store passwords in archive filenames, logs or PR attachments.

## 3. Proposed verification exercise (to be executed later)

**Prerequisites:** Docker Engine and Docker Compose available, a running `db` container, non-production synthetic records with known identifiers/counts, valid local `.env` values and sufficient available disk space. The DBA/QA reviewer must agree on the sample records and expected state.

1. **Capture baseline:** record the PostgreSQL version, database name, selected table names, row counts and a few non-sensitive synthetic record identifiers before backup. Save commands, timestamps and expected values in the test evidence.
2. **Generate a logical archive:** run `pg_dump` from inside the existing `db` service in custom format, streaming bytes to a timestamped file on the host **outside** the Compose volume. Do not allocate a pseudo-TTY for binary output (use `docker compose exec -T` if using Compose exec).
3. **Check the archive:** record its file size and checksum; list its archive contents with `pg_restore --list`. An archive listing alone does **not** prove a successful recovery.
4. **Create a fresh restore destination:** create a disposable empty database, e.g. `fleetsync_restore_check`, with a name confirmed not to exist. Never drop or overwrite the application/source database for this test.
5. **Restore into that empty database:** use `pg_restore` against the disposable target with an error-on-failure option, capture exit status and non-sensitive logs. If later migrations or roles require ownership/privileges, agree on an explicit restore policy with the Architect before testing; do not assume that a clean database has the application's final users or extensions.
6. **Verify data integrity:** query the restored database, compare recorded counts and selected synthetic values to the baseline, and document any schema/extension or permissions differences. A successful command exit without data verification is insufficient.
7. **Clean up carefully:** after QA accepts the evidence, remove only the specifically named temporary restore database. Retain the archive only under the team's agreed test-retention rules; never attach real data to a GitHub issue.

**Acceptance:** backup succeeds; archive is readable; restore into a clean, separate database succeeds; recorded table counts and selected synthetic records match; timestamp, archive name, checksum, actual commands/results, tester and reviewer are recorded. Any discrepancy means **not passed**.

**Limit:** restoring into a separate database on the **same** PostgreSQL instance checks logical backup/restore but does not prove disaster recovery after host or volume loss. A separate fresh instance/volume restore exercise should be considered before declaring host-loss recovery supported.

## 4. Data-loss and startup cautions

- `docker compose down` (without `-v`) ordinarily retains the named volume; it is not a replacement for backup.
- `docker compose down -v` removes declared named volumes, including `postgres_data`, and can destroy the local database. **Do not use it during routine recovery or backup verification.**
- Restoring into the current database can overwrite or conflict with live records; the verification target must be isolated.
- Do not assume the future `api`, `web`, seed or migration commands run today. The full-stack deployment and readiness tests are Sprint 3/final tasks under NFR-OPS-01 and OPS-05.

## 5. Evidence record (blank until actually tested)

| Field | Value |
|---|---|
| Execution status | **Not executed** |
| Test date, operator, QA reviewer | Pending |
| PostgreSQL/image and Compose versions | Pending |
| Archive filename, location, checksum | Pending |
| Baseline table counts and synthetic identifiers | Pending |
| `pg_dump` / archive inspection exit and logs | Pending |
| Disposable restore database and `pg_restore` result | Pending |
| Count/value comparison, anomalies | Pending |
| Final test result | **Not assessed** |

**Review requests:** Ali Eren Kurt (architecture and restore assumptions) and Abdullah Tecimen (test evidence and acceptance). Once reviewed, DD-4 may be marked **design specified / restore test pending**, but must **not** be marked as successfully restored until real evidence exists.
