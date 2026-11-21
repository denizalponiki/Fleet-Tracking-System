"""JWT bearer authentication and role checks (ADR-005).

`issue_token` is used by the identity module at login. Routes declare who may call them with
`Depends(require_role(Role.FLEET_MANAGER, ...))` or just `Depends(current_user)`.
"""

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Annotated
from uuid import UUID

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.shared.config import get_settings
from app.shared.problems import DomainError


class Role(StrEnum):
    STAFF = "STAFF"
    FLEET_MANAGER = "FLEET_MANAGER"
    MAINTENANCE_OFFICER = "MAINTENANCE_OFFICER"


@dataclass(frozen=True)
class CurrentUser:
    id: UUID
    role: Role


_hasher = PasswordHasher()  # Argon2id with library defaults


def hash_password(raw: str) -> str:
    return _hasher.hash(raw)


def verify_password(raw: str, password_hash: str) -> bool:
    try:
        return _hasher.verify(password_hash, raw)
    except VerificationError:
        return False


def issue_token(user_id: UUID, role: Role, now: datetime | None = None) -> str:
    settings = get_settings()
    issued = now or datetime.now(UTC)
    claims = {
        "sub": str(user_id),
        "role": role.value,
        "iss": settings.jwt_issuer,
        "iat": issued,
        "exp": issued + timedelta(seconds=settings.jwt_expires_seconds),
    }
    return jwt.encode(claims, settings.jwt_secret.get_secret_value(), algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> CurrentUser:
    settings = get_settings()
    try:
        claims = jwt.decode(
            token,
            settings.jwt_secret.get_secret_value(),
            algorithms=[settings.jwt_algorithm],
            issuer=settings.jwt_issuer,
            options={"require": ["sub", "role", "exp", "iss"]},
        )
        return CurrentUser(id=UUID(claims["sub"]), role=Role(claims["role"]))
    except (jwt.PyJWTError, ValueError) as exc:
        raise DomainError(401, "UNAUTHORIZED", "No valid access token was sent.") from exc


_bearer = HTTPBearer(auto_error=False)


def current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> CurrentUser:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise DomainError(401, "UNAUTHORIZED", "No valid access token was sent.")
    return decode_token(credentials.credentials)


def require_role(*roles: Role):
    """Dependency factory: the signed-in user must have one of `roles`, otherwise 403."""

    def _check(user: Annotated[CurrentUser, Depends(current_user)]) -> CurrentUser:
        if user.role not in roles:
            allowed = " or ".join(r.value for r in roles)
            raise DomainError(403, "FORBIDDEN", f"This operation requires the {allowed} role.")
        return user

    return _check
