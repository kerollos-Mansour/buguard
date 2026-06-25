Implement Phase 2: Database Models.

Follow the existing project architecture exactly. Do not change folders, files, naming conventions, or introduce new layers.

Create SQLAlchemy 2.0 models only inside:

app/db/models/

* asset.py
* tag.py
* asset_tag.py
* relationship.py

Requirements:

Asset:

* id (UUID)
* type
* value
* status
* first_seen
* last_seen
* source
* metadata (JSONB)
* Unique(type, value)

Tag:

* id (UUID)
* name (unique)

AssetTag:

* asset_id
* tag_id

Relationship:

* id (UUID)
* source_asset_id
* target_asset_id
* relationship_type

Relationships:

* Asset ↔ Tags (Many-to-Many)
* Asset ↔ Relationship (Self-referencing graph)

Rules:

* Use SQLAlchemy 2.0 style.
* Use PostgreSQL types where appropriate.
* Add proper constraints, indexes, and relationships.
* Register models with Base.
* Do not modify architecture.
* Do not create schemas.
* Do not create repositories.
* Do not create services.
* Do not create API routes.
* Do not generate documentation or explanations.

Only implement the model files.
