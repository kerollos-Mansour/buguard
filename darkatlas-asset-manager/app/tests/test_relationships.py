import pytest
from fastapi import HTTPException

from app.schemas.asset import AssetCreate
from app.schemas.relationship import RelationshipCreate


def _create_asset(asset_service, type_, value):
    return asset_service.create_asset(AssetCreate(type=type_, value=value))


def test_create_relationship_success(asset_service, relationship_service):
    source = _create_asset(asset_service, "DOMAIN", "source.com")
    target = _create_asset(asset_service, "IP_ADDRESS", "1.1.1.1")

    rel = relationship_service.create_relationship(
        RelationshipCreate(
            source_asset_id=source.id,
            target_asset_id=target.id,
            relationship_type="RESOLVES_TO"
        )
    )

    assert rel.source_asset_id == source.id
    assert rel.target_asset_id == target.id
    assert rel.relationship_type == "RESOLVES_TO"


def test_self_relationship_raises_error(asset_service, relationship_service):
    asset = _create_asset(asset_service, "DOMAIN", "self.com")

    with pytest.raises(HTTPException) as exc_info:
        relationship_service.create_relationship(
            RelationshipCreate(
                source_asset_id=asset.id,
                target_asset_id=asset.id,
                relationship_type="RESOLVES_TO"
            )
        )
    assert exc_info.value.status_code == 400


def test_relationship_with_missing_source_raises_error(asset_service, relationship_service):
    import uuid
    target = _create_asset(asset_service, "IP_ADDRESS", "2.2.2.2")

    with pytest.raises(HTTPException) as exc_info:
        relationship_service.create_relationship(
            RelationshipCreate(
                source_asset_id=uuid.uuid4(),
                target_asset_id=target.id,
                relationship_type="RESOLVES_TO"
            )
        )
    assert exc_info.value.status_code == 404


def test_duplicate_relationship_is_idempotent(asset_service, relationship_service):
    source = _create_asset(asset_service, "DOMAIN", "idem-source.com")
    target = _create_asset(asset_service, "IP_ADDRESS", "3.3.3.3")

    rel_data = RelationshipCreate(
        source_asset_id=source.id,
        target_asset_id=target.id,
        relationship_type="RESOLVES_TO"
    )

    rel1 = relationship_service.create_relationship(rel_data)
    rel2 = relationship_service.create_relationship(rel_data)
    assert rel1.id == rel2.id


def test_get_asset_relationships(asset_service, relationship_service):
    source = _create_asset(asset_service, "DOMAIN", "rel-source.com")
    target = _create_asset(asset_service, "IP_ADDRESS", "4.4.4.4")

    relationship_service.create_relationship(
        RelationshipCreate(
            source_asset_id=source.id,
            target_asset_id=target.id,
            relationship_type="RESOLVES_TO"
        )
    )

    result = relationship_service.get_asset_relationships(source.id)
    assert result["outgoing"]["total"] == 1
    assert result["incoming"]["total"] == 0


def test_get_asset_graph_includes_nodes_and_edges(asset_service, relationship_service):
    source = _create_asset(asset_service, "DOMAIN", "graph-source.com")
    target = _create_asset(asset_service, "IP_ADDRESS", "5.5.5.5")

    relationship_service.create_relationship(
        RelationshipCreate(
            source_asset_id=source.id,
            target_asset_id=target.id,
            relationship_type="RESOLVES_TO"
        )
    )

    graph = relationship_service.get_asset_graph(source.id, depth=2)
    node_ids = [n.id for n in graph["nodes"]]

    assert source.id in node_ids
    assert target.id in node_ids
    assert len(graph["edges"]) >= 1


def test_get_relationships_for_missing_asset(relationship_service):
    import uuid
    with pytest.raises(HTTPException) as exc_info:
        relationship_service.get_asset_relationships(uuid.uuid4())
    assert exc_info.value.status_code == 404
