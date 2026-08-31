from __future__ import annotations

"""Execute the ordered notebook series and keep committed notebooks clean."""

import argparse
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]


def execute(path: Path, timeout: int, skip_plots: bool) -> None:
    notebook = nbformat.read(path, as_version=4)
    original_sources = [cell.source for cell in notebook.cells]
    if skip_plots:
        for cell in notebook.cells:
            if cell.cell_type == "code" and (
                "plt.subplots" in cell.source or "plt.figure" in cell.source
            ):
                cell.source = "print('Plot cell skipped during non-visual validation run.')"
    client = NotebookClient(
        notebook,
        timeout=timeout,
        kernel_name="tribal-water",
        resources={"metadata": {"path": str(path.parent)}},
        on_cell_start=lambda cell, cell_index: print(
            f"  cell {cell_index}: {''.join(cell.get('source', [])).splitlines()[0][:70] if cell.get('source') else '<empty>'}",
            flush=True,
        ),
    )
    client.execute()
    for cell, source in zip(notebook.cells, original_sources):
        cell.source = source
        if cell.cell_type == "code":
            cell.outputs = []
            cell.execution_count = None
    nbformat.write(notebook, path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument(
        "--include-plots", action="store_true",
        help="Execute plotting cells. Omit for a portable data-path validation run.",
    )
    args = parser.parse_args()
    notebooks = sorted((ROOT / "notebooks").glob("*.ipynb"))
    if len(notebooks) != 7:
        raise RuntimeError(f"Expected seven notebooks; found {len(notebooks)}")
    for path in notebooks:
        print(f"Executing {path.name}", flush=True)
        execute(path, args.timeout, skip_plots=not args.include_plots)


if __name__ == "__main__":
    main()
