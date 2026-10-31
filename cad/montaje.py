"""Guía de montaje: pasos, catálogo de piezas y salidas para la web.

Cada pieza del ensamblaje se asigna al primer paso cuyo prefijo coincide con su
nombre. Con eso se generan:
- docs/model/montaje.json: pasos y catálogo para el visor interactivo
  (docs/montaje.html).
- docs/montaje.md: la guía en texto, con un esquema por paso (render_pv.py).
"""
import json
import re
from pathlib import Path

import params as P

DOCS = Path(__file__).resolve().parent.parent / "docs"

# (id, título, prefijos, dirección de despiece X/Y/Z, cámara, texto, tornillería)
STEPS = [
    ("bastidor", "Bastidor inferior",
     ("larguero_izq", "larguero_der", "larguero_tras", "larguero_del", "travesano_central", "escuadra",
      "pata"),
     (0, 0, -1), (-1.1, 1.6, 0.9),
     "Corta los perfiles 4040 según la lista de corte. Une los largueros delantero, trasero y el "
     "travesaño central a los dos largueros laterales con escuadras. Antes de apretar, comprueba "
     "que las dos diagonales miden lo mismo (±1 mm). Enrosca las patas niveladoras en la ranura "
     "inferior de los largueros laterales.",
     ["Escuadras 4040 con tornillo M8 x 16 y tuerca en T M8", "4 patas niveladoras M8"]),
    ("placas", "Placas laterales y travesaños",
     ("placa_izq", "placa_der", "travesano_mesa", "tirante_sup"),
     (1, 0, 0), (-1.1, 1.6, 0.9),
     "Corta y taladra las dos placas de MDF de 19 mm con la plantilla A4 a escala 1:1. Atorníllalas "
     "a los largueros laterales. Rosca M8 en las testas de los dos travesaños de la mesa y del "
     "tirante superior, y atorníllalos desde fuera de las placas. Mide la separación interior entre "
     f"placas arriba y abajo: debe ser {P.BEAM_LENGTH:.0f} mm.",
     ["M8 x 35 + arandela + tuerca en T M8 (3 por placa)", "M8 x 40 en las testas (6)"]),
    ("viga", "Viga X, guías y motor X",
     ("viga_x", "guia_mgn12", "soporte_motor_x", "soporte_tensor_x", "motor_x", "polea_motor_x",
      "polea_loca_x", "final_x_soporte", "encoder_cinta", "encoder_soporte_cinta"),
     (0, 1, 0), (-0.9, 1.5, 0.8),
     "Rosca 2 x M8 en cada testa de la viga 4080 y atorníllala entre las placas. Fija la guía MGN12 "
     "de arriba en la cara delantera con tornillos cada 25 mm, alineada con una regla. Coloca la de "
     "abajo paralela a la primera, midiendo con calibre a lo largo de todo el recorrido. Monta el "
     "soporte del motor X a la izquierda y el del tensor a la derecha. Pon la cinta del encoder en "
     "sus soportes, tensa y sin tocar la viga, y el soporte del sensor de final de carrera.",
     ["M8 x 40 (4)", "M3 x 8 + tuerca en T M3 (80)", "M5 x 10 + tuerca en T M5 (8)", "Polea GT2 20T y polea loca"]),
    ("carro", "Carro y cabezales",
     ("patin", "carro_", "cabezal", "correa_x", "encoder_soporte_sensor", "encoder_sensor",
      "final_x_bandera"),
     (0, 1, 0), (-0.9, 1.4, 0.7),
     "Mete los patines MGN12H en las guías sin sacarlos de su tapón: si se salen, se pierden las "
     "bolas. Atornilla la placa del carro a los 4 patines y la bandeja de los cabezales con el ajuste "
     "de altura a media carrera. Cierra la correa GT2 de 10 mm en la pinza y ténsala. Monta el sensor "
     "del encoder y la bandera de home en el carro.",
     ["M3 x 10 (16) para los patines", "M3 + insertos térmicos para sensor y bandera"]),
    ("mesa", "Mesa de vacío y estación de servicio",
     ("mesa_placa", "mesa_camara", "ventilador", "servicio_"),
     (0, 0, 1), (-0.8, 1.2, 1.4),
     "Atornilla las 4 cámaras impresas a los travesaños de la mesa, cada una con su ventilador de 80 mm "
     "debajo. Encima va la placa de aluminio perforada: sella el borde con cinta de espuma para que "
     "el vacío no se escape. La estación de servicio va a la derecha, bajo la posición de home del carro.",
     ["M4 + tuerca en T M4 para las cámaras", "Cinta de espuma de 3 mm"]),
    ("arrastre", "Arrastre del film (eje Y)",
     ("eje_arrastre", "rodillo_arrastre", "rodamiento_arrastre", "alojamiento_rodamiento", "presion_",
      "eje_levante", "soporte_motor_y", "motor_y", "polea_80t_y", "polea_20t_y", "correa_y", "encoder_y"),
     (0, -1, 0), (-1.2, 1.0, 0.6),
     "Atornilla los alojamientos de los rodamientos 6001 por dentro de las placas. Pasa el eje de 12 mm "
     "con el rodillo de arrastre. Fuera de la placa derecha van la polea de 80 dientes, el motor Y "
     "con su soporte y la correa de 6 mm. Monta el eje de levante de 8 mm con las 6 levas y las 6 "
     "unidades de presión. Termina con la palanca y el imán del encoder Y en la punta izquierda del "
     "eje; el sensor AS5047P queda a 1-2 mm del imán.",
     ["M4 x 30 (6) para los alojamientos", "M5 x 30 (4) para el soporte del motor Y", "Rodamientos 6001 (2)"]),
    ("film", "Guías, rollo y salida del film",
     ("guia_trasera", "guia_delantera", "mesa_entrada", "mesa_salida", "eje_rollo", "rollo_", "nucleo_",
      "mandril_", "collarin_", "film"),
     (0, -1, 0.3), (1.2, -1.5, 1.0),
     "Atornilla las guías de 25 mm trasera y delantera con M6 en las testas. Engancha a presión los 4 "
     "segmentos de la mesa de entrada en la guía trasera y los 4 de la rampa de salida en la delantera. "
     "Mete los mandriles en el núcleo del rollo y fíjalos con los collarines. Deja caer el eje del "
     "rollo por las ranuras traseras de las placas. Recorrido del film: rollo, guía trasera, bajo las "
     "ruedas de presión, mesa de vacío y rampa de salida, por donde cae hacia delante.",
     ["M6 x 30 (4)", "Rodamientos 6005 (2) en los mandriles"]),
    ("electronica", "Electrónica, fuente y pantalla",
     ("electronica_", "panel_", "pantalla_"),
     (0, 0, 1), (-0.8, 1.3, 1.1),
     "Atornilla la bandeja de MDF de 10 mm a los largueros laterales y al travesaño central. Encima van "
     "la caja impresa con la SKR, la Raspberry Pi, el Pico y los convertidores, y la fuente de 24 V "
     "sujeta con sus dos bridas. El panel de red va en el larguero trasero y la seta de emergencia en "
     "el delantero. La pantalla va en la esquina delantera derecha: su pletina se atornilla a la placa y "
     "el brazo de la carcasa a la pletina.",
     ["M5 x 12 + tuerca en T M5 (6) para la bandeja", "Separadores M3 de nylon (16)", "M5 x 30 (3) para la pantalla"]),
    ("cables", "Cadena portacables y canaletas",
     ("canaleta_", "cadena_"),
     (0, 0, 1), (-1.0, 1.3, 1.0),
     "Pega o atornilla las canaletas impresas sobre los largueros y por dentro de las placas. Monta la "
     "bandeja de la cadena portacables sobre la viga y el brazo en el carro. Por la cadena van los "
     "cables de los cabezales, el sensor del encoder y los tubos de tinta. Separa la potencia (motores, "
     "24 V) de las señales (encoders, flat de los cabezales); el cable de los encoders, apantallado.",
     ["Tornillo para madera 3 x 12 para las canaletas", "Bridas"]),
    ("tinta", "Tinta: botellas, bombas y subdepósitos",
     ("tinta_",),
     (0, -1, 0), (1.3, -1.4, 0.9),
     "Atornilla las dos escuadras de la repisa a la ranura trasera del larguero trasero; la pata apoya "
     "en la mesa de trabajo. Encima van la caja de plástico, la base impresa y las 5 botellas de 1 L, "
     "con el blanco sobre el agitador. Por fuera de la placa izquierda atornilla los soportes de las "
     "bombas y de los subdepósitos, y la caja del driver. Recorrido de cada color: botella, bomba, "
     "subdepósito, cadena portacables y carro. Para cebar, se rellenan los subdepósitos con las bombas "
     "y se aspira desde los dampers con jeringa.",
     ["M5 x 12 + tuerca en T M5 (2) para la repisa", "M5 x 30 + arandela + tuerca (12) por la placa",
      "Clips de tubo (2)"]),
]

# Nombre base de la pieza (sin el índice final) -> (descripción, STL impreso o None)
CATALOG = {
    "placa_izq": ("Placa lateral izquierda, MDF 19 mm", None),
    "placa_der": ("Placa lateral derecha, MDF 19 mm", None),
    "larguero_izq": ("Larguero lateral izquierdo 4040", None),
    "larguero_der": ("Larguero lateral derecho 4040", None),
    "larguero_tras": ("Larguero trasero 4040", None),
    "larguero_del": ("Larguero delantero 4040", None),
    "travesano_central": ("Travesaño central 4040", None),
    "escuadra": ("Escuadra 4040", None),
    "pata": ("Pata niveladora M8", None),
    "viga_x": ("Viga X 4080", None),
    "tirante_sup": ("Tirante superior trasero 4040", None),
    "travesano_mesa": ("Travesaño de la mesa 4040", None),
    "guia_mgn12": ("Guía lineal MGN12", None),
    "soporte_motor_x": ("Soporte del motor X", "soporte_motor_x"),
    "soporte_tensor_x": ("Soporte del tensor X", "soporte_tensor_x"),
    "motor_x": ("Motor NEMA17 del eje X", None),
    "polea_motor_x": ("Polea GT2 20T del motor X", None),
    "polea_loca_x": ("Polea loca GT2 del tensor X", None),
    "correa_x": ("Correa GT2 10 mm del eje X", None),
    "patin": ("Patín MGN12H", None),
    "carro_placa": ("Placa del carro", "carro_placa"),
    "carro_bandeja": ("Bandeja de cabezales (ajuste de altura)", "carro_bandeja"),
    "carro_pinza_correa": ("Pinza de la correa", "carro_pinza_correa"),
    "cabezal": ("Cabezal Epson XP600 (maqueta)", None),
    "encoder_cinta": ("Cinta del encoder 180 LPI", None),
    "encoder_soporte_cinta_izq": ("Soporte izquierdo de la cinta del encoder", "encoder_soporte_cinta_izq"),
    "encoder_soporte_cinta_der": ("Soporte derecho de la cinta del encoder", "encoder_soporte_cinta_der"),
    "encoder_soporte_sensor": ("Soporte del sensor del encoder X", "encoder_soporte_sensor"),
    "encoder_sensor": ("Sensor del encoder X (H9730)", None),
    "final_x_bandera": ("Bandera de home X", "final_x_bandera"),
    "final_x_soporte": ("Soporte del sensor de home X", "final_x_soporte"),
    "encoder_y_soporte": ("Soporte del encoder Y", "encoder_y_soporte"),
    "encoder_y_iman": ("Imán diametral del encoder Y", None),
    "encoder_y_pcb": ("Placa AS5047P del encoder Y", None),
    "cadena_bandeja": ("Bandeja de la cadena portacables", "cadena_bandeja"),
    "cadena_portacables": ("Cadena portacables 10 x 20", None),
    "cadena_brazo": ("Brazo de la cadena en el carro", "cadena_brazo"),
    "mesa_placa": ("Placa perforada de aluminio de la mesa", None),
    "mesa_camara": ("Cámara de vacío impresa", "mesa_camara"),
    "ventilador": ("Ventilador 80 mm 24 V de la mesa", None),
    "eje_arrastre": ("Eje del rodillo de arrastre Ø12", None),
    "rodillo_arrastre": ("Rodillo de arrastre Ø30", None),
    "rodamiento_arrastre": ("Rodamiento 6001", None),
    "alojamiento_rodamiento": ("Alojamiento del rodamiento 6001", "rodillo_alojamiento_6001"),
    "presion_soporte": ("Soporte de la unidad de presión", "presion_soporte"),
    "presion_brazo": ("Brazo de la unidad de presión", "presion_brazo"),
    "presion_rueda": ("Rueda de presión (TPU)", "presion_rueda_tpu"),
    "presion_leva": ("Leva de levante", "presion_leva"),
    "presion_muelle": ("Muelle de la unidad de presión", None),
    "presion_palanca": ("Palanca de levante", "presion_palanca"),
    "eje_levante": ("Eje de levante Ø8", None),
    "soporte_motor_y": ("Soporte del motor Y", "soporte_motor_y"),
    "motor_y": ("Motor NEMA17 del eje Y", None),
    "polea_80t_y": ("Polea GT2 80T del rodillo", None),
    "polea_20t_y": ("Polea GT2 20T del motor Y", None),
    "correa_y": ("Correa GT2 6 mm del eje Y", None),
    "guia_trasera": ("Guía trasera Ø25", None),
    "guia_delantera": ("Guía delantera Ø25", None),
    "mesa_entrada": ("Segmento de la mesa de entrada", "mesa_entrada_segmento"),
    "mesa_salida": ("Segmento de la rampa de salida", "mesa_salida_segmento"),
    "eje_rollo_entrada": ("Eje del rollo Ø25", None),
    "rollo_entrada": ("Rollo de film DTF de 60 cm", None),
    "nucleo_entrada": ("Núcleo de cartón de 3\"", None),
    "mandril_entrada": ("Mandril del rollo", "rollo_mandril"),
    "collarin_entrada": ("Collarín del mandril (freno)", "rollo_collarin"),
    "collarin_placa_entrada": ("Collarín del eje en la placa", "rollo_collarin"),
    "film": ("Film DTF", None),
    "servicio_base": ("Base de la estación de servicio", "servicio_base"),
    "servicio_tapa": ("Tapas de limpieza (capping)", None),
    "electronica_bandeja": ("Bandeja de electrónica, MDF 10 mm", None),
    "electronica_caja": ("Caja de la electrónica", "electronica_caja"),
    "electronica_placa_skr": ("BTT SKR Mini E3 V3.0", None),
    "electronica_raspberry_pi": ("Raspberry Pi 3", None),
    "electronica_pico_encoder": ("Raspberry Pi Pico (encoders)", None),
    "electronica_conversor_5v": ("Convertidor 24 V a 5 V", None),
    "electronica_conversor_12v": ("Convertidor 24 V a 12 V", None),
    "electronica_fuente_24v": ("Fuente de 24 V", None),
    "electronica_ventilador": ("Ventilador 4010 de la caja", None),
    "electronica_brida_fuente": ("Brida de la fuente", "electronica_brida_fuente"),
    "panel_iec": ("Panel de la entrada de red", "panel_iec"),
    "panel_iec_conector": ("Conector IEC con interruptor y fusible", None),
    "panel_seta": ("Panel de la seta de emergencia", "panel_seta"),
    "panel_seta_pulsador": ("Seta de emergencia", None),
    "pantalla_carcasa": ("Carcasa de la pantalla", "pantalla_carcasa"),
    "pantalla_soporte": ("Pletina de la pantalla", "pantalla_soporte"),
    "pantalla_tactil": ("Pantalla táctil de 7\" (KlipperScreen)", None),
    "canaleta": ("Canaleta de cables con tapa", "canaleta_tramo_200"),
    "tinta_repisa": ("Repisa de las botellas, MDF 12 mm", None),
    "tinta_escuadra_repisa": ("Escuadra de la repisa", "tinta_escuadra_repisa"),
    "tinta_pata_repisa": ("Pata de la repisa", "tinta_pata_repisa"),
    "tinta_caja_botellas": ("Caja de plástico (bandeja antiderrames)", None),
    "tinta_base_botellas": ("Base de las botellas", "tinta_base_botellas"),
    "tinta_agitador": ("Agitador magnético", None),
    "tinta_botella": ("Botella de tinta de 1 L", None),
    "tinta_tapon": ("Tapón con salida de tubo y respiradero", None),
    "tinta_soporte_bombas": ("Soporte de las bombas", "tinta_soporte_bombas"),
    "tinta_bomba": ("Bomba peristáltica 12 V", None),
    "tinta_caja_driver": ("Caja del driver de las bombas", "tinta_caja_driver"),
    "tinta_soporte_subdepositos": ("Soporte de los subdepósitos", "tinta_soporte_subdepositos"),
    "tinta_subdeposito": ("Subdepósito con flotador", None),
    "tinta_flotador": ("Tapa con sensor de nivel", None),
    "tinta_tubo": ("Tubo de tinta", None),
    "tinta_tubos_carro": ("Mazo de tubos hacia el carro", None),
    "tinta_clip_tubos": ("Clip de tubos", "tinta_clip_tubos"),
}


def base_name(name):
    """placa_izq -> placa_izq, presion_brazo_3 -> presion_brazo, tinta_botella_C -> tinta_botella."""
    for key in sorted(CATALOG, key=len, reverse=True):
        if name == key or name.startswith(key + "_"):
            return key
    return re.sub(r"_[+-]?\w$", "", name)


def step_of(name):
    for i, (_, _, prefixes, *_rest) in enumerate(STEPS):
        if name.startswith(prefixes):
            return i
    return len(STEPS) - 1


def catalog(names):
    out = {}
    for n in names:
        key = base_name(n)
        label, stl = CATALOG.get(key, (key.replace("_", " ").capitalize(), None))
        suffix = n[len(key):].strip("_")
        if suffix and suffix.upper() in P.INK_COLORS:
            label += f" ({suffix.upper()})"
        out[n] = {"label": label, "step": step_of(n), "stl": f"stl/{stl}.stl" if stl else None}
    return out


def write_json(names, path):
    steps = [{"id": sid, "title": title, "explode": list(explode), "text": text, "hardware": hw,
              "image": f"img/montaje_{i + 1:02d}.png"}
             for i, (sid, title, _, explode, _, text, hw) in enumerate(STEPS)]
    data = {"steps": steps, "parts": catalog(names)}
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Montaje:", path)


def write_md(names):
    parts = catalog(names)
    lines = ["# Guía de montaje", "",
             "Generada por `cad/montaje.py` a partir del modelo. En "
             "[montaje.html](montaje.html) está la versión interactiva en 3D: pulsa una pieza "
             "para ver qué es, en qué paso va y descargar su STL.", "",
             "En cada esquema, lo montado en pasos anteriores sale en gris y lo de ese paso, en color.", ""]
    for i, (sid, title, _, _, _, text, hw) in enumerate(STEPS):
        lines += [f"## {i + 1}. {title}", "", f"![{title}](img/montaje_{i + 1:02d}.png)", "", text, ""]
        if hw:
            lines += ["**Tornillería y material:** " + "; ".join(hw) + ".", ""]
        counts = {}
        for n, info in parts.items():
            if info["step"] == i:
                key = (info["label"].split(" (")[0], info["stl"])
                counts[key] = counts.get(key, 0) + 1
        lines += ["| Pieza | Cant. | STL |", "|---|---:|---|"]
        for (label, stl), q in counts.items():
            link = f"[{Path(stl).name}]({stl})" if stl else ""
            lines.append(f"| {label} | {q} | {link} |")
        lines.append("")
    (DOCS / "montaje.md").write_text("\n".join(lines), encoding="utf-8")
    print("Guía:", DOCS / "montaje.md")
