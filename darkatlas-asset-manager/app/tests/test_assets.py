import pytest
from fastapi import HTTPException

from app.schemas.asset import AssetCreate


def test_create_asset_success(asset_service, sample_asset_data):
    asset = asset_service.create_asset(sample_asset_data)
    assert asset.type == "DOMAIN"
    assert asset.value == "example.com"
    assert asset.status == "ACTIVE"


def test_duplicate_asset_raises_error(asset_service, sample_asset_data):
    asset_service.create_asset(sample_asset_data)
    with pytest.raises(HTTPException) as exc_info:
        asset_service.create_asset(sample_asset_data)
    assert exc_info.value.status_code == 400


def test_get_asset_by_id(asset_service, sample_asset_data):
    created = asset_service.create_asset(sample_asset_data)
    fetched = asset_service.get_asset(created.id)
    assert fetched.id == created.id
    assert fetched.value == "example.com"


def test_get_asset_not_found(asset_service):
    import uuid
    with pytest.raises(HTTPException) as exc_info:
        asset_service.get_asset(uuid.uuid4())
    assert exc_info.value.status_code == 404


def test_filter_by_type(asset_service, sample_asset_data, another_asset_data):
    asset_service.create_asset(sample_asset_data)
    asset_service.create_asset(another_asset_data)

    items, total = asset_service.get_assets(filters={"type": "DOMAIN"})
    assert total == 1
    assert items[0].type == "DOMAIN"


def test_filter_by_status(asset_service, sample_asset_data):
    asset_service.create_asset(sample_asset_data)

    items, total = asset_service.get_assets(filters={"status": "ACTIVE"})
    assert total == 1

    items, total = asset_service.get_assets(filters={"status": "INACTIVE"})
    assert total == 0


def test_search_by_value(asset_service, sample_asset_data, another_asset_data):
    asset_service.create_asset(sample_asset_data)
    asset_service.create_asset(another_asset_data)

    items, total = asset_service.get_assets(search="example")
    assert total == 1
    assert "example" in items[0].value


def test_pagination(asset_service):
    for i in range(5):
        asset_service.create_asset(AssetCreate(type="DOMAIN", value=f"page-test-{i}.com"))

    items, total = asset_service.get_assets(page=1, size=2)
    assert total == 5
    assert len(items) == 2

    items_p2, _ = asset_service.get_assets(page=2, size=2)
    assert len(items_p2) == 2
    assert items[0].id != items_p2[0].id


def test_soft_delete_asset(asset_service, sample_asset_data):
    created = asset_service.create_asset(sample_asset_data)
    asset_service.delete_asset(created.id)

    with pytest.raises(HTTPException) as exc_info:
        asset_service.get_asset(created.id)
    assert exc_info.value.status_code == 404
