# Templates and further study

This chapter collects the templates used throughout the book, a self-assessment for the end of the course, further reading for each chapter and suggestions for further study. Copy the templates into any document or spreadsheet. Leave a field blank, marked "unknown", when the information does not yet exist; an honest gap is more useful than an invented value.

## Dossier templates

### Decision brief

| Field | What to record |
|---|---|
| Decision, date and owner | The decision requested, when it is needed and who is accountable |
| Problem and scope | What is wrong today, for whom, and what is out of scope |
| Recommendation | The proposed option and at least one credible alternative |
| Mandatory conditions | Legal, security or continuity conditions every option must meet |
| Cost and consequences | Investment, operating cost changes and transition effects |
| Uncertainty | What is not yet known and how it will be resolved |
| Condition for the next stage | The results that release, narrow or stop further funding |

### Capability assessment

| Field | What to record |
|---|---|
| Capability | Identifier, name, definition and level-1 domain |
| Importance | High, medium or low, and the strategic objective it supports |
| Effectiveness | Score from 1 to 5 and the data behind it |
| Confidence | High, medium or low, and the source of the rating |
| Supporting elements | Processes, applications and the accountable owner |
| Proposed action | Measure, quick fix, investment or no change, with the reason |

### Application inventory record

| Field | What to record |
|---|---|
| Application | Identifier, business purpose and accountable owner |
| Users and consumers | Interactive users and non-interactive consumers such as batch jobs |
| Authority and interfaces | Facts it is authoritative for, interfaces and dependencies |
| Cost | Annual operating cost by type: licences, infrastructure, support, shared services |
| Lifecycle and contract | Support status, contract end date and exit terms |
| Assessment | TIME scores and quadrant, and the proposed disposition |
| Gaps | Missing facts and who will find them |

### Fact-authority register

| Field | What to record |
|---|---|
| Fact | The business fact or relationship, with its definition |
| Authority | The authoritative source and the accountable owner |
| Writers and consumers | Who may change it and who relies on it, with freshness needs |
| Correction | How disputes and errors are resolved, and by whom |
| Policy | Access rules and the source of the retention policy |

### Exception record

| Field | What to record |
|---|---|
| Standard | The standard affected and its owner |
| Reason and scope | Why compliance is not yet possible and what is covered |
| Controls | Compensating controls that are operating now, and conditions still to be met |
| Risk owner | Who accepts the residual risk, within which delegation |
| Expiry | End date, review trigger and the funded plan to comply |

### Benefits register

| Field | What to record |
|---|---|
| Benefit | Identifier, affected population and baseline |
| Mechanism | How the change produces the benefit, and its measure and owner |
| Type | Cash, capacity or risk reduction |
| Timing and cost | When it arrives and what it costs to realise |
| Checks | Possible double counting and alternative causes |
| Realisation | The data that will show it happened, and the action if it does not |

### Transition state

| Field | What to record |
|---|---|
| State | Identifier, entry condition and exit condition |
| Authority | The authoritative source and allowed writers for each fact |
| Operation | Interfaces, recovery, reconciliation and the support owner |
| Temporary elements | Bridges and workarounds, with their retirement condition and budget |
| Work | Work packages, predecessors, durations and resource assumptions |
| Money and risk | Annual cash need, main risks and the effect of each change card |

### Source log

| Field | What to record |
|---|---|
| Claim | The claim the source is used for, and its scope |
| Source | Full reference and the kind of source |
| Location | Where in the source the support appears |
| Design | Method, sample and main limits |
| Inference | How it applies to Helios, and the strongest counterargument |
| Test | The observation that would confirm or overturn the inference |

## Self-assessment

Before submitting the capstone, check that you can do each of the following without notes. If one is weak, return to the chapter shown.

| I can… | Chapter |
|---|---|
| Explain why a local solution can raise enterprise cost, with a mechanism | 1 |
| Tailor an architecture method to a decision and write principles in a standard format | 2 |
| Build a capability heat map that separates importance, effectiveness and confidence | 3 |
| Place capabilities in the operating-model grid and justify the placement | 4 |
| Score applications with TIME and say what the score leaves out | 5 |
| Assign authority for individual facts and design a correction workflow | 6 |
| Diagnose a delivery bottleneck using Conway's law and local data | 7 |
| Describe who holds decision rights for each IT decision domain | 8 |
| Calculate the availability of a service with shared dependencies | 9 |
| Calculate NPV, IRR and payback, and use real and nominal rates consistently | 10 |
| Find the critical path and explain how shared resources change it | 11 |
| Diagnose an adoption problem and choose between design and training fixes | 12 |
| Apply mandatory conditions and find the weight at which a ranking tips | 13 |
| Recognise Simpson's paradox and regression to the mean, and calculate a difference-in-differences | 14 |
| Design an AI experiment with consequence-based errors and stop conditions | 15 |
| Appraise a study and separate findings, inference and proposal | 16 |

## Further reading

Two or three sources for each chapter, chosen to take the topic further. Most are cited in the chapter itself; the reference list gives full details.

- **Chapter 1, The enterprise architecture problem.** Ross, Weill and Robertson set out the organising-logic view of enterprise architecture that this book builds on {REF:eastrategy}. ISO/IEC/IEEE 42010 defines the vocabulary of architecture descriptions {REF:iso42010}. Van der Raadt and van Vliet show how to design an architecture function {REF:vanderraadt}.
- **Chapter 2, Frameworks, methods and modelling.** Read the ArchiMate 4 Specification {REF:archimate4} with Lankhorst's summary of what changed {REF:archimate4changes}. The TOGAF Standard {REF:togaf} is the primary source for the ADM, and Kotusev's case study shows how one organisation actually used it {REF:kotusevtogaf}.
- **Chapter 3, Capabilities, value streams and requirements.** The TOGAF series guides on business capabilities {REF:togafcap}, value streams {REF:togafvs} and capability-based planning {REF:togafcbp} give definitions and worked examples.
- **Chapter 4, Operating models and alignment.** Ross, Beath and Mocker develop the operational backbone and digital platform {REF:designed4digital}. Henderson and Venkatraman's paper remains the clearest statement of the strategic alignment model {REF:alignment}, and Ross's briefing argues for focusing IT on the operating model {REF:operatingmodel}.
- **Chapter 5, Application portfolios.** The AWS guidance explains each migration strategy {REF:sevenrs}. Ellram's analysis of total cost of ownership {REF:tco} and Opara-Martins and colleagues on lock-in {REF:lockin} cover the economics of leaving a system or supplier.
- **Chapter 6, Information and data governance.** DAMA-DMBOK covers every knowledge area of data management {REF:dmbok}. The General Data Protection Regulation itself, especially its principles and its requirement for data protection by design, is short enough to read directly {REF:gdpr}.
- **Chapter 7, Technology strategy and platforms.** Read Conway's original paper {REF:conway}, the mirroring study {REF:mirroring} and Skelton and Pais on designing team boundaries {REF:teamtopologies}.
- **Chapter 8, Governance and decision rights.** Weill and Ross's book is the source of the domains and archetypes {REF:itgov}. COBIT 2019 {REF:cobit} and ISO/IEC 38500 {REF:iso38500} give the standard frameworks for governance of IT.
- **Chapter 9, Risk, security and assurance.** The NIST Cybersecurity Framework 2.0 {REF:csf} and NIST SP 800-207 on zero trust {REF:zerotrust} are free and readable; ISO 31000 frames risk around objectives {REF:iso31000}.
- **Chapter 10, Investment economics.** The OpenStax finance chapters on NPV {REF:npv} and IRR {REF:irr} cover the methods with exercises. Benaroch and Kauffman develop real options for IT {REF:realoptions}, and Peppard, Ward and Daniel explain benefits management {REF:benefits}.
- **Chapter 11, Roadmaps and transitions.** Kelley and Walker's paper introduced the critical path method {REF:cpm}; TOGAF's phases E and F describe transition architectures and migration planning {REF:togafadm}.
- **Chapter 12, Change and adoption.** Cummings, Bridgman and Brown re-examine Lewin {REF:lewinrethink}, Appelbaum and colleagues review the evidence for Kotter's model {REF:kotterreview}, and Dang and Pekkola follow an architecture adoption over time {REF:change}.
- **Chapter 13, Sourcing and suppliers.** Lacity, Khan and Willcocks summarise outsourcing research {REF:lacity}; Williamson's paper explains transaction cost reasoning {REF:williamson}.
- **Chapter 14, Measuring outcomes.** Huntington-Klein's chapter on difference-in-differences is free online {REF:did}. Tamm and colleagues model how EA creates value {REF:eavalue}, and Forsgren, Humble and Kim present the research behind the DORA measures {REF:accelerate}.
- **Chapter 15, Innovation, AI and sustainability.** March's paper on exploration and exploitation {REF:march}, the NIST AI Risk Management Framework {REF:airmf} and the Software Carbon Intensity specification {REF:sci} are the primary sources.
- **Chapter 16, Research methods.** Recker's introduction covers research design, methods and writing in information systems {REF:recker}. Kotusev's study of architecture artefacts is a good example to appraise {REF:kotusevartifacts}.
- **Chapter 17, Capstone.** Weill and Ross's one-page governance summary {REF:governance} and Lankhorst and colleagues on enterprise modelling and analysis {REF:lankhorst} help with the dossier and its defence.

## Further study

To transfer the course to your own work, choose one real problem whose details you are permitted to use. Define the decision, gather authorised data and reuse the reasoning structures from the book, replacing the Helios assumptions with your organisation's facts and verifying current technical, legal and contractual conditions. For deeper research work, compare two primary studies that address the same question, analysing their constructs, methods, contexts and limits before drawing a recommendation. If your organisation's models are still in ArchiMate 3.2, plan their conversion to version 4 as a small project of its own, using the differences listed in Chapter 2.
