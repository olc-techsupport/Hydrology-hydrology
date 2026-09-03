from __future__ import annotations

"""Apply the common NIFA-aligned learning structure to the notebook series."""

import json
import re
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT/"notebooks"

MODULES = {
    "01": {
        "objectives": [
            "distinguish a Census statistical boundary from legal jurisdiction and community-defined lands",
            "inspect watershed overlap, stream networks, and public monitoring coverage at multiple spatial scales",
            "document how an off-boundary feature is relevant without representing it as an OST feature",
        ],
        "checkpoint": "Choose one mapped boundary or feature. Record what it represents, who produced it, and one claim it cannot support.",
        "contribution": "Improve one map label, boundary caveat, source note, or glossary link. Ask a partner whether the revision prevents a likely misinterpretation.",
        "next": "Notebook 02 examines the coverage and record characteristics of configured public groundwater monitoring sites.",
    },
    "02": {
        "objectives": [
            "inspect record length, missingness, and sampling frequency before fitting a trend",
            "interpret the direction and uncertainty of a depth-to-water trend",
            "distinguish absence of public monitoring evidence from evidence about groundwater conditions",
        ],
        "checkpoint": "Select one well. Explain its period of record, the sign convention for depth to water, and whether the available observations justify a trend statement.",
        "contribution": "Add or improve one public-site description, unit note, missing-data warning, or trend limitation. Do not add OST-controlled data.",
        "next": "Notebook 03 examines seasonal streamflow and screening-level reliability measures for configured public streamgages.",
    },
    "03": {
        "objectives": [
            "summarize seasonal streamflow and annual record completeness",
            "explain how screening thresholds affect a reliability classification",
            "avoid treating a configured screening value as an approved operational trigger",
        ],
        "checkpoint": "Change one screening threshold temporarily and note which results change. Explain why this sensitivity matters for interpretation.",
        "contribution": "Improve one unit, threshold-status label, missing-record check, or plain-language description of streamflow reliability.",
        "next": "Notebook 04 evaluates the coverage, units, and screening benchmarks of public water-quality observations.",
    },
    "04": {
        "objectives": [
            "inspect sampling coverage and harmonize parameter units before comparison",
            "distinguish a screening flag from a regulatory, exposure, or health conclusion",
            "identify additional evidence needed to investigate a possible contaminant source",
        ],
        "checkpoint": "Choose one parameter and verify its reported unit, screening benchmark source, sample period, and number of sites before interpreting a flag.",
        "contribution": "Improve one unit conversion note, benchmark citation, coverage statement, or limitation. Do not infer a contaminant source from a flag alone.",
        "next": "Notebook 05 uses NOAA Climate Division 7 as a regional proxy for historical drought context.",
    },
    "05": {
        "objectives": [
            "summarize drought frequency using a regional PDSI proxy",
            "explain the spatial and conceptual limits of NOAA Climate Division 7",
            "distinguish correlation from prediction and causation when comparing drought and streamflow",
        ],
        "checkpoint": "Describe one year with strong apparent agreement and one with disagreement between PDSI and streamflow. List plausible reasons without selecting a cause.",
        "contribution": "Improve one proxy limitation, correlation caveat, period label, or explanation of the PDSI scale.",
        "next": "Notebook 06 combines selected historical components into an experimental screening index.",
    },
    "06": {
        "objectives": [
            "explain normalization, component availability, and weighting in a composite index",
            "test whether rankings are sensitive to alternate transparent weights",
            "identify value judgments and uncertainty hidden by a single index score",
        ],
        "checkpoint": "Compare the default weights with one alternative. Record which rankings change and why that prevents treating the index as an objective management threshold.",
        "contribution": "Improve one weight explanation, missing-component warning, sensitivity result, or label identifying the index as experimental.",
        "next": "Notebook 07 adds scenario-based climate projections while keeping them separate from historical observations and forecasts.",
    },
    "07": {
        "objectives": [
            "distinguish a climate scenario, model projection, and forecast",
            "compare time periods and scenarios without implying certainty",
            "explain why a single-model result is insufficient for a research-grade local projection",
        ],
        "checkpoint": "Rewrite one projected change as a bounded statement naming the model, scenario, period, spatial representation, and major uncertainty.",
        "contribution": "Improve one uncertainty statement, scenario label, time-period comparison, or recommendation for multi-model analysis.",
        "next": "Synthesize the series by tracing one claim back through its artifact, configuration, public source, assumptions, and required review authority.",
    },
}

REPLACEMENTS = {
    "Do any watersheds cross both Nations simultaneously?": "Which watersheds cross the Census statistical boundary, and what does that imply for hydrologic context?",
    "How far is the nearest USGS groundwater monitoring well from Pine Ridge?\n  From Pine Ridge?": "How far is the nearest configured public USGS groundwater monitoring well from the Pine Ridge Census statistical boundary?",
    "both Nations": "multiple jurisdictions",
    "the Tribal-collected well data\n  from `data/raw/`": "other data that could be considered only through a separately approved governance process",
    "The monitoring gap documented here motivates the operational\n  pipeline in `pipeline/groundwater.py`": "The monitoring coverage documented here motivates discussion of what a future, separately governed monitoring workflow would require.",
    "The operational pipeline (`pipeline/groundwater.py`) automates\n  the status classification developed here for ongoing monitoring": "Any future operational classification would require technical validation and explicit OLC/OST approval.",
    "and `pipeline/compute_stages.py`": "for the experimental historical synthesis",
    "The operational pipeline\n(`pipeline/water_quality.py`) automates these threshold checks\nfor ongoing monitoring.": "Automating these checks for operational use is outside the current series and would require validation and approval.",
    "This is a federal infrastructure equity finding, not a data artifact.": "This describes the coverage of the selected public dataset; causes and equity implications require additional evidence and review.",
    "Key finding: recharge rates are much slower than extraction rates in\n  much of the study area under current and projected climate conditions.": "Use the cited aquifer study to compare its spatial scope, assumptions, and period with this notebook before drawing a recharge or extraction conclusion.",
    "data on the Pine Ridge study area is a systemic equity finding. Tribal water\nquality programs are not supplementing federal monitoring, they are\nproviding the only monitoring that exists.": "in the selected public query is a coverage limitation. Causes, program comparisons, and equity implications require additional evidence and OLC/OST review.",
    "Nitrate and arsenic exceedances are more likely anthropogenic (agriculture, septic).": "A screening flag does not identify a contaminant source. Evaluating geogenic or human sources requires site-specific hydrogeologic, land-use, and sampling evidence.",
    "print(\"  pipeline/compute_stages.py operational drought stage trigger\")": "print(\"  Future operational triggers are outside this educational series.\")",
    "USGS NWIS (public), Tribal-collected well data (if available)": "USGS NWIS public groundwater observations and published inventory context",
    "**Tribal-collected data:** Well level measurements from `data/raw/`.\nThese reveal local conditions invisible to the federal monitoring network.": "**Governance boundary:** This public teaching path does not load OST-controlled data. Any future use requires a separately approved process.",
    "**Tribal-collected data:** Well level measurements from `data/raw/`.\nThese reveal local conditions invisible to the federal monitoring network\nand are handled under CARE principles.": "**Governance boundary:** This public teaching path does not load OST-controlled data. Any future use requires a separately approved process.",
    "- What does Tribal-collected well data add that USGS cannot see?": "- What additional evidence or local expertise would be needed to understand conditions not represented by the selected public sites?",
    "USGS/EPA Water Quality Portal (public), Tribal sampling data (if available)": "USGS/EPA Water Quality Portal public observations",
    "- What do Tribal-collected samples show that the public record cannot?": "- What additional evidence or local expertise would be needed to evaluate conditions not represented by the public record?",
    "notebooks 01 and 02. Where Tribal sampling data is available in `data/raw/`,\nit is analyzed separately under CARE governance principles.": "notebooks 01 and 02. This public teaching path does not load OST-controlled data; any future use requires a separately approved process.",
    "- Where are the data gaps that Tribal sampling programs fill?": "- Where does the selected public record have limited spatial, temporal, or parameter coverage?",
    "print(\"Tribal sampling data (data/raw/) fills this gap.\")": "print(\"The selected public record has limited coverage; causes and implications require additional evidence.\")",
    "    print(\"has very limited coverage on the Pine Ridge study area. Tribal sampling\")\n    print(\"programs provide the only ground-level data available.\")": "    print(\"has limited coverage in the configured query. Do not infer that water, local knowledge, or other monitoring is absent.\")",
    "print(\"Tribal-collected well data (data/raw/) fills this gap.\")": "print(\"The selected public record has limited coverage; causes and implications require additional evidence.\")",
    "    # Note: Tribal groundwater data is NOT exported to outputs/ \n    # it stays in data/raw/ under Tribal governance\n": "",
    "print(generate_citations([\"usgs_nwis_groundwater\", \"tribal_groundwater\"]))": "print(generate_citations([\"usgs_nwis_groundwater\"]))",
    "print(generate_citations([\"usgs_nwis_water_quality\", \"tribal_water_quality\"]))": "print(generate_citations([\"usgs_nwis_water_quality\"]))",
    "    print(\"  (or add Tribal well data to data/raw/)\")": "    print(\"  Groundwater is omitted when the configured public record is insufficient.\")",
    "## USGS Monitoring Coverage: The Gap as Equity Finding": "## Public USGS Monitoring Coverage",
    "print(f\"Boundaries loaded from notebook 01: {len(study_boundary)} Nations\")": "print(f\"Boundary features loaded from notebook 01: {len(study_boundary)}\")",
    "print(f\"Boundaries downloaded: {len(study_boundary)} Nations\")": "print(f\"Boundary features downloaded: {len(study_boundary)}\")",
    "print(f\"Nations: {len(study_boundary)} | Primary: {len(primary)}\")": "print(f\"Boundary features: {len(study_boundary)} | Selected study feature: {len(primary)}\")",
}


def markdown_cell(text: str) -> dict:
    lines = text.strip().splitlines()
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in lines[:-1]] + [lines[-1]],
    }


def scaffold(module: dict) -> str:
    objectives = "\n".join(f"- {item}" for item in module["objectives"])
    return f"""
## Learning Objectives

By the end of this notebook, learners will be able to:

{objectives}

## Prerequisites and Timing

Allow approximately 75–100 minutes. Before beginning, activate the repository environment, read the series governance statement, and complete the preceding notebook where applicable. Work in pairs and rotate analyst, data-steward, skeptic, and documentarian roles.

## Governance Checkpoint

This notebook uses public environmental data describing Oglala Lakota lands and waters. Public availability does not establish permission for every reuse or interpretation. Do not add OST-controlled data, sensitive locations, or community knowledge. Results are educational and screening-level pending OLC/OST review.
"""


def learning_close(module: dict) -> str:
    return f"""
## Learner Checkpoint

{module['checkpoint']}

## Interpretation Protocol

Before writing a conclusion, separate:

1. **Observation:** what the computed public data show, including unit, period, spatial scope, and missingness.
2. **Interpretation:** a plausible explanation, stated with uncertainty.
3. **Additional evidence:** literature, local monitoring, expertise, or validation needed to evaluate that explanation.
4. **Decision authority:** who is authorized to approve publication, thresholds, or management action.

Do not convert monitoring absence, association, a screening flag, or scenario output into a causal, regulatory, health, policy, or community conclusion.

## Contribution Activity

{module['contribution']} Review the change with a partner and record what became clearer or more defensible.

## Evidence Record and Next Step

Record one regenerated result, its source and scope, one transformation, one limitation, and one question requiring more evidence or local knowledge.

{module['next']}
"""


def main() -> None:
    for path in sorted(NOTEBOOK_DIR.glob("[0-9][0-9]_*.ipynb")):
        number = path.name[:2]
        module = MODULES[number]
        notebook = json.loads(path.read_text(encoding="utf-8"))

        # Make the transformation idempotent.
        notebook["cells"] = [
            cell for cell in notebook["cells"]
            if not (
                cell.get("cell_type") == "markdown"
                and any(
                    marker in "".join(cell.get("source", []))
                    for marker in ("## Learning Objectives", "## Learner Checkpoint", "## Summary and Findings")
                )
            )
        ]

        # Remove optional restricted-data sections from the public teaching path.
        public_cells = []
        skipping_restricted_section = False
        for cell in notebook["cells"]:
            source = "".join(cell.get("source", []))
            if cell.get("cell_type") == "markdown" and source.startswith("## Load Tribal-Collected"):
                skipping_restricted_section = True
                continue
            if skipping_restricted_section:
                if cell.get("cell_type") == "markdown" and source.startswith("## "):
                    skipping_restricted_section = False
                else:
                    continue
            public_cells.append(cell)
        notebook["cells"] = public_cells

        for cell in notebook["cells"]:
            if cell.get("cell_type") == "code":
                cell["execution_count"] = None
                cell["outputs"] = []
            source = "".join(cell.get("source", []))
            for old, new in REPLACEMENTS.items():
                source = source.replace(old, new)

            if number == "02":
                source = source.replace("    load_tribal_groundwater,\n", "")
                source = re.sub(
                    r"\*\*Tribal-collected data:\*\*.*?(?=\n## Research Questions)",
                    "**Governance boundary:** This public teaching path does not load OST-controlled data. Any future use requires a separately approved process.\n",
                    source,
                    flags=re.DOTALL,
                )
            if number == "04":
                source = source.replace("    load_tribal_water_quality,\n", "")
                source = source.replace(
                    "for the study area, the same monitoring infrastructure gap documented in\nnotebooks 01 and 02. Where Tribal sampling data is available in `data/raw/`,\nthis notebook shows both side by side.",
                    "in the configured query. This is a limitation of the selected public record, not evidence that water, knowledge, local monitoring, or community concern is absent. This public teaching path does not load OST-controlled data.",
                )
                source = source.replace(
                    "    print(\"FINDING: Absence of public WQ monitoring data in this area\")\n    print(\"is itself a significant equity finding. The Water Quality Portal\")\n    print(\"has very limited coverage on the Pine Ridge study area. Tribal sampling\")\n    print(\"programs provide the only systematic record of drinking water quality.\")",
                    "    print(\"The configured public query returned limited coverage.\")\n    print(\"Do not infer that water, local knowledge, or other monitoring is absent.\")\n    print(\"Causes and implications require additional evidence and review.\")",
                )
                source = re.sub(
                    r"\n# Tribal data.*?(?=\n#|\Z)", "", source, flags=re.DOTALL
                )
                source = re.sub(
                    r"\nif not tribal_wq_flagged\.empty:\n    datasets\.append\([^\n]+\)\n",
                    "\n",
                    source,
                )
                source = re.sub(
                    r"\n# Tribal WQ data:.*\Z", "\n", source, flags=re.DOTALL
                )
            if cell.get("source"):
                cell["source"] = source.splitlines(keepends=True)

        if number == "02":
            notebook["cells"] = [
                cell for cell in notebook["cells"]
                if "tribal_gw" not in "".join(cell.get("source", []))
            ]

        notebook["cells"].insert(1, markdown_cell(scaffold(module)))
        notebook["cells"].append(markdown_cell(learning_close(module)))
        for cell in notebook["cells"]:
            cell.setdefault("id", uuid.uuid4().hex[:8])
        path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
