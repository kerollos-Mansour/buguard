import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base

class Relationship(Base):
    __tablename__ = "relationship"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_asset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("asset.id", ondelete="CASCADE"), nullable=False, index=True)
    target_asset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("asset.id", ondelete="CASCADE"), nullable=False, index=True)
    relationship_type: Mapped[str] = mapped_column(String, nullable=False, index=True)

    source_asset: Mapped["Asset"] = relationship(
        "Asset", foreign_keys=[source_asset_id], back_populates="source_relationships"
    )
    target_asset: Mapped["Asset"] = relationship(
        "Asset", foreign_keys=[target_asset_id], back_populates="target_relationships"
    )
