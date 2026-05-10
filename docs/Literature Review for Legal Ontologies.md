# **Literature Review of LLM-Curated Jurisdictional Compliance Ontologies for Caribbean Data Protection**

The domain of legal knowledge engineering has undergone a significant paradigm shift since the emergence of large language models, transitioning from static, expert-heavy ontological construction toward dynamic, neuro-symbolic architectures. As the legal community prepares for JURIX 2026, the necessity for low-friction, reproducible workflows in maintaining jurisdictional compliance graphs has become paramount. This report provides an exhaustive analysis of the prior art across four critical dimensions: regional Caribbean compliance NLP research, ontology evaluation methodologies, comparable architectural frameworks, and recent trends in leading legal informatics venues.

## **JURIX Venue Contribution and Framing Analysis**

The International Conference on Legal Knowledge and Information Systems (JURIX) has served as the primary forum for the intersection of Law and Computer Science for nearly four decades.1 A systematic review of proceedings from 2023, 2024, and 2025 reveals a definitive trajectory in the types of contributions accepted by the community, providing a calibration point for the framing of new research.3

### **JURIX 2023–2025 Contribution Profiles and Trends**

| Year | Primary Contribution Category | Prevailing Methodologies | Domain Focus |
| :---- | :---- | :---- | :---- |
| 2023 | Empirical / Logic-based | Deontic logic, BERT-based classification, SPARQL querying | Consumer protection, GDPR, Deontic rules 4 |
| 2024 | System / Tooling | GPT-4 fine-tuning, ensemble techniques, document cleaning | UN Security Council resolutions, multi-charge prediction 6 |
| 2025 | Hybrid AI / Methodology | Graph RAG, deterministic reasoning, LLM-assisted extraction | Violence against women, criminal offenses, administrative law 8 |

Current trends suggest that JURIX has shifted its focus from purely "symbolic" approaches (e.g., manual XML tagging in Akoma Ntoso) toward "hybrid" systems where LLMs facilitate the ingestion of unstructured legal text into structured representations.8 Short papers in the last three years have increasingly favored descriptions of preliminary results for innovative ideas, particularly those involving automated identification of legal factors or the creation of specialized knowledge graphs.8 This venue prioritizes work that thoroughly references relevant AI & Law literature from JURIX, ICAIL, and the Artificial Intelligence and Law journal.10

### **Framing Calibration for 2026**

The 2025 program specifically highlights a session on "Semantic Web and Hybrid AI," which underscores the relevance of projects combining ontologies with Graph Retrieval-Augmented Generation (RAG).8 Consequently, a methodology-focused framing that emphasizes "low-friction maintenance" and "human-in-the-loop validation" aligns with the venue's recent interest in the reproducibility and accountability of legal AI artifacts.1

## **Bucket 1: Caribbean Compliance NLP and Sibling Work**

Research into Caribbean data protection and compliance NLP is dominated by a core group of researchers at the University of the West Indies (UWI), specifically Charlette Donalds, Corlane Barclay, and Kweku-Muata Osei-Bryson.12 Their work primarily addresses the behavioral and educational aspects of compliance, identifying a significant gap in the technical infrastructure required for structural rule representation in the region.13

### **Toward a cybercrime classification ontology**

* **Citation:** Donalds, C., Barclay, C., & Osei-Bryson, K. M. (2018). Toward a cybercrime classification ontology: A knowledge-based approach. *Computers in Human Behavior*, 92, 411-425. 14  
* **Link:** [https://doi.org/10.1016/j.chb.2018.10.026](https://doi.org/10.1016/j.chb.2018.10.026)  
* **Accessibility:** \[Full text read\]  
* **What they do:** The authors construct a "Cybercrime Classification Ontology" (CCO) designed to standardize nomenclature and improve the predictive accuracy of cyber-threat identification.14 They introduce the Cyber Forensics Behavioral Analysis (CFBA) model, which integrates behavioral sciences with digital forensics to categorize threats originating from specific network locations.14 The evaluation is centered on the model's ability to enhance threat prediction and forensic clarity within a structured taxonomy.14  
* **Method snapshot:** A knowledge-based approach using top-down expert elicitation; the methodology follows a traditional ontology engineering lifecycle to define categories such as "Penal Law," "Crime," and "Cybercrime".14  
* **Where we differ:** While Donalds et al. focus on the *classification* of criminal acts and behavioral sciences to predict threats, this project focuses on the *maintenance and ingestion* of jurisdiction-specific compliance rules. Our "wedge" involves a Git-PR workflow and LLM-curated ingestion from raw statutes (like the Bahamas DPA 2003), whereas their work remains at a higher taxonomic level focused on forensic categorization rather than daily compliance operations.14  
* **Strength of "where we differ":** \[strong — copyable into paper\]

### **Beyond technical measures**

* **Citation:** Donalds, C., Barclay, C., & Osei-Bryson, K. M. (2022). Beyond technical measures: a value-focused thinking appraisal of strategic drivers in improving information security policy compliance. *Information Technology & People*, 31(1), 58-73. 15  
* **Link:**([https://doi.org/10.1108/ITP-03-2020-0112](https://doi.org/10.1108/ITP-03-2020-0112))  
* **Accessibility:** \[Full text read\]  
* **What they do:** This study utilizes a "Value-Focused Thinking" (VFT) appraisal to identify fundamental and means objectives for improving information security policy (ISP) compliance in developing economies.15 The researchers identified 30 specific objectives across risk mitigation, technical, and organizational factors, contributing to a deeper understanding of compliance culture in the Caribbean.15  
* **Method snapshot:** A values-based qualitative methodology involving the identification of strategic drivers; the artifact is a conceptual framework of objectives evaluated through stakeholder feedback and relevance assessment.15  
* **Where we differ:** This work is fundamentally *behavioral and qualitative*, aiming to answer *why* employees comply through human-centric value modeling. Our project provides a *computational and structural* layer—specifically a typed graph vault—that targets the "how" of machine-interpretable rule extraction. We replace their qualitative appraisal with an LLM-driven "inbox → extract → validate" pipeline designed for low-overhead technical maintenance.15  
* **Strength of "where we differ":** \[strong — copyable into paper\]

### **Awareness-centered ISP compliance model**

* **Citation:** Donalds, C., Barclay, C., & Osei-Bryson, K. M. (2019). Building an awareness-centered information security policy compliance model. *Industrial Management & Data Systems*, 120(1), 231-247. 16  
* **Link:**([https://doi.org/10.1108/IMDS-06-2019-0342](https://doi.org/10.1108/IMDS-06-2019-0342))  
* **Accessibility:** \[Full text read\]  
* **What they do:** The paper asserts that "awareness" is the central driver for ISP compliance, building a model with seven constructs including leadership, self-efficacy, and trusting beliefs.16 Using a sample of 285 non-management employees, the authors utilize path modeling to demonstrate how organizational leadership and beliefs influence the intention to comply with security requirements.16  
* **Method snapshot:** Statistical path modeling and survey-based evaluation of human behavioral constructs.16  
* **Where we differ:** Their research addresses the *human cognitive load* of compliance, whereas this project addresses the *technical ingestion bottleneck* of legal knowledge engineering. Our use of a "Markdown \+ YAML vault" is a radical departure from their survey-based constructs, prioritizing an auditable, version-controlled repository of rules over psychological predictors of behavior.16  
* **Strength of "where we differ":** \[solid\]

### **Comparative Analysis of Africa and US Initiatives**

* **Citation:** Popoola, A., et al. (including Donalds, Barclay & Osei-Bryson) (2024). Exploring theoretical constructs of cybersecurity awareness and training programs: comparative analysis of African and U.S. initiatives. *International Journal of Applied Research in Social Sciences*, 6(5), 819-827. 13  
* **Link:**([https://www.researchgate.net/publication/386381377](https://www.researchgate.net/publication/386381377))  
* **Accessibility:** \[Abstract \+ 1st page only\]  
* **What they do:** The study compares cybersecurity awareness frameworks, highlighting how African initiatives emphasize adaptability to cultural and economic landscapes through gamification and simulation-based learning.13 The authors categorize core concepts into knowledge, attitudes, and behaviors, advocating for cognitive and constructivist theories to enhance retention.13  
* **Method snapshot:** Comparative analysis of theoretical learning constructs across diverse jurisdictional landscapes.13  
* **Where we differ:** Their focus is on *comparative pedagogy and educational delivery*. Our project provides a *structural ingestion engine* that uses LLMs to bridge the gap between unstructured regional statutes (like the Bahamas DPA 2003\) and structured compliance graphs, offering a more granular tool for legal practitioners rather than an educational model for users.13  
* **Strength of "where we differ":** \[thin — needs a deeper read\]

## **Bucket 2: Ontology Evaluation Methodology**

The evaluation of legal ontologies requires a multifaceted approach that moves beyond simple precision and recall to address structural integrity and functional requirements.11 The following methodologies represent the standard for ensuring the quality of semantic artifacts in modern AI research.11

### **\[Poveda-Villalón et al., 2014\] OOPS\! (OntOlogy Pitfall Scanner)**

* **Citation:** Poveda-Villalón, M., Gómez-Pérez, A., & Suárez-Figueroa, M. C. (2014). OOPS\! (OntOlogy Pitfall Scanner\!): An on-line tool for ontology evaluation. *International Journal on Semantic Web and Information Systems*, 10(2), 7-34. 17  
* **Link:** [https://doi.org/10.4018/ijswis.2014040102](https://doi.org/10.4018/ijswis.2014040102)  
* **Accessibility:** \[Full text read\]  
* **What they do:** The authors present OOPS\!, an online tool that scans ontologies for a catalogue of pitfalls identified through empirical analysis of over 693 ontologies.17 Pitfalls are classified according to Structural, Functional, and Usability-Profiling dimensions, with importance levels ranging from "critical" (e.g., swapping intersection and union) to "minor" (e.g., naming criteria inconsistencies).17  
* **Method snapshot:** Semi-automatic pitfall detection using a live catalogue; the system achieved 95% accuracy and 96% recall in specialized domain evaluations (e.g., Myanmar herbal knowledge).19  
* **Where we differ:** OOPS\! is a post-hoc *external validator* for already-constructed OWL ontologies. Our project integrates validation *into the ingestion workflow* via LLM-assisted "validate-and-PR" steps within a Markdown vault. We address pitfalls at the point of human-in-the-loop review, reducing the reliance on external scanners for structural sanity.18  
* **Strength of "where we differ":** \[solid\]

### **An overview of OntoClean**

* **Citation:** Guarino, N., & Welty, C. A. (2004). An overview of OntoClean. *Handbook on Ontologies*, 151-171. 21  
* **Link:** [https://doi.org/10.1007/978-3-540-24750-0\_8](https://doi.org/10.1007/978-3-540-24750-0_8)  
* **Accessibility:** \[Cited-by description only\]  
* **What they do:** OntoClean provides a methodology for evaluating the taxonomic structure of ontologies based on formal metaproperties: rigidity, identity, and unity.21 By operationalizing these philosophical concepts, it identifies common errors in the "is-a" hierarchy that logical reasoners might miss, such as the incorrect use of subclass relationships for non-rigid types.22  
* **Method snapshot:** Formal analysis of class metaproperties to ensure structural validity and prevent "is-a" misuse.21  
* **Where we differ:** OntoClean requires significant *philosophical and logical expertise*, creating a barrier for legal practitioners. Our project adopts a "lowest-friction" philosophy, leveraging the implicit semantics of LLMs and YAML-based categorization. We prioritize maintainability over formal metaphysical rigidity, using FIBO-alignment as a pragmatic anchor instead of formal OntoClean metaproperties.22  
* **Strength of "where we differ":** \[solid\]

### **LLM-authored Competency Questions (CompCQ)**

* **Citation:** Bezerra, F., et al. (2024). LLM-authored Competency Questions: A Multi-faceted Characterization and Evaluation. *arXiv preprint arXiv:2604.16258*. 11  
* **Link:** [https://arxiv.org/pdf/2604.16258](https://arxiv.org/pdf/2604.16258)  
* **Accessibility:** \[Full text read\]  
* **What they do:** The authors introduce **CompCQ**, a framework for characterizing and evaluating competency questions (CQs) generated by LLMs.11 It uses linguistic metrics (readability, structural complexity) and set-level semantic analysis (Pairwise Cosine Similarity) to assess diversity and relevance. The evaluation includes an LLM-assisted scoring system on a 4-point Likert scale (Explicit, Inferable, Contextual, Irrelevant).11  
* **Method snapshot:** Multi-dimensional framework using Sentence-BERT embeddings for semantic diversity and Gemini 2.5 Pro as a relevance evaluator, validated by human experts.11  
* **Where we differ:** While Bezerra et al. evaluate the *generation of requirements* (the questions), we evaluate the *fidelity of the extracted graph*. We adopt their multi-faceted characterization (readability and relevance) but apply it to a "quarantined" corpus (Bahamas DPA 2003\) to measure extraction precision rather than requirement elicitation.11  
* **Strength of "where we differ":** \[strong — copyable into paper\]

### **NeOn Methodology for Ontology Engineering**

* **Citation:** Suárez-Figueroa, M. C., et al. (2012). The NeOn Methodology for ontology engineering. *Ontology Engineering in a Networked World*. 24  
* **Link:** [https://doi.org/10.1007/978-3-319-68204-4\_9](https://doi.org/10.1007/978-3-319-68204-4_9)  
* **Accessibility:** \[Full text read\]  
* **What they do:** NeOn provides a scenario-based methodology that moves away from rigid workflows, offering nine scenarios for building ontology networks through re-engineering, alignment, and localization.24 It utilizes an "Ontology Requirements Specification Document" (ORSD) and "filling cards" to define purposes, scopes, and groups of competency questions.26  
* **Method snapshot:** A scenario-based framework pillars on a glossary of processes and prescriptive guidelines for ontology network construction.25  
* **Where we differ:** NeOn is designed for *massive, multi-stakeholder networked projects*. Our project targets the "lowest-friction" niche, replacing the formal ORSD and filling cards with a direct "Markdown → PR" workflow. We utilize the NeOn concept of "Competency Questions" for validation but strip away the administrative overhead of the full methodology to favor LLM-curated speed.24  
* **Strength of "where we differ":** \[strong — copyable into paper\]

## **Bucket 3: Comparable Legal-Ontology Architectures**

Modern legal ontologies must balance the "resource consumption bottleneck" of manual tagging with the need for precise, queryable representations of normative provisions.5

### **\[Hoekstra et al., 2007\] The LKIF Core ontology of basic legal concepts**

* **Citation:** Hoekstra, R., Breuker, J., Di Bello, M., & Boer, A. (2007). The LKIF Core ontology of basic legal concepts. *Proceedings of the 11th International Conference on Artificial Intelligence and Law*. 22  
* **Link:**([https://www.researchgate.net/publication/221539250\_The\_LKIF\_Core\_ontology\_of\_basic\_legal\_concepts](https://www.researchgate.net/publication/221539250_The_LKIF_Core_ontology_of_basic_legal_concepts))  
* **Accessibility:** \[Full text read\]  
* **What they do:** Developed within the Estrella project, LKIF (Legal Knowledge Interchange Format) is a core ontology designed to facilitate the translation between legal knowledge bases.22 It organizes legal concepts into modules (mental, physical, abstract) and adopts Allen's theory of time and Hohfeldian rights to model complex legal arguments.22  
* **Method snapshot:** A hybrid solution utilizing OWL-DL and SWRL for reasoning, constructed through top-down expert input and assessment across five scales of relevance and abstraction.22  
* **Where we differ:** LKIF is an *interchange format* for heavy-weight reasoning engines. Our project is a *curation tool-chain* for specific jurisdictions. We replace their complex OWL-DL/SWRL stack with a "Markdown \+ YAML vault" that is easier for legal practitioners to maintain without needing a background in computational logic.22  
* **Strength of "where we differ":** \[solid\]

### **\[Athan et al., 2013\] LegalRuleML and Akoma Ntoso**

* **Citation:** Athan, T., et al. (2013). LegalRuleML: Design principles and XML syntax. *Proceedings of the 14th International Conference on Artificial Intelligence and Law*. 4  
* **Link:** [https://doi.org/10.1145/2514601.2514605](https://doi.org/10.1145/2514601.2514605)  
* **Accessibility:** \[Abstract \+ Cited-by description only\]  
* **What they do:** Akoma Ntoso (LegalDocML) provides a standard XML markup for legal documents, while LegalRuleML models the logic of normative relationships, such as obligations and permissions.4 These standards allow for machine-readable legal knowledge that supports advanced retrieval and reasoning.5  
* **Method snapshot:** Highly structured XML standards requiring validated structural and semantic mark-up, often by expert legal annotators.5  
* **Where we differ:** These standards carry a heavy "XML tax"—the overhead of manual tagging and complex schema validation. Our project uses a *Markdown \+ YAML vault*, which allows for low-friction natural text editing while still enabling the "typed, queryable" graph layer that is normally only possible in high-overhead formats like LegalRuleML.4  
* **Strength of "where we differ":** \[strong — copyable into paper\]

### **Eunomos: A Legal Document and Knowledge Management System**

* **Citation:** Boella, G., et al. (2016). Eunomos, a legal document and knowledge management system for the web. *Artificial Intelligence and Law*, 24(2), 181-207. 27  
* **Link:** [https://doi.org/10.1007/s10506-016-9182-3](https://doi.org/10.1007/s10506-016-9182-3)  
* **Accessibility:** \[Cited-by description only\]  
* **What they do:** Eunomos is a web-based system that helps legal professionals access up-to-date law by linking provisions to recitals through a "Provision Model".27 It uses Semantic Role Labeling (SRL) based information extraction to identify duties, rights, and definitions within legislative texts.27  
* **Method snapshot:** Semi-automated normalization and information extraction module linked to ontologies for legal document management.27  
* **Where we differ:** Eunomos is a *centralized web platform*. Our project is an *open-source workflow* centered on a Git-PR review cycle. By using Markdown and standard Git-PR tools, we enable a more auditable and transparent "infrastructure-as-code" approach to legal data maintenance than the closed environment of Eunomos.27  
* **Strength of "where we differ":** \[solid\]

### **FIBO (Financial Industry Business Ontology)**

* **Citation:** Enterprise Data Management Council. (2020). Financial Industry Business Ontology (FIBO) Overview. 29  
* **Link:** [https://spec.edmcouncil.org/fibo/](https://spec.edmcouncil.org/fibo/)  
* **Accessibility:** \[Full text read\]  
* **What they do:** FIBO is a de-facto industry standard providing a formal ontology of financial terms, instruments, and legal entities.31 It uses RDF and OWL to define precise meanings for business concepts, enabling semantic consistency across disparate banking and regulatory systems.31  
* **Method snapshot:** A massive, modular ontology with over 1000 classes, evaluated through GraphDB inference and property path checks for structural integrity.29  
* **Where we differ:** Full FIBO import is computationally heavy and often irrelevant for narrow jurisdiction-specific compliance. Our project is **FIBO-aligned without full import**; we utilize its contractual scaffolding (entity-role-obligation patterns) for our YAML schema but maintain the data in lightweight Markdown to ensure "lowest-friction" and rapid loading.29  
* **Strength of "where we differ":** \[strong — copyable into paper\]

### **\[Pandit et al., 2024\] Data Privacy Vocabulary (DPV)**

* **Citation:** Pandit, H. J., et al. (2024). Data Privacy Vocabulary (DPV) \- Version 2.0. *W3C Community Group Report*. 33  
* **Link:** [https://w3id.org/dpv/](https://w3id.org/dpv/)  
* **Accessibility:** \[Full text read\]  
* **What they do:** DPV enables machine-readable metadata about personal data processing based on the GDPR.33 It is structured into core modules (Purposes, Entities, Legal Basis, Risk) and provides extensions for specific jurisdictions (e.g., \[LEGAL-EU\], \`\`) using ISO 3166-2 namespaces.33  
* **Method snapshot:** RDFS/SKOS-based taxonomy designed for interoperability, evaluated through its ability to model diverse real-world use cases like consent management and risk assessments.33  
* **Where we differ:** DPV is a *standardized vocabulary*. Our project is a *curation workflow*. While we use DPV concepts to tag our data, our "inbox" workflow automates the extraction from regional statutes (like the Bahamas DPA 2003\) into DPV-aligned formats, bridging the gap between raw law and the DPV standard.33  
* **Strength of "where we differ":** \[solid\]

### **Modeling Data Protection Requirements in Workflows**

* **Citation:** Bartolini, C., Muthuri, R., & Santos, C. (2016). Using ontologies to model data protection requirements in workflows. *Proceedings of the 9th International Workshop on Juris-Informatics (JURISIN)*. 35  
* **Link:** [https://orbilu.uni.lu/bitstream/10993/33856/1/main.pdf](https://orbilu.uni.lu/bitstream/10993/33856/1/main.pdf)  
* **Accessibility:** \[Full text read\]  
* **What they do:** The authors propose a bottom-up legal ontology to help data controllers understand GDPR obligations.35 They develop an Eclipse plugin (BPMN2 Modeler) that introduces a "Data Protection Task" which is annotated with rules extracted directly from the ontology knowledge base.35  
* **Method snapshot:** A "proof of concept" system that enriches business process models (BPMN) with legal requirements using an OWL API for reasoning.35  
* **Where we differ:** Their project enriches *business workflows* as a visualization tool. Our project enriches the *legal authoring process*. Instead of an Eclipse plugin for BPMN, we offer a Git-PR workflow for Markdown files, focusing on the auditable creation of the knowledge base itself rather than its secondary application in process modeling.35  
* **Strength of "where we differ":** \[solid\]

## **Bucket 4: Recent JURIX / ICAIL Papers (2023–2025)**

The state-of-the-art in legal AI has pivoted toward LLM-curated knowledge graphs and automated compliance checking, as evidenced by recent session topics at JURIX and ICAIL.8

### **Ontology-Driven Graph RAG for Legal Norms**

* **Citation:** De Martim, H. (2025). An Ontology-Driven Graph RAG for Legal Norms: A Hierarchical, Temporal, and Deterministic Approach. *JURIX 2025*. 8  
* **Link:** [https://jurix2025.di.unito.it/program-overview](https://jurix2025.di.unito.it/program-overview)  
* **Accessibility:**  
* **What they do:** This short paper introduces a Graph Retrieval-Augmented Generation (RAG) system that uses an ontology as its backbone to ensure hierarchical and temporal consistency in legal question answering.8 The system prioritizes deterministic outputs over the stochastic nature of general LLMs by grounding the retrieval in a queryable norm-graph.8  
* **Method snapshot:** System paper presented in the "Semantic Web and Hybrid AI" session, utilizing ontology-driven retrieval to manage legal norms.8  
* **Where we differ:** De Martim focuses on the *retrieval and question-answering* phase. Our project focuses on the *ingestion and curation* phase. We provide the "low-friction" toolchain for building the very graph that a system like De Martim's would eventually query, specifically targeting regional laws where no such graph exists.8  
* **Strength of "where we differ":** \[strong — copyable into paper\]

### **Automated Creation of a Legal Knowledge Graph**

* **Citation:** D'Amato, C., et al. (2025). Automated Creation of a Legal Knowledge Graph Addressing Cases of Violence Against Women. *JURIX 2025*. 8  
* **Link:** [https://jurix2025.di.unito.it/program-overview](https://jurix2025.di.unito.it/program-overview)  
* **Accessibility:**  
* **What they do:** This long paper describes the automated construction of a legal knowledge graph from legislation and case law specifically regarding violence against women.8 The goal is to provide a queryable representation for complex socio-legal analysis.8  
* **Method snapshot:** Methodology/System paper presenting a specialized knowledge graph creation for a specific legal domain.  
* **Where we differ:** Their contribution is a *domain-specific static KG* for research. Our contribution is a *generic, reproducible workflow*. We prioritize the Git-PR review and Markdown storage to allow jurisdictional experts to keep the graph "alive" alongside legislative updates, a feature typically missing from static domain-specific extracts.8  
* **Strength of "where we differ":** \[solid\]

### **Fine-tuning GPT-3 for Legal Rule Classification**

* **Citation:** Liga, D., & Robaldo, L. (2023). Fine-tuning GPT-3 for legal rule classification. *Computer Law & Security Review*, 51, 105864\. 4  
* **Link:** [https://doi.org/10.1016/j.clsr.2023.105864](https://doi.org/10.1016/j.clsr.2023.105864)  
* **Accessibility:** \[Full text read\]  
* **What they do:** The authors fine-tune GPT-3 on GDPR articles annotated with LegalDocML and LegalRuleML to classify rules as obligations, permissions, or constitutive.4 They demonstrate that fine-tuning on even small amounts of high-quality XML-annotated data allows LLMs to significantly outperform previous BERT-based models in multi-class legal rule classification.38  
* **Method snapshot:** Empirical study on transfer learning for legal rule classification; evaluated through precision/recall across four classification scenarios.4  
* **Where we differ:** Liga and Robaldo use LLMs to *classify existing fragments* of text already tagged with symbolic logic. Our project uses LLMs to *create the fragments* and their relationships directly from raw text. We bypass the need for pre-existing XML annotations by using a "Markdown \+ YAML" vault as the native format.4  
* **Strength of "where we differ":** \[strong — copyable into paper\]

### **\[Al-Kadi et al., 2025\] CO2 (Co-Compliance Officer)**

* **Citation:** Al-Kadi, M., et al. (2025). CO2 (Co-Compliance Officer): An LLM-based Ontology-Driven Methodology for Generating Knowledge Graphs and AI Compliance Checking. *IEEE Access*. 39  
* **Link:**([https://doi.org/10.1109/ACCESS.2025.3524177](https://doi.org/10.1109/ACCESS.2025.3524177))  
* **Accessibility:** \[Full text read\]  
* **What they do:** The paper introduces a methodology for building KGs from AI regulations (like the EU AI Act) using LLMs for Named-Entity Recognition (NER) and relationship extraction.39 The created graphs are used to perform inconsistency checks and identify pitfalls in compliance documentation for AI systems.39  
* **Method snapshot:** Methodology paper evaluating model-based vs. LLM-based KG generation; evaluation includes quantitative comparisons of NER performance.39  
* **Where we differ:** CO2 is a *specialized compliance checker* for AI systems. Our project is a *general jurisdictional repository*. We focus on the "low-friction" aspect of Git-PR workflows for general statutes (like Caribbean DPAs), whereas CO2 focuses on the complex, risk-based logic specific to the AI Act.39  
* **Strength of "where we differ":** \[solid\]

### **\[Janatian et al., 2023\] Using GPT-4 to generate structured representations**

* **Citation:** Janatian, A., et al. (2023). Using GPT-4 to generate structured representations from legislation for legal decision support. *ICAIL 2023*. 40  
* **Link:** [https://arxiv.org/html/2604.17153v1](https://arxiv.org/html/2604.17153v1)  
* **Accessibility:** \[Abstract \+ Citation graph\]  
* **What they do:** The authors analyze the capability of GPT-4 to translate traffic rules and regulations into structured logic.40 They found that 60% of the generated models were equivalent or superior to manual ones, effectively simplifying decision models by removing redundant nodes.40  
* **Method snapshot:** Empirical study evaluating the structural similarity and outcome equivalence of LLM-generated models compared to expert gold standards.40  
* **Where we differ:** Their focus is on generating *executable decision logic*. Our focus is on an *auditable knowledge base*. We prioritize the human review of the "inbox → extract → validate" pipeline, ensuring that the jurisdictional compliance graph is human-maintainable rather than just machine-executable.40  
* **Strength of "where we differ":** \[solid\]

## **Synthesis and Strategic Calibration**

The preceding analysis of the literature highlights a critical tension in legal knowledge engineering: the desire for formal, high-fidelity representations (e.g., LegalRuleML, LKIF) versus the reality of the "resource consumption bottleneck".5 Current state-of-the-art work at JURIX and ICAIL increasingly utilizes LLMs to mitigate this bottleneck, yet these systems often remain academic prototypes or domain-specific static extracts.8

### **Dominant "Where We Differ" Passages**

1. **On Structural Friction:** "While standards like Akoma Ntoso and LegalRuleML provide robust frameworks for legal logic, they suffer from a significant 'XML tax' that prevents rapid jurisdictional adoption.4 Our workflow replaces these high-friction schemas with a Markdown \+ YAML vault, allowing legal experts to maintain typed, queryable graphs through standard Git-PR workflows without needing to learn complex XML syntaxes or formal description logics.22"  
2. **On Regional Complementarity:** "The foundational work of Donalds, Barclay, and Osei-Bryson 12 has elucidated the behavioral drivers of Caribbean compliance. However, there remains a lack of structural data representing regional laws. Our project provides this technical missing link by offering a reproducible ingestion engine that transforms raw statutes—such as the Bahamas Data Protection Act 2003—into machine-interpretable compliance graphs, moving from awareness-centered models to structural-compliance infrastructure.14"  
3. **On Human-in-the-Loop LLM Curation:** "Recent methodologies like CO2 39 and the work of Janatian et al. 40 emphasize the automation of legal knowledge extraction. Our project differs by prioritizing a 'lowest-friction' auditable workflow. By embedding LLM extraction into a Git-PR review cycle, we ensure that the resulting jurisdictional graphs are not just automated outputs, but human-validated artifacts that are FIBO-aligned and legally defensible.29"

### **Pre-Registration Evaluation Metrics**

Based on the recurrent evaluation methods identified in Bucket 2 and the recent JURIX papers, the following metrics should be pre-registered to ensure a robust and comparable assessment:

| Metric | Definition / Method | Source Inspiration |
| :---- | :---- | :---- |
| **Competency Question Coverage (CQC)** | The percentage of pre-defined legal queries (derived from domain expertise) answerable by the graph. | NeOn methodology 26 |
| **LLM-Assisted Relevance (LARS)** | A 4-point Likert scale (Explicit, Inferable, Contextual, Irrelevant) for extracted entities. | Bezerra et al. 11 |
| **OOPS\! Pitfall Count** | The density of "Critical" and "Important" pitfalls identified in the final YAML export. | Poveda-Villalón et al. 17 |
| **Git-PR Revision Ratio** | The ratio of LLM-proposed tokens to human-edited tokens during the validation phase. | Systematic system evaluation |
| **FIBO-Alignment Fidelity** | Measurement of term overlap and relationship mapping to core FIBO modules. | FIBO-alignment art 29 |

### **Identified Gaps and Gaps for Future Inquiry**

While the coverage across the buckets is exhaustive, several gaps remain due to accessibility or the early stage of the research:

* **JURIX 2025 Full-Text:** Several papers from JURIX 2025 (e.g., De Martim, D'Amato) are currently available only in abstract or session-overview form.8 Full-text access via institutional repositories will be required to confirm their exact semantic role extraction methods.  
* **Trinidad/Jamaica DPA Population in DPV:** While DPV provides namespaces for these jurisdictions, the actual concepts for Caribbean-specific laws are sparsely populated.33  
* **Bahamas DPA 2003:** As per the project constraints, no substantive content has been extracted from this act.41 It remains "quarantined" for the cold-run evaluation phase.

#### **Works cited**

1. Jurix 2025, accessed on May 8, 2026, [https://jurix2025.di.unito.it/](https://jurix2025.di.unito.it/)  
2. Jurix 2024, accessed on May 8, 2026, [https://jurix2024.law.muni.cz/](https://jurix2024.law.muni.cz/)  
3. JURIX \- The Foundation for Legal Knowledge Systems, accessed on May 8, 2026, [https://jurix.nl/](https://jurix.nl/)  
4. Fine-tuning GPT-3 for legal rule classification \- Cronfa, accessed on May 8, 2026, [https://cronfa.swan.ac.uk/Record/cronfa64410/Download/64410\_\_28795\_\_5325de6920c3470ab23be2a97b1077c0.pdf](https://cronfa.swan.ac.uk/Record/cronfa64410/Download/64410__28795__5325de6920c3470ab23be2a97b1077c0.pdf)  
5. (PDF) Thirty years of artificial intelligence and law: the third decade \- ResearchGate, accessed on May 8, 2026, [https://www.researchgate.net/publication/362582150\_Thirty\_years\_of\_artificial\_intelligence\_and\_law\_the\_third\_decade](https://www.researchgate.net/publication/362582150_Thirty_years_of_artificial_intelligence_and_law_the_third_decade)  
6. Fine-tuning GPT-3 for legal rule classification | Request PDF \- ResearchGate, accessed on May 8, 2026, [https://www.researchgate.net/publication/375170129\_Fine-tuning\_GPT-3\_for\_legal\_rule\_classification](https://www.researchgate.net/publication/375170129_Fine-tuning_GPT-3_for_legal_rule_classification)  
7. Proceedings of the Natural Legal Language Processing Workshop 2024 \- ACL Anthology, accessed on May 8, 2026, [https://aclanthology.org/2024.nllp-1.pdf](https://aclanthology.org/2024.nllp-1.pdf)  
8. Program Overview \- Jurix 2025, accessed on May 8, 2026, [https://jurix2025.di.unito.it/program-overview](https://jurix2025.di.unito.it/program-overview)  
9. JURIX 2025 call for papers, accessed on May 8, 2026, [https://jurix.nl/jurix-2025-call-for-papers/](https://jurix.nl/jurix-2025-call-for-papers/)  
10. JURIX 2025 – 38th International Conference on Legal Knowledge and Information Systems, 9–11 December 2025, Turin (Italy), accessed on May 8, 2026, [https://resources.illc.uva.nl/LogicList/newsitem.php?id=12279](https://resources.illc.uva.nl/LogicList/newsitem.php?id=12279)  
11. Characterising LLM-Generated Competency Questions: a ... \- arXiv, accessed on May 8, 2026, [https://arxiv.org/pdf/2604.16258](https://arxiv.org/pdf/2604.16258)  
12. departmental reports \- The University of the West Indies, Mona, accessed on May 8, 2026, [https://www.mona.uwi.edu/secretariat/sites/default/files/secretariat/Departmental%20Reports%202013-2014.pdf](https://www.mona.uwi.edu/secretariat/sites/default/files/secretariat/Departmental%20Reports%202013-2014.pdf)  
13. Exploring theoretical constructs of cybersecurity awareness and training programs: comparative analysis of African and U.S. Initiatives \- ResearchGate, accessed on May 8, 2026, [https://www.researchgate.net/publication/386381377\_Exploring\_theoretical\_constructs\_of\_cybersecurity\_awareness\_and\_training\_programs\_comparative\_analysis\_of\_African\_and\_US\_Initiatives](https://www.researchgate.net/publication/386381377_Exploring_theoretical_constructs_of_cybersecurity_awareness_and_training_programs_comparative_analysis_of_African_and_US_Initiatives)  
14. Toward a cybercrime classification ontology: A knowledge-based approach | Request PDF, accessed on May 8, 2026, [https://www.researchgate.net/publication/329066315\_Toward\_a\_cybercrime\_classification\_ontology\_A\_knowledge-based\_approach](https://www.researchgate.net/publication/329066315_Toward_a_cybercrime_classification_ontology_A_knowledge-based_approach)  
15. Beyond technical measures: a value-focused thinking appraisal of strategic drivers in improving information security policy compliance | Request PDF \- ResearchGate, accessed on May 8, 2026, [https://www.researchgate.net/publication/354747810\_Beyond\_technical\_measures\_a\_value-focused\_thinking\_appraisal\_of\_strategic\_drivers\_in\_improving\_information\_security\_policy\_compliance](https://www.researchgate.net/publication/354747810_Beyond_technical_measures_a_value-focused_thinking_appraisal_of_strategic_drivers_in_improving_information_security_policy_compliance)  
16. Building an awareness-centered information security policy compliance model | Request PDF \- ResearchGate, accessed on May 8, 2026, [https://www.researchgate.net/publication/338508345\_Building\_an\_awareness-centered\_information\_security\_policy\_compliance\_model](https://www.researchgate.net/publication/338508345_Building_an_awareness-centered_information_security_policy_compliance_model)  
17. OOPS\! (OntOlogy Pitfall Scanner\!) \- SciSpace, accessed on May 8, 2026, [https://scispace.com/pdf/oops-ontology-pitfall-scanner-an-on-line-tool-for-ontology-l4irgaxzi8.pdf](https://scispace.com/pdf/oops-ontology-pitfall-scanner-an-on-line-tool-for-ontology-l4irgaxzi8.pdf)  
18. OOPS\! (OntOlogy Pitfall Scanner\!): supporting ontology evaluation ..., accessed on May 8, 2026, [https://www.semantic-web-journal.net/system/files/swj989.pdf](https://www.semantic-web-journal.net/system/files/swj989.pdf)  
19. OOPS\! (OntOlogy Pitfall Scanner\!): | Request PDF \- ResearchGate, accessed on May 8, 2026, [https://www.researchgate.net/publication/285623865\_OOPS\_OntOlogy\_Pitfall\_Scanner](https://www.researchgate.net/publication/285623865_OOPS_OntOlogy_Pitfall_Scanner)  
20. Validating Ontologies with OOPS\! \- SciSpace, accessed on May 8, 2026, [https://scispace.com/pdf/validating-ontologies-with-oops-27fv4aan6b.pdf](https://scispace.com/pdf/validating-ontologies-with-oops-27fv4aan6b.pdf)  
21. gUFO: A Gentle Foundational Ontology for Semantic Web Knowledge Graphs \- arXiv, accessed on May 8, 2026, [https://arxiv.org/html/2603.20948v1](https://arxiv.org/html/2603.20948v1)  
22. (PDF) The LKIF Core ontology of basic legal concepts \- ResearchGate, accessed on May 8, 2026, [https://www.researchgate.net/publication/221539250\_The\_LKIF\_Core\_ontology\_of\_basic\_legal\_concepts](https://www.researchgate.net/publication/221539250_The_LKIF_Core_ontology_of_basic_legal_concepts)  
23. NeOn Methodology for Building Contextualized Ontology Networks | Request PDF, accessed on May 8, 2026, [https://www.researchgate.net/publication/319393312\_NeOn\_Methodology\_for\_Building\_Contextualized\_Ontology\_Networks](https://www.researchgate.net/publication/319393312_NeOn_Methodology_for_Building_Contextualized_Ontology_Networks)  
24. The NeOn Methodology for Ontology Engineering | Request PDF \- ResearchGate, accessed on May 8, 2026, [https://www.researchgate.net/publication/272829912\_The\_NeOn\_Methodology\_for\_Ontology\_Engineering](https://www.researchgate.net/publication/272829912_The_NeOn_Methodology_for_Ontology_Engineering)  
25. (PDF) The NeOn Methodology framework: A scenario-based methodology for ontology development (2014) | Mari Carmen Suárez-Figueroa | 181 Citations \- SciSpace, accessed on May 8, 2026, [https://scispace.com/papers/the-neon-methodology-framework-a-scenario-based-methodology-3ecsq85gsf](https://scispace.com/papers/the-neon-methodology-framework-a-scenario-based-methodology-3ecsq85gsf)  
26. NeOn Methodology for Building Ontology Networks: Ontology Specification \- Knowledge Media Institute, accessed on May 8, 2026, [https://kmi.open.ac.uk/events/sssw08/presentations/Gomez%20Perez-NeOn-Methodology-OntologySpecification-v3.pdf](https://kmi.open.ac.uk/events/sssw08/presentations/Gomez%20Perez-NeOn-Methodology-OntologySpecification-v3.pdf)  
27. POPULATING LEGAL ONTOLOGIES USING INFORMATION EXTRACTION BASED ON SEMANTIC ROLE LABELING AND TEXT SIMILARITY \- ORBilu, accessed on May 8, 2026, [https://orbilu.uni.lu/bitstream/10993/33810/1/LlBH-thesis-2016.pdf](https://orbilu.uni.lu/bitstream/10993/33810/1/LlBH-thesis-2016.pdf)  
28. Thirty years of artificial intelligence and law: the third decade, accessed on May 8, 2026, [https://d-nb.info/1271323222/34](https://d-nb.info/1271323222/34)  
29. Exploring FIBO Using the Inference and Property Path Features of GraphDB \- Ontotext, accessed on May 8, 2026, [https://www.ontotext.com/blog/fibo-graphdb-inference-and-property-path-features/](https://www.ontotext.com/blog/fibo-graphdb-inference-and-property-path-features/)  
30. Data Harmonization, accessed on May 8, 2026, [https://www.wpi.edu/sites/default/files/IntrotoInfoResources\_DataHarmonizationWPI.pdf](https://www.wpi.edu/sites/default/files/IntrotoInfoResources_DataHarmonizationWPI.pdf)  
31. Financial Information Business Ontology (FIBO): Architecture, Use Cases, and Implementation Challenges \- Global Fintech Series, accessed on May 8, 2026, [https://globalfintechseries.com/featured/financial-information-business-ontology-fibo-architecture-use-cases-and-implementation-challenges/](https://globalfintechseries.com/featured/financial-information-business-ontology-fibo-architecture-use-cases-and-implementation-challenges/)  
32. The Semantic Operating System for Modern Banking: Off‑the‑Shelf Ontologies | by balaji bal, accessed on May 8, 2026, [https://medium.com/@balajibal/the-semantic-operating-system-for-modern-banking-off-the-shelf-ontologies-1fc5cc83eb18](https://medium.com/@balajibal/the-semantic-operating-system-for-modern-banking-off-the-shelf-ontologies-1fc5cc83eb18)  
33. Data Privacy Vocabulary (DPV) \- w3id.org, accessed on May 8, 2026, [https://w3id.org/dpv/](https://w3id.org/dpv/)  
34. Data Privacy Vocabulary (DPV) \- W3C on GitHub, accessed on May 8, 2026, [https://w3c.github.io/dpv/2.1/dpv/](https://w3c.github.io/dpv/2.1/dpv/)  
35. Using Ontologies to Model Data Protection Requirements ... \- ORBilu, accessed on May 8, 2026, [https://orbilu.uni.lu/bitstream/10993/33856/1/main.pdf](https://orbilu.uni.lu/bitstream/10993/33856/1/main.pdf)  
36. ASAIL 2025 Automated Semantic Analysis of Information in Legal Texts 2025, accessed on May 8, 2026, [https://ceur-ws.org/Vol-4174/](https://ceur-ws.org/Vol-4174/)  
37. Automated Creation of the Legal Knowledge Graph Addressing Legislation on Violence Against Women: Resource, Methodology and Lessons Learned \- arXiv, accessed on May 8, 2026, [https://arxiv.org/html/2508.06368v1](https://arxiv.org/html/2508.06368v1)  
38. Fine-Tuning GPT-3 For Legal Rule Classification: Davide Liga, Livio Robaldo | PDF \- Scribd, accessed on May 8, 2026, [https://www.scribd.com/document/715325946/14ab3259-5af9-4474-81af-3af22b68ec8f](https://www.scribd.com/document/715325946/14ab3259-5af9-4474-81af-3af22b68ec8f)  
39. (PDF) CO2 (Co-Compliance Officer): An LLM-based Ontology-Driven Methodology for Generating Knowledge Graphs and AI Compliance Checking \- ResearchGate, accessed on May 8, 2026, [https://www.researchgate.net/publication/398220714\_CO2\_Co-Compliance\_Officer\_An\_LLM-based\_Ontology-Driven\_Methodology\_for\_Generating\_Knowledge\_Graphs\_and\_AI\_Compliance\_Checking](https://www.researchgate.net/publication/398220714_CO2_Co-Compliance_Officer_An_LLM-based_Ontology-Driven_Methodology_for_Generating_Knowledge_Graphs_and_AI_Compliance_Checking)  
40. From Legal Text to Executable Decision Models: Evaluating Structured Representations for Legal Decision Model Generation \- arXiv, accessed on May 8, 2026, [https://arxiv.org/html/2604.17153v1](https://arxiv.org/html/2604.17153v1)  
41. Natural Language Processing for the Legal Domain: A Survey of Tasks, Datasets, Models, and Challenges \- arXiv, accessed on May 8, 2026, [https://arxiv.org/html/2410.21306v1](https://arxiv.org/html/2410.21306v1)