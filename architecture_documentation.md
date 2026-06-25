# DarkAtlas Asset Management System - Architecture Documentation

## 1. Folder and File Responsibilities

*   **`app/`**: The main application package containing all source code.
    *   **`main.py`**: The entry point of the FastAPI application. It initializes the app instance, configures middleware, and includes all API routers.
*   **`app/core/`**: Contains core application configuration and cross-cutting concerns.
    *   **`config.py`**: Manages environment variables and application settings using Pydantic `BaseSettings`.
    *   **`security.py`**: Houses security utilities such as API key hashing, validation, and encryption functions.
    *   **`exceptions.py`**: Defines custom application exceptions and global FastAPI exception handlers to ensure consistent error responses.
*   **`app/api/`**: The presentation layer. Contains all HTTP route definitions and handlers.
    *   **`assets.py`**: Endpoints for managing individual assets (CRUD, search).
    *   **`relationships.py`**: Endpoints for defining and querying connections between assets.
    *   **`imports.py`**: Endpoints for handling bulk data ingestion.
    *   **`health.py`**: Liveness and readiness probes for monitoring tools and container orchestration.
*   **`app/services/`**: The business logic layer. Orchestrates operations between the API and data access layers.
    *   **`asset_service.py`**: Implements core asset logic (creation rules, deduplication, state transitions).
    *   **`import_service.py`**: Handles parsing, validating, and processing bulk asset payloads.
    *   **`relationship_service.py`**: Validates and constructs the graph of dependencies between assets.
*   **`app/db/`**: The data persistence layer, containing database configurations, ORM definitions, and data access objects.
    *   **`database.py`**: Configures the SQLAlchemy engine, session maker, and the declarative base for models.
    *   **`models/`**: Contains SQLAlchemy ORM classes that map directly to database tables.
        *   **`asset.py`**: The core `Asset` table mapping.
        *   **`tag.py`**: The `Tag` table mapping.
        *   **`relationship.py`**: The `Relationship` table mapping.
        *   **`asset_tag.py`**: The many-to-many junction table between assets and tags.
    *   **`repositories/`**: Encapsulates all direct database queries, hiding SQLAlchemy syntax from the rest of the application.
        *   **`asset_repository.py`**: Handles database interactions for assets.
        *   **`tag_repository.py`**: Handles database interactions for tags.
        *   **`relationship_repository.py`**: Handles database interactions for relationships.
*   **`app/schemas/`**: Defines Pydantic models used for input validation, serialization, and API documentation.
    *   **`asset.py`**: Input/output schemas for assets.
    *   **`tag.py`**: Input/output schemas for tags.
    *   **`relationship.py`**: Input/output schemas for relationships.
*   **`app/tests/`**: Contains the automated test suite (unit, integration, and end-to-end tests) using Pytest.
*   **`docker-compose.yml`**: Defines the multi-container Docker application, setting up the FastAPI app and PostgreSQL database to run together.
*   **`Dockerfile`**: Instructions for building the application's container image.
*   **`requirements.txt`**: Specifies the Python dependencies required to run the application.
*   **`.env.example`**: A template file illustrating the required environment variables.
*   **`README.md`**: Project documentation, setup instructions, and general information.

---

## 2. Why this Architecture was Chosen

The **Layered (N-Tier) Architecture** with a Repository Pattern was chosen because it provides a clean, predictable, and highly structured foundation. For an intern assessment, it demonstrates a strong grasp of enterprise software design without introducing the unnecessary overhead of microservices or heavy Domain-Driven Design (DDD). 
This structure ensures that changes in one part of the system (e.g., swapping a database engine or changing an API response format) have minimal impact on other parts, leading to a highly maintainable codebase.

---

## 3. Scalability Benefits

*   **Horizontal Scaling:** Because the application is stateless and API-driven, multiple instances of the FastAPI container can be spun up behind a load balancer to handle increased traffic.
*   **Database Optimization:** The Repository Pattern allows database queries to be optimized, cached (e.g., using Redis), or refactored centrally without touching business logic.
*   **Feature Expansion:** New features (like a background worker for asynchronous asset scanning) can easily reuse the existing `services` layer without needing to route through the HTTP API layer.

---

## 4. Separation of Concerns

The architecture strictly enforces boundaries between different responsibilities:
1.  **API Layer:** Cares *only* about HTTP requests, routing, status codes, and input/output validation (via Pydantic). It delegates all actual work to the Service Layer.
2.  **Service Layer:** Cares *only* about business rules, logic, and workflow orchestration. It doesn't know it's being called by an HTTP endpoint, and it doesn't know if data is stored in Postgres or memory.
3.  **Repository Layer:** Cares *only* about executing database queries and returning mapped data. It abstracts the SQLAlchemy ORM away from the Service Layer.
4.  **Database Layer:** Cares *only* about persisting data, maintaining relational integrity, and indexing.

---

## 5. Database Design Conceptually

The database uses a relational model (PostgreSQL) optimized for flexibility and fast querying of network assets. It relies heavily on UUIDs for primary keys to ensure global uniqueness and prevent enumeration. The design uses normalized tables for core entities, with foreign keys enforcing referential integrity. Junction tables are utilized to handle many-to-many associations, such as tagging.

---

## 6. Conceptual Table Definitions

*   **Asset Table:**
    *   `id` (UUID, Primary Key)
    *   `type` (Enum: DOMAIN, SUBDOMAIN, IP_ADDRESS, SERVICE)
    *   `value` (String, Indexed, Unique per type - e.g., "example.com", "192.168.1.1")
    *   `status` (Enum: ACTIVE, INACTIVE, DELETED)
    *   `created_at` (Timestamp)
    *   `updated_at` (Timestamp)
*   **Tag Table:**
    *   `id` (UUID, Primary Key)
    *   `name` (String, Unique - e.g., "production", "vulnerable")
*   **AssetTag Table (Junction):**
    *   `asset_id` (UUID, Foreign Key to Asset)
    *   `tag_id` (UUID, Foreign Key to Tag)
    *   *(Composite Primary Key: asset_id + tag_id)*
*   **Relationship Table:**
    *   `id` (UUID, Primary Key)
    *   `source_asset_id` (UUID, Foreign Key to Asset)
    *   `target_asset_id` (UUID, Foreign Key to Asset)
    *   `type` (Enum: RESOLVES_TO, SUBDOMAIN_OF, RUNS_ON)
    *   `created_at` (Timestamp)

---

## 7. API Endpoints Conceptually

*   `GET /assets` - Fetch a list of assets (supports pagination, sorting, and filtering by type/tag).
*   `POST /assets` - Register a new single asset.
*   `GET /assets/{id}` - Retrieve details for a specific asset by its ID.
*   `PUT /assets/{id}` - Update properties or status of a specific asset.
*   `DELETE /assets/{id}` - Soft-delete an asset.
*   `POST /assets/import` - Upload a batch of assets (e.g., JSON list) for bulk processing.
*   `GET /assets/{id}/relationships` - Retrieve the graph/list of connected assets for a given asset.
*   `POST /relationships` - Establish a new link between two existing assets.

---

## 8. Service Responsibilities

*   **`AssetService`:** Orchestrates the lifecycle of an asset. It receives data from the API, enforces business rules (like checking for duplicates), coordinates with the `TagRepository` if tags are provided, and finally calls the `AssetRepository` to save changes.
*   **`ImportService`:** Handles the complexity of bulk data ingestion. It parses the payload, chunks the data if necessary, and efficiently communicates with the `AssetService` or `AssetRepository` to perform bulk inserts/upserts while minimizing database load.
*   **`RelationshipService`:** Ensures that relationships make logical sense (e.g., verifying both source and target assets exist before linking, and preventing recursive or invalid relationship types).

---

## 9. Repository Responsibilities

*   **`AssetRepository`:** Contains all SQLAlchemy session calls related to assets. It handles complex queries like "find all assets of type IP that have the tag 'critical'". 
*   **`TagRepository`:** Retrieves existing tags by name or creates them if they don't exist.
*   **`RelationshipRepository`:** Handles the insertion of dependency links and the retrieval of an asset's relationship tree.

---

## 10. Deduplication Strategy

To prevent redundant data, deduplication is enforced at both the Database and Service levels.
1.  **Database Level:** A unique constraint is placed on the combination of `(type, value)` in the Asset table (e.g., there can only be one DOMAIN with the value "example.com").
2.  **Service Level:** Before creation, the `AssetService` queries the repository to check if an asset with the requested `type` and `value` already exists. If it does, the system performs an "Upsert" (Update/Insert) operation. Instead of throwing an error or creating a duplicate, it updates the existing record's `updated_at` timestamp and merges any new tags or relationships provided in the request.

---

## 11. Lifecycle Management Strategy

Assets are managed using a **Soft Delete** and **State Machine** strategy. 
Assets are rarely permanently removed (hard deleted) from the database because historical context is vital in Attack Surface Monitoring. Instead, the `Asset` table includes a `status` field. When an asset is "deleted", its status transitions from `ACTIVE` to `DELETED`. API read endpoints (`GET /assets`) filter out `DELETED` assets by default, while still allowing administrators or specific queries to audit historical data.

---

## 12. Authentication Strategy

The system utilizes **API Key Authentication**, which is ideal for a machine-to-machine backend system.
Clients must provide an API key in the HTTP headers (e.g., `X-API-Key: your_secure_token`). A FastAPI Dependency intercepts the request, hashes the provided token, and validates it against stored valid keys. If validation fails, a `401 Unauthorized` exception is raised immediately, halting the request flow before it ever reaches the API route handler.

---

## 13. Testing Strategy

The testing strategy follows the standard testing pyramid utilizing Pytest:
*   **Unit Tests:** Focus on testing pure business logic within the `services/` layer and utility functions in `core/`. Database repositories are mocked to ensure tests run rapidly and in isolation.
*   **Integration Tests:** Focus on the `repositories/` layer. These tests connect to a dedicated, ephemeral PostgreSQL test database to verify that SQLAlchemy models, queries, and constraints behave as expected.
*   **End-to-End (E2E) Tests:** Use FastAPI's `TestClient` to simulate real HTTP requests against the endpoints. These tests validate the entire request lifecycle, from payload validation through service logic down to database persistence and back to the JSON response.

---

## 14. Request Flow from Endpoint to Database

*Example Scenario: Creating a new Asset via `POST /assets`*

1.  **Client Request:** The client sends an HTTP POST request with a JSON payload to the API.
2.  **API Layer:** The route in `app/api/assets.py` receives the request. The Pydantic schema (`app/schemas/asset.py`) automatically parses and validates the JSON. If validation passes, the route handler passes the resulting Pydantic object to the `AssetService`.
3.  **Service Layer:** The `AssetService` receives the data. It applies business logic, such as executing the deduplication strategy to check if the asset exists. Assuming it is new, it prepares the data to be saved.
4.  **Repository Layer:** The `AssetService` calls `AssetRepository.create()`. The repository maps the data to the SQLAlchemy `Asset` model, adds it to the database session, and commits the transaction to PostgreSQL.
5.  **Response:** The database returns the newly created record. The Repository passes this up to the Service, which passes it to the API route. The route serializes the data back into a JSON-compliant Pydantic response schema and returns an `HTTP 201 Created` status to the client.
