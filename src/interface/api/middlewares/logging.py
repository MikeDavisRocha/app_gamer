import sys
import time

from fastapi import Request
from loguru import logger

# Configuração básica do Logger para sair no stdout (terminal)
# Em produção, poderíamos configurar para salvar em arquivo ou enviar para um serviço
logger.remove()  # Remove o handler padrão para não duplicar
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
    level="INFO",
)


async def logging_middleware(request: Request, call_next):
    """
    Middleware que loga todas as requisições HTTP com método, caminho e tempo de execução.
    """
    start_time = time.time()

    # Processa a requisição
    response = await call_next(request)

    process_time = time.time() - start_time

    # Define a cor do log baseada no status code
    log_level = "INFO"
    if response.status_code >= 500:
        log_level = "ERROR"
    elif response.status_code >= 400:
        log_level = "WARNING"

    log_message = f"{request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.4f}s"

    # Registra o log
    if log_level == "ERROR":
        logger.error(log_message)
    elif log_level == "WARNING":
        logger.warning(log_message)
    else:
        logger.info(log_message)

    return response
