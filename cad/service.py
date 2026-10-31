"""Fase 0.8 - Estación de servicio y tinta (base y volúmenes reservados).

En la fase 0 solo se fija dónde va y cómo se sujeta: una base impresa
atornillada a los dos travesaños de mesa, a la derecha del film, bajo el carro
aparcado en home. El mecanismo (tapas que suben a sellar los cabezales,
limpiador, bomba de purga) se diseña en la fase 4; aquí solo se reservan sus
volúmenes para que nada más los invada.

También se reserva el rack de tanques de tinta, por fuera de la placa izquierda:
se rellena desde fuera, se ve el nivel y la tinta queda por debajo de las
boquillas. Los tubos entran por un agujero de la placa y suben al carro por la
cadena portacables.
"""
import params as P
from lib import PRINTED_ALT, RESERVED, RUBBER, box, rod_z

X0, X1 = P.SERVICE_X0, P.SERVICE_X1
BASE_Z = (-P.PLATEN_DEPTH, -P.PLATEN_DEPTH + 6)
BASE_Y = (P.PLATEN_RAIL_Y[0] - 10, P.PLATEN_RAIL_Y[1] + 10)
CAP_DROP = 5                       # tapas bajadas: 5 mm por debajo de las boquillas


def home_head_xs():
    first = P.CARRIAGE_HOME_X - (P.HEAD_COUNT - 1) * P.HEAD_PITCH_X / 2
    return [first + i * P.HEAD_PITCH_X for i in range(P.HEAD_COUNT)]


def base():
    body = box(X0, X1, *BASE_Y, *BASE_Z)
    for ry in P.PLATEN_RAIL_Y:
        for x in (X0 + 15, X1 - 15):
            body = body.cut(rod_z(BASE_Z[0] - 1, BASE_Z[1] + 1, x, ry, P.M5_CLEAR))
    # Paso para el tubo de desecho hacia la bomba
    return body.cut(rod_z(BASE_Z[0] - 1, BASE_Z[1] + 1, (X0 + X1) / 2, 30, 12))


def plate_holes():
    """Paso de los tubos de tinta en las placas laterales: (y, z, d)."""
    y, z, d = P.INK_TUBE_HOLE
    return [(y, z, d)]


def printed_parts():
    return {"servicio_base": base()}


def add(assy):
    assy.add(base(), name="servicio_base", color=PRINTED_ALT)
    hx, hy, _ = P.HEAD_SIZE
    top = P.HEAD_GAP - CAP_DROP
    for i, x in enumerate(home_head_xs()):
        assy.add(box(x - hx / 2 - 2, x + hx / 2 + 2, -hy / 2 - 2, hy / 2 + 2, top - 8, top),
                 name=f"servicio_tapa_{i}", color=RUBBER)
    xs = home_head_xs()
    assy.add(box(xs[0] - 30, xs[-1] + 30, -30, 30, BASE_Z[1], top - 8),
             name="reserva_servicio_elevador", color=RESERVED)
    # Limpiador: a la izquierda de las tapas, el carro lo cruza al salir de home
    assy.add(box(X0 + 4, X0 + 10, -hy / 2 - 4, hy / 2 + 4, BASE_Z[1], top),
             name="reserva_servicio_limpiador", color=RESERVED)
    # Rack de tanques de tinta por fuera de la placa izquierda
    depth, (ry0, ry1), (rz0, rz1) = P.INK_RACK
    xo = P.BEAM_X0 - P.SIDE_PLATE_T - 20          # deja sitio a collarines y encoder Y
    assy.add(box(xo - depth, xo, ry0, ry1, rz0, rz1), name="reserva_tanques_tinta", color=RESERVED)
    # Bomba de purga y tubo, bajo la base entre los dos travesaños
    assy.add(box(X0 + 25, X1 - 25, P.PLATEN_RAIL_Y[0] + 25, P.PLATEN_RAIL_Y[1] - 25,
                 BASE_Z[0] - 50, BASE_Z[0]), name="reserva_servicio_bomba", color=RESERVED)
