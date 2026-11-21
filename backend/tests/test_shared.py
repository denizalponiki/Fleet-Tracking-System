from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Annotated
from uuid import uuid4

import pytest
from fastapi import Depends
from pydantic import BaseModel, Field

from app.shared.events import DomainEvent, EventBus
from app.shared.problems import DomainError
from app.shared.security import (
    CurrentUser,
    Role,
    hash_password,
    issue_token,
    require_role,
    verify_password,
)

# ------------------------------------------------------------------ problems (ADR-003)


@pytest.fixture
def probe_client(app, client):
    class Body(BaseModel):
        estimatedKm: int = Field(ge=1, le=5000)

    @app.post("/probe/validate")
    def validate(body: Body):
        return body

    @app.get("/probe/conflict")
    def conflict():
        raise DomainError(409, "RESERVATION_CONFLICT", "The vehicle is already reserved.",
                          suggestedVehicleIds=["0b6f1c2a-0000-4000-8000-000000000102"])

    @app.get("/probe/manager")
    def manager_only(user: Annotated[CurrentUser, Depends(require_role(Role.FLEET_MANAGER))]):
        return {"id": str(user.id), "role": user.role}

    return client


def test_domain_error_is_problem_json(probe_client):
    response = probe_client.get("/probe/conflict")
    assert response.status_code == 409
    assert response.headers["content-type"] == "application/problem+json"
    body = response.json()
    assert body["code"] == "RESERVATION_CONFLICT"
    assert body["type"] == "https://fleetsync.local/problems/reservation-conflict"
    assert body["status"] == 409
    assert body["instance"] == "/probe/conflict"
    assert body["suggestedVehicleIds"] == ["0b6f1c2a-0000-4000-8000-000000000102"]


def test_request_validation_becomes_400_with_field_errors(probe_client):
    response = probe_client.post("/probe/validate", json={"estimatedKm": 0})
    assert response.status_code == 400
    body = response.json()
    assert body["code"] == "VALIDATION_ERROR"
    assert body["errors"][0]["field"] == "estimatedKm"


def test_unknown_route_is_not_found_problem(client):
    response = client.get("/api/v1/does-not-exist")
    assert response.status_code == 404
    assert response.json()["code"] == "NOT_FOUND"


# ------------------------------------------------------------------ security (ADR-005)


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_missing_token_is_401(probe_client):
    response = probe_client.get("/probe/manager")
    assert response.status_code == 401
    assert response.json()["code"] == "UNAUTHORIZED"


def test_wrong_role_is_403(probe_client):
    response = probe_client.get("/probe/manager", headers=_auth(issue_token(uuid4(), Role.STAFF)))
    assert response.status_code == 403
    assert response.json()["code"] == "FORBIDDEN"


def test_right_role_passes(probe_client):
    user_id = uuid4()
    response = probe_client.get("/probe/manager", headers=_auth(issue_token(user_id, Role.FLEET_MANAGER)))
    assert response.status_code == 200
    assert response.json() == {"id": str(user_id), "role": "FLEET_MANAGER"}


def test_expired_token_is_401(probe_client):
    old = datetime.now(UTC) - timedelta(hours=2)
    response = probe_client.get("/probe/manager", headers=_auth(issue_token(uuid4(), Role.FLEET_MANAGER, now=old)))
    assert response.status_code == 401


def test_tampered_token_is_401(probe_client):
    token = issue_token(uuid4(), Role.STAFF)
    response = probe_client.get("/probe/manager", headers=_auth(token[:-2] + "xx"))
    assert response.status_code == 401


def test_password_hash_roundtrip():
    stored = hash_password("demo1234")
    assert stored.startswith("$argon2id$")
    assert verify_password("demo1234", stored)
    assert not verify_password("wrong-password", stored)


# ------------------------------------------------------------------ events (ADR-002)


@dataclass(frozen=True)
class TripCompleted(DomainEvent):
    vehicle_id: str
    odometer_km: int


def test_event_bus_calls_handlers_in_order_and_returns_results():
    bus = EventBus()
    bus.subscribe(TripCompleted, lambda e: f"alert for {e.odometer_km}")
    bus.subscribe(TripCompleted, lambda e: "second")
    assert bus.publish(TripCompleted("v1", 60020)) == ["alert for 60020", "second"]


def test_event_bus_handler_error_propagates():
    bus = EventBus()

    def boom(_):
        raise DomainError(422, "ODOMETER_DECREASED", "lower")

    bus.subscribe(TripCompleted, boom)
    with pytest.raises(DomainError):
        bus.publish(TripCompleted("v1", 1))


# ------------------------------------------------------------------ app


@pytest.mark.parametrize(("ready", "status", "body"), [
    (True, 200, {"status": "ok", "database": True}),
    (False, 503, {"status": "unavailable", "database": False}),
])
def test_health_reflects_database_readiness(monkeypatch, ready, status, body):
    from fastapi.testclient import TestClient

    import app.main as main

    monkeypatch.setattr(main, "database_is_ready", lambda: ready)
    response = TestClient(main.create_app()).get("/api/v1/health")
    assert response.status_code == status
    assert response.json() == body


def test_every_module_has_a_router():
    from app.main import MODULE_ROUTERS

    tags = sorted(tag for router in MODULE_ROUTERS for tag in router.tags)
    assert tags == sorted([
        "auth", "drivers", "vehicles", "maintenance", "reservations", "locations",
        "carpool", "handover", "fuel", "reports",
    ])  # the ten tags in docs/openapi.yaml
