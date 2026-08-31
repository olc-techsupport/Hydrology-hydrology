from __future__ import annotations

from src.config import load_config, streamflow_site_ids, streamflow_site_names


def test_project_scope_is_pine_ridge_only() -> None:
    config = load_config()
    assert config["study_area"]["nation"] == "Oglala Sioux Tribe"
    assert config["study_area"]["census_boundary_name"] == "Pine Ridge"
    assert config["study_area"]["climate_division"] == 7
    assert "secondary" not in config["study_area"]


def test_streamgages_have_unique_ids_and_context() -> None:
    config = load_config()
    ids = streamflow_site_ids(config)
    assert len(ids) == len(set(ids))
    assert all(site["context"].strip() for site in config["usgs_streamflow_sites"])
    assert set(streamflow_site_names(config)) == set(ids)


def test_screening_weights_sum_to_one() -> None:
    weights = load_config()["stress_index_weights"]
    assert sum(weights.values()) == 1.0


def test_governance_review_is_not_claimed_complete() -> None:
    project = load_config()["project"]
    assert "pending" in project["governance_status"].lower()
    assert project["governance_contact"]["email"] == "cgriffith@olc.edu"
