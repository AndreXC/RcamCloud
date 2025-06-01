

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from Postgres.GetSessionPostgres.GetSessionPostgres import get_db_session
from services.delete_service import DeleteService


router = APIRouter()
@router.delete("/delete/{filepath:path}")
async def delete(filepath: str, db: AsyncSession = Depends(get_db_session)):
    return await DeleteService().delete(filepath, db)

