"""Vistas rápidas en PNG del esqueleto (out/layout_*.png), sin visor externo."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import cadquery as cq

import layout

LIGHT = np.array([0.4, -0.6, 0.7])
LIGHT = LIGHT / np.linalg.norm(LIGHT)

# azim: ángulo de la cámara en el plano XY desde +X (90 = desde delante, +Y)
VIEWS = {
    "iso": dict(elev=25, azim=120),
    "iso_trasera": dict(elev=25, azim=-60),
    # Sección lateral: vista desde +X sin la placa derecha ni lo que cuelga de ella
    "lateral": dict(elev=0, azim=0, hide=("placa_der", "reserva_motor_y", "pata_2", "pata_3")),
    "frontal": dict(elev=0, azim=90),
    "chasis": dict(elev=22, azim=125, only=("placa_izq", "placa_der", "larguero", "travesano", "tirante",
                                             "viga", "escuadra", "pata")),
    "carro": dict(elev=20, azim=115, only=("carro", "patin", "cabezal")),
    "carro_trasera": dict(elev=30, azim=-70, only=("carro", "patin", "cabezal")),
    "motor_x": dict(elev=35, azim=-60, only=("soporte_motor_x", "motor_x", "polea_motor")),
    "mesa": dict(elev=35, azim=120, only=("mesa_placa", "mesa_camara", "ventilador")),
    "mesa_camara": dict(elev=55, azim=110, only=("mesa_camara_1",)),
    "presion": dict(elev=15, azim=30, only=tuple(f"presion_{p}_2" for p in
                                                  ("soporte", "brazo", "rueda", "leva", "muelle"))),
    "presion_lateral": dict(elev=0, azim=0, only=tuple(f"presion_{p}_2" for p in
                                                        ("brazo", "rueda", "leva", "muelle"))),
    "motor_y": dict(elev=20, azim=30, only=("soporte_motor_y", "motor_y", "polea_80t", "polea_20t",
                                            "correa_y", "presion_palanca")),
}


def triangles(assy, hide=(), only=None):
    tris, colors = [], []
    for child in assy.children:
        if child.name in hide or (only and not child.name.startswith(only)):
            continue
        shape = cq.Compound.makeCompound(child.obj.vals())
        verts, faces = shape.tessellate(1.0, 0.5)
        v = np.array([p.toTuple() for p in verts])
        r, g, b, a = child.color.toTuple()
        for f in faces:
            t = v[list(f)]
            n = np.cross(t[1] - t[0], t[2] - t[0])
            norm = np.linalg.norm(n)
            shade = 0.45 + 0.55 * abs(n @ LIGHT / norm) if norm else 1
            tris.append(t)
            colors.append((r * shade, g * shade, b * shade, a))
    return tris, colors


def render(assy, path, elev, azim, hide=(), only=None):
    tris, colors = triangles(assy, hide, only)
    fig = plt.figure(figsize=(12, 8), dpi=110)
    ax = fig.add_subplot(projection="3d", proj_type="ortho")
    ax.add_collection3d(Poly3DCollection(tris, facecolors=colors, edgecolors="none"))
    pts = np.concatenate(tris)
    lo, hi = pts.min(axis=0), pts.max(axis=0)
    ax.set_xlim(lo[0], hi[0]); ax.set_ylim(lo[1], hi[1]); ax.set_zlim(lo[2], hi[2])
    ax.set_box_aspect(hi - lo)
    ax.view_init(elev=elev, azim=azim)
    ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def main():
    layout.OUT.mkdir(exist_ok=True)
    assy = layout.build()
    for name, view in VIEWS.items():
        render(assy, layout.OUT / f"layout_{name}.png", **view)
        print("Vista:", layout.OUT / f"layout_{name}.png")


if __name__ == "__main__":
    main()
