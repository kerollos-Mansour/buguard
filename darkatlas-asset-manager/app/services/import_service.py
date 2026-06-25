from typing import List, Dict, Any
from app.db.repositories.asset_repository import AssetRepository
from app.schemas.asset import AssetCreate, AssetUpdate
from app.db.models.asset import Asset

class ImportService:
    def __init__(self, asset_repository: AssetRepository):
        self.asset_repository = asset_repository

    async def import_assets(self, assets_in: List[AssetCreate]) -> List[Asset]:
        result_assets = []
        for asset_data in assets_in:
            existing_asset = await self.asset_repository.get_by_type_and_value(asset_data.type, asset_data.value)
            
            if existing_asset:
                update_data = AssetUpdate()
                
                if asset_data.asset_metadata:
                    merged_metadata = existing_asset.asset_metadata or {}
                    merged_metadata.update(asset_data.asset_metadata)
                    update_data.asset_metadata = merged_metadata
                
                if asset_data.source:
                    update_data.source = asset_data.source
                    
                updated_asset = await self.asset_repository.update(existing_asset, update_data)
                result_assets.append(updated_asset)
            else:
                new_asset = await self.asset_repository.create(asset_data)
                result_assets.append(new_asset)
                
        return result_assets
