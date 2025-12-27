from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.exceptions import DomainException

# Imports dos nossos handlers
from src.interface.api.exception_handlers import (
    domain_exception_handler,
    general_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from src.interface.api.middlewares.logging import logging_middleware
from src.interface.api.v1.endpoints import auth, consoles, games

app = FastAPI(title="Gamer API", description="API para gerenciamento de jogos - Desafio Backend", version="1.0.0")

app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)

app.add_exception_handler(DomainException, domain_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(consoles.router, prefix="/api/v1/consoles", tags=["Consoles"])
app.include_router(games.router, prefix="/api/v1/games", tags=["Games"])


@app.get("/health", tags=["Health Check"])
async def health_check():
    """
    Verifica se a API está no ar.
    """
    return {"status": "ok", "message": "Service is running"}
