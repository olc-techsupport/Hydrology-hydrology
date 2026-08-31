from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = sorted((ROOT / "notebooks").glob("*.ipynb"))


def code_source(path: Path) -> str:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    return "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook["cells"]
        if cell["cell_type"] == "code"
    )


def test_series_has_seven_ordered_notebooks() -> None:
    assert [path.name[:2] for path in NOTEBOOKS] == [f"{i:02d}" for i in range(1, 8)]


def test_notebooks_contain_no_removed_scope_terms() -> None:
    removed_terms = ("rosebud", "sicangu", "oceti_sakowin", "all_streamgages")
    for path in NOTEBOOKS:
        text = path.read_text(encoding="utf-8").lower()
        assert not any(term in text for term in removed_terms), path.name


def test_notebook_code_is_syntactically_valid() -> None:
    for path in NOTEBOOKS:
        source = "\n".join(
            line for line in code_source(path).splitlines()
            if not line.lstrip().startswith(("%", "!"))
        )
        ast.parse(source, filename=path.name)


def test_committed_notebooks_have_no_saved_outputs() -> None:
    for path in NOTEBOOKS:
        notebook = json.loads(path.read_text(encoding="utf-8"))
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                assert cell.get("outputs", []) == []
                assert cell.get("execution_count") is None
