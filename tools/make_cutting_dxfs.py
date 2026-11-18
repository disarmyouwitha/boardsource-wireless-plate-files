"""Write simple millimetre cutting DXFs; mirror RHS once, in the file itself."""
from pathlib import Path
from collections import Counter
import json
import math
from PIL import Image, ImageDraw, ImageFont
from extend_lhs_header import ROOT


def read(file):
    lines=file.read_text().splitlines()
    pairs=[(int(c),v.strip()) for c,v in zip(lines[::2],lines[1::2])]
    result=[]; inside=False; entity=None
    for i,(code,value) in enumerate(pairs):
        if code==2 and value=='ENTITIES': inside=True;continue
        if not inside:continue
        if code==0:
            if entity:result.append(entity)
            if value=='ENDSEC':break
            assert value in ('LINE','ARC','CIRCLE'),value
            entity={'type':value}
        elif entity is not None and code in (10,20,11,21,40,50,51):
            entity[code]=float(value)
    return result


def sample(e):
    if e['type']=='LINE':return [(e[10],e[20]),(e[11],e[21])]
    start=e.get(50,0);span=(e[51]-start)%360 if e['type']=='ARC' else 360
    return [(e[10]+e[40]*math.cos(math.radians(start+span*i/256)),
             e[20]+e[40]*math.sin(math.radians(start+span*i/256))) for i in range(257)]


def mirror(e,axis):
    e=e.copy();e[10]=axis-e[10]
    if e['type']=='LINE':e[11]=axis-e[11]
    elif e['type']=='ARC':e[50],e[51]=(180-e[51])%360,(180-e[50])%360
    return e


def length(e):
    if e['type']=='LINE':return math.hypot(e[11]-e[10],e[21]-e[20])
    return e[40]*math.radians((e[51]-e[50])%360 if e['type']=='ARC' else 360)


def write(file,es,template):
    # Keep KiCad's complete tables, layers, handles and DXF subclass records.
    # Some quote importers reject a bare ENTITIES-only DXF even when its
    # primitives can be read by CAD tools.
    lines=template.read_text().splitlines()
    pairs=[(int(c),v) for c,v in zip(lines[::2],lines[1::2])]
    inside=False;index=-1;output=[]
    for code,value in pairs:
        if code==2 and value.strip()=='ENTITIES':inside=True
        elif inside and code==0:
            if value.strip()=='ENDSEC':inside=False
            else:
                index+=1
                assert value.strip()==es[index]['type']
        elif inside and index>=0 and code in es[index]:
            value=f'{es[index][code]:.9f}'
        output.append((code,value))
    assert index==len(es)-1
    file.write_text(''.join(f'{k:3d}\n{v}\n' for k,v in output))


out=ROOT/'fabrication/dxf';out.mkdir(parents=True,exist_ok=True)
report={};preview=[]
for side,name,flip in [('LEFT','ble_plate_screen_lhs_8pin',False),
                       ('RIGHT','ble_plate_screen_rhs_no_side_usb',True)]:
    template=ROOT/'Ble Plate Plots'/f'{name}.dxf'
    source=read(template)
    assert sum(e['type']=='CIRCLE' for e in source)==6, 'Unexpected drilling circles'
    # Reflection about x=0 is sufficient: only handedness changes, never scale.
    target=[mirror(e,0) if flip else e.copy() for e in source]
    file=out/f'{side}-aluminum-plate-mm.dxf';write(file,target,template)
    actual=read(file)
    assert len(actual)==len(source)
    assert math.isclose(sum(map(length,source)),sum(map(length,actual)),abs_tol=1e-6)
    for original,result in zip(source,actual):
        restored=mirror(result,0) if flip else result
        for k,v in original.items():
            if k=='type': assert restored[k]==v
            elif k in (50,51): assert abs((restored[k]-v+180)%360-180)<1e-6
            else:assert math.isclose(restored[k],v,abs_tol=1e-6)
    assert len({tuple(sorted((str(k),v) for k,v in e.items())) for e in actual})==len(actual)
    report[side]={'file':file.name,'units':'mm','mirrored':flip,
                  'counts':dict(Counter(e['type'] for e in actual)),
                  'cut_length_mm':sum(map(length,actual)),
                  'verified':'round-trip reflection and lengths match source within 0.000001 mm'}
    preview.append((side,actual))
(out/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
im=Image.new('RGB',(1700,750),'white');d=ImageDraw.Draw(im)
font=lambda n:ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',n)
d.text((35,20),'Fabrication DXFs: LEFT and RIGHT already oriented',fill='#172b42',font=font(30))
d.text((35,65),'Millimetres. Upload one file per part. Do not mirror or rescale on the quoting website.',fill='#435366',font=font(21))
for i,(side,es) in enumerate(preview):
    ps=[p for e in es for p in sample(e)]
    xmin=min(p[0] for p in ps); ymax=max(p[1] for p in ps)
    def xy(p):return 35+i*850+(p[0]-xmin)*5.5,155+(ymax-p[1])*5.5
    d.text((35+i*850,112),side,fill='#172b42',font=font(24))
    for e in es:d.line([xy(p) for p in sample(e)],fill='#e02020',width=2)
im.save(ROOT/'assets/cutting-dxf-orientation.png')
print(json.dumps(report,indent=2))
