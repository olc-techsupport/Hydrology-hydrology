# OLC/OST review checklist

## Deferred governance review

- [ ] Confirm preferred names for OST, Oglala Lakota people, OLC, and Pine Ridge Reservation.
- [ ] Approve or replace the draft OST RRB/OLC IRB language.
- [ ] Confirm Camille Griffith's preferred title and contact listing.
- [ ] Decide which Indigenous data-governance frameworks should be named.
- [ ] Define review requirements for public environmental data about OST lands.

## Scientific review

- [ ] Review the territorial boundary and hydrologic context envelope.
- [ ] Review every configured monitoring site and inclusion rationale.
- [ ] Confirm climate division 7 as an acceptable drought proxy.
- [ ] Review threshold labels and prevent operational interpretation.
- [ ] Review water-quality parameter units and benchmark sources.
- [ ] Review compound-index weights and uncertainty communication.

## Attribution and release

- [ ] Add the complete NIFA award name and number.
- [ ] Decide author order, OLC departmental attribution, and copyright ownership.
- [ ] Add `CITATION.cff` after attribution is approved.
- [ ] Confirm which generated outputs should remain versioned.
- [ ] Record approval status and date without implying endorsement before approval.

## Instructional review

- [ ] Confirm that the learning outcomes match the intended NIFA audience and award scope.
- [ ] Pilot each notebook with at least one learner who is new to Python.
- [ ] Review estimated timing, prerequisite language, and mixed-skill activities.
- [ ] Check that prompts separate observations, interpretations, outside evidence, and decisions.
- [ ] Remove or qualify causal, infrastructure, health, regulatory, and management claims not established by the analysis.
- [ ] Confirm that contribution activities do not invite learners to add restricted data.
- [ ] Record pilot feedback and resulting revisions.

## Technical release checks

- [ ] Run `python -m pytest` and `python scripts/execute_notebooks.py` in a clean environment.
- [ ] Confirm every committed artifact is present in `outputs/provenance_manifest.csv`.
- [ ] Update regeneration dates and review status in the manifest.
- [ ] Review notebook outputs and figures for sensitive information before committing.
- [ ] Create and document a resolved environment lock for the approved delivery platform.
