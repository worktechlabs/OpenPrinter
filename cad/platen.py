"""Fase 0.5 - Mesa de vacío.

Placa superior de aluminio de 3 mm perforada (DXF para corte) sobre
PLATEN_SEGMENTS cámaras de vacío impresas iguales. Cada cámara lleva su
ventilador de 80 mm debajo, así que cada segmento es una zona que se puede
apagar cuando se usa film más estrecho.

Las cámaras se apoyan en los dos travesaños de mesa (M5 con tuerca en T) y la
placa se atornilla a ellas con M3 avellanados a insertos. Las juntas entre
cámaras y con la placa se sellan con cinta de espuma.
"""
import cadquery as cq

import params as P
from lib import MOTOR, PLATEN, PRINTED_ALT, box, rod_z

PX0, PX1 = P.PLATEN_X
PY0, PY1 = P.PLATEN_Y
SEG_W = (PX1 - PX0) / P.PLATEN_SEGMENTS
CH_Z0, CH_Z1 = -P.PLATEN_DEPTH, -P.PLATEN_TOP_T
WALL = 3
FAN_Y = sum(P.PLATEN_RAIL_Y) / 2          # entre los dos travesaños
FAN_HOLE = P.PLATEN_FAN - 6
FAN_SCREW = 71.5 / 2                      # 80 mm: tornillos en cuadrado de 71,5
POST_PITCH = 40                           # pilares que sostienen la placa
BOSS = 4.5 + WALL                         # centro de los insertos M3 desde el borde


def _boss_points(x0):
    xs = (x0 + BOSS, x0 + SEG_W - BOSS)
    ys = (PY0 + BOSS, (PY0 + PY1) / 2, PY1 - BOSS)
    return [(x, y) for x in xs for y in ys]


def segment(x0=PX0):
    xc = x0 + SEG_W / 2
    body = box(x0, x0 + SEG_W, PY0, PY1, CH_Z0, CH_Z1)
    body = body.cut(box(x0 + WALL, x0 + SEG_W - WALL, PY0 + WALL, PY1 - WALL,
                        CH_Z0 + WALL, CH_Z1 + 1))

    # Pilares de apoyo de la placa, fuera de la boca del ventilador
    for i in range(1, int(SEG_W // POST_PITCH) + 1):
        for j in range(1, int((PY1 - PY0) // POST_PITCH) + 1):
            x, y = x0 + i * SEG_W / (SEG_W // POST_PITCH + 1), PY0 + j * POST_PITCH
            if (x - xc) ** 2 + (y - FAN_Y) ** 2 < (FAN_HOLE / 2 + 8) ** 2 or y > PY1 - 10:
                continue
            body = body.union(rod_z(CH_Z0 + WALL, CH_Z1, x, y, 8))
    # Torretas para insertos M3 de la placa superior
    for x, y in _boss_points(x0):
        body = body.union(rod_z(CH_Z0 + WALL, CH_Z1, x, y, 9))
        body = body.cut(rod_z(CH_Z1 - 8, CH_Z1 + 1, x, y, 4.2))

    # Boca y tornillos del ventilador
    body = body.cut(rod_z(CH_Z0 - 1, CH_Z0 + WALL + 1, xc, FAN_Y, FAN_HOLE))
    for dx in (-FAN_SCREW, FAN_SCREW):
        for dy in (-FAN_SCREW, FAN_SCREW):
            body = body.cut(rod_z(CH_Z0 - 1, CH_Z0 + WALL + 1, xc + dx, FAN_Y + dy, 4.3))
    # Tornillos M5 a los travesaños de mesa
    for ry in P.PLATEN_RAIL_Y:
        for fx in (0.25, 0.75):
            body = body.cut(rod_z(CH_Z0 - 1, CH_Z0 + WALL + 1, x0 + fx * SEG_W, ry, 5.5))
    return body


def top_sketch():
    """Placa superior en coordenadas (X, Y)."""
    sk = cq.Sketch().push([((PX0 + PX1) / 2, (PY0 + PY1) / 2)]).rect(PX1 - PX0, PY1 - PY0).reset()
    screws = [pt for k in range(P.PLATEN_SEGMENTS) for pt in _boss_points(PX0 + k * SEG_W)]
    sk = sk.push(screws).circle(1.7, mode="s").reset()

    pitch = P.PLATEN_HOLE_PITCH
    walls = [PX0 + k * SEG_W for k in range(P.PLATEN_SEGMENTS + 1)]
    holes = []
    x = PX0 + pitch / 2
    while x < PX1:
        y = PY0 + pitch
        while y < PY1 - pitch / 2:
            near_wall = min(abs(x - w) for w in walls) < WALL + 3
            near_screw = any((x - sx) ** 2 + (y - sy) ** 2 < 36 for sx, sy in screws)
            if not near_wall and not near_screw:
                holes.append((x, y))
            y += pitch
        x += pitch
    return sk.push(holes).circle(P.PLATEN_HOLE_D / 2, mode="s").reset(), len(holes)


def top_plate():
    sk, _ = top_sketch()
    return cq.Workplane("XY").placeSketch(sk).extrude(P.PLATEN_TOP_T).translate((0, 0, CH_Z1))


def printed_parts():
    return {"mesa_camara": segment()}


def add(assy):
    assy.add(top_plate(), name="mesa_placa", color=PLATEN)
    for k in range(P.PLATEN_SEGMENTS):
        x0 = PX0 + k * SEG_W
        assy.add(segment(x0), name=f"mesa_camara_{k}", color=PRINTED_ALT)
        xc = x0 + SEG_W / 2
        fan = box(xc - P.PLATEN_FAN / 2, xc + P.PLATEN_FAN / 2,
                  FAN_Y - P.PLATEN_FAN / 2, FAN_Y + P.PLATEN_FAN / 2, CH_Z0 - 25, CH_Z0)
        assy.add(fan.cut(rod_z(CH_Z0 - 26, CH_Z0 + 1, xc, FAN_Y, FAN_HOLE)),
                 name=f"ventilador_{k}", color=MOTOR)


def export(out):
    sk, n = top_sketch()
    face = cq.Workplane("XY").placeSketch(sk).extrude(P.PLATEN_TOP_T).section()
    cq.exporters.export(face, str(out / "mesa_placa.dxf"))
    print(f"  1 x placa aluminio {P.PLATEN_TOP_T} mm, {PX1 - PX0:.0f} x {PY1 - PY0:.0f} mm, "
          f"{n} agujeros de {P.PLATEN_HOLE_D} mm (mesa_placa.dxf)")
