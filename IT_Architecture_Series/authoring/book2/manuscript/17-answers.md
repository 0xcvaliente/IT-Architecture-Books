# Exercise answers and assessment guidance

Attempt each exercise before reading its answer. Calculations show their working and use the chapter's simplifying assumptions. Design and critique answers give one model answer and the criteria a marker should apply; a different answer earns equal credit when it meets the same criteria.

## Chapter 1

**1.1** One scenario observes acceptance: while one CRM is down for thirty minutes at the declared arrival rate, every valid submission receives a receipt that survives a restart of the portal, measured as zero lost receipts. A second observes recovery: after the CRM returns, the oldest pending handoff falls below one minute old within thirty minutes. Credit answers that give a stimulus, environment, response and threshold for each, and observe two different things.

**1.2** P = 0.5 × 4 + 0.2 × 3 + 0.3 × 3 = 3.5; Q = 0.5 × 5 + 0.2 × 4 + 0.3 × 2 = 3.9; R = 0.5 × 2 + 0.2 × 3 + 0.3 × 5 = 3.1. Model paragraph: "Q scores highest but cannot export data in an open format, which is mandatory, so Q is ineligible. Of the eligible options, P (3.5) beats R (3.1), and we recommend P. Choosing Q would require the owner of the export requirement to withdraw it and accept the exit risk." Credit answers that exclude Q before ranking.

**1.3** Context: the payment provider is an external authority. Container: the order coordinator owns the attempt. Sequence: the timeout follows a possible authorisation. Data: the provider operation ID and the state "payment unknown" are stored. Deployment: the reconciliation job runs with its own credentials. A contradiction a review could detect: the sequence retries with the same operation ID, but the data view has nowhere to store it.

**1.4** "When we grow" cannot be observed, and the trigger names a solution rather than a condition. A measurable rewrite: "Revisit the single-service design if a second team needs to release order logic independently more than twice a month, or if order processing exceeds 70 percent CPU at peak for two consecutive months after optimisation."

**1.5** (a) Constraint. (b) Preference. (c) Assumption, needing an owner, a test and a deadline. (d) Preference, unless the business sets a budget ceiling, which would make it a constraint.

## Chapter 2

**2.1** The net drain is 9 − 5 = 4 per second, so recovery takes 9,000 / 4 = 2,250 seconds, or 37.5 minutes. It fails the thirty-minute objective even before failures and slow calls are considered.

**2.2** First, after 2,000 independent failure-free trials the 95 percent upper bound is 1 − 0.05^(1/2,000) ≈ 0.15 percent, fifteen times the 0.01 percent claimed; supporting 99.99 percent would need 29,956 clean trials. Second, the trials may share causes of failure, such as one build or one host, so they are less independent than the count suggests, and they may never have exercised the failures that matter, such as a CRM outage or a crash at a transaction boundary. Full credit needs the calculation and both defects.

**2.3** Vary only the retry policy, for example fixed one-second retries against exponential backoff with jitter. Hold the build, data, CRM quota, offered workload and failure schedule constant. Observe distinct confirmed handoffs, unknown outcomes, oldest pending age, attempts and throttled calls per business unit. Inject a thirty-minute CRM outage and a worker crash after a CRM commit. Decision rule: both policies must lose nothing and create no duplicate in CRM A or C; among those, choose the one that clears the backlog sooner. Repeat runs and report the spread.

**2.4** At 0.5 seconds, each cycle takes 2.5 seconds, so the rate is 60 / 2.5 = 24 per second; at 3 seconds, 60 / 5 = 12 per second. The test halves its own load as the system slows, so it cannot show behaviour under the intended 24 per second; an open workload is needed for that question.

**2.5** W = L / λ = 1,875 / 3,000 per day = 0.625 days, or 15 hours on average. The average is well inside 24 hours, but the rule applies to every correction: with one nightly run, a correction that arrives just after a run starts waits about a day plus the run's duration, and longer if a run fails, so the worst case breaks the rule while the average looks safe. Little's law assumes a stable system over a long period, with arrivals and departures balanced; it gives the mean wait and says nothing about its spread or its maximum, which is what a deadline needs. Chapter 11 works through this case.

## Chapter 3

**3.1** CRM A keeps the external reference unique and returns the existing case for a repeat, so a retry is harmless. CRM B has no unique reference, so a repeat creates a second case, and its lagging index may not show the first. A common adapter cannot create a guarantee that CRM B lacks; B needs a delayed search with bounded manual review, or a contract change.

**3.2** Store the business unit with the submission at acceptance and use it for every delivery attempt; a change applies only to new submissions. Moving open requests needs a governed transfer that closes the case in the old CRM, records the new route and creates the case in the new CRM. Routing each retry by the customer's current business unit could deliver one request to two CRMs.

**3.3** Logical isolation, with separate work selection, limits and alerts in one deployment, handles a slow CRM well. A separate deployment also contains process-level failures, such as an adapter that exhausts memory on very large responses. Neither helps when the shared database fails. Credit answers that tie the boundary to a named failure.

**3.4** Timeouts: 36,000 × 0.008 = 288. Unresolved after the search: 288 × 0.25 = 72. Agent time: 72 × 5 = 360 minutes, or 6 hours per recall surge.

**3.5** CRM C down, `retry_due`: "Received" for the first minute, then "Received, awaiting service team". CRM B in `manual_review`: "Received, awaiting service team", because the customer needs reassurance, not the internal state. Confirmed and resolved: the CRM's status, "Resolved". Credit answers that never show an error for a safely stored request and never show a CRM status before confirmation.

## Chapter 4

**4.1** With only `lease_owner = $2`, thread 1's confirm matches the row, because the handoff is `in_flight` and its owner is still w3. It records attempt 4's result while attempt 5 is still running, and attempt 5's confirm later matches nothing because the state is no longer `in_flight`. With `attempts = $3` added, thread 1 passes 4 while the row holds 5, so its update changes no row; it logs the late reply for comparison, and attempt 5 records its own result. CRM C ends with one case: both sends carry the submission ID as the idempotency key within 24 hours, so the second returns the first response. The token protects the portal's record, and CRM C's contract protects the CRM. Credit answers that separate the two protections.

**4.2** Keep the record in `manual_review` with both candidate case IDs and the evidence for each. The agent compares them with the submission and applies one guarded update that moves the record to `confirmed` with the chosen case only if it is still in `manual_review`; a duplicate is closed through CRM B's own process. The system must not claim that the second case never existed or that the request failed. A late reply is compared with the recorded case ID and logged.

**4.3** A model ADR chooses polling: one delivery path per receipt, modest volumes and a team that runs PostgreSQL. The broker alternative offers independent consumers and buffering but adds a relay, a second durability boundary and more operation. Consequences: work selection and fairness are built in SQL, and replay is limited to the outbox. Trigger: a second consumer needs replay, polling exceeds 10 percent of database CPU at peak, or a business unit's oldest pending handoff exceeds its target at the agreed peak. Credit a measurable trigger.

**4.4** Either CRM B committed the case and its index has not caught up, or the create never committed. A search five minutes after the timeout cannot tell them apart, because the index has no stated maximum lag. Under ADR-M03 the handoff stays in `retry_due` with `next_action = 'lookup'` and `next_attempt_at` fifteen minutes after the timeout; if that lookup still finds no single match, the handoff moves to `manual_review`. A new create is never allowed after an unknown outcome with CRM B.

**4.5** Make the count and the claim atomic: the claim transaction first locks a per-business-unit row, for example `SELECT ... FROM unit_limit WHERE business_unit = 'B' FOR UPDATE`, or takes an advisory lock, then counts B's `in_flight` handoffs and claims at most 8 minus that count. A second worker waits for the first to commit and then counts again. Without the lock, both could see seven in flight and both claim one.

## Chapter 5

**5.1** The backlog is 5 × 2,700 = 13,500 handoffs. Clearing it in 1,800 seconds while 5 arrive each second needs 5 + 13,500 / 1,800 = 12.5 successful creates per second. With 15 percent failures that is 12.5 / 0.85 ≈ 14.7 attempts per second, and with 2 calls of polling about 16.7, so the quota must be at least 17. With 16 calls and polling on, creates get 14 calls, 11.9 succeed, the net drain is 6.9 per second and recovery takes about 13,500 / 6.9 ≈ 1,957 seconds, or 33 minutes, which misses. With polling paused, 13.6 succeed, the net drain is 8.6 and recovery takes about 1,570 seconds, or 26 minutes, which meets it. A longer outage therefore makes the polling pause part of the promise, not an optimisation.

**5.2** Attempts include retries and failed calls; the total across business units can hide CRM B's growing backlog; and completions may be counted at the worker rather than as confirmed CRM cases, so duplicates look like progress. Check successful completions against arrivals per business unit, the oldest pending age and the manual queue.

**5.3** Request a temporary uplift for declared recalls, run one account-wide limiter and pause CRM B status polling during recovery. Every request stays durable; customers of business unit B see "Received, awaiting service team" for up to about 16 minutes after an outage, and support needs a script explaining this. Until the uplift is confirmed, publish a 75-minute objective for B with the sponsor's approval. Discarding or failing accepted requests is never valid.

**5.4** Creates get 12 − 2 = 10 calls per second, of which 9 succeed; the net drain is 9 − 5 = 4 per second, so recovery takes 9,000 / 4 = 2,250 seconds, or 37.5 minutes, which fails. Pausing polling would give 10.8 successful creates per second and about 1,552 seconds, or 26 minutes, which meets it.

**5.5** The receipt shows that the portal stored the request, and a confirmed handoff shows that the CRM holds it; neither shows that an agent can act on it. Following Saltzer, Reed and Clark, that check can be completed only at the endpoint, the business unit's working queue, for example by a daily reconciliation of submissions against open CRM cases. The outbox and retries are valuable performance enhancements, not the end-to-end guarantee.

## Chapter 6

**6.1** After reserving three: A = 1,997, R = 3, C = 0. After confirming two: A = 1,997, R = 1, C = 2. After releasing one: A = 1,998, R = 0, C = 2. The sum is 2,000 at every step and nothing is negative.

**6.2** The promoted product still receives 350 attempts per second on its one allocation row, and every one of them meets the same row lock however the other products are spread. Useful responses act on that row: shorter lock-hold time, bounded admission or allocation buckets.

**6.3** The ceiling is 1 / 0.0025 = 400 per second. The offered 350 per second gives a utilisation of 350 × 0.0025 = 0.875, so the row keeps up on average, but waiting grows sharply near saturation and any burst above 400 builds a queue. If every attempt succeeds, the units last 2,000 / 350 ≈ 5.7 seconds.

**6.4** Utilisation is 200 × 0.0015 = 0.3, so the row is locked 30 percent of the time. With random arrivals, about 30 percent of attempts find it locked; under REPEATABLE READ each of those waits and then fails with SQLSTATE 40001 once the holder commits, even when units remain. If every failure retries until it succeeds, the attempt rate is about 200 / (1 − 0.3) ≈ 286 per second, and each failed attempt has held a connection while waiting. Under READ COMMITTED the second transaction waits, re-evaluates `available >= 1` against the newest row version and either takes a unit or changes nothing, so it can never oversell and needs no retry.

**6.5** The event carries the order ID, an event ID and version, the seller scope, the committed reservation IDs, the verified authorisation reference and the confirmation time. It means that invariant I4 holds; a checkout request entering a queue never produces it. Consumers deduplicate by event ID, and a later cancellation is a separate event.

**6.6** Step 1 finds `available` at zero, so the update matches no row, the insert adds nothing and the statement returns no row. Step 2 looks up the `reservation_id`, finds the active reservation for the same order and product, and returns it with its expiry time, which is the answer the first request would have received. If the service checked the sold-out flag first, the customer who holds the unit would be told "sold out", would probably leave, and the unit would stay reserved until it expired five minutes later. The flag may only answer requests whose identifier the service has never stored.

## Chapter 7

**Check your understanding (Chapter 7).** The stock proof rests on the guarded transitions: the conditional update that never takes a unit below zero, the single guarded transition that lets only one of expiry and confirmation consume a reservation, and, for buckets or regions, the conservation equation with its in-transit term. The workflow argument rests on the durable order states, each transition's operation ID, the payment-unknown and cancellation-pending states with owners, and the rule that a void is never treated as done until the provider confirms it.

**7.1** Yes. The guard compares `expires_at` with `now()`, which is 12:04:58, the start of the transaction, so the confirmation wins three seconds after expiry; a test in PostgreSQL 18 showed exactly this. I1 and I3 still hold, because the state guard and the row lock still let only one of expiry and confirmation consume the reservation. The broken rule is the five-minute expiry policy, stretched by however long the transaction stays open, so a unit that should have returned to stock goes to a late payer. Run the confirm as its own short transaction after the checks, or compare with `statement_timestamp()`, the start of the current statement. Credit answers that identify the transaction start time and keep the single guarded transition.

**7.2** Holding until the outcome is known prevents late authorisations without stock but lets slow or abandoned checkouts lock scarce units; control it with a maximum hold and per-customer limits. A fixed deadline frees units predictably but needs fresh reservations or voids for late results; control it with a reconciliation job and an owned cancellation-pending queue.

**7.3** The ceiling is 8 / 0.004 = 2,000 per second. With units in only 2 of 8 buckets, a random first pick misses with probability 6 / 8 = 75 percent. The service must try the remaining buckets, or check a total maintained in the same transactions, before answering "sold out".

**7.4** West available + East available + reserved + committed + in transit = 2,000. West asks East about transfer T. If East credited it, West marks T complete. If East has no record, East records T as refused, so it can never be credited later, and only then does West return the units. Reclaiming without East's answer could let both regions sell the same units. A region restored from backup must replay the transfer history before selling.

**7.5** Reservation-first keeps a unit for the paying customer but holds scarce stock; a late callback needs a fresh reservation or a void, and a timed-out void leaves the order in owned cancellation pending. Payment-first avoids holding stock for non-payers but can authorise payments with no stock left, making voids routine and needing the same pending state. Credit answers that cover both failures for both orderings and choose by the event's policy.

## Chapter 8

**8.1** A duplicate callback can receive a correct HTTP 200 while its effect is applied twice. The test must show that stock did not change again, no second charge or capture was made, the order made no extra transition, and the event ID was recorded.

**8.2** p95 latency measures only the time to an answer, while the policies admit different numbers of customers and leave different numbers of payments unresolved and units unsold. Further measurements: distinct customers admitted and confirmed, time from checkout to a final outcome, what rejected customers did next, and how many unresolved payments completed after the cutoff.

**8.3** Reserve one unit, let the provider authorise while delaying its reply, let the reservation expire, then deliver the authorisation. Expect no confirmation against the expired reservation, and either a fresh reservation or a void with a durable void request ID and the order in cancellation pending. Then make the void time out and expect the order to stay visibly pending. The design fails if the order is confirmed against released stock, stock goes negative, a second charge is made, or the order is marked cancelled before the void is confirmed.

**8.4** The history is invalid. In the sequential specification, r1 takes one unit, the repeat of r1 returns r1's reservation without taking another, and r2 then takes the second unit, so r2 should have succeeded. The final state also breaks I1: A + R + C = 0 + 1 + 0 = 1, not 2, so a unit has leaked. A likely defect is that the decrement and the insert run in separate transactions: the repeat of r1 decremented and committed, then its insert failed with SQLSTATE 23505, and nothing put the unit back. The fix is one statement or one transaction that rolls back on 23505, followed by the step 2 lookup. A test that checked only the replies, all of which look plausible, would miss the leak; comparing reservation rows with the counter catches it.

**8.5** The end-to-end mean is 40 + 60 + 150 = 250 milliseconds. Each stage takes 20 milliseconds with probability 0.97, at least 0.95, so each stage's p95 is 20 milliseconds and their sum is 40. Both stages are fast together with probability 0.97 × 0.97 = 0.9409, below 0.95, so the end-to-end p95 is 20 + 800 = 820 milliseconds.

**8.6** The late authorisation needs a stock condition, which the rule table cannot express, so `run()` checks it: when the key is `('expired', 'pending', 'authorise')` and `available >= 1`, the transition becomes `('active', 'authorised', -1)`, a fresh reservation; otherwise the existing void rule applies. To test the void branch inside a one-unit model, add an event in which another customer takes the returned unit, `('expired', 'pending', 'other_reserves')` with a stock change of −1, count it in a variable `other`, and change the assertion to `available + held + other == 1`. Two schedules then run: reserve, expire, authorise, confirm gives `committed/authorised, available=0`; reserve, expire, other_reserves, authorise, void_confirmed gives `expired/voided, available=0`. Credit answers that keep the one-unit invariant true in both schedules.

**8.7** Utilisation is (350 + 300) × 0.0014 = 0.91, too close to 1: waits would grow long and any burst would overload the row. Two buckets give 0.455 each, still above 0.4; three give about 0.30 each, so three buckets are needed. At the end of the sale, units remain in fewer buckets, so a random first pick misses more often, up to two times in three when only one bucket has units; the service must try the other buckets before answering "sold out", and arrival order across buckets is lost.

**8.8** If the reply to a block request is lost, Aster has already debited 100 units into an in-transit record. A retry with a new transfer ID looks like a new request, so Aster debits a second block, and the partner may credit both, or credit one and leave 100 units stuck in transit. Either way, the conservation equation no longer matches what was sold. Contract term: "Each block request carries a transfer ID chosen by the partner; after a timeout the partner retries or queries with the same ID, and Aster returns the original result for an ID it already holds." Test: drop the reply to a block transfer in the joint test, let the partner retry, and check that the transfer table holds one transfer and that Aster's in-transit units plus the partner's credited units equal 100.

## Chapter 9

**9.1** A closure-time measure counts only closed requests, so a division that leaves difficult requests open reports faster closures while customers wait longer. Publish the count and age of open requests alongside it, and define the population explicitly.

**9.2** Total hours are 10 × 2 + 90 × 6 = 560 across 100 requests, a combined mean of 5.6 hours. Averaging the two means gives 4 hours and treats 10 requests as if they were as numerous as 90.

**9.3** Keep the source system, source event ID, source version, event time, processing time and a digest of canonical content. Same ID, version and digest: a duplicate. A higher version of the same ID: a correction. Same ID and version with a different digest: a conflict for quarantine.

**9.4** The event belongs to the 10 May window. It reaches Beacon on 13 May, after the publications of 11, 12 and 13 May, so the run that starts at 01:00 on 14 May includes it and restates 10 May at 07:00 on 14 May, within the seven-day window. In the accumulating and retracting refinement mode, the new value replaces the old and the publication records which one it supersedes. The dashboard marks 10 May as restated, shows the previous value and gives the reason, a late record from the late-arriving source.

**9.5** The correct total is 700 × 3 + 300 × 8 = 4,500 hours over 1,000 requests, a mean of 4.5 hours. After the join, each large customer's completion appears twice, so there are 1,300 rows and 2,100 + 2 × 2,400 = 6,900 hours, a mean of about 5.31 hours: the total is inflated by half and the mean drifts towards the duplicated group. Tests: the number of rows after the join must equal the number of completions, and the dimension's business key must be unique among its current rows. Counting distinct request keys in the result is a useful third check.

## Chapter 10

**10.1** Four hours are 14,400 seconds, so the minimum average rate is 10,000,000 / 14,400 ≈ 694.44 records per second. It ignores transformation cost, skew, joins, retries, checks and publication, so a capacity plan needs measured rates on representative data and time reserved for reruns.

**10.2** In a fresh ledger: P1, day 2, mean (2 + 6) / 2 = 4.0 hours over 2 requests; P2, mean (2 + 6 + 13) / 3 = 7.0 hours over 3, superseding P1 because r6 arrived late; P3, mean (5 + 6 + 13) / 3 = 8.0 hours over 3, superseding P2 because r4 was corrected. The latest mean is twice the first, yet nothing about day 2's service changed: one slow closure arrived late and one start time was corrected. Only the ledger's inputs and reasons show this, so the dashboard should display them with any restated value.

**10.3** Key events by source and event ID and keep the highest version. A repeat of the same version and content has no effect; an older version never replaces a newer one; the same version with different content goes to quarantine for the source owner. Affected publications are restated only through the versioned correction process, and arrival order never decides.

**10.4** For the monthly snapshot, batch fits naturally with a formal close at a fixed extract boundary. For the intraday view, only streaming can help, and only for the three streaming sources, so the view must say that extract-based sources are a day old. A hybrid is a strong answer.

**10.5** A withdrawal is a new version of the same request with a withdrawn flag, for example ('r3', 2, 1, None), which `latest()` keeps as the current version and `publish()` excludes from the mean while listing it among the inputs. After r3 is withdrawn, day 1 is computed from r1 (4 hours) and r2 version 2 (16 hours): P4, mean 10.0 hours over 2 requests, supersedes P3 with the reason "withdrawal of r3". The ledger must show the fall from 3 requests to 2 and the reason, so that a reader does not mistake the higher mean for slower service.

## Chapter 11

**Check your understanding (Chapter 11).** Evidence: the metric version and population used, source completeness for the period, the case mix by product and complexity, staffing and workload per agent, and the same measure for comparable divisions over time. Alternative explanations to rule out: a changed metric definition, a late or missing source, more difficult requests, more reopened cases, a policy or process change, and too few agents rather than slower ones. Even then, "less efficient" is a judgement about people that the data alone cannot support; a publishable sentence reports the measured difference and its likely causes.

**11.1** (a) A key-set comparison finds both the duplicates and the missing records; a row count misses them, because they cancel. (b) Grouped totals by division find the misassignment; a key-set comparison misses it, because every key is present. (c) A digest of canonical content, or a value comparison, finds the changed amounts; grouped totals may miss them if the rounding differences cancel within a group. (d) A relationship check finds the orphan closures; counts and key sets on the closures table alone miss them. All checks must use the same extraction boundary.

**11.2** Before republishing, reapply every lifecycle decision recorded since the backup from the controlled list, and verify that the removed record is absent from the raw zone and every rebuilt table, index, cache and export. A restore that ignores later deletion decisions is incomplete even when the database restore succeeds.

**11.3** Check the metric version, source completeness, provisional data, case mix, reopened requests, late events, policy changes and staffing levels, and look for evidence that separates the explanations, such as the same slowdown in other divisions. A correlation with a division does not show that its staff caused it; a generated narrative should report supported observations with links and pass human review.

**11.4** Model answer for Alternative B: own division, tenant in scope (allow); own division, tenant out of scope (deny); another division (deny); group analyst, approved aggregate (allow); group analyst, raw detail (deny); revoked analyst, anything (deny). Run every case through the dashboard, notebook, direct query and export, showing that a missing path is truly inaccessible rather than untested.

**11.5** A curated view can keep its columns and meaning while one source moves from extracts to a change stream, so dashboards and notebooks need no change, which is the protection Codd's data independence describes. It does not decide the grain of a fact, the metric definition or the correction policy.

**11.6** The longest gap follows the 19:00 run: a correction arriving at 19:01 joins the nightly run at 01:00 and appears at 07:00, about 12 hours later. With one failed run the worst case is a correction arriving at 13:01 whose 19:00 run fails: it joins the nightly run and appears at 07:00, about 18 hours later. With two consecutive failures, a correction arriving at 07:01 misses 13:00 and 19:00 and appears at 07:00 the next day, just under 24 hours later, with no margin. The schedule can absorb one failed run safely, against three for the four-hourly schedule in ADR-B02, whose worst case after three failures is about 22 hours.

**11.7** The request mixes two products. The regulator's rule names the daily service figures, while the monthly snapshot exists so that finance can reproduce a closed month exactly. Restating a closed month would break that purpose and gain nothing the regulator asked for. A good response keeps the close, records late corrections as adjustments in the next month's close with a reference to the daily restatement, and shows finance the reconciliation between the two. Credit answers that distinguish the products and keep both requirements visible.

## Chapter 12

**12.1** Monthly jobs, rare recovery procedures, occasional partner updates and support scripts may not run in one week, as the finance job shows. Add scheduler entries, database account lists, configuration and owner interviews, and observe across a month end.

**12.2** Rehosting is favoured when the deadline is firm and phased migration cannot show credible progress by the decision date, provided the old platform can run securely on new hosting. Phased migration is favoured when a stable seam exists, CDC works on the source and the intermediate states can be operated. Compare the total cost of coexistence, migration and any later second move.

**12.3** Assign authority at order creation, record it with the order and keep it for the order's life: orders created before a cohort's switch stay with the legacy platform until they close, or move through a governed transfer. Never route updates by an attribute that can change, and cover partner, batch and support writers as well as the web shop.

**12.4** Find the account's owner and the code or job that uses it, read what it changes, and ask the support manager whether the behaviour is still needed. If it is, rebuild it as a scheduled function of the new service and add it to the inventory, fence plan and dual-run comparison. If not, retire it by an approved change before cutover and disable the account.

**12.5** Without the epoch term, a delayed dispatch command from the legacy platform could be accepted after cutover, risking a second dispatch. Orion can compensate by disabling the legacy platform's partner credentials at the fence, giving every dispatch command a unique ID that the partner deduplicates, and reconciling dispatches daily. These controls are weaker, because they rely on Orion finding every path to the partner.

## Chapter 13

**13.1** Changes committed between P0 and P1, from 01:00 to 01:20, are in neither input: the snapshot was taken before them and CDC starts after them. Each job checks only its own work, so both report success. Starting CDC before P0 would apply some changes that the snapshot already contains, so the applier must be idempotent, for example by applying each change only if its position is later than the one recorded for the row. The safe design starts CDC exactly at the snapshot's position.

**13.2** Queued changes: 8 × 3,600 × 17.4 ≈ 501,000. The net drain is 250 − 17.4 = 232.6 per second, so catch-up takes about 501,000 / 232.6 ≈ 2,150 seconds, or 36 minutes, at the average rate; a weekday peak would take longer.

**13.3** For the application, marketplace import, partner account, finance job and `ops_batch`: revoke write rights, end sessions, disable any scheduler entry, and attempt a probe write with each account, which must fail. The partner also confirms that it uses the new route. Record the final log position only after all five probes fail.

**13.4** O-201 disappears from `legacy_order` but remains in the target, so the query reports it as "extra in target". The result is false: the target has simply not yet applied the deletion at position 1005. Keep deletions visible on the legacy side, for example as a tombstone row with the position of the deletion, or read deleted keys from the change log, and exclude any key whose deletion lies after the applied position from the "extra" check until the next run.

**13.5** Returning authority is possible because reverse CDC keeps the legacy database current and the new states are disabled; it contains the defect quickly but needs a fence on the new store and a correction of VAT values already written. Fixing forward keeps authority in place and is faster for a small, well-understood fix. Needed information: the number of affected orders, whether invoices have gone out, the time to fix, and whether reverse CDC is current.

## Chapter 14

**14.1** The latest safe decision becomes 45 − 8 = 37 minutes. With 14-minute smoke tests, the revised plan decides at 6 + 3 + 6 + 2 + 14 + 3 = 34, which fits with three minutes to spare, and the rule changes to "smoke tests must pass by minute 34".

**14.2** The worst time appears once in three rehearsals for steps 1, 2, 3 and 5, twice for step 4 and in all three for step 6, so the probability is (1/3)⁴ × 2/3 × 1 = 2/243, under 1 percent. Summing the worst times is therefore very conservative when steps vary independently. The reasoning fails when steps share a cause, such as month-end load slowing both the drain and the reconciliation, and when three rehearsals have not revealed the true worst case of a step.

**14.3** "ADR-O07, week −16. The partner's status API will arrive six weeks late, in week −8. We will cut over as planned in week −10, using the partner's 15-minute status file, converted to API calls by Orion's adapter. Conditions: rehearsal 4 in week −12 processes a full day's file; the business owner approves a temporary 20-minute status objective; the partner moves to the API by week −4; after a no-go that cannot be fixed within a week, we give the hosting extension notice by week −8. Owner: migration lead. Next review: after rehearsal 4." Credit a notice that names the option, conditions, owner and review date.

**14.4** Clean final reconciliation (report, confirmed by the data owner); every legacy writer fenced (failed probes, database lead); epoch 8 active with the applier rejected (failed applier write, database lead); smoke tests passed, including the partner call (test log, test lead); reverse path ready (operators and scripts, operations lead). The cutover manager collects the confirmations and the business owner decides.

**14.5** The proposal sends the first customer writes to the new service before any end-to-end test in production. Any fault in identities, routing, configuration or the partner call would reach customers, and the six-minute reverse path would be lost because real orders would exist only in the new store. Saving nine minutes does not justify that when the plan already has ten minutes of margin.

## Chapter 15

**15.1** "For release 1.4, at the tested peak of 20 submissions per second, the receipt path meets Q1, Q3 and Q6: the peak load test returned 95 percent of receipts within 0.6 seconds (X-02), local-commit and outage tests lost no receipt (X-03 to X-05), and the tenant-scope tests disclosed nothing (X-06). Open conditions: the vendor confirms CRM B's quota in writing (sponsor, by 30 April), and a timed database restore is rehearsed (operations lead, by 15 May)." Credit scope, version, evidence and owned conditions.

**15.2** "Which requirement do you expect microservices to improve: independent release, scaling one part, or isolating a failure? If we pick one, I will compare both designs against that scenario, including the cost of the extra network boundary. If the split wins, we revise the decision record; if not, we record the trigger that would reopen it." Credit a respectful answer that asks for the requirement.

**15.3** The `ops_batch` script is closed once rebuilt or retired and a probe write with its account fails. The partner delay is an accepted residual risk under ADR-O07, with an owner and review date. The DNS time-to-live is a deferred investigation until it is lowered and verified a day before cutover.

**15.4** Executive: "Demand will far exceed our 2,000 units. We will admit up to 50 checkouts at a time for the product and ask others to retry, so that admitted customers get an answer within seconds and nothing is oversold. In testing this sold 1,988 units, compared with 1,942 when everyone was admitted." Engineering: a 50-attempt admission gate per hot product, the reservation statement at READ COMMITTED, a sold-out flag, and the experiment results with their limits.

**15.5** P = 4 × 3 = 12 and Q = 2 × 5 = 10, so P ranks first. Rating Q's likelihood at 3 gives 15 and reverses the order, as would rating P's likelihood at 3, giving 9. The review should record the reasoning behind each score and treat the risks as close.

## Chapter 16

**16.1** Meridian and Aster both record durable intent with an operation ID so that a crash cannot erase a commitment. Meridian's receipt says nothing about the CRM case, which the CRM owns once confirmed, while Aster's confirmed order depends on two authorities: its own stock and the payment provider.

**16.2** Apply the same rubric to both versions and cite specific improvements, such as a failure sequence that exposed a race or a repeated experiment that confirmed a recovery assumption. Do not award points for extra pages. State the remaining weaknesses and whether the revision changes the release decision.

**16.3** Technical, month one: build and fault-test the outbox and claim query, evidenced by code and an experiment record. Stakeholder, month two: run a review of one decision, evidenced by a revised decision record. Operational, month three: rehearse a recovery with a colleague, evidenced by a timed report. State which experiences were simulated.

**16.4** In Raft, an entry is committed once a majority of servers has stored it; any future leader holds every committed entry, and all servers apply the same entries in the same order, so a committed entry survives a leader failover. With PostgreSQL's default asynchronous replication, a failover can lose commits that the primary had already confirmed, so a customer may hold a reservation that the new primary does not have, and the stock count is one unit too high. With `ANY 1 (s1, s2)` and `synchronous_commit = on`, every confirmed commit is on disk on at least one standby, so promoting the standby with the latest commits keeps it. The price is a standby round trip inside every commit, which lengthens the lock-hold time and lowers the hot row's ceiling, and commits stall if no listed standby responds. In both cases the application still handles unknown outcomes: a client whose request timed out retries with the same `reservation_id`, and the step 2 lookup returns the reservation if it survived; if it did not, the retry is a new attempt. Payment compensation lies outside the log. Credit answers that make the PostgreSQL guarantee conditional on synchronous commit and the failover choice.

**16.5** At risk: the claim that every legacy and support writer was fenced and its account disabled; the retirement checklist; the authority epoch, if the account can declare the current epoch; and the assumption that the writer inventory was complete. Immediate actions: identify the account, its owner and the statements it ran, revoke its privileges, and check whether the 40 updates conflicted with the new service's orders, correcting them through the normal business process. Follow-up: add the source to the writer inventory with its evidence, decide whether its function must be rebuilt in the new service, and add a daily check for writes by unexpected roles. Credit answers that connect the event to the fence and the inventory without inventing facts about the account.
