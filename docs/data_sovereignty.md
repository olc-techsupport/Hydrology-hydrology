# Data Sovereignty

This document describes the data governance frameworks that apply to
`tribal_water_monitoring` and explains how they are implemented throughout
the repository.

## Why Data Sovereignty Matters for Water

Water data about Indigenous lands is not neutral. A dataset of groundwater
levels, streamflow measurements, or water quality samples describes a Tribal
Nation's most critical resource and its absence from federal monitoring
networks describes a century of underinvestment in Tribal infrastructure.

Both the presence of data and the absence of data carry governance
implications. Who collected it? Who can use it? Who benefits from the
analysis? Who has authority over what the results say? These questions
must be answered before the first line of code runs.

## Frameworks Implemented in This Repository

### OCAP®: Ownership, Control, Access, Possession

Developed by the First Nations Information Governance Centre (FNIGC),
OCAP® establishes that Indigenous peoples have:

- **Ownership**:   the community owns information collectively
- **Control**:     the community controls all aspects of data management
- **Access**:      members can access data about their community
- **Possession**:  physical custody of data is maintained by the community

**How this repository implements OCAP®:**

Tribal-collected operational data (well levels, water quality samples)
is stored in `data/raw/`, which is gitignored and never committed to
version control. This data stays on the Tribal Nation's infrastructure
under their physical possession and control. The repository provides
tools to analyze it, not a mechanism to extract or share it.

Public federal data (USGS NWIS, NOAA, Census, NHD) downloaded to
`data/cache/` is also gitignored. Analysis results in `outputs/` are
likewise gitignored and analysis products derived from Tribal operational
data should be reviewed by the relevant Nation before external sharing.

Reference: https://fnigc.ca/ocap-training/

### CARE Principles for Indigenous Data Governance

The CARE Principles were developed by the Global Indigenous Data Alliance
to address the ethical dimensions of data use that FAIR principles alone
cannot. CARE applies throughout the data lifecycle.

**C : Collective Benefit**
Data ecosystems shall be designed and function in ways that enable
Indigenous Peoples to derive benefit from the data.

*In this repository:* Analysis results should be shared with the relevant
Tribal Nation's water program before publication or external distribution.
The operational pipeline (pipeline track) is designed specifically to
support day-to-day Tribal water management decisions, not research outputs.

**A : Authority to Control**
Indigenous Peoples' rights and interests in data must be recognized and
their authority to control such data must be respected.

*In this repository:* All configurable thresholds (drought stages, alert
levels) are reviewed with Tribal water staff, not set unilaterally by
the analyst. The `config/config.yaml` file is designed for this
conversation. Tribal-collected data is analyzed only with the Nation's
knowledge and consent.

**R : Responsibility**
Those working with Indigenous data have a responsibility to share how
those data are used and to support the capacity of Indigenous Peoples
to govern their own data.

*In this repository:* Every transformation step is documented and visible.
No black-box models. When someone asks "why is this well flagged critical?",
the answer is a specific value, a specific threshold, and a specific line
of code. The system is designed to be understood and maintained by Tribal
staff, not just researchers.

**E : Ethics**
Indigenous Peoples' rights and wellbeing should be the primary concern
at all stages of the data life cycle.

*In this repository:* Federal monitoring gaps are documented as equity
findings. The absence of USGS monitoring wells on Tribal lands is a 
systemic infrastructure equity issue, not a reason to conclude that groundwater is fine.

Reference: https://www.gida-global.org/care

### FAIR Principles

The FAIR Principles govern technical data management:
Findable, Accessible, Interoperable, Reusable.

**How this repository implements FAIR:**

All analysis notebooks are reproducible from public sources and include
full citation information for every dataset used. The `outputs/` directory
uses standard formats (CSV, GeoJSON, parquet) that can be opened by any
GIS or data analysis software. Metadata is embedded in every output file.

**Important:** A dataset can be fully FAIR and still violate every CARE
principle. FAIR governs technical accessibility; CARE and OCAP® govern
the ethical obligations to Tribal Nations. Both are required.

Reference: https://www.go-fair.org/fair-principles/

### IEEE 2890-2025: Recommended Practice for Provenance of Indigenous Peoples' Data

IEEE 2890-2025 is the first international standard specifically addressing
the provenance of data about Indigenous Peoples. Published November 2025,
it establishes common parameters for describing where data came from,
how it is connected to people and place, and how governance responsibilities
travel with data through transformations.

**How this repository implements IEEE 2890-2025:**

The `src/sovereignty.py` module maintains a registry of all data sources
with provenance metadata: what the data is, who stewards it, what license
applies, and specific governance notes for Tribal contexts. Every notebook
calls `print_data_acknowledgment()` at the top and `generate_citations()`
at the bottom.

Reference: https://standards.ieee.org/ieee/2890/10318/

## The Critical Distinction: Public vs. Tribal Data

This repository works with two fundamentally different categories of data:

### Public Federal Data
USGS NWIS, NOAA climate data, Census TIGER boundaries, NHD hydrography.

These datasets are freely available and are downloaded automatically.
They are gitignored (not committed) but can be re-downloaded by anyone.

**Governance note:** Public federal data covers Tribal lands but was not
collected by or for Tribal Nations. Analysis results derived from this
data about Tribal territories still carry ethical obligations and results
should be shared with the relevant Nation before publication.

### Tribal Operational Data
Well level measurements, water quality samples, monitoring logs.

This data is collected by Tribal staff on Tribal infrastructure.
It is stored in `data/raw/`, gitignored, and never leaves the local
system without explicit Tribal authorization.

**Governance note:** Tribal operational data is governed by OCAP®.
The Nation that collected it owns it, controls its use, and must be
consulted before any analysis results derived from it are shared externally.

## Monitoring Gaps as Equity Findings

A recurring theme in this repository is the systematic absence of federal
monitoring infrastructure on Tribal lands:

- No USGS groundwater monitoring wells within or immediately adjacent
  to Oceti Sakowin territories
- Sparse USGS streamflow gauge coverage
- Limited EPA/USGS water quality monitoring

These gaps are documented explicitly throughout the analysis notebooks as
**federal infrastructure equity findings**, not as evidence that water
conditions are stable or that data is unavailable. The operational pipeline
is designed specifically to fill these gaps with Tribal-collected data.

When a federal agency report notes "data not available"
for a Tribal area, that absence reflects a policy and funding decision,
not a physical reality about the land or water.

## Adapting This Repository for Your Nation

If you are adapting this repository for a different Tribal Nation,
the data sovereignty framework applies regardless of geography:

1. Identify the appropriate Tribal governance office to notify
2. Review the analysis purpose with that office before beginning
3. Confirm how and with whom analysis results will be shared
4. Replace placeholder thresholds with values confirmed by Tribal staff
5. Ensure Tribal operational data stays on Tribal infrastructure

See `docs/adaptation_guide.md` for the technical steps.

## References

- OCAP® Principles: https://fnigc.ca/ocap-training/
- CARE Principles: https://www.gida-global.org/care
- Carroll et al. (2020). The CARE Principles for Indigenous Data Governance.
  *Data Science Journal*, 19(1). https://doi.org/10.5334/dsj-2020-043
- FAIR Principles: https://www.go-fair.org/fair-principles/
- IEEE 2890-2025: https://standards.ieee.org/ieee/2890/10318/
- Local Contexts: https://localcontexts.org/
- First Nations Information Governance Centre: https://fnigc.ca/
- Global Indigenous Data Alliance: https://www.gida-global.org/
