"""Plantillas de corte a tamaño real en hojas A4 (docs/plantillas/*.pdf).

Lee el DXF de la placa lateral que genera chassis.export (así la plantilla es
exactamente la geometría del modelo) y lo reparte en hojas A4 apaisadas a
escala 1:1, con solape, cuadrícula de 50 mm para empalmar, centros de taladro
marcados y una regla de 100 mm para comprobar la escala de impresión.

Uso: python cad/layout.py  (genera out/placa_lateral.dxf)
     python cad/plantillas.py
"""
import math
from collections import Counter
from pathlib import Path

import ezdxf
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Arc, Circle

import params as P

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "docs" / "plantillas"

A4 = (210, 297)              # mm; la orientación se elige para usar menos hojas
MARGIN = 8                   # margen que respeta casi cualquier impresora
OVERLAP = 10
INCH = 25.4

DRILL_NAMES = {3.4: "M3", 4.5: "M4", 5.5: "M5", 6.5: "M6", 8.5: "M8", 16.0: "eje Ø12", 20.0: "tubos"}


def _load(dxf_path, origin):
    """Entidades del DXF trasladadas para que la esquina trasera-inferior sea (0, 0)."""
    ox, oy = origin
    doc = ezdxf.readfile(dxf_path)
    lines, arcs, circles = [], [], []
    for e in doc.modelspace():
        t = e.dxftype()
        if t == "LINE":
            s, f = e.dxf.start, e.dxf.end
            lines.append(((s.x - ox, s.y - oy), (f.x - ox, f.y - oy)))
        elif t == "ARC":
            c = e.dxf.center
            arcs.append(((c.x - ox, c.y - oy), e.dxf.radius, e.dxf.start_angle, e.dxf.end_angle))
        elif t == "CIRCLE":
            c = e.dxf.center
            circles.append(((c.x - ox, c.y - oy), e.dxf.radius))
    return lines, arcs, circles


def _drill_label(d):
    d = round(d, 1)
    name = DRILL_NAMES.get(d)
    return f"Ø{d:g}" + (f" ({name})" if name else "")


def _draw_part(ax, geo, lw=0.9, labels=True):
    lines, arcs, circles = geo
    for (x0, y0), (x1, y1) in lines:
        ax.plot([x0, x1], [y0, y1], color="black", lw=lw, solid_capstyle="round")
    for (cx, cy), r, a0, a1 in arcs:
        ax.add_patch(Arc((cx, cy), 2 * r, 2 * r, theta1=a0, theta2=a1, color="black", lw=lw))
    for (cx, cy), r in circles:
        ax.add_patch(Circle((cx, cy), r, fill=False, color="black", lw=lw))
        arm = max(r + 4, 6)
        ax.plot([cx - arm, cx + arm], [cy, cy], color="#c0392b", lw=0.35)
        ax.plot([cx, cx], [cy - arm, cy + arm], color="#c0392b", lw=0.35)
        if labels:
            ax.text(cx + r + 1.5, cy + 1.5, _drill_label(2 * r), fontsize=6, color="#c0392b",
                    clip_on=True)


def _setup_page_axes(fig, page, x0, y0):
    w, h = page[0] - 2 * MARGIN, page[1] - 2 * MARGIN
    ax = fig.add_axes([MARGIN / page[0], MARGIN / page[1], w / page[0], h / page[1]])
    ax.set_xlim(x0, x0 + w)
    ax.set_ylim(y0, y0 + h)
    ax.set_aspect("equal")
    ax.axis("off")
    return ax, w, h


def _grid(ax, size, step=50):
    W, H = size
    for x in range(0, int(W) + 1, step):
        ax.plot([x, x], [0, H], color="#9db7d5", lw=0.3, zorder=0)
        ax.text(x + 1, 1, f"{x}", fontsize=5, color="#5d7fa8", clip_on=True)
    for y in range(0, int(H) + 1, step):
        ax.plot([0, W], [y, y], color="#9db7d5", lw=0.3, zorder=0)
        ax.text(1, y + 1, f"{y}", fontsize=5, color="#5d7fa8", clip_on=True)


def _scale_bar(fig, page):
    x0 = MARGIN / page[0]
    ax = fig.add_axes([x0, 1 - (MARGIN + 6) / page[1], 100 / page[0], 4 / page[1]])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 4)
    ax.axis("off")
    ax.plot([0, 100], [1, 1], color="black", lw=1)
    for x in range(0, 101, 10):
        ax.plot([x, x], [0, 2 if x % 50 else 3], color="black", lw=0.6)
    ax.text(102, 0.5, "100 mm: compruébalo con una regla", fontsize=6, va="bottom")


def _cover(pdf, title, size, geo, notes, holes):
    fig = plt.figure(figsize=(A4[1] / INCH, A4[0] / INCH))
    fig.text(0.04, 0.94, title, fontsize=15, weight="bold")
    W, H = size
    ax = fig.add_axes([0.04, 0.30, 0.55, 0.58])
    _draw_part(ax, geo, lw=0.6, labels=False)
    ax.set_xlim(-10, W + 10)
    ax.set_ylim(-25, H + 10)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.annotate("", (0, -12), (W, -12), arrowprops=dict(arrowstyle="<->", lw=0.6))
    ax.text(W / 2, -20, f"{W:.0f} mm", ha="center", fontsize=8)
    ax.annotate("", (-6, 0), (-6, H), arrowprops=dict(arrowstyle="<->", lw=0.6))
    ax.text(-9, H / 2, f"{H:.0f} mm", rotation=90, va="center", ha="right", fontsize=8)
    ax.text(2, H + 3, "← TRASERA (entrada del film)", fontsize=7)
    ax.text(W - 2, H + 3, "DELANTERA (salida) →", fontsize=7, ha="right")

    fig.text(0.63, 0.88, "Instrucciones", fontsize=11, weight="bold")
    fig.text(0.63, 0.86, "\n".join(notes), fontsize=7.2, va="top", linespacing=1.45)

    rows = sorted(Counter(holes).items())
    fig.text(0.04, 0.25, "Taladros (desde la esquina trasera-inferior)", fontsize=9, weight="bold")
    text = []
    for (d, x, y), n in rows:
        text.append(f"{_drill_label(d):<16} Y={x:6.1f}  Z={y:6.1f}" + (f"  x{n}" if n > 1 else ""))
    cols = [text[i::3] for i in range(3)]
    for i, col in enumerate(cols):
        fig.text(0.04 + i * 0.31, 0.23, "\n".join(col), fontsize=6.3, va="top", family="monospace",
                 linespacing=1.3)
    pdf.savefig(fig)
    plt.close(fig)


def tiled_pdf(path, title, geo, size, notes):
    W, H = size
    holes = [(round(2 * r, 1), round(c[0], 1), round(c[1], 1)) for c, r in geo[2]]
    def layout(page):
        w, h = page[0] - 2 * MARGIN, page[1] - 2 * MARGIN
        cols = max(1, math.ceil((W - OVERLAP) / (w - OVERLAP)))
        rows = max(1, math.ceil((H - OVERLAP) / (h - OVERLAP)))
        return rows * cols, page, w, h, rows, cols

    _, page, w, h, rows, cols = min(layout(A4), layout((A4[1], A4[0])))
    with PdfPages(path) as pdf:
        notes = notes + [f"Son {rows * cols} hojas: {rows} filas x {cols} columnas, con {OVERLAP} mm",
                         "de solape. Empálmalas haciendo coincidir la cuadrícula de 50 mm."]
        _cover(pdf, title, size, geo, notes, holes)
        for r in range(rows):
            for c in range(cols):
                x0 = c * (w - OVERLAP)
                y0 = (rows - 1 - r) * (h - OVERLAP)
                fig = plt.figure(figsize=(page[0] / INCH, page[1] / INCH))
                ax, _, _ = _setup_page_axes(fig, page, x0, y0)
                _grid(ax, size)
                _draw_part(ax, geo)
                # Bandas de solape
                if c > 0:
                    ax.axvspan(x0, x0 + OVERLAP, color="#f1c40f", alpha=0.18, lw=0)
                if r > 0:
                    ax.axhspan(y0 + h - OVERLAP, y0 + h, color="#f1c40f", alpha=0.18, lw=0)
                ax.add_patch(plt.Rectangle((x0, y0), w, h, fill=False, lw=0.4, ls=":", color="#888"))
                _scale_bar(fig, page)
                fig.text(1 - MARGIN / page[0], 1 - (MARGIN + 10) / page[1],
                         f"{title} · hoja fila {r + 1} / columna {c + 1}", fontsize=7, ha="right")
                fig.text(1 - MARGIN / page[0], MARGIN / page[1] / 2,
                         "Imprimir al 100 % (tamaño real, sin ajustar a página)", fontsize=6, ha="right")
                pdf.savefig(fig)
                plt.close(fig)
    return rows * cols


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    y0, y1 = P.FRAME_Y
    z0, z1 = P.FRAME_Z
    size = (y1 - y0, z1 - z0)
    geo = _load(ROOT / "out" / "placa_lateral.dxf", (y0, z0))
    t = P.SIDE_PLATE_T
    notes = [
        f"1. Imprime al 100 % (tamaño real). Mide la regla de 100 mm de cada hoja.",
        "2. Empalma las hojas por la cuadrícula y pégalas con cinta.",
        f"3. Pega la plantilla sobre un tablero de MDF de {t} mm. Pon debajo el",
        "   segundo tablero, sujeta los dos con sargentos y córtalos juntos:",
        "   las dos placas laterales son iguales y saldrán idénticas.",
        "4. Contorno y ranuras de los rollos: caladora con hoja para madera,",
        "   por fuera de la línea. Lija hasta la línea.",
        "5. Taladros: granetea las cruces rojas, pasa broca de 3 mm por los",
        "   dos tableros y luego abre a la medida indicada.",
        "6. Ranuras: taladra Ø26 en el fondo (asiento del eje) y corta las",
        "   dos rectas con la caladora.",
        "7. Sella los cantos con cola diluida o barniz para que no se deshilachen.",
        "",
        "Los rodamientos del rodillo NO van en el MDF: van en el alojamiento",
        "impreso (rodillo_alojamiento_6001.stl), por dentro, con 3 tornillos M4.",
    ]
    n = tiled_pdf(OUT_DIR / "placa_lateral_A4.pdf", f"OpenDTF · placa lateral (x2, MDF {t} mm)",
                  geo, size, notes)
    print(f"Plantilla: {OUT_DIR / 'placa_lateral_A4.pdf'} (portada + {n} hojas A4)")


if __name__ == "__main__":
    main()
