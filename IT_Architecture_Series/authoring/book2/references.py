SOURCES = {
# Method: arguments, decisions and evidence
"c4": ("S. Brown", "The C4 model for visualising software architecture", "https://c4model.com/", "*c4model.com*, n.d."),
"adr": ("M. Nygard", "Documenting architecture decisions", "https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions", "*Cognitect blog*, Nov. 15, 2011"),
"atam": ("R. Kazman, M. Klein, and P. Clements", "ATAM: Method for architecture evaluation", "https://www.sei.cmu.edu/library/atam-method-for-architecture-evaluation/", "Software Engineering Institute, Carnegie Mellon University, Pittsburgh, PA, USA, Tech. Rep. CMU/SEI-2000-TR-004, Aug. 2000"),
"openclosed": ("B. Schroeder, A. Wierman, and M. Harchol-Balter", "Open versus closed: A cautionary tale", "https://www.usenix.org/conference/nsdi-06/open-versus-closed-cautionary-tale", "in *Proc. 3rd USENIX Symp. Networked Systems Design and Implementation (NSDI '06)*, San Jose, CA, USA, May 2006, pp. 239-252"),
"little": ("J. D. C. Little", "A proof for the queuing formula: L = λW", "https://doi.org/10.1287/opre.9.3.383", "*Operations Research*, vol. 9, no. 3, pp. 383-387, 1961, doi: 10.1287/opre.9.3.383"),
"parnas": ("D. L. Parnas", "On the criteria to be used in decomposing systems into modules", "https://doi.org/10.1145/361598.361623", "*Communications of the ACM*, vol. 15, no. 12, pp. 1053-1058, Dec. 1972, doi: 10.1145/361598.361623"),

# Integration studio
"http": ("R. Fielding, M. Nottingham, and J. Reschke, Eds.", "HTTP semantics", "https://www.rfc-editor.org/info/rfc9110", "IETF, RFC 9110, Jun. 2022, doi: 10.17487/RFC9110"),
"idemkey": ("J. Jena and S. Dalal", "The Idempotency-Key HTTP header field", "https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/07/", "IETF HTTPAPI Working Group, expired Internet-Draft draft-ietf-httpapi-idempotency-key-header-07, Oct. 15, 2025, work in progress"),
"outbox": ("Amazon Web Services", "Transactional outbox pattern", "https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html", "*AWS Prescriptive Guidance: Cloud design patterns, architectures, and implementations*"),
"pgselect": ("PostgreSQL Global Development Group", "SELECT: The locking clause", "https://www.postgresql.org/docs/18/sql-select.html", "*PostgreSQL 18 Documentation*"),
"helland2012": ("P. Helland", "Idempotence is not a medical condition", "https://doi.org/10.1145/2181796.2187821", "*ACM Queue*, vol. 10, no. 4, pp. 30-46, Apr. 2012, doi: 10.1145/2181796.2187821"),
"kleppmann": ("M. Kleppmann", "How to do distributed locking", "https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html", "Feb. 8, 2016"),
"lamport": ("L. Lamport", "Time, clocks, and the ordering of events in a distributed system", "https://doi.org/10.1145/359545.359563", "*Communications of the ACM*, vol. 21, no. 7, pp. 558-565, Jul. 1978, doi: 10.1145/359545.359563"),
"rabbit": ("RabbitMQ", "Consumer acknowledgements and publisher confirms", "https://www.rabbitmq.com/docs/confirms", "*RabbitMQ Documentation*"),
"azcompute": ("Microsoft", "Compare AWS and Azure compute services", "https://learn.microsoft.com/en-us/azure/architecture/aws-professional/compute", "*Azure Architecture Center*, Jun. 2026"),
"azdatabase": ("Microsoft", "Compare AWS and Azure database services", "https://learn.microsoft.com/en-us/azure/architecture/aws-professional/databases", "*Azure Architecture Center*, Oct. 2026"),
"azmessaging": ("Microsoft", "Comparing AWS and Azure messaging services", "https://learn.microsoft.com/en-us/azure/architecture/aws-professional/messaging", "*Azure Architecture Center*, Sep. 2026"),
"endtoend": ("J. H. Saltzer, D. P. Reed, and D. D. Clark", "End-to-end arguments in system design", "https://web.mit.edu/Saltzer/www/publications/endtoend/endtoend.pdf", "*ACM Transactions on Computer Systems*, vol. 2, no. 4, pp. 277-288, Nov. 1984, doi: 10.1145/357401.357402"),

# Transaction studio
"helland2007": ("P. Helland", "Life beyond distributed transactions: An apostate's opinion", "https://www.cidrdb.org/cidr2007/papers/cidr07p15.pdf", "in *Proc. 3rd Biennial Conf. Innovative Data Systems Research (CIDR)*, Asilomar, CA, USA, Jan. 2007, pp. 132-141"),
"isolation": ("PostgreSQL Global Development Group", "Transaction isolation", "https://www.postgresql.org/docs/18/transaction-iso.html", "*PostgreSQL 18 Documentation*, sec. 13.2"),
"serialfail": ("PostgreSQL Global Development Group", "Serialization failure handling", "https://www.postgresql.org/docs/18/mvcc-serialization-failure-handling.html", "*PostgreSQL 18 Documentation*, sec. 13.5"),
"saga": ("H. Garcia-Molina and K. Salem", "Sagas", "https://doi.org/10.1145/38713.38742", "in *Proc. 1987 ACM SIGMOD Int. Conf. Management of Data*, San Francisco, CA, USA, May 1987, pp. 249-259, doi: 10.1145/38713.38742"),
"tail": ("J. Dean and L. A. Barroso", "The tail at scale", "https://doi.org/10.1145/2408776.2408794", "*Communications of the ACM*, vol. 56, no. 2, pp. 74-80, Feb. 2013, doi: 10.1145/2408776.2408794"),
"linearizability": ("M. P. Herlihy and J. M. Wing", "Linearizability: A correctness condition for concurrent objects", "https://doi.org/10.1145/78969.78972", "*ACM Transactions on Programming Languages and Systems*, vol. 12, no. 3, pp. 463-492, Jul. 1990, doi: 10.1145/78969.78972"),

# Data studio
"kimball": ("R. Kimball", "Fact tables", "https://www.kimballgroup.com/2008/11/fact-tables/", "*Kimball Group*, Nov. 5, 2008"),
"dataflow": ("T. Akidau, R. Bradshaw, C. Chambers, S. Chernyak, R. J. Fernández-Moctezuma, R. Lax, S. McVeety, D. Mills, F. Perry, E. Schmidt, and S. Whittle", "The Dataflow Model: A practical approach to balancing correctness, latency, and cost in massive-scale, unbounded, out-of-order data processing", "https://www.vldb.org/pvldb/vol8/p1792-Akidau.pdf", "*Proceedings of the VLDB Endowment*, vol. 8, no. 12, pp. 1792-1803, Aug. 2015, doi: 10.14778/2824032.2824076"),
"kafka": ("Apache Software Foundation", "Design", "https://kafka.apache.org/43/design/design/", "*Apache Kafka 4.3 Documentation*"),
"azanalytics": ("Microsoft", "Compare AWS and Azure analytics services", "https://learn.microsoft.com/en-us/azure/architecture/aws-professional/analytics", "*Azure Architecture Center*, Sep. 2026"),
"codd": ("E. F. Codd", "A relational model of data for large shared data banks", "https://doi.org/10.1145/362384.362685", "*Communications of the ACM*, vol. 13, no. 6, pp. 377-387, Jun. 1970, doi: 10.1145/362384.362685"),
"gdpr": ("European Parliament and Council of the European Union", "Regulation (EU) 2016/679 (General Data Protection Regulation)", "https://eur-lex.europa.eu/eli/reg/2016/679/oj", "*Official Journal of the European Union*, L 119, pp. 1-88, May 4, 2016"),
"zerotrust": ("S. Rose, O. Borchert, S. Mitchell, and S. Connelly", "Zero trust architecture", "https://doi.org/10.6028/NIST.SP.800-207", "NIST SP 800-207, Aug. 2020, doi: 10.6028/NIST.SP.800-207"),
"airmf": ("E. Tabassi", "Artificial Intelligence Risk Management Framework (AI RMF 1.0)", "https://doi.org/10.6028/NIST.AI.100-1", "NIST AI 100-1, National Institute of Standards and Technology, Jan. 2023, doi: 10.6028/NIST.AI.100-1"),
"nist600": ("National Institute of Standards and Technology", "Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile", "https://doi.org/10.6028/NIST.AI.600-1", "NIST AI 600-1, Jul. 2024, doi: 10.6028/NIST.AI.600-1"),

# Modernisation studio and portfolio
"fowlerstrangler": ("M. Fowler", "Original strangler fig application", "https://martinfowler.com/bliki/OriginalStranglerFigApplication.html", "*martinfowler.com*, Jun. 29, 2004"),
"fowlerstrangler2024": ("M. Fowler", "Strangler fig", "https://martinfowler.com/bliki/StranglerFigApplication.html", "*martinfowler.com*, Aug. 22, 2024"),
"strangler": ("Microsoft", "Strangler Fig pattern", "https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig", "*Azure Architecture Center*"),
"pglogrepl": ("PostgreSQL Global Development Group", "Logical replication: Architecture", "https://www.postgresql.org/docs/18/logical-replication-architecture.html", "*PostgreSQL 18 Documentation*, sec. 29.9"),
"pglogsec": ("PostgreSQL Global Development Group", "Logical replication: Security", "https://www.postgresql.org/docs/18/logical-replication-security.html", "*PostgreSQL 18 Documentation*"),
"pgemptypath": ("N. Misch", "Empty search_path in logical replication apply worker and walsender", "https://www.postgresql.org/message-id/E1k5AbJ-0004t8-6p%40gemulon.postgresql.org", "*pgsql-committers* mailing list, Aug. 10, 2020, commit 11da970, security fix for CVE-2020-14349"),
"pgaltertable": ("PostgreSQL Global Development Group", "ALTER TABLE", "https://www.postgresql.org/docs/18/sql-altertable.html", "*PostgreSQL 18 Documentation*"),
"raft": ("D. Ongaro and J. Ousterhout", "In search of an understandable consensus algorithm", "https://www.usenix.org/conference/atc14/technical-sessions/presentation/ongaro", "in *Proc. 2014 USENIX Annual Technical Conference (USENIX ATC 14)*, Philadelphia, PA, USA, Jun. 2014, pp. 305-319"),
"pgsync": ("PostgreSQL Global Development Group", "Log-shipping standby servers: Synchronous replication", "https://www.postgresql.org/docs/18/warm-standby.html#SYNCHRONOUS-REPLICATION", "*PostgreSQL 18 Documentation*, sec. 26.2.8"),
}
