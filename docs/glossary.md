# Glossary

Terms used in the `tribal_water_monitoring` repository and notebooks.
Terms are grouped by domain. Scientific jargon is defined in plain language
suitable for community members who are not hydrologists.

## Water Systems

**Aquifer**  
A layer of rock or sediment underground that holds water and allows water
to move through it. Most drinking water wells on Pine Ridge and Rosebud
draw from the Arikaree aquifer, part of the larger Ogallala (High Plains) Aquifer system.

**Arikaree Aquifer**  
The primary groundwater source for much of Pine Ridge and Rosebud. It
is an ancient geologic formation of sand and gravel that holds water
accumulated over thousands of years. Recharge (natural refilling) is
very slow; water pumped out today may take decades or even centuries to be replaced.

**Baseflow**  
The portion of streamflow sustained by groundwater discharge between
rainfall and snowmelt events. High baseflow means the stream stays wet
even in dry periods because groundwater is seeping into it. Low baseflow
means the stream dries up quickly after precipitation stops.

**Baseflow Index (BFI)**  
A ratio (0–1) expressing what fraction of total streamflow comes from
groundwater. BFI near 0 = stream is almost entirely runoff-driven and
will dry up quickly. BFI near 1 = stream is primarily groundwater-fed
and more reliable, but sensitive to aquifer depletion.

**Cfs (cubic feet per second)**  
The standard unit for measuring streamflow in the United States.
One cfs = about 450 gallons per minute. A typical garden hose runs
at about 0.02 cfs. The White River at normal stage runs at 50–500 cfs.

**Depth to water**  
How far underground the water table is at a given well, measured in
feet below the land surface. A larger number means the water table is
deeper. This is the standard measurement from field surveys.

**Ephemeral stream**  
A stream that flows only during and immediately after precipitation.
It is dry most of the year. Many draws and small drainages on Oceti
Sakowin lands are ephemeral.

**Gaining reach**  
A section of stream where groundwater flows INTO the stream, adding to
its flow. Gaining reaches stay wet longer in drought.

**Groundwater recharge**  
Water that infiltrates through the soil and eventually reaches the
aquifer, replenishing it. On the Northern Great Plains, recharge is
slow (inches per year or less) and depends on adequate snowpack and
spring precipitation.

**Hydraulic head/water level**  
The height of water in a well above a reference point. Used to map
which direction groundwater flows underground.

**Intermittent stream**  
A stream that flows seasonally, typically during spring snowmelt
and after significant rain, but is dry for part of the year.

**Losing reach**  
A section of stream where water seeps from the stream into the
groundwater below. Losing reaches can help recharge aquifers.

**Ogallala (High Plains) Aquifer**  
The largest aquifer system in North America, underlying portions of
eight Great Plains states. The Arikaree formation beneath Pine Ridge
and Rosebud is part of this system. It is being depleted faster than
it recharges across much of its extent (outside of the northernmost
units on Pine Ridge and Rosebud, where it is more stable).

**Perennial stream**  
A stream that flows year-round. The White River is nominally perennial
but can reach near-zero flow in extreme drought years.

**Streamflow**  
The volume of water moving through a stream at a given point, measured
in cfs. USGS gauges measure this continuously at permanent monitoring
stations.

**Water table**  
The upper surface of the groundwater zone. It is the depth at which the
ground is saturated (filled) with water. When wells are pumped faster than
recharge, the water table drops.

**Water year**  
October 1 through September 30. USGS uses water years (not calendar
years) when reporting annual streamflow statistics because this period
captures a full precipitation cycle including winter snowpack.

## Climate and Drought

**PDSI (Palmer Drought Severity Index)**  
A standardized measure of drought that accounts for both precipitation
deficit and temperature-driven water demand. Values: near zero = normal,
negative = drought (more negative = worse), positive = wet conditions.
Thresholds: -2 = moderate drought, -3 = severe drought, -4 = extreme drought.

**NOAA Climate Division**  
NOAA divides each state into climate divisions based on similar climate
patterns. South Dakota has 9 divisions. Division 7 (Southwest) covers
most of Pine Ridge; Division 6 (South Central) covers most of Rosebud.
PDSI is reported at the division level.

**RCP (Representative Concentration Pathway)**  
A scenario of future greenhouse gas emissions used in climate projections.
RCP 4.5 = moderate emissions reduction. RCP 8.5 = high emissions (business
as usual). The difference between scenarios represents the effect of
policy choices made in coming decades.

**MACAv2**  
Multivariate Adaptive Constructed Analogs, version 2. A statistically
downscaled climate dataset that translates global climate model outputs
to a 4km resolution covering the continental US. Used in notebook 07
for future temperature and precipitation projections.

**Evapotranspiration (ET)**  
Water lost from the land surface through evaporation from soil and
transpiration through plants. Higher temperatures increase ET, which
means more water is needed to maintain the same vegetation condition.
A crucial mechanism by which warming worsens drought.

**Heat stress days**  
Days when maximum temperature exceeds a threshold harmful to livestock
or human health. In this series, 100°F and 110°F thresholds are used.
More heat stress days = more water demand from livestock = more pressure
on groundwater.

## Data and Analysis

**7Q10**  
The lowest 7-day average streamflow expected to occur once every 10 years.
A standard low-flow metric used in water quality permitting. Represents
the "design low flow" for a stream; the conditions that stress aquatic life
and reduce dilution of pollutants.

**Anomaly**  
The departure of a value from the long-term average. A PDSI anomaly of
-2 means conditions were 2 units drier than average. Anomalies allow
comparison across variables with different units.

**Compound stress**  
Conditions where multiple stress indicators are simultaneously bad.
The Compound Water Stress Index (CWSI) in notebook 06 measures compound
stress combining groundwater, streamflow, and drought simultaneously.

**Theil-Sen slope**  
A robust method for estimating the trend in a time series. Unlike ordinary
linear regression, it is not affected by outlier years (like an extreme
flood or drought year). Standard method for detecting trends in
environmental monitoring data.

**Percentile rank**  
A value's position relative to all other values in the historical record.
A groundwater level at the 10th percentile is deeper than 90% of
historical observations.

## Governance

**CARE Principles**  
Collective Benefit, Authority to Control, Responsibility, Ethics. A
framework for ethical Indigenous data governance developed by the Global
Indigenous Data Alliance. See `docs/data_sovereignty.md`.

**IEEE 2890-2025**  
The first international standard for provenance of Indigenous Peoples'
data, published November 2025. Establishes parameters for documenting
where data came from, how it was processed, and how governance
responsibilities travel with it.

**Local Contexts**  
A platform for Indigenous communities to add context and traditional
knowledge labels to cultural heritage materials and data. Provides
Traditional Knowledge (TK) and Biocultural (BC) labels that travel
with data to signal community authority and appropriate use conditions.
See https://localcontexts.org/

**OCAP®**  
Ownership, Control, Access, Possession. A framework for First Nations
data governance developed by the First Nations Information Governance
Centre. Establishes that Indigenous communities own their data and
maintain authority over its use. See `docs/data_sovereignty.md`.

**TK Label**  
A Traditional Knowledge label from Local Contexts. Signals cultural
authority and appropriate use conditions for data about Indigenous
knowledge, territories, and resources.

**Water sovereignty**  
The right of Tribal Nations to manage, protect, and benefit from their
water resources according to their own laws, governance structures, and
cultural values. Encompasses both the legal right (water rights) and
the practical capacity (infrastructure, monitoring, decision-making)
to exercise that right.

## Agencies and Programs

**NWIS (National Water Information System)**  
USGS database of streamflow, groundwater level, and water quality
measurements from monitoring sites across the US. The primary source
of public surface and groundwater data in this repository.
URL: https://waterdata.usgs.gov/nwis

**NHD (National Hydrography Dataset)**  
USGS mapping of streams, rivers, lakes, and water bodies across the US.
Used in notebook 01 to show stream networks on Oceti Sakowin lands.

**WBD (Watershed Boundary Dataset)**  
USGS mapping of watershed boundaries (HUC polygons). Used in notebook 01
to show how HUC-8 watershed boundaries relate to Tribal territories.

**WQP (Water Quality Portal)**  
A joint USGS/EPA database of water quality measurements from federal,
state, and tribal monitoring programs.
URL: https://www.waterqualitydata.us/

**HUC (Hydrologic Unit Code)**  
A hierarchical numbering system for watershed boundaries. HUC-2 = major
river basins (18 in US). HUC-8 = subbasins (~2,100 in US). HUC-12 =
small watersheds (~100,000 in US). Smaller HUC number = larger area.

**MCL (Maximum Contaminant Level)**  
EPA regulatory standard for drinking water contaminants. MCLs are
legally enforceable for public water systems. Private wells are not
regulated by MCLs but the thresholds are used as reference points in
notebook 04. Key MCLs: nitrate 10 mg/L, arsenic 10 µg/L, fluoride 4 mg/L.

## Units Quick Reference

| Unit | What it measures | Context |
|---|---|---|
| cfs | Streamflow | 1 cfs ≈ 450 gal/min |
| ft bls | Groundwater depth (feet below land surface) | Larger = deeper = worse |
| mg/L | Water quality concentration (milligrams per liter) | Same as ppm |
| µg/L | Water quality trace elements (micrograms per liter) | Same as ppb |
| NTU | Turbidity (Nephelometric Turbidity Units) | Cloudiness of water |
| mm | Precipitation depth | 25.4 mm = 1 inch |
| °F | Temperature | 32°F = 0°C, 100°F = 37.8°C |
