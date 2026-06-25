Implement Phase 3 and Phase 4 only.

Follow the existing project architecture exactly. Do not change folders, file names, or introduce new layers.

Phase 3 — Schemas

Create Pydantic schemas inside:

app/schemas/

* asset.py
* tag.py
* relationship.py
* common.py

Requirements:

* AssetCreate
* AssetUpdate
* AssetResponse
* TagCreate
* TagResponse
* RelationshipCreate
* RelationshipResponse
* Pagination schemas
* Standard API response schemas
* Validation rules where appropriate

Phase 4 — Repositories

Create repositories inside:

app/db/repositories/

* asset_repository.py
* tag_repository.py
* relationship_repository.py

Requirements:

* Database access only
* CRUD queries
* Filtering
* Search
* Pagination support
* Relationship queries
* No business logic

Rules:

* Use SQLAlchemy 2.0 style.
* Keep repositories focused on data access only.
* Do not modify existing models.
* Do not create services.
* Do not create API routes.
* Do not create tests.
* Do not generate documentation or explanations.
* Do not print architecture summaries.

Only implement schemas and repositories while respecting the current architecture.
