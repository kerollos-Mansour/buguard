Implement Phase 1: Database Setup only.

Tasks:

* Configure SQLAlchemy in `app/db/database.py`

  * Engine
  * SessionLocal
  * Base
  * get_db()

* Configure PostgreSQL using environment variables from `.env`

* Setup Alembic

  * `alembic.ini`
  * `alembic/env.py`
  * connect Base.metadata
  * enable autogenerate migrations

* Update:

  * `.env.example`
  * `requirements.txt`
  * `docker-compose.yml` (PostgreSQL service only if needed)

Rules:

* Keep current architecture unchanged.
* Do not create models.
* Do not create repositories.
* Do not create services.
* Do not create API routes.
* Use SQLAlchemy 2.0 style.

Generate only Phase 1 files and configuration.
