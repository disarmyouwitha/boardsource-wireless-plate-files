"""Fill the side USB recess in the LHS draft and a separate RHS source."""
import re
from extend_lhs_header import ROOT, points, coord, shape
from kicad_sexpr import nodes, kind

SIDE_IDS = {
    'f3a9782f-4557-4a55-86db-81dedbb8d66b',
    '639c0e59-e95c-4114-bccd-2e7277505454',
    '0a834a20-a08a-4667-adcf-dc41ef8fe21a',
    'd3c11c8f-a73d-4211-934b-a6da255728ad',
    'c8c79177-94d4-43e2-a654-f0a5554fbb68',
    'a15a7506-eae4-4933-84da-9ad754258706',
    'bc77e35b-31cb-4e19-bcaa-39f2d5b0ed72',
    'c91c4ad9-278a-4c52-a162-c4f8b5291bc4',
    'fe96060c-63d4-46e0-a0e3-515fe6bde1cc',
    '280e303b-6cb0-4a63-ad86-38ea386bc34f',
    'c53d867d-f307-4731-893a-4d66b9a43dc0',
    '4a316f85-e8c6-40b1-bcd4-f1cb60471700',
    'e21aa84b-970e-47cf-b64f-3b55ee0e1b51',
    'bead5d8b-2710-444a-94af-19f10c3f14a7',
    '40976bf0-19de-460f-ad64-224d4f51e16b',
}

UNUSED_HOLES = {
    '9340c285-5767-42d5-8b6d-63fe2a40ddf3',  # Ø2.4 below header slot
    '2d6db888-4e40-41c8-b701-07170fc894bc',  # Ø2.4 beside reset hole
    '0315dc9c-883e-4454-b7e1-3fa88875eafe',  # Ø4.2 reset access; owner removed
}


def remove_unused_holes(file):
    text = file.read_text()
    holes = [n for _, _, n in nodes(text) if kind(n) == 'gr_circle']
    removed = [n for n in holes if any(uid in n for uid in UNUSED_HOLES)]
    assert len(removed) == 3
    for node in removed: text = text.replace(node, '')
    assert all(n in text for n in holes if n not in removed)
    assert '0315dc9c-883e-4454-b7e1-3fa88875eafe' not in text
    file.write_text(text)
    print(file.name, ': two marked Ø2.4 holes and Ø4.2 reset hole removed.')


def revise(source, target, lhs):
    old = source.read_text()
    if 'c91c4ad9-278a-4c52-a162-c4f8b5291bc4' not in old:
        raise SystemExit('Side recess absent; rebuild LHS first before rerunning.')
    changes = []
    circles = []
    for start, end, node in nodes(old):
        if kind(node) == 'gr_circle': circles.append(node)
        uid = re.search(r'\(uuid "([^"]+)"\)', node)
        if not uid: continue
        new = node
        if uid[1] in SIDE_IDS: new = ''
        elif not lhs and uid[1] == 'b88717bd-086f-46cd-9d3f-0396009d0996':
            new = coord(node, 'start', (187.616096, 101.197891))
        elif lhs and kind(node) == 'gr_line':
            ps = points(node)
            if all(abs(p[1]-88.57)<.000002 for p in ps.values()):
                label=max(ps,key=lambda k:ps[k][0])
                new=coord(node,label,(187.616096,88.57))
        if new != node: changes.append((start,end,new))
    result=old
    for start,end,new in reversed(changes): result=result[:start]+new+result[end:]
    if lhs:
        extra=shape('gr_line',start=(187.616096,88.57),end=(187.616096,101.197891))
        result=result.rstrip()[:-1]+'\n'+extra+'\n)\n'
    else:
        for _,_,n in nodes(result):
            if kind(n)=='gr_curve' and '(layer "Edge.Cuts")' in n:
                result=result.replace(n,'')
    assert all(n in result for n in circles), 'A mounting/reset hole changed'
    target.write_text(result)
    print(target.name, ': side USB recess filled; all circular holes retained.')


if __name__ == '__main__':
    lhs=ROOT/'Kicad/ble_plate_scr_lhs_8pin.kicad_pcb'
    revise(lhs,lhs,True)
    revise(ROOT/'Kicad/ble_plate_scr.kicad_pcb',
           ROOT/'Kicad/ble_plate_scr_rhs_no_side_usb.kicad_pcb',False)
    for file in [lhs, ROOT/'Kicad/ble_plate_scr_rhs_no_side_usb.kicad_pcb']:
        remove_unused_holes(file)
