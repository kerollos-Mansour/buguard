from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import Session

from app.db.models.relationship import Relationship
from app.schemas.relationship import RelationshipCreate

class RelationshipRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, relationship_create: RelationshipCreate) -> Relationship:
        relationship = Relationship(
            source_asset_id=relationship_create.source_asset_id,
            target_asset_id=relationship_create.target_asset_id,
            relationship_type=relationship_create.relationship_type
        )
        self.session.add(relationship)
        self.session.flush()
        self.session.refresh(relationship)
        return relationship

    def get_by_id(self, relationship_id: UUID) -> Optional[Relationship]:
        stmt = select(Relationship).options(
            selectinload(Relationship.source_asset),
            selectinload(Relationship.target_asset)
        ).where(Relationship.id == relationship_id)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()

    def get_by_source_and_target(self, source_id: UUID, target_id: UUID, rel_type: str) -> Optional[Relationship]:
        stmt = select(Relationship).where(
            Relationship.source_asset_id == source_id,
            Relationship.target_asset_id == target_id,
            Relationship.relationship_type == rel_type
        )
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()

    def get_by_source_asset(self, source_id: UUID, page: int = 1, size: int = 50) -> Tuple[List[Relationship], int]:
        stmt = select(Relationship).options(
            selectinload(Relationship.target_asset)
        ).where(Relationship.source_asset_id == source_id)
        
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = self.session.execute(count_stmt)
        total = total_result.scalar_one()
        
        stmt = stmt.offset((page - 1) * size).limit(size)
        result = self.session.execute(stmt)
        items = list(result.scalars().all())
        
        return items, total

    def get_by_target_asset(self, target_id: UUID, page: int = 1, size: int = 50) -> Tuple[List[Relationship], int]:
        stmt = select(Relationship).options(
            selectinload(Relationship.source_asset)
        ).where(Relationship.target_asset_id == target_id)
        
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = self.session.execute(count_stmt)
        total = total_result.scalar_one()
        
        stmt = stmt.offset((page - 1) * size).limit(size)
        result = self.session.execute(stmt)
        items = list(result.scalars().all())
        
        return items, total

    def delete(self, relationship: Relationship) -> None:
        self.session.delete(relationship)
        self.session.flush()
