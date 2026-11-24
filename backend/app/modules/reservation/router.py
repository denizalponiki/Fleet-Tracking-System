"""HTTP routes of the reservation module (OpenAPI tags: reservations, locations).

Add one route per operation in docs/openapi.yaml with the same operationId, and guard it with
Depends(current_user) or Depends(require_role(...)) from app.shared.security.
"""

from fastapi import APIRouter

router = APIRouter(tags=["reservations", "locations"])
