from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schemas.FileHashRequestModel import FileHashRequest
from server.Model.HashModel.Hashmodel import FileHash


class HashChecker:
    def __init__(self, db_session: AsyncSession):
        """
        db_session: sessão assíncrona do banco de dados PostgreSQL
        """
        self.db_session = db_session

    async def validate_input(self, filename: str, sha256: str):
        if not filename or not isinstance(filename, str):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "status": False,
                    "match": None,
                    "error": "Nome do arquivo inválido.",
                    "message": "O campo 'filename' deve ser uma string não vazia."
                }
            )
        if not sha256 or not isinstance(sha256, str) or len(sha256) != 64:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "status": False,
                    "match": None,
                    "error": "Hash SHA256 inválido.",
                    "message": "O campo 'sha256' deve ser uma string hexadecimal de 64 caracteres."
                }
            )
        return None

    async def check(self, info: FileHashRequest) -> JSONResponse:
        try:
            error_response = await self.validate_input(info.filename, info.sha256)
            if error_response:
                return error_response

            stmt = select(FileHash).where(FileHash.filename == info.filename)
            result = await self.db_session.execute(stmt)
            file_hash = result.scalar_one_or_none()

            if file_hash is None:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={
                        "status": False,
                        "match": None,
                        "error": "Arquivo não encontrado.",
                        "message": f"O arquivo '{info.filename}' não está registrado no servidor."
                    }
                )

            match = file_hash.hash == info.sha256
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "status": True,
                    "match": match,
                    "filename": info.filename,
                    "message": "Hash confere." if match else "Hash não confere."
                }
            )

        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "status": False,
                    "match": None,
                    "error": str(e),
                    "message": "Erro ao verificar hash."
                }
            )
