"""Utilidades de geometría compartidas por todos los módulos."""
import math

import cadquery as cq

# Colores (r, g, b, a)
ALU = cq.Color(0.75, 0.77, 0.80, 1)
PLATE = cq.Color(0.20, 0.45, 0.75, 1)
BEAM = cq.Color(0.35, 0.36, 0.38, 1)
STEEL = cq.Color(0.55, 0.55, 0.58, 1)
HEAD = cq.Color(0.10, 0.10, 0.10, 1)
PLATEN = cq.Color(0.30, 0.32, 0.36, 1)
FILM = cq.Color(0.70, 0.90, 1.00, 0.55)
ROLL = cq.Color(0.85, 0.95, 1.00, 0.85)
RUBBER = cq.Color(0.15, 0.15, 0.15, 1)
RESERVED = cq.Color(0.90, 0.20, 0.20, 0.25)
ENVELOPE = cq.Color(0.95, 0.55, 0.10, 0.12)
PRINTED = cq.Color(0.95, 0.55, 0.10, 1)       # piezas impresas en 3D
PRINTED_ALT = cq.Color(0.20, 0.70, 0.45, 1)   # piezas impresas, segundo color
MOTOR = cq.Color(0.12, 0.12, 0.14, 1)
BELT = cq.Color(0.10, 0.10, 0.10, 1)

# Ranura del perfil serie 40, ranura 8 (simplificada)
SLOT_OPEN = 8.2       # boca de la ranura
SLOT_LIP = 4.0        # espesor del labio
SLOT_INNER = 16.0     # ancho de la cámara interior
SLOT_DEPTH = 12.0     # profundidad total
CORE_BORE = 6.8       # taladro central (roscar M8)


def box(x0, x1, y0, y1, z0, z1):
    return (cq.Workplane("XY")
            .box(x1 - x0, y1 - y0, z1 - z0, centered=False)
            .translate((x0, y0, z0)))


def rod_x(x0, x1, y, z, d):
    """Cilindro a lo largo de X."""
    return cq.Workplane("YZ").circle(d / 2).extrude(x1 - x0).translate((x0, y, z))


def rod_y(y0, y1, x, z, d):
    """Cilindro a lo largo de Y."""
    return cq.Workplane("XZ").circle(d / 2).extrude(-(y1 - y0)).translate((x, y0, z))


def rod_z(z0, z1, x, y, d):
    """Cilindro a lo largo de Z."""
    return cq.Workplane("XY").circle(d / 2).extrude(z1 - z0).translate((x, y, z0))


def strip_yz(points, x0, x1, t=0.8):
    """Banda de film siguiendo una polilínea en el plano YZ."""
    solid = None
    for (y0, z0), (y1, z1) in zip(points, points[1:]):
        length = math.hypot(y1 - y0, z1 - z0)
        ny, nz = -(z1 - z0) / length * t, (y1 - y0) / length * t
        seg = (cq.Workplane("YZ")
               .polyline([(y0, z0), (y1, z1), (y1 + ny, z1 + nz), (y0 + ny, z0 + nz)])
               .close().extrude(x1 - x0).translate((x0, 0, 0)))
        solid = seg if solid is None else solid.union(seg)
    return solid


def _profile_section(nu, nv):
    """Sección de perfil 40·nu x 40·nv centrada en el origen (plano local uv)."""
    w, h = 40 * nu, 40 * nv
    sec = cq.Sketch().rect(w, h)
    slots = []
    for i in range(nu):
        u = -w / 2 + 20 + 40 * i
        for sign in (-1, 1):
            slots.append((u, sign * h / 2, False))
    for j in range(nv):
        v = -h / 2 + 20 + 40 * j
        for sign in (-1, 1):
            slots.append((sign * w / 2, v, True))
    for u, v, vertical in slots:
        # boca + cámara, orientadas hacia el exterior de la cara
        for width, d0, d1 in ((SLOT_OPEN, 0, SLOT_LIP), (SLOT_INNER, SLOT_LIP, SLOT_DEPTH)):
            depth = d1 - d0
            mid = (d0 + d1) / 2
            if vertical:
                cu = u - math.copysign(mid, u)
                sec = sec.push([(cu, v)]).rect(depth, width, mode="s").reset()
            else:
                cv = v - math.copysign(mid, v)
                sec = sec.push([(u, cv)]).rect(width, depth, mode="s").reset()
    centers = [(-w / 2 + 20 + 40 * i, -h / 2 + 20 + 40 * j)
               for i in range(nu) for j in range(nv)]
    return sec.push(centers).circle(CORE_BORE / 2, mode="s").reset()


def profile(axis, length, start, center, size=(1, 1)):
    """Perfil de aluminio serie 40.

    axis: "x", "y" o "z" (dirección del perfil)
    start: coordenada inicial a lo largo del eje
    center: centro de la sección en las otras dos coordenadas, en orden
            (y, z) para "x", (x, z) para "y", (x, y) para "z"
    size: múltiplos de 40 de la sección, en el mismo orden que center
    """
    a, b = center
    nu, nv = size
    sec = _profile_section(nu, nv)
    if axis == "x":
        wp = cq.Workplane("YZ").placeSketch(sec).extrude(length)
        return wp.translate((start, a, b))
    if axis == "y":
        # Plano XZ: normal -Y, por eso se extruye en negativo
        wp = cq.Workplane("XZ").placeSketch(sec).extrude(-length)
        return wp.translate((a, start, b))
    wp = cq.Workplane("XY").placeSketch(sec).extrude(length)
    return wp.translate((a, b, start))


def corner_bracket(origin, leg_a, leg_b, size=40, t=4):
    """Escuadra en L de 40 mm.

    origin: vértice interior de la escuadra
    leg_a, leg_b: vectores unitarios (ejes globales) de cada ala
    """
    ox, oy, oz = origin
    width_dir = [1 - abs(leg_a[i]) - abs(leg_b[i]) for i in range(3)]

    def plate(leg, normal):
        pts = []
        for s_leg in (0, size):
            for s_w in (-size / 4, size / 4):
                for s_t in (0, t):
                    pts.append(tuple(
                        (ox, oy, oz)[k] + leg[k] * s_leg + width_dir[k] * s_w + normal[k] * s_t
                        for k in range(3)))
        xs, ys, zs = zip(*pts)
        return box(min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))

    return plate(leg_a, leg_b).union(plate(leg_b, leg_a))


def leveling_foot(x, y, z_top, d=40, h=8, stem=30):
    """Pata niveladora M8: base de goma bajo una varilla roscada."""
    base = cq.Workplane("XY").circle(d / 2).extrude(h).translate((x, y, z_top - stem - h))
    rod = cq.Workplane("XY").circle(4).extrude(stem).translate((x, y, z_top - stem))
    return base.union(rod)
