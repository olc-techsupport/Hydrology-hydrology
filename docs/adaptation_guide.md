# Adaptation Guide

**For Tribal Nations adapting this repository for their own use**

This repository was built and demonstrated at Pine Ridge (Oglala Lakota)
and Rosebud (Sicangu Lakota) Reservations, Oceti Sakowin. It is designed
to be forked and adapted for any Tribal Nation's water monitoring program
with minimal changes to the core code.

This guide walks through every change you need to make.

## Before You Start

**Talk to your water program first.**  
This system is most useful when the people who will use it help shape
what it monitors and what thresholds matter. Before writing any code,
sit with your Tribal water office and answer:

1. Which wells do we want to monitor?
2. What level of groundwater decline counts as "watch" vs. "emergency"?
3. Which USGS stream gauges are near our territory?
4. What water quality parameters matter most for our drinking water sources?
5. Who will update the data, and how often?

The answers to these questions go into `config/config.yaml`. The system
is only as good as the thresholds reflect local knowledge.

## Step 1: Fork and Clone the Repository

```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/your-org/tribal_water_monitoring
cd tribal_water_monitoring

# Create your conda environment
conda env create -f environment.yml
conda activate tribal-water

# Register the Jupyter kernel
python -m ipykernel install --user --name tribal-water \
    --display-name "Python (tribal-water)"
```

## Step 2: Update config/config.yaml

This is the primary configuration file. Change these sections:

### Nation identity
```yaml
nation:
  primary:    "Your Nation Name"       # ex. "Confederated Tribes of Warm Springs"
  secondary:  "Second Nation"          # if applicable, or remove
  collective: "Your collective term"   # ex. "Columbia River Tribes"
```

### Bounding box
```yaml
# adjust to your territory
bounding_box:
  west:  -121.5   
  south:   44.3
  east:  -120.0
  north:   45.2
```
Find your bounding box by looking up your Nation's territory on a map.
Use decimal degrees (WGS84). Add a buffer of 0.5–1.0 degrees around
the actual boundary to capture upstream context.

### USGS streamflow sites
Find USGS stream gauges near your territory:
https://waterdata.usgs.gov/nwis/rt
```yaml
# replace with your gauges
usgs_streamflow_sites:
  - "14076500"   
  - "14092500"
```

### USGS groundwater sites
The project discovers USGS monitoring locations with the modern Water Data API.
These are sites with USGS observations, **not** a complete inventory of water
wells. The loader tiles large areas and raises an error when a query fails; an
API failure must never be reported as a monitoring gap.

For discrete depth-to-water readings, the project uses the modern USGS field
measurements API. The legacy `gwlevels` endpoint was retired in 2026.

### Historical and state well inventories

Use a separate inventory layer for wells that are known to exist but are not
actively monitored by USGS. For Pine Ridge and Bennett County, call
`load_carter_2007_inventory()` to download the supplemental workbook for
Carter and Heakin (2007), USGS Scientific Investigations Map 2993. Every row
is marked `is_monitoring_site=False` and retains its source and publication
year, so it cannot be mistaken for current observations.

For more recent construction records, use the South Dakota DANR Water Well
Completion Reports service. Treat these as an inventory with record-specific
completion dates and verification status, not as water-level measurements.
```yaml
# replace with your sites
usgs_groundwater_sites:
  - "430000121000001"   
```
Note: USGS groundwater monitoring is sparse on many Tribal lands.
If no sites exist near your territory, document that gap and focus
on Tribal-collected well data (Step 5).

### Streamflow thresholds
Review with your water staff. Thresholds depend on the specific gauge
and what flow rates matter for your community's water use.
```yaml
# adjust based on your gauge and conditions
thresholds:
  streamflow:
    normal_cfs:    100    
    watch_cfs:      40
    emergency_cfs:  10
```

### Water quality thresholds
The defaults are EPA MCLs. Add Tribal-specific thresholds where
your community's standards are more protective.
```yaml
# EPA MCLs: adjust if Tribal standard differs
  water_quality:
    nitrate_mgl:    10.0   
    arsenic_ugl:    10.0
    tds_mgl:       500.0
    # Add parameters specific to your geology/contamination concerns
```

### Stress index weights
Adjust based on which resource is most critical for your community.
If your community depends almost entirely on groundwater, increase GW weight.
```yaml
# example: increase if GW is the primary source
stress_index_weights:
  groundwater:  0.50   
  streamflow:   0.25
  drought:      0.25
```

### Dashboard settings
```yaml
dashboard:
  title:       "Your Nation Water Monitoring"
  center_lat:   44.7    # center of your territory
  center_lon: -120.8
  zoom:          9
```

## Step 3: Update src/constants.py

Change the Tribal Nation name lists:

```python
# Replace Oceti Sakowin names with your Nations
CENSUS_NAMES = [
    "Warm Springs",
    # Add other Nations if applicable
]

CENSUS_TO_COMMON = {
    "Warm Springs": "Confederated Tribes of Warm Springs",
    # Add others
}

PRIMARY_NATIONS = ["Confederated Tribes of Warm Springs"]

NATION_CENTROIDS = {
    "Confederated Tribes of Warm Springs": {"lat": 44.77, "lon": -121.27},
}

# Update bounding boxes
YOUR_NATION_BBOX = (-122.0, 44.3, -120.5, 45.2)
```

Also update NOAA climate division assignments in `src/loaders.py`
for the PDSI loader — find your division(s) at:
https://www.ncei.noaa.gov/monitoring-references/maps/us-climate-divisions.php

## Step 4: Update src/sovereignty.py

Update the data source registry with any sources specific to your territory.
At minimum, update the `tribal_groundwater` and `tribal_water_quality`
entries to reflect your Nation's water program:

```python
"tribal_groundwater": {
    "name":    "Your Nation Water Program groundwater monitoring data",
    "steward": "Your Nation Water Resources Department",
    "license": "Tribal governance — OCAP® applies",
    ...
},
```

## Step 5: Add Your Field Data Templates

The blank Excel templates in `data/templates/` are generic. You may want
to customize them for your field staff:

- Add your Nation's logo or header
- Pre-fill the `entered_by` dropdown with staff names
- Add columns for parameters specific to your monitoring program
- Translate column headers if staff prefer another language

Keep the required columns (`well_id`, `date`, `water_level_ft` for
groundwater; `site_id`, `date`, `sample_type` for water quality) with
the same names — the pipeline depends on them.

If you add new columns, update `src/constants.py`:
```python
GW_TEMPLATE_FIELDS = [
    "well_id", "date", "water_level_ft",
    "measurement_method", "entered_by", "notes",
    "your_new_column",  # add here
]
```

## Step 6: Update the Notebooks

Each notebook has a header cell with Nation-specific references.
Search for "Oceti Sakowin", "Pine Ridge", "Oglala Lakota", and "Rosebud"
in each notebook and update accordingly.

Cells to update in each notebook:
- The governance preamble call: update `source_keys` if you are using
  different data sources
- `PRIMARY_NATIONS` references
- Bounding box variables
- Any hardcoded NOAA climate division numbers

## Step 7: Update the Dashboard Title

In `app/app.py`, change:
```python
st.title("Tribal Water Monitoring")
```
to your Nation's name. This is the first thing staff and leadership will
see so it should feel like your system, not a generic template.

## Step 8: Test with a Small Dataset

Before sharing with your water office, test with 5–10 rows of data:

1. Create `data/raw/groundwater.xlsx` with 5–10 rows using real or
   realistic test data
2. Run `python pipeline/groundwater.py`
3. Run `streamlit run app/app.py`
4. Walk through each panel and confirm:
   - Does the well map show wells in the right place?
   - Does "Declining" correctly identify wells where level is dropping?
   - Do the thresholds match what your water staff told you?

If something doesn't look right, fix it before going live. Trust
is built in the first demonstration, and lost if the first thing
staff see is a well incorrectly flagged.

## Step 9: Deploy

**Option A: Local deployment (recommended first step)**
Run the pipeline and dashboard locally on a laptop or workstation
in the Tribal water office. Staff run `run_pipeline.bat` weekly.
No internet required after initial data setup.

**Option B: Server deployment**
For wider access within the Tribal network, deploy Streamlit on a
local sovereign server or private cloud. Keep `data/raw/` on Tribal 
infrastructure, do not move Tribal operational data to public cloud.

**Option C: Offline-only**
If connectivity is very limited, pre-download all public data, run
the pipeline once, and distribute the resulting dashboard as a
static HTML export. Update manually when new data is added.

## Common Adaptation Questions

**Q: My Nation doesn't have any USGS groundwater wells nearby.**  
A: That is common and is itself a significant finding; document it in
your notebook 01 analysis. Start with Tribal-collected well data in
`data/raw/` and focus the operational pipeline on that. The notebooks
degrade when USGS data is absent.

**Q: I want to add a parameter that isn't in the default water quality template.**  
A: Add the column to the template Excel file and to `WQ_TEMPLATE_FIELDS`
in `src/constants.py`. Then add the threshold to `config.yaml` and
the exceedance flag logic to `flag_water_quality_exceedances()` in
`src/indicators.py`.

**Q: Our territory spans multiple states/NOAA climate divisions.**  
A: Update `PRIMARY_DIVISIONS` in the PDSI loader cell of notebook 05
to include all relevant divisions. The heatmap in that notebook will
show all of them.

**Q: We want to add a variable the system doesn't currently support.**  
A: The cleanest path is to add a new loader function to `src/loaders.py`
following the same pattern (check cache, download, return DataFrame),
a corresponding indicator function in `src/indicators.py`, and a new
notebook or section in an existing notebook. Open an issue or pull
request on GitHub to share your additions with other Nations.

**Q: Who do I contact if I need help?**  
A: You can reach Lilly or Jim at:   
[daearconsulting@gmail.com](mailto:daearconsulting@gmail.com)

## Giving Back

If your adaptation improves something that would benefit other Nations such as
a better API endpoint, a new data source, a cleaner indicator calculation,
please consider contributing it back to the shared repository via pull request.

The goal is a growing library of water monitoring tools that serve all
Tribal Nations, not parallel forks that diverge and can't be maintained.
