from typing import Optional, List, Tuple, Any, Dict
from uuid import UUID
from sqlalchemy import select, func, or_, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import Session

from app.db.models.asset import Asset
from app.db.models.tag import Tag
from app.schemas.asset import AssetCreate, AssetUpdate

class AssetRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, asset_create: AssetCreate) -> Asset:
        asset = Asset(
            type=asset_create.type,
            value=asset_create.value,
            status=asset_create.status,
            source=asset_create.source,
            asset_metadata=asset_create.asset_metadata
        )
        self.session.add(asset)
        self.session.flush()
        self.session.refresh(asset)
        return asset

    def get_by_id(self, asset_id: UUID) -> Optional[Asset]:
        stmt = select(Asset).options(selectinload(Asset.tags)).where(Asset.id == asset_id)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()
        
    def get_by_type_and_value(self, type: str, value: str) -> Optional[Asset]:
        stmt = select(Asset).options(selectinload(Asset.tags)).where(Asset.type == type, Asset.value == value)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()

    def get_all(self, page: int = 1, size: int = 50, filters: Optional[Dict[str, Any]] = None, search: Optional[str] = None) -> Tuple[List[Asset], int]:
        stmt = select(Asset).options(selectinload(Asset.tags))
        
        if filters:
            if "type" in filters and filters["type"]:
                stmt = stmt.where(Asset.type == filters["type"])
            if "status" in filters and filters["status"]:
                stmt = stmt.where(Asset.status == filters["status"])
                
        if search:
            stmt = stmt.where(or_(
                Asset.value.ilike(f"%{search}%"),
                Asset.source.ilike(f"%{search}%")
            ))
            
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = self.session.execute(count_stmt)
        total = total_result.scalar_one()
        
        stmt = stmt.order_by(Asset.last_seen.desc()).offset((page - 1) * size).limit(size)
        result = self.session.execute(stmt)
        items = list(result.scalars().all())
        
        return items, total

    def update(self, asset: Asset, asset_update: AssetUpdate) -> Asset:
        update_data = asset_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(asset, key, value)
            
        self.session.flush()
        self.session.refresh(asset)
        return asset

    def delete(self, asset: Asset) -> None:
        self.session.delete(asset)
        self.session.flush()

    def add_tag(self, asset: Asset, tag: Tag) -> None:
        if tag not in asset.tags:
            asset.tags.append(tag)
            self.session.flush()

    def remove_tag(self, asset: Asset, tag: Tag) -> None:
        if tag in asset.tags:
            asset.tags.remove(tag)
            self.session.flush()
