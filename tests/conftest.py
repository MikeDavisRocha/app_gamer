import sys
import asyncio
import pytest

# Fix para Windows + Python 3.13 + asyncpg
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

@pytest.fixture(scope="session")
def event_loop_policy():
    """Define a policy do event loop para toda a sessão de testes."""
    if sys.platform == 'win32':
        return asyncio.WindowsSelectorEventLoopPolicy()
    return asyncio.DefaultEventLoopPolicy()

@pytest.fixture(scope="function")
async def async_db_session():
    """
    Cria uma sessão de banco de dados isolada para cada teste.
    """
    # CORREÇÃO AQUI: Importar do config.py e usar a função get_db
    from src.infra.database.config import get_db
    
    # get_db é um generator assíncrono, então iteramos sobre ele
    async for session in get_db():
        yield session
        # Rollback garante que o teste não suje o banco para o próximo
        await session.rollback()
        # Não precisamos fechar manualmente pois o context manager do get_db já faz isso,
        # mas o rollback é essencial.