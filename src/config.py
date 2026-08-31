from __future__ import annotations

"""Validated access to the OLC Pine Ridge project configuration."""

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT/"config"/"config.yaml"


@lru_cache(maxsize=1)
def load_config(path: str | Path = CONFIG_PATH) -> dict[str, Any]:
    """Load and minimally validate the single project configuration."""
    config_path = Path(path)
    with config_path.open(encoding="utf-8") as stream:
        config = yaml.safe_load(stream)

    required = {
        "project", "study_area", "analysis", "usgs_streamflow_sites",
        "usgs_groundwater_sites", "usgs_wq_sites", "thresholds",
        "stress_index_weights", "paths", "governance",
    }
    missing = sorted(required - set(config or {}))
    if missing:
        raise ValueError(f"Missing config sections: {', '.join(missing)}")

    bbox = config["study_area"]["hydrologic_context_bbox"]
    if len(bbox) != 4 or not (bbox[0] < bbox[2] and bbox[1] < bbox[3]):
        raise ValueError("hydrologic_context_bbox must be [west, south, east, north]")

    weights = config["stress_index_weights"]
    if abs(sum(float(value) for value in weights.values()) - 1.0) > 1e-9:
        raise ValueError("stress_index_weights must sum to 1.0")

    ids = [str(site["id"]) for site in config["usgs_streamflow_sites"]]
    if len(ids) != len(set(ids)):
        raise ValueError("usgs_streamflow_sites contains duplicate IDs")
    if any(not site.get("context") for site in config["usgs_streamflow_sites"]):
        raise ValueError("Every streamflow site needs an inclusion context")
    return config


def streamflow_site_ids(config: dict[str, Any] | None = None) -> list[str]:
    """Return configured USGS streamgage IDs."""
    cfg = config or load_config()
    return [str(site["id"]) for site in cfg["usgs_streamflow_sites"]]


def streamflow_site_names(config: dict[str, Any] | None = None) -> dict[str, str]:
    """Map configured USGS streamgage IDs to display names."""
    cfg = config or load_config()
    return {str(site["id"]): site["name"] for site in cfg["usgs_streamflow_sites"]}
