"""Extend only the left screen plate slot; preserve unrelated native objects."""
from pathlib import Path
import math
import re
import uuid
from kicad_sexpr import nodes, kind

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'Kicad/ble_plate_scr.kicad_pcb'
FILE = ROOT / 'Kicad/ble_plate_scr_lhs_8pin.kicad_pcb'


def points(node):
    return {k: (float(x), float(y)) for k, x, y in
            re.findall(r'\((start|mid|end|center) ([-\d.]+) ([-\d.]+)\)', node)}


def circle(a, b, c):
    ax, ay = a; bx, by = b; cx, cy = c
    d = 2 * (ax*(by-cy) + bx*(cy-ay) + cx*(ay-by))
    x = ((ax*ax+ay*ay)*(by-cy)+(bx*bx+by*by)*(cy-ay)+(cx*cx+cy*cy)*(ay-by))/d
    y = ((ax*ax+ay*ay)*(cx-bx)+(bx*bx+by*by)*(ax-cx)+(cx*cx+cy*cy)*(bx-ax))/d
    return (x, y), math.dist((x, y), a)


def coord(node, key, p):
    return re.sub(r'\('+key+r' [-\d.]+ [-\d.]+\)',
                  f'({key} {p[0]:.6f} {p[1]:.6f})', node)


def shape(typ, **ps):
    text = '(' + typ + '\n'
    text += ''.join(f'\t({k} {p[0]:.6f} {p[1]:.6f})\n' for k, p in ps.items())
    return text + '\t(stroke (width 0.1) (type default))\n\t(layer "Edge.Cuts")\n\t(uuid "'+str(uuid.uuid4())+'")\n)'


def main():
    old = SOURCE.read_text()
    if '9550fd03-3ac4-4a0e-967e-3337905513e0' not in old:
        raise SystemExit('Original LHS slot absent; refusing to apply twice.')
    slot = {'9550fd03-3ac4-4a0e-967e-3337905513e0',
            '08a7c925-7fae-4530-b0c9-120e185cb318',
            'ee27d19c-8dca-4ac8-a760-6dfd54d28071',
            '7edc9030-db7b-43ac-a1b3-b87eeacb4c2d',
            '03312988-54f1-4396-b668-b499b9254ef6',
            '5528bcad-2950-4673-90eb-c37e6952c475',
            'e38b5d6a-dde4-4f60-8079-f7f6e36b49df',
            'd1c0da87-8627-405b-a7e6-6e5875177125'}
    arc_id = 'bc77e35b-31cb-4e19-bcaa-39f2d5b0ed72'
    edge_id = 'b88717bd-086f-46cd-9d3f-0396009d0996'
    bridge_id = 'bead5d8b-2710-444a-94af-19f10c3f14a7'
    entries = list(nodes(old))
    arc = next(n for _, _, n in entries if arc_id in n)
    p = points(arc)
    center, radius = circle(p['start'], p['mid'], p['end'])
    top, bottom, outer, width, r = 85.49, 88.57, 187.616096, 22.12, .5
    left = outer - width
    # The new opening merges into the existing rounded reset-side perimeter.
    hit = (center[0]-math.sqrt(radius**2-(bottom-center[1])**2), bottom)
    a = math.atan2(p['start'][1]-center[1], p['start'][0]-center[0])
    b = math.atan2(hit[1]-center[1], hit[0]-center[0])
    delta = (b-a+math.pi) % (2*math.pi) - math.pi
    mid = (center[0]+radius*math.cos(a+delta/2), center[1]+radius*math.sin(a+delta/2))
    replacements = []
    changed = []
    for start, end, node in entries:
        uid = re.search(r'\(uuid "([^"]+)"\)', node)
        if not uid: continue
        uid = uid[1]
        new = node
        if uid in slot or uid == bridge_id: new = ''
        elif uid == arc_id: new = coord(coord(node, 'mid', mid), 'end', hit)
        elif uid == edge_id: new = coord(node, 'start', (outer, top))
        if node != new:
            changed.append(uid); replacements.append((start, end, new))
    assert len(changed) == 11, changed
    result = old
    for start, end, new in reversed(replacements): result = result[:start]+new+result[end:]
    q = r / math.sqrt(2)
    extra = [shape('gr_line', start=(left+r, top), end=(outer, top)),
             shape('gr_arc', start=(left, top+r), mid=(left+r-q, top+r-q), end=(left+r, top)),
             shape('gr_line', start=(left, top+r), end=(left, bottom-r)),
             shape('gr_arc', start=(left+r, bottom), mid=(left+r-q, bottom-r+q), end=(left, bottom-r)),
             shape('gr_line', start=hit, end=(left+r, bottom))]
    result = result.rstrip()[:-1] + '\n' + '\n'.join(extra) + '\n)\n'
    # The source represents ONE plate, mirrored for the RHS when fabricated.
    # Keep that source intact for the RHS; write a separate LHS variant.
    # Remove inherited zero-length Edge.Cuts curves far outside the plate.
    for _, _, node in entries:
        if kind(node) == 'gr_curve' and '(layer "Edge.Cuts")' in node:
            ps = re.findall(r'\(xy ([-\d.]+) ([-\d.]+)\)', node)
            assert len(set(ps)) == 1
            result = result.replace(node, '')
        elif not any(uid in node for uid in changed):
            assert node in result
    # Imported reset-perimeter endpoints have gaps up to 0.020 mm. Snap only
    # straight segment ends to their adjacent arc ends; retain the arc radii.
    edge_nodes = [n for _, _, n in nodes(result) if
                  kind(n) in ('gr_line', 'gr_arc') and '(layer "Edge.Cuts")' in n]
    repairs = 0
    for node in edge_nodes:
        if kind(node) != 'gr_line': continue
        fixed = node
        for label, pt in points(node).items():
            candidates = [q for other in edge_nodes if other != node
                          for k, q in points(other).items() if k in ('start', 'end')]
            near = min(candidates, key=lambda q: math.dist(pt, q))
            gap = math.dist(pt, near)
            if .000002 < gap < .025:
                fixed = coord(fixed, label, near); repairs += 1
        result = result.replace(node, fixed)
    FILE.write_text(result)
    print(f'LHS slot: {width:.2f} mm to inner edge x={outer}, height={bottom-top:.2f} mm; R{r}.')
    print(f'Left end moved {169.5825-left:.6f} mm toward keys. Original/RHS source unchanged.')
    print(f'Repaired {repairs} inherited sub-0.025 mm outline gaps in the LHS variant.')


if __name__ == '__main__': main()
