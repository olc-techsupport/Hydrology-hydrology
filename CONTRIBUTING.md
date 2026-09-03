# Contributing

This repository is maintained for the Oglala Lakota College Math and Science Department and is currently limited to the Pine Ridge Reservation and documented hydrologic context.

Before proposing a change:

1. Do not add OST-collected or sensitive operational data.
2. Put study scope, sites, dates, and thresholds in `config/config.yaml` rather than notebook-local constants.
3. Give every off-boundary monitoring site a clear hydrologic rationale.
4. Preserve the distinction between a Census statistical boundary, OST lands, and hydrologic context.
5. Label thresholds and compound indicators as screening-level unless formal approval is documented.
6. Run `python -m pytest -q` and `python scripts/execute_notebooks.py`.
7. Review every generated artifact before committing it.

Governance wording and external release remain subject to OST RRB/OLC IRB review. Contact Camille Griffith, PhD (`cgriffith@olc.edu`) for interim review coordination; listing her does not imply approval.

## Learner-sized contributions

Small improvements are welcome: clarify a unit or label, add a provenance note, strengthen a limitation, improve a glossary link, or add a test for an existing transformation. In a workshop, pair the author with a reviewer who asks whether a future learner can reproduce and interpret the result.

Do not add OST-controlled data, sensitive locations, community knowledge, new operational thresholds, or external-facing claims through an ordinary pull request. Pause and use the approved governance and review process described in `docs/data_sovereignty.md`.

Before proposing a change, run:

```powershell
python -m pytest
python scripts/execute_notebooks.py
```

Update `outputs/provenance_manifest.csv` when a committed artifact is regenerated. Notebook changes should be committed without saved cell outputs; deliberate figures and tables belong in `outputs/` with their review status recorded.
