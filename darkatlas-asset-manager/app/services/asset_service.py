from typing import Optional, List, Tuple, Any, Dict
from uuid import UUID
from fastapi import HTTPException, status

from app.db.repositories.asset_repository import AssetRepository
from app.db.repositories.tag_repository import TagRepository
from app.schemas.asset import AssetCreate, AssetUpdate
from app.db.models.asset import Asset

class AssetService:
    def __init__(self, asset_repository: AssetRepository, tag_repository: TagRepository):
        self.asset_repository = asset_repository
        self.tag_repository = tag_repository

    def create_asset(self, asset_in: AssetCreate) -> Asset:
        existing_asset = self.asset_repository.get_by_type_and_value(asset_in.type, asset_in.value)
        if existing_asset:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Asset with type '{asset_in.type}' and value '{asset_in.value}' already exists."
            )
        return self.asset_repository.create(asset_in)

    def get_asset(self, asset_id: UUID) -> Asset:
        asset = self.asset_repository.get_by_id(asset_id)
        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asset not found."
            )
        return asset

    def get_assets(self, page: int = 1, size: int = 50, filters: Optional[Dict[str, Any]] = None, search: Optional[str] = None) -> Tuple[List[Asset], int]:
        return self.asset_repository.get_all(page=page, size=size, filters=filters, search=search)

    def update_asset(self, asset_id: UUID, asset_in: AssetUpdate) -> Asset:
        asset = self.get_asset(asset_id)
        
        if asset_in.type is not None or asset_in.value is not None:
            new_type = asset_in.type if asset_in.type is not None else asset.type
            new_value = asset_in.value if asset_in.value is not None else asset.value
            
            if new_type != asset.type or new_value != asset.value:
                existing = self.asset_repository.get_by_type_and_value(new_type, new_value)
                if existing and existing.id != asset_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Another asset with this type and value already exists."
                    )
                    
        return self.asset_repository.update(asset, asset_in)

    def update_status(self, asset_id: UUID, new_status: str) -> Asset:
        asset = self.get_asset(asset_id)
        if asset.status == new_status:
            return asset
            
        update_data = AssetUpdate(status=new_status)
        return self.asset_repository.update(asset, update_data)

    def delete_asset(self, asset_id: UUID) -> None:
        asset = self.get_asset(asset_id)
        self.asset_repository.delete(asset)

    def add_tag_to_asset(self, asset_id: UUID, tag_name: str) -> Asset:
        asset = self.get_asset(asset_id)
        tag = self.tag_repository.get_by_name(tag_name)
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tag '{tag_name}' not found."
            )
            
        self.asset_repository.add_tag(asset, tag)
        return asset

    def remove_tag_from_asset(self, asset_id: UUID, tag_name: str) -> Asset:
        asset = self.get_asset(asset_id)
        tag = self.tag_repository.get_by_name(tag_name)
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tag '{tag_name}' not found."
            )
            
        self.asset_repository.remove_tag(asset, tag)
        return asset
