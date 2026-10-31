"""Renders de presentación (PyVista/VTK) para la documentación y la web.

Genera docs/img/*.png sin los volúmenes reservados ni la envolvente del carro.
"""
from pathlib import Path

import numpy as np
import pyvista as pv

import cadquery as cq

import layout
import params as P

IMG = Path(__file__).resolve().parent.parent / "docs" / "img"
HIDDEN = ("reserva", "envolvente")
SIZE = (1600, 1000)

# Vistas: posición de cámara relativa al punto focal (dirección), zoom, filtro
VIEWS = {
    "general": dict(direction=(-1.1, 1.6, 0.9), zoom=1.25),
    "general_trasera": dict(direction=(1.2, -1.5, 1.0), zoom=1.25),
    "lateral": dict(direction=(1, 0, 0), zoom=1.9, parallel=True,
                    hide=("placa_der", "pata_2", "pata_3", "soporte_motor_y", "motor_y", "polea_80t_y",
                          "polea_20t_y", "correa_y", "presion_palanca", "collarin_placa_entrada_1",
                          "collarin_placa_recogida_1", "eje_", "rodamiento_arrastre_1")),
    "carro": dict(direction=(-0.9, 1.4, 0.7), zoom=1.1, only=("carro", "patin", "cabezal")),
    "presion": dict(direction=(-1.2, 1.0, 0.5), zoom=1.0,
                    only=tuple(f"presion_{p}_2" for p in ("soporte", "brazo", "rueda", "leva", "muelle"))),
    "mesa": dict(direction=(-0.8, 1.2, 1.4), zoom=1.15,
                 only=("mesa_placa", "mesa_camara", "ventilador", "mesa_entrada")),
    "mesa_camara": dict(direction=(-0.5, 0.8, 1.6), zoom=1.1, only=("mesa_camara_1",)),
    "motor_y": dict(direction=(1.4, 1.0, 0.6), zoom=1.1,
                    only=("soporte_motor_y", "motor_y", "polea_80t_y", "polea_20t_y", "correa_y")),
    "mandril": dict(direction=(1.3, -0.9, 0.6), zoom=1.0,
                    only=("mandril_entrada_+1", "collarin_entrada_+1")),
}


def meshes(assy):
    out = []
    for child in assy.children:
        if child.name.startswith(HIDDEN):
            continue
        shape = cq.Compound.makeCompound(child.obj.vals())
        verts, tris = shape.tessellate(0.3, 0.3)
        if not tris:
            continue
        pts = np.array([v.toTuple() for v in verts])
        faces = np.hstack([[3, *t] for t in tris])
        mesh = pv.PolyData(pts, faces).compute_normals(split_vertices=True, feature_angle=35)
        out.append((child.name, mesh, child.color.toTuple()))
    return out


def _selected(name, only, hide):
    if only and not name.startswith(only):
        return False
    return not (hide and name.startswith(hide))


def render(items, path, direction, zoom=1.0, only=None, hide=None, parallel=False):
    pl = pv.Plotter(off_screen=True, window_size=SIZE)
    pl.set_background("#f4f5f7", top="#ffffff")
    pl.enable_anti_aliasing("ssaa")
    chosen = [(n, m, c) for n, m, c in items if _selected(n, only, hide)]
    for _, mesh, (r, g, b, a) in chosen:
        pl.add_mesh(mesh, color=(r, g, b), opacity=a, smooth_shading=True,
                    specular=0.25, specular_power=20, ambient=0.18, diffuse=0.85)
    bounds = pv.MultiBlock([m for _, m, _ in chosen]).bounds
    center = np.array([(bounds[0] + bounds[1]) / 2, (bounds[2] + bounds[3]) / 2,
                       (bounds[4] + bounds[5]) / 2])
    radius = np.linalg.norm([bounds[1] - bounds[0], bounds[3] - bounds[2], bounds[5] - bounds[4]]) / 2
    d = np.array(direction, dtype=float)
    d /= np.linalg.norm(d)
    pl.camera.focal_point = center
    pl.camera.position = center + d * radius * 3.2
    pl.camera.up = (0, 0, 1)
    if parallel:
        pl.enable_parallel_projection()
    pl.reset_camera()
    pl.camera.zoom(zoom)
    pl.screenshot(str(path))
    pl.close()


def main():
    IMG.mkdir(parents=True, exist_ok=True)
    items = meshes(layout.build(carriage_x=-120))
    for name, view in VIEWS.items():
        render(items, IMG / f"{name}.png", **view)
        print("Render:", IMG / f"{name}.png")


if __name__ == "__main__":
    main()
