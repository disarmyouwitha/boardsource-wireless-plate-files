# Left screen plate: eight-contact opening

The original `ble_plate_scr` file represents a single plate. It remains an unchanged baseline; the revised right-hand source is `ble_plate_scr_rhs_no_side_usb.kicad_pcb`, in the same common orientation for mirroring. The new `ble_plate_scr_lhs_8pin.kicad_pcb` is the left-only variant, with a separate millimetre DXF. All switch placements are retained. Reset access holes were subsequently removed at owner request.

The closed 14.50 × 3.08 mm header opening becomes an open-ended slot, matching the style in the owner's plate photograph. Its switch-facing end moves 4.086404 mm toward the switches, from x=169.582500 to x=165.496096. Its upper edge is y=85.490000 and lower edge y=88.570000. The upper lip meets the inner plate edge at x=187.616096, yielding a 22.12 mm envelope. The later side-USB revision extends both lips to the straight inner edge; both lips now end at x=187.616096. The closed end retains R0.5 corners. Clearance to the adjacent switch cutout is 2.613904 mm.

The width was inferred from the reference photo's geometry and the eight-contact requirement; the host header centres are not present in this plate source. A row of eight 2.54 mm contacts spans 17.78 mm centre-to-centre, but header housing size and exact registration must still be checked on the host. The actual-size SVG includes a 50 mm scale bar. Print at 100%, without fit-to-page. This is a mechanical draft, not a claim of measured host alignment.

The LHS variant also repairs three inherited outline endpoint gaps smaller than 0.025 mm and removes two remote, zero-length Edge.Cuts curves. Existing copper fills were refilled after the mechanical revision. The original file is byte-identical to the starting revision.

KiCad native DRC: no errors or malformed-outline violations after these repairs. Four warnings remain: two isolated unconnected copper pours, the unavailable `bs_custom_kicad` mounting-hole library, and a nonmirrored back reference label. The edge-only DXF excludes copper, library references, and text. The source plate had an invalid-outline error before this edit. No design-rule checks were disabled for this work.

Rebuild the native draft with `python3 tools/extend_lhs_header.py`, then run `python3 tools/close_side_usb.py` to fill the side USB recesses and build the RHS variant, and refill zones before saving/exporting. Render the preview with `python3 tools/make_lhs_preview.py` (Pillow required). The 1:1 check sheet approximates arcs with fine polylines; use the native KiCad/DXF, which retain real arcs, for fabrication. Build the revised 1.2 mm STEP pair with `python3 tools/make_plate_steps.py`. The right STEP is exported in its final handedness.

## Side USB revision

At the owner’s request the side USB recess, between the header slot and reset hole, is filled on both new variants. The inner perimeter follows x=187.616096 through the former recess. The larger reset circles were initially retained and later removed at owner request. The subsequent marked-hole revision removes two small circles per half, as detailed below. The LHS keeps the 22.12 × 3.08 mm opening; the RHS keeps the original closed 14.50 × 3.08 mm slot. Top USB notches remain. RHS output uses the common source orientation, matching the original file: mirror for right-hand fabrication. Both updated native files have zero DRC errors and the same four warnings recorded above. Separate DXFs are exported in millimetres.

## Marked-hole revision and print sheet

The owner marked two small holes on each half for removal. Removed the Ø2.4 mm circles at source centres (168.619192, 94.285564) and (183.051192, 102.806564). The Ø4.2 mm reset hole at (178.9825, 101.855) was subsequently removed; the five other circular mounting holes remain. These coordinates use the common, unmirrored source frame. No other geometry changed in this revision.

The [print-ready US Letter PDF](../output/pdf/ble-plates-1to1-fit-check.pdf) reflects this current state. It has one half per page, with the right half already mirrored, a 100 mm ruler, and a 25.4 mm square. Print at Actual Size / 100%, with no Fit or Shrink. Check physical header alignment before ordering. The [SVG](../assets/ble-plate-lhs-8pin-1to1.svg) remains a left-only alternative.

## Ready-oriented cutting exports

Use `fabrication/dxf/LEFT-aluminum-plate-mm.dxf` and `fabrication/dxf/RIGHT-aluminum-plate-mm.dxf` for vendor uploads. Unlike the common-orientation source DXFs described above, the RIGHT cutting file is already mirrored. Both exports omit the footprint drill marker to avoid an overlapping cut at an existing Edge.Cuts mounting circle. Geometry and dimensions are retained. The PDF already has this same final handedness.

## Reset access removed

Owner requested removal of the Ø4.2 mm reset-button access circle on both halves. Native files, both sets of DXFs, previews and the 1:1 PDF now omit it. Five circular mounting holes remain per half. The PDF and cutting files supersede the earlier uploads/cart that still had reset access holes. No slot, switch placement or perimeter dimensions changed.
