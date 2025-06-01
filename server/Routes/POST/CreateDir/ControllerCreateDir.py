from fastapi import APIRouter
from .schemas.directory_schema import DirectoryRequest
from .services.directory_service import DirectoryService

router = APIRouter()

@router.post("/mkdir")
def create_directory(data: DirectoryRequest):
    service = DirectoryService()
    return service.create(data.path)
