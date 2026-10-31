"""Fase 0.2 - Chasis.

Dos placas laterales de aluminio de 10 mm atornilladas a un bastidor inferior
de perfil 4040. Entre las placas van, atornillados a la testa de cada perfil
(rosca M8 en el taladro central): la viga X 4080, el tirante superior trasero
y los dos travesaños que sostienen la mesa.

Las placas llevan todos los agujeros de alineación (viga, rodillo de arrastre,
guía trasera, ejes de los rollos), así que su precisión fija la de la máquina.
"""
import math

import cadquery as cq

import params as P
import yfeed
from lib import ALU, BEAM, PLATE, RUBBER, STEEL, corner_bracket, leveling_foot, profile

Y0, Y1 = P.FRAME_Y
Z0, Z1 = P.FRAME_Z
PR = P.PROFILE
XL, XR = P.BEAM_X0, P.BEAM_X1        # caras interiores de las placas
BEAM_YC = (P.BEAM_Y_BACK + P.BEAM_Y_FRONT) / 2


def _roll_slot(sk, seat, edge_y, toward):
    """Ranura abierta para el eje de un rollo: entra desde el borde de la placa
    subiendo ROLL_SLOT_RISE grados, para que el eje caiga a su asiento."""
    sy, sz = seat
    run = abs(edge_y - sy) + 15
    rise = run * math.tan(math.radians(P.ROLL_SLOT_RISE))
    ey, ez = sy + toward * run, sz + rise
    angle = math.degrees(math.atan2(ez - sz, ey - sy))
    mid = ((sy + ey) / 2, (sz + ez) / 2)
    return (sk.push([mid])
            .slot(math.hypot(ey - sy, ez - sz), P.ROLL_SHAFT_D + 1, angle=angle, mode="s")
            .reset())


def side_plate_sketch():
    """Contorno y agujeros de la placa lateral en coordenadas (Y, Z)."""
    sk = (cq.Sketch()
          .push([((Y0 + Y1) / 2, (Z0 + Z1) / 2)]).rect(Y1 - Y0, Z1 - Z0).reset()
          .vertices().fillet(P.PLATE_FILLET).reset())

    m8 = [
        # Largueros laterales del bastidor (tornillo + tuerca en T en la ranura)
        (Y0 + 60, Z0 + PR / 2), ((Y0 + Y1) / 2, Z0 + PR / 2), (Y1 - 60, Z0 + PR / 2),
        # Viga X 4080 (dos taladros de testa)
        (BEAM_YC, P.BEAM_Z_BOTTOM + 20), (BEAM_YC, P.BEAM_Z_BOTTOM + 60),
        # Tirante superior trasero
        (Y0 + PR / 2, Z1 - PR / 2),
    ] + [(y, P.PLATEN_RAIL_Z) for y in P.PLATEN_RAIL_Y]
    sk = sk.push(m8).circle(P.M8_CLEAR / 2, mode="s").reset()

    sk = (sk.push([(P.REAR_GUIDE_Y, -P.REAR_GUIDE_D / 2)])
          .circle(P.M6_CLEAR / 2, mode="s").reset())
    sk = (sk.push([(P.GRIT_ROLLER_Y, -P.GRIT_ROLLER_D / 2)])
          .circle(P.GRIT_BEARING_OD / 2, mode="s").reset())

    # Eje de levante de la presión y soporte del motor Y (en ambas placas: el
    # motor se puede montar a cualquier lado)
    for y, z, d in yfeed.plate_holes():
        sk = sk.push([(y, z)]).circle(d / 2, mode="s").reset()

    sk = _roll_slot(sk, P.UNWIND_ROLL, Y0, -1)
    sk = _roll_slot(sk, P.TAKEUP_ROLL, Y1, +1)
    return sk


def side_plate(side):
    plate = cq.Workplane("YZ").placeSketch(side_plate_sketch()).extrude(P.SIDE_PLATE_T)
    x = XL - P.SIDE_PLATE_T if side == "izq" else XR
    return plate.translate((x, 0, 0))


def cut_list():
    """(nombre, sección, longitud, cantidad, notas)"""
    inner = P.BEAM_LENGTH - 2 * PR
    return [
        ("Larguero lateral", "4040", Y1 - Y0, 2, "tuercas en T para placa y patas"),
        ("Larguero delantero/trasero", "4040", inner, 2, "unión con escuadras"),
        ("Travesaño central", "4040", inner, 1, "unión con escuadras"),
        ("Travesaño de mesa", "4040", P.BEAM_LENGTH, 2, "roscar M8 en ambas testas"),
        ("Tirante superior trasero", "4040", P.BEAM_LENGTH, 1, "roscar M8 en ambas testas"),
        ("Viga X", "4080", P.BEAM_LENGTH, 1, "roscar M8 x2 en cada testa; corte a escuadra ±0,1"),
    ]


def add(assy):
    zc = Z0 + PR / 2
    inner_x0 = XL + PR
    inner = P.BEAM_LENGTH - 2 * PR

    assy.add(side_plate("izq"), name="placa_izq", color=PLATE)
    assy.add(side_plate("der"), name="placa_der", color=PLATE)

    # Bastidor inferior: largueros laterales pegados a las placas
    assy.add(profile("y", Y1 - Y0, Y0, (XL + PR / 2, zc)), name="larguero_izq", color=ALU)
    assy.add(profile("y", Y1 - Y0, Y0, (XR - PR / 2, zc)), name="larguero_der", color=ALU)
    rails_y = {"larguero_tras": Y0 + PR / 2, "travesano_central": 0, "larguero_del": Y1 - PR / 2}
    for name, y in rails_y.items():
        assy.add(profile("x", inner, inner_x0, (y, zc)), name=name, color=ALU)

    # Escuadras interiores del bastidor
    n = 0
    for y in rails_y.values():
        for x, dx in ((inner_x0, 1), (XR - PR, -1)):
            for dy in (-1, 1):
                if (y == Y0 + PR / 2 and dy < 0) or (y == Y1 - PR / 2 and dy > 0):
                    continue
                origin = (x, y + dy * PR / 2, zc)
                assy.add(corner_bracket(origin, (dx, 0, 0), (0, dy, 0)),
                         name=f"escuadra_{n}", color=STEEL)
                n += 1

    # Perfiles entre placas
    assy.add(profile("x", P.BEAM_LENGTH, XL, (BEAM_YC, P.BEAM_Z_BOTTOM + 40), size=(1, 2)),
             name="viga_x", color=BEAM)
    assy.add(profile("x", P.BEAM_LENGTH, XL, (Y0 + PR / 2, Z1 - PR / 2)),
             name="tirante_sup", color=ALU)
    for i, y in enumerate(P.PLATEN_RAIL_Y):
        assy.add(profile("x", P.BEAM_LENGTH, XL, (y, P.PLATEN_RAIL_Z)),
                 name=f"travesano_mesa_{i}", color=ALU)

    # Patas niveladoras bajo los largueros laterales
    for i, (x, y) in enumerate([(XL + PR / 2, Y0 + 30), (XL + PR / 2, Y1 - 30),
                                (XR - PR / 2, Y0 + 30), (XR - PR / 2, Y1 - 30)]):
        assy.add(leveling_foot(x, y, Z0, stem=P.FOOT_H - 8), name=f"pata_{i}", color=RUBBER)


def export(out):
    """DXF de la placa lateral (para corte) y lista de corte de perfiles."""
    face = cq.Workplane("XY").placeSketch(side_plate_sketch()).extrude(P.SIDE_PLATE_T).section()
    cq.exporters.export(face, str(out / "placa_lateral.dxf"))

    rows = cut_list()
    with open(out / "lista_corte.csv", "w", encoding="utf-8") as f:
        f.write("pieza;seccion;longitud_mm;cantidad;notas\n")
        for name, sec, length, qty, notes in rows:
            f.write(f"{name};{sec};{length:.1f};{qty};{notes}\n")

    print("\nLista de corte")
    for name, sec, length, qty, notes in rows:
        print(f"  {qty} x {sec} {length:7.1f} mm  {name} ({notes})")
    print(f"  2 x placa aluminio {P.SIDE_PLATE_T} mm, {Y1 - Y0} x {Z1 - Z0} mm (placa_lateral.dxf)")
