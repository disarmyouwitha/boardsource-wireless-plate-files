"""Render the native Edge.Cuts geometry and an actual-size LHS check sheet."""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont
from extend_lhs_header import points, circle
from kicad_sexpr import nodes, kind

ROOT = Path(__file__).resolve().parents[1]


def shapes(file):
    result = []
    for _, _, n in nodes(file.read_text()):
        if '(layer "Edge.Cuts")' not in n: continue
        k = kind(n); p = points(n)
        if k == 'gr_line': ps = [p['start'], p['end']]
        elif k == 'gr_arc':
            c, r = circle(p['start'], p['mid'], p['end'])
            a, m, z = [math.atan2(p[t][1]-c[1], p[t][0]-c[0]) for t in ('start','mid','end')]
            span = (z-a) % (2*math.pi)
            if (m-a) % (2*math.pi) > span: span -= 2*math.pi
            ps = [(c[0]+r*math.cos(a+span*i/64), c[1]+r*math.sin(a+span*i/64)) for i in range(65)]
        elif k == 'gr_circle':
            c = p['center']; r = math.dist(c, p['end'])
            ps = [(c[0]+r*math.cos(i*2*math.pi/128),c[1]+r*math.sin(i*2*math.pi/128)) for i in range(129)]
        else: continue
        result.append(ps)
    return result


def loops(ss):
    ss = [p[:] for p in ss]; result=[]
    while ss:
        chain=ss.pop()
        while math.dist(chain[0], chain[-1]) > .03:
            nearest=min(((math.dist(chain[-1],p[end]),i,end) for i,p in enumerate(ss) for end in (0,-1)))
            gap,i,end=nearest
            assert gap < .03, (gap,chain[-1])
            p=ss.pop(i)
            chain.extend(p if end==0 else p[::-1])
        result.append(chain)
    return sorted(result,key=lambda p:abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]))),reverse=True)


old=shapes(ROOT/'Kicad/ble_plate_scr.kicad_pcb')
new=shapes(ROOT/'Kicad/ble_plate_scr_lhs_8pin.kicad_pcb')
im=Image.new('RGB',(1800,1020),'#f5f6f8'); d=ImageDraw.Draw(im)
font=lambda size:ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',size)
d.text((45,25),'BLE screen plate — left-hand 8-contact opening',font=font(34),fill='#172b42')
d.text((45,78),'Side USB recess filled on both halves; reset holes removed. Red marks the left header slot.',font=font(22),fill='#435366')
for label,ss,offset in [('Original left',old,60),('Revised left',new,930)]:
    d.text((offset,140),label,font=font(28),fill='#172b42')
    xy=lambda p:(offset+(p[0]-50.166096)*5.5,210+(p[1]-38.019142)*5.5)
    for i,poly in enumerate(loops(ss)):
        d.polygon([xy(p) for p in poly],fill='#263943' if i==0 else '#f5f6f8')
    if ss is new:
        for ps in ss:
            if all(165<p[0]<188 and 85.48<=p[1]<=88.80 for p in ps):
                d.line([xy(p) for p in ps],fill='#ff2020',width=5)
    d.text((offset,780),'14.50 mm closed slot' if ss is old else '22.12 mm to inner edge / 3.08 mm high',font=font(23),fill='#172b42')
d.text((60,860),'Slot end extends 4.086 mm toward the switches; inner end opens into the existing edge.',font=font(24),fill='#172b42')
d.text((60,910),'Photo-matched opening: verify all eight physical header contacts with the 1:1 sheet before cutting.',font=font(23),fill='#435366')
out=ROOT/'assets';out.mkdir(exist_ok=True)
im.save(out/'ble-plate-lhs-8pin-comparison.png')
pair=Image.new('RGB',(1800,850),'#f5f6f8'); pd=ImageDraw.Draw(pair)
pd.text((50,25),'Revised pair — side USB recesses removed',font=font(34),fill='#172b42')
pd.text((50,80),'LEFT: eight-contact opening     /     RIGHT: original display slot     /     Reset holes removed',font=font(23),fill='#435366')
rhs=shapes(ROOT/'Kicad/ble_plate_scr_rhs_no_side_usb.kicad_pcb')
for ss,offset,mirror in [(new,60,False),(rhs,930,True)]:
    def xy(p):
        x=187.616096-p[0] if mirror else p[0]-50.166096
        return offset+x*5.5,190+(p[1]-38.019142)*5.5
    for i,poly in enumerate(loops(ss)):
        pd.polygon([xy(p) for p in poly],fill='#263943' if i==0 else '#f5f6f8')
pd.text((50,775),'Native/DXF sources retain the common orientation; mirror the RHS for the finished pair.',font=font(23),fill='#435366')
pair.save(out/'ble-plate-no-side-usb-pair.png')
paths=[]
for ps in new:
    xy=lambda p:(p[0]-40,p[1]-20)
    paths.append('<polyline points="'+' '.join(f'{xy(p)[0]:.6f},{xy(p)[1]:.6f}' for p in ps)+'"/>')
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="160mm" height="130mm" viewBox="0 0 160 130">
<rect width="160" height="130" fill="white"/>
<g fill="none" stroke="#ff0000" stroke-width="0.15">'''+''.join(paths)+'''</g>
<g font-family="sans-serif" font-size="3" fill="black">
<text x="10" y="8">LEFT ONLY — 8-contact slot — print at 100%, no fit-to-page</text>
<text x="10" y="13">22.12 mm to inner edge, 3.08 mm height; check on physical host.</text>
<text x="65" y="123">50 mm scale check</text></g>
<path d="M10 122 H60 M10 120 V124 M60 120 V124" stroke="black" stroke-width=".2"/>
</svg>'''
(out/'ble-plate-lhs-8pin-1to1.svg').write_text(svg)
print('Rendered comparison and 1:1 sheet; all outline chains closed within 0.03 mm.')
