class IllegalTransition(Exception):
    """An event that the state model does not allow in the current state."""

# (reservation, payment, event) -> (new reservation, new payment, stock change)
RULES = {
    ('none', 'none', 'reserve'): ('active', 'pending', -1),
    ('active', 'pending', 'authorise'): ('active', 'authorised', 0),
    ('active', 'authorised', 'confirm'): ('committed', 'authorised', 0),
    ('active', 'pending', 'expire'): ('expired', 'pending', +1),
    ('committed', 'authorised', 'expire'): ('committed', 'authorised', 0),
    ('expired', 'pending', 'authorise'): ('expired', 'void_requested', 0),
    ('expired', 'void_requested', 'void_confirmed'): ('expired', 'voided', 0),
}

def run(events: list[tuple[str, str]]) -> str:
    reservation, payment, available, seen = 'none', 'none', 1, set()
    for name, event_id in events:
        if event_id in seen:
            continue                     # a repeated request or message changes nothing
        key = (reservation, payment, name)
        if key not in RULES:
            raise IllegalTransition(f'{name} while {reservation}/{payment}')
        reservation, payment, change = RULES[key]
        available += change
        seen.add(event_id)
        held = reservation in ('active', 'committed')
        assert available >= 0 and available + held == 1   # one unit in total
    return f'{reservation}/{payment}, available={available}'

R, A, X = ('reserve', 'r1'), ('authorise', 'p1'), ('expire', 'x1')
C, V, A2 = ('confirm', 'c1'), ('void_confirmed', 'v1'), ('authorise', 'p2')
for title, events in [('confirm before expiry', [R, A, C, X]),
                      ('reservation repeated after the sale', [R, A, C, R]),
                      ('late authorisation after expiry', [R, X, A, V]),
                      ('duplicate callback after void', [R, X, A, V, A]),
                      ('confirm after expiry', [R, X, C]),
                      ('new authorisation after void', [R, X, A, V, A2])]:
    try:
        print(f'{title}: {run(events)}')
    except IllegalTransition as error:
        print(f'{title}: rejected ({error})')
