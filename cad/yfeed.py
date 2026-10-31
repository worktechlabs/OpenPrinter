"""Fase 0.6 - Arrastre Y.

- Rodillo de arrastre: tubo de Ø30 sobre eje de Ø12 que gira en rodamientos
  6001 alojados en las placas laterales. Superficie con recubrimiento abrasivo
  (grit) o goma fina.
- Unidades de presión (impresas), colgadas de la ranura inferior de la viga X:
  soporte, brazo basculante con rueda de TPU sobre rodamiento 625 y muelle de
  compresión bajo la cola del brazo, que hace bajar la rueda contra el rodillo.
- Levante: un eje de Ø8 con una leva excéntrica por unidad. Al girarlo con la
  palanca exterior, las levas empujan la cola de los brazos y las ruedas suben
  para meter o sacar el film.
- Motor Y: NEMA17 en un soporte impreso por fuera de la placa derecha,
  reducción 4:1 con correa GT2 (20T -> 80T).
"""
import math

import cadquery as cq

import params as P
from lib import BELT, MOTOR, PRINTED, PRINTED_ALT, RUBBER, STEEL, box, rod_x, rod_y, strip_yz

GY = P.GRIT_ROLLER_Y
GZ = -P.GRIT_ROLLER_D / 2
XL, XR = P.BEAM_X0, P.BEAM_X1
T = P.SIDE_PLATE_T
OUT_R = XR + T                    # cara exterior de la placa derecha

# Unidad de presión (coordenadas Y, Z)
PVY, PVZ = P.PINCH_PIVOT
SY, SZ = P.LIFT_SHAFT
WHEEL_R = P.PINCH_WHEEL_D / 2
AXLE = (GY, 0.1 + WHEEL_R)        # rueda apoyada sobre el film
ARM_HALF = 8                      # medio ancho del brazo
CHEEK = (ARM_HALF + 0.5, ARM_HALF + 3.5)
BLOCK_Z0 = 32                     # cara inferior del bloque bajo la viga
SPRING_Y = PVY - 10               # bajo la cola del brazo
BRIDGE_Z = (3, 6)                 # puente entre mejillas donde apoya el muelle

# Motor Y
PULLEY_X = (OUT_R + 9, OUT_R + 21)
YM_Z = GZ - P.Y_MOTOR_DZ
YM_FACE_X = OUT_R + 28            # cara del motor (exterior del soporte)
YM_BOLTS = [(GY + dy, YM_Z + dz) for dy in (-25, 25) for dz in (-21, 27)]


def pinch_xs():
    n, fw = P.PINCH_COUNT, P.FILM_WIDTH
    return [-fw / 2 + 30 + i * (fw - 60) / (n - 1) for i in range(n)]


def _yz_prism(points, x0, x1):
    return cq.Workplane("YZ").polyline(points).close().extrude(x1 - x0).translate((x0, 0, 0))


def pinch_bracket(x=0.0):
    zb = P.BEAM_Z_BOTTOM
    block = box(x - CHEEK[1], x + CHEEK[1], P.BEAM_Y_BACK, P.BEAM_Y_FRONT, BLOCK_Z0, zb)
    for side in (-1, 1):
        cx0, cx1 = sorted((x + side * CHEEK[0], x + side * CHEEK[1]))
        cheek = (box(cx0, cx1, SY - 9, P.BEAM_Y_BACK, 12, SZ + 12)
                 .union(box(cx0, cx1, P.BEAM_Y_BACK, PVY + 6, 12, zb))
                 .union(box(cx0, cx1, SPRING_Y - 6, SPRING_Y + 6, BRIDGE_Z[0], 12)))
        block = block.union(cheek)
    block = block.union(box(x - CHEEK[1], x + CHEEK[1], SPRING_Y - 6, SPRING_Y + 6, *BRIDGE_Z))
    block = block.cut(rod_x(x - 20, x + 20, PVY, PVZ, 3.2))               # pasador M3
    block = block.cut(rod_x(x - 20, x + 20, SY, SZ, P.LIFT_SHAFT_D + 0.4))
    # M5 a la ranura inferior de la viga y alojamiento del muelle
    slot_y = (P.BEAM_Y_BACK + P.BEAM_Y_FRONT) / 2
    block = block.cut(cq.Workplane("XY").circle(2.75).extrude(10).translate((x, slot_y, BLOCK_Z0 - 1)))
    block = block.cut(cq.Workplane("XY").circle(3.5).extrude(2).translate((x, SPRING_Y, BRIDGE_Z[1] - 1.5)))
    return block


def pinch_arm(x=0.0):
    ay, az = AXLE
    pts = [(SY - 7, PVZ - 5), (SY - 7, PVZ + 5), (PVY + 6, PVZ + 5), (ay + 9, az + 5),
           (ay + 9, az - 5), (ay - 6, az - 5), (PVY, PVZ - 5)]
    arm = _yz_prism(pts, x - ARM_HALF, x + ARM_HALF)
    arm = arm.cut(box(x - P.PINCH_WHEEL_W / 2 - 1, x + P.PINCH_WHEEL_W / 2 + 1,
                      ay - WHEEL_R - 2, ay + WHEEL_R + 2, -1, PVZ + 6))      # horquilla
    arm = arm.cut(rod_x(x - 20, x + 20, PVY, PVZ, 3.4))
    arm = arm.cut(rod_x(x - 20, x + 20, ay, az, 5.2))                         # eje M5 rueda
    return arm


def pinch_wheel(x=0.0):
    ay, az = AXLE
    w = P.PINCH_WHEEL_W
    return (rod_x(x - w / 2, x + w / 2, ay, az, P.PINCH_WHEEL_D)
            .cut(rod_x(x - w, x + w, ay, az, 16)))                           # rodamiento 625


def cam(x=0.0, engaged=False):
    """Leva excéntrica de 10 mm de ancho sobre el eje de levante."""
    dz = -P.CAM_ECC if engaged else P.CAM_ECC
    return (rod_x(x - 5, x + 5, SY, SZ + dz, P.CAM_D)
            .cut(rod_x(x - 6, x + 6, SY, SZ, P.LIFT_SHAFT_D + 0.2)))


def spring(x=0.0):
    """Muelle de compresión Ø6 entre el puente del soporte y la cola del brazo."""
    z0, z1 = BRIDGE_Z[1] - 1.5, PVZ - 5
    return cq.Workplane("XY").circle(3).extrude(z1 - z0).translate((x, SPRING_Y, z0))


def lift_lever():
    x0 = OUT_R + 30
    hub = rod_x(x0, x0 + 8, SY, SZ, 18)
    bar = box(x0, x0 + 8, SY - 5, SY + 5, SZ, SZ + 70)
    return hub.union(bar).cut(rod_x(x0 - 1, x0 + 9, SY, SZ, P.LIFT_SHAFT_D + 0.2))


def motor_mount():
    y0, y1 = GY - 38, GY + 38
    z0, z1 = YM_Z - 33, YM_Z + 33
    back = box(OUT_R, OUT_R + 6, y0, y1, z0, z1)
    front = box(YM_FACE_X - 6, YM_FACE_X, y0, y1, z0, z1)
    walls = (box(OUT_R, YM_FACE_X, y0, y0 + 6, z0, z1)
             .union(box(OUT_R, YM_FACE_X, y1 - 6, y1, z0, z1))
             .union(box(OUT_R, YM_FACE_X, y0, y1, z0, z0 + 6)))
    body = back.union(front).union(walls)
    body = body.cut(rod_x(YM_FACE_X - 7, YM_FACE_X + 1, GY, YM_Z, 23))
    # Colisos verticales M3 para tensar la correa moviendo el motor
    for dy in (-15.5, 15.5):
        for dz in (-15.5, 15.5):
            slot = (cq.Workplane("YZ").slot2D(9.4, 3.4, angle=90).extrude(8)
                    .translate((YM_FACE_X - 7, GY + dy, YM_Z + dz)))
            body = body.cut(slot)
    for y, z in YM_BOLTS:
        body = body.cut(rod_x(OUT_R - 1, OUT_R + 7, y, z, 5.5))
    return body


def _belt_runs():
    (r1, c1), (r2, c2) = (P.Y_PULLEY_PD[1] / 2, (GY, GZ)), (P.Y_PULLEY_PD[0] / 2, (GY, YM_Z))
    dy, dz = c2[0] - c1[0], c2[1] - c1[1]
    d = math.hypot(dy, dz)
    uy, uz = dy / d, dz / d
    cos_t = (r1 - r2) / d
    sin_t = math.sqrt(1 - cos_t ** 2)
    runs = []
    for s in (-1, 1):
        vy, vz = uy * cos_t - s * uz * sin_t, uz * cos_t + s * uy * sin_t
        p1 = (c1[0] + r1 * vy, c1[1] + r1 * vz)
        p2 = (c2[0] + r2 * vy, c2[1] + r2 * vz)
        runs.append([p1, p2] if s > 0 else [p2, p1])
    return runs


def printed_parts():
    return {
        "presion_soporte": pinch_bracket(),
        "presion_brazo": pinch_arm(),
        "presion_rueda_tpu": pinch_wheel(),
        "presion_leva": cam(),
        "presion_palanca": lift_lever(),
        "soporte_motor_y": motor_mount(),
    }


def add(assy):
    # Rodillo, eje y rodamientos
    assy.add(rod_x(XL - T - P.GRIT_SHAFT_OUT_L, PULLEY_X[1] + 3, GY, GZ, P.GRIT_SHAFT_D),
             name="eje_arrastre", color=STEEL)
    assy.add(rod_x(*P.PLATEN_X, GY, GZ, P.GRIT_ROLLER_D)
             .cut(rod_x(P.PLATEN_X[0] - 1, P.PLATEN_X[1] + 1, GY, GZ, P.GRIT_SHAFT_D)),
             name="rodillo_arrastre", color=STEEL)
    for i, x0 in enumerate((XL - T + 1, XR + 1)):
        bearing = (rod_x(x0, x0 + 8, GY, GZ, P.GRIT_BEARING_OD)
                   .cut(rod_x(x0 - 1, x0 + 9, GY, GZ, P.GRIT_SHAFT_D)))
        assy.add(bearing, name=f"rodamiento_arrastre_{i}", color=STEEL)

    # Unidades de presión y eje de levante
    for i, x in enumerate(pinch_xs()):
        assy.add(pinch_bracket(x), name=f"presion_soporte_{i}", color=PRINTED)
        assy.add(pinch_arm(x), name=f"presion_brazo_{i}", color=PRINTED_ALT)
        assy.add(pinch_wheel(x), name=f"presion_rueda_{i}", color=RUBBER)
        assy.add(cam(x), name=f"presion_leva_{i}", color=PRINTED)
        assy.add(spring(x), name=f"presion_muelle_{i}", color=STEEL)
    assy.add(rod_x(XL - T - 5, OUT_R + 45, SY, SZ, P.LIFT_SHAFT_D), name="eje_levante", color=STEEL)
    assy.add(lift_lever(), name="presion_palanca", color=PRINTED)

    # Motor Y y transmisión
    assy.add(motor_mount(), name="soporte_motor_y", color=PRINTED_ALT)
    assy.add(box(YM_FACE_X, YM_FACE_X + P.NEMA_LEN, GY - P.NEMA / 2, GY + P.NEMA / 2,
                 YM_Z - P.NEMA / 2, YM_Z + P.NEMA / 2), name="motor_y", color=MOTOR)
    assy.add(rod_x(*PULLEY_X, GY, GZ, P.Y_PULLEY_PD[1] + 2)
             .cut(rod_x(PULLEY_X[0] - 1, PULLEY_X[1] + 1, GY, GZ, P.GRIT_SHAFT_D)),
             name="polea_80t_y", color=STEEL)
    assy.add(rod_x(*PULLEY_X, GY, YM_Z, 16), name="polea_20t_y", color=STEEL)
    bx0 = (PULLEY_X[0] + PULLEY_X[1] - P.Y_BELT_W) / 2
    for i, run in enumerate(_belt_runs()):
        assy.add(strip_yz(run, bx0, bx0 + P.Y_BELT_W, t=1.5), name=f"correa_y_{i}", color=BELT)


def plate_holes():
    """Agujeros que este módulo necesita en las placas laterales: (y, z, d)."""
    return ([(SY, SZ, P.LIFT_SHAFT_D + 0.5)]
            + [(y, z, P.M5_CLEAR) for y, z in YM_BOLTS])
