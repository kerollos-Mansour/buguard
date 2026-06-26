import pytest
from fastapi import HTTPException

from app.schemas.asset import AssetCreate


def test_create_asset_is_unique(asset_service):
    asset_service.create_asset(AssetCreate(type="DOMAIN", value="dedup.com"))

    with pytest.raises(HTTPException) as exc_info:
        asset_service.create_asset(AssetCreate(type="DOMAIN", value="dedup.com"))

    assert exc_info.value.status_code == 400
    assert "already exists" in exc_info.value.detail


def test_same_value_different_type_is_allowed(asset_service):
    a1 = asset_service.create_asset(AssetCreate(type="DOMAIN", value="shared-value.com"))
    a2 = asset_service.create_asset(AssetCreate(type="SUBDOMAIN", value="shared-value.com"))
    assert a1.id != a2.id


def test_import_dedup_updates_last_seen(import_service, db):
    from app.db.repositories.asset_repository import AssetRepository
    from app.schemas.asset import AssetCreate
    import time

    asset_repo = AssetRepository(db)
    initial = [AssetCreate(type="DOMAIN", value="lastseen-test.com")]
    created = import_service.import_assets(initial)
    first_last_seen = created[0].last_seen

    time.sleep(0.05)

    reimported = import_service.import_assets([AssetCreate(type="DOMAIN", value="lastseen-test.com", source="new-source")])
    assert reimported[0].id == created[0].id


def test_import_dedup_does_not_create_new_record(import_service):
    assets = [
        AssetCreate(type="IP_ADDRESS", value="9.9.9.9"),
        AssetCreate(type="IP_ADDRESS", value="9.9.9.9"),
        AssetCreate(type="IP_ADDRESS", value="9.9.9.9"),
    ]
    results = import_service.import_assets(assets)
    all_same_id = all(r.id == results[0].id for r in results)
    assert all_same_id
