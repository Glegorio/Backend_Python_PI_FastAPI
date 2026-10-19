from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# Criação do Engine Assíncrono com pool de conexões 
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Sessões Assíncronas
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

# Base declarativa para o mapeamento das entidades/tabelas 
class Base(DeclarativeBase):
    pass

# Injeção de Dependências do FastAPI para obter a sessão do Banco
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Gera uma sessão do banco de dados por requisição HTTP.
    Garante o fechamento automático da conexão ao termino da requisição.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()