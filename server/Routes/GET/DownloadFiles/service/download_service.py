import os
from fastapi.responses import FileResponse
from fastapi import HTTPException, status

UPLOAD_DIR = "storage"

class DownloadService:
    async def download(self, filepath: str) -> FileResponse:
        file_path = os.path.join(UPLOAD_DIR, filepath)

        if not os.path.isfile(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Arquivo não encontrado"
            )

        return FileResponse(
            path=file_path,
            filename=os.path.basename(file_path),
            media_type="application/octet-stream",
            status_code=status.HTTP_200_OK
        )
