"""FastAPI application: mounts every module's router under /api/v1 (C4 Level 3)."""

from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse

from app.modules.carpool.router import router as carpool_router
from app.modules.fuel.router import router as fuel_router
from app.modules.handover.router import router as handover_router
from app.modules.identity.router import router as identity_router
from app.modules.maintenance.router import router as maintenance_router
from app.modules.reporting.router import router as reporting_router
from app.modules.reservation.router import router as reservation_router
from app.modules.vehicle.router import router as vehicle_router
from app.shared.config import get_settings
from app.shared.db import database_is_ready
from app.shared.problems import register_problem_handlers

MODULE_ROUTERS: list[APIRouter] = [
    identity_router,
    vehicle_router,
    maintenance_router,
    reservation_router,
    carpool_router,
    handover_router,
    fuel_router,
    reporting_router,
]


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version="0.1.0", docs_url=f"{settings.api_prefix}/docs",
                  openapi_url=f"{settings.api_prefix}/openapi.json")
    register_problem_handlers(app)

    @app.get(f"{settings.api_prefix}/health", tags=["ops"], include_in_schema=False)
    def health() -> JSONResponse:
        """Readiness check for Docker Compose (NFR-OPS-05): 200 when the database answers, else 503."""
        ready = database_is_ready()
        return JSONResponse({"status": "ok" if ready else "unavailable", "database": ready},
                            status_code=200 if ready else 503)

    for router in MODULE_ROUTERS:
        app.include_router(router, prefix=settings.api_prefix)
    return app


app = create_app()
