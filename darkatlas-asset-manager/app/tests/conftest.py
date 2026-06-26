import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.db.database import Base
from app.db.repositories.asset_repository import AssetRepository
from app.db.repositories.tag_repository import TagRepository
from app.db.repositories.relationship_repository import RelationshipRepository
from app.services.asset_service import AssetService
from app.services.import_service import ImportService
from app.services.relationship_service import RelationshipService
from app.schemas.asset import AssetCreate

# Uses a dedicated test database — make sure PostgreSQL is running
# and the user has permission to create/drop tables.
TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/darkatlas_test"

engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    # Import all models so Base knows about them before creating tables
    import app.db.models.asset       # noqa
    import app.db.models.tag         # noqa
    import app.db.models.asset_tag   # noqa
    import app.db.models.relationship  # noqa

    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def asset_service(db):
    asset_repo = AssetRepository(db)
    tag_repo = TagRepository(db)
    return AssetService(asset_repo, tag_repo)


@pytest.fixture
def import_service(db):
    asset_repo = AssetRepository(db)
    return ImportService(asset_repo)


@pytest.fixture
def relationship_service(db):
    rel_repo = RelationshipRepository(db)
    asset_repo = AssetRepository(db)
    return RelationshipService(rel_repo, asset_repo)


@pytest.fixture
def sample_asset_data():
    return AssetCreate(type="DOMAIN", value="example.com", status="ACTIVE")


@pytest.fixture
def another_asset_data():
    return AssetCreate(type="IP_ADDRESS", value="192.168.1.1", status="ACTIVE")
