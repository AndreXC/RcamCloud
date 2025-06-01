from fastapi import APIRouter
from .service.list_files_service import ListFilesService

router = APIRouter()

@router.get("/listar-arquivos")
async def list_all_files():
    return await ListFilesService().list_files()
