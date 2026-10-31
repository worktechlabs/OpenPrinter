"""Ensamblaje general de la máquina.

Combina los módulos ya detallados (chasis, viga X, carro, mesa, arrastre, rollos, servicio) con los volúmenes del esqueleto de
distribución (fase 0.1) de los que aún no lo están. Genera out/layout.step,
out/layout.glb y las salidas de fabricación de cada módulo.
"""
from pathlib import Path

import cadquery as cq

import carriage
import chassis
import ink
import motion
import params as P
import platen
import rolls
import service
import wiring
import xaxis
import yfeed
from lib import ENVELOPE, FILM, box, strip_yz

OUT = Path(__file__).resolve().parent.parent / "out"


def x_axis(assy, carriage_x):
    xaxis.add(assy)
    carriage.add(assy, carriage_x)
    motion.add(assy, carriage_x)
    # Envolvente de recorrido del carro
    hw = P.CARRIAGE_W / 2
    assy.add(box(P.CARRIAGE_X_MIN - hw, P.CARRIAGE_X_MAX + hw, P.BEAM_Y_FRONT, P.SHELF_FRONT_Y,
                 P.HEAD_GAP, P.CARRIAGE_TOP_Z), name="envolvente_carro", color=ENVELOPE)


def media_path(assy):
    platen.add(assy)
    yfeed.add(assy)
    rolls.add(assy)
    service.add(assy)
    ink.add(assy)
    wiring.add(assy)
    fw = P.FILM_WIDTH
    # Elevado 0,3 mm para que no coincida con la cara de la mesa en los renders
    film = strip_yz(rolls.film_path(), -fw / 2, fw / 2).translate((0, 0, 0.3))
    assy.add(film, name="film", color=FILM)


def build(carriage_x=0.0):
    assy = cq.Assembly(name="openprinter_layout")
    chassis.add(assy)
    x_axis(assy, carriage_x)
    media_path(assy)
    return assy


def export_printed(folder):
    """STL de todas las piezas impresas, en la posición del carro x = 0."""
    folder.mkdir(exist_ok=True)
    parts = {**xaxis.printed_parts(), **carriage.printed_parts(),
             **platen.printed_parts(), **yfeed.printed_parts(),
             **rolls.printed_parts(), **service.printed_parts(), **motion.printed_parts(),
             **ink.printed_parts(), **wiring.printed_parts()}
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
    platen.export(OUT)
    export_printed(OUT / "stl")
    P.summary()
    print("Exportado:", OUT / "layout.step", OUT / "layout.glb")


if __name__ == "__main__":
    main()
