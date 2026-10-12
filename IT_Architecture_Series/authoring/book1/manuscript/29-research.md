# Research study guide

Use these readings to practise turning an argument into a design decision. The chapters summarise each idea briefly; read the relevant passages in the source and write your own critique. An old paper can still make a lasting theoretical contribution, while an old implementation detail may no longer describe a current product. Keep those two questions apart.

## Foundational papers and reports

| Reading | Focus in the source | Your analytical task |
| --- | --- | --- |
| Parnas on modular decomposition {REF:parnas} | Alternative criteria for dividing a system into modules | Find a decision in your design that is likely to change, and test whether one module hides it |
| Codd on the relational model {REF:codd} | Data independence and logical representation | Separate a business dependency from a physical access path in your schema |
| Saltzer, Reed and Clark on end-to-end arguments {REF:endtoend} | Where correctness responsibility belongs | Explain why a transport acknowledgement is insufficient as a business receipt |
| Lamport on time and ordering {REF:lamport} | Partial order and logical clocks | Draw concurrent events and state what a timestamp can and cannot establish |
| Herlihy and Wing on linearizability {REF:linearizability} | A correctness condition for concurrent objects | Classify two read histories from your design as linearizable or not |
| Gilbert and Lynch on CAP {REF:cap} | Formal definitions and partition assumptions | Describe one operation that must refuse progress to keep its consistency promise |
| Ongaro and Ousterhout on Raft {REF:raft} | Election, log replication and safety conditions | Explain why majority replication is part of an algorithm, more than a design slogan |
| Dean and Barroso on tail latency {REF:tail} | Outliers in requests that fan out to many servers | Challenge the independence assumption in the fan-out calculation of Chapter 12 |
| Fielding's dissertation, Chapter 5 {REF:rest} | REST constraints and their consequences | Audit one API against the constraints, keeping REST distinct from JSON |
| Garcia-Molina and Salem on sagas {REF:saga} | Long-lived transactions and compensation | Contrast the single-database setting with the commerce workflow and list the extra assumptions an external provider adds |
| Kohnfelder and Garg on STRIDE {REF:stride} | The first statement of the six threat categories | Apply each category to one data flow and judge which threats the paper's examples miss today |
| Kazman, Klein and Clements on the ATAM {REF:atam} | Utility trees, scenarios, sensitivity and trade-off points | Evaluate one important decision and list the evidence still missing |
| Akidau and colleagues on the Dataflow Model {REF:dataflow} | Event time, processing time, watermarks and triggers | Map the paper's concepts onto a daily batch publication and its correction policy |

These sources differ in kind. The journal and conference papers went through academic review; Fielding's work is a doctoral dissertation; the ATAM document is a university technical report; the STRIDE paper first appeared in an internal company journal. Weigh each claim with that history in mind.

## Practitioner sources and standards

Some influential ideas come from practitioners rather than from research. Fowler's strangler fig article {REF:fowlerstrangler} and the SRE Workbook's chapter on alerting {REF:sloalert} record methods refined in practice. Read them for the problem each method solves and the responsibilities it adds; they describe experience, and controlled experiments proving the method superior are rare.

Read HTTP, TLS, OAuth and OpenID Connect references for the specific protocol property discussed in a chapter. Read NIST publications for the scope and intent of their guidance. Read database documentation for the exact version's constraints and isolation behaviour. Treat Azure, AWS, orchestration and observability documentation as a description of current product behaviour, and check it again before implementation.

## A source critique you can assess

For each selected reading, write 400 to 600 words that cover:

1. the question the source addresses;
2. its method or argument;
3. its assumptions;
4. one conclusion you can support;
5. one limitation or boundary;
6. a concrete implication for your case.

Cite the exact source and section, and keep what the author establishes separate from your own inference. A strong critique need not reject the source; it shows where the result can responsibly be used.

Finish by proposing an observation that could challenge your recommendation. For example, a module boundary justified by expected vendor change becomes less valuable if the dominant change turns out to be cross-cutting policy. Keep the foundational argument and your application of it distinguishable.
