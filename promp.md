Implement **API Key Authentication** for this FastAPI project while strictly following the existing project architecture and coding style.

Requirements:

* Do **NOT** refactor the project or change the existing architecture.
* Do **NOT** introduce JWT, user authentication, login, or user models.
* Use a simple **API Key** approach because the task explicitly requires "Lightweight authentication (API Key or JWT)" and this project has no user management.
* Reuse the current dependency injection pattern already used throughout the project.

Implementation details:

1. Implement the authentication logic inside `app/core/security.py`.
2. Read the API key from environment variables (`API_KEY`).
3. Create a FastAPI dependency named `verify_api_key`.
4. The dependency should read the `X-API-Key` header.
5. If the key is missing or invalid, return HTTP 401 with a clear JSON response.
6. Do not hardcode secrets; use the existing configuration/settings module if one exists. Otherwise, use `os.getenv`.
7. Protect **only write operations**:

   * POST
   * PUT
   * PATCH
   * DELETE
     Leave GET endpoints public.
8. Apply the dependency only at the router/endpoint level without changing business logic or service code.
9. Ensure Swagger/OpenAPI automatically exposes the `X-API-Key` header for protected endpoints.
10. Update `.env.example` if necessary by adding `API_KEY=your-secret-key`.
11. Keep the implementation clean, minimal, and production-ready.

Constraints:

* Do not modify database models.
* Do not change services or repositories unless absolutely required.
* Do not break existing endpoints.
* Follow the current project's folder structure and architecture.
* Keep the implementation consistent with the existing codebase.

At the end, provide:

1. A summary of every modified file.
2. A brief explanation of how to test the authentication using Swagger and cURL.
3. Confirmation that the implementation satisfies the task requirement for lightweight authentication.
