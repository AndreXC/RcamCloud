
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import Dict
from pydantic import BaseModel
from fastapi.responses import FileResponse
from pathlib import Path
from urllib.parse import unquote
from app import DirectorySnapshot, DirectoryComparator
import shutil

app = FastAPI()
SERVER_DIR = Path("storage_server")

class SnapshotModel(BaseModel):
    snapshot: Dict[str, str]  # { caminho_relativo: hash }

@app.post("/sync")
async def sync_files(request: SnapshotModel):
    local_snapshot = request.snapshot
    server_snapshot = DirectorySnapshot("storage_server").get_snapshot()

    comparator = DirectoryComparator(local_snapshot, server_snapshot)
    diffs = comparator.compare()

    return JSONResponse(content=diffs)



@app.get("/download")
def download_file(file: str):
    requested_path = SERVER_DIR / unquote(file)
    if requested_path.exists() and requested_path.is_file():
        return FileResponse(path=requested_path, filename=requested_path.name)
    return {"error": "File not found"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...), rel_path: str = Form(...)):
    destino = SERVER_DIR / rel_path
    destino.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(destino, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return JSONResponse(content={"status": "ok", "file": rel_path})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})