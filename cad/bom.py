"""Listas de compra de las fases 0 y 1, calculadas a partir del modelo.

Genera docs/compra_faseN.md y docs/compra_faseN.csv. Las longitudes y
cantidades salen de params.py y de los módulos, así que si cambia el ancho de
film la lista se actualiza sola. Los precios son una estimación orientativa
para comparar opciones, no un presupuesto.
"""
import math
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
    "rollo_mandril": 2, "rollo_collarin": 4,
    "mesa_entrada_segmento": rolls.ENTRY_SEGMENTS, "mesa_salida_segmento": rolls.ENTRY_SEGMENTS, "servicio_base": 1,
    "rodillo_alojamiento_6001": 2,
}
PRINTED_QTY_F1 = {
    "encoder_soporte_cinta_izq": 1, "encoder_soporte_cinta_der": 1, "encoder_soporte_sensor": 1,
    "final_x_bandera": 1, "final_x_soporte": 1, "encoder_y_soporte": 1,
    "cadena_bandeja": 2, "cadena_brazo": 1,
    "tinta_escuadra_repisa": sum(x < ink.RAIL_END_X - 15 for x in ink.BRACKETS_X),
    "tinta_pata_repisa": sum(x >= ink.RAIL_END_X - 15 for x in ink.BRACKETS_X),
    "tinta_base_botellas": 1, "tinta_soporte_bombas": 1, "tinta_soporte_subdepositos": 1,
    "tinta_caja_driver": 1, "tinta_clip_tubos": len(ink.CLIP_POINTS),
    "pantalla_carcasa": 1, "pantalla_soporte": 1,
    "electronica_caja": 1, "electronica_brida_fuente": 2, "panel_iec": 1, "panel_seta": 1,
    "canaleta_tramo_200": math.ceil(wiring.duct_length() / 200),
}
REUSED = "reutilizable de impresora 3D"


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
    grit_shaft = (yfeed.PULLEY_X[1] + 3) - (P.BEAM_X0 - P.SIDE_PLATE_T - P.GRIT_SHAFT_OUT_L)
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
        (("Estructura", "Placa lateral de MDF",
          f"{P.SIDE_PLATE_T} mm, {P.FRAME_Y[1] - P.FRAME_Y[0]} x {P.FRAME_Z[1] - P.FRAME_Z[0]} mm",
          2, 8, "cortar con la plantilla docs/plantillas/placa_lateral_A4.pdf")
         if P.SIDE_PLATE_MATERIAL == "mdf" else
         ("Estructura", "Placa lateral aluminio 5083/6082",
          f"{P.SIDE_PLATE_T} mm, {P.FRAME_Y[1] - P.FRAME_Y[0]} x {P.FRAME_Z[1] - P.FRAME_Z[0]} mm",
          2, 70, "corte láser o agua con placa_lateral.dxf")),
        ("Estructura", "Escuadra interior serie 40", "40 x 40 mm con tornillería", n_br, 1.5, ""),
        ("Estructura", "Pata niveladora", "M8, base Ø40", 4, 2.5, ""),
        ("Movimiento X", "Guía lineal MGN12", f"{P.RAIL_LENGTH} mm", 2, 30, "comprar con los patines"),
        ("Movimiento X", "Patín MGN12H", "", 4, 8, "incluido a veces con la guía"),
        ("Movimiento X", "Correa GT2 10 mm", f"{_round_up(belt_x, 500)} mm (abierta)", 1, 8,
         "fibra de vidrio o acero; para la fase 1 vale una de 6 mm reutilizada"),
        ("Movimiento X", "Polea GT2 20T, 10 mm", "eje 5 mm", 1, 3, "o de 6 mm reutilizada"),
        ("Movimiento X", "Polea loca GT2 20T lisa, 10 mm", "eje 5 mm", 1, 3, "o de 6 mm reutilizada"),
        ("Arrastre Y", "Eje acero calibrado Ø12 h6", f"{_round_up(grit_shaft)} mm", 1, 12,
         "eje del rodillo de arrastre"),
        ("Arrastre Y", "Rodillo Ø30", f"{P.PLATEN_X[1] - P.PLATEN_X[0]:.0f} mm",
         1, 25, "barra de aluminio taladrada a Ø12, o tubo Ø30 con tapones; recubrir con lija adhesiva o goma"),
        ("Arrastre Y", "Rodamiento 6001-2RS", "12 x 28 x 8", 2, 1.5,
         "en alojamientos impresos (MDF)" if P.SIDE_PLATE_MATERIAL == "mdf" else "en las placas laterales"),
        ("Arrastre Y", "Tornillo M4 x 35 + tuerca + arandela", "", 6, 0.15, "alojamientos del rodamiento"),
        ("Arrastre Y", "Eje acero Ø8", f"{_round_up(lift_shaft)} mm", 1, 6, "eje de levante"),
        ("Arrastre Y", "Rodamiento 625ZZ", "5 x 16 x 5", n_pinch, 0.6, "ruedas de presión"),
        ("Arrastre Y", "Muelle de compresión", "Ø6 x 12 mm, hilo 0,6-0,8", n_pinch, 0.3, "ajustar la fuerza probando"),
        ("Arrastre Y", "Polea GT2 80T, 6 mm", "eje 12 mm", 1, 8, "en el rodillo"),
        ("Arrastre Y", "Polea GT2 20T, 6 mm", "eje 5 mm", 1, 2, "en el motor Y"),
        ("Arrastre Y", "Correa GT2 6 mm cerrada", f"~{_round_up(belt_y, 10)} mm", 1, 3,
         f"cálculo {belt_y:.0f} mm; los colisos del soporte dan ±4 mm"),
        ("Rollos y guías", "Tubo aluminio Ø25", f"{_round_up(roll_shaft)} mm", 1, 10, "eje del rollo"),
        ("Rollos y guías", "Barra aluminio Ø25", f"{P.BEAM_LENGTH:.0f} mm", 2, 12,
         "guías delantera y trasera; roscar M6 en las testas"),
        ("Rollos y guías", "Rodamiento 6005-2RS", "25 x 47 x 12", 2, 3, "mandriles"),
        ("Rollos y guías", "Fieltro adhesivo", "3 mm", 1, 3, "freno del rollo de entrada"),
        ("Mesa de vacío", "Placa aluminio perforada",
         f"{P.PLATEN_TOP_T} mm, {P.PLATEN_X[1] - P.PLATEN_X[0]:.0f} x {P.PLATEN_Y[1] - P.PLATEN_Y[0]} mm",
         1, 45, "corte láser con mesa_placa.dxf"),
        ("Mesa de vacío", "Ventilador 80 mm 24 V", "alta presión estática", P.PLATEN_SEGMENTS, 6,
         "24 V para alimentarlos de la misma fuente"),
        ("Mesa de vacío", "Cinta de espuma", "3 x 10 mm, 5 m", 1, 5, "juntas de cámaras y placa"),
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


def items_fase1():
    """Fase 1: movimiento, sensores, cableado y electrónica."""
    x0, x1, y0, y1 = P.ELEC_PLATE
    strip_len = P.ENC_STRIP_X[1] - P.ENC_STRIP_X[0] + 60
    chain_len = (P.CHAIN_FIX_X - P.CARRIAGE_X_MIN) + math.pi * P.CHAIN_R + 60
    return [
        ("Control", "BTT SKR Mini E3 V3.0", "4 x TMC2209, Klipper", 1, 0, "del inventario"),
        ("Control", "Raspberry Pi 3 o superior", "con tarjeta microSD de 16 GB", 1, 0, "ya disponible"),
        ("Control", "Raspberry Pi Pico", "RP2040", 1, 5, "monitor del encoder X"),
        ("Motores", "Motor NEMA17", "40 mm", 2, 0, "X e Y; del inventario (Creality 42-40, 42HD4041)"),
        ("Sensores", "Cinta de encoder 180 LPI", f"{_round_up(strip_len, 100)} mm", 1, 15,
         "recambio de plóter de gran formato, o de impresoras rotas"),
        ("Sensores", "Resistencias 10 kΩ y 20 kΩ", "divisor 5 V a 3,3 V", 2, 0.1,
         "canales A y B del encoder X hacia el Pico, si el sensor es de 5 V"),
        ("Sensores", "Sensor de encoder de cuadratura", "tipo H9730/H9740, 180 LPI", 1, 6,
         "o sacado de una impresora rota"),
        ("Sensores", "Placa AS5047P + imán diametral", "imán 6 x 2,5 mm", 1, 15, "encoder Y"),
        ("Sensores", "Sensor óptico de horquilla", "tipo TCST2103, módulo", 1, 2, "final de carrera X"),
        ("Sensores", "Sensor reflexivo TCRT5000", "módulo", 1, 1, "detección de film"),
        ("Sensores", "Microinterruptor", "con palanca", 1, 1, "palanca de presión"),
        ("Cableado", "Cadena portacables", f"10 x 20 mm, {_round_up(chain_len, 100)} mm", 1, 8, ""),
        ("Cableado", "Cable apantallado 4 hilos", "2 m", 2, 2, "encoders"),
        ("Cableado", "Alargadores de motor y conectores JST", "", 1, 10, ""),
        ("Alimentación", "Fuente 24 V", "de impresora 3D, 200 W o más", 1, 0, "del inventario"),
        ("Alimentación", "Convertidor 24 V a 5 V", "5 A", 1, 8, "Raspberry Pi y Pico"),
        ("Alimentación", "Seta de emergencia NC", "22 mm, con caja", 1, 8, "corta los 24 V de los motores"),
        ("Alimentación", "Conector IEC con interruptor y fusible", "", 1, 5, ""),
        ("Montaje", "Bandeja inferior de electrónica", f"MDF 10 mm, {x1 - x0} x {y1 - y0} mm",
         1, 4, "apoya en los largueros laterales y el central"),
        ("Montaje", "Convertidor 24 V a 12 V", "5 A", 1, 6, "ventiladores 4010 y bombas de tinta"),
        ("Montaje", "Tapa de ranura 8 mm", "2 m", 1, 6, "cables de sensores por las ranuras de la viga"),
        ("Montaje", "Bridas y portabridas adhesivos", "", 1, 4, ""),
        ("Montaje", "Separadores M3 de nylon", "6 mm", 16, 0.1, ""),
        ("Montaje", "Tuerca en T M5 + tornillo M5", "", 3 + 2 * 4, 0.3, "placa de electrónica y bandeja"),
        ("Montaje", "Inserto térmico M3 + tornillo M3", "", 12, 0.15, "soportes de sensores y brazo"),
        ("Pantalla", 'Pantalla táctil 7" HDMI + USB', "1024 x 600, KlipperScreen", 1, 35,
         "medir la que se compre y ajustar SCREEN_SIZE"),
        ("Pantalla", "Cable HDMI fino + USB", "1,5 m", 1, 6, "por las canaletas hasta la Raspberry Pi"),
        ("Tinta", "Caja de plástico con tapa", f"{' x '.join(str(v) for v in P.INK_BOX)} mm o mayor", 1, 9,
         "tipo Really Useful Box 9 L; bandeja antiderrames de las botellas"),
        ("Tinta", "Repisa", f"MDF 12 mm, {ink.SHELF_X[1] - ink.SHELF_X[0]:.0f} x "
         f"{ink.SHELF_Y[0] - ink.SHELF_Y[1]:.0f} mm", 1, 3, ""),
        ("Tinta", "Tapón de botella con 2 racores", "salida de tubo + respiradero", len(P.INK_COLORS), 3,
         "para las botellas de 1 L del fabricante"),
        ("Tinta", "Filtro de aire para respiradero", "", len(P.INK_COLORS), 1, ""),
        ("Tinta", "Bomba peristáltica 12 V", "tubo de silicona 2 x 4 mm", len(P.INK_COLORS), 7,
         "rellena los subdepósitos; parada, cierra el tubo"),
        ("Tinta", "Subdepósito de tinta con sensor de nivel", "~100 ml, flotador", len(P.INK_COLORS), 6,
         "recambio de DTF/UV, o depósito + interruptor de flotador"),
        ("Tinta", "Módulo MOSFET 4 + 1 canales o placa ULN2803", "entrada 3,3 V", 1, 6,
         "bombas desde los GPIO de la Raspberry Pi"),
        ("Tinta", "Agitador magnético mini + imán", "", 1, 12, "bajo la botella de blanco"),
        ("Tinta", "Tubo de tinta 3 x 2 mm", "10 m", 1, 10, "botella, bomba, subdepósito y carro"),
        ("Tinta", "Racores y uniones para tubo de 3 mm", "", 1, 5, ""),
        ("Tinta", "Resistencias 10 kΩ + diodos 1N4007", "", len(P.INK_COLORS), 0.2,
         "pull-up de los flotadores y diodo de cada bomba (firmware/README.md)"),
    ]


def printed_mass(phase=0):
    if phase == 0:
        parts = {**xaxis.printed_parts(), **carriage.printed_parts(), **platen.printed_parts(),
                 **yfeed.printed_parts(), **rolls.printed_parts(), **service.printed_parts()}
        qtys = PRINTED_QTY
    else:
        parts = {**motion.printed_parts(), **ink.printed_parts(), **wiring.printed_parts()}
        qtys = PRINTED_QTY_F1
    out = []
    for name, part in parts.items():
        qty = qtys[name]
        grams = part.val().Volume() / 1000 * PETG_DENSITY * INFILL_FACTOR
        out.append((name, qty, grams))
    return out


def write_list(phase, rows, footnote):
    DOCS.mkdir(exist_ok=True)
    printed = printed_mass(phase)
    total_printed = sum(q * g for _, q, g in printed)
    filament_cost = total_printed / 1000 * 20

    with open(DOCS / f"compra_fase{phase}.csv", "w", encoding="utf-8") as f:
        f.write("categoria;articulo;especificacion;cantidad;precio_unitario_eur;notas\n")
        for row in rows:
            f.write(";".join(str(v) for v in row) + "\n")

    lines = [
        f"# Lista de compra: fase {phase}",
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
              f"| **Total fase {phase}** | **{total + filament_cost:.0f}** |", "",
              footnote, ""]
    (DOCS / f"compra_fase{phase}.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Fase {phase}: {len(rows)} líneas, ~{total:.0f} € + filamento "
          f"{total_printed / 1000:.2f} kg -> {DOCS / f'compra_fase{phase}.md'}")


def write():
    write_list(0, items(), "No incluye motores, electrónica (fase 1), cabezales, tintas ni herramientas.")
    write_list(1, items_fase1(), "Las placas, la Raspberry Pi, los motores y las correas se cuentan a 0 € "
               "porque se reutilizan de impresoras 3D. No incluye cabezales ni tintas.")


if __name__ == "__main__":
    write()
