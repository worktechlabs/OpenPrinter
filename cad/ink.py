"""Compartimento de tinta, por fuera de la placa izquierda.

Caja cerrada para proteger la tinta del polvo y la luz:
- Marco de perfil V-slot 2020 (del inventario), atornillado a la placa lateral
  con M5 y tuercas en T.
- Paneles: delantero y trasero de MDF de 6 mm, exterior de metacrilato para
  ver los niveles y tapa abatible para rellenar.
- Bandeja impresa con alojamientos para 4 depósitos de color (C, M, Y, K) y uno
  de blanco más ancho, sobre un agitador magnético para que el dióxido de
  titanio no se deposite.
- Los tubos salen por la tapa, suben pegados a la placa con clips impresos y
  entran por el agujero trasero hasta la bandeja de la cadena portacables.

El nivel medio de la tinta queda unos 40 mm por debajo de las boquillas. La
regulación fina de presión (subdepósitos o bomba) es de la fase 4.
"""
import cadquery as cq

import params as P
from lib import ALU, PRINTED, PRINTED_ALT, RUBBER, box, profile, rod_x, rod_y, rod_z

X_IN = P.BEAM_X0 - P.SIDE_PLATE_T          # cara exterior de la placa izquierda
X_OUT = X_IN - P.INK_BOX_DEPTH
Y0, Y1 = P.INK_BOX_Y
Z0, Z1 = P.INK_BOX_Z
S = 20                                     # perfil 2020
PT = P.INK_PANEL_T
TRAY_T = 5
TRAY_Z = Z0 + S                            # cara superior de los largueros inferiores
TUBE_D = 10                                # mazo de 5 tubos de tinta con espiral

INK_COLOR = {
    "C": cq.Color(0.0, 0.62, 0.86, 0.75),
    "M": cq.Color(0.85, 0.1, 0.55, 0.75),
    "Y": cq.Color(0.98, 0.85, 0.1, 0.75),
    "K": cq.Color(0.12, 0.12, 0.12, 0.85),
    "W": cq.Color(0.97, 0.97, 0.97, 0.9),
}
ACRYLIC = cq.Color(0.80, 0.90, 0.95, 0.30)
MDF = cq.Color(0.72, 0.60, 0.45, 1)


def frame():
    """Perfiles 2020: 4 montantes, 4 largueros en Y y 4 travesaños en X."""
    parts = []
    xs = (X_IN - S / 2, X_OUT + S / 2)
    ys = (Y0 + S / 2, Y1 - S / 2)
    for x in xs:
        for y in ys:
            parts.append(profile("z", Z1 - Z0, Z0, (x, y), pitch=20))
    for x in xs:
        for z in (Z0 + S / 2, Z1 - S / 2):
            parts.append(profile("y", Y1 - Y0 - 2 * S, Y0 + S, (x, z), pitch=20))
    for y in ys:
        for z in (Z0 + S / 2, Z1 - S / 2):
            parts.append(profile("x", P.INK_BOX_DEPTH - 2 * S, X_OUT + S, (y, z), pitch=20))
    return parts


def cut_list():
    """(nombre, sección, longitud, cantidad)"""
    return [
        ("Montante del compartimento de tinta", "2020 V-slot", Z1 - Z0, 4),
        ("Larguero del compartimento de tinta", "2020 V-slot", Y1 - Y0 - 2 * S, 4),
        ("Travesaño del compartimento de tinta", "2020 V-slot", P.INK_BOX_DEPTH - 2 * S, 4),
    ]


def plate_holes():
    """M5 de los montantes interiores a la placa, y paso de los tubos: (y, z, d)."""
    holes = [(y, z, P.M5_CLEAR) for y in (Y0 + S / 2, Y1 - S / 2) for z in (Z0 + 30, Z1 - 30)]
    y, z, d = P.INK_TUBE_HOLE
    return holes + [(y, z, d)]


def _tank_slots():
    """(color, y0, y1) de cada depósito a lo largo de Y, centrados en la bandeja."""
    widths = [P.INK_TANK_WHITE[1] if c == "W" else P.INK_TANK[1] for c in P.INK_COLORS]
    gap = 4
    total = sum(widths) + gap * (len(widths) - 1)
    y = (Y0 + Y1) / 2 - total / 2
    out = []
    for c, w in zip(P.INK_COLORS, widths):
        out.append((c, y, y + w))
        y += w + gap
    return out


def tank_x():
    tx = P.INK_TANK[0]
    xc = (X_IN + X_OUT) / 2
    return xc - tx / 2, xc + tx / 2


def tray():
    """Bandeja impresa con alojamientos de 3 mm para los depósitos."""
    body = box(X_OUT + 2, X_IN - 2, Y0 + 1, Y1 - 1, TRAY_Z, TRAY_Z + TRAY_T)   # apoya en todos los perfiles
    for x0c, x1c in ((X_IN - S - 0.5, X_IN), (X_OUT, X_OUT + S + 0.5)):       # rebajes de los montantes
        for y0c, y1c in ((Y0, Y0 + S + 0.5), (Y1 - S - 0.5, Y1)):
            body = body.cut(box(x0c - 1, x1c + 1, y0c - 1, y1c + 1, TRAY_Z - 1, TRAY_Z + TRAY_T + 1))
    x0, x1 = tank_x()
    for c, y0, y1 in _tank_slots():
        if c == "W":
            continue                       # el blanco va sobre el agitador
        body = body.cut(box(x0 - 1, x1 + 1, y0 - 1, y1 + 1, TRAY_Z + TRAY_T - 3, TRAY_Z + TRAY_T + 1))
    return body


def tanks():
    out = []
    x0, x1 = tank_x()
    base = TRAY_Z + TRAY_T - 3
    for c, y0, y1 in _tank_slots():
        if c == "W":
            stirrer = box(x0 - 2, x1 + 2, y0 - 2, y1 + 2, TRAY_Z + TRAY_T, TRAY_Z + TRAY_T + P.INK_STIRRER_H)
            out.append(("tinta_agitador", stirrer, RUBBER))
            z0, h = TRAY_Z + TRAY_T + P.INK_STIRRER_H, P.INK_TANK_WHITE[2]
        else:
            z0, h = base, P.INK_TANK[2]
        tank = box(x0, x1, y0, y1, z0, z0 + h)
        cap = rod_z(z0 + h, z0 + h + 8, (x0 + x1) / 2, (y0 + y1) / 2, 16)
        out.append((f"tinta_deposito_{c}", tank.union(cap), INK_COLOR[c]))
    return out


def panels():
    """Paneles: delantero y trasero (MDF), exterior (metacrilato) y tapa (MDF)."""
    return [
        ("tinta_panel_delantero", box(X_OUT, X_IN, Y1, Y1 + PT, Z0, Z1), MDF),
        ("tinta_panel_trasero", box(X_OUT, X_IN, Y0 - PT, Y0, Z0, Z1), MDF),
        ("tinta_panel_exterior", box(X_OUT - 3, X_OUT, Y0 - PT, Y1 + PT, Z0, Z1), ACRYLIC),
        ("tinta_tapa", box(X_OUT - 3, X_IN, Y0 - PT, Y1 + PT, Z1, Z1 + PT)
         .cut(rod_z(Z1 - 1, Z1 + PT + 1, X_IN - 25, Y0 + S + 10, TUBE_D + 4)), MDF),
    ]


def tube_path():
    """Mazo de tubos desde la tapa hasta el agujero de la placa (cilindros)."""
    ty, tz, _ = P.INK_TUBE_HOLE
    x = X_IN - 25
    xp = X_IN - TUBE_D / 2 - 2               # pegado a la placa
    z_top = 130
    y_lid = Y0 + S + 10                      # por delante del travesaño superior trasero
    segs = [
        rod_z(Z1 - 10, z_top, x, y_lid, TUBE_D),
        rod_x(x, xp, y_lid, z_top, TUBE_D),
        rod_y(ty, y_lid, xp, z_top, TUBE_D),
        rod_z(tz, z_top, xp, ty, TUBE_D),
        rod_x(xp, X_IN + P.SIDE_PLATE_T + 20, ty, tz, TUBE_D),
    ]
    body = segs[0]
    for s in segs[1:]:
        body = body.union(s)
    return body


def tube_clip(y, z):
    """Clip impreso para el mazo de tubos, atornillado a la placa (tornillo para madera)."""
    x0 = X_IN - TUBE_D - 6
    body = box(x0, X_IN, y - 8, y + 8, z - TUBE_D / 2 - 4, z + TUBE_D / 2 + 4)
    body = body.cut(rod_y(y - 9, y + 9, X_IN - TUBE_D / 2 - 2, z, TUBE_D + 0.5))
    return body.cut(rod_x(x0 - 1, X_IN + 1, y, z + TUBE_D / 2 + 1, 3.5))


CLIP_POINTS = [(-90, 130), (-160, 130)]     # sobre el tramo horizontal del mazo


def printed_parts():
    return {"tinta_bandeja": tray(), "tinta_clip_tubos": tube_clip(*CLIP_POINTS[0])}


def add(assy):
    for i, prof in enumerate(frame()):
        assy.add(prof, name=f"tinta_perfil_{i}", color=ALU)
    assy.add(tray(), name="tinta_bandeja", color=PRINTED_ALT)
    for name, shape, color in tanks():
        assy.add(shape, name=name, color=color)
    for name, shape, color in panels():
        assy.add(shape, name=name, color=color)
    assy.add(tube_path(), name="tinta_tubos", color=cq.Color(0.9, 0.9, 0.9, 0.8))
    for i, (y, z) in enumerate(CLIP_POINTS):
        assy.add(tube_clip(y, z), name=f"tinta_clip_tubos_{i}", color=PRINTED)
