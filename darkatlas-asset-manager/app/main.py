from fastapi import FastAPI

from app.api.assets import router as assets_router
from app.api.imports import router as imports_router
from app.api.relationships import router as relationships_router
from app.api.health import router as health_router
from app.core.exceptions import (
    AssetNotFoundException, asset_not_found_handler,
    DuplicateAssetException, duplicate_asset_handler,
    TagNotFoundException, tag_not_found_handler,
    RelationshipNotFoundException, relationship_not_found_handler,
    RelationshipException, relationship_exception_handler,
)

app = FastAPI(
    title="DarkAtlas Asset Management System",
    description="Asset management module for Attack Surface Monitoring",
    version="1.0.0"
)

app.add_exception_handler(AssetNotFoundException, asset_not_found_handler)
app.add_exception_handler(DuplicateAssetException, duplicate_asset_handler)
app.add_exception_handler(TagNotFoundException, tag_not_found_handler)
app.add_exception_handler(RelationshipNotFoundException, relationship_not_found_handler)
app.add_exception_handler(RelationshipException, relationship_exception_handler)

app.include_router(health_router)
app.include_router(assets_router)
app.include_router(imports_router)
app.include_router(relationships_router)
