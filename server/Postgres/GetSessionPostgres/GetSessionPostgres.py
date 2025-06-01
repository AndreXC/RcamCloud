# dependencies.py ou router.py

from sqlalchemy.ext.asyncio import AsyncSession
from CreateSessionPostgres.session_manager import DatabaseSessionManager
from typing import AsyncGenerator
from fastapi.responses import JSONResponse
from fastapi import status

db_manager = DatabaseSessionManager()

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        async for session in db_manager.get_session():
            yield session
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": False,
                "match": None,
                "error": "Hash SHA256 inválido.",
                "message": "O campo 'sha256' deve ser uma string hexadecimal de 64 caracteres."
            }
        )
