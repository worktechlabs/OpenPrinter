"""Modelo 3D para la web.

- docs/model/openprinter.glb: ensamblaje con un nodo por pieza (nombre del
  ensamblaje), para el visor y el montaje interactivo.
- docs/model/montaje.json: pasos de montaje y catálogo de piezas.
- docs/model/openprinter_completo.stl y tinta_completo.stl: la máquina y el
  sistema de tinta en un solo STL, para verlos en cualquier visor o laminador.
- docs/stl/: el STL de cada pieza impresa.

Ensamblaje sin volúmenes reservados. La placa perforada de la mesa se sustituye
por una placa lisa: sus ~800 agujeros multiplicarían por dos el tamaño del GLB.
"""
from pathlib import Path

import cadquery as cq

import layout
import montaje
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


def export_stl(assy, path, prefix=None):
    shapes = [s for c in assy.children if prefix is None or c.name.startswith(prefix)
              for s in c.obj.vals()]
    cq.exporters.export(cq.Compound.makeCompound(shapes), str(path), tolerance=0.5, angularTolerance=0.5)
    print(f"STL: {path} ({path.stat().st_size / 1e6:.1f} MB)")


def main():
    MODEL.mkdir(parents=True, exist_ok=True)
    assy = build()
    path = MODEL / "openprinter.glb"
    assy.export(str(path), tolerance=0.5, angularTolerance=0.5)
    print(f"GLB: {path} ({path.stat().st_size / 1e6:.1f} MB)")
    names = [c.name for c in assy.children]
    montaje.write_json(names, MODEL / "montaje.json")
    montaje.write_md(names)
    export_stl(assy, MODEL / "openprinter_completo.stl")
    export_stl(assy, MODEL / "tinta_completo.stl", "tinta_")
    layout.export_printed(MODEL.parent / "stl")


if __name__ == "__main__":
    main()
