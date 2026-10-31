"""Fase 1 - Sensores, cadena portacables y electrónica.

- Encoder X: cinta de 180 LPI entre las dos guías, sujeta por dos soportes
  impresos en los extremos de la viga (el derecho tensa con muelle). El sensor
  óptico va en la cara trasera de la placa del carro, entre los patines.
- Final de carrera X: sensor de horquilla sobre el soporte del tensor y bandera
  impresa en la parte alta del carro.
- Encoder Y: AS5047P frente a un imán diametral en la punta del eje del rodillo,
  por fuera de la placa izquierda.
- Cadena portacables X: bandeja impresa detrás de la viga, anclaje fijo en el
  centro del recorrido y brazo impreso sobre la pinza de correa del carro.
"""
import cadquery as cq

import params as P
import xaxis
import yfeed
from lib import (BELT, MOTOR, PRINTED, PRINTED_ALT, RUBBER, STEEL, box, rod_x,
                 rod_y, rod_z)

YF, YB = P.BEAM_Y_FRONT, P.BEAM_Y_BACK
SY0, SY1 = P.ENC_STRIP_Y - 0.1, P.ENC_STRIP_Y + 0.1
SZ0, SZ1 = P.ENC_STRIP_Z
PY0 = P.CARRIAGE_PLATE_Y                    # cara trasera de la placa del carro
TOP = P.CARRIAGE_TOP_Z
IDLER_TOP = xaxis.TOP_Z + xaxis.TOP_T       # cara superior del soporte del tensor
GY, GZ = yfeed.GY, yfeed.GZ
PLATE_OUT_L = P.BEAM_X0 - P.SIDE_PLATE_T    # cara exterior de la placa izquierda
SHAFT_END = PLATE_OUT_L - P.GRIT_SHAFT_OUT_L

# Carro: insertos que necesitan estas piezas (los usa carriage.plate)
SENSOR_SCREWS = [(-8, 93), (8, 93)]         # (dx, z) en la cara trasera
FLAG_SCREW = (93, PY0 + 5)                  # (dx, y) en la cara superior
# Soporte del final de carrera, sobre el soporte del tensor
HOME_X = xaxis.IDLER_X0
HOME_SCREWS = [xaxis.HOME_SENSOR_SCREW]


# --- Encoder X -------------------------------------------------------------

def strip():
    return box(*P.ENC_STRIP_X, SY0, SY1, SZ0, SZ1)


def strip_bracket(side):
    """Soporte de extremo de la cinta, en la cara delantera de la viga."""
    x0, x1 = (P.BEAM_X0 + 5, P.BEAM_X0 + 35) if side < 0 else (P.BEAM_X1 - 45, P.BEAM_X1 - 5)
    body = box(x0, x1, YF, YF + 10, P.RAIL_Z[0] - 8, SZ1 + 7)
    body = body.cut(box(x0 - 1, x1 + 1, SY0 - 0.3, SY1 + 0.3, SZ0 - 0.5, SZ1 + 0.5))   # ranura
    body = body.cut(rod_y(YF - 1, YF + 11, (x0 + x1) / 2, P.RAIL_Z[0], 5.5))         # M5 a la ranura
    body = body.cut(cq.Workplane("XY").circle(1.4).extrude(12)
                    .translate(((x0 + x1) / 2, P.ENC_STRIP_Y, SZ1 + 1)))          # prisionero M3
    if side > 0:   # alojamiento del muelle de tensión
        body = body.cut(rod_x(x0 + 6, x1 - 6, P.ENC_STRIP_Y, (SZ0 + SZ1) / 2, 6))
    return body


def sensor_bracket(cx=0.0):
    z0, z1 = P.ENC_SENSOR_Z[0] - 2, 98
    body = box(cx - 14, cx + 14, PY0 - 4, PY0, z0, z1)
    for dx, z in SENSOR_SCREWS:
        body = body.cut(rod_y(PY0 - 5, PY0 + 1, cx + dx, z, 3.4))
    return body


def sensor(cx=0.0):
    """Sensor óptico de cuadratura (tipo H9730) con la horquilla abierta abajo."""
    z0, z1 = P.ENC_SENSOR_Z
    body = box(cx - 7, cx + 7, YF + 1, PY0 - 4, z0, z1)
    return body.cut(box(cx - 8, cx + 8, SY0 - 0.9, SY1 + 0.9, z0 - 1, SZ1 + 1))


# --- Final de carrera X ------------------------------------------------------

def home_flag(cx=0.0):
    fy0, fy1 = PY0 + 2, PY0 + 8
    fin = box(cx + 88, cx + 98, fy0, fy1, TOP, TOP + 18)
    arm = box(cx + 88, cx + 112, fy0, fy1, TOP + 10, TOP + 18)
    body = fin.union(arm)
    return body.cut(rod_z(TOP - 1, TOP + 19, cx + FLAG_SCREW[0], FLAG_SCREW[1], 3.4))


def home_sensor():
    """Soporte del sensor de horquilla (impreso) + sensor, sobre el soporte del tensor."""
    x0, y0, y1 = HOME_X, PY0 - 3, PY0 + 13
    base = box(x0, x0 + 30, y0, y1, IDLER_TOP, IDLER_TOP + 3)
    body = base.union(box(x0, x0 + 14, y0, y1, IDLER_TOP, IDLER_TOP + 20))
    # Horquilla abierta hacia -X para la bandera
    body = body.cut(box(x0 - 1, x0 + 10, PY0 + 1, PY0 + 9, IDLER_TOP + 3, IDLER_TOP + 21))
    for x, y in HOME_SCREWS:
        body = body.cut(rod_z(IDLER_TOP - 1, IDLER_TOP + 4, x, y, 3.4))
    return body


# --- Encoder Y ---------------------------------------------------------------

def y_encoder_bracket():
    x_base = PLATE_OUT_L
    pcb_x = SHAFT_END - 2.5 - 1.5                     # imán 2,5 mm + 1,5 mm de aire
    base = box(x_base - 6, x_base, GY - 30, GY + 30, GZ - 14, GZ + 14)
    base = base.cut(rod_x(x_base - 7, x_base + 1, GY, GZ, 18))
    for dy in (-22, 22):
        base = base.cut(rod_x(x_base - 7, x_base + 1, GY + dy, GZ, 3.4))
    for dy in (-13, 13):
        post = rod_x(pcb_x, x_base - 6, GY + dy, GZ, 7)
        base = base.union(post.cut(rod_x(pcb_x - 1, x_base, GY + dy, GZ, 2.5)))
    return base


def y_encoder_parts():
    pcb_x = SHAFT_END - 2.5 - 1.5
    magnet = rod_x(SHAFT_END - 2.5, SHAFT_END, GY, GZ, 6)
    pcb = box(pcb_x - 1.6, pcb_x, GY - 16, GY + 16, GZ - 12.5, GZ + 12.5)
    return magnet, pcb


# --- Cadena portacables ------------------------------------------------------

# La altura se calcula desde el brazo del carro hacia abajo: el tramo superior
# de la cadena pasa justo bajo el brazo, y la bandeja queda a la altura que
# pida el radio de curvatura.
CHAIN_TOP = TOP + 2                          # cara superior del tramo superior
CHAIN_ZC = CHAIN_TOP - P.CHAIN_R - P.CHAIN_H / 2
CHAIN_Z0 = CHAIN_ZC - P.CHAIN_R - P.CHAIN_H / 2
TRAY_Z0 = CHAIN_Z0 - 4
TRAY_TOP = max(TRAY_Z0 + 18, P.RAIL_Z[1] + 10)


def tray_segment(x0, x1):
    flange = box(x0, x1, YB - 3, YB, TRAY_Z0, TRAY_TOP)
    shelf = box(x0, x1, P.CHAIN_Y[0] - 7, YB, TRAY_Z0, TRAY_Z0 + 4)
    lip = box(x0, x1, P.CHAIN_Y[0] - 7, P.CHAIN_Y[0] - 3, TRAY_Z0, TRAY_Z0 + 24)
    body = flange.union(shelf).union(lip)
    for fx in (0.25, 0.75):
        for z in P.RAIL_Z:      # M5 a las ranuras traseras de la viga que caen en el ala
            if TRAY_Z0 + 5 < z < TRAY_TOP - 5:
                body = body.cut(rod_y(YB - 4, YB + 1, x0 + fx * (x1 - x0), z, 5.5))
    return body


def chain(cx):
    """Cadena en la posición del carro cx: tramo inferior, curva y tramo superior."""
    r_in, r_out = P.CHAIN_R - P.CHAIN_H / 2, P.CHAIN_R + P.CHAIN_H / 2
    zc = CHAIN_ZC
    # Tramo recto total fijo: con el carro en X_MIN la curva queda justo en el carro
    straight = P.CHAIN_FIX_X - P.CARRIAGE_X_MIN
    xb = (P.CHAIN_FIX_X + cx - straight) / 2
    y0, y1 = P.CHAIN_Y
    body = (cq.Workplane("XZ").circle(r_out).circle(r_in).extrude(-(y1 - y0))
            .cut(box(0, r_out + 1, 0, y1 - y0, -r_out - 1, r_out + 1))
            .translate((xb, y0, zc)))
    if P.CHAIN_FIX_X - xb > 0.5:
        body = body.union(box(xb, P.CHAIN_FIX_X, y0, y1, CHAIN_Z0, CHAIN_Z0 + P.CHAIN_H))
    if cx - xb > 0.5:
        body = body.union(box(xb, cx, y0, y1, zc + r_in, zc + r_out))
    return body


def chain_arm(cx=0.0):
    z_top_chain = CHAIN_TOP
    y_clamp = P.BELT_FRONT_Y - 9
    riser = box(cx - 15, cx + 15, y_clamp, PY0, TOP, z_top_chain + 9)
    arm = box(cx - 15, cx + 15, P.CHAIN_Y[0] - 3, y_clamp, z_top_chain + 1, z_top_chain + 9)
    body = riser.union(arm)
    for dx in (-8, 8):
        body = body.cut(rod_z(TOP - 1, z_top_chain + 10, cx + dx, (y_clamp + PY0) / 2, 3.4))
    return body


def plate_holes():
    """Agujeros en las placas laterales: soporte del encoder Y (en ambas)."""
    return [(GY + dy, GZ, 3.4) for dy in (-22, 22)]


def printed_parts():
    w = (P.CHAIN_TRAY_X[1] - P.CHAIN_TRAY_X[0]) / 2
    return {
        "encoder_soporte_cinta_izq": strip_bracket(-1),
        "encoder_soporte_cinta_der": strip_bracket(1),
        "encoder_soporte_sensor": sensor_bracket(),
        "final_x_bandera": home_flag(),
        "final_x_soporte": home_sensor(),
        "encoder_y_soporte": y_encoder_bracket(),
        "cadena_bandeja": tray_segment(0, w),
        "cadena_brazo": chain_arm(),
    }


def add(assy, cx):
    assy.add(strip(), name="encoder_cinta", color=STEEL)
    for side, name in ((-1, "izq"), (1, "der")):
        assy.add(strip_bracket(side), name=f"encoder_soporte_cinta_{name}", color=PRINTED)
    assy.add(sensor_bracket(cx), name="encoder_soporte_sensor", color=PRINTED)
    assy.add(sensor(cx), name="encoder_sensor", color=MOTOR)

    assy.add(home_flag(cx), name="final_x_bandera", color=PRINTED)
    assy.add(home_sensor(), name="final_x_soporte", color=PRINTED_ALT)

    assy.add(y_encoder_bracket(), name="encoder_y_soporte", color=PRINTED)
    magnet, pcb = y_encoder_parts()
    assy.add(magnet, name="encoder_y_iman", color=RUBBER)
    assy.add(pcb, name="encoder_y_pcb", color=PRINTED_ALT)

    x0, x1 = P.CHAIN_TRAY_X
    mid = (x0 + x1) / 2
    for i, (a, b) in enumerate(((x0, mid - 0.5), (mid + 0.5, x1))):
        assy.add(tray_segment(a, b), name=f"cadena_bandeja_{i}", color=PRINTED_ALT)
    assy.add(chain(cx), name="cadena_portacables", color=BELT)
    assy.add(chain_arm(cx), name="cadena_brazo", color=PRINTED)

