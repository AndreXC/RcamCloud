from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas.FileHashRequestModel import FileHashRequest
from  .CheckHash.checkHash import HashChecker
from Postgres.GetSessionPostgres.GetSessionPostgres import get_db_session
router = APIRouter()

@router.post("/verificar-hash")
async def verificar_hash(
    info: FileHashRequest,
    db: AsyncSession = Depends(get_db_session)
):
    checker = HashChecker(db)
    return await checker.check(info)
