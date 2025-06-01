# dependencies.py ou router.py

from sqlalchemy.ext.asyncio import AsyncSession
from ..CreateSessionPostgres.session_manager import DatabaseSessionManager
from typing import AsyncGenerator
from fastapi import HTTPException, status

db_manager = DatabaseSessionManager()

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        async for session in db_manager.get_session():
            yield session
    except Exception as e:
        # Não pode retornar, deve lançar exceção para FastAPI tratar e enviar resposta
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter sessão do banco: {str(e)}"
        )

