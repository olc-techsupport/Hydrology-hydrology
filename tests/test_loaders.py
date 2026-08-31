from __future__ import annotations

from src.constants import STUDY_AREA_CENSUS_NAMES
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
