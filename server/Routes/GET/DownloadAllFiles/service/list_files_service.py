import os
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

UPLOAD_DIR = "storage"  # Diretório onde os arquivos serão armazenados

class ListFilesService:
    async def list_files(self):
        try:
            if not os.path.exists(UPLOAD_DIR):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Diretório de upload não encontrado."
                )

            file_list = []
            for root, _, files in os.walk(UPLOAD_DIR):
                for file in files:
                    rel_dir = os.path.relpath(root, UPLOAD_DIR)
                    rel_file = os.path.normpath(os.path.join(rel_dir, file))
                    file_list.append(rel_file.replace("\\", "/"))

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "status": True,
                    "total": len(file_list),
                    "files": file_list,
                    "message": "retorno lista de arquivos."
                }
            )

        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "status": False,
                    "error": str(e),
                    "files": [],
                    "message": "Erro ao listar os arquivos."
                }
            )
