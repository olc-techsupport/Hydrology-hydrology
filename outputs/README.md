# Generated release candidates

These files were regenerated from the OST/Pine Ridge-scoped notebooks on 2026-08-31 using the configuration committed with the repository. They are screening-level release candidates, not approved OST or OLC findings.

The notebook series was executed in order. Tables, GeoJSON, Parquet outputs, and committed static figures reflect the Pine Ridge configuration. Figures remain screening-level release candidates until their scientific content, labels, accessibility, and governance framing are reviewed.

Key scope-specific artifacts:

- `pine_ridge_census_boundary.geojson` — Census statistical boundary; not a legal boundary determination.
- `pine_ridge_context_streams.geojson` — NHD streams in the configured hydrologic context; not all features are within OST lands.
- `pine_ridge_monitoring_coverage.csv` — screening summary of public groundwater monitoring proximity.
- `pine_ridge_pdsi_division7.csv` — NOAA Division 7 regional drought proxy.

Other tables retain topic-oriented names because their inputs are now controlled by the single Pine Ridge configuration. See `docs/data_sources.md` for required provenance and interpretation metadata before formal release.

`provenance_manifest.csv` records the generating notebook, source keys, period, spatial scope, configuration, regeneration date, and current review status for committed data artifacts. It is a release checklist, not evidence of approval.
