# Experiments, templates and research tasks

This chapter collects extensions to the experiments, the dossier templates and the research tasks for the four studios. Each experiment builds on a listing printed in its chapter. Before changing a listing, write down what you expect; afterwards, record what happened, why, and what the model leaves out.

## Experiments

- **Drain time and failure bounds (Chapter 2).** Add a parameter for the share of attempts that fail and reproduce every recovery time in Chapter 5, including the 16-minute recovery with status polling paused above 1,000 pending handoffs. Compute the zero-failure bound for 300, 3,000 and 30,000 trials and compare it with the rule of thumb 3 / n. List the measurements that would replace each constant-rate assumption.
- **The outbox and its workers (Chapter 4).** With PostgreSQL, create the outbox schema and a few hundred submissions. Run the claim query in two sessions before committing either, and confirm that they receive different rows. Expire the lease of a CRM B handoff, run the sweep, and show that no worker can claim it for fifteen minutes and that its next action is a lookup. Then show that a confirm carrying the old attempt number changes nothing, even when it comes from a worker with the same owner ID. Implement the eight-handoff limit from exercise 4.5 and test it with two simultaneous claims.
- **The hot row (Chapter 6).** Create the stock and reservation tables with one product and two units. In two sessions, show that the second reservation waits and then succeeds under READ COMMITTED, and fails with SQLSTATE 40001 under REPEATABLE READ. Reproduce the five rows of the retry table in Chapter 6, including the repeat of the winning request after the product has sold out. Time a reservation sent as one statement and as three round trips, and estimate h and 1 / h for each.
- **Event orderings (Chapter 8).** Write the invariant for an order of two units, then extend the state model to two units. Add the fresh-reservation path from exercise 8.6 and a void that times out.
- **Publication ledger (Chapter 10).** Add the withdrawal record from exercise 10.5. Then publish a second measure, the number of open requests, from the same inputs, and decide whether a change in either measure creates a new publication.
- **Correction schedules (Chapter 11).** Write a function that returns the worst-case delay from a record's arrival to its publication for a list of runs, each with a start time and a duration, when k consecutive runs fail. Reproduce the CC-B1 table, then find the cheapest schedule that survives two failed runs within 24 hours.
- **The access matrix (Chapter 11).** Add an `export` action allowed only to the publisher, and an analyst with a delegation for one tenant of another division. Update the hand-written matrix before changing the policy, then introduce a deliberate defect and confirm that the matrix catches it.
- **Reconciliation and fencing (Chapter 13).** Add an order-lines table and a check for orders whose line totals differ, a mapping-version column, and the deletion tombstones from exercise 13.4. With PostgreSQL, create the epoch fence on small `orders`, `order_lines` and `status_history` tables and reproduce its behaviours with three sessions, including one that sets `session_replication_role` to `replica`, first with `ENABLE ALWAYS` and then without it. Then publish the three tables from a second PostgreSQL instance, subscribe as `orion_applier`, and show that the apply worker passes the fence at epoch 7, is stopped at epoch 8, and slips through if the insert, update and delete triggers are made statement-level.

## Dossier templates

Replace each prompt with case-specific reasoning, and keep identifiers stable so that reviewers can follow the links between documents. A template filled with generic language explains nothing; each field should make a specific claim about your case.

### Decision brief

- **Decision ID, version and date:**
- **Decision needed, from whom and by when:**
- **What changed or what problem exists, in business terms:**
- **What stays the same in every option:**
- **Options, each with cost, effect on customers and main risk:**
- **Recommendation and the reason for it:**
- **Conditions, open questions and their owners:**
- **Links to the supporting scenarios, decision records and experiments:**

### Requirement and assumption register

| ID | Type | Statement and scope | Owner | Verification task or evidence | Consequence if false |
|---|---|---|---|---|---|
| R-01 | Requirement | | | | |
| A-01 | Assumption | | | | |

### Quality scenario

- **ID:**
- **Stimulus and its source:**
- **Environment, such as normal operation, peak load or a named failure:**
- **Required response:**
- **Measure and threshold:**
- **Owner of the promise:**

### Architecture decision record

- **ID, status and date:**
- **Context and the scenarios it serves:**
- **Decision:**
- **Mechanism and the authority that enforces it:**
- **Alternatives considered and why each was not chosen:**
- **Consequences, including residual risks:**
- **Evidence identifiers:**
- **Review triggers, each an observable condition:**
- **Supersedes, or is superseded by:**

### Experiment record

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

### Change card

- **Card ID and date:**
- **New fact and its source:**
- **Assumptions and decisions affected:**
- **Question for the team:**
- **Response chosen, and the decision record that records it:**

### Review finding

- **ID and the requirement affected:**
- **Architecture version reviewed:**
- **Defect or uncertainty, and its consequence:**
- **Severity and the reason for it:**
- **Evidence:**
- **Correction, or the residual risk accepted:**
- **Owner and deadline:**
- **Closure evidence:**
- **Status: open, closed, accepted residual risk or deferred investigation:**

### Migration gate

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

## Research tasks

Write one critique of 400 to 600 words for each studio. Identify the source's question, method, assumptions, supported conclusion and limits, then explain one way it transfers to the studio and one way it does not. Suggested sources and questions are:

- **Integration:** Saltzer, Reed and Clark on end-to-end arguments {REF:endtoend}, or Helland on idempotence {REF:helland2012}. Where should Meridian check that a request reached the service team?
- **Transactions:** Garcia-Molina and Salem on sagas {REF:saga}, or Helland on life beyond distributed transactions {REF:helland2007}. Which of Aster's guarantees need one transactional scope, and which can rely on messages?
- **Data:** Akidau and colleagues on the Dataflow Model {REF:dataflow}, or Codd on the relational model {REF:codd}. How should Beacon trade completeness against the 07:00 deadline?
- **Modernisation:** Fowler on the strangler fig application {REF:fowlerstrangler}, or Kleppmann on fencing {REF:kleppmann}. Which of Orion's writers can a routing seam control, and which need a fence?

Chapter 16's research synthesis then compares the kinds of knowledge these sources provide.
