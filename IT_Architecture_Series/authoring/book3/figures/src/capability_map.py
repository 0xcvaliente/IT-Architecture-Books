"""Helios capability map with a heat map: importance, effectiveness and confidence."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from svgkit import ACCENT, ACCENT_SURFACE, MUTED, SURFACE, Svg

# (domain, [(capability, importance, effectiveness 1-5, confidence)])
MAP = [
    ('Customer\nmanagement', [('Customer identity\nresolution', 'High', 2, 'Medium'),
                              ('Customer contact\nmanagement', 'Medium', 3, 'High'),
                              ('Account\nmanagement', 'Medium', 4, 'High')]),
    ('Service\nmanagement', [('Service request\nintake', 'High', 2, 'Low'),
                             ('Entitlement\nchecking', 'High', 2, 'Medium'),
                             ('Case\ncoordination', 'High', 2, 'Medium')]),
    ('Fulfilment', [('Technician\nscheduling', 'High', 4, 'High'),
                    ('Field service\ndelivery', 'High', 4, 'High'),
                    ('Order\nallocation', 'Medium', 3, 'Medium'),
                    ('Subscription\nprovisioning', 'Medium', 4, 'Medium')]),
    ('Finance', [('Billing', 'High', 4, 'High'),
                 ('Financial\nreconciliation', 'Medium', 2, 'Medium')]),
    ('Enterprise\ninformation', [('Group\nreporting', 'High', 2, 'Medium'),
                                 ('Data quality\nmanagement', 'Medium', 1, 'Low')]),
]
W, H = 880, 560
CW, GAP, X0, CH, STEP = 166, 7, 10, 108, 118
s = Svg(W, H, 'Helios capability heat map',
        'Fourteen Helios capabilities in five domains, each showing importance, effectiveness '
        'on a five-point scale and confidence. Customer identity resolution, entitlement '
        'checking, case coordination and group reporting are priority candidates; service request intake and '
        'data quality management need measurement first because confidence is low.')
for i, (domain, caps) in enumerate(MAP):
    x = X0 + i * (CW + GAP)
    s.rect(x, 10, CW, 50, fill='#ffffff', stroke=MUTED, sw=2, rx=6)
    lines = domain.count('\n') + 1
    s.text(x + CW / 2, 40 - (lines - 1) * 9, domain, size=14, weight='bold', anchor='middle', lead=18)
    for j, (name, imp, eff, conf) in enumerate(caps):
        y = 72 + j * STEP
        priority = imp == 'High' and eff <= 2 and conf != 'Low'
        investigate = conf == 'Low'
        fill, stroke = (ACCENT_SURFACE, ACCENT) if priority else (SURFACE, MUTED)
        s.rect(x, y, CW, CH, fill=fill, stroke=stroke, sw=3 if priority else 2,
               dash='9 6' if investigate else None)
        s.text(x + 10, y + 22, name, size=14, weight='bold', lead=17)
        s.text(x + 10, y + 63, f'Importance: {imp}\nEffectiveness: {eff} of 5\n'
               f'Confidence: {conf.lower()}', size=13, fill=MUTED, lead=15)
LX, LY = X0 + 3 * (CW + GAP), 330
s.text(LX, LY, 'Key', size=14, weight='bold')
s.rect(LX, LY + 14, 40, 26, fill=ACCENT_SURFACE, stroke=ACCENT, sw=3, rx=4)
s.text(LX + 50, LY + 26, 'Priority candidate: importance high,\neffectiveness 2 or below and\nconfidence medium or high',
       size=13, fill=MUTED, lead=16)
s.rect(LX, LY + 82, 40, 26, fill=SURFACE, stroke=MUTED, sw=2, dash='9 6', rx=4)
s.text(LX + 50, LY + 94, 'Low confidence: measure\nbefore investing', size=13, fill=MUTED, lead=16)
s.rect(LX, LY + 134, 40, 26, fill=SURFACE, stroke=MUTED, sw=2, rx=4)
s.text(LX + 50, LY + 152, 'Other capabilities', size=13, fill=MUTED)
s.text(LX, LY + 196, 'Effectiveness: 1 = fails often,\n3 = adequate, 5 = strong and measured',
       size=13, fill=MUTED, lead=16)
s.save('capability_map')
