from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Any, Dict

from app.db.database import get_db
from app.db.repositories.relationship_repository import RelationshipRepository
from app.db.repositories.asset_repository import AssetRepository
from app.services.relationship_service import RelationshipService
from app.schemas.relationship import RelationshipCreate, RelationshipResponse

router = APIRouter(tags=["relationships"])

def get_relationship_service(db: Session = Depends(get_db)) -> RelationshipService:
    rel_repo = RelationshipRepository(db)
    asset_repo = AssetRepository(db)
    return RelationshipService(rel_repo, asset_repo)

@router.post("/relationships", response_model=RelationshipResponse, status_code=status.HTTP_201_CREATED)
def create_relationship(rel_in: RelationshipCreate, service: RelationshipService = Depends(get_relationship_service)):
    return service.create_relationship(rel_in)

@router.get("/assets/{id}/relationships")
def get_asset_relationships(
    id: UUID, 
    page: int = Query(1, ge=1), 
    size: int = Query(50, ge=1, le=1000), 
    service: RelationshipService = Depends(get_relationship_service)
):
    return service.get_asset_relationships(id, page, size)

@router.get("/assets/{id}/graph")
def get_asset_graph(
    id: UUID, 
    depth: int = Query(1, ge=1, le=5), 
    service: RelationshipService = Depends(get_relationship_service)
):
    return service.get_asset_graph(id, depth)
