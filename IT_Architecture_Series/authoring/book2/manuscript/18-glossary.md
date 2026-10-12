# Glossary

**Accumulating and retracting mode.** A refinement mode (an accumulation mode in the Dataflow Model) for emitting a later result for a window in which the new value replaces the earlier one and the earlier value is explicitly withdrawn; Beacon's restatements work this way.

**Admission control.** A rule that limits how much work enters a system, for example at most 50 reservations in flight for one product, so that admitted work finishes and the rest receives a clear answer.

**Architecture decision record (ADR).** A short document that records one significant decision with its context, alternatives, consequences, evidence and review triggers, under a stable identifier such as ADR-M05.

**Architecture dossier.** The connected set of documents that explains a design and the reasons for it: brief, quality scenarios, views, decision records, experiments, findings and a decision brief.

**Assumption.** A statement believed to be true but not yet verified; it needs an owner, a verification task and a deadline.

**Authority epoch.** A number that increases each time write authority over a domain moves; the data store rejects writers whose declared epoch is not the current one.

**Bucket.** One of several rows that together hold a product's allocation, so that reservations spread their locks across rows and the throughput ceiling rises to about k / h for k buckets.

**Change card.** A one-page statement of a new fact that arrives part-way through a studio, with the assumptions and decisions it affects and the question it raises.

**Change data capture (CDC).** Reading committed changes from a database's transaction log and applying them to another store, so that every committed writer is seen.

**Closed workload.** A load test in which a fixed population of virtual users each waits for a response before sending again, so the offered load falls as the system slows.

**Compensation.** A business action that semantically undoes an earlier step of a saga, such as releasing a reservation or voiding a payment authorisation; it can itself fail or stay pending.

**Constraint.** A requirement that decides whether an option is eligible at all; it is applied before preferences are scored.

**Cutover.** The planned moment when write authority moves from an old system to a new one, usually inside a maintenance window.

**Decision brief.** A one-page summary for the person who must decide: what changed, what stays the same, the options with cost and effect, a recommendation and its conditions.

**Dossier.** See architecture dossier.

**Dual run.** A period in which the old system stays authoritative while the new one receives the same data or requests, and daily comparisons check that both agree.

**Event time.** The time at which the source says a business event happened, as opposed to when it was processed or published.

**Fencing token.** A number that increases each time a lease or authority is granted; the system that receives a write rejects any write carrying an older number.

**Grain.** The exact meaning of one row in a fact table, such as one row per request and reporting day.

**Handoff.** The delivery of a stored submission to the business unit's CRM, tracked in one of five states: `pending`, `in_flight`, `confirmed`, `retry_due` or `manual_review`.

**Hot row.** A single database row that a large share of transactions must lock, such as the stock row of a promoted product.

**Idempotency key.** A client-chosen identifier sent with a request so that the server can recognise a repeat and return the original result instead of acting twice.

**In-transit record.** A durable record of units or work that one party has debited and another has not yet credited, identified by a transfer ID so that the transfer completes exactly once.

**Invariant.** A condition that must hold after every transaction, such as A + R + C = 2,000 for Aster's event stock.

**Isolation level.** The degree to which concurrent transactions see each other's changes; PostgreSQL offers READ COMMITTED, REPEATABLE READ and SERIALIZABLE.

**Latest safe decision point.** The last moment in a cutover window at which a "no" can still be carried out in time, equal to the end of the window minus the rehearsed time to reverse.

**Lease.** A time-limited claim on a piece of work, recorded with its owner and expiry, after which another worker may take the work.

**Linearizability.** A correctness condition under which every operation appears to take effect at one instant between its start and its end, in an order that the object's sequential specification allows.

**Little's law.** For a stable system over the long run, the average number of items in the system equals the arrival rate multiplied by the average time each item spends there: L = λW.

**Lock-hold time.** The time a transaction holds a row lock, from the update until the commit completes; written h, it limits the row to about 1 / h updates per second.

**Metric contract.** A definition of a measure that fixes its population, start and end events, time zone, exclusions, owner and version.

**Open workload.** A load test in which requests arrive on a schedule whether or not earlier requests have finished, as real customers do during a surge.

**Outbox.** A table written in the same transaction as a business change, recording the intent to send a message; a worker or relay delivers it later.

**p50, p95, p99.** The 50th, 95th and 99th percentiles of a set of measurements; p50 is the median, and p95 is the value that 95 percent of observations do not exceed.

**Percentile.** The value that a stated percentage of observations do not exceed; it says nothing about the observations above it.

**Preference.** A statement that ranks eligible options, such as low cost or fast delivery, without excluding any of them.

**Processing time.** The time at which a pipeline received or processed a record, as opposed to the event time the source reports.

**Publication ledger.** An append-only record of every published result, with its identifier, value, the exact inputs it used and the publication it supersedes.

**Publication time.** The time at which a particular result became visible to its readers.

**Quality gate.** A check that must pass before a result is published; a gate that can never fail protects nothing.

**Quality scenario.** A requirement stated as a stimulus, an environment, a required response and a measure, so that it can be tested.

**Receipt.** The portal's confirmation that it has durably stored a submission and taken responsibility for its handoff.

**Reconciliation.** A comparison of two stores, by key sets, versions, relationships, totals or content digests, within a declared boundary, to find records that are missing, extra or different.

**Refinement mode.** How a later result for a window relates to an earlier one: discarding, accumulating, or accumulating and retracting; the Dataflow Model calls it the accumulation mode.

**Replication lag.** The time between a change committing in the source and the same change being applied in the target.

**Reservation.** A record that holds one unit of stock for an order until it is committed, released or expired; its identifier makes a repeated request harmless.

**Restatement.** A new publication of a past period's result that replaces an earlier one because late, corrected or withdrawn data changed it.

**Retry storm.** A surge of load caused by failed requests being retried, which adds more contention and causes further failures.

**Review trigger.** An observable condition, recorded in a decision record, that should reopen the decision when it occurs.

**Saga.** A long-lived transaction split into a sequence of smaller transactions, each paired with a compensating action that semantically undoes it if the sequence cannot finish.

**Serialization failure.** An error, SQLSTATE 40001, that PostgreSQL raises under REPEATABLE READ or SERIALIZABLE when a transaction would conflict with a concurrent one; the whole transaction must be retried.

**Strangler fig.** A migration approach in which a new system grows around the old one behind a routing seam until the old one can be removed.

**Synchronous replication.** Replication in which a commit waits until one or more standbys confirm that they have stored it, so that a failover does not lose confirmed transactions.

**Tenant.** A customer organisation whose data is kept separate from other customers' data in a shared system.

**Trigger (Dataflow Model).** The rule that decides when to emit a result for a window, for example at 07:00 each morning for the previous day, and at each later run while late data for that day keeps arriving.

**Utilisation.** The fraction of time a resource is busy, equal to its arrival rate multiplied by the time each request occupies it; waiting grows sharply as utilisation approaches 1.

**Void.** The cancellation of a payment authorisation before money is captured, as opposed to a refund of money already captured.

**Watermark.** A system's estimate of how complete its input is up to a given event time.

**Window.** A grouping of events by event time, such as one business day, for which a result is computed.

**Write fence.** A control that stops an old authority from changing data after authority has moved, enforced where the data is stored.

**Zero-failure bound.** The upper limit on a failure probability that a run of n independent failure-free trials supports; at 95 percent confidence it is 1 − 0.05^(1/n).
