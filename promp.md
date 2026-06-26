

> Implement Docker setup for this backend project exactly according to the internship requirements.
>
> The goal is to make the system runnable with a single command:
>
> ```bash
> docker compose up
> ```
>
> Requirements:
>
> 1. Create a Dockerfile for the FastAPI application.
>
>    * Use a lightweight Python base image.
>    * Install dependencies from requirements.txt.
>    * Copy project files.
>    * Expose port 8000.
>    * Run the FastAPI app using uvicorn.
>
> 2. Update docker-compose.yml to include:
>
>    * A PostgreSQL service (db)
>    * A FastAPI service (api)
>    * Proper environment variables (DATABASE_URL, API_KEY if needed)
>    * depends_on so API waits for DB
>
> 3. Ensure the API connects to PostgreSQL inside Docker (not localhost).
>
> 4. Keep the setup simple and aligned with the assignment requirements.
>
>    * No advanced Docker optimizations
>    * No unnecessary complexity
>
> 5. Do not modify business logic or application code unless required for database connection.
>
> Output only the required Dockerfile and docker-compose.yml changes.

---

