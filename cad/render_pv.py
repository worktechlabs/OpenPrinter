"""Renders de presentación (PyVista/VTK) para la documentación y la web.

Genera docs/img/*.png sin los volúmenes reservados ni la envolvente del carro.
"""
from pathlib import Path

import numpy as np
import pyvista as pv

import cadquery as cq

import layout
import montaje
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
                          "eje_", "rodamiento_arrastre_1", "tinta_", "pantalla")),
    "carro": dict(direction=(-0.9, 1.4, 0.7), zoom=1.1, only=("carro", "patin", "cabezal")),
    "presion": dict(direction=(-1.2, 1.0, 0.5), zoom=1.0,
                    only=tuple(f"presion_{p}_2" for p in ("soporte", "brazo", "rueda", "leva", "muelle"))),
    "mesa": dict(direction=(-0.8, 1.2, 1.4), zoom=1.15,
                 only=("mesa_placa", "mesa_camara", "ventilador", "mesa_entrada")),
    "mesa_camara": dict(direction=(-0.5, 0.8, 1.6), zoom=1.1, only=("mesa_camara_1",)),
    "motor_y": dict(direction=(1.4, 1.0, 0.6), zoom=1.1,
                    only=("soporte_motor_y", "motor_y", "polea_80t_y", "polea_20t_y", "correa_y")),
    "carro_trasera": dict(direction=(0.9, -1.4, 0.8), zoom=1.1,
                          only=("carro", "patin", "cabezal", "encoder_soporte_sensor", "encoder_sensor",
                                "final_x_bandera")),
    "cadena": dict(direction=(0.6, -1.5, 0.9), zoom=1.15,
                   only=("cadena", "carro", "patin", "viga_x", "encoder_s")),
    "general_izquierda": dict(direction=(-1.6, 0.9, 0.8), zoom=1.2),
    "tinta_botellas": dict(direction=(1.2, -1.6, 1.0), zoom=1.1,
                           only=("tinta_repisa", "tinta_escuadra", "tinta_pata", "tinta_caja_botellas",
                                 "tinta_base", "tinta_botella", "tinta_tapon", "tinta_agitador",
                                 "tinta_tubo_botella")),
    "tinta_bombas": dict(direction=(-1.5, -0.9, 0.6), zoom=1.1,
                         only=("tinta_soporte", "tinta_bomba", "tinta_caja_driver", "tinta_subdeposito",
                               "tinta_flotador", "tinta_tubo_bomba", "tinta_tubo_sub", "tinta_tubos_carro",
                               "tinta_clip")),
    "pantalla": dict(direction=(-0.5, 1.6, 0.7), zoom=1.2, only=("pantalla",)),
    "salida": dict(direction=(-1.2, 1.3, 0.7), zoom=1.15,
                   only=("mesa_salida", "guia_delantera", "mesa_placa", "mesa_camara")),
    "electronica": dict(direction=(-0.8, 1.3, 1.1), zoom=1.05,
                        only=("electronica_caja", "electronica_fuente", "electronica_brida",
                              "electronica_ventilador")),
    "electronica_interior": dict(direction=(-0.6, 1.2, 1.4), zoom=1.1,
                                 only=("electronica_placa_skr", "electronica_raspberry", "electronica_pico",
                                       "electronica_conversor", "electronica_fuente", "electronica_brida")),
    "cableado": dict(direction=(-1.0, 1.3, 1.0), zoom=1.2,
                     only=("canaleta", "electronica", "panel", "cadena", "larguero", "travesano_central",
                           "placa_izq", "tinta_tubos_carro", "tinta_caja_driver")),
    "encoder_y": dict(direction=(-1.4, 0.5, 0.5), zoom=1.0,
                      only=("encoder_y", "rodamiento_arrastre_0")),
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


GREY = (0.80, 0.81, 0.83)


def render_steps(items):
    """Esquema de cada paso de montaje: lo anterior en gris, lo del paso en color."""
    for i, (sid, title, _, _, cam, *_rest) in enumerate(montaje.STEPS):
        pl = pv.Plotter(off_screen=True, window_size=SIZE)
        pl.set_background("#f4f5f7", top="#ffffff")
        pl.enable_anti_aliasing("ssaa")
        shown = []
        for name, mesh, (r, g, b, a) in items:
            step = montaje.step_of(name)
            if step > i:
                continue
            color, opacity = ((r, g, b), a) if step == i else (GREY, min(a, 0.55))
            pl.add_mesh(mesh, color=color, opacity=opacity, smooth_shading=True,
                        specular=0.25, specular_power=20, ambient=0.2, diffuse=0.85)
            shown.append(mesh)
        bounds = pv.MultiBlock([m for _, m, _ in items]).bounds
        center = np.array([(bounds[0] + bounds[1]) / 2, (bounds[2] + bounds[3]) / 2,
                           (bounds[4] + bounds[5]) / 2])
        radius = np.linalg.norm([bounds[1] - bounds[0], bounds[3] - bounds[2], bounds[5] - bounds[4]]) / 2
        d = np.array(cam, dtype=float)
        d /= np.linalg.norm(d)
        pl.camera.focal_point = center
        pl.camera.position = center + d * radius * 3.2
        pl.camera.up = (0, 0, 1)
        pl.reset_camera(bounds=bounds)
        pl.camera.zoom(1.25)
        pl.add_text(f"{i + 1}. {title}", position="upper_left", font_size=14, color="#222222")
        path = IMG / f"montaje_{i + 1:02d}.png"
        pl.screenshot(str(path))
        pl.close()
        print("Render:", path)


def main(names=None):
    """Renderiza todas las vistas, o solo las indicadas: render_pv.py carro mesa"""
    IMG.mkdir(parents=True, exist_ok=True)
    items = meshes(layout.build(carriage_x=-120))
    if not names or "montaje" in names:
        render_steps(items)
    for name, view in VIEWS.items():
        if names and name not in names:
            continue
        render(items, IMG / f"{name}.png", **view)
        print("Render:", IMG / f"{name}.png")


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
