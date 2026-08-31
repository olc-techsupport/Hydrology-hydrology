from __future__ import annotations

"""
loaders.py public data loaders for tribal_water_monitoring.

All functions follow the same pattern:
  - Check cache first, download only if needed
  - force_refresh=True to re-download
  - Return clean GeoDataFrame or DataFrame
  - Treat missing/sparse data as a policy finding, not an error

Data sources:
  USGS NWIS     : streamflow, groundwater levels, water quality
  Census TIGER  : AIANNH Tribal boundaries
  USGS NHD      : stream network
  USGS WBD      : watershed (HUC) boundaries
  NOAA          : PDSI drought index
"""

import io
import json
import logging
import warnings
import zipfile
import tempfile
from pathlib import Path
from typing import Optional

import geopandas as gpd
import numpy as np
import pandas as pd
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from src.constants import (
    CACHE_DIR,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    CENSUS_TIGER_BASE,
    USGS_NWIS_SITE_URL,
    USGS_NWIS_DV_URL,
    USGS_NWIS_GWL_URL,
    USGS_NWIS_WQ_URL,
    USGS_MONITORING_LOCATIONS_URL,
    USGS_FIELD_MEASUREMENTS_URL,
    CARTER_2007_INVENTORY_URL,
    NHD_FLOWLINE_URL,
    WBD_HUC8_URL,
    NOAA_DROUGHT_BASE,
    OCETI_SAKOWIN_CENSUS_NAMES,
    CENSUS_TO_COMMON,
    NWIS_PARAMS,
)

log = logging.getLogger(__name__)

_retry = retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True,
)


# Tribal boundaries

def load_tribal_boundaries(
    nation_names: list[str] | None = None,
    force_refresh: bool = False,
) -> gpd.GeoDataFrame:
    """
    Load AIANNH Tribal boundaries from Census TIGER.

    Parameters
    nation_names  : Census NAME field values to filter.
                    Defaults to all eight Oceti Sakowin Nations.
    force_refresh : Re-download even if cached.

    Returns
    GeoDataFrame with columns: NAME, common_name, area_km2, geometry
    """
    if nation_names is None:
        nation_names = OCETI_SAKOWIN_CENSUS_NAMES

    cache_path = CACHE_DIR/"tl_2023_us_aiannh.geojson"

    if not cache_path.exists() or force_refresh:
        log.info("Downloading Census TIGER AIANNH boundaries...")
        url = f"{CENSUS_TIGER_BASE}/TIGER2023/AIANNH/tl_2023_us_aiannh.zip"
        r   = requests.get(url, timeout=300)
        r.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            with tempfile.TemporaryDirectory() as tmp:
                z.extractall(tmp)
                shp = next(Path(tmp).glob("*.shp"))
                all_aiannh = gpd.read_file(shp).to_crs(CRS_GEOGRAPHIC)
        all_aiannh.to_file(cache_path, driver="GeoJSON")
        log.info("AIANNH cached: %d features", len(all_aiannh))
    else:
        all_aiannh = gpd.read_file(cache_path)

    from shapely.validation import make_valid

    gdf = all_aiannh[all_aiannh["NAME"].isin(nation_names)].copy()
    gdf = gdf.dissolve(by="NAME", as_index=False)
    gdf["geometry"]    = gdf.geometry.apply(make_valid)
    gdf["common_name"] = gdf["NAME"].map(CENSUS_TO_COMMON)
    gdf["area_km2"]    = gdf.to_crs(CRS_PROJECTED).geometry.area / 1e6

    return gdf.reset_index(drop=True)


# USGS NWIS streamflow

@_retry
def load_streamflow(
    site_ids: list[str],
    start_date: str = "2000-01-01",
    end_date: str   = "2024-12-31",
    force_refresh: bool = False,
) -> pd.DataFrame:
    """
    Load daily mean streamflow from USGS NWIS (RDB format).

    Parameters
    site_ids    : List of USGS site IDs (e.g. ['06447000'])
    start_date  : Start date string 'YYYY-MM-DD'
    end_date    : End date string 'YYYY-MM-DD'

    Returns
    DataFrame with columns: site_no, datetime, flow_cfs
    """
    param_code = NWIS_PARAMS["streamflow_cfs"]
    cache_key  = f"nwis_flow_{'_'.join(sorted(site_ids))}_{start_date[:4]}_{end_date[:4]}.csv"
    cache_file = CACHE_DIR / cache_key

    if cache_file.exists() and not force_refresh:
        df = pd.read_csv(cache_file, parse_dates=["datetime"])
        log.info("Streamflow loaded from cache: %d records", len(df))
        return df

    sites_str = ",".join(site_ids)
    r = requests.get(
        USGS_NWIS_DV_URL,
        params={
            "format":      "rdb",
            "sites":        sites_str,
            "startDT":      start_date,
            "endDT":        end_date,
            "parameterCd":  param_code,
            "statCd":       "00003",   # daily mean
        },
        timeout=120,
    )
    r.raise_for_status()

    records = _parse_nwis_rdb(r.text, value_col=f"{param_code}_00003_va",
                           value_name="flow_cfs") 
    df = pd.DataFrame(records)
    if df.empty:
        warnings.warn(
            f"No streamflow data returned for sites {site_ids}. "
            "USGS gauge coverage may be sparse near Tribal lands, "
            "this is a monitoring gap, not a data error.",
            UserWarning,
            stacklevel=2,
        )
        return df

    df["datetime"] = pd.to_datetime(df["datetime"])
    df.to_csv(cache_file, index=False)
    log.info("Streamflow downloaded and cached: %d records", len(df))
    return df


# USGS NWIS groundwater levels

def load_usgs_groundwater_sites(
    bbox: tuple[float, float, float, float],
    force_refresh: bool = False,
) -> gpd.GeoDataFrame:
    """
    Fetch USGS groundwater monitoring well sites within a bounding box.

    Uses USGS's modern Water Data API, not the retired NWIS site endpoint.
    A monitoring site is not a complete inventory of water wells; use
    :func:`load_carter_2007_inventory` for the historical Pine Ridge/Bennett
    inventory.

    Parameters
    bbox : (min_lon, min_lat, max_lon, max_lat)

    Returns
    GeoDataFrame of USGS monitoring well sites.
    Note: Coverage is systematically sparse on Tribal lands. Document gaps
    as a policy finding.
    """
    bbox_str   = f"{bbox[0]:.2f}_{bbox[1]:.2f}_{bbox[2]:.2f}_{bbox[3]:.2f}"
    cache_file = CACHE_DIR / f"usgs_gw_sites_{bbox_str}_v2.geojson"

    if cache_file.exists() and not force_refresh:
        return gpd.read_file(cache_file).to_crs(CRS_GEOGRAPHIC)
    else:
        try:
            features = []
            # Tiling keeps queries predictable and avoids legacy API size limits.
            for tile in _bbox_tiles(bbox, max_span_degrees=4.0):
                features.extend(_get_usgs_ogc_features(
                    USGS_MONITORING_LOCATIONS_URL,
                    {"bbox": ",".join(map(str, tile)), "site_type_code": "GW"},
                ))
        except Exception as e:
            raise RuntimeError(
                "USGS groundwater-site discovery failed; do not interpret this "
                "as a monitoring gap."
            ) from e

    if not features:
        warnings.warn(
            "USGS returned no groundwater monitoring sites for this area. This "
            "does not represent a complete inventory of water wells.",
            UserWarning, stacklevel=2,
        )
        return gpd.GeoDataFrame()

    records = []
    for feature in features:
        props = feature.get("properties", {})
        coords = (feature.get("geometry") or {}).get("coordinates", [None, None])
        site_id = props.get("monitoring_location_number") or props.get("id", "")
        records.append({
            "site_no": str(site_id).replace("USGS-", ""),
            "monitoring_location_id": props.get("id", f"USGS-{site_id}"),
            "station_nm": props.get("monitoring_location_name"),
            "site_tp_cd": props.get("site_type_code"),
            "dec_long_va": coords[0], "dec_lat_va": coords[1],
            "aquifer_code": props.get("aquifer_code"),
            "well_depth_ft": props.get("well_constructed_depth"),
        })
    df = pd.DataFrame(records).drop_duplicates(subset=["monitoring_location_id"])
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df["dec_long_va"], df["dec_lat_va"]),
        crs=CRS_GEOGRAPHIC,
    )
    gdf.to_file(cache_file, driver="GeoJSON")
    return gdf


@_retry
def load_usgs_groundwater_levels(
    site_no: str,
    start_date: str = "1980-01-01",
    force_refresh: bool = False,
) -> pd.DataFrame:
    """
    Load discrete groundwater level measurements for one USGS well.

    Uses the USGS modern ``field-measurements`` API.  The legacy ``gwlevels``
    endpoint was decommissioned in February 2026.

    Returns
    DataFrame with columns: site_no, date, water_level_ft
    """
    cache_file = CACHE_DIR/f"gwl_{site_no}.csv"

    if cache_file.exists() and not force_refresh:
        df = pd.read_csv(cache_file, parse_dates=["date"])
        return df

    location_id = site_no if str(site_no).startswith("USGS-") else f"USGS-{site_no}"
    features = _get_usgs_ogc_features(
        USGS_FIELD_MEASUREMENTS_URL,
        {
            "monitoring_location_id": location_id,
            "parameter_code": NWIS_PARAMS["gw_depth_ft"],
            "datetime": f"{start_date}/..",
        },
    )
    df = pd.DataFrame([f.get("properties", {}) for f in features])
    if df.empty:
        return pd.DataFrame(columns=["site_no", "date", "water_level_ft"])

    df["date"] = pd.to_datetime(df["time"], errors="coerce")
    df["water_level_ft"] = pd.to_numeric(df["value"], errors="coerce")
    df["site_no"] = str(site_no).replace("USGS-", "")

    result = (
        df[["site_no", "date", "water_level_ft"]]
        .dropna(subset=["date", "water_level_ft"])
        .reset_index(drop=True)
    )
    result.to_csv(cache_file, index=False)
    return result


def load_carter_2007_inventory(
    force_refresh: bool = False,
) -> gpd.GeoDataFrame:
    """Load Carter and Heakin (2007) Pine Ridge/Bennett well inventory.

    This is a historical inventory, not an indication of current monitoring or
    current water-level observations.  Its provenance is retained in every row.
    """
    cache_file = CACHE_DIR/"carter_2007_pine_ridge_inventory.xls"
    if not cache_file.exists() or force_refresh:
        response = requests.get(CARTER_2007_INVENTORY_URL, timeout=120)
        response.raise_for_status()
        cache_file.write_bytes(response.content)

    sheets = pd.read_excel(cache_file, sheet_name=None, header=2)
    frames = []
    for sheet_name, frame in sheets.items():
        # Table 3 is the individual water-level record.  Tables 1 and 2 are
        # the well inventory tables, so avoid turning every measurement into a
        # duplicate inventory feature.
        if sheet_name == "All observation well data":
            continue
        frame.columns = [str(c).strip().lower().replace(" ", "_") for c in frame.columns]
        lon = next((c for c in frame if c.startswith("longitude")), None)
        lat = next((c for c in frame if c.startswith("latitude")), None)
        if lon and lat:
            subset = frame.copy()
            subset["dec_long_va"] = subset[lon].map(_dms_to_decimal_degrees)
            subset["dec_long_va"] = -subset["dec_long_va"].abs()
            subset["dec_lat_va"] = subset[lat].map(_dms_to_decimal_degrees)
            if "site_identification_number" in subset.columns:
                subset = subset.rename(columns={"site_identification_number": "site_no"})
            subset = subset.dropna(subset=["dec_long_va", "dec_lat_va"])
            subset["inventory_class"] = sheet_name
            frames.append(subset)
    if not frames:
        raise ValueError("Carter 2007 workbook contains no sheets with decimal latitude/longitude columns.")

    inventory = pd.concat(frames, ignore_index=True)
    if "site_no" in inventory.columns:
        inventory = inventory.drop_duplicates(subset=["site_no"])
    inventory["data_source"] = "USGS SIM 2993 supplemental data"
    inventory["source_year"] = 2007
    inventory["is_monitoring_site"] = False
    # Carter and Heakin specify NAD 27, not WGS84.  Transform precisely before
    # returning the project's standard WGS84 geometry.
    return gpd.GeoDataFrame(
        inventory,
        geometry=gpd.points_from_xy(inventory["dec_long_va"], inventory["dec_lat_va"]),
        crs="EPSG:4267",
    ).to_crs(CRS_GEOGRAPHIC)


# USGS/EPA Water Quality Portal

@_retry
def load_water_quality(
    bbox: tuple[float, float, float, float],
    start_date: str = "2000-01-01",
    characteristics: list[str] | None = None,
    force_refresh: bool = False,
) -> pd.DataFrame:
    """
    Load water quality data from the USGS/EPA Water Quality Portal.

    Parameters
    bbox            : (min_lon, min_lat, max_lon, max_lat)
    start_date      : Earliest sample date
    characteristics : List of parameter names to retrieve.
                      Defaults to key drinking water parameters.
    """
    if characteristics is None:
        characteristics = [
            "Nitrate", "pH", "Total dissolved solids",
            "Turbidity", "Arsenic", "Fluoride",
        ]

    cache_key  = (
        f"wq_{bbox[0]:.1f}_{bbox[1]:.1f}_{bbox[2]:.1f}_{bbox[3]:.1f}"
        f"_{start_date[:4]}.csv"
    )
    cache_file = CACHE_DIR / cache_key

    if cache_file.exists() and not force_refresh:
        df = pd.read_csv(cache_file, low_memory=False)
        if "ActivityStartDate" in df.columns:
            df["ActivityStartDate"] = pd.to_datetime(
                df["ActivityStartDate"], errors="coerce"
            )
        log.info("Water quality loaded from cache: %d records", len(df))
        return df

    # WQP REST API service is part of the URL path, not a query param
    # https://www.waterqualitydata.us/data/Result/search/
    url = "https://www.waterqualitydata.us/data/Result/search/"

    from datetime import datetime
    start_dt     = datetime.strptime(start_date, "%Y-%m-%d")
    start_wqp    = start_dt.strftime("%m-%d-%Y")   # MM-dd-yyyy

    params = {
        "bBox":               f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}",
        "startDateLo":        start_wqp,
        "characteristicName": characteristics,      # pass list directly
        "mimeType":           "csv",
        "dataProfile":        "narrowResult",
}

    try:
        r = requests.get(url, params=params, timeout=180)
        r.raise_for_status()
    except requests.HTTPError as e:
        warnings.warn(
            f"WQP request failed ({e}). "
            "Public water quality monitoring is sparse on Tribal lands: "
            "this absence is a monitoring equity finding.",
            UserWarning, stacklevel=2,
        )
        return pd.DataFrame()

    if not r.content or len(r.content) < 100:
        warnings.warn(
            "WQP returned empty response for this bounding box. "
            "Public water quality monitoring coverage on Tribal lands is sparse.",
            UserWarning, stacklevel=2,
        )
        return pd.DataFrame()

    df = pd.read_csv(io.StringIO(r.text), dtype=str, low_memory=False)

    if df.empty:
        return df

    if "ActivityStartDate" in df.columns:
        df["ActivityStartDate"] = pd.to_datetime(
            df["ActivityStartDate"], errors="coerce"
        )
    if "ResultMeasureValue" in df.columns:
        df["result_value"] = pd.to_numeric(
            df["ResultMeasureValue"], errors="coerce"
        )

    df.to_csv(cache_file, index=False)
    log.info("Water quality downloaded and cached: %d records", len(df))
    return df


# NHD stream flowlines

@_retry
def load_nhd_flowlines(
    bbox: tuple[float, float, float, float],
    min_stream_order: int = 1,
    force_refresh: bool = False,
) -> gpd.GeoDataFrame:
    """
    Load NHDPlus HR stream network flowlines within a bounding box.

    Parameters
    bbox             : (min_lon, min_lat, max_lon, max_lat)
    min_stream_order : Minimum Strahler stream order (1 = all streams)
    """
    cache_key  = f"nhd_{bbox[0]:.2f}_{bbox[1]:.2f}_{bbox[2]:.2f}_{bbox[3]:.2f}_o{min_stream_order}.geojson"
    cache_file = CACHE_DIR / cache_key

    if cache_file.exists() and not force_refresh:
        return gpd.read_file(cache_file)

    where = f"streamorde >= {min_stream_order}" if min_stream_order > 0 else "1=1"

    r = requests.get(
        NHD_FLOWLINE_URL,
        params={
            "where":          where,
            "outFields":      "reachcode,gnis_name,streamorde,lengthkm",
            "f":              "geojson",
            "returnGeometry": "true",
            "outSR":          "4326",
            "geometry":       f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}",
            "geometryType":   "esriGeometryEnvelope",
            "spatialRel":     "esriSpatialRelIntersects",
            "inSR":           "4326",
        },
        timeout=120,
    )

    # 500 = no data in area (i.e. no perennial streams mapped)
    if r.status_code == 500:
        log.info("NHD returned 500 for bbox %s likely no mapped streams", bbox)
        return gpd.GeoDataFrame()

    r.raise_for_status()

    gdf = gpd.read_file(io.BytesIO(r.content))
    if not gdf.empty:
        gdf = gdf.set_crs(CRS_GEOGRAPHIC, allow_override=True)
        gdf.to_file(cache_file, driver="GeoJSON")

    return gdf


# WBD HUC boundaries

@_retry
def load_huc_boundary(
    bbox: tuple[float, float, float, float],
    huc_level: int = 8,
    force_refresh: bool = False,
) -> gpd.GeoDataFrame:
    """
    Load USGS Watershed Boundary Dataset (WBD) HUC polygons.

    Note: HUC boundaries are hydrologically defined, they do not align
    with Tribal territorial boundaries. Always overlay with Tribal boundaries
    for context.

    Parameters
    bbox      : (min_lon, min_lat, max_lon, max_lat)
    huc_level : HUC level (8, 10, or 12). Default 8.
    """
    cache_key  = f"wbd_huc{huc_level}_{bbox[0]:.2f}_{bbox[1]:.2f}_{bbox[2]:.2f}_{bbox[3]:.2f}.geojson"
    cache_file = CACHE_DIR / cache_key

    if cache_file.exists() and not force_refresh:
        return gpd.read_file(cache_file)

    # WBD service layer IDs (wbd/MapServer is separate from NHDPlus_HR):
    # 0=WBDLine, 1=HUC2, 2=HUC4, 3=HUC6, 4=HUC8, 5=HUC10, 6=HUC12
    layer_map = {2: 1, 4: 2, 6: 3, 8: 4, 10: 5, 12: 6}
    layer_id  = layer_map.get(huc_level, 4)  # default HUC-8
    url = f"https://hydro.nationalmap.gov/arcgis/rest/services/wbd/MapServer/{layer_id}/query"

    r = requests.get(
        url,
        params={
            "where":          "1=1",
            "outFields":      f"huc{huc_level},name,areasqkm",
            "f":              "geojson",
            "returnGeometry": "true",
            "outSR":          "4326",
            "geometry":       f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}",
            "geometryType":   "esriGeometryEnvelope",
            "spatialRel":     "esriSpatialRelIntersects",
            "inSR":           "4326",
        },
        timeout=120,
    )

    if r.status_code == 500:
        log.info("WBD returned 500 for bbox %s", bbox)
        return gpd.GeoDataFrame()

    r.raise_for_status()

    # Validate JSON before passing to geopandas or endpoint may return
    # an error object or empty result that pyogrio cannot parse
    try:
        payload = r.json()
    except Exception:
        log.warning("WBD response is not valid JSON for bbox %s", bbox)
        return gpd.GeoDataFrame()

    if payload.get("error"):
        log.warning("WBD API error for bbox %s: %s", bbox, payload["error"])
        return gpd.GeoDataFrame()

    features = payload.get("features", [])
    if not features:
        log.info("WBD returned 0 features for bbox %s", bbox)
        return gpd.GeoDataFrame()

    gdf = gpd.read_file(io.BytesIO(r.content))
    if not gdf.empty:
        gdf = gdf.set_crs(CRS_GEOGRAPHIC, allow_override=True)
        gdf.to_file(cache_file, driver="GeoJSON")

    return gdf


# NOAA PDSI

def load_pdsi(
    state_code: str = "39",
    start_year: int = 1895,
    end_year:   int = 2024,
    force_refresh: bool = False,
) -> pd.DataFrame:
    """
    Load NOAA Climate Division PDSI (Palmer Drought Severity Index).

    South Dakota state code: 39
    Climate divisions 1–9 cover the state.

    Returns
    DataFrame with columns: division, year, month, date, pdsi
    """
    cache_file = CACHE_DIR/"noaa_pdsi_climdiv.txt"

    if not cache_file.exists() or force_refresh:
        log.info("Downloading NOAA PDSI...")
        # NOAA updates filename monthly so try current then discover
        base_url = NOAA_DROUGHT_BASE
        try:
            import re
            dir_r = requests.get(base_url + "/", timeout=30)
            matches = re.findall(r"climdiv-pdsidv-v1\.0\.0-\d{8}", dir_r.text)
            fname   = matches[-1] if matches else "climdiv-pdsidv-v1.0.0-20250108"
        except Exception:
            fname = "climdiv-pdsidv-v1.0.0-20250108"

        r = requests.get(f"{base_url}/{fname}", timeout=120)
        r.raise_for_status()
        cache_file.write_text(r.text)

    raw_text = cache_file.read_text()
    records  = []

    SD_DIVISIONS = list(range(1, 10))
    DIV_NAMES = {
        1: "Northwest", 2: "North Central", 3: "Northeast",
        4: "West Central", 5: "Central", 6: "East Central",
        7: "Southwest", 8: "South Central", 9: "Southeast",
    }

    # NOAA climdiv format: SS + DD + EE + YYYY (10 chars)
    #   SS   = state code (2 digits, ex. 39 = South Dakota)
    #   DD   = climate division (2 digits, 01–09)
    #   EE   = element code (05 = PDSI)
    #   YYYY = year (4 digits)
    # Values are actual PDSI units (not scaled)
    PDSI_ELEMENT = "05"

    for line in raw_text.strip().splitlines():
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) < 13:
            continue
        code = parts[0]
        if len(code) != 10:
            continue
        st      = code[0:2]
        div_str = code[2:4]
        element = code[4:6]
        if st != state_code or element != PDSI_ELEMENT:
            continue
        try:
            div  = int(div_str)
            year = int(code[6:10])
        except ValueError:
            continue
        if div not in SD_DIVISIONS:
            continue
        if year < start_year or year > end_year:
            continue

        for month_idx, raw_val in enumerate(parts[1:13], start=1):
            try:
                val  = float(raw_val)
                pdsi = np.nan if val <= -99 else val
            except ValueError:
                pdsi = np.nan
            records.append({
                "division": div,
                "div_name": DIV_NAMES.get(div, str(div)),
                "year":     year,
                "month":    month_idx,
                "date":     pd.Timestamp(year=year, month=month_idx, day=1),
                "pdsi":     pdsi,
            })

    if not records:
        warnings.warn(
            f"PDSI file parsed but no records matched state_code='{state_code}'. "
            "Delete data/cache/noaa_pdsi_climdiv.txt and re-run to force re-download.",
            UserWarning, stacklevel=2,
        )
        return pd.DataFrame(columns=["division","div_name","year","month","date","pdsi"])

    df = pd.DataFrame(records).dropna(subset=["pdsi"]).reset_index(drop=True)
    return df


# Tribal operational data loaders (local files)

def load_tribal_groundwater(
    path: str | Path | None = None,
) -> pd.DataFrame:
    """
    Load Tribal-collected groundwater level data from local Excel or CSV.

    This data is GITIGNORED and stays under Tribal control.
    See data/templates/groundwater_template.xlsx for the expected format.

    Returns empty DataFrame with correct columns if file not found 
    The pipeline degrades to public data only.
    """
    from src.constants import GW_TEMPLATE_FIELDS, RAW_DIR

    if path is None:
        # Try common locations
        candidates = [
            RAW_DIR / "groundwater.csv",
            RAW_DIR / "groundwater.xlsx",
            RAW_DIR / "groundwater_master.xlsx",
        ]
        path = next((p for p in candidates if p.exists()), None)

    if path is None:
        warnings.warn(
            "No Tribal groundwater data file found in data/raw/. "
            "Public USGS data will be used for analysis. "
            "See data/templates/groundwater_template.xlsx to start "
            "collecting field measurements.",
            UserWarning, stacklevel=2,
        )
        return pd.DataFrame(columns=GW_TEMPLATE_FIELDS)

    path = Path(path)
    if path.suffix in (".xlsx", ".xls"):
        df = pd.read_excel(path, dtype=str)
    else:
        df = pd.read_csv(path, dtype=str)

    # Standardize
    df.columns = df.columns.str.lower().str.strip()
    df["date"] = pd.to_datetime(df.get("date"), errors="coerce")
    df["water_level_ft"] = pd.to_numeric(df.get("water_level_ft"), errors="coerce")

    # Basic validation
    n_before = len(df)
    df = df.dropna(subset=["well_id", "date", "water_level_ft"])
    df = df[df["water_level_ft"] > 0]
    df = df[df["water_level_ft"] < 1000]
    n_after = len(df)

    if n_before > n_after:
        warnings.warn(
            f"Removed {n_before - n_after} invalid rows from groundwater data "
            "(missing required fields, negative values, or > 1000 ft).",
            UserWarning, stacklevel=2,
        )

    return df.reset_index(drop=True)


def load_tribal_water_quality(
    path: str | Path | None = None,
) -> pd.DataFrame:
    """
    Load Tribal-collected water quality data from local Excel or CSV.

    This data is GITIGNORED and stays under Tribal control.
    See data/templates/water_quality_template.xlsx for the expected format.
    """
    from src.constants import WQ_TEMPLATE_FIELDS, RAW_DIR

    if path is None:
        candidates = [
            RAW_DIR/"water_quality.csv",
            RAW_DIR/"water_quality.xlsx",
            RAW_DIR/"water_quality_master.xlsx",
        ]
        path = next((p for p in candidates if p.exists()), None)

    if path is None:
        warnings.warn(
            "No Tribal water quality data file found in data/raw/. "
            "Public WQP data will be used for context. "
            "See data/templates/water_quality_template.xlsx to start "
            "collecting sampling results.",
            UserWarning, stacklevel=2,
        )
        return pd.DataFrame(columns=WQ_TEMPLATE_FIELDS)

    path = Path(path)
    if path.suffix in (".xlsx", ".xls"):
        df = pd.read_excel(path, dtype=str)
    else:
        df = pd.read_csv(path, dtype=str)

    df.columns = df.columns.str.lower().str.strip()
    df["date"] = pd.to_datetime(df.get("date"), errors="coerce")

    # Parse numeric columns
    numeric_cols = ["nitrate_mgl", "ph", "tds_mgl", "turbidity_ntu",
                    "arsenic_ugl", "fluoride_mgl"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df.dropna(subset=["site_id", "date"]).reset_index(drop=True)


# Internal helpers

def _bbox_tiles(
    bbox: tuple[float, float, float, float],
    max_span_degrees: float,
) -> list[tuple[float, float, float, float]]:
    """Split a bounding box into stable, API-friendly tiles."""
    min_lon, min_lat, max_lon, max_lat = bbox
    if min_lon >= max_lon or min_lat >= max_lat:
        raise ValueError("bbox must be (min_lon, min_lat, max_lon, max_lat)")
    tiles = []
    lon = min_lon
    while lon < max_lon:
        next_lon = min(lon + max_span_degrees, max_lon)
        lat = min_lat
        while lat < max_lat:
            next_lat = min(lat + max_span_degrees, max_lat)
            tiles.append((lon, lat, next_lon, next_lat))
            lat = next_lat
        lon = next_lon
    return tiles


def _dms_to_decimal_degrees(value: object) -> float:
    """Convert USGS packed DMS coordinates (for example 430229) to decimal."""
    if pd.isna(value):
        return np.nan
    digits = str(value).split(".")[0].strip()
    if not digits.isdigit() or len(digits) not in (6, 7):
        return np.nan
    degree_digits = 2 if len(digits) == 6 else 3
    degrees = int(digits[:degree_digits])
    minutes = int(digits[degree_digits:degree_digits + 2])
    seconds = int(digits[degree_digits + 2:])
    if minutes >= 60 or seconds >= 60:
        return np.nan
    return degrees + minutes / 60 + seconds / 3600


def _get_usgs_ogc_features(
    url: str,
    params: dict[str, str],
    page_size: int = 1_000,
) -> list[dict]:
    """Fetch every feature from a paginated USGS OGC API query.

    The API returns only a page at a time.  Following its ``next`` link avoids
    silently treating a partial first page as complete coverage.
    """
    request_params = {**params, "f": "json", "limit": page_size}
    features: list[dict] = []
    next_url: str | None = url
    while next_url:
        response = requests.get(next_url, params=request_params, timeout=120)
        response.raise_for_status()
        payload = response.json()
        features.extend(payload.get("features", []))
        next_link = next(
            (link.get("href") for link in payload.get("links", [])
             if link.get("rel") == "next"),
            None,
        )
        next_url = next_link
        # The next link already contains query parameters.
        request_params = {}
    return features

def _parse_nwis_rdb(text: str, value_col: str, value_name: str) -> list[dict]:
    from io import StringIO

    lines = [l for l in text.splitlines() if not l.startswith("#")]
    if len(lines) < 3:
        return []

    cols = lines[0].split("\t")

    # Skip ALL non-data rows after the header:
    # the format row (5s, 15s, 10s...) and any blanks
    data_lines = []
    for line in lines[1:]:
        if not line.strip():
            continue
        first_field = line.split("\t")[0].strip()
        # Format rows start with digit-width specs like "5s" or "15s"
        # Real data rows start with "USGS"
        if first_field in ("agency_cd",) or "s" in first_field.lower()[:3]:
            continue
        data_lines.append(line)

    if not data_lines:
        return []

    df = pd.read_csv(
        StringIO("\n".join(data_lines)),
        sep="\t", header=None, names=cols, dtype=str,
    )

    bare_code = value_col.replace("_va", "").replace("_cd", "")
    val_col = next(
        (c for c in df.columns if bare_code in c and not c.endswith("_cd")),
        None,
    )
    if val_col is None:
        log.warning(
            "_parse_nwis_rdb: no value column for '%s'. Available: %s",
            bare_code, cols,
        )
        return []

    records = []
    for _, row in df.iterrows():
        raw      = row.get(val_col, "")
        datetime = row.get("datetime", "")
        # Skip rows where datetime is not a plausible date string
        if not datetime or len(datetime) < 8 or not datetime[0].isdigit():
            continue
        try:
            records.append({
                "site_no":  row.get("site_no", ""),
                "datetime": datetime,
                value_name: float(raw) if raw not in ("", None, "Ice") else np.nan,
            })
        except (ValueError, KeyError):
            continue

    return records

def _parse_nwis_site_rdb(text: str) -> pd.DataFrame:
    """Parse a USGS NWIS site inventory RDB response."""
    from io import StringIO

    lines      = [l for l in text.splitlines() if not l.startswith("#")]
    if len(lines) < 3:
        return pd.DataFrame()

    cols       = lines[0].split("\t")
    data_lines = [l for l in lines[2:] if l.strip()]
    if not data_lines:
        return pd.DataFrame()

    return pd.read_csv(
        StringIO("\n".join(data_lines)),
        sep="\t", header=None, names=cols, dtype=str,
    )
