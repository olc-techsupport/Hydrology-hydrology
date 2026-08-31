# Generated release candidates

These files were regenerated from the OST/Pine Ridge-scoped notebooks on 2026-08-31 using the configuration committed with the repository. They are screening-level release candidates, not approved OST or OLC findings.

The notebook series was executed in order with visualization cells skipped during portable validation. Tables, GeoJSON, and Parquet outputs reflect the Pine Ridge configuration. Former Rosebud and statewide products were removed. Static figures remain uncommitted until the native Windows plotting environment and the visual content are reviewed.

Key scope-specific artifacts:

- `pine_ridge_census_boundary.geojson` — Census statistical boundary; not a legal boundary determination.
- `pine_ridge_context_streams.geojson` — NHD streams in the configured hydrologic context; not all features are within OST lands.
- `pine_ridge_monitoring_coverage.csv` — screening summary of public groundwater monitoring proximity.
- `pine_ridge_pdsi_division7.csv` — NOAA Division 7 regional drought proxy.

Other tables retain topic-oriented names because their inputs are now controlled by the single Pine Ridge configuration. See `docs/data_sources.md` for required provenance and interpretation metadata before formal release.
