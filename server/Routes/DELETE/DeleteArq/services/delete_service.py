from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from .processamento.delete_handler import DeleteHandler

class DeleteService:
    def __init__(self):
        self.handler = DeleteHandler()

    async def delete(self, path: str, db: AsyncSession) -> JSONResponse:
        result = await self.handler.delete(path, db)

        if result["success"]:
            return JSONResponse(
                status_code=result["status_code"],
                content={
                    "status": True,
                    "path": result.get("path"),
                    "message": result.get("message")
                }
            )
        else:
            return JSONResponse(
                status_code=result["status_code"],
                content={
                    "status": False,
                    "error": result.get("error"),
                    "message": result.get("message")
                }
            )
