# Left screen plate: eight-contact opening

The original `ble_plate_scr` file represents a single plate. Preserve it for the right-hand fabrication/mirroring workflow. The new `ble_plate_scr_lhs_8pin.kicad_pcb` is the left-only variant, with a separate millimetre DXF. Both reset-button holes and all switch placements are retained.

The closed 14.50 × 3.08 mm header opening becomes an open-ended slot, matching the style in the owner's plate photograph. Its switch-facing end moves 4.086404 mm toward the switches, from x=169.582500 to x=165.496096. Its upper edge is y=85.490000 and lower edge y=88.570000. The upper lip meets the inner plate edge at x=187.616096, yielding a 22.12 mm envelope. The lower lip joins the original reset-side perimeter radius, so that lip is shorter than the upper lip. The closed end retains R0.5 corners. Clearance to the adjacent switch cutout is 2.613904 mm.

The width was inferred from the reference photo's geometry and the eight-contact requirement; the host header centres are not present in this plate source. A row of eight 2.54 mm contacts spans 17.78 mm centre-to-centre, but header housing size and exact registration must still be checked on the host. The actual-size SVG includes a 50 mm scale bar. Print at 100%, without fit-to-page. This is a mechanical draft, not a claim of measured host alignment.

The LHS variant also repairs three inherited outline endpoint gaps smaller than 0.025 mm and removes two remote, zero-length Edge.Cuts curves. Existing copper fills were refilled after the mechanical revision. The original file is byte-identical to the starting revision.

KiCad native DRC: no errors or malformed-outline violations after these repairs. Four warnings remain: two isolated unconnected copper pours, the unavailable `bs_custom_kicad` mounting-hole library, and a nonmirrored back reference label. The edge-only DXF excludes copper, library references, and text. The source plate had an invalid-outline error before this edit. No design-rule checks were disabled for this work.

Rebuild the native draft with `python3 tools/extend_lhs_header.py`, then refill zones before saving/exporting. Render the preview with `python3 tools/make_lhs_preview.py` (Pillow required). The 1:1 check sheet approximates arcs with fine polylines; use the native KiCad/DXF, which retain real arcs, for fabrication. Existing STEP files have not been regenerated for the LHS variant.
