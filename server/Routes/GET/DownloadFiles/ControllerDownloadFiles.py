from fastapi import APIRouter, Depends
from service.download_service import DownloadService

router = APIRouter()
@router.get("/download/{filepath:path}")
async def download(filepath: str):
    return await DownloadService().download(filepath)
