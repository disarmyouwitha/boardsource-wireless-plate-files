"""Actual-size US Letter review sheets; does not modify CAD or DXF files."""
from pathlib import Path
import ast
import math
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import letter
from pypdf import PdfReader
from extend_lhs_header import ROOT, points, circle
from kicad_sexpr import nodes, kind

# Reuse the reviewed outline sampler without the preview module's side effects.
module = ast.parse((ROOT/'tools/make_lhs_preview.py').read_text())
exec(compile(ast.Module(body=[n for n in module.body if isinstance(n,ast.FunctionDef)
                             and n.name in ('shapes','loops')],type_ignores=[]),
             'outline_helpers','exec'))

out=ROOT/'output/pdf';out.mkdir(parents=True,exist_ok=True)
file=out/'ble-plates-1to1-fit-check.pdf'
c=canvas.Canvas(str(file),pagesize=letter)
c.setTitle('BLE plate fit check - actual size - left and right')
c.setAuthor('StenoSquid PCB project')
W,H=letter


def text(x,y,s,size=10):
    c.setFont('Helvetica',size);c.setFillColorRGB(.10,.16,.21)
    c.drawString(x*mm,H-y*mm,s)


for page,(side,name,mirrored) in enumerate([
    ('LEFT','ble_plate_scr_lhs_8pin',False),
    ('RIGHT','ble_plate_scr_rhs_no_side_usb',True)],1):
    text(18,21,f'{side} PLATE - 1:1 FIT CHECK',17)
    text(18,30,'Print ACTUAL SIZE / 100%. Disable Fit, Shrink and scaling.',10)
    text(18,37,'US Letter (8.5 x 11 in). Check the rulers before comparing the hardware.',9)
    text(18,47,'Current draft: side USB recess filled; marked small holes and reset holes removed.',9)
    text(18,54,'Top USB notch retained. '+
         ('Eight-contact open slot.' if not mirrored else 'Original closed display slot.'),9)
    ss=shapes(ROOT/'Kicad'/f'{name}.kicad_pcb')
    polys=loops(ss)
    expected=28 if mirrored else 27  # RHS also has a closed display slot.
    assert len(polys)==expected, f'{side}: unexpected closed-contour count {len(polys)}'
    xmin=min(p[0] for ps in ss for p in ps);xmax=max(p[0] for ps in ss for p in ps)
    ymin=min(p[1] for ps in ss for p in ps);ymax=max(p[1] for ps in ss for p in ps)
    # Only translate/mirror native millimetres. Never scale to the page bounds.
    xoff=(W/mm-(xmax-xmin))/2; yoff=72
    def xy(p):
        x=xmax-p[0] if mirrored else p[0]-xmin
        return (xoff+x)*mm,H-(yoff+p[1]-ymin)*mm
    c.setStrokeColorRGB(1,0,0);c.setLineWidth(.18*mm)
    for ps in ss:
        path=c.beginPath();path.moveTo(*xy(ps[0]))
        for p in ps[1:]:path.lineTo(*xy(p))
        c.drawPath(path)
    text(18,180,'Trace the red outline. The right page is already mirrored into its final orientation.',9)
    text(18,187,'Check: header/socket access, switch clearance and mounting alignment.',9)
    c.setStrokeColorRGB(0,0,0);c.setLineWidth(.2*mm)
    y=H-207*mm;c.line(18*mm,y,118*mm,y)
    for i in range(11):
        x=(18+i*10)*mm;tick=(2.5 if i%5==0 else 1.5)*mm
        c.line(x,y-tick,x,y+tick)
    text(18,218,'This bar MUST measure 100 mm end to end.',10)
    c.rect(160*mm,H-(197+25.4)*mm,25.4*mm,25.4*mm)
    text(155,229,'25.4 mm / 1 in square',8)
    text(18,242,'Notes / measured discrepancies:',10)
    c.setStrokeColorRGB(.7,.7,.7)
    for y in (251,260):c.line(18*mm,H-y*mm,197*mm,H-y*mm)
    text(18,271,f'2026-11-18 draft | Mechanical fit review, not fabrication approval | Page {page}/2',8)
    c.showPage()
c.save()
r=PdfReader(file)
assert len(r.pages)==2
assert all(float(p.mediabox.width)==612 and float(p.mediabox.height)==792 for p in r.pages)
print(file)
