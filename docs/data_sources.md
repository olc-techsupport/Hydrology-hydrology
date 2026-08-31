# Data sources and release provenance

Every released table, figure, or geospatial file should be traceable to a source notebook and configuration revision.

| Source | Use | Spatial interpretation |
|---|---|---|
| Census TIGER AIANNH | Reproducible Pine Ridge statistical boundary | Not a legal or OST-defined jurisdictional boundary |
| USGS Water Data APIs/NWIS | Streamflow and groundwater monitoring | Sites may be adjacent or hydrologically relevant; verify each location |
| Water Quality Portal | Public water-quality context | Coverage and reporting practices vary by organization and period |
| USGS NHD/WBD | Streams and watershed boundaries | Hydrologic units cross political and territorial boundaries |
| NOAA climate divisions | Historical PDSI | Division 7 is a regional proxy, not a Reservation-specific observation |
| MACAv2-METDATA | Downscaled climate projections | Scenario/model output, not a forecast or local monitoring record |
| Carter and Heakin (2007), USGS SIM 2993 | Historical Pine Ridge/Bennett well inventory | Historical inventory, not current monitoring coverage |

## Required artifact metadata

For every committed release artifact, record:

- generating notebook and git commit;
- source dataset and source URL;
- retrieval date or cached-source date;
- analysis period;
- territorial boundary and hydrologic context used;
- included site IDs and off-boundary rationale;
- units and transformations;
- known missingness and limitations; and
- review status.

Generated outputs are not automatically release artifacts. Notebook execution should write to `outputs/`; maintainers should review the diff and commit only products intended for distribution.
