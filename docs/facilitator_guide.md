# Facilitator guide: Pine Ridge Hydrology

## Purpose and audience

This seven-session series introduces reproducible hydrologic analysis using public data describing the Pine Ridge Reservation and hydrologically connected areas. It is intended for OLC learners, instructors, project staff, and community collaborators with mixed coding experience. Learners do not need to understand every line of Python before participating.

The series teaches analytical mechanics and careful interpretation. It does not authorize use of OST-controlled data, establish management thresholds, or present findings approved by OST or OLC.

## Before the series

- Confirm the current governance and release status with the designated OLC/OST reviewer.
- Provide a tested environment or a preconfigured computer lab. Do not spend the first session debugging individual Conda installations if a shared environment is available.
- Run `python scripts/execute_notebooks.py` and `python -m pytest` before meeting learners.
- Review the public data sources, cached-download plan, and any internet restrictions.
- Do not introduce OST-controlled data unless a separately approved access, storage, analysis, and publication process is in place.

## Repeating session pattern

Each notebook is designed for approximately 75–100 minutes:

1. **Orient (10 minutes):** read the purpose, learning objectives, governance checkpoint, and research questions.
2. **Predict (10 minutes):** learners record what they expect and what evidence could change their view.
3. **Run and inspect (30–40 minutes):** execute code in pairs and pause at checkpoints.
4. **Interpret (15–20 minutes):** separate observations, interpretations, outside evidence, and decisions.
5. **Contribute (10–20 minutes):** make one small documentation, test, provenance, or visualization improvement and review it with a partner.

For a shorter demonstration, use notebooks 01 and 03 and omit the contribution activity. Do not compress governance or limitations discussions.

## Mixed-skill roles

- **Facilitator:** protects time, inclusion, and shared understanding.
- **Data steward:** checks provenance, permissions, scope, and metadata.
- **Analyst:** runs transformations and explains what the code produces.
- **Skeptic:** asks what the data cannot support and looks for alternative explanations.
- **Documentarian:** records decisions, questions, and limitations in plain language.
- **Reviewer:** checks whether another learner could reproduce the result.

Rotate roles. Reading, documenting, questioning, and reviewing are technical contributions.

## Session map

| Session | Core skill | Interpretation focus | Suggested learner contribution |
|---|---|---|---|
| 01 Watersheds | Spatial joins and scale | Statistical boundaries versus hydrologic context | Clarify a map label or boundary caveat |
| 02 Groundwater | Time series and robust trends | Monitoring evidence versus monitoring absence | Document one site and its record limits |
| 03 Surface water | Seasonal flow and reliability | Screening thresholds versus approved triggers | Add a unit or threshold-status note |
| 04 Water quality | Units, benchmarks, and missingness | Exceedance flag versus health or regulatory conclusion | Check one parameter’s unit and source |
| 05 Drought | Regional proxy data | Association versus causation | Explain one limitation of PDSI Division 7 |
| 06 Compound stress | Normalization and weights | Value judgments embedded in an index | Compare and document an alternate weighting |
| 07 Climate | Scenarios and model uncertainty | Projection versus forecast | Rewrite one claim with uncertainty intact |

## Interpretation protocol

Ask teams to report findings in four columns:

| Observation | Interpretation | Additional evidence needed | Decision authority |
|---|---|---|---|
| What the computed data show | A plausible explanation | Literature, local monitoring, expertise, or validation needed | Who is authorized to decide or publish |

Do not allow a policy conclusion to be presented as a direct output of a graph. Monitoring gaps may motivate questions about infrastructure equity, but claims about causes, investment, program performance, or community conditions require appropriate evidence and review.

## Inclusive review activity

Give each team a small change: a clearer label, provenance note, limitation, assertion, or glossary definition. One learner proposes the change, another asks one substantive question, and the author revises it. Review should test whether the work is understandable and defensible, not whether the author belongs in technical work.

## Common sticking points

- Environment activation and selecting the correct notebook kernel
- Distinguishing a notebook cell from reusable source code
- Network timeouts and cached data
- Missing values, uneven monitoring periods, and mixed units
- Interpreting depth-to-water direction correctly
- Treating correlation, thresholds, or scenario output as causal or predictive
- Confusing a Census statistical boundary with a legal or community-defined boundary

Normalize these difficulties. Pair learners, provide copy-and-paste commands, and explain that the first pass is about following the evidence trail rather than memorizing syntax.

## Governance pause conditions

Stop the activity and contact the appropriate steward if a proposed change would add restricted data, sensitive locations, community knowledge, individual-level information, or an external publication claim. A `.gitignore` rule is not a governance agreement.

## Completion evidence

A learner has completed the series when they can:

- locate the configuration and data-source record;
- rerun an analysis and identify its generated artifact;
- explain at least one transformation and one limitation;
- distinguish observation from interpretation and decision;
- identify who must review a sensitive or external claim; and
- make and review a small reproducibility improvement.
