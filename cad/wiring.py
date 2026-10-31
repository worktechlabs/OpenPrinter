"""Electrónica, fuente, paneles de mando y canaletas de cables.

- Bandeja inferior de MDF de 10 mm de lado a lado, apoyada en los dos largueros
  laterales y en el travesaño central, bajo la mesa de vacío.
- Encima: la fuente de 24 V (a la derecha) y una caja impresa con la SKR Mini
  E3 V3.0, la Raspberry Pi 3, el Pico y los convertidores (a la izquierda), con
  dos ventiladores 4010 en la tapa.
- Panel trasero con la entrada de red IEC (interruptor y fusible) y panel
  delantero con la seta de emergencia.
- Pantalla táctil de 7" (KlipperScreen por HDMI + USB a la Raspberry Pi) en la
  esquina delantera derecha, inclinada hacia atrás, en una carcasa impresa
  atornillada a la cara interior de la placa derecha.
- Canaletas impresas con tapa: una a lo largo del borde trasero de la bandeja y
  otras por encima de los largueros laterales y por la cara interior de las
  placas, hasta la bandeja de la cadena portacables (carro, motor X, tinta), el
  motor Y y el encoder Y. Los cables de sensores sueltos van por las ranuras de
  los perfiles con tapas de ranura.
"""
import cadquery as cq

import params as P
from lib import ALU, MOTOR, PLATEN, PRINTED, PRINTED_ALT, box, rod_x, rod_y, rod_z

XL, XR = P.BEAM_X0, P.BEAM_X1
Y0F, Y1F = P.FRAME_Y
PR = P.PROFILE
Z_RAIL_TOP = P.FRAME_Z[0] + PR                 # cara superior de los largueros inferiores
PX0, PX1, PY0, PY1 = P.ELEC_PLATE
ZT = Z_RAIL_TOP + P.ELEC_PLATE_T               # cara superior de la bandeja
DW, DH = P.CABLE_DUCT
WALL = 2.5

# Caja de la electrónica (izquierda) y fuente (derecha)
BOX = (-275, -40, -35, 95, ZT, ZT + 50)        # X0, X1, Y0, Y1, Z0, Z1
PSU_X0 = -15
PSU_Y0 = -30                                   # deja paso a la canaleta trasera y a las bridas
COMPONENTS = {                                 # nombre: (x0, y0, ancho X, fondo Y, alto, color)
    "placa_skr": (-262, -30, P.SKR_SIZE[0], P.SKR_SIZE[1], 22, PRINTED_ALT),
    "raspberry_pi": (-152, -28, P.PI_SIZE[0], P.PI_SIZE[1], 20, PRINTED_ALT),
    "pico_encoder": (-152, 38, 51, 21, 4, PRINTED_ALT),
    "conversor_5v": (-92, 38, 45, 25, 15, MOTOR),
    "conversor_12v": (-92, 66, 45, 25, 15, MOTOR),
}
FAN_XS = (-215, -110)
FAN_Y = 30

# Canaletas: (nombre, x0, x1, y0, y1, z0, z1)
_ZD = (Z_RAIL_TOP, Z_RAIL_TOP + DH)
_ZDP = (ZT, ZT + DH)
DUCTS = [
    ("trasera_bandeja", PX0 + 5, PX1 - 5, PY0 + 2, PY0 + 2 + DW, *_ZDP),
    ("larguero_izq", XL + 2, XL + 2 + DW, Y0F + 20, PY0, *_ZD),
    ("larguero_der", XR - 2 - DW, XR - 2, PY0 - 50, PY0, *_ZD),
    ("larguero_der_delante", XR - 2 - DW, XR - 2, PY1, Y1F - PR - 5, *_ZD),
    ("larguero_tras", XL + 2 + DW, -470, Y0F + PR / 2 - DW / 2, Y0F + PR / 2 + DW / 2, *_ZD),
    ("larguero_del", 470, XR - 2 - DW, Y1F - PR / 2 - DW / 2, Y1F - PR / 2 + DW / 2, *_ZD),
    # Verticales por la cara interior de las placas
    ("vertical_cadena", XL, XL + DH, -185, -185 + DW - 3, Z_RAIL_TOP + DH, P.RAIL_Z[0] + 32),
    ("vertical_encoder_y", XL, XL + DH - 3, -92, -82, Z_RAIL_TOP + DH, -60),
    ("vertical_motor_y", XR - DH, XR, -108, -92, Z_RAIL_TOP + DH, -140),
    ("vertical_pantalla", XR - DH, XR, 266, 266 + DW - 3, Z_RAIL_TOP + DH, -2),
]

# Pantalla: carcasa en coordenadas locales (Y hacia la cara, Z hacia arriba) que
# luego se inclina SCREEN_TILT grados alrededor del borde inferior trasero.
SW, SH, SD = P.SCREEN_SIZE
CASE = (SW + 12, SD + 6, SH + 12)              # X, Y, Z
CASE_X1 = XR - 9                               # deja sitio al soporte
CASE_X0 = CASE_X1 - CASE[0]
PIVOT = (Y1F, 10)                              # (Y, Z) del borde inferior trasero
FLANGE = (255, Y1F, 0, 118)                    # pletina en la placa: Y0, Y1, Z0, Z1


def plate_holes():
    """Pasos de cable (motor Y y encoder Y) y M5 del soporte de la pantalla (y, z, d)."""
    return [(-100, -150, 14), (-87, -60, 8)] + [(y, z, P.M5_CLEAR) for y, z in screen_screws()]


def screen_screws():
    y0, y1, z0, z1 = FLANGE
    return [(y0 + 12, z0 + 12), (y1 - 12, z0 + 12), (y0 + 12, z1 - 12)]


def _tilt(shape):
    """Pasa de coordenadas locales de la pantalla a las de la máquina."""
    py, pz = PIVOT
    return shape.rotate((0, 0, 0), (1, 0, 0), P.SCREEN_TILT).translate((0, py, pz))


def screen_case():
    """Carcasa impresa: bandeja con marco delantero; la pantalla entra por detrás."""
    w, d, h = CASE
    body = box(CASE_X0, CASE_X1, 0, d, 0, h)
    body = body.cut(box(CASE_X0 + 3, CASE_X1 - 3, -1, d - 3, 3, h - 3))           # alojamiento
    body = body.cut(box(CASE_X0 + 9, CASE_X1 - 9, d - 4, d + 1, 9, h - 9))         # ventana
    # Brazo trasero que llega a la pletina de la placa
    arm = box(CASE_X1 - 30, XR - 6, -60, 0, 15, h - 15)
    return _tilt(body.union(arm))


def screen_bracket():
    """Pletina impresa en la cara interior de la placa derecha; el brazo de la
    carcasa se atornilla a ella con 2 M4."""
    y0, y1, z0, z1 = FLANGE
    body = box(XR - 6, XR, y0, y1, z0, z1)
    for y, z in screen_screws():
        body = body.cut(rod_x(XR - 7, XR + 1, y, z, P.M5_CLEAR))
    return body


def screen():
    w, d, h = CASE
    return _tilt(box(CASE_X0 + 4, CASE_X1 - 4, 3, d - 3, 4, h - 4))


def tray():
    plate = box(PX0, PX1, PY0, PY1, Z_RAIL_TOP, ZT)
    # M5 a tuercas en T: dos en cada larguero lateral y dos en el travesaño central
    screws = [(x, y) for x in (XL + PR / 2, XR - PR / 2) for y in (PY0 + 25, PY1 - 25)]
    screws += [(-300, 0), (230, 0)]
    for x, y in screws:
        plate = plate.cut(rod_z(Z_RAIL_TOP - 1, ZT + 1, x, y, P.M5_CLEAR))
    return plate


def electronics_box():
    x0, x1, y0, y1, z0, z1 = BOX
    body = box(x0, x1, y0, y1, z0, z1).cut(box(x0 + WALL, x1 - WALL, y0 + WALL, y1 - WALL, z0 - 1, z1 - WALL))
    for x in FAN_XS:
        body = body.cut(rod_z(z1 - WALL - 1, z1 + 1, x, FAN_Y, 37))
        for dx in (-16, 16):
            for dy in (-16, 16):
                body = body.cut(rod_z(z1 - WALL - 1, z1 + 1, x + dx, FAN_Y + dy, 3.2))
    # Salidas de cables: hacia la canaleta trasera y hacia la fuente
    body = body.cut(box(x0 + 20, x1 - 20, y0 - 1, y0 + WALL + 1, z0 - 1, z0 + 14))
    body = body.cut(box(x1 - WALL - 1, x1 + 1, -20, 40, z0 - 1, z0 + 20))
    # Rejilla de ventilación en el frente
    for i in range(10):
        x = x0 + 25 + i * 18
        body = body.cut(box(x, x + 6, y1 - WALL - 1, y1 + 1, z0 + 15, z1 - 12))
    return body


def components():
    out = []
    for name, (x0, y0, w, d, h, color) in COMPONENTS.items():
        out.append((f"electronica_{name}", box(x0, x0 + w, y0, y0 + d, ZT + 6, ZT + 6 + h), color))
    psu = box(PSU_X0, PSU_X0 + P.PSU_SIZE[0], PSU_Y0, PSU_Y0 + P.PSU_SIZE[1], ZT, ZT + P.PSU_SIZE[2])
    out.append(("electronica_fuente_24v", psu, ALU))
    _, _, _, _, _, z1 = BOX
    for i, x in enumerate(FAN_XS):
        out.append((f"electronica_ventilador_{i}", box(x - 20, x + 20, FAN_Y - 20, FAN_Y + 20, z1, z1 + 10), MOTOR))
    return out


def psu_clamp(x):
    """Brida impresa para la fuente: abraza un extremo y se atornilla a la bandeja."""
    y0, y1 = PSU_Y0 - 6, PSU_Y0 + P.PSU_SIZE[1] + 6
    h = P.PSU_SIZE[2]
    body = box(x - 6, x + 6, y0, y1, ZT, ZT + h + 4)
    body = body.cut(box(x - 7, x + 7, PSU_Y0, PSU_Y0 + P.PSU_SIZE[1], ZT - 1, ZT + h))
    for y in (y0 + 3, y1 - 3):
        body = body.cut(rod_z(ZT - 1, ZT + h + 5, x, y, 4.5))
    return body


def duct(x0, x1, y0, y1, z0, z1):
    """Canaleta en U con tapa (sólido simplificado), en tramos imprimibles."""
    return box(x0, x1, y0, y1, z0, z1)


def iec_panel():
    """Panel trasero con la entrada IEC C14 (interruptor + fusible), sobre el larguero trasero."""
    x0, x1 = -470, -400
    y = Y0F
    panel = box(x0, x1, y - 4, y + 2, Z_RAIL_TOP, Z_RAIL_TOP + 60)
    foot = box(x0, x1, y + 2, y + PR, Z_RAIL_TOP, Z_RAIL_TOP + 4)
    body = panel.union(foot).cut(box(-459, -411, y - 5, y + 3, Z_RAIL_TOP + 16, Z_RAIL_TOP + 44))
    for x in (x0 + 8, x1 - 8):
        body = body.cut(rod_z(Z_RAIL_TOP - 1, Z_RAIL_TOP + 5, x, y + PR / 2, P.M5_CLEAR))
    return body


def estop_panel():
    """Panel delantero con la seta de emergencia, sobre el larguero delantero."""
    x0, x1 = 400, 470
    y = Y1F
    panel = box(x0, x1, y - 2, y + 4, Z_RAIL_TOP, Z_RAIL_TOP + 60)
    foot = box(x0, x1, y - PR, y - 2, Z_RAIL_TOP, Z_RAIL_TOP + 4)
    body = panel.union(foot).cut(rod_y(y - 3, y + 5, (x0 + x1) / 2, Z_RAIL_TOP + 32, 22.5))
    for x in (x0 + 8, x1 - 8):
        body = body.cut(rod_z(Z_RAIL_TOP - 1, Z_RAIL_TOP + 5, x, y - PR / 2, P.M5_CLEAR))
    return body


def duct_length():
    return sum(max(x1 - x0, y1 - y0, z1 - z0) for _, x0, x1, y0, y1, z0, z1 in DUCTS)


def printed_parts():
    return {
        "electronica_caja": electronics_box(),
        "electronica_brida_fuente": psu_clamp(PSU_X0),
        "panel_iec": iec_panel(),
        "panel_seta": estop_panel(),
        "canaleta_tramo_200": duct(0, 200, 0, DW, 0, DH),
        "pantalla_carcasa": screen_case(),
        "pantalla_soporte": screen_bracket(),
    }


def add(assy):
    assy.add(tray(), name="electronica_bandeja", color=PLATEN)
    assy.add(electronics_box(), name="electronica_caja", color=PRINTED)
    for name, shape, color in components():
        assy.add(shape, name=name, color=color)
    for i, x in enumerate((PSU_X0 + 6, PSU_X0 + P.PSU_SIZE[0] - 6)):
        assy.add(psu_clamp(x), name=f"electronica_brida_fuente_{i}", color=PRINTED)
    assy.add(iec_panel(), name="panel_iec", color=PRINTED)
    assy.add(box(-459, -411, Y0F + 2, Y0F + 32, Z_RAIL_TOP + 16, Z_RAIL_TOP + 44),
             name="panel_iec_conector", color=MOTOR)
    assy.add(estop_panel(), name="panel_seta", color=PRINTED)
    cx = 435
    assy.add(rod_y(Y1F + 4, Y1F + 30, cx, Z_RAIL_TOP + 32, 40), name="panel_seta_pulsador",
             color=cq.Color(0.85, 0.1, 0.1, 1))
    for name, *dims in DUCTS:
        assy.add(duct(*dims), name=f"canaleta_{name}", color=PRINTED_ALT)
    assy.add(screen_case(), name="pantalla_carcasa", color=PRINTED)
    assy.add(screen_bracket(), name="pantalla_soporte", color=PRINTED)
    assy.add(screen(), name="pantalla_tactil", color=MOTOR)
