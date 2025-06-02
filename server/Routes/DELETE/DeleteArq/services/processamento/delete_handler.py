# services/delete_handler.py

import os
import shutil
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from Model.HashModel.Hashmodel import FileHash
from fastapi import status


UPLOAD_DIR = "storage"


class DeleteHandler:
    def __init__(self, upload_dir: str = UPLOAD_DIR):
        self.upload_dir = upload_dir

    async def delete(self, path: str, db: AsyncSession) -> dict:
        """
        Realiza a exclusão de arquivo/diretório e seu registro no banco.
        Retorna um dicionário com os dados do resultado.
        """
        target_path = os.path.join(self.upload_dir, path)

        # Apaga do disco
        deleted_from_disk = self._delete_from_disk(target_path)

        if not deleted_from_disk:
            return {
                "success": False,
                "status_code": status.HTTP_404_NOT_FOUND,
                "error": "Arquivo ou diretório não encontrado.",
                "message": f"Nenhum item encontrado com o caminho '{path}'."
            }

        # Apaga do banco
        try:
            stmt = select(FileHash).where(FileHash.filename == path)
            result = await db.execute(stmt)
            file_record = result.scalar_one_or_none()

            if file_record:
                await db.delete(file_record)
                await db.commit()

            return {
                "success": True,
                "status_code": status.HTTP_200_OK,
                "path": path,
                "message": "Item deletado com sucesso do disco e banco de dados."
            }

        except Exception as e:
            await db.rollback()
            return {
                "success": False,
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "error": str(e),
                "message": "Erro ao deletar item do banco de dados."
            }

    def _delete_from_disk(self, path: str) -> bool:
        """
        Exclui o arquivo ou diretório do disco.
        Retorna True se a exclusão ocorreu, False caso contrário.
        """
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
                return True
            elif os.path.isfile(path):
                os.remove(path)
                return True
            return False
        except Exception:
            return False
