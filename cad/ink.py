"""Tinta a granel con relleno automático.

Como en las DTF comerciales, la presión en las boquillas no depende de la
botella sino de un subdepósito pequeño a altura fija:

- Botellas de tinta de 1 L (las que vende el fabricante, con el tapón cambiado
  por uno con salida de tubo y respiradero con filtro), dentro de una caja de
  plástico comprada que hace de bandeja antiderrames. La caja va en una repisa
  detrás de la máquina, a la derecha, fuera del ancho del rollo para poder
  cargarlo desde atrás. El blanco va sobre un agitador magnético.
- Una bomba peristáltica de 12 V por color, en un soporte impreso por fuera de
  la placa izquierda. No toca la tinta y, parada, cierra el tubo.
- Un subdepósito de ~100 ml con flotador por color, en un soporte impreso por
  fuera de la placa izquierda. Cuando el flotador baja, la bomba rellena; el
  nivel queda unos 40 mm por debajo de las boquillas.
- Del subdepósito, los tubos suben pegados a la placa y entran por el agujero
  trasero a la bandeja de la cadena portacables, hasta el carro.

Las bombas las mueve un módulo MOSFET (o ULN2803) desde los GPIO de la
Raspberry Pi, que Klipper usa como segunda MCU; los flotadores van a otros GPIO.
"""
import cadquery as cq

import params as P
from lib import MOTOR, PRINTED, PRINTED_ALT, RUBBER, box, rod_x, rod_y, rod_z

XL = P.BEAM_X0
X_PLATE = XL - P.SIDE_PLATE_T              # cara exterior de la placa izquierda
Y0F = P.FRAME_Y[0]
PR = P.PROFILE
Z_RAIL_TOP = P.FRAME_Z[0] + PR
Z_TABLE = P.FRAME_Z[0] - P.FOOT_H
TUBE_D = 10                                # mazo de 5 tubos de tinta con espiral
TUBE_1 = 4                                 # tubo de un color

INK_COLOR = {
    "C": cq.Color(0.0, 0.62, 0.86, 0.8),
    "M": cq.Color(0.85, 0.1, 0.55, 0.8),
    "Y": cq.Color(0.98, 0.85, 0.1, 0.8),
    "K": cq.Color(0.12, 0.12, 0.12, 0.9),
    "W": cq.Color(0.97, 0.97, 0.97, 0.95),
}
CLEAR = cq.Color(0.80, 0.90, 0.95, 0.30)
MDF = cq.Color(0.72, 0.60, 0.45, 1)
TUBE = cq.Color(0.92, 0.92, 0.92, 0.85)

# Repisa y caja de botellas, detrás a la derecha
SHELF_T = 12
SHELF_X = (P.INK_BOX_X0 - 15, P.INK_BOX_X0 + P.INK_BOX[0] + 10)
SHELF_Y = (Y0F - 5, Y0F - 5 - P.INK_SHELF_DEPTH - 30)
SHELF_Z = Z_RAIL_TOP                       # cara superior, enrasada con el larguero
BOX_X = (P.INK_BOX_X0, P.INK_BOX_X0 + P.INK_BOX[0])
BOX_Y = (Y0F - 40, Y0F - 40 - P.INK_BOX[1])  # hueco de 40 mm para bajar el eje del rollo
BOX_Z = (SHELF_Z, SHELF_Z + P.INK_BOX[2])
BRACKETS_X = (P.INK_BOX_X0 + 30, P.INK_BOX_X0 + 195, SHELF_X[1] - 20)
RAIL_END_X = P.BEAM_X1 - PR                # el larguero trasero acaba aquí

# Bombas y subdepósitos, por fuera de la placa izquierda
SUB_X = (X_PLATE - 10 - P.INK_SUBTANK[0], X_PLATE - 10)
SUB_PITCH = P.INK_SUBTANK[1] + 3
PUMP_Z = Z_RAIL_TOP + 2 + 17               # eje de las bombas
PUMP_HOLDER_Z = (P.FRAME_Z[0] + 2, PUMP_Z + 20)
HEAD_X = (X_PLATE - 92, X_PLATE - 62)      # cabezales de las bombas, hacia fuera
DRIVER_Z = (Z_RAIL_TOP - 20, Z_RAIL_TOP + 25)
DRIVER_HOLE_Z = Z_RAIL_TOP + 13            # paso de cables a la canaleta del larguero izquierdo


def box_center():
    return (BOX_X[0] + BOX_X[1]) / 2, (BOX_Y[0] + BOX_Y[1]) / 2


def bottle_positions():
    """(color, x, y, z_base): fila delantera C M Y, trasera K y W (sobre el agitador)."""
    cx, cy = box_center()
    z = BOX_Z[0] + 2 + 3                       # sobre la base impresa
    front, back = cy + 50, cy - 50
    return [("C", cx - 100, front, z), ("M", cx, front, z), ("Y", cx + 100, front, z),
            ("K", cx - 100, back, z), ("W", cx + 25, back, BOX_Z[0] + 2 + P.INK_STIRRER[2])]


def subtank_ys():
    return [P.INK_SUBTANK_Y0 + i * SUB_PITCH + P.INK_SUBTANK[1] / 2 for i in range(len(P.INK_COLORS))]


# --- Repisa y caja -----------------------------------------------------------

def shelf():
    return box(*SHELF_X, SHELF_Y[1], SHELF_Y[0], SHELF_Z - SHELF_T, SHELF_Z)


def shelf_bracket(x, on_rail=True):
    """Escuadra impresa: se atornilla a la ranura trasera del larguero (M5 + tuerca
    en T) y apoya en la mesa de trabajo con una pata al fondo."""
    w = 20
    z_arm = SHELF_Z - SHELF_T
    arm = box(x - w / 2, x + w / 2, SHELF_Y[1], Y0F, z_arm - 12, z_arm)
    foot_out = box(x - w / 2, x + w / 2, SHELF_Y[1], SHELF_Y[1] + 18, Z_TABLE, z_arm - 12)
    if on_rail:
        leg = box(x - w / 2, x + w / 2, Y0F - 12, Y0F, P.FRAME_Z[0], z_arm)
        body = arm.union(foot_out).union(leg)
        body = body.cut(rod_y(Y0F - 13, Y0F + 1, x, P.FRAME_Z[0] + PR / 2, P.M5_CLEAR))
    else:
        foot_in = box(x - w / 2, x + w / 2, Y0F - 30, Y0F - 12, Z_TABLE, z_arm - 12)
        body = arm.union(foot_out).union(foot_in)
    # Cartela
    gus = (cq.Workplane("YZ").polyline([(SHELF_Y[1] + 18, z_arm - 12), (SHELF_Y[1] + 18, Z_TABLE + 30),
                                        (SHELF_Y[1] + 90, z_arm - 12)]).close()
           .extrude(6).translate((x - 3, 0, 0)))
    return body.union(gus)


def bottle_box():
    """Caja de plástico comprada (sin tapa, o con la tapa recortada)."""
    (x0, x1), (y1, y0) = BOX_X, BOX_Y
    z0, z1 = BOX_Z
    bx, by = P.INK_BOX_BOTTOM
    cx, cy = box_center()
    rim = 4
    outer = (cq.Workplane("XY").workplane(offset=z0).center(cx, cy).rect(bx, by)
             .workplane(offset=z1 - z0 - 6).rect(x1 - x0 - 2 * rim, y1 - y0 - 2 * rim).loft())
    shell = outer.faces(">Z").shell(-2)
    lip = box(x0, x1, y0, y1, z1 - 6, z1).cut(box(x0 + rim + 2, x1 - rim - 2, y0 + rim + 2, y1 - rim - 2,
                                                   z1 - 7, z1 + 1))
    return shell.union(lip)


def bottle(x, y, z):
    bx, by, bh = P.INK_BOTTLE
    body = (cq.Workplane("XY").box(bx, by, bh, centered=(True, True, False))
            .edges("|Z").fillet(12).translate((x, y, z)))
    neck = rod_z(z + bh, z + bh + 12, x, y, 34)
    cap = rod_z(z + bh + 12, z + bh + 28, x, y, 40)
    return body.union(neck), cap


def bottle_base():
    """Base impresa con alojamientos para que las botellas no se muevan."""
    bx, by = P.INK_BOX_BOTTOM
    cx, cy = box_center()
    z = BOX_Z[0] + 2
    body = box(cx - bx / 2 + 6, cx + bx / 2 - 6, cy - by / 2 + 6, cy + by / 2 - 6, z, z + 3)
    s = P.INK_BOTTLE[0] + 1
    for c, x, y, _ in bottle_positions():
        if c == "W":
            sx = P.INK_STIRRER[0] + 1
            body = body.cut(box(x - sx / 2, x + sx / 2, y - sx / 2, y + sx / 2, z - 1, z + 4))
            continue
        ring = box(x - s / 2 - 3, x + s / 2 + 3, y - s / 2 - 3, y + s / 2 + 3, z + 3, z + 15)
        body = body.union(ring.cut(box(x - s / 2, x + s / 2, y - s / 2, y + s / 2, z, z + 16)))
    return body


# --- Bombas y subdepósitos ----------------------------------------------------

def pump(y):
    motor = rod_x(HEAD_X[1], X_PLATE - 14, y, PUMP_Z, 24)
    head = box(*HEAD_X, y - 12, y + 12, PUMP_Z - 15, PUMP_Z + 15)
    return motor.union(head)


def pump_holder():
    """Soporte impreso de las 5 bombas, atornillado a la placa izquierda."""
    ys = subtank_ys()
    y0, y1 = ys[0] - SUB_PITCH / 2 - 3, ys[-1] + SUB_PITCH / 2 + 3
    z0, z1 = PUMP_HOLDER_Z
    back = box(X_PLATE - 6, X_PLATE, y0, y1, z0, z1)
    flange = box(HEAD_X[1], HEAD_X[1] + 6, y0, y1, z0, z1)
    base = box(HEAD_X[1], X_PLATE, y0, y1, z0, z0 + 5)
    body = back.union(flange).union(base)
    for y in ys:
        body = body.cut(rod_x(HEAD_X[1] - 1, HEAD_X[1] + 7, y, PUMP_Z, 25))
    for y, z in pump_holder_screws():
        body = body.cut(rod_x(X_PLATE - 7, X_PLATE + 1, y, z, P.M5_CLEAR))
    # Paso para la cabeza del M8 del larguero lateral
    return body.cut(rod_x(X_PLATE - 7, X_PLATE + 1, Y0F + 60, P.FRAME_Z[0] + PR / 2, 18))


def pump_holder_screws():
    ys = subtank_ys()
    z0, z1 = PUMP_HOLDER_Z
    return [(y, z) for y in (ys[0] - 2, ys[-1] + 2) for z in (z0 + 10, z1 - 8)]


def driver_box():
    """Caja impresa del módulo MOSFET de las bombas, junto a ellas."""
    y0 = subtank_ys()[-1] + SUB_PITCH / 2 + 12
    x0, x1 = X_PLATE - 50, X_PLATE
    z0, z1 = DRIVER_Z
    body = box(x0, x1, y0, y0 + 70, z0, z1).cut(box(x0 + 2, x1 + 1, y0 + 2, y0 + 68, z0 + 2, z1 - 2))
    return body.cut(rod_x(x1 - 3, x1 + 1, y0 + 35, DRIVER_HOLE_Z, 12))


def driver_box_y():
    return subtank_ys()[-1] + SUB_PITCH / 2 + 12


def subtank(y):
    sx, sy, sh = P.INK_SUBTANK
    z0 = P.INK_SUBTANK_Z0
    body = box(*SUB_X, y - sy / 2, y + sy / 2, z0, z0 + sh)
    cap = box(SUB_X[0] + 5, SUB_X[1] - 5, y - sy / 2 + 2, y + sy / 2 - 2, z0 + sh, z0 + sh + 10)
    return body, cap


def subtank_rack():
    """Soporte impreso de los subdepósitos: respaldo, fondo, separadores y barra."""
    ys = subtank_ys()
    y0, y1 = ys[0] - SUB_PITCH / 2 - 2, ys[-1] + SUB_PITCH / 2 + 2
    z0 = P.INK_SUBTANK_Z0
    back = box(SUB_X[1], X_PLATE, y0, y1, z0 - 5, z0 + P.INK_SUBTANK[2] + 20)
    floor = box(SUB_X[0] - 4, SUB_X[1], y0, y1, z0 - 5, z0)
    bar = box(SUB_X[0] - 4, SUB_X[0], y0, y1, z0 + 30, z0 + 50)
    body = back.union(floor).union(bar)
    for k in range(len(ys) + 1):
        y = ys[0] - SUB_PITCH / 2 + k * SUB_PITCH
        body = body.union(box(SUB_X[0] - 4, SUB_X[1], y - 1.5, y + 1.5, z0, z0 + 40))
    for y, z in subtank_rack_screws():
        body = body.cut(rod_x(SUB_X[1] - 1, X_PLATE + 1, y, z, P.M5_CLEAR))
    return body


def subtank_rack_screws():
    ys = subtank_ys()
    z0 = P.INK_SUBTANK_Z0
    return [(y, z) for y in (ys[0] - 4, ys[-1] + 4) for z in (z0 + 8, z0 + P.INK_SUBTANK[2] + 10)]


def plate_holes():
    """M5 de los soportes de bombas, subdepósitos y caja del driver; paso de cables
    del driver y paso de tubos hacia la cadena: (y, z, d)."""
    holes = [(y, z, P.M5_CLEAR) for y, z in subtank_rack_screws() + pump_holder_screws()]
    yd = driver_box_y()
    holes.append((yd + 35, DRIVER_HOLE_Z, 12))
    y, z, d = P.INK_TUBE_HOLE
    return holes + [(y, z, d)]


# --- Tubos ----------------------------------------------------------------------

def _pipe(points, d):
    """Tubo por una polilínea de tramos paralelos a los ejes."""
    body = None
    for (x0, y0, z0), (x1, y1, z1) in zip(points, points[1:]):
        if x0 != x1:
            seg = rod_x(min(x0, x1) - d / 2, max(x0, x1) + d / 2, y0, z0, d)
        elif y0 != y1:
            seg = rod_y(min(y0, y1) - d / 2, max(y0, y1) + d / 2, x0, z0, d)
        else:
            seg = rod_z(min(z0, z1) - d / 2, max(z0, z1) + d / 2, x0, y0, d)
        body = seg if body is None else body.union(seg)
    return body


def tubes():
    """(nombre, sólido): de las botellas a las bombas, de las bombas a los
    subdepósitos y de los subdepósitos a la cadena portacables."""
    out = []
    ys = subtank_ys()
    drop_y = BOX_Y[0] + 7                      # bajada entre la caja y el hueco del eje
    z_over = max(z + P.INK_BOTTLE[2] for *_, z in bottle_positions()) + 28 + 15
    z_low = P.FRAME_Z[0] + 10
    x_in = HEAD_X[0] - 8                       # bajo los cabezales de las bombas
    for k, (c, x, y, z) in enumerate(bottle_positions()):
        top = z + P.INK_BOTTLE[2] + 28
        out.append((f"tinta_tubo_botella_{c}",
                    _pipe([(x, y, top), (x, y, z_over + 4 * k), (x, drop_y, z_over + 4 * k),
                           (SHELF_X[0] + 2, drop_y, z_over + 4 * k)], TUBE_1)))
    out.append(("tinta_tubo_aspiracion",
                _pipe([(SHELF_X[0] + 2, drop_y, z_over), (SHELF_X[0] - 8, drop_y, z_over),
                       (SHELF_X[0] - 8, drop_y, z_low), (x_in, drop_y, z_low), (x_in, ys[-1], z_low)],
                      TUBE_D)))
    sub_z = P.INK_SUBTANK_Z0 + 20
    for c, y in zip(P.INK_COLORS, ys):
        out.append((f"tinta_tubo_bomba_{c}",
                    _pipe([(HEAD_X[0], y, PUMP_Z), (x_in, y, PUMP_Z), (x_in, y, sub_z),
                           (SUB_X[0], y, sub_z)], TUBE_1)))
    ty, tz, _ = P.INK_TUBE_HOLE
    xp = X_PLATE - TUBE_D / 2 - 2
    top = P.INK_SUBTANK_Z0 + P.INK_SUBTANK[2] + 10
    xc = (SUB_X[0] + SUB_X[1]) / 2
    ym = (ys[0] + ys[-1]) / 2
    for c, y in zip(P.INK_COLORS, ys):
        out.append((f"tinta_tubo_sub_{c}", _pipe([(xc, y, top), (xc, y, top + 15), (xc, ym, top + 15)], TUBE_1)))
    out.append(("tinta_tubos_carro",
                _pipe([(xc, ym, top + 15), (xp, ym, top + 15), (xp, ym, tz), (xp, ty, tz),
                       (XL + 20, ty, tz)], TUBE_D)))
    return out


def tube_clip(y, z):
    """Clip impreso para el mazo de tubos, atornillado a la placa (tornillo para madera)."""
    x0 = X_PLATE - TUBE_D - 6
    body = box(x0, X_PLATE, y - 8, y + 8, z - TUBE_D / 2 - 4, z + TUBE_D / 2 + 4)
    body = body.cut(rod_y(y - 9, y + 9, X_PLATE - TUBE_D / 2 - 2, z, TUBE_D + 0.5))
    return body.cut(rod_x(x0 - 1, X_PLATE + 1, y, z + TUBE_D / 2 + 1, 3.5))


CLIP_POINTS = [(-255, P.INK_TUBE_HOLE[1]), (-210, P.INK_TUBE_HOLE[1])]


def printed_parts():
    return {
        "tinta_escuadra_repisa": shelf_bracket(0),
        "tinta_pata_repisa": shelf_bracket(0, on_rail=False),
        "tinta_base_botellas": bottle_base(),
        "tinta_soporte_bombas": pump_holder(),
        "tinta_soporte_subdepositos": subtank_rack(),
        "tinta_caja_driver": driver_box(),
        "tinta_clip_tubos": tube_clip(*CLIP_POINTS[0]),
    }


def add(assy):
    assy.add(shelf(), name="tinta_repisa", color=MDF)
    for i, x in enumerate(BRACKETS_X):
        name = "tinta_escuadra_repisa" if x < RAIL_END_X - 15 else "tinta_pata_repisa"
        assy.add(shelf_bracket(x, on_rail=x < RAIL_END_X - 15), name=f"{name}_{i}", color=PRINTED)
    assy.add(bottle_box(), name="tinta_caja_botellas", color=CLEAR)
    assy.add(bottle_base(), name="tinta_base_botellas", color=PRINTED_ALT)
    for c, x, y, z in bottle_positions():
        if c == "W":
            sx, sy, sh = P.INK_STIRRER
            assy.add(box(x - sx / 2, x + sx / 2, y - sy / 2, y + sy / 2, z - sh, z), name="tinta_agitador",
                     color=RUBBER)
        body, cap = bottle(x, y, z)
        assy.add(body, name=f"tinta_botella_{c}", color=INK_COLOR[c])
        assy.add(cap, name=f"tinta_tapon_{c}", color=MOTOR)
    assy.add(pump_holder(), name="tinta_soporte_bombas", color=PRINTED)
    for c, y in zip(P.INK_COLORS, subtank_ys()):
        assy.add(pump(y), name=f"tinta_bomba_{c}", color=MOTOR)
    assy.add(driver_box(), name="tinta_caja_driver", color=PRINTED_ALT)
    assy.add(subtank_rack(), name="tinta_soporte_subdepositos", color=PRINTED)
    for c, y in zip(P.INK_COLORS, subtank_ys()):
        body, cap = subtank(y)
        assy.add(body, name=f"tinta_subdeposito_{c}", color=INK_COLOR[c])
        assy.add(cap, name=f"tinta_flotador_{c}", color=MOTOR)
    for name, shape in tubes():
        assy.add(shape, name=name, color=TUBE)
    for i, (y, z) in enumerate(CLIP_POINTS):
        assy.add(tube_clip(y, z), name=f"tinta_clip_tubos_{i}", color=PRINTED)
