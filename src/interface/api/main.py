from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from src.interface.api.middlewares.logging import logging_middleware

# Imports dos nossos handlers
from src.interface.api.exception_handlers import (
    domain_exception_handler,
    validation_exception_handler,
    http_exception_handler,
    general_exception_handler
)
from src.core.exceptions import DomainException
from src.interface.api.v1.endpoints import auth, consoles, games


app = FastAPI(
    title="Gamer API",
    description="API para gerenciamento de jogos - Desafio Backend",
    version="1.0.0"
)

app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)

app.add_exception_handler(DomainException, domain_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(consoles.router, prefix="/consoles", tags=["Consoles"])
app.include_router(games.router, prefix="/games", tags=["Games"])

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Service is running"}