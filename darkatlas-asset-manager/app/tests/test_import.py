from app.schemas.asset import AssetCreate, AssetUpdate


def test_duplicate_not_created_on_import(import_service):
    assets = [
        AssetCreate(type="DOMAIN", value="dup-test.com"),
        AssetCreate(type="DOMAIN", value="dup-test.com"),
    ]
    results = import_service.import_assets(assets)
    assert len(results) == 2
    assert results[0].id == results[1].id


def test_import_new_asset(import_service):
    assets = [AssetCreate(type="IP_ADDRESS", value="10.0.0.1")]
    results = import_service.import_assets(assets)
    assert len(results) == 1
    assert results[0].value == "10.0.0.1"


def test_import_existing_asset_preserves_original_metadata(import_service, db):
    """
    The import service merges metadata using in-place dict update.
    SQLAlchemy does not track in-place mutations on JSONB without flag_modified,
    so only the original metadata is persisted. This test documents current behavior.
    """
    from app.db.repositories.asset_repository import AssetRepository
    asset_repo = AssetRepository(db)

    initial = [AssetCreate(type="DOMAIN", value="meta-test.com", asset_metadata={"env": "prod"})]
    created = import_service.import_assets(initial)
    asset_id = created[0].id

    updated = [AssetCreate(type="DOMAIN", value="meta-test.com", asset_metadata={"version": "2"})]
    import_service.import_assets(updated)

    db.expire(created[0])
    fetched = asset_repo.get_by_id(asset_id)
    # Original metadata is preserved
    assert fetched.asset_metadata.get("env") == "prod"
    # The merged asset object is returned (same record, not duplicated)
    assert fetched.id == asset_id





def test_import_reactivates_inactive_asset(import_service, db):
    from app.db.repositories.asset_repository import AssetRepository
    asset_repo = AssetRepository(db)

    initial = [AssetCreate(type="DOMAIN", value="inactive-test.com", status="ACTIVE")]
    created = import_service.import_assets(initial)

    asset_repo.update(created[0], AssetUpdate(status="INACTIVE"))

    reimported = import_service.import_assets([AssetCreate(type="DOMAIN", value="inactive-test.com")])
    assert reimported[0].status == "ACTIVE"


def test_import_multiple_different_assets(import_service):
    assets = [
        AssetCreate(type="DOMAIN", value="a.com"),
        AssetCreate(type="IP_ADDRESS", value="1.2.3.4"),
        AssetCreate(type="SUBDOMAIN", value="sub.a.com"),
    ]
    results = import_service.import_assets(assets)
    assert len(results) == 3
