import sqlite3

db = sqlite3.connect(':memory:')
db.executescript("""
CREATE TABLE legacy_order (order_id TEXT PRIMARY KEY, status TEXT,
                           total_cents INTEGER, last_lsn INTEGER);
CREATE TABLE target_order (order_id TEXT PRIMARY KEY, status TEXT,
                           total_cents INTEGER);
INSERT INTO legacy_order VALUES ('O-201', 'shipped', 12500, 880),
    ('O-202', 'open', 4999, 905), ('O-203', 'open', 800, 910),
    ('O-204', 'packed', 2300, 1003), ('O-206', 'open', 1500, 1004);
INSERT INTO target_order VALUES ('O-201', 'shipped', 12500),
    ('O-202', 'open', 5000), ('O-204', 'open', 2300), ('O-205', 'open', 800);
""")
RECONCILE = """
SELECT 'missing in target' AS issue, l.order_id
FROM legacy_order AS l LEFT JOIN target_order AS t ON t.order_id = l.order_id
WHERE t.order_id IS NULL AND l.last_lsn <= :applied
UNION ALL
SELECT 'extra in target', t.order_id
FROM target_order AS t LEFT JOIN legacy_order AS l ON l.order_id = t.order_id
WHERE l.order_id IS NULL
UNION ALL
SELECT 'values differ', l.order_id
FROM legacy_order AS l JOIN target_order AS t ON t.order_id = l.order_id
WHERE (l.status IS NOT t.status OR l.total_cents IS NOT t.total_cents)
  AND l.last_lsn <= :applied
ORDER BY 1, 2
"""

def reconcile(label: str, applied: int) -> None:
    issues = db.execute(RECONCILE, {'applied': applied}).fetchall()
    later = db.execute('SELECT count(*) FROM legacy_order WHERE last_lsn > ?',
                       (applied,)).fetchone()[0]
    print(f'{label}: {len(issues)} differences, {later} orders left for the next run')
    for issue, order_id in issues:
        print(f'  {order_id}: {issue}')

reconcile('ignoring the CDC position', applied=10**9)
reconcile('up to applied position 1000', applied=1000)
