import uuid
from datetime import datetime
from typing import List, Any, Optional

from sqlalchemy import String, UniqueConstraint, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.db.database import Base

class Asset(Base):
    __tablename__ = "asset"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type: Mapped[str] = mapped_column(String, nullable=False, index=True)
    value: Mapped[str] = mapped_column(String, nullable=False, index=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="ACTIVE")
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # 'metadata' is a reserved attribute on SQLAlchemy declarative models
    # We must alias the Python attribute name.
    asset_metadata: Mapped[Optional[dict[str, Any]]] = mapped_column("metadata", JSONB, nullable=True)

    __table_args__ = (
        UniqueConstraint("type", "value", name="uq_asset_type_value"),
    )

    tags: Mapped[List["Tag"]] = relationship(
        "Tag", secondary="asset_tag", back_populates="assets"
    )

    source_relationships: Mapped[List["Relationship"]] = relationship(
        "Relationship",
        foreign_keys="[Relationship.source_asset_id]",
        back_populates="source_asset",
        cascade="all, delete-orphan"
    )

    target_relationships: Mapped[List["Relationship"]] = relationship(
        "Relationship",
        foreign_keys="[Relationship.target_asset_id]",
        back_populates="target_asset",
        cascade="all, delete-orphan"
    )
