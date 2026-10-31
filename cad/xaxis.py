"""Fase 0.3 - Viga X.

Sobre la viga 4080 (del chasis) van dos guías MGN12 en la cara delantera, una
por ranura. La correa GT2 de 10 mm corre por encima de la viga en un plano
horizontal: motor a la izquierda (eje hacia abajo, sobre un soporte impreso) y
polea loca a la derecha en un tensor impreso que desliza en X.
"""
import cadquery as cq

import params as P
from lib import BELT, MOTOR, PRINTED_ALT, STEEL, box, rod_z

YF, YB = P.BEAM_Y_FRONT, P.BEAM_Y_BACK
ZT = P.BEAM_Z_TOP
BASE_T = 6                   # base de los soportes sobre la viga
PULLEY_Z = (P.BELT_Z - 6, P.BELT_Z + 9)
TOP_Z = PULLEY_Z[1] + 1      # cara inferior de la placa superior de los soportes
TOP_T = 8
SLOT_Y = (YB + YF) / 2       # ranura superior del 4080
FRONT_Y = P.PULLEY_Y + 28    # borde delantero de los soportes
IDLER_X0 = P.BEAM_X1 - P.BEAM_END + 6
HOME_SENSOR_SCREW = (IDLER_X0 + 22, -91)    # inserto M3 para el soporte del final de carrera X


def _beam_bolts(solid, xs):
    """Agujeros M5 para tuercas en T en la ranura superior de la viga."""
    for x in xs:
        solid = solid.cut(rod_z(ZT - 1, TOP_Z + TOP_T + 1, x, SLOT_Y, 5.5))
    return solid


def motor_mount():
    x0, x1 = P.BEAM_X0, P.BEAM_X0 + P.BEAM_END - 4
    mx, my = P.MOTOR_X, P.PULLEY_Y
    body = (box(x0, x1, YB, YF, ZT, ZT + BASE_T)                       # base
            .union(box(x0, x1, YB, YB + 8, ZT, TOP_Z + TOP_T))         # pared trasera
            .union(box(x0, x0 + 8, YB, FRONT_Y, ZT, TOP_Z + TOP_T))    # pared lateral
            .union(box(x0, x1, YB, FRONT_Y, TOP_Z, TOP_Z + TOP_T)))    # asiento del motor
    body = body.cut(rod_z(TOP_Z - 1, TOP_Z + TOP_T + 1, mx, my, 23))   # centrador NEMA17
    for dx in (-15.5, 15.5):
        for dy in (-15.5, 15.5):
            body = body.cut(rod_z(TOP_Z - 1, TOP_Z + TOP_T + 1, mx + dx, my + dy, 3.4))
    # Hueco para la polea y la salida de la correa
    body = body.cut(box(x0 + 8, x1 + 1, my - 12, FRONT_Y + 1, ZT + BASE_T, TOP_Z))
    return _beam_bolts(body, (x0 + 18, x1 - 8))


def idler_mount():
    x0, x1 = IDLER_X0, P.BEAM_X1
    ix, iy = P.IDLER_X, P.PULLEY_Y
    body = (box(x0, x1, YB, YF, ZT, ZT + BASE_T)
            .union(box(x0, x1, YB, YB + 8, ZT, TOP_Z + TOP_T))
            .union(box(x1 - 8, x1, YB, FRONT_Y, ZT, TOP_Z + TOP_T))    # pared del tornillo tensor
            .union(box(x0, x1, YB, FRONT_Y, TOP_Z, TOP_Z + TOP_T)))
    body = body.cut(box(x0 - 1, x1 - 8, iy - 12, FRONT_Y + 1, ZT + BASE_T, TOP_Z))
    # Colisos para el eje M5 de la polea (tensado en X) y paso del tornillo tensor M4
    slot = (cq.Workplane("XY").slot2D(14, 5.5).extrude(TOP_T + 2)
            .translate((ix, iy, TOP_Z - 1)))
    body = body.cut(slot).cut(slot.translate((0, 0, -(TOP_Z - ZT))))
    body = body.cut(cq.Workplane("YZ").circle(2.2).extrude(10)
                    .translate((x1 - 9, iy, P.BELT_Z)))
    hx, hy = HOME_SENSOR_SCREW
    body = body.cut(rod_z(TOP_Z + TOP_T - 6, TOP_Z + TOP_T + 1, hx, hy, 4.2))
    return _beam_bolts(body, (x0 + 10, x1 - 18))


def belt():
    y_front, y_back = P.BELT_FRONT_Y, P.PULLEY_Y - P.PULLEY_PD / 2
    z0, z1 = P.BELT_Z - P.BELT_W / 2, P.BELT_Z + P.BELT_W / 2
    return (box(P.MOTOR_X, P.IDLER_X, y_front, y_front + 1.5, z0, z1)
            .union(box(P.MOTOR_X, P.IDLER_X, y_back - 1.5, y_back, z0, z1)))


def printed_parts():
    return {"soporte_motor_x": motor_mount(), "soporte_tensor_x": idler_mount()}


def add(assy):
    for i, z in enumerate(P.RAIL_Z):
        rail = box(P.RAIL_X0, P.RAIL_X0 + P.RAIL_LENGTH, YF, YF + P.RAIL_H,
                   z - P.RAIL_W / 2, z + P.RAIL_W / 2)
        assy.add(rail, name=f"guia_mgn12_{i}", color=STEEL)

    for name, part in printed_parts().items():
        assy.add(part, name=name, color=PRINTED_ALT)

    mx, iy = P.MOTOR_X, P.PULLEY_Y
    motor_z = TOP_Z + TOP_T
    nema = box(mx - P.NEMA / 2, mx + P.NEMA / 2, iy - P.NEMA / 2, iy + P.NEMA / 2,
               motor_z, motor_z + P.NEMA_LEN)
    assy.add(nema, name="motor_x", color=MOTOR)
    assy.add(rod_z(PULLEY_Z[0], PULLEY_Z[1], mx, iy, 16), name="polea_motor_x", color=STEEL)
    assy.add(rod_z(PULLEY_Z[0], PULLEY_Z[1], P.IDLER_X, iy, 16), name="polea_loca_x", color=STEEL)
    assy.add(belt(), name="correa_x", color=BELT)
