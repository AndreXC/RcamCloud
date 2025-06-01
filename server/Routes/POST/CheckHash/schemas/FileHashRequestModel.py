from pydantic import BaseModel
class FileHashRequest(BaseModel):
    filename: str  # agora é caminho relativo (ex: subpasta/arquivo.txt)
    sha256: str