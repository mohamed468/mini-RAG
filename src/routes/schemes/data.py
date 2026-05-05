from pydantic import BaseModel,Field
from typing import Optional
class ProcessRequest(BaseModel):
    file_id : str | None = None
    chunk_size: int = Field(default=100, ge=1)
    overlap_size: int = Field(default=20, ge=0)
    do_reset: int = Field(default=0, ge=0, le=1)