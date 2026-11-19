# Manufacturing options for the revised plates

Checked 2026-11-18. These are quoting options, not confirmed quotes or guarantees that every feature meets a selected process. Complete the physical 1:1 fit check first.

| Service | Route | Required preparation |
|---|---|---|
| [JLCPCB FR4 PCB fabrication](https://jlcpcb.com/pcb-fabrication/fr4-pcb) | Make the switch plates as unassembled FR4 PCB parts | Export dedicated Gerber/drill packages after fit approval and plate-thickness selection; current DXFs/PDF are not PCB order packages. |
| [SendCutSend G10/FR4](https://sendcutsend.com/materials/g10-fr4/) | Waterjet-cut G10/FR4 sheet; catalog includes nominal 1.6 mm stock | Upload the separate edge-only DXFs; use the already-oriented LEFT/RIGHT files in `fabrication/dxf/`. Confirm slot, switch-hole tolerances and material thickness in the quote. |
| [JLCCNC](https://jlccnc.com/) | CNC machining; service lists FR4 | Generate new STEP models for the revised plates at the chosen thickness. Original STEP files in this repo are outdated for this revision. |

SendCutSend accepts [DXF and other 2D vector files](https://sendcutsend.com/faq/what-file-type-format-can-i-send-you/). Its FR4 catalog lists waterjet tolerance +/-0.009 in (about 0.23 mm), so request confirmation that the switch openings/rounded slot end are suitable before selecting that route. The native plate switch holes are 14.05 mm nominal; service tolerance matters for switch fit.

JLCCNC's [ordering guide](https://jlccnc.com/help/article/how-to-place-cnc-orders) describes 3D CAD upload, with PDF/DWG/DXF as supplementary 2D drawings.

Plate thickness is a separate decision from the StenoSquid flash PCB's 1.6 mm fabrication choice. Measure the existing plate and verify switch clips/socket-stack clearance. The inherited README's 1.2 mm recommendation and native KiCad's 1.6 mm setting are not a newly verified thickness requirement.

Use `fabrication/dxf/LEFT-aluminum-plate-mm.dxf` and `fabrication/dxf/RIGHT-aluminum-plate-mm.dxf` for quoting. The right file is already mirrored, matching the PDF; do not mirror either file again. The older source DXFs in `Ble Plate Plots/` retain the common editing orientation. The PDF is for paper fit review, not a cutting order. No order placed through these services as part of this plate revision.

## Black anodized aluminum requirement

Owner measured existing plate at 1.14 mm and requires black aluminum. The original README recommended 1.2 mm; the native CAD thickness was 1.6 mm. DXF geometry is independent of thickness. 1.2 mm is 0.06 mm above the owner measurement; physical switch/socket fit still needs checking. SendCutSend lists black Type II anodizing starting at 0.063 in (1.6 mm), so its 0.040 in unfinished quote is unsuitable. [Anodizing specifications](https://sendcutsend.com/services/anodizing/). A custom supplier quote for 1.2 mm aluminum with black anodizing is needed to keep near the original thickness. Do not substitute 1.6 mm solely to obtain a finish without a stack/clip fit check.
