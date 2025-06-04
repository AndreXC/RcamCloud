from typing import Dict
from pydantic import BaseModel

class SnapshotModel(BaseModel):
    snapshot: Dict[str, str]
