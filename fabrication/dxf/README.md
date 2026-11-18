# Aluminum cutting DXFs

- `LEFT-aluminum-plate-mm.dxf`: left half, extended eight-contact slot.
- `RIGHT-aluminum-plate-mm.dxf`: right half, original closed display slot, **already mirrored**.

Upload each file separately. Units are millimetres; do not mirror or scale either file on the vendor website. Aluminum alloy, thickness, finish, quantity, and cutting process are quote selections, not encoded by this 2D outline. Verify the physical 1:1 template and existing plate thickness before ordering.

These contain only LINE, ARC and CIRCLE cuts, with no frames, labels or repeated drill outlines. Both keep the large reset hole and remove the two marked small holes and the side USB recess. Top USB notches remain. Six circular holes remain per half. The additional footprint drill marker from the plotting defaults was omitted (`--drill-shape-opt 0`) to avoid overlapping cuts at the already-defined mounting hole.

The original native RHS/source DXF elsewhere in the repository remains in the common left-shaped editing orientation. Use the files in this directory for quoting. The PDF right page matches this finished orientation.

`validation.json` records entity counts, cut lengths, and inverse-reflection checks. Reflection preserves arc radius and reverses/swaps arc angles to retain the same cut geometry. `tools/make_cutting_dxfs.py` rebuilds these exports after the native Edge.Cuts plots are exported in millimetres with drill shapes off. Preview: `assets/cutting-dxf-orientation.png`.
