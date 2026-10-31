# OpenPrinter — Plan de diseño

Impresora DTF (Direct To Film) open source, de rollo, ancho de film 600 mm
(configurable a 330 mm), diseñada desde cero: chasis de perfil de aluminio 4040,
piezas impresas en 3D y, más adelante, electrónica abierta (Raspberry Pi + MCU).

## Principios

- **Paramétrico**: todas las cotas salen de `cad/params.py`. Cambiar el ancho
  de film regenera toda la máquina.
- **Modular**: cada bloque (chasis, viga X, carro, mesa, arrastre, rollos,
  estación de servicio) es un módulo independiente que se puede rediseñar sin
  tocar los demás.
- **Fabricable en casa**: piezas imprimibles en 3D (PETG/ASA/PA-CF) y perfil
  4040 cortado a medida. Las placas que más adelante convenga hacer en aluminio
  se exportan también en DXF.
- **Iterativo**: primero volúmenes, después piezas reales, después detalle.

## Convenciones

- Unidades: mm.
- **X**: recorrido del carro (ancho de la máquina). X = 0 en el centro del film.
- **Y**: avance del film. El film entra por detrás (Y negativa) y sale por
  delante (Y positiva). Y = 0 en la línea de impresión (centro de las boquillas).
- **Z**: hacia arriba. Z = 0 en la superficie de la mesa (platen).
- El lado derecho (X positiva) aloja la estación de servicio (*home* del carro).

## Orden de diseño 3D

### Fase 0 — Mecánica sin cubierta

| # | Módulo | Contenido | Estado |
|---|--------|-----------|--------|
| 0.1 | Esqueleto de distribución | Volúmenes de todos los bloques, recorridos y holguras | Hecho |
| 0.2 | Chasis | Bastidor 4040, placas laterales, patas niveladoras | Hecho (pendiente validar con proveedor de corte) |
| 0.3 | Viga X | Viga 4080, 2 guías MGN12, soporte de motor y tensor impresos, correa GT2 | Primera versión, en revisión |
| 0.4 | Carro | Placa, bandeja de cabezales con ajuste de altura y pinza de correa, impresos | Primera versión, en revisión |
| 0.5 | Mesa (platen) | Placa perforada de aluminio, 4 cámaras de vacío impresas con ventilador | Primera versión, en revisión |
| 0.6 | Arrastre Y | Rodillo, 6 unidades de presión impresas con levante por levas, motor Y 4:1 | Primera versión, en revisión |
| 0.7 | Rollos | Ejes fijos, mandriles con rodamiento, collarines/freno, guías y mesa de entrada | Primera versión, en revisión |
| 0.8 | Estación de servicio | Base impresa y volúmenes reservados (tapas, limpiador, bomba) | Primera versión, en revisión |

**Hito fase 0**: chasis montado, el carro se desliza a lo largo de la viga y el
film avanza del rollo de entrada al de recogida, todo movido a mano.

### Fase 1 — Movimiento

Arquitectura y decisiones en [docs/fase1_movimiento.md](docs/fase1_movimiento.md).
Modelado en `cad/motion.py`: encoder X (cinta y sensor), final de carrera X,
encoder Y en el rodillo, cadena portacables con su bandeja y placa de
electrónica. Lista de compra en [docs/compra_fase1.md](docs/compra_fase1.md).

### Más adelante

- Driver del cabezal, sistema de tinta (rack de tanques ya reservado por fuera
  de la placa izquierda), estación de servicio funcional.
- Agitador de polvo y túnel de curado.
- Cubierta y cerramiento.

En el esqueleto solo se **reservan volúmenes** para estos elementos, para que el
diseño mecánico no los bloquee.

## Estructura del repositorio

```
OpenPrinter/
├── PLAN.md            este documento
├── cad/
│   ├── params.py      cotas globales
│   ├── lib.py         utilidades: perfil serie 40, escuadras, patas, colores
│   ├── layout.py      ensamblaje general (módulos detallados + volúmenes)
│   ├── chassis.py     chasis (fase 0.2): placas, bastidor, DXF y lista de corte
│   ├── xaxis.py       viga X (fase 0.3): guías, motor, tensor, correa
│   ├── carriage.py    carro (fase 0.4): placa, bandeja de cabezales, pinza
│   ├── platen.py      mesa de vacío (fase 0.5): placa perforada, cámaras
│   ├── yfeed.py       arrastre Y (fase 0.6): rodillo, presión, levante, motor Y
│   ├── rolls.py       rollos y guías (fase 0.7)
│   ├── service.py     estación de servicio y reserva de tinta (fase 0.8)
│   ├── motion.py      sensores, cadena y electrónica (fase 1)
│   ├── bom.py         listas de compra
│   ├── render_pv.py   renders de presentación
│   ├── web.py         modelo 3D de la web
│   ├── render.py      vistas PNG rápidas
│   └── ...            un módulo por bloque a medida que se detallen
└── out/               STEP / STL / vistas generadas (no se versiona)
```

## Cómo generar el modelo

```
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python cad\layout.py
.venv\Scripts\python cad\render.py
```

Genera en `out/`:

- `layout.step` / `layout.glb`: ensamblaje completo (FreeCAD, Fusion, etc.)
- `placa_lateral.dxf`: contorno y agujeros de las placas laterales, para corte
- `mesa_placa.dxf`: placa superior perforada de la mesa de vacío, para corte
- `lista_corte.csv`: perfiles a cortar con longitudes y mecanizados
- `stl/*.stl`: piezas impresas, listas para el laminador
- `layout_*.png`: vistas rápidas

## Chasis (0.2)

- Dos placas laterales con todos los agujeros de alineación: viga X, rodillo
  de arrastre, guías, eje de levante y ranuras abiertas para los ejes de los
  rollos (inclinadas para que el eje caiga a su asiento). Material según
  `SIDE_PLATE_MATERIAL`:
  - **MDF de 19 mm** (primera máquina, low cost): se cortan con la plantilla
    A4 de `docs/plantillas/placa_lateral_A4.pdf`. El rodamiento 6001 del
    rodillo va en un alojamiento impreso (`rodillo_alojamiento_6001`) por la
    cara interior, sujeto con 3 tornillos M4 pasantes. Los perfiles se
    atornillan con M8 x 35 y arandela ancha para no clavar el MDF.
  - **Aluminio de 10 mm** (5083 o 6082, corte láser o agua): el rodamiento va
    encajado en la placa.
- Bastidor inferior de 4040: largueros laterales atornillados a las placas,
  largueros delantero/trasero y travesaño central unidos con escuadras.
- Entre placas, atornillados a la testa (M8): viga X 4080, tirante superior
  trasero y dos travesaños que sostienen la mesa.
- Cuatro patas niveladoras M8 bajo los largueros laterales.
- Los perfiles que van entre placas deben cortarse todos a la misma longitud
  y a escuadra: de eso depende el paralelismo de las placas.

## Viga X (0.3)

- Dos guías MGN12 de 1000 mm en la cara delantera de la viga 4080, una sobre
  cada ranura (M3 con tuercas en T). La separación vertical de 40 mm entre
  guías absorbe el par del carro, que va en voladizo hacia delante.
- Correa GT2 de 10 mm en un plano horizontal por encima de la viga, para no
  estorbar al carro ni a las guías.
- Motor NEMA17 a la izquierda, eje hacia abajo, sobre un soporte impreso
  atornillado a la ranura superior de la viga (M5 con tuerca en T).
- Polea loca a la derecha en un soporte impreso con colisos: se tensa en X con
  un tornillo M4.

## Carro (0.4)

Todo impreso (PETG o ASA en fase 0; PA-CF o aluminio si hace falta más rigidez):

| Pieza | Tamaño aprox. (mm) | Fijación |
|---|---|---|
| `carro_placa` | 200 × 10 × 115 | 16 × M3 a 4 patines MGN12H |
| `carro_bandeja` | 180 × 127 × 60 | 4 × M4 en colisos verticales a insertos de la placa |
| `carro_pinza_correa` | 60 × 15 × 23 | 2 × M3 a insertos de la placa |
| `soporte_motor_x` | 56 × 69 × 31 | 2 × M5 a la viga, 4 × M3 al motor |
| `soporte_tensor_x` | 54 × 69 × 31 | 2 × M5 a la viga |

- **Ajuste de altura cabezal-film**: la bandeja sube y baja ±4 mm en los
  colisos. Se fija con 4 M4; más adelante se puede añadir un tornillo de
  reglaje o una leva.
- **Cabezales**: dos XP600 separados 50 mm en X, colgando por ventanas en la
  bandeja y apoyados en su pestaña.
- **Pendiente de verificar con un cabezal XP600 real** (son cotas aproximadas):
  tamaño del cuerpo, forma y posición de la pestaña y de sus tornillos, y
  distancia de la cara de boquillas a la pestaña. Hasta entonces la bandeja no
  se debe imprimir en definitiva; sí sirve como prototipo de ajuste.
- El volumen reservado sobre los cabezales es para dampers, tubos de tinta y la
  cadena portacables.

## Mesa de vacío (0.5)

- Placa superior de aluminio de 3 mm, 640 × 225 mm, con unos 800 agujeros de
  2 mm a paso de 12,5 mm (DXF). Va atornillada con M3 avellanados a insertos.
- Debajo, 4 cámaras impresas iguales de 160 × 225 × 37 mm (`mesa_camara.stl`,
  imprimir 4). Tienen pilares que sostienen la placa para que no se hunda.
- Cada cámara lleva su ventilador de 80 mm debajo, entre los dos travesaños.
  Son 4 zonas independientes: con film más estrecho se apagan las de los lados.
- Las cámaras se atornillan a los travesaños de mesa (M5 con tuerca en T). Las
  juntas se sellan con cinta de espuma.

## Arrastre Y (0.6)

- **Rodillo**: tubo de Ø30 mm sobre eje de Ø12 que gira en rodamientos 6001
  alojados en las placas. La superficie lleva recubrimiento abrasivo (grit) o
  goma fina; hay que probar cuál agarra mejor el PET sin marcarlo.
- **Presión**: 6 unidades impresas colgadas de la ranura inferior de la viga
  (M5). Cada una tiene:
  - un soporte con dos mejillas;
  - un brazo basculante sobre un pasador M3;
  - una rueda de TPU sobre un rodamiento 625 (eje M5);
  - un muelle de compresión de Ø6 bajo la cola del brazo, que hace bajar la
    rueda contra el rodillo.
- **Levante**: un eje de Ø8 atraviesa todas las unidades y las dos placas, con
  una leva excéntrica impresa por unidad. Con la palanca exterior, las levas
  empujan la cola de los brazos y las ruedas suben unos 2 mm para meter el film.
- **Motor Y**: NEMA17 en un soporte impreso por fuera de la placa derecha, con
  reducción 4:1 por correa GT2 de 6 mm (20T a 80T). Teóricamente da unos
  7 µm por micropaso (1/16); la precisión real la dará un encoder en el rodillo
  (fase 1). Los colisos del soporte sirven para tensar la correa.
- Las dos placas laterales llevan los agujeros del motor Y y del eje de
  levante. El motor se puede montar a cualquier lado.

| Pieza impresa | Cantidad | Material |
|---|---|---|
| `mesa_camara` | 4 | PETG |
| `presion_soporte` | 6 | PETG/ASA |
| `presion_brazo` | 6 | PETG/ASA |
| `presion_rueda_tpu` | 6 | TPU 95A |
| `presion_leva` | 6 | PETG |
| `presion_palanca` | 1 | PETG |
| `soporte_motor_y` | 1 | PETG/ASA |

## Rollos y guías (0.7)

- **Ejes de los rollos**: tubo de aluminio de Ø25 que no gira. Se deja caer en
  las ranuras inclinadas de las placas y no se puede salir en X gracias a dos
  collarines impresos por fuera.
- **Mandriles**: 2 por rollo, impresos. Entran 30 mm en el núcleo de cartón de
  3" y giran sobre el eje con un rodamiento 6005 (25 × 47 × 12).
- **Collarines**: uno junto a cada mandril fija su posición para el ancho de
  film que uses. En el rollo de entrada ese collarín hace de freno, con un
  fieltro contra el mandril, para dar tensión al film.
- **Guías**: dos tubos de Ø25 entre placas, detrás y delante de la mesa,
  atornillados con M6 a sus testas. El film pasa por encima con su cara superior
  a la altura de la mesa.
- **Mesa de entrada**: 4 segmentos impresos que se enganchan a presión en la
  guía trasera y llevan el film hasta el rodillo de arrastre.
- La recogida motorizada es de la fase 1; aquí solo se reserva el volumen del
  motor, por dentro de la placa izquierda.

## Estación de servicio (0.8)

- Base impresa a la derecha del film, atornillada a los dos travesaños de mesa
  (M5), justo bajo el carro aparcado en home (X = 405 mm).
- Volúmenes reservados: dos tapas bajo los cabezales (5 mm por debajo de las
  boquillas cuando están bajadas), el elevador de las tapas, el limpiador a la
  izquierda de las tapas (el carro lo cruza al salir de home) y la bomba de
  purga debajo de la base.
- El mecanismo se diseña en la fase 4, junto con el sistema de tinta.

## Piezas impresas de la fase 0

| Pieza | Cantidad | Material |
|---|---|---|
| `carro_placa` | 1 | PETG/ASA |
| `carro_bandeja` | 1 | PETG/ASA (prototipo hasta medir el XP600) |
| `carro_pinza_correa` | 1 | PETG |
| `soporte_motor_x` | 1 | PETG/ASA |
| `soporte_tensor_x` | 1 | PETG/ASA |
| `mesa_camara` | 4 | PETG |
| `presion_soporte` | 6 | PETG/ASA |
| `presion_brazo` | 6 | PETG/ASA |
| `presion_rueda_tpu` | 6 | TPU 95A |
| `presion_leva` | 6 | PETG |
| `presion_palanca` | 1 | PETG |
| `soporte_motor_y` | 1 | PETG/ASA |
| `rollo_mandril` | 4 | PETG |
| `rollo_collarin` | 8 | PETG |
| `mesa_entrada_segmento` | 4 | PETG |
| `servicio_base` | 1 | PETG |

**Hito de diseño**: la fase 0 está modelada completa y sin choques en todo el
recorrido del carro. El siguiente paso es validarla con piezas reales: medir un
XP600, imprimir el carro y una unidad de presión, y pedir presupuesto de las
placas.

## Licencias

- Hardware (modelos CAD, planos, DXF, STL): CERN-OHL-S v2 (`LICENSE-HARDWARE`)
- Software y firmware: GPL-3.0 (`LICENSE`)
