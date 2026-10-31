"""Fase 0.7 - Rollos y guías del film.

- Ejes de los rollos: tubo de aluminio de Ø25 que no gira. Se deja caer en las
  ranuras inclinadas de las placas y se sujeta en X con collarines por fuera.
- Mandriles impresos (2 por rollo) que entran en el núcleo de 3" y giran sobre
  el eje con un rodamiento 6005. Un collarín por mandril fija su posición; en el
  rollo de entrada ese collarín hace de freno, con un fieltro contra el mandril.
- Guías: tubos de Ø25 delante y detrás, atornillados a las placas (M6 en las
  testas). Sobre la trasera se enganchan segmentos impresos que forman la mesa de
  entrada hasta el rodillo de arrastre.
- La recogida se motorizará en la fase 1; aquí solo se reserva su volumen.
"""
import cadquery as cq

import params as P
from lib import FILM, PRINTED, PRINTED_ALT, RESERVED, ROLL, STEEL, box, rod_x

XL, XR = P.BEAM_X0, P.BEAM_X1
T = P.SIDE_PLATE_T
GR = P.REAR_GUIDE_D / 2
SHAFT_X = (XL - T - 16, XR + T + 16)
COLLAR_W, COLLAR_D = 12, 45
CHUCK_FLANGE_T = 6
ENTRY_SEGMENTS = 4
ENTRY_T = 3


def chuck(x_face=0.0, side=1):
    """Mandril. x_face: cara del núcleo; side=+1 si el núcleo queda hacia +X."""
    ins = (cq.Workplane("YZ").circle(P.CORE_ID / 2 - 0.3).extrude(P.CHUCK_INSERT)
           .faces(">X").chamfer(2))
    flange = cq.Workplane("YZ").circle(P.CHUCK_FLANGE_D / 2).extrude(-CHUCK_FLANGE_T)
    body = ins.union(flange)
    bo, bw = P.CHUCK_BEARING
    body = (body.cut(cq.Workplane("YZ").circle(P.ROLL_SHAFT_D / 2 + 1).extrude(100, both=True))
            .cut(cq.Workplane("YZ").circle(bo / 2).extrude(bw).translate((P.CHUCK_INSERT - bw, 0, 0))))
    # Aligerado: 6 ventanas en el cuerpo que entra en el núcleo
    for k in range(6):
        win = (cq.Workplane("YZ").circle(7).extrude(P.CHUCK_INSERT - bw - 4)
               .translate((2, 0, 25)).rotate((0, 0, 0), (1, 0, 0), k * 60))
        body = body.cut(win)
    if side < 0:
        body = body.mirror("YZ")
    return body.translate((x_face, 0, 0))


def collar(x0=0.0):
    """Collarín de apriete M4 (impreso)."""
    ring = (cq.Workplane("YZ").circle(COLLAR_D / 2).circle(P.ROLL_SHAFT_D / 2 + 0.2)
            .extrude(COLLAR_W))
    boss = box(0, COLLAR_W, -6, 6, COLLAR_D / 2 - 4, COLLAR_D / 2 + 6)
    body = ring.union(boss).cut(box(-1, COLLAR_W + 1, -1, 1, P.ROLL_SHAFT_D / 2, COLLAR_D / 2 + 7))
    body = body.cut(cq.Workplane("XZ").circle(2.2).extrude(20, both=True)
                    .translate((COLLAR_W / 2, 0, COLLAR_D / 2 + 1.5)))
    return body.translate((x0, 0, 0))


def entry_segment(x0=-P.FILM_WIDTH / 2, width=None):
    """Mesa de entrada: placa que se engancha a la guía trasera."""
    width = width or (P.PLATEN_X[1] - P.PLATEN_X[0]) / ENTRY_SEGMENTS - 2
    gy = P.REAR_GUIDE_Y
    y_end = P.GRIT_ROLLER_Y - P.GRIT_ROLLER_D / 2 - 3
    plate = box(x0, x0 + width, gy - 2, y_end, -ENTRY_T, 0)
    ring = (rod_x(x0, x0 + width, gy, -GR, 2 * GR + 7)
            .cut(rod_x(x0 - 1, x0 + width + 1, gy, -GR, 2 * GR + 0.4))
            .cut(box(x0 - 1, x0 + width + 1, gy - 30, gy - 6, -60, 10))   # boca del clip
            .cut(box(x0 - 1, x0 + width + 1, gy - 30, gy + 30, -ENTRY_T, 10)))
    body = plate.union(ring).cut(rod_x(x0 - 1, x0 + width + 1, gy, -GR, 2 * GR + 0.4))
    # Nervios bajo la placa
    for fx in (0.2, 0.5, 0.8):
        x = x0 + fx * width
        body = body.union(box(x - 1.5, x + 1.5, gy + GR + 2, y_end - 4, -ENTRY_T - 6, -ENTRY_T))
    return body


def printed_parts():
    return {"rollo_mandril": chuck(), "rollo_collarin": collar(),
            "mesa_entrada_segmento": entry_segment(0)}


def add(assy):
    fw = P.FILM_WIDTH
    gz = -GR
    assy.add(rod_x(XL, XR, P.REAR_GUIDE_Y, gz, P.REAR_GUIDE_D), name="guia_trasera", color=STEEL)
    assy.add(rod_x(XL, XR, P.FRONT_GUIDE_Y, gz, P.REAR_GUIDE_D), name="guia_delantera", color=STEEL)

    seg_w = (P.PLATEN_X[1] - P.PLATEN_X[0]) / ENTRY_SEGMENTS
    for k in range(ENTRY_SEGMENTS):
        assy.add(entry_segment(P.PLATEN_X[0] + k * seg_w + 1, seg_w - 2),
                 name=f"mesa_entrada_{k}", color=PRINTED_ALT)

    rolls = [("entrada", P.UNWIND_ROLL, P.FILM_ROLL_OD_MAX),
             ("recogida", P.TAKEUP_ROLL, P.FILM_CORE_OD + 10)]
    for name, (y, z), od in rolls:
        assy.add(rod_x(*SHAFT_X, y, z, P.ROLL_SHAFT_D), name=f"eje_rollo_{name}", color=STEEL)
        film = (rod_x(-fw / 2, fw / 2, y, z, od)
                .cut(rod_x(-fw / 2 - 1, fw / 2 + 1, y, z, P.FILM_CORE_OD)))
        core = (rod_x(-fw / 2, fw / 2, y, z, P.FILM_CORE_OD)
                .cut(rod_x(-fw / 2 - 1, fw / 2 + 1, y, z, P.CORE_ID)))
        assy.add(film, name=f"rollo_{name}", color=ROLL if name == "entrada" else FILM)
        assy.add(core, name=f"nucleo_{name}", color=PRINTED)
        for side, xf in ((1, -fw / 2), (-1, fw / 2)):
            assy.add(chuck(xf, side).translate((0, y, z)), name=f"mandril_{name}_{side:+d}",
                     color=PRINTED_ALT)
            cx = xf - side * (CHUCK_FLANGE_T + 1) - (COLLAR_W if side > 0 else 0)
            assy.add(collar(cx).translate((0, y, z)), name=f"collarin_{name}_{side:+d}", color=PRINTED)
        for k, cx in enumerate((XL - T - 1 - COLLAR_W, XR + T + 1)):
            assy.add(collar(cx).translate((0, y, z)), name=f"collarin_placa_{name}_{k}",
                     color=PRINTED)

    # Reserva: motor de recogida (fase 1), por dentro de la placa izquierda
    ty, tz = P.TAKEUP_ROLL
    assy.add(box(XL + P.PROFILE + 5, XL + P.PROFILE + 70, ty - 30, ty + 30,
                 tz + 45, tz + 95), name="reserva_motor_recogida", color=RESERVED)


def film_path():
    """Polilínea (Y, Z) del film desde el rollo de entrada al de recogida."""
    uy, uz = P.UNWIND_ROLL
    ty, tz = P.TAKEUP_ROLL
    return [
        (uy, uz + P.FILM_ROLL_OD_MAX / 2),
        (P.REAR_GUIDE_Y - GR, -GR),
        (P.REAR_GUIDE_Y, 0),
        (P.FRONT_GUIDE_Y, 0),
        (P.FRONT_GUIDE_Y + GR, -GR),
        (ty, tz + (P.FILM_CORE_OD + 10) / 2),
    ]


def plate_holes():
    """Agujeros que este módulo necesita en las placas laterales: (y, z, d)."""
    return [(P.FRONT_GUIDE_Y, -GR, P.M6_CLEAR)]
