from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.core.exceptions import DomainException

async def domain_exception_handler(request: Request, exc: DomainException):
    """
    Trata erros de regra de negócio (ex: Jogo não encontrado, Email duplicado).
    Retorna 400 Bad Request por padrão para erros de domínio.
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "success": False,
            "error": {
                "code": "DOMAIN_ERROR",
                "message": str(exc)
            }
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Trata erros automáticos do Pydantic (ex: campo faltando, tipo errado).
    Formata o erro 422 para o padrão do projeto.
    """
    # Pega apenas a primeira mensagem de erro para simplificar
    error_msg = exc.errors()[0].get("msg") if exc.errors() else "Validation error"
    field = exc.errors()[0].get("loc")[-1] if exc.errors() else "field"
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": f"{field}: {error_msg}"
            }
        }
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Trata erros HTTP manuais (raise HTTPException).
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "HTTP_ERROR",
                "message": str(exc.detail)
            }
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """
    Fallback para qualquer erro não tratado (Bug no código).
    Retorna 500 e esconde o traceback do usuário final.
    """
    print(f"CRITICAL ERROR: {exc}") # Aqui entraria o Logger estruturado
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred. Please contact support."
            }
        }
    )