"""Cotas globales de OpenPrinter (mm). Convenciones de ejes en PLAN.md.

Solo se tocan los valores de la sección "Entradas"; lo demás se deriva.
"""

# --- Entradas ---------------------------------------------------------------

# Film
FILM_WIDTH = 600            # ancho del rollo (330 para versión A3)
PRINT_WIDTH = 580           # ancho imprimible
FILM_CORE_OD = 86           # núcleo de cartón de 3" (interior 76,2)
FILM_ROLL_OD_MAX = 130      # ~100 m de film de 75 µm

# Cabezales (maqueta XP600: cotas aproximadas, verificar con un cabezal real)
HEAD_COUNT = 1              # cabezales montados: 1 = CMYK+WW (ver docs/cabezales.md)
HEAD_SLOTS = 2              # huecos en carro y recorrido: el 2.º (blanco) se añade sin tocar el chasis
HEAD_SIZE = (40, 33, 60)    # cuerpo X, Y, Z desde la cara de boquillas
HEAD_FLANGE = (40, 47, 3)   # pestaña de fijación X, Y, espesor (tornillos delante/detrás)
HEAD_FLANGE_Z = 35          # cara de boquillas -> cara inferior de la pestaña
HEAD_PITCH_X = 50           # separación entre centros de cabezal
HEAD_GAP = 2.0              # boquilla-film
HEAD_ADJUST = 4             # recorrido del ajuste de altura (+/-)

# Carro y recorrido
CARRIAGE_W = 200            # ancho del carro en X
ACCEL_ZONE = 60             # aceleración/frenado a cada lado del área impresa
OVERTRAVEL = 10             # margen de seguridad en los extremos
SERVICE_ZONE = 150          # longitud de la estación de servicio en X
SERVICE_MARGIN = 30         # separación borde de film - estación
BEAM_END = 60               # soportes extremos de la viga (motor / tensor)

# Perfil y placas
PROFILE = 40                # perfil 4040
BEAM_SECTION = (40, 80)     # viga X 4080: Y, Z
SIDE_PLATE_MATERIAL = "mdf"     # "mdf" (fase 1, low cost) o "aluminio"
SIDE_PLATE_T = 19 if SIDE_PLATE_MATERIAL == "mdf" else 10
GRIT_HOUSING = (56, 12, 22)     # alojamiento impreso del 6001 en MDF: Ø, espesor, radio tornillos
GRIT_SHAFT_CLEAR = 16           # paso del eje del rodillo por el MDF
PLATE_FILLET = 10
M8_CLEAR = 8.5
M6_CLEAR = 6.5
M5_CLEAR = 5.5
GRIT_BEARING_OD = 28        # rodamiento 6001 (12x28x8)
ROLL_SHAFT_D = 25           # ejes de los rollos
ROLL_SLOT_RISE = 8          # grados de subida de la ranura del eje hacia el borde

# Posiciones en Y (avance del film) y Z (altura)
BEAM_Y_FRONT = -110         # cara delantera de la viga, donde va la guía
BEAM_Z_BOTTOM = 40

# Guías lineales: 2 x MGN12 en la cara delantera de la viga, 2 patines MGN12H cada una
RAIL_W, RAIL_H = 12, 8
RAIL_LENGTH = 1000
RAIL_Z = (BEAM_Z_BOTTOM + 20, BEAM_Z_BOTTOM + 60)   # sobre las ranuras del 4080
BLOCK_W, BLOCK_L, BLOCK_H = 27, 45.4, 13            # BLOCK_H: base guía -> cara patín
BLOCK_HOLES = 20                                    # 4 x M3 en cuadrado de 20
BLOCK_SPACING_X = 120                               # entre centros de patines

# Correa GT2 10 mm sobre la viga, motor a la izquierda y tensor a la derecha
BELT_W = 10
PULLEY_PD = 12.73           # 20 dientes
BELT_FRONT_Y = -103         # tramo unido al carro
BELT_Z = 133                # centro de la correa
NEMA = 42.3                 # NEMA17; motor eje abajo sobre soporte impreso
NEMA_LEN = 48

# Carro impreso (PETG/ASA; PA-CF más adelante)
CARRIAGE_PLATE_T = 10
CARRIAGE_TOP_Z = 145
SHELF_T = 10                # bandeja de cabezales
SHELF_FRONT_Y = 40
SHELF_FLANGE_H = 60         # ala vertical de la bandeja (ajuste de altura)

GRIT_ROLLER_D = 30          # rodillo de arrastre
GRIT_ROLLER_Y = -125        # bajo la viga: las palancas de presión cuelgan de ella

PLATEN_Y = (-105, 120)      # mesa de impresión
PLATEN_DEPTH = 40           # cámara de vacío bajo la mesa
PLATEN_MARGIN_X = 20        # sobrante de mesa a cada lado del film
PLATEN_RAIL_Y = (-60, 80)   # travesaños 4040 que sostienen la mesa
PLATEN_TOP_T = 3            # placa superior de aluminio perforada
PLATEN_SEGMENTS = 4         # cámaras impresas, una zona de vacío por ventilador
PLATEN_HOLE_D = 2.0         # agujeros de succión
PLATEN_HOLE_PITCH = 12.5
PLATEN_FAN = 80             # ventilador por segmento

# Arrastre Y
GRIT_SHAFT_D = 12           # eje del rodillo (rodamientos 6001 en las placas)
PINCH_COUNT = 6             # unidades de presión a lo largo del film
PINCH_WHEEL_D = 22          # rueda de TPU sobre rodamiento 625
PINCH_WHEEL_W = 8
PINCH_PIVOT = (-140, 20)    # eje de giro del brazo (Y, Z)
LIFT_SHAFT = (-161, 34)     # eje de levante con levas (Y, Z), Ø8
LIFT_SHAFT_D = 8
CAM_D, CAM_ECC = 16, 4      # leva excéntrica: diámetro y excentricidad
Y_PULLEY_PD = (12.73, 50.93)   # GT2 20T en motor, 80T en rodillo (4:1)
Y_MOTOR_DZ = 70             # motor Y por debajo del rodillo
Y_BELT_W = 6

# Fase 1: sensores y cableado
ENC_STRIP_Y = -104          # cinta del encoder X (cara delantera de la viga, entre guías)
ENC_STRIP_Z = (74, 86)      # 12 mm (cinta de 15 mm recortada), entre los patines
ENC_STRIP_X = (-545, 545)
ENC_SENSOR_Z = (72, 90)
GRIT_SHAFT_OUT_L = 13       # el eje del rodillo sale por fuera de la placa izquierda (encoder Y)
CHAIN_W, CHAIN_H = 27, 15   # cadena portacables exterior (interior 10 x 20)
CHAIN_R = 18                # radio de curvatura (cadenas 10 x 20 comerciales: R18)
CHAIN_FIX_X = 5             # anclaje fijo, centro del recorrido
CHAIN_Y = (-187, -160)
CHAIN_TRAY_X = (-560, 40)     # llega a la placa izquierda: canaleta y tubos de tinta
ELEC_PLATE = (-545, 555, -60, 100)   # bandeja inferior: apoya en los largueros laterales y el central

# Tinta a granel, detrás: botellas de 1 L en una caja comprada (bandeja
# antiderrames) sobre una repisa colgada del larguero trasero. Una bomba
# peristáltica por color rellena un subdepósito con flotador, fijado a la placa
# izquierda a altura fija: él fija la presión en las boquillas, no la botella.
INK_COLORS = ("C", "M", "Y", "K", "W")
INK_BOX = (395, 255, 155)           # caja de referencia (Really Useful Box 9 L), exterior X, Y, Z
INK_BOX_BOTTOM = (355, 215)         # base exterior (las paredes tienen desmoldeo)
INK_BOX_X0 = 320                    # a la derecha, fuera del ancho del rollo (se carga desde atrás)
INK_SHELF_DEPTH = 270               # repisa de MDF 12 mm detrás del larguero trasero
INK_BOTTLE = (90, 90, 190)          # botella de tinta de 1 L (cuerpo)
INK_STIRRER = (100, 100, 25)        # agitador magnético bajo la botella de blanco
INK_PUMP = (40, 33, 50)             # bomba peristáltica 12 V (cuerpo + cabezal)
INK_SUBTANK = (55, 25, 90)          # subdepósito con flotador: X, Y, Z (~100 ml)
INK_SUBTANK_Y0 = -355               # banco de subdepósitos, por fuera de la placa izquierda
INK_SUBTANK_Z0 = -95
INK_LEVEL_DROP = 42                 # nivel del flotador por debajo de las boquillas
INK_TUBE_HOLE = (-185, 102, 20)     # paso de tubos en las placas, sobre la bandeja de la cadena (Y, Z, Ø)

# Pantalla táctil (KlipperScreen en la Raspberry Pi): esquina delantera derecha
SCREEN_SIZE = (194, 110, 20)        # módulo de 7" (ajustar a la que se compre): ancho, alto, fondo
SCREEN_TILT = 20                    # grados hacia atrás

# Electrónica: placa de MDF sobre el travesaño central, bajo la mesa
ELEC_PLATE_T = 10
PSU_SIZE = (215, 115, 50)           # fuente de 24 V del inventario (medir la real)
SKR_SIZE = (101.5, 72)              # BTT SKR Mini E3 V3.0
PI_SIZE = (85, 56)                  # Raspberry Pi 3
CABLE_DUCT = (20, 15)               # canaleta impresa: ancho, alto

REAR_GUIDE_D = 25
REAR_GUIDE_Y = -200
UNWIND_ROLL = (-280, -150)  # centro (Y, Z) del rollo de entrada
OUTPUT_EDGE = (335, -80)    # borde de la rampa de salida: el film impreso cae por delante
FRONT_GUIDE_Y = 135         # tubo de salida delante de la mesa (mismo Ø que la trasera)
CORE_ID = 76.2              # interior del núcleo de 3"
CHUCK_FLANGE_D = 100        # mandriles impresos con rodamiento 6005 (25x47x12)
CHUCK_INSERT = 30           # longitud que entra en el núcleo
CHUCK_BEARING = (47, 12)

FRAME_Y = (-360, 330)       # extensión de las placas laterales
FRAME_Z = (-260, 170)
FOOT_H = 23                 # pata niveladora: base 8 + rosca vista 15

# --- Derivadas --------------------------------------------------------------

HEAD_GROUP_W = (HEAD_SLOTS - 1) * HEAD_PITCH_X + HEAD_SIZE[0]

# Posiciones del centro del carro
SERVICE_X0 = FILM_WIDTH / 2 + SERVICE_MARGIN
SERVICE_X1 = SERVICE_X0 + SERVICE_ZONE
CARRIAGE_HOME_X = (SERVICE_X0 + SERVICE_X1) / 2
CARRIAGE_X_MIN = -(PRINT_WIDTH / 2 + HEAD_GROUP_W / 2 + ACCEL_ZONE + OVERTRAVEL)
CARRIAGE_X_MAX = max(PRINT_WIDTH / 2 + HEAD_GROUP_W / 2 + ACCEL_ZONE,
                     CARRIAGE_HOME_X) + OVERTRAVEL

# Viga X y separación interior entre placas laterales
BEAM_X0 = CARRIAGE_X_MIN - CARRIAGE_W / 2 - BEAM_END
BEAM_X1 = CARRIAGE_X_MAX + CARRIAGE_W / 2 + BEAM_END
BEAM_LENGTH = BEAM_X1 - BEAM_X0
BEAM_Y_BACK = BEAM_Y_FRONT - BEAM_SECTION[0]
BEAM_Z_TOP = BEAM_Z_BOTTOM + BEAM_SECTION[1]

CARRIAGE_PLATE_Y = BEAM_Y_FRONT + BLOCK_H
RAIL_X0 = (CARRIAGE_X_MIN + CARRIAGE_X_MAX) / 2 - RAIL_LENGTH / 2
PULLEY_Y = BELT_FRONT_Y - PULLEY_PD / 2
MOTOR_X = BEAM_X0 + BEAM_END / 2 - 2
IDLER_X = BEAM_X1 - BEAM_END / 2
SHELF_Z = HEAD_GAP + HEAD_FLANGE_Z - SHELF_T   # cara inferior de la bandeja
PLATEN_RAIL_Z = -PLATEN_DEPTH - PROFILE / 2

PLATEN_X = (-FILM_WIDTH / 2 - PLATEN_MARGIN_X, FILM_WIDTH / 2 + PLATEN_MARGIN_X)


def summary():
    rows = [
        ("Ancho de film", FILM_WIDTH),
        ("Recorrido del carro", CARRIAGE_X_MAX - CARRIAGE_X_MIN),
        ("Posición home del carro", CARRIAGE_HOME_X),
        ("Longitud viga X", BEAM_LENGTH),
        ("Guías MGN12", RAIL_LENGTH),
        ("Ancho total", BEAM_LENGTH + 2 * SIDE_PLATE_T),
        ("Fondo total", FRAME_Y[1] - FRAME_Y[0]),
        ("Alto total", FRAME_Z[1] - FRAME_Z[0] + FOOT_H),
    ]
    for name, value in rows:
        print(f"{name:<26}{value:>8.0f} mm")


if __name__ == "__main__":
    summary()
