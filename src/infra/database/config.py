from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from src.core.config import settings

# Cria o motor de conexão assíncrono usando a URL do .env
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# Fábrica de sessões (será usada em cada requisição)
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# Classe Base para os modelos do ORM
Base = declarative_base()

# Função de dependência para injetar a sessão nas rotas do FastAPI
async def get_db():
    async with SessionLocal() as session:
        yield session