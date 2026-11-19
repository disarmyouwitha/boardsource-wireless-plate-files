"""Export each revised plate as a 1.2 mm STEP solid using KiCad CLI."""
import argparse
import re
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from extend_lhs_header import ROOT, coord, points
from kicad_sexpr import kind, nodes


def make_profile(source, mirror):
    entries = [node for _, _, node in nodes(source.read_text())]
    outline = [node for node in entries if '(layer "Edge.Cuts")' in node]
    assert sum(kind(node) == 'gr_circle' for node in outline) == 5
    assert all(kind(node) in {'gr_arc', 'gr_line', 'gr_circle'} for node in outline)
    if mirror:
        # Reflection about x=0 matches the right-hand DXF. Reflecting the
        # midpoint along with both ends preserves each arc's sweep.
        for index, node in enumerate(outline):
            for label, (x, y) in points(node).items():
                node = coord(node, label, (-x, y))
            outline[index] = node
    version, layers = [node for node in entries if kind(node) in {'version', 'layers'}]
    # KiCad's default stackup reserves 0.09 mm for copper and solder mask.
    # Compensate in the temporary profile to export a 1.2 mm bare solid.
    return '\n'.join(['(kicad_pcb', version, '(generator "pcbnew")',
                      '(general (thickness 1.29))', layers, *outline, ')', ''])


def verify(file):
    step = file.read_text()
    assert len(re.findall(r'=\s*MANIFOLD_SOLID_BREP\s*\(', step)) == 1, file
    assert len(re.findall(r'=\s*CLOSED_SHELL\s*\(', step)) == 1, file
    coords = {number: tuple(map(float, xyz.split(',')))
              for number, xyz in re.findall(
                  r"#(\d+)\s*=\s*CARTESIAN_POINT\s*\('[^']*',\s*\(([^()]*)\)\)", step)}
    vertices = [coords[number] for number in re.findall(
        r"=\s*VERTEX_POINT\s*\('[^']*',\s*#(\d+)\)", step)]
    assert vertices, file
    z_planes = sorted({round(vertex[2], 6) for vertex in vertices})
    assert len(z_planes) == 2 and abs(z_planes[1] - z_planes[0] - 1.2) < 1e-6, z_planes
    print(f'{file.name}: one closed solid, 1.2 mm thick, {len(vertices)} vertices')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kicad-cli', default='kicad-cli')
    args = parser.parse_args()
    output = ROOT / 'fabrication/step'
    output.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory() as scratch:
        for side, source in [('LEFT', 'ble_plate_scr_lhs_8pin'),
                             ('RIGHT', 'ble_plate_scr_rhs_no_side_usb')]:
            profile = Path(scratch) / f'{side}-plate.kicad_pcb'
            profile.write_text(make_profile(ROOT / 'Kicad' / f'{source}.kicad_pcb', side == 'RIGHT'))
            step = output / f'{side}-aluminum-plate-1p2mm.step'
            subprocess.run([args.kicad_cli, 'pcb', 'export', 'step', '--force',
                            '--board-only', '--output', str(step), str(profile)], check=True)
            verify(step)


if __name__ == '__main__':
    main()
