from __future__ import annotations

"""
Stable technical constants for the OLC Pine Ridge hydrology series.

Project scope, sites, dates, thresholds, and institutional language live in
config/config.yaml. This module contains only paths, APIs, field schemas, and
other technical constants.
"""

from pathlib import Path

# Repository root
REPO_ROOT = Path(__file__).resolve().parents[1]

# Coordinate reference systems (CRS)
CRS_GEOGRAPHIC = "EPSG:4326"   # WGS84 lat/lon for all spatial data
CRS_PROJECTED  = "EPSG:5070"   # Albers Equal Area CONUS for area calculations

# Data directories
CACHE_DIR     = REPO_ROOT/"data"/"cache"
RAW_DIR       = REPO_ROOT/"data"/"raw"
PROCESSED_DIR = REPO_ROOT/"data"/"processed"
TEMPLATE_DIR  = REPO_ROOT/"data"/"templates"
OUTPUTS_DIR   = REPO_ROOT/"outputs"
FIGURES_DIR   = OUTPUTS_DIR/"figures"

for _d in [CACHE_DIR, PROCESSED_DIR, OUTPUTS_DIR, FIGURES_DIR]:
    _d.mkdir(parents=True, exist_ok=True)

# API base URLs
USGS_NWIS_BASE      = "https://waterservices.usgs.gov/nwis"
USGS_NWIS_SITE_URL  = f"{USGS_NWIS_BASE}/site/"
USGS_NWIS_DV_URL    = f"{USGS_NWIS_BASE}/dv/"         # daily values
# The legacy ``gwlevels`` service was decommissioned in 2026.  New
# groundwater work uses the Water Data APIs below.
USGS_NWIS_GWL_URL   = f"{USGS_NWIS_BASE}/gwlevels/"   # legacy; do not use for new code
USGS_NWIS_WQ_URL    = "https://www.waterqualitydata.us/data/Result/search/"
USGS_WATERDATA_OGC_BASE = "https://api.waterdata.usgs.gov/ogcapi/v0/collections"
USGS_MONITORING_LOCATIONS_URL = f"{USGS_WATERDATA_OGC_BASE}/monitoring-locations/items"
USGS_FIELD_MEASUREMENTS_URL   = f"{USGS_WATERDATA_OGC_BASE}/field-measurements/items"
CARTER_2007_INVENTORY_URL = "https://pubs.usgs.gov/sim/2993/includes/sim2993_data.xls"
CENSUS_TIGER_BASE   = "https://www2.census.gov/geo/tiger"
NHD_FLOWLINE_URL    = "https://hydro.nationalmap.gov/arcgis/rest/services/NHDPlus_HR/MapServer/3/query"
WBD_HUC8_URL        = "https://hydro.nationalmap.gov/arcgis/rest/services/NHDPlus_HR/MapServer/12/query"
NOAA_DROUGHT_BASE   = "https://www.ncei.noaa.gov/pub/data/cirs/climdiv"
MACA_THREDDS_BASE   = "http://thredds.northwestknowledge.net:8080/thredds/dodsC/agg_macav2metdata_"

# Exact Census TIGER AIANNH name and project display name.
STUDY_AREA_CENSUS_NAMES = ["Pine Ridge"]
CENSUS_TO_COMMON = {
    "Pine Ridge": "Oglala Lakota",
}
COMMON_TO_CENSUS = {v: k for k, v in CENSUS_TO_COMMON.items()}

# USGS NWIS parameter codes
# Used when requesting specific variables from the NWIS API
NWIS_PARAMS = {
    "streamflow_cfs":     "00060",   # Discharge (cfs)
    "stage_ft":           "00065",   # Gage height (ft)
    "gw_depth_ft":        "72019",   # Depth to water level below land surface (ft)
    "gw_elev_ft":         "72020",   # Water level elevation above NGVD (ft)
    "temp_c":             "00010",   # Water temperature (°C)
    "do_mgl":             "00300",   # Dissolved oxygen (mg/L)
    "ph":                 "00400",   # pH
    "specific_cond":      "00095",   # Specific conductance (µS/cm at 25°C)
    "turbidity_fnu":      "63680",   # Turbidity (FNU)
    "nitrate_mgl":        "00618",   # Nitrate (mg/L as N)
    "tds_mgl":            "70300",   # Total dissolved solids (mg/L)
}

# Groundwater field names (must match Excel template)
GW_TEMPLATE_FIELDS = [
    "well_id",
    "date",
    "water_level_ft",
    "measurement_method",
    "entered_by",
    "notes",
]

# Optional GW fields (add when available)
GW_OPTIONAL_FIELDS = [
    "lat",
    "lon",
    "aquifer",
    "well_depth_ft",
    "casing_diameter_in",
]

# Water quality field names (must match Excel template)
WQ_TEMPLATE_FIELDS = [
    "site_id",
    "date",
    "sample_type",    # tap, spring, well, stream
    "nitrate_mgl",
    "ph",
    "tds_mgl",
    "turbidity_ntu",
    "arsenic_ugl",
    "fluoride_mgl",
    "entered_by",
    "notes",
]

# Data sovereignty references
GOVERNANCE_REFS = {
    "ocap":     "https://fnigc.ca/ocap-training/",
    "care":     "https://www.gida-global.org/care",
    "fair":     "https://www.go-fair.org/fair-principles/",
    "ieee_2890":"https://standards.ieee.org/ieee/2890/10318/",
    "local_contexts": "https://localcontexts.org/",
}
