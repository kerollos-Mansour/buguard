Please make the following small improvements to the project structure:

* Add `core/dependencies.py` for shared FastAPI dependencies (database session and authentication dependencies).
* Add `schemas/common.py` for shared response schemas (pagination and standard API responses).
* Expand the `tests` directory with:

  * `conftest.py`
  * `test_assets.py`
  * `test_import.py`
  * `test_dedup.py`
  * `test_relationships.py`
* Add `__init__.py` files to all Python package directories.

Do not change the architecture.
Do not add new layers or modules.
Keep the structure simple and aligned with FastAPI best practices.
Only update the project structure and file skeletons.
