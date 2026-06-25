from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID

class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class TagCreate(TagBase):
    pass

class TagResponse(TagBase):
    id: UUID
    
    model_config = ConfigDict(from_attributes=True)
