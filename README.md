# DarkAtlas Asset Manager

A FastAPI-based application for managing and tracking assets (like domains, IP addresses, etc.) with automated deduplication and lifecycle tracking.

## Getting Started

You can run this project either completely containerized using Docker (recommended) or run it locally on your machine.

---

## 🐳 Running with Docker (Recommended)

Running the project via Docker is the quickest way to get started as it handles setting up the PostgreSQL database and the API environment automatically.

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed.
- [Docker Compose](https://docs.docker.com/compose/install/) installed.

### Steps to Run

1. **Build and start the containers:**
   ```bash
   docker compose up -d --build
   ```

2. **Apply Database Migrations:**
   The first time you run the project (or when the database schema changes), you need to initialize the database tables by running migrations inside the container:
   ```bash
   docker compose exec -e PYTHONPATH=/app api alembic upgrade head
   ```

3. **Access the Application:**
   - **API Base URL:** `http://localhost:8000`
   - **Interactive API Documentation (Swagger UI):** `http://localhost:8000/docs`
   - **Alternative API Docs (ReDoc):** `http://localhost:8000/redoc`

4. **Stopping the Containers:**
   To stop the application without removing your database data, run:
   ```bash
   docker compose down
   ```

---

## 💻 Running Locally (Without Docker)

If you prefer to run the FastAPI application directly on your host machine, follow these steps.

### Prerequisites
- Python 3.10+
- A running PostgreSQL instance.

### Steps to Run

1. **Clone the repository and navigate to the project root:**
   ```bash
   cd darkatlas-asset-manager
   ```

2. **Create and activate a Virtual Environment:**
   *On Windows:*
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   *On macOS/Linux:*
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Configuration:**
   - Ensure your local PostgreSQL database is running.
   - Create a database for the project (e.g., `darkatlas`).
   - Copy `.env.example` to `.env` and update the `DATABASE_URL` variable to match your local PostgreSQL credentials:
     ```env
     DATABASE_URL=postgresql://<username>:<password>@localhost:5432/<database_name>
     ```

5. **Run Database Migrations:**
   Apply the Alembic migrations to create the necessary tables in your database:
   ```bash
   alembic upgrade head
   ```

6. **Start the Development Server:**
   ```bash
py -m uvicorn app.main:app --reload
   ```

7. **Access the Application:**
   Visit `http://localhost:8000/docs` in your browser.

---

## 🧪 Running Tests

To run the automated test suite (ensure your virtual environment is active and dependencies are installed):

```bash
pytest
```
*(Note: Be sure your `DATABASE_URL` in the `.env` file points to a safe test database before running tests if your tests are not configured to use an isolated testing DB).*
