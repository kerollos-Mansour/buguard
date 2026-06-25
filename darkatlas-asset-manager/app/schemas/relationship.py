from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID

class RelationshipBase(BaseModel):
    source_asset_id: UUID
    target_asset_id: UUID
    relationship_type: str = Field(..., min_length=1, max_length=50)

class RelationshipCreate(RelationshipBase):
    pass

class RelationshipResponse(RelationshipBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
