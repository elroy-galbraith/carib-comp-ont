---
class: Obligation
id: dpa2020_obligation_lawful_processing
label: Obligation to Process Personal Data Lawfully
uri: https://ontology.carib-comp.org/compliance/entity/dpa2020_obligation_lawful_processing
source_document: dpa2020
source_section: "§10"
source_text: >
  A data controller shall ensure that personal data are processed in accordance
  with the data protection principles set out in the First Schedule.
properties:
  imposesObligationOn: "[[dpa2020_s2_data_controller]]"
  applicableTo: "[[dpa2020_s2_personal_data]]"
  partOfStatute: "[[dpa2020]]"
prompt_version: manual-v1
model_snapshot: hand-curated
validation: PASS
---

## Obligation to Process Personal Data Lawfully

**Source:** §10 and the First Schedule of the Data Protection Act 2020.

> A data controller shall ensure that personal data are processed in accordance
> with the data protection principles set out in the First Schedule.

### Data Protection Principles (First Schedule)

1. **Lawfulness, fairness and transparency** — personal data shall be processed lawfully, fairly and in a transparent manner in relation to the data subject
2. **Purpose limitation** — collected for specified, explicit and legitimate purposes and not further processed in a manner incompatible with those purposes
3. **Data minimisation** — adequate, relevant and limited to what is necessary
4. **Accuracy** — accurate and, where necessary, kept up to date
5. **Storage limitation** — kept in a form that permits identification of data subjects for no longer than is necessary
6. **Integrity and confidentiality** — processed in a manner that ensures appropriate security

### Obligation bearer

`cco:imposesObligationOn cco:dpa2020_s2_data_controller` — the data controller is the primary bearer of this obligation.
