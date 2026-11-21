"""RFC 9457 problem responses with a machine-readable `code` (ADR-003).

Domain code raises `DomainError`; this module turns it, and FastAPI's own validation and
HTTP errors, into `application/problem+json` bodies that match the `Problem` schema in
`docs/openapi.yaml`.
"""

import re
from http import HTTPStatus
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

PROBLEM_MEDIA_TYPE = "application/problem+json"
PROBLEM_BASE_URI = "https://fleetsync.local/problems/"


class DomainError(Exception):
    """A business-rule or state error. `code` must be a value of `ErrorCode` in openapi.yaml."""

    def __init__(self, status: int, code: str, detail: str, **extensions: Any) -> None:
        super().__init__(detail)
        self.status = status
        self.code = code
        self.detail = detail
        self.extensions = extensions


def problem_type(code: str) -> str:
    return PROBLEM_BASE_URI + code.lower().replace("_", "-")


def problem_body(status: int, code: str, detail: str | None = None, **extensions: Any) -> dict[str, Any]:
    body: dict[str, Any] = {
        "type": problem_type(code),
        "title": _title(code),
        "status": status,
        "code": code,
    }
    if detail:
        body["detail"] = detail
    body.update({k: v for k, v in extensions.items() if v is not None})
    return body


def _title(code: str) -> str:
    return re.sub(r"_", " ", code).capitalize()


def _response(status: int, body: dict[str, Any], request: Request) -> JSONResponse:
    body.setdefault("instance", request.url.path)
    return JSONResponse(body, status_code=status, media_type=PROBLEM_MEDIA_TYPE)


_STATUS_CODES = {
    401: "UNAUTHORIZED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
}


def register_problem_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def _domain(request: Request, exc: DomainError) -> JSONResponse:
        return _response(exc.status, problem_body(exc.status, exc.code, exc.detail, **exc.extensions), request)

    @app.exception_handler(RequestValidationError)
    async def _validation(request: Request, exc: RequestValidationError) -> JSONResponse:
        errors = [
            {"field": ".".join(str(p) for p in err["loc"] if p not in ("body", "query", "path")), "message": err["msg"]}
            for err in exc.errors()
        ]
        detail = f"{len(errors)} field{'s are' if len(errors) != 1 else ' is'} invalid."
        return _response(400, problem_body(400, "VALIDATION_ERROR", detail, errors=errors), request)

    @app.exception_handler(StarletteHTTPException)
    async def _http(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        code = _STATUS_CODES.get(exc.status_code, "VALIDATION_ERROR")  # only ErrorCode values are allowed
        detail = exc.detail if isinstance(exc.detail, str) else HTTPStatus(exc.status_code).phrase
        response = _response(exc.status_code, problem_body(exc.status_code, code, detail), request)
        if exc.headers:
            response.headers.update(exc.headers)
        return response
