# db/session_manager.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)

class DatabaseSessionManager:
    def __init__(self):
        try:
            load_dotenv()

            user = os.getenv("POSTGRES_USER")
            password = os.getenv("POSTGRES_PASSWORD")
            host = os.getenv("POSTGRES_HOST")
            port = os.getenv("POSTGRES_PORT", "5432")
            db_name = os.getenv("POSTGRES_DB_NAME")

            if not all([user, password, host, db_name]):
                missing = [var for var in ["POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_HOST", "POSTGRES_DB_NAME"] if not os.getenv(var)]
                raise ValueError(f"Variáveis de ambiente ausentes: {', '.join(missing)}")

            self._database_url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"
            self._engine = create_async_engine(self._database_url, echo=False)
            self._sessionmaker = sessionmaker(bind=self._engine, class_=AsyncSession, expire_on_commit=False)

        except Exception as e:
            logger.error(f"Erro ao configurar conexão com o banco de dados: {e}")
            self._engine = None
            self._sessionmaker = None
            self._error = e

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        if not self._sessionmaker:
            raise RuntimeError(f"Erro ao conectar ao banco de dados: {self._error}")
        
        try:
            async with self._sessionmaker() as session:
                yield session
        except Exception as e:
            logger.error(f"Erro ao criar sessão com o banco de dados: {e}")
            raise RuntimeError(f"Erro ao criar sessão com o banco de dados: {e}")
