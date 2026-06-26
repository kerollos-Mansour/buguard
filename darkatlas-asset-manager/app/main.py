from fastapi import FastAPI

from app.api.assets import router as assets_router
from app.api.imports import router as imports_router
from app.api.relationships import router as relationships_router
from app.api.health import router as health_router

app = FastAPI(
    title="DarkAtlas Asset Management System",
    description="Asset management module for Attack Surface Monitoring",
    version="1.0.0"
)

app.include_router(health_router)
app.include_router(assets_router)
app.include_router(imports_router)
app.include_router(relationships_router)
