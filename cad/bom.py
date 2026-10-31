"""Lista de compra de la fase 0, calculada a partir del modelo.

Genera docs/compra_fase0.md y docs/compra_fase0.csv. Las longitudes y
cantidades salen de params.py y de los módulos, así que si cambia el ancho de
film la lista se actualiza sola. Los precios son una estimación orientativa
para comparar opciones, no un presupuesto.
"""
import math
from pathlib import Path

import cadquery as cq

import carriage
import chassis
import params as P
import platen
import rolls
import service
import xaxis
import yfeed

DOCS = Path(__file__).resolve().parent.parent / "docs"
PETG_DENSITY = 1.27          # g/cm³
INFILL_FACTOR = 0.6          # masa real aprox. respecto al sólido (perímetros + 40 % relleno)

PRINTED_QTY = {
    "carro_placa": 1, "carro_bandeja": 1, "carro_pinza_correa": 1,
    "soporte_motor_x": 1, "soporte_tensor_x": 1,
    "mesa_camara": P.PLATEN_SEGMENTS,
    "presion_soporte": P.PINCH_COUNT, "presion_brazo": P.PINCH_COUNT,
    "presion_rueda_tpu": P.PINCH_COUNT, "presion_leva": P.PINCH_COUNT,
    "presion_palanca": 1, "soporte_motor_y": 1,
    "rollo_mandril": 4, "rollo_collarin": 8,
    "mesa_entrada_segmento": rolls.ENTRY_SEGMENTS, "servicio_base": 1,
}


def _round_up(mm, step=50):
    return int(math.ceil(mm / step) * step)


def _bracket_count():
    assy = cq.Assembly()
    chassis.add(assy)
    return sum(1 for c in assy.children if c.name.startswith("escuadra"))


def items():
    """(categoría, artículo, especificación, cantidad, precio unitario €, notas)"""
    n_br = _bracket_count()
    n_pinch = P.PINCH_COUNT
    rail_screws = 2 * int(P.RAIL_LENGTH // 50)
    belt_x = 2 * (P.IDLER_X - P.MOTOR_X) + math.pi * P.PULLEY_PD + 150
    # Correa Y cerrada: longitud aproximada entre poleas 20T y 80T
    d1, d2 = P.Y_PULLEY_PD
    c = P.Y_MOTOR_DZ
    belt_y = 2 * c + math.pi * (d1 + d2) / 2 + (d2 - d1) ** 2 / (4 * c)
    grit_shaft = (yfeed.PULLEY_X[1] + 3) - (P.BEAM_X0 - P.SIDE_PLATE_T - 5)
    lift_shaft = (yfeed.OUT_R + 45) - (P.BEAM_X0 - P.SIDE_PLATE_T - 5)
    roll_shaft = rolls.SHAFT_X[1] - rolls.SHAFT_X[0]
    m8_tnuts = 6 + 2 * n_br + 4
    m5_tnuts = 2 + 2 + 4 * P.PLATEN_SEGMENTS + n_pinch + 4
    inserts_m3 = 6 * P.PLATEN_SEGMENTS + 2

    rows = []
    for name, sec, length, qty, notes in chassis.cut_list():
        price = 12 * length / 1000 * (2 if sec == "4080" else 1)
        rows.append(("Estructura", f"Perfil {sec} ranura 8", f"{length:.0f} mm, {name.lower()}",
                     qty, round(price, 1), notes))
    rows += [
        ("Estructura", "Placa lateral aluminio 5083/6082",
         f"{P.SIDE_PLATE_T} mm, {P.FRAME_Y[1] - P.FRAME_Y[0]} x {P.FRAME_Z[1] - P.FRAME_Z[0]} mm",
         2, 70, "corte láser o agua con placa_lateral.dxf"),
        ("Estructura", "Escuadra interior serie 40", "40 x 40 mm con tornillería", n_br, 1.5, ""),
        ("Estructura", "Pata niveladora", "M8, base Ø40", 4, 2.5, ""),
        ("Movimiento X", "Guía lineal MGN12", f"{P.RAIL_LENGTH} mm", 2, 30, "comprar con los patines"),
        ("Movimiento X", "Patín MGN12H", "", 4, 8, "incluido a veces con la guía"),
        ("Movimiento X", "Correa GT2 10 mm", f"{_round_up(belt_x, 500)} mm (abierta)", 1, 8, "fibra de vidrio o acero"),
        ("Movimiento X", "Polea GT2 20T, 10 mm", "eje 5 mm", 1, 3, ""),
        ("Movimiento X", "Polea loca GT2 20T lisa, 10 mm", "eje 5 mm", 1, 3, ""),
        ("Arrastre Y", "Eje acero calibrado Ø12 h6", f"{_round_up(grit_shaft)} mm", 1, 12,
         "eje del rodillo de arrastre"),
        ("Arrastre Y", "Rodillo Ø30", f"{P.PLATEN_X[1] - P.PLATEN_X[0]:.0f} mm",
         1, 25, "barra de aluminio taladrada a Ø12, o tubo Ø30 con tapones; recubrir con lija adhesiva o goma"),
        ("Arrastre Y", "Rodamiento 6001-2RS", "12 x 28 x 8", 2, 1.5, "en las placas laterales"),
        ("Arrastre Y", "Eje acero Ø8", f"{_round_up(lift_shaft)} mm", 1, 6, "eje de levante"),
        ("Arrastre Y", "Rodamiento 625ZZ", "5 x 16 x 5", n_pinch, 0.6, "ruedas de presión"),
        ("Arrastre Y", "Muelle de compresión", "Ø6 x 12 mm, hilo 0,6-0,8", n_pinch, 0.3, "ajustar la fuerza probando"),
        ("Arrastre Y", "Polea GT2 80T, 6 mm", "eje 12 mm", 1, 8, "en el rodillo"),
        ("Arrastre Y", "Polea GT2 20T, 6 mm", "eje 5 mm", 1, 2, "en el motor Y"),
        ("Arrastre Y", "Correa GT2 6 mm cerrada", f"~{_round_up(belt_y, 10)} mm", 1, 3,
         f"cálculo {belt_y:.0f} mm; los colisos del soporte dan ±4 mm"),
        ("Rollos y guías", "Tubo aluminio Ø25", f"{_round_up(roll_shaft)} mm", 2, 10, "ejes de los rollos"),
        ("Rollos y guías", "Barra aluminio Ø25", f"{P.BEAM_LENGTH:.0f} mm", 2, 12,
         "guías delantera y trasera; roscar M6 en las testas"),
        ("Rollos y guías", "Rodamiento 6005-2RS", "25 x 47 x 12", 4, 3, "mandriles"),
        ("Rollos y guías", "Fieltro adhesivo", "3 mm", 1, 3, "freno del rollo de entrada"),
        ("Mesa de vacío", "Placa aluminio perforada",
         f"{P.PLATEN_TOP_T} mm, {P.PLATEN_X[1] - P.PLATEN_X[0]:.0f} x {P.PLATEN_Y[1] - P.PLATEN_Y[0]} mm",
         1, 45, "corte láser con mesa_placa.dxf"),
        ("Mesa de vacío", "Ventilador 80 mm 12 V", "alta presión estática", P.PLATEN_SEGMENTS, 6, ""),
        ("Mesa de vacío", "Cinta de espuma", "3 x 10 mm, 5 m", 1, 5, "juntas de cámaras y placa"),
        ("Motores (fase 1)", "Motor NEMA17", "48 mm, 1,5-2 A", 2, 13,
         "X e Y; en la fase 0 se mueve a mano"),
        ("Tornillería", "Tuerca en T M8 ranura 8", "", m8_tnuts, 0.25, ""),
        ("Tornillería", "Tornillo M8", "16 y 20 mm", m8_tnuts + 10, 0.2,
         "10 de ellos a la testa de los perfiles entre placas"),
        ("Tornillería", "Tuerca en T M5 ranura 8", "", m5_tnuts, 0.2, ""),
        ("Tornillería", "Tornillo M5", "10-16 mm", m5_tnuts + 4 + n_pinch + 1, 0.1,
         "incluye ejes de ruedas y polea loca"),
        ("Tornillería", "Tuerca en T M3 ranura 8", "", rail_screws, 0.15, "fijación de guías MGN12"),
        ("Tornillería", "Tornillo M3", "8-25 mm", rail_screws + 16 + 8 + 4 + 2 + n_pinch, 0.05,
         "guías, patines, motores, cabezales, pasadores"),
        ("Tornillería", "Tornillo M3 avellanado", "8 mm", inserts_m3 - 2, 0.05, "placa de la mesa"),
        ("Tornillería", "Inserto térmico M3", "", inserts_m3, 0.1, ""),
        ("Tornillería", "Inserto térmico M4 + tornillo M4", "16 mm", 4, 0.3, "ajuste de altura de la bandeja"),
        ("Tornillería", "Tornillo M4 + tuerca", "20-35 mm", 8 + 1 + 4 * P.PLATEN_SEGMENTS, 0.1,
         "collarines, tensor X, ventiladores"),
        ("Tornillería", "Tornillo M6", "16 mm", 4, 0.2, "guías de film"),
        ("Tornillería", "Prisionero M3", "6 mm", n_pinch + 1, 0.1, "levas y palanca"),
    ]
    return rows


def printed_mass():
    parts = {**xaxis.printed_parts(), **carriage.printed_parts(), **platen.printed_parts(),
             **yfeed.printed_parts(), **rolls.printed_parts(), **service.printed_parts()}
    out = []
    for name, part in parts.items():
        qty = PRINTED_QTY[name]
        grams = part.val().Volume() / 1000 * PETG_DENSITY * INFILL_FACTOR
        out.append((name, qty, grams))
    return out


def write():
    DOCS.mkdir(exist_ok=True)
    rows = items()
    printed = printed_mass()
    total_printed = sum(q * g for _, q, g in printed)
    filament_cost = total_printed / 1000 * 20

    with open(DOCS / "compra_fase0.csv", "w", encoding="utf-8") as f:
        f.write("categoria;articulo;especificacion;cantidad;precio_unitario_eur;notas\n")
        for row in rows:
            f.write(";".join(str(v) for v in row) + "\n")

    lines = [
        "# Lista de compra: fase 0",
        "",
        "Generada por `cad/bom.py` a partir del modelo (film de "
        f"{P.FILM_WIDTH} mm). Si cambias `params.py`, vuelve a generarla.",
        "",
        "> Los precios son **orientativos**, para hacerse una idea del presupuesto y",
        "> comparar opciones. No son un presupuesto: compruébalos con tu proveedor.",
        "",
    ]
    total = 0
    category = None
    for cat, name, spec, qty, price, notes in rows:
        if cat != category:
            lines += ["", f"## {cat}", "", "| Artículo | Especificación | Cant. | € aprox. | Notas |",
                      "|---|---|---:|---:|---|"]
            category = cat
        subtotal = qty * price
        total += subtotal
        lines.append(f"| {name} | {spec} | {qty} | {subtotal:.0f} | {notes} |")

    lines += ["", "## Piezas impresas", "",
              f"Masa estimada con PETG al ~{INFILL_FACTOR:.0%} del sólido. STL en `out/stl/`.", "",
              "| Pieza | Cant. | g/ud | g total |", "|---|---:|---:|---:|"]
    for name, qty, grams in printed:
        lines.append(f"| `{name}` | {qty} | {grams:.0f} | {qty * grams:.0f} |")
    lines += [f"| **Total** | | | **{total_printed:.0f} g** |", ""]

    lines += ["## Resumen", "",
              "| Concepto | € aprox. |", "|---|---:|",
              f"| Material comprado | {total:.0f} |",
              f"| Filamento (~{total_printed / 1000:.1f} kg a 20 €/kg) | {filament_cost:.0f} |",
              f"| **Total fase 0** | **{total + filament_cost:.0f}** |", "",
              "No incluye cabezales, electrónica, tintas ni herramientas.", ""]
    (DOCS / "compra_fase0.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Lista de compra: {len(rows)} líneas, ~{total:.0f} € + filamento "
          f"{total_printed / 1000:.1f} kg -> {DOCS / 'compra_fase0.md'}")


if __name__ == "__main__":
    write()
