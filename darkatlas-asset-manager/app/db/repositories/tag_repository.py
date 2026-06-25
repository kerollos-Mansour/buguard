from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.tag import Tag
from app.schemas.tag import TagCreate

class TagRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, tag_create: TagCreate) -> Tag:
        tag = Tag(name=tag_create.name)
        self.session.add(tag)
        await self.session.flush()
        await self.session.refresh(tag)
        return tag

    async def get_by_id(self, tag_id: UUID) -> Optional[Tag]:
        stmt = select(Tag).where(Tag.id == tag_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[Tag]:
        stmt = select(Tag).where(Tag.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, page: int = 1, size: int = 50, search: Optional[str] = None) -> Tuple[List[Tag], int]:
        stmt = select(Tag)
        
        if search:
            stmt = stmt.where(Tag.name.ilike(f"%{search}%"))
            
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.session.execute(count_stmt)
        total = total_result.scalar_one()
        
        stmt = stmt.order_by(Tag.name).offset((page - 1) * size).limit(size)
        result = await self.session.execute(stmt)
        items = list(result.scalars().all())
        
        return items, total

    async def update(self, tag: Tag, tag_update: TagCreate) -> Tag:
        tag.name = tag_update.name
        await self.session.flush()
        await self.session.refresh(tag)
        return tag

    async def delete(self, tag: Tag) -> None:
        await self.session.delete(tag)
        await self.session.flush()
