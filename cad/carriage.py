"""Fase 0.4 - Carro (impreso en 3D).

Tres piezas impresas:
- placa del carro: atornillada a los 4 patines MGN12H (M3)
- bandeja de cabezales: pieza en L atornillada a la placa con 4 M4 en colisos
  verticales, que dan el ajuste de altura cabezal-film (±HEAD_ADJUST)
- pinza de correa: detrás de la placa, por encima de la viga

Los cabezales XP600 son maquetas: las cotas de la pestaña y de los tornillos
hay que confirmarlas con un cabezal real antes de imprimir la bandeja.
"""
import cadquery as cq

import params as P
from lib import HEAD, PRINTED, RESERVED, STEEL, box, rod_y

YF = P.BEAM_Y_FRONT
PY0 = P.CARRIAGE_PLATE_Y                 # cara trasera de la placa (sobre los patines)
PY1 = PY0 + P.CARRIAGE_PLATE_T
PLATE_Z0 = P.SHELF_Z + 3
HALF_W = P.CARRIAGE_W / 2
SHELF_HALF_W = HALF_W - 10
FLANGE_T = 8
SHELF_TOP = P.SHELF_Z + P.SHELF_T
ADJ_SCREWS = [(dx, dz) for dx in (-60, 60) for dz in (P.SHELF_Z + 22, P.SHELF_Z + 47)]


def head_xs(cx=0.0):
    first = cx - (P.HEAD_COUNT - 1) * P.HEAD_PITCH_X / 2
    return [first + i * P.HEAD_PITCH_X for i in range(P.HEAD_COUNT)]


def blocks(cx=0.0):
    """Patines MGN12H con el hueco de la guía."""
    out = []
    for z in P.RAIL_Z:
        for dx in (-P.BLOCK_SPACING_X / 2, P.BLOCK_SPACING_X / 2):
            x = cx + dx
            b = box(x - P.BLOCK_L / 2, x + P.BLOCK_L / 2, YF + 3, PY0,
                    z - P.BLOCK_W / 2, z + P.BLOCK_W / 2)
            b = b.cut(box(x - P.BLOCK_L, x + P.BLOCK_L, YF, YF + P.RAIL_H + 0.5,
                          z - P.RAIL_W / 2 - 0.5, z + P.RAIL_W / 2 + 0.5))
            out.append(b)
    return out


def plate(cx=0.0):
    body = box(cx - HALF_W, cx + HALF_W, PY0, PY1, PLATE_Z0, P.CARRIAGE_TOP_Z)
    h = P.BLOCK_HOLES / 2
    for z in P.RAIL_Z:
        for dx in (-P.BLOCK_SPACING_X / 2, P.BLOCK_SPACING_X / 2):
            for ox in (-h, h):
                for oz in (-h, h):
                    body = body.cut(rod_y(PY0 - 1, PY1 + 1, cx + dx + ox, z + oz, 3.4))
    # Insertos térmicos M4 para la bandeja
    for dx, dz in ADJ_SCREWS:
        body = body.cut(rod_y(PY1 - 8, PY1 + 1, cx + dx, dz, 5.6))
    # Insertos M3 para la pinza de correa (desde atrás)
    for dx in (-20, 20):
        body = body.cut(rod_y(PY0 - 1, PY0 + 6, cx + dx, P.CARRIAGE_TOP_Z - 8, 4.2))
    return body


def shelf(cx=0.0):
    x0, x1 = cx - SHELF_HALF_W, cx + SHELF_HALF_W
    fy0, fy1 = PY1, PY1 + FLANGE_T
    flange = box(x0, x1, fy0, fy1, P.SHELF_Z, P.SHELF_Z + P.SHELF_FLANGE_H)
    tray = box(x0, x1, fy0, P.SHELF_FRONT_Y, P.SHELF_Z, SHELF_TOP)
    body = flange.union(tray)
    for x in (x0, x1 - 6):
        rib = (cq.Workplane("YZ")
               .polyline([(fy1, SHELF_TOP), (fy1, P.SHELF_Z + P.SHELF_FLANGE_H),
                          (P.SHELF_FRONT_Y - 20, SHELF_TOP)])
               .close().extrude(6).translate((x, 0, 0)))
        body = body.union(rib)

    hx, hy, _ = P.HEAD_SIZE
    fy = P.HEAD_FLANGE[1]
    for x in head_xs(cx):
        body = body.cut(box(x - hx / 2 - 0.5, x + hx / 2 + 0.5, -hy / 2 - 0.5, hy / 2 + 0.5,
                            P.SHELF_Z - 1, SHELF_TOP + 1))
        for y in (-fy / 2 + 3.5, fy / 2 - 3.5):
            body = body.cut(cq.Workplane("XY").circle(1.4).extrude(P.SHELF_T + 2)
                            .translate((x, y, P.SHELF_Z - 1)))   # M3 roscado o inserto
    # Colisos verticales M4 para el ajuste de altura
    for dx, dz in ADJ_SCREWS:
        slot = (cq.Workplane("XZ").slot2D(2 * P.HEAD_ADJUST + 4.5, 4.5, angle=90)
                .extrude(-(FLANGE_T + 2)).translate((cx + dx, fy0 - 1, dz)))
        body = body.cut(slot)
    return body


def belt_clamp(cx=0.0):
    y0, y1 = P.BELT_FRONT_Y - 9, PY0
    z0, z1 = P.BEAM_Z_TOP + 2, P.CARRIAGE_TOP_Z
    body = box(cx - 30, cx + 30, y0, y1, z0, z1)
    # Ranura de la correa (tramo delantero) y tornillos a la placa
    body = body.cut(box(cx - 31, cx + 31, P.BELT_FRONT_Y - 0.5, P.BELT_FRONT_Y + 2,
                        P.BELT_Z - P.BELT_W / 2 - 0.5, P.BELT_Z + P.BELT_W / 2 + 0.5))
    for dx in (-20, 20):
        body = body.cut(rod_y(y0 - 1, y1 + 1, cx + dx, z1 - 8, 3.4))
    return body


def heads(cx=0.0):
    hx, hy, hz = P.HEAD_SIZE
    fx, fy, ft = P.HEAD_FLANGE
    fz = P.HEAD_GAP + P.HEAD_FLANGE_Z
    out = []
    for x in head_xs(cx):
        body = box(x - hx / 2, x + hx / 2, -hy / 2, hy / 2, P.HEAD_GAP, P.HEAD_GAP + hz)
        flange = box(x - fx / 2, x + fx / 2, -fy / 2, fy / 2, fz, fz + ft)
        out.append(body.union(flange))
    return out


def printed_parts():
    return {"carro_placa": plate(), "carro_bandeja": shelf(), "carro_pinza_correa": belt_clamp()}


def add(assy, cx):
    for i, b in enumerate(blocks(cx)):
        assy.add(b, name=f"patin_{i}", color=STEEL)
    assy.add(plate(cx), name="carro_placa", color=PRINTED)
    assy.add(shelf(cx), name="carro_bandeja", color=PRINTED)
    assy.add(belt_clamp(cx), name="carro_pinza_correa", color=PRINTED)
    for i, h in enumerate(heads(cx)):
        assy.add(h, name=f"cabezal_{i}", color=HEAD)

    # Reserva: dampers, placa del cabezal, tubos de tinta y cadena portacables
    # (entre los nervios de la bandeja)
    top = P.HEAD_GAP + P.HEAD_SIZE[2]
    assy.add(box(cx - SHELF_HALF_W + 6, cx + SHELF_HALF_W - 6, PY1 + FLANGE_T, P.SHELF_FRONT_Y,
                 top, P.CARRIAGE_TOP_Z), name="reserva_carro", color=RESERVED)
