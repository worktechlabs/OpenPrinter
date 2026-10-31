"""Ensamblaje general de la máquina.

Combina los módulos ya detallados (chasis, viga X, carro) con los volúmenes del esqueleto de
distribución (fase 0.1) de los que aún no lo están. Genera out/layout.step,
out/layout.glb y las salidas de fabricación de cada módulo.
"""
from pathlib import Path

import cadquery as cq

import carriage
import chassis
import params as P
import xaxis
from lib import ENVELOPE, FILM, PLATEN, RESERVED, ROLL, RUBBER, STEEL, box, rod_x, strip_yz

OUT = Path(__file__).resolve().parent.parent / "out"


def x_axis(assy, carriage_x):
    xaxis.add(assy)
    carriage.add(assy, carriage_x)
    # Envolvente de recorrido del carro
    hw = P.CARRIAGE_W / 2
    assy.add(box(P.CARRIAGE_X_MIN - hw, P.CARRIAGE_X_MAX + hw, P.BEAM_Y_FRONT, P.SHELF_FRONT_Y,
                 P.HEAD_GAP, P.CARRIAGE_TOP_Z), name="envolvente_carro", color=ENVELOPE)


def media_path(assy):
    xl, xr = P.BEAM_X0, P.BEAM_X1
    fw = P.FILM_WIDTH

    # Mesa de impresión con cámara de vacío
    px0, px1 = P.PLATEN_X
    py0, py1 = P.PLATEN_Y
    assy.add(box(px0, px1, py0, py1, -P.PLATEN_DEPTH, 0), name="mesa_vacio", color=PLATEN)
    # Mesa de entrada entre la guía trasera y el rodillo de arrastre
    r = P.GRIT_ROLLER_D / 2
    assy.add(box(px0, px1, P.REAR_GUIDE_Y + P.REAR_GUIDE_D / 2, P.GRIT_ROLLER_Y - r - 2, -4, 0),
             name="mesa_entrada", color=PLATEN)

    # Rodillo de arrastre (eje pasante a las placas) y rodillos de presión
    assy.add(rod_x(xl - P.SIDE_PLATE_T - 20, xr + P.SIDE_PLATE_T + 20,
                   P.GRIT_ROLLER_Y, -r, 12), name="eje_arrastre", color=STEEL)
    assy.add(rod_x(px0, px1, P.GRIT_ROLLER_Y, -r, P.GRIT_ROLLER_D),
             name="rodillo_arrastre", color=STEEL)
    n_pinch = 6
    for i in range(n_pinch):
        x = -fw / 2 + 30 + i * (fw - 60) / (n_pinch - 1)
        assy.add(rod_x(x - 10, x + 10, P.GRIT_ROLLER_Y, 8, 14), name=f"presion_{i}", color=RUBBER)
        assy.add(box(x - 6, x + 6, P.GRIT_ROLLER_Y - 8, P.GRIT_ROLLER_Y + 8, 15, P.BEAM_Z_BOTTOM),
                 name=f"palanca_presion_{i}", color=RESERVED)

    # Guía trasera
    assy.add(rod_x(xl, xr, P.REAR_GUIDE_Y, -P.REAR_GUIDE_D / 2, P.REAR_GUIDE_D),
             name="guia_trasera", color=STEEL)

    # Rollos: eje + film enrollado
    for name, (y, z), od in [("rollo_entrada", P.UNWIND_ROLL, P.FILM_ROLL_OD_MAX),
                             ("rollo_recogida", P.TAKEUP_ROLL, P.FILM_CORE_OD + 10)]:
        assy.add(rod_x(xl - P.SIDE_PLATE_T - 20, xr + P.SIDE_PLATE_T + 20, y, z, 25),
                 name=f"eje_{name}", color=STEEL)
        assy.add(rod_x(-fw / 2, fw / 2, y, z, od), name=name, color=ROLL)

    # Recorrido del film
    uy, uz = P.UNWIND_ROLL
    ty, tz = P.TAKEUP_ROLL
    path = [
        (uy, uz + P.FILM_ROLL_OD_MAX / 2),
        (P.REAR_GUIDE_Y - P.REAR_GUIDE_D / 2, -P.REAR_GUIDE_D / 2),
        (P.REAR_GUIDE_Y, 0),
        (py1, 0),
        (py1 + 40, -30),
        (ty, tz + (P.FILM_CORE_OD + 10) / 2),
    ]
    assy.add(strip_yz(path, -fw / 2, fw / 2), name="film", color=FILM)

    # Estación de servicio (solo volumen)
    assy.add(box(P.SERVICE_X0, P.SERVICE_X1, -40, 40, -60, 0),
             name="reserva_estacion_servicio", color=RESERVED)

    # Motor Y fuera de la placa derecha
    assy.add(box(xr + P.SIDE_PLATE_T, xr + P.SIDE_PLATE_T + 60,
                 P.GRIT_ROLLER_Y - 40, P.GRIT_ROLLER_Y + 40, -90, 10),
             name="reserva_motor_y", color=RESERVED)
    # Electrónica bajo la mesa
    assy.add(box(-280, 200, -60, 100, P.FRAME_Z[0] + P.PROFILE + 20,
                 P.PLATEN_RAIL_Z - P.PROFILE / 2 - 10),
             name="reserva_electronica", color=RESERVED)


def build(carriage_x=0.0):
    assy = cq.Assembly(name="openprinter_layout")
    chassis.add(assy)
    x_axis(assy, carriage_x)
    media_path(assy)
    return assy


def export_printed(folder):
    """STL de todas las piezas impresas, en la posición del carro x = 0."""
    folder.mkdir(exist_ok=True)
    parts = {**xaxis.printed_parts(), **carriage.printed_parts()}
    for name, part in parts.items():
        cq.exporters.export(part, str(folder / f"{name}.stl"), tolerance=0.05, angularTolerance=0.1)
        bb = part.val().BoundingBox()
        print(f"STL {name:<22} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:6.1f} mm")


def main():
    OUT.mkdir(exist_ok=True)
    assy = build()
    assy.export(str(OUT / "layout.step"))
    assy.export(str(OUT / "layout.glb"))
    chassis.export(OUT)
    export_printed(OUT / "stl")
    P.summary()
    print("Exportado:", OUT / "layout.step", OUT / "layout.glb")


if __name__ == "__main__":
    main()
