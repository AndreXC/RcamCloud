import os
import shutil
from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from server.Model.HashModel.Hashmodel import FileHash

UPLOAD_DIR = "storage"  # ajuste conforme necessário

class DeleteService:
    async def delete(self, path: str, db: AsyncSession) -> JSONResponse:
        target_path = os.path.join(UPLOAD_DIR, path)

        try:
            # Apaga do disco
            deleted_from_disk = False
            if os.path.isdir(target_path):
                shutil.rmtree(target_path)
                deleted_from_disk = True
            elif os.path.isfile(target_path):
                os.remove(target_path)
                deleted_from_disk = True

            if not deleted_from_disk:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={
                        "status": False,
                        "error": "Arquivo ou diretório não encontrado.",
                        "message": f"Nenhum item encontrado com o caminho '{path}'."
                    }
                )

            # Apaga do banco via ORM
            stmt = select(FileHash).where(FileHash.filename == path)
            result = await db.execute(stmt)
            file_record = result.scalar_one_or_none()

            if file_record:
                await db.delete(file_record)
                await db.commit()


            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "status": True,
                    "path": path,
                    "message": "Item deletado com sucesso do disco e banco de dados."
                }
            )

        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "status": False,
                    "error": str(e),
                    "message": "Erro ao deletar item."
                }
            )
