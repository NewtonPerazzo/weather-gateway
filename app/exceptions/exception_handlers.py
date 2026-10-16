import logging

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


logger = logging.getLogger(__name__)


def error_response(status_code: int, error: str, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": error, "message": message},
    )


def error_for_status(status_code: int) -> str:
    return {
        400: "invalid_request",
        401: "unauthorized",
        403: "forbidden",
        404: "resource_not_found",
        409: "resource_conflict",
        422: "invalid_request",
        429: "service_busy",
    }.get(status_code, "request_failed")


def get_downstream_error(response: httpx.Response) -> str:
    try:
        payload = response.json()
    except ValueError:
        return error_for_status(response.status_code)

    error = payload.get("error") if isinstance(payload, dict) else None
    return error if isinstance(error, str) else error_for_status(response.status_code)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def request_validation_handler(
        request: Request,
        exception: RequestValidationError,
    ) -> JSONResponse:
        return error_response(
            status_code=422,
            error="invalid_request",
            message="Please review the information and try again.",
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exception: HTTPException,
    ) -> JSONResponse:
        error = (
            "invalid_access_token"
            if exception.status_code == 401
            else error_for_status(exception.status_code)
        )
        return error_response(
            status_code=exception.status_code,
            error=error,
            message="We could not complete this request right now.",
        )

    @app.exception_handler(httpx.HTTPStatusError)
    async def upstream_http_error_handler(
        request: Request,
        exception: httpx.HTTPStatusError,
    ) -> JSONResponse:
        response = exception.response
        return error_response(
            status_code=response.status_code,
            error=get_downstream_error(response),
            message="We could not complete this request right now.",
        )

    @app.exception_handler(httpx.RequestError)
    async def upstream_request_error_handler(
        request: Request,
        exception: httpx.RequestError,
    ) -> JSONResponse:
        logger.exception("Gateway could not reach an upstream service")
        return error_response(
            status_code=503,
            error="service_unavailable",
            message="The requested service is temporarily unavailable.",
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exception: Exception,
    ) -> JSONResponse:
        logger.exception("Unhandled gateway error")
        return error_response(
            status_code=500,
            error="internal_error",
            message="We could not complete this request right now.",
        )
