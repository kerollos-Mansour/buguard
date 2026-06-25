from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional, List

from app.db.database import get_db
from app.db.repositories.asset_repository import AssetRepository
from app.db.repositories.tag_repository import TagRepository
from app.services.asset_service import AssetService
from app.schemas.asset import AssetCreate, AssetUpdate, AssetResponse
from app.schemas.common import PaginatedResponse

router = APIRouter(tags=["assets"])

def get_asset_service(db: Session = Depends(get_db)) -> AssetService:
    asset_repo = AssetRepository(db)
    tag_repo = TagRepository(db)
    return AssetService(asset_repo, tag_repo)

@router.post("/assets", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
async def create_asset(asset_in: AssetCreate, service: AssetService = Depends(get_asset_service)):
    return await service.create_asset(asset_in)

@router.get("/assets", response_model=PaginatedResponse[AssetResponse])
async def get_assets(
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=1000),
    type: Optional[str] = None,
    status_filter: Optional[str] = Query(None, alias="status"),
    search: Optional[str] = None,
    service: AssetService = Depends(get_asset_service)
):
    filters = {}
    if type:
        filters["type"] = type
    if status_filter:
        filters["status"] = status_filter
        
    items, total = await service.get_assets(page=page, size=size, filters=filters, search=search)
    pages = (total + size - 1) // size if size else 0
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=pages
    )

@router.get("/assets/{id}", response_model=AssetResponse)
async def get_asset(id: UUID, service: AssetService = Depends(get_asset_service)):
    return await service.get_asset(id)

@router.put("/assets/{id}", response_model=AssetResponse)
async def update_asset(id: UUID, asset_in: AssetUpdate, service: AssetService = Depends(get_asset_service)):
    return await service.update_asset(id, asset_in)

@router.delete("/assets/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset(id: UUID, service: AssetService = Depends(get_asset_service)):
    await service.delete_asset(id)
