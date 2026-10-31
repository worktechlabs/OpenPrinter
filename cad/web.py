"""Modelo 3D para la web (docs/model/openprinter.glb).

Ensamblaje sin volúmenes reservados. La placa perforada de la mesa se sustituye
por una placa lisa: sus ~800 agujeros multiplicarían por dos el tamaño del GLB.
"""
from pathlib import Path

import cadquery as cq

import layout
import params as P
from lib import box

MODEL = Path(__file__).resolve().parent.parent / "docs" / "model"
CARRIAGE_X = -120            # carro en una posición intermedia, no en home


def build():
    src = layout.build(carriage_x=CARRIAGE_X)
    out = cq.Assembly(name="openprinter")
    for c in src.children:
        if c.name.startswith(("reserva", "envolvente")):
            continue
        obj = c.obj
        if c.name == "mesa_placa":
            obj = box(*P.PLATEN_X, *P.PLATEN_Y, -P.PLATEN_TOP_T, 0)
        out.add(obj, name=c.name, color=c.color)
    return out


def main():
    MODEL.mkdir(parents=True, exist_ok=True)
    path = MODEL / "openprinter.glb"
    build().export(str(path), tolerance=0.5, angularTolerance=0.5)
    print(f"GLB: {path} ({path.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
