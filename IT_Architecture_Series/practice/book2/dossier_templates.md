# Architecture dossier templates

Replace each prompt with case-specific reasoning, and keep identifiers stable so that reviewers can follow the links between documents. A template filled with generic language explains nothing; each field should make a specific claim about your case.

## Decision brief

- **Decision ID, version and date:**
- **Decision needed, from whom and by when:**
- **What changed or what problem exists, in business terms:**
- **What stays the same in every option:**
- **Options, each with cost, effect on customers and main risk:**
- **Recommendation and the reason for it:**
- **Conditions, open questions and their owners:**
- **Links to the supporting scenarios, decision records and experiments:**

## Requirement and assumption register

| ID | Type | Statement and scope | Owner | Verification task or evidence | Consequence if false |
|---|---|---|---|---|---|
| R-01 | Requirement | | | | |
| A-01 | Assumption | | | | |

## Quality scenario

- **ID:**
- **Stimulus and its source:**
- **Environment, such as normal operation, peak load or a named failure:**
- **Required response:**
- **Measure and threshold:**
- **Owner of the promise:**

## Architecture decision record

- **ID, status and date:**
- **Context and the scenarios it serves:**
- **Decision:**
- **Mechanism and the authority that enforces it:**
- **Alternatives considered and why each was not chosen:**
- **Consequences, including residual risks:**
- **Evidence identifiers:**
- **Review triggers, each an observable condition:**
- **Supersedes, or is superseded by:**

## Experiment record

- **Question, phrased so that it can fail:**
- **Claim under test and the decision it informs:**
- **Model or build, configuration and data version:**
- **Independent variables and controlled conditions:**
- **Workload model, open or closed, and offered rate:**
- **Failures injected and their timing:**
- **Business-level observations:**
- **Decision rule, written before the run:**
- **Result, variation and threats to validity:**
- **Design consequence:**
- **How to reproduce the experiment:**

## Change card

- **Card ID and date:**
- **New fact and its source:**
- **Assumptions and decisions affected:**
- **Question for the team:**
- **Response chosen, and the decision record that records it:**

## Review finding

- **ID and the requirement affected:**
- **Architecture version reviewed:**
- **Defect or uncertainty, and its consequence:**
- **Severity and the reason for it:**
- **Evidence:**
- **Correction, or the residual risk accepted:**
- **Owner and deadline:**
- **Closure evidence:**
- **Status: open, closed, accepted residual risk or deferred investigation:**

## Migration gate

- **Transition, with the current and target write authority:**
- **Scope of the data and the writers covered:**
- **Source position and mapping version:**
- **Writers fenced, and the evidence that each is stopped:**
- **Reconciliation results:**
- **Access, capacity and operating checks:**
- **Forward duration, reverse duration and latest decision point:**
- **Recovery before customer writes:**
- **Recovery after customer writes:**
- **Decision owner and communication plan:**
- **Retirement evidence:**
