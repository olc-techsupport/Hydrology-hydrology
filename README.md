# Pine Ridge Hydrology

An educational and reproducible hydrology analysis series developed for the Oglala Lakota College Math and Science Department. The series focuses on the Pine Ridge Reservation and hydrologically relevant adjacent areas.

Developed by: Lilly Jones, PhD, Daear Consulting LLC                                                                               
Developed for: Oglala Lakota College                                                                                            
Funding: This material was developed as part of a project funded by the USDA National Institute of Food and Agriculture (NIFA).                       
Project role: Daear Consulting LLC developed the geospatial code, workflows, documentation, and instructional materials under contract to Oglala Lakota College.                                                                                                                      

License: Apache License 2.0 (code; review of other materials is pending)

## Current status

This repository currently provides seven analysis notebooks and supporting Python modules. It does **not** yet provide an operational monitoring pipeline, dashboard, emergency-alert system, or approved OST management thresholds. Figures and indicators are screening-level educational products unless and until OLC and OST reviewers approve another use.

Specific OST Research Review Board (RRB) and OLC Institutional Review Board (IRB) wording remains under review. Interim review contact:

> Camille Griffith, PhD
>
> Director, OST RRB and OLC IRB
>
> cgriffith@olc.edu

Listing this contact does not indicate approval of the current repository.

## Study scope

The territorial study area is the Pine Ridge Reservation. Hydrologic analyses may include selected upstream, downstream, or nearby sites needed to describe connected watersheds and aquifers. Those sites are documented as context and must not be represented as being within OST lands solely because they occur in the analysis envelope.

All project scope is defined in [`config/config.yaml`](config/config.yaml), including the study-area name, bounding box, dates, climate division, monitoring sites, inclusion rationales, and screening thresholds.

## Notebook series

1. `01_watershed_regional_context.ipynb`: land, watersheds, and monitoring context
2. `02_groundwater_monitoring.ipynb`: groundwater systems and monitoring gaps
3. `03_surface_water_reliability.ipynb`: White River and tributary flow reliability
4. `04_water_quality_context.ipynb`: public water-quality monitoring context
5. `05_drought_water_stress.ipynb`: drought history and water stress
6. `06_compound_water_stress_index.ipynb`: screening-level compound indicator
7. `07_climate_projections_water.ipynb`: climate projections and implications

The notebooks are ordered and may consume outputs produced by earlier notebooks.

## Setup

```powershell
conda env create -f environment.yml
conda activate tribal-water
python -m ipykernel install --user --name tribal-water --display-name "Python (tribal-water)"
jupyter lab notebooks/
```

Run the notebooks from 01 through 07. Public downloads are cached under `data/cache/`, which is excluded from version control.

For an automated non-visual validation of the complete data path, run:

```powershell
python scripts/execute_notebooks.py
```

Pass `--include-plots` to execute visualization cells as well. The default skips plot cells so native geospatial rendering differences do not prevent validation of data loading, analysis, and table exports.

## Data and generated products

Public sources include USGS water data, the Water Quality Portal, Census TIGER AIANNH boundaries, the National Hydrography Dataset, the Watershed Boundary Dataset, NOAA climate-division drought data, and MACAv2 climate projections.

Public source data are cached locally. Selected generated tables and figures may be committed to `outputs/` when they are deliberate release artifacts. Every released artifact should identify its source notebook, analysis period, spatial scope, and limitations. Cached downloads and any locally held OST operational data must not be committed.

No OST-collected operational dataset is included in this repository. Adding such data requires an approved governance, storage, access, and publication process.

## Interpretation limits

- Census AIANNH geometry is used for reproducible statistical mapping; it is not a legal determination of jurisdiction or a substitute for OST-defined lands.
- A public monitoring gap is not evidence that water or water use is absent.
- Off-boundary sites provide hydrologic context and are not automatically OST sites.
- Default thresholds are transparent screening values, not approved operational, regulatory, health, or emergency triggers.
- Results require scientific and OLC/OST governance review before external use.

See [`docs/data_sovereignty.md`](docs/data_sovereignty.md) for the draft data governance statement and [`docs/data_sources.md`](docs/data_sources.md) for source and product provenance expectations.

## Deferred items

- Final OST RRB/OLC IRB language and review status
- Confirmation of locally appropriate governance frameworks and terminology
- `CITATION.cff`, author order, institutional attribution, and NIFA award details
- A dependency lock file after the analysis environment is finalized
