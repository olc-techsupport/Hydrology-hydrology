from __future__ import annotations

import json
import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = sorted((ROOT / "notebooks").glob("[0-9][0-9]_*.ipynb"))

REQUIRED_MARKERS = (
    "## Learning Objectives",
    "## Prerequisites and Timing",
    "## Governance Checkpoint",
    "## Learner Checkpoint",
    "## Interpretation Protocol",
    "## Contribution Activity",
)

STALE_OR_UNAUTHORIZED_PHRASES = (
    "both nations",
    "pipeline/groundwater.py",
    "pipeline/water_quality.py",
    "pipeline/compute_stages.py",
    "tribal-collected well data from `data/raw/`",
)


def notebook_markdown(path: Path) -> str:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    return "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook["cells"]
        if cell["cell_type"] == "markdown"
    )


def test_series_has_seven_ordered_notebooks() -> None:
    assert [path.name[:2] for path in NOTEBOOKS] == [f"{number:02d}" for number in range(1, 8)]


def test_each_notebook_has_instructional_scaffolding() -> None:
    for path in NOTEBOOKS:
        markdown = notebook_markdown(path)
        for marker in REQUIRED_MARKERS:
            assert marker in markdown, f"{path.name} is missing {marker}"


def test_notebooks_do_not_reference_removed_scope_or_nonexistent_pipeline() -> None:
    for path in NOTEBOOKS:
        text = path.read_text(encoding="utf-8").lower()
        for phrase in STALE_OR_UNAUTHORIZED_PHRASES:
            assert phrase not in text, f"{path.name} contains stale phrase: {phrase}"


def test_notebook_json_and_code_cell_contract() -> None:
    for path in NOTEBOOKS:
        notebook = json.loads(path.read_text(encoding="utf-8"))
        assert notebook.get("nbformat") == 4
        assert any(cell["cell_type"] == "code" for cell in notebook["cells"])
        assert all(cell.get("id") for cell in notebook["cells"])


def test_committed_notebooks_are_clean_and_code_is_syntactically_valid() -> None:
    for path in NOTEBOOKS:
        notebook = json.loads(path.read_text(encoding="utf-8"))
        code = []
        for cell in notebook["cells"]:
            if cell["cell_type"] != "code":
                continue
            assert cell.get("execution_count") is None
            assert cell.get("outputs", []) == []
            code.extend(
                line for line in "".join(cell.get("source", [])).splitlines()
                if not line.lstrip().startswith(("%", "!"))
            )
        ast.parse("\n".join(code), filename=path.name)


def test_committed_data_artifacts_have_manifest_entries() -> None:
    manifest = (ROOT / "outputs" / "provenance_manifest.csv").read_text(encoding="utf-8")
    excluded = {
        "README.md",
        "provenance_manifest.csv",
        # Reproducible intermediate geospatial extracts are intentionally ignored.
        "nhd_streams_primary.geojson",
        "pine_ridge_context_streams.geojson",
    }
    artifacts = {
        path.name for path in (ROOT / "outputs").iterdir()
        if path.is_file() and path.name not in excluded
    }
    assert artifacts
    for artifact in artifacts:
        assert f"\n{artifact}," in manifest, f"missing manifest entry for {artifact}"
