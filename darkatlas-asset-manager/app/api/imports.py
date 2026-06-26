from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db.repositories.asset_repository import AssetRepository
from app.services.import_service import ImportService
from app.schemas.asset import AssetCreate, AssetResponse
from app.core.security import verify_api_key

router = APIRouter(tags=["imports"])

def get_import_service(db: Session = Depends(get_db)) -> ImportService:
    asset_repo = AssetRepository(db)
    return ImportService(asset_repo)

@router.post("/assets/import", response_model=List[AssetResponse], status_code=status.HTTP_201_CREATED)
def import_assets(assets_in: List[AssetCreate], service: ImportService = Depends(get_import_service), api_key: str = Depends(verify_api_key)):
    return service.import_assets(assets_in)
