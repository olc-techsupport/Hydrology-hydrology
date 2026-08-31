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
