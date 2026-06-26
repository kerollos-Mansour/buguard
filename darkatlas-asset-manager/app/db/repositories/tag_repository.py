from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.db.models.tag import Tag
from app.schemas.tag import TagCreate

class TagRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, tag_create: TagCreate) -> Tag:
        tag = Tag(name=tag_create.name)
        self.session.add(tag)
        self.session.flush()
        self.session.refresh(tag)
        return tag

    def get_by_id(self, tag_id: UUID) -> Optional[Tag]:
        stmt = select(Tag).where(Tag.id == tag_id)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()

    def get_by_name(self, name: str) -> Optional[Tag]:
        stmt = select(Tag).where(Tag.name == name)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()

    def get_all(self, page: int = 1, size: int = 50, search: Optional[str] = None) -> Tuple[List[Tag], int]:
        stmt = select(Tag)
        
        if search:
            stmt = stmt.where(Tag.name.ilike(f"%{search}%"))
            
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = self.session.execute(count_stmt)
        total = total_result.scalar_one()
        
        stmt = stmt.order_by(Tag.name).offset((page - 1) * size).limit(size)
        result = self.session.execute(stmt)
        items = list(result.scalars().all())
        
        return items, total

    def update(self, tag: Tag, tag_update: TagCreate) -> Tag:
        tag.name = tag_update.name
        self.session.flush()
        self.session.refresh(tag)
        return tag

    def delete(self, tag: Tag) -> None:
        self.session.delete(tag)
        self.session.flush()
