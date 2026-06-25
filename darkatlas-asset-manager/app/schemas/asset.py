from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any, List
from app.schemas.tag import TagResponse

class AssetBase(BaseModel):
    type: str = Field(..., min_length=1, max_length=50)
    value: str = Field(..., min_length=1)
    status: str = Field("ACTIVE", min_length=1, max_length=20)
    source: Optional[str] = None
    asset_metadata: Optional[Dict[str, Any]] = None

class AssetCreate(AssetBase):
    pass

class AssetUpdate(BaseModel):
    type: Optional[str] = Field(None, min_length=1, max_length=50)
    value: Optional[str] = Field(None, min_length=1)
    status: Optional[str] = Field(None, min_length=1, max_length=20)
    source: Optional[str] = None
    asset_metadata: Optional[Dict[str, Any]] = None

class AssetResponse(AssetBase):
    id: UUID
    first_seen: datetime
    last_seen: datetime
    tags: List[TagResponse] = []
    
    model_config = ConfigDict(from_attributes=True)
