import os
import hashlib
from fastapi import UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from Model.HashModel.Hashmodel import FileHash
from sqlalchemy import insert

UPLOAD_DIR = "storage"  # ajuste conforme necessário

class UploadService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def process_file(self, file: UploadFile) -> JSONResponse:
        try:
            rel_path = file.filename.replace("\\", "/").lstrip("/")
            file_path = os.path.join(UPLOAD_DIR, rel_path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            contents = await file.read()
            if not contents:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "status": False,
                        "error": "Arquivo vazio.",
                        "message": "Não foi possível ler o arquivo enviado."
                    }
                )

            sha256 = hashlib.sha256(contents).hexdigest()

            with open(file_path, "wb") as f:
                f.write(contents)

            # Salvar no banco de dados
            stmt = insert(FileHash).values(filename=rel_path, hash=sha256)
            await self.db.execute(stmt)
            await self.db.commit()

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "status": True,
                    "hash": sha256,
                    "path": rel_path,
                    "message": "Arquivo enviado com sucesso."
                }
            )
        except Exception as e:
            await self.db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "status": False,
                    "error": str(e),
                    "message": "Erro ao fazer upload do arquivo."
                }
            )
