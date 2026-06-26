
**Prompt:**

 Implement automated tests for the backend project using pytest. Do not modify any production code.

 The goal is to create simple and clear test cases (not complex or over-engineered code).

 Focus only on core business logic:

 * Deduplication logic: ensure duplicate assets are not created and last_seen is updated correctly
 * Filtering logic: test filtering by type, status, tags, value contains, and pagination
 * Relationships logic: test creating relationships, retrieving related assets, and basic graph consistency
 Requirements:

 * Keep the tests simple and easy to understand (avoid complex patterns or unnecessary abstraction)
 * Use basic pytest structure with clear test cases
 * Use sample/mock data where needed
 * Cover both success and failure scenarios where relevant
 * Ensure tests run independently
> Do not write any explanations or documentation. Only implement straightforward, minimal, and readable test cases inside the existing test files.

---
