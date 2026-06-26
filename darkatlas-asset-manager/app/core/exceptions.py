from fastapi import Request
from fastapi.responses import JSONResponse


# --- Custom Exceptions ---

class AssetNotFoundException(Exception):
    def __init__(self, detail: str = "Asset not found."):
        self.detail = detail


class DuplicateAssetException(Exception):
    def __init__(self, detail: str = "Asset already exists."):
        self.detail = detail


class TagNotFoundException(Exception):
    def __init__(self, detail: str = "Tag not found."):
        self.detail = detail


class RelationshipNotFoundException(Exception):
    def __init__(self, detail: str = "Relationship not found."):
        self.detail = detail


class RelationshipException(Exception):
    def __init__(self, detail: str = "Invalid relationship."):
        self.detail = detail


# --- Global Exception Handlers ---

async def asset_not_found_handler(request: Request, exc: AssetNotFoundException):
    return JSONResponse(status_code=404, content={"detail": exc.detail})


async def duplicate_asset_handler(request: Request, exc: DuplicateAssetException):
    return JSONResponse(status_code=400, content={"detail": exc.detail})


async def tag_not_found_handler(request: Request, exc: TagNotFoundException):
    return JSONResponse(status_code=404, content={"detail": exc.detail})


async def relationship_not_found_handler(request: Request, exc: RelationshipNotFoundException):
    return JSONResponse(status_code=404, content={"detail": exc.detail})


async def relationship_exception_handler(request: Request, exc: RelationshipException):
    return JSONResponse(status_code=400, content={"detail": exc.detail})
