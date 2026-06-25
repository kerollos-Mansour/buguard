Implement Phase 7 — API Endpoints.

Follow the existing architecture exactly.

Create endpoints inside:

app/api/

* assets.py
* imports.py
* relationships.py
* health.py

Requirements:

Assets:

* POST /assets
* GET /assets
* GET /assets/{id}
* PUT /assets/{id}
* DELETE /assets/{id}

Support:

* Search
* Filtering
* Pagination

Imports:

* POST /assets/import

Relationships:

* POST /relationships
* GET /assets/{id}/relationships
* GET /assets/{id}/graph

Health:

* GET /health

Rules:

* API layer must contain routing only.
* No business logic in endpoints.
* Use services via dependency injection.
* Use schemas for request/response validation.
* Keep architecture unchanged.
