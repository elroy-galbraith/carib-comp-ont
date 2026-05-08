# Outreach Email Draft

---

## Email A — Charlette Donalds

**To:** [charlette.donalds@uwimona.edu.jm]  
**Subject:** Complementary privacy-compliance ontology — DPA 2020 / your cybercrime work

Dear Dr Donalds,

Your 2023 paper "Towards a Cybercrime Classification Ontology for Developing
Countries" (co-authored with Dr Barclay and Prof Osei-Bryson) directly motivated
the work I am writing to share with you. You identified the gap in structured
representations of Caribbean cyber-law; I have been building a complementary
artifact focused on the privacy-compliance side — specifically the Jamaica Data
Protection Act 2020.

I have a working prototype: a curator-agent loop that converts statute sections
into reviewable git PRs against a FIBO-aligned OWL schema. The prototype answers
three competency questions via SPARQL against an Oxigraph instance loaded from
the vault. It is CLI-only, MIT-licensed, and designed to be cloned and inspected
in under fifteen minutes.

I am attaching a one-page summary and a link to a two-minute screen recording
[link to be added after recording]. The full repository is at
https://github.com/[your-handle]/carib-comp-ont.

I have a few specific questions where your expertise would be invaluable:

1. Have you encountered any FIBO-aligned compliance ontologies in the Caribbean
   — including unreleased or grant-funded work — that I should be engaging with?
2. Where do you see the natural seams between cybercrime classification and
   privacy compliance? The data-breach / notification-obligation intersection
   seems real and worth surfacing.
3. Would you be open to reviewing the schema in an advisory capacity before the
   Phase 2 freeze? Even a single exchange of feedback would be valuable.
4. Is there a UWI-affiliated venue — workshop track, special issue — where this
   methodology and case study would land well alongside or in addition to ICEGOV?

I want to be clear that I am framing this as complementary work, not competition.
Your cybercrime classification provides a layer that mine does not; my
privacy-compliance layer provides coverage yours does not. Alignment between the
two is a Phase 2 goal, and I would value your input on how to approach it.

Thank you for your time.

Best regards,  
Elroy Galbraith  
elroy.galbraith@gmail.com

---

## Email B — Corlane Barclay

**To:** [corlane.barclay@uwimona.edu.jm]  
**Subject:** DPA 2020 ontology prototype — legal-informatics angle

Dear Dr Barclay,

I am reaching out because your work with Dr Donalds and Prof Osei-Bryson on
cybercrime classification has been a direct influence on a privacy-compliance
prototype I have been building. The legal-informatics angle of that paper — the
attention to how Caribbean legal structures translate into formal knowledge
representations — is exactly the framing I am trying to apply to the Jamaica
Data Protection Act 2020.

I have built a small end-to-end prototype: a curator-agent loop that converts
statute sections into reviewable git branches against a FIBO-aligned OWL schema,
with competency questions answered via SPARQL. The one-page summary attached
describes the methodology and the artifact.

I am particularly interested in your view on two things:

1. The privacy-compliance and cybercrime domains intersect at incident-response
   obligations (data breach → DPA notification duty + Cybercrimes Act offence).
   Are there additional legal seams you see between the two bodies of legislation?
2. Is there a UWI venue — a workshop, a journal special issue — where a joint
   or aligned presentation of these two ontologies would fit?

I would welcome any feedback, even brief.

Best regards,  
Elroy Galbraith  
elroy.galbraith@gmail.com

---

## Email C — Kweku-Muata Osei-Bryson

**To:** [kweku-muata.osei-bryson@uwimona.edu.jm]  
**Subject:** Curator-agent methodology for statute ontology — seeking methodological feedback

Dear Prof Osei-Bryson,

I am a researcher working on a privacy-compliance ontology for Caribbean
jurisdictions, motivated in part by your group's cybercrime classification work.
I am writing specifically because of your methodological rigour — I want to
stress-test the time-cost study design before committing to it.

The prototype uses a curator-agent loop: a single-shot LLM call (Claude Haiku,
JSON-Schema-constrained) converts a statute section to structured entities, which
arrive as a git PR for human review. The plan is to run a two-author time-cost
study comparing (a) manual curation and (b) LLM-assisted curation of the same
statute sections, with inter-annotator agreement measured against a gold
standard.

My questions for you:

1. The two-author design is standard for annotation agreement studies. Is there
   a design variation you would recommend for this kind of semi-automated
   pipeline, where the human is reviewing LLM output rather than starting from
   scratch?
2. I am considering ICEGOV as the primary venue. Given the Caribbean
   development-computing angle, is there a venue you think is a better fit or
   a complementary submission target?
3. Would you be willing to review the methodology section of the Phase 2 paper
   draft before submission?

I attach a one-page summary and a two-minute demo recording [link TBA].

Thank you for your consideration.

Best regards,  
Elroy Galbraith  
elroy.galbraith@gmail.com

---

## Send checklist

- [ ] Record the two-minute demo and obtain a shareable link
- [ ] Update GitHub URL in all three emails
- [ ] Verify email addresses via UWI staff directory
- [ ] Attach `docs/outreach/one_pager.md` (or export to PDF first)
- [ ] Send Donalds and Barclay emails on the same day (they co-authored)
- [ ] Send Osei-Bryson email 1–2 days later with a personalised subject
- [ ] If no response in 14 days, send a single short follow-up per person
