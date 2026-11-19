# Aluminum cutting DXFs

- `LEFT-aluminum-plate-mm.dxf`: left half, extended eight-contact slot.
- `RIGHT-aluminum-plate-mm.dxf`: right half, original closed display slot, **already mirrored**.

Upload each file separately. Units are millimetres; do not mirror or scale either file on the vendor website. Aluminum alloy, thickness, finish, quantity, and cutting process are quote selections, not encoded by this 2D outline. Verify the physical 1:1 template and existing plate thickness before ordering.

These contain only LINE, ARC and CIRCLE cuts, with no frames, labels or repeated drill outlines. Both remove the large reset hole, the two marked small holes and the side USB recess. Top USB notches remain. Five circular mounting holes remain per half. The additional footprint drill marker from the plotting defaults was omitted (`--drill-shape-opt 0`) to avoid overlapping cuts at the already-defined mounting hole.

The original native RHS/source DXF elsewhere in the repository remains in the common left-shaped editing orientation. Use the files in this directory for quoting. The PDF right page matches this finished orientation.

`validation.json` records entity counts, cut lengths, and inverse-reflection checks. Reflection preserves arc radius and reverses/swaps arc angles to retain the same cut geometry. `tools/make_cutting_dxfs.py` rebuilds these exports after the native Edge.Cuts plots are exported in millimetres with drill shapes off. Preview: `assets/cutting-dxf-orientation.png`.

## SendCutSend import check

On 2026-11-18, both complete DXF exports imported into SendCutSend at 137.45 × 94.324 mm. A minimal ENTITIES-only export had been rejected, so the current files preserve KiCad's complete DXF tables, layers, handles and subclass records. Geometry, radii, units and handedness are unchanged.

The owner measured the existing plate at 1.14 mm. A comparison quote for one of each in 5052 H32 aluminum at 0.040 in (1.016 mm), no finish/coating: LEFT $14.24, RIGHT $14.48; subtotal $28.72; shipping/handling $5.00; displayed total $33.72 before any tax calculation. This stock is approximately 0.124 mm thinner than the measured plate. No order placed. Prices are time-specific and not a guaranteed final checkout amount.

Black finish is required by the owner. The earlier unfinished SendCutSend comparison quote does not meet that requirement and predates reset-hole removal. SendCutSend lists anodizing from 0.063 in (1.6 mm), not 1.2 mm: https://sendcutsend.com/services/anodizing/ . Do not order the old cart as a black-finished part.
