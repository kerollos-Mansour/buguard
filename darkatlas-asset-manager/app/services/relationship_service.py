from typing import List, Tuple, Dict, Any
from uuid import UUID
from fastapi import HTTPException, status

from app.db.repositories.relationship_repository import RelationshipRepository
from app.db.repositories.asset_repository import AssetRepository
from app.schemas.relationship import RelationshipCreate
from app.db.models.relationship import Relationship

class RelationshipService:
    def __init__(self, relationship_repository: RelationshipRepository, asset_repository: AssetRepository):
        self.relationship_repository = relationship_repository
        self.asset_repository = asset_repository

    async def create_relationship(self, relationship_in: RelationshipCreate) -> Relationship:
        source_asset = await self.asset_repository.get_by_id(relationship_in.source_asset_id)
        if not source_asset:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source asset not found.")
            
        target_asset = await self.asset_repository.get_by_id(relationship_in.target_asset_id)
        if not target_asset:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target asset not found.")
            
        if source_asset.id == target_asset.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Asset cannot be related to itself.")

        existing = await self.relationship_repository.get_by_source_and_target(
            source_asset.id, target_asset.id, relationship_in.relationship_type
        )
        if existing:
            return existing

        return await self.relationship_repository.create(relationship_in)

    async def get_asset_relationships(self, asset_id: UUID, page: int = 1, size: int = 50) -> Dict[str, Any]:
        asset = await self.asset_repository.get_by_id(asset_id)
        if not asset:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found.")
            
        outgoing, out_total = await self.relationship_repository.get_by_source_asset(asset_id, page=page, size=size)
        incoming, in_total = await self.relationship_repository.get_by_target_asset(asset_id, page=page, size=size)
        
        return {
            "outgoing": {"items": outgoing, "total": out_total},
            "incoming": {"items": incoming, "total": in_total}
        }

    async def get_asset_graph(self, asset_id: UUID, depth: int = 1) -> Dict[str, Any]:
        asset = await self.asset_repository.get_by_id(asset_id)
        if not asset:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found.")

        visited = set()
        nodes = []
        edges = []

        async def traverse(current_asset_id: UUID, current_depth: int):
            if current_depth > depth or current_asset_id in visited:
                return
            visited.add(current_asset_id)
            
            curr_asset = await self.asset_repository.get_by_id(current_asset_id)
            if curr_asset:
                nodes.append(curr_asset)

            outgoing, _ = await self.relationship_repository.get_by_source_asset(current_asset_id, size=1000)
            incoming, _ = await self.relationship_repository.get_by_target_asset(current_asset_id, size=1000)

            for rel in outgoing:
                edges.append(rel)
                await traverse(rel.target_asset_id, current_depth + 1)
                
            for rel in incoming:
                if rel not in edges:
                    edges.append(rel)
                await traverse(rel.source_asset_id, current_depth + 1)

        await traverse(asset_id, 0)
        
        return {
            "nodes": nodes,
            "edges": edges
        }

    async def delete_relationship(self, relationship_id: UUID) -> None:
        relationship = await self.relationship_repository.get_by_id(relationship_id)
        if not relationship:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relationship not found.")
            
        await self.relationship_repository.delete(relationship)
