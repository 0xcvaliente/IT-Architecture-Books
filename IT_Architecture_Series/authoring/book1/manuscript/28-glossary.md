# Glossary and final review

Use the glossary for retrieval practice. Cover each definition, explain the term with a Meridian example, then check your answer.

**4+1 view model.** Kruchten's architecture description with logical, process, development and physical views, tied together by scenarios.

**ABAC.** Attribute-based access control: decisions based on attributes of the principal, the resource, the action and the context, such as a request's business unit or submitter.

**Access token.** A token that lets a client call a protected API. Its audience is that API, which validates the issuer, audience, lifetime and scopes before acting on it.

**ADR.** Architecture decision record: a short document that records a significant decision, its context, the options considered and its consequences.

**Anti-corruption layer.** A translation layer that lets a system use another system's functions in its own domain model, so that the other model does not leak in.

**API.** An agreed interface through which software requests behaviour or data from other software.

**arc42.** Starke and Hruschka's twelve-section template for architecture documentation, from goals, constraints and context to decisions, quality requirements and risks.

**ATAM.** Architecture Tradeoff Analysis Method: a scenario-based evaluation that records risks, non-risks, sensitivity points and trade-off points.

**Authentication.** Establishing, with evidence, which principal is making a request.

**Authorisation.** Deciding whether a principal may perform an action on a resource under current conditions.

**Availability.** The proportion of time or requests for which a defined service works, under a stated measurement.

**Availability zone.** A failure domain inside a cloud region, with separate power, cooling and networking.

**Available-to-promise.** The quantity of stock that the business may still promise to new customers after reservations and allocations.

**Backpressure.** A mechanism that slows or rejects producers when a downstream consumer is near its capacity.

**Blue-green deployment.** A release that runs old and new environments side by side and switches traffic between them.

**Bounded context.** A boundary within which a domain model and its terms have one consistent meaning.

**Bulkhead.** Separate resource pools, such as connection pools or threads, for different dependencies, so that one failing dependency cannot exhaust everything.

**Burn rate.** How fast a service is consuming its error budget, relative to the rate that its SLO allows.

**C4 model.** Simon Brown's set of context, container, component and code diagrams for describing software architecture.

**Canary release.** A release that sends a small share of traffic to a new version and compares its results before a wider rollout.

**CAP theorem.** The result that a replicated system cannot guarantee both linearizable consistency and a response to every request while a network partition lasts.

**Capability.** Something the organisation must be able to do, independent of the team or product that does it today.

**Change data capture.** Reading committed changes from a source system's log or tables so that they can be applied elsewhere in order.

**Circuit breaker.** A mechanism that stops calls to a failing dependency for a time and then lets controlled probes through.

**Cohesion.** How closely the responsibilities inside one module belong together.

**Commitment discount.** A lower cloud price in exchange for committing to a level of usage or spend for one or three years.

**Compensation.** A new business action that semantically undoes an earlier completed step, such as a refund or a payment void.

**Concern.** In ISO/IEC/IEEE 42010, a matter of interest to a stakeholder, such as whether an agent can see another business unit's requests.

**Confabulation.** Confidently stated but false or unsupported content produced by a generative model, often called hallucination.

**Consensus.** Agreement among replicas on one value or one log order despite failures, under a stated fault model.

**Consistency.** A word with two common meanings: preserving database constraints within a transaction, or a replication guarantee about what reads can observe. Say which one you mean.

**Container.** A packaged, isolated runtime process; in the C4 model, a separately deployable application or data store.

**Contract.** The syntax, meaning, guarantees, limits and change rules of an interface.

**Conway's law.** The observation that systems tend to mirror the communication structure of the organisation that builds them.

**Coupling.** The degree to which a change in one part of a system forces a change in another.

**CQRS.** Command query responsibility segregation: one model for changing data and separate read models, each shaped for particular queries, for reading it.

**Data owner.** The role accountable for the business meaning and approved use of a set of data.

**Dead-letter queue.** A holding place for messages that failed normal processing and need controlled handling.

**Disaster recovery.** Restoring a service after a site or regional failure, with strategies that range from backup and restore to multi-site active/active.

**DORA metrics.** Five software delivery measures from the DevOps Research and Assessment programme (not the EU Digital Operational Resilience Act): change lead time, deployment frequency, failed deployment recovery time, change fail rate and deployment rework rate.

**Dual-write problem.** The inconsistency that arises when a service changes its database and sends a message as two separate actions, so that a crash between them loses or invents work.

**Durability.** The guarantee that committed data survives the failures that the storage system is designed to tolerate.

**Egress.** Data transferred out of a cloud region, usually charged per gigabyte.

**Elasticity.** The ability to add or remove resources as demand changes, within service and configuration limits.

**ELT.** Extract, load, transform: loading raw data into the target platform first and transforming it there, which makes the raw copy something the platform must protect.

**Error budget.** The amount of failure an SLO allows in its period, such as 0.1 percent of eligible requests in a month.

**ETL.** Extract, transform, load: transforming data before loading it into the target, which limits how far raw source fields spread.

**Event.** A record that something meaningful has happened.

**Event sourcing.** Storing every change to an entity as an event in an append-only log and deriving the current state by replaying the events.

**Event time.** When an event actually occurred, according to the system that recorded it.

**Expand and contract migration.** A schema change in three compatible phases: add the new structure, move data and readers across, then remove the old structure.

**Fact table.** An analytical table of measurements at a declared grain, such as a transaction fact, a periodic snapshot or an accumulating snapshot.

**Feature flag.** A runtime switch that separates deploying code from exposing its behaviour to users.

**FinOps.** The practice of managing technology spending for business value by working on both usage and price.

**Fitness function.** An automated check that fails when the system breaks an important architectural rule, such as a forbidden dependency between modules.

**Functional dependency.** A rule that one set of values determines another, such as a tenant and contract determining the contract's expiry date.

**Grain.** The business meaning of one row in a fact table.

**Grounding.** Basing a generated answer on supplied source passages, ideally with a citation to the passage behind each statement.

**Happened-before.** Lamport's ordering of events by order within a process, the sending of a message before its receipt, and transitivity; events not ordered this way are concurrent.

**ID token.** An OpenID Connect token that tells the client application who signed in; its audience is the client, so it is never a credential for calling an API.

**Idempotency.** The property that repeating an operation has the same intended effect as performing it once.

**Idempotency key.** A client-supplied identifier that lets a server recognise a repeated request and return the first result; Meridian's submission key is one.

**Inbox.** A processed-event table that a consumer updates in the same transaction as the state change an event causes, so that a redelivered event is recognised and skipped; also called an idempotent consumer.

**Information hiding.** Basing a module boundary on a design decision that the module keeps secret, so that a change to that decision stays inside the module.

**Infrastructure as code.** Versioned definitions of infrastructure that are applied through automation.

**Integration styles.** Hohpe and Woolf's four ways for applications to share data and behaviour: file transfer, shared database, remote procedure invocation and messaging.

**Invariant.** A condition that must hold before and after every allowed state change.

**ISO/IEC 25010.** The international product quality model that defines quality characteristics such as reliability, security and maintainability.

**Isolation level.** The degree to which concurrent transactions can observe one another's effects.

**JWT.** JSON Web Token: a compact token format, usually signed, whose claims can be trusted only after its signature, issuer, audience and lifetime have been validated.

**Landing zone.** A prepared cloud foundation of accounts, policies, networking, logging and deployment paths for workloads.

**Large language model.** A model trained on large amounts of text that generates text by repeatedly predicting the next token.

**Latency.** The elapsed time of an operation between stated start and end points.

**Lease.** A time-limited claim on a piece of work, such as an outbox record, which expires so that work held by a crashed worker becomes available again.

**Least privilege.** Giving each principal only the authority that its task requires.

**Lineage.** The record of a value's sources, transformations and processing runs.

**Linearizability.** A consistency condition in which every operation appears to take effect at a single instant between its start and its end, respecting real-time order.

**Little's law.** For a stable system, the average work in progress equals the arrival rate multiplied by the average time in the system.

**Liveness probe.** A health check that tells the platform when to restart a container.

**Mirroring hypothesis.** The proposition, tested by MacCormack, Baldwin and Rusnak, that a product's architecture mirrors the structure of the organisation that develops it.

**Normalisation.** Decomposing tables so that each fact is stored once and every non-key attribute depends on the whole key, which removes update, insertion and deletion anomalies.

**OAuth 2.0.** A framework for delegated access in which a client obtains access tokens to call protected resources.

**Observability.** The ability to understand a system's behaviour from the outputs it produces.

**OpenID Connect.** An identity layer on top of OAuth 2.0 that issues ID tokens telling a client who signed in.

**Partition.** Either a division of data across nodes or a network failure that splits nodes into groups. Say which one you mean.

**Pilot light.** A disaster-recovery strategy that keeps data replicated live in the recovery region but leaves the application switched off until a disaster.

**PKCE.** Proof Key for Code Exchange: an OAuth protection that binds an authorisation code to the client that requested it.

**Principal.** A person, service or device to which identity and authority are assigned.

**Prompt injection.** Input that changes a language model's behaviour in ways its designers did not intend, either typed directly or hidden in content that the application retrieves.

**Quality attribute scenario.** A testable requirement stated as source of stimulus, stimulus, environment, artefact, response and response measure.

**Quorum.** The minimum set of voters, usually a majority, whose agreement a distributed protocol needs before it can make progress.

**RBAC.** Role-based access control: permissions granted through roles, such as service agent or administrator.

**Read model.** A copy of data shaped for a particular query or screen, updated from the system of record and allowed to lag behind it.

**Readiness probe.** A health check that tells the platform whether a container should receive traffic.

**Repudiation.** The threat that someone performs an action and later denies it, while the system cannot prove otherwise.

**Retrieval-augmented generation.** Retrieving relevant passages and supplying them to a language model with the question, so that the answer can be grounded in them.

**Row-level security.** Database rules that filter which rows each user or session may read or change.

**RPO.** Recovery point objective: the largest acceptable loss of data, measured back in time from a failure.

**RTO.** Recovery time objective: the longest acceptable time to restore a service after a failure.

**Safety and liveness.** Two kinds of property: safety means that a bad outcome never happens, and liveness, or progress, means that useful work eventually completes under stated conditions.

**Saga.** A long-running process made of local transactions, each paired with a compensating action for use when the process cannot complete.

**SBOM.** Software bill of materials: a list of the components inside a built artefact, generated from the actual build.

**Schema compatibility modes.** The rules a schema registry checks between versions: backward (consumers on the new schema read old data), forward (consumers on the old schema read new data) and full (both).

**Sensitivity point.** An architectural parameter that strongly affects a measurable quality response.

**Serializability.** The guarantee that concurrent transactions produce the same result as some serial order of the same transactions.

**Session guarantees.** Consistency promises that hold within one client's session, such as read your writes and monotonic reads, as defined by Terry and colleagues.

**Sharding.** Splitting data across independent databases by a key, such as tenant or customer.

**SLA.** Service level agreement: a contract that sets service targets and the consequences of missing them.

**SLI.** Service level indicator: a measured property of a service, such as the proportion of successful requests.

**SLO.** Service level objective: a target for an SLI over a stated period.

**Snapshot isolation.** An isolation level in which each transaction reads a consistent snapshot and the first of two concurrent writers to the same row wins.

**Strangler fig.** A migration pattern, named after a fig that grows around a host tree, that routes functionality piece by piece to a new system until the old one can be removed.

**STRIDE.** A threat checklist of spoofing, tampering, repudiation, information disclosure, denial of service and elevation of privilege.

**Submission ID.** The UUID that the Meridian portal assigns when it stores a request; it appears in the receipt and is the idempotency key for the CRM handoff.

**Submission key.** The client-chosen idempotency key for a Meridian submission, unique for each tenant and submitting user.

**System of record.** The authoritative source for a defined set of business facts.

**Tail latency.** The latency of the slowest requests, such as those above the 99th percentile.

**Technical debt.** The future cost of change or operation created by earlier design or implementation choices.

**Tenancy model.** How a shared system separates tenants: a silo per tenant, a bridge of shared and dedicated parts, or a shared pool.

**Tenant.** A customer organisation or other administrative scope that a shared system keeps logically separate.

**Throughput.** Completed work per unit of time.

**Trade-off point.** A parameter that is a sensitivity point for more than one quality and affects them in different directions.

**Transactional outbox.** A table of outgoing messages written in the same transaction as the business change and delivered later by a separate process.

**Trust boundary.** A line across which assumptions about identity, authority or the trustworthiness of data change.

**Unit economics.** Cost or value expressed per business unit of output, such as cost per completed service request.

**Utility tree.** A hierarchy from overall utility through quality attributes to scenarios rated by importance and difficulty.

**View.** In ISO/IEC/IEEE 42010, a representation of one system that follows a viewpoint, such as the deployment view of the Meridian portal.

**Viewpoint.** In ISO/IEC/IEEE 42010, the conventions for building one kind of view: the concerns it addresses, its notations and model kinds, and how to analyse it.

**Watermark.** A pipeline's estimate that all events up to a given event time have arrived.

**Write skew.** An anomaly in which two transactions read overlapping data, write to different rows and together break an invariant that each would have preserved alone.

**Zero Trust.** An approach that removes implicit trust based on network location or asset ownership and decides each access from identity, resource and context.

## Final retrieval practice

Explain in a few sentences each:

- Why a timeout leaves the outcome of an operation unknown.
- Why a private subnet does not decide who may read a request.
- Why backups and replicas protect against different failures.
- Why two diagrams can both be correct while answering different questions.
- Why a vendor-neutral design can still choose a managed service.

Then choose one decision from your capstone and defend it without naming any product. State the requirement, the alternatives, the evidence, the trade-off and the condition that would change your choice. If you can do that clearly, you are practising the central work of an architect.
