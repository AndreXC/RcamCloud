from pydantic import BaseModel

class DirectoryRequest(BaseModel):
    path: str
