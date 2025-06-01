import os
from fastapi.responses import JSONResponse
from fastapi import status

UPLOAD_DIR = "storage"  # Diretório onde os arquivos serão armazenados

class DirectoryService:
    def create(self, path: str) -> JSONResponse:
        dir_path = os.path.join(UPLOAD_DIR, path)
        try:
            if os.path.exists(dir_path):
                return JSONResponse(
                    status_code=status.HTTP_201_CREATED,
                    content={
                        "status": True,
                        "error": "",
                        "directory": path,
                        "message": f"Diretório já existe: {path}"
                    }
                )
            os.makedirs(dir_path)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "status": True,
                    "error": "",
                    "directory": path,
                    "message": f"Diretório criado com sucesso: {path}"
                }
            )
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "status": False,
                    "error": str(e),
                    "directory": path,
                    "message": f"Erro ao criar diretório: {str(e)}"
                }
            )
