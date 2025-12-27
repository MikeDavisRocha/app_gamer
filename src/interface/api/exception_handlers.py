from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.core.exceptions import DomainException


async def domain_exception_handler(request: Request, exc: DomainException):
    logger.warning(f"Domain Error: {exc} | Path: {request.url.path}")  # <--- Log estruturado
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"success": False, "error": {"code": "DOMAIN_ERROR", "message": str(exc)}},
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_msg = exc.errors()[0].get("msg") if exc.errors() else "Validation error"
    logger.info(f"Validation Error: {error_msg} | Path: {request.url.path}")  # <--- Log informativo

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"success": False, "error": {"code": "VALIDATION_ERROR", "message": error_msg}},
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(f"HTTP Error {exc.status_code}: {exc.detail} | Path: {request.url.path}")

    # Mapeia status codes para códigos de erro mais específicos
    error_code_map = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        409: "CONFLICT",
        422: "UNPROCESSABLE_ENTITY",
        429: "TOO_MANY_REQUESTS",
        500: "INTERNAL_ERROR",
        502: "BAD_GATEWAY",
        503: "SERVICE_UNAVAILABLE",
    }
    
    error_code = error_code_map.get(exc.status_code, "HTTP_ERROR")

    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": {"code": error_code, "message": str(exc.detail)}},
    )


async def general_exception_handler(request: Request, exc: Exception):
    # Aqui é CRÍTICO. Usamos logger.exception para gravar o Traceback completo (stack trace)
    logger.exception(f"CRITICAL UNHANDLED ERROR: {exc} | Path: {request.url.path}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {"code": "INTERNAL_ERROR", "message": "An unexpected error occurred. Please contact support."},
        },
    )
