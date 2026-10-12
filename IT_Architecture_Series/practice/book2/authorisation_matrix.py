PRINCIPALS = {      # authenticated identities with their approved scope
    'ana': {'role': 'analyst', 'division': 'N', 'tenants': {'T1', 'T2'},
            'active': True},
    'sam': {'role': 'analyst', 'division': 'S', 'tenants': {'T1', 'T2', 'T3'},
            'active': True},
    'gita': {'role': 'group', 'active': True},
    'pat': {'role': 'publisher', 'active': True},
}
RESOURCES = {f'{d}{t}': {'kind': 'detail', 'division': d, 'tenant': f'T{t}'}
             for d in 'NS' for t in '123'}
RESOURCES['G1'] = {'kind': 'aggregate'}

def allowed(who: str, what: str, action: str = 'read',
            check_tenant: bool = True) -> bool:
    p, r = PRINCIPALS.get(who), RESOURCES.get(what)
    if p is None or r is None or not p['active']:
        return False                                  # deny by default
    if action == 'publish':
        return p['role'] == 'publisher' and r['kind'] == 'aggregate'
    if action != 'read':
        return False
    if r['kind'] == 'aggregate':
        return p['role'] == 'group'
    return (p['role'] == 'analyst' and p['division'] == r['division']
            and (r['tenant'] in p['tenants'] or not check_tenant))

# Written by hand from the policy statement, not generated from allowed().
EXPECTED_READS = {('ana', 'N1'), ('ana', 'N2'), ('sam', 'S1'), ('sam', 'S2'),
                  ('sam', 'S3'), ('gita', 'G1')}

def failures(**options) -> list[tuple[str, str]]:
    return [(p, r) for p in PRINCIPALS for r in RESOURCES
            if allowed(p, r, **options) != ((p, r) in EXPECTED_READS)]

print('read matrix failures:', failures())
print('publishers of G1:', [p for p in PRINCIPALS if allowed(p, 'G1', 'publish')])
print('unknown action allowed:', allowed('ana', 'N1', 'delete'))
print('division-only policy failures:', failures(check_tenant=False))
PRINCIPALS['sam']['active'] = False                    # access revoked
print('sam after revocation:', [r for r in RESOURCES if allowed('sam', r)])
