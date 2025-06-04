from fastapi import APIRouter
from .schemas.sync_shcemas import SnapshotModel
from .services.sync_service import SyncService

router = APIRouter()    
@router.post("/SyncFiles")
async def sync_files(request: SnapshotModel):
    service = SyncService()
    return service.CheckSync(request)
    
    
