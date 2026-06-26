from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List, Literal

from app.db.database import get_db
from app.db.repositories.asset_repository import AssetRepository
from app.db.repositories.tag_repository import TagRepository
from app.services.asset_service import AssetService
from app.schemas.asset import AssetCreate, AssetUpdate, AssetResponse
from app.schemas.common import PaginatedResponse
from app.core.security import verify_api_key

router = APIRouter(tags=["assets"])

def get_asset_service(db: Session = Depends(get_db)) -> AssetService:
    asset_repo = AssetRepository(db)
    tag_repo = TagRepository(db)
    return AssetService(asset_repo, tag_repo)

@router.post("/assets", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
def create_asset(asset_in: AssetCreate, service: AssetService = Depends(get_asset_service), api_key: str = Depends(verify_api_key)):
    return service.create_asset(asset_in)

@router.get("/assets", response_model=PaginatedResponse[AssetResponse])
def get_assets(
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=1000),
    type: Optional[str] = None,
    status_filter: Optional[str] = Query(None, alias="status"),
    search: Optional[str] = None,
    tag: Optional[str] = None,
    sort: Optional[Literal["first_seen", "last_seen", "value"]] = Query(None, description="Sort by field"),
    order: Literal["asc", "desc"] = Query("desc", description="Sort order"),
    service: AssetService = Depends(get_asset_service)
):
    filters = {}
    if type:
        filters["type"] = type
    if status_filter:
        filters["status"] = status_filter

    sort_by = sort if sort else "last_seen"
    items, total = service.get_assets(page=page, size=size, filters=filters, search=search, tag=tag, sort_by=sort_by, order=order)
    pages = (total + size - 1) // size if size else 0
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=pages
    )

@router.get("/assets/{id}", response_model=AssetResponse)
def get_asset(id: UUID, service: AssetService = Depends(get_asset_service)):
    return service.get_asset(id)

@router.put("/assets/{id}", response_model=AssetResponse)
def update_asset(id: UUID, asset_in: AssetUpdate, service: AssetService = Depends(get_asset_service), api_key: str = Depends(verify_api_key)):
    return service.update_asset(id, asset_in)

@router.delete("/assets/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(id: UUID, service: AssetService = Depends(get_asset_service), api_key: str = Depends(verify_api_key)):
    service.delete_asset(id)
