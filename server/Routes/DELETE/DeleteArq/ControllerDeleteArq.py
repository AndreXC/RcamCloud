

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from Postgres.GetSessionPostgres.GetSessionPostgres import get_db_session
from .services.delete_service import DeleteService
from pydantic import BaseModel


class FilePathPayload(BaseModel):
    path: str

router = APIRouter()

@router.delete("/delete")
async def delete(payload: FilePathPayload, db: AsyncSession = Depends(get_db_session)):
    return await DeleteService().delete(payload.path, db)