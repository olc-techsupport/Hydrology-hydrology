# Data Intake Guide

**For Tribal water monitoring staff and field technicians**

This guide explains how to record and submit groundwater level and water
quality measurements so they can be used in the monitoring dashboard and
analysis notebooks. No data science experience is required.

## The Short Version

1. Open your Excel template from `data/templates/`
2. Add new rows: one row per measurement
3. Do not change column names or delete old rows
4. Save the file to `data/raw/`
5. Run the pipeline (or notify your data coordinator)

## Groundwater Level Measurements

### File to use
`data/templates/groundwater_template.xlsx`

Save your completed file to: `data/raw/groundwater.xlsx`

### Required fields

| Column | What to enter | Example |
|---|---|---|
| `well_id` | Your well identifier: use the same ID every time | `PR-01` |
| `date` | Date of measurement in YYYY-MM-DD format | `2024-06-15` |
| `water_level_ft` | Depth to water in feet below land surface | `127.3` |

### Optional fields (add when available)

| Column | What to enter | Example |
|---|---|---|
| `measurement_method` | How you measured it | `tape`, `transducer`, `estimate` |
| `entered_by` | Your name or initials | `JSD` |
| `notes` | Anything unusual | `well casing damaged`, `pump running` |
| `lat` | Well latitude (decimal degrees) | `43.3521` |
| `lon` | Well longitude (decimal degrees) | `-102.4417` |
| `aquifer` | Which aquifer the well draws from | `Arikaree` |

## Important rules for groundwater data

**Depth to water means feet BELOW ground surface.**  
A reading of 150 ft means the water is 150 feet underground.
A reading that goes from 120 to 135 over time means the water table
is dropping (getting deeper i.e. worse conditions).
Do NOT enter water elevation above sea level here: that is a different
measurement. If you are unsure which your equipment reports, ask your
supervisor or the data coordinator.

**Use the same well ID every time.**  
If you call a well `PR-01` in January, call it `PR-01` in June.
If the ID changes, the trend analysis will treat it as a new well
and you will lose the historical record.

**Date format: YYYY-MM-DD only.**  
`2024-06-15` is correct. `6/15/24` will cause problems.
Excel may try to reformat dates. If it does, format the date column
as "Text" before entering values.

**Do not delete old rows.**  
Only add new rows at the bottom. The dashboard needs the full history
to compute trends. Deleting old rows breaks trend analysis.

**One measurement per row.**  
If you measure two wells on the same day, that is two rows.

### Example groundwater entries

```
well_id  | date       | water_level_ft | measurement_method | entered_by | notes
---------|------------|----------------|-------------------|------------|------
PR-01    | 2024-05-01 | 124.5          | tape              | JSD        |
PR-01    | 2024-06-01 | 125.8          | tape              | JSD        | after dry May
PR-02    | 2024-05-03 | 98.2           | transducer        | MRT        |
PR-02    | 2024-06-03 | 99.1           | transducer        | MRT        |
```

## Water Quality Measurements

### File to use
`data/templates/water_quality_template.xlsx`

Save your completed file to: `data/raw/water_quality.xlsx`

### Required fields

| Column | What to enter | Example |
|---|---|---|
| `site_id` | Your site identifier | `PR-SPRING-01` |
| `date` | Sample date in YYYY-MM-DD format | `2024-07-10` |
| `sample_type` | Type of source sampled | `well`, `spring`, `tap`, `stream` |

### Parameter fields (enter what you tested)

| Column | Parameter | EPA limit | Units |
|---|---|---|---|
| `nitrate_mgl` | Nitrate | 10 mg/L | mg/L |
| `ph` | pH | 6.5 – 8.5 | unitless |
| `tds_mgl` | Total dissolved solids | 500 mg/L (secondary) | mg/L |
| `turbidity_ntu` | Turbidity | 1 NTU (drinking water) | NTU |
| `arsenic_ugl` | Arsenic | 10 µg/L | µg/L |
| `fluoride_mgl` | Fluoride | 4 mg/L | mg/L |

Leave a cell blank if you did not test that parameter for that sample.
Do not enter `0` for a parameter you did not test; blank means "not tested,"
while `0` means "tested and found none."

### Additional fields

| Column | What to enter |
|---|---|
| `entered_by` | Your name or initials |
| `notes` | Lab, field conditions, unusual observations |

### Important rules for water quality data

**Units matter.**  
Nitrate is measured in mg/L. Arsenic is measured in µg/L (micrograms per liter,
1000× smaller than mg/L). Entering arsenic in mg/L instead of µg/L will make
it look 1000× worse than it is. Check your lab report for units.

**Leave untested parameters blank.**  
If your lab only tests for nitrate and pH, leave all other columns blank.

**Record the site ID consistently.**  
Same rules as well ID — use the same name every time for the same site.

### Example water quality entries

```
site_id      | date       | sample_type | nitrate_mgl | ph  | tds_mgl | entered_by | notes
-------------|------------|-------------|-------------|-----|---------|------------|------
PR-WELL-01   | 2024-07-10 | well        | 4.2         | 7.3 | 312     | JSD        | routine quarterly
PR-SPRING-01 | 2024-07-10 | spring      | 1.8         | 7.8 | 445     | JSD        | after rain
PR-TAP-01    | 2024-07-10 | tap         | 3.1         | 7.2 | 298     | JSD        | community center tap
```

## How Data Flows into the Dashboard

```
You record a measurement
        
You add it to the Excel file in data/raw/
        
Data coordinator runs the pipeline:
    python pipeline/groundwater.py
    python pipeline/water_quality.py
        
Dashboard updates automatically
        
Well status map, alerts, and weekly changes reflect new data
```

On systems where `run_pipeline.bat` has been configured, double-clicking
that file runs all pipeline steps automatically.

## Common Problems and Solutions

**Problem:** Date column shows `#####` in Excel  
**Solution:** Widen the date column. Format it as "Text" to prevent Excel
from auto-converting dates.

**Problem:** Well is showing as "Declining" but you don't think it is  
**Solution:** Check that water level is entered as depth BELOW ground surface
(larger number = deeper). If you are entering elevation above sea level,
the trend will be inverted. Talk to your data coordinator.

**Problem:** You entered a wrong value  
**Solution:** Correct it by editing that row. Do not delete the row,
just fix the value and add a note in the `notes` column explaining the correction.

**Problem:** A well has a new ID after being redeveloped or renamed  
**Solution:** Keep the old ID for historical records and start a new ID for
the new or renamed well. Note the connection in the `notes` column.
(`"Well redeveloped 2024-08-01: continued as PR-01B"`)

## Questions and Contact

If you are unsure about any measurement, unit, or entry, stop and ask
before entering data. One bad entry can distort trend analysis for a well.

Data coordinator: [add contact information]  
Tribal water program: [add contact information]

## Your Data Is Yours

Reminder: the data you enter stays on local infrastructure and is never
automatically shared outside the Tribal water program. The gitignore
configuration ensures this data is never uploaded to GitHub or any
external server.

If analysis results from your data are going to be shared with anyone
outside the water program that requires explicit review and authorization 
by the appropriate Tribal governance office.

See `docs/data_sovereignty.md` for the full governance framework.
