from __future__ import annotations

from src.constants import STUDY_AREA_CENSUS_NAMES
from pathlib import Path

import src.loaders as loaders
from src.loaders import _bbox_tiles


def test_default_boundary_scope_is_single_study_area() -> None:
    assert STUDY_AREA_CENSUS_NAMES == ["Pine Ridge"]


def test_bbox_tiling_rejects_invalid_extent() -> None:
    try:
        _bbox_tiles((-101.0, 43.0, -102.0, 42.0), 4.0)
    except ValueError:
        pass
    else:
        raise AssertionError("invalid bbox should raise ValueError")


class FakeResponse:
    def __init__(self, payload: dict, status_code: int = 200) -> None:
        self.payload = payload
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def json(self) -> dict:
        return self.payload


def feature(objectid: int) -> dict:
    return {
        "type": "Feature",
        "id": objectid,
        "properties": {"objectid": objectid, "reachcode": str(objectid)},
        "geometry": {
            "type": "LineString",
            "coordinates": [[-102.0, 43.0], [-101.9, 43.1]],
        },
    }


def test_nhd_loader_fetches_every_page(monkeypatch, tmp_path: Path) -> None:
    pages = {
        0: {"features": [feature(i) for i in range(2_000)], "exceededTransferLimit": True},
        2_000: {"features": [feature(i) for i in range(2_000, 2_125)]},
    }
    offsets: list[int] = []

    def fake_get(url, params, timeout):
        offsets.append(params["resultOffset"])
        return FakeResponse(pages[params["resultOffset"]])

    monkeypatch.setattr(loaders, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(loaders.requests, "get", fake_get)

    result = loaders.load_nhd_flowlines((-103.5, 42.5, -103.1, 42.8))

    assert offsets == [0, 2_000]
    assert len(result) == 2_125
    assert (tmp_path / "nhd_-103.50_42.50_-103.10_42.80_o1_v2.geojson").exists()


def test_nhd_loader_checks_after_an_exact_page_without_flag(monkeypatch, tmp_path: Path) -> None:
    pages = {
        0: {"features": [feature(i) for i in range(2_000)]},
        2_000: {"features": []},
    }
    offsets: list[int] = []

    def fake_get(url, params, timeout):
        offsets.append(params["resultOffset"])
        return FakeResponse(pages[params["resultOffset"]])

    monkeypatch.setattr(loaders, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(loaders.requests, "get", fake_get)

    result = loaders.load_nhd_flowlines((-103.5, 42.5, -103.1, 42.8))

    assert offsets == [0, 2_000]
    assert len(result) == 2_000


def test_nhd_loader_does_not_cache_repeated_pages(monkeypatch, tmp_path: Path) -> None:
    repeated = {"features": [feature(i) for i in range(2_000)], "exceededTransferLimit": True}

    monkeypatch.setattr(loaders, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(
        loaders.requests,
        "get",
        lambda url, params, timeout: FakeResponse(repeated),
    )

    try:
        loaders.load_nhd_flowlines((-103.5, 42.5, -103.1, 42.8))
    except RuntimeError as error:
        assert "repeated page" in str(error)
    else:
        raise AssertionError("repeated pages must fail")

    assert not (tmp_path / "nhd_-103.50_42.50_-103.10_42.80_o1_v2.geojson").exists()


def test_nhd_loader_tiles_large_bbox_and_deduplicates_edges(monkeypatch, tmp_path: Path) -> None:
    queried_tiles: list[str] = []

    def fake_get(url, params, timeout):
        queried_tiles.append(params["geometry"])
        tile_id = len(queried_tiles)
        # Object 1 appears in every tile as a feature crossing tile boundaries.
        return FakeResponse({"features": [feature(1), feature(tile_id + 1)]})

    monkeypatch.setattr(loaders, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(loaders.requests, "get", fake_get)

    result = loaders.load_nhd_flowlines((-103.5, 42.5, -102.6, 43.2))

    assert len(queried_tiles) == 4
    assert result["objectid"].nunique() == 5
