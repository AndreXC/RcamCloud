from fastapi import APIRouter, File, UploadFile, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from .services.upload_service import UploadService
from Postgres.GetSessionPostgres.GetSessionPostgres import get_db_session

router = APIRouter()

@router.post("/upload")
async def upload_file(
    File: UploadFile = File(...),
    File_Hash: str = Form(None),
    db: AsyncSession = Depends(get_db_session)
):
    service = UploadService(db)
    return await service.process_file(File, File_Hash)
