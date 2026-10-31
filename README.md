# OpenPrinter

Impresora **DTF (Direct To Film)** de código y hardware abiertos, diseñada desde
cero para construirse con herramientas de *maker*: impresora 3D, perfil de
aluminio 4040 y placas cortadas por un servicio de láser o agua.

![OpenPrinter, fase 0](docs/img/general.png)

**[Web del proyecto con visor 3D interactivo](https://worktechlabs.github.io/OpenPrinter/)** ·
**[Lista de compra de la fase 0](docs/compra_fase0.md)** ·
**[Plan de diseño](PLAN.md)**

*Open source DTF (Direct To Film) printer, designed from scratch to be built
with maker tools. English summary at the end.*

> **Estado: fase 0, diseño mecánico.** Todavía no se ha fabricado ni probado
> nada. Las cotas pueden cambiar en cualquier momento. No compres material
> basándote en este repositorio hasta que una fase esté marcada como validada.

## Qué es DTF

La impresión DTF imprime con tinta pigmentada (CMYK más una capa de blanco) sobre
un film de PET. Sobre la tinta húmeda se espolvorea un adhesivo termofusible en
polvo, se cura con calor y el transfer resultante se plancha sobre la prenda.
Sirve para algodón, poliéster y mezclas, en prendas claras u oscuras.

## Por qué este proyecto

Las impresoras DTF comerciales de gama baja suelen ser impresoras de oficina
modificadas. Su mayor problema es la **tinta blanca**: el dióxido de titanio se
deposita y obstruye el cabezal si no circula. Además suelen tener firmware
cerrado y contadores de mantenimiento.

OpenPrinter quiere ser una máquina que se pueda entender, reparar y mejorar
pieza a pieza, con la circulación del blanco y el mantenimiento resueltos desde
el diseño.

## Alcance

### Objetivos

- **Formato**: rollo de film de 600 mm de ancho, configurable a 330 mm (A3+)
  cambiando un solo parámetro.
- **Color**: CMYK + blanco con dos cabezales piezoeléctricos Epson XP600.
- **Fabricación accesible**:
  - Chasis de perfil 4040 y dos placas laterales de aluminio (DXF incluido).
  - Carro, soportes y piezas auxiliares impresas en 3D.
  - Componentes comerciales estándar: guías MGN12, correa GT2, motores NEMA,
    rodamientos.
- **Diseño paramétrico y abierto**: CAD en Python (CadQuery). Todas las cotas
  salen de un único archivo y se exportan a STEP, STL y DXF.
- **Electrónica abierta**: Raspberry Pi como host y un microcontrolador
  (RP2040 o STM32) para el movimiento y la sincronización del disparo con un
  encoder lineal.
- **Software abierto**: un RIP propio que genere la capa de blanco, el tramado
  y las pasadas entrelazadas.
- **Driver de cabezal abierto**, el objetivo de investigación a largo plazo:
  una placa que genere la forma de onda y los datos del XP600 sin depender de
  placas cerradas.
- **Mantenimiento integrado**:
  - Recirculación y agitación de la tinta blanca.
  - Control de presión negativa.
  - Estación de servicio (*capping*, limpieza y purga).
- **Postproceso**: agitador de polvo y túnel de curado, como módulos aparte.

### Fuera de alcance

- No es una copia ni una modificación de ninguna impresora comercial.
- No se incluye firmware, documentación ni software propietario de Epson ni de
  terceros. Solo mediciones y desarrollos propios.
- No es un producto terminado ni certificado. Se ofrece sin garantía (ver
  licencias).
- Los cabezales térmicos (tipo HP45) solo se usarán, si acaso, para probar el
  movimiento y el software en papel. No sirven para la tinta DTF de producción.

## Hoja de ruta

| Fase | Contenido | Estado |
|---|---|---|
| 0 | Mecánica sin cubierta: chasis, viga X, carro, mesa de vacío, arrastre, rollos | Diseño completo, falta validar con piezas reales |
| 1 | Movimiento: motores, encoder, electrónica de control, firmware | Pendiente |
| 2 | Software: RIP abierto, primera impresión en papel | Pendiente |
| 3 | Cabezal XP600: estudio de la señal y placa driver abierta | Pendiente |
| 4 | Tinta y servicio: presión negativa, circulación del blanco, estación de servicio | Pendiente |
| 5 | Postproceso: agitador de polvo y túnel de curado | Pendiente |
| 6 | Cubierta y cerramiento | Pendiente |

El detalle de la fase 0, con las convenciones, los módulos y las decisiones de
diseño, está en [PLAN.md](PLAN.md).

### Progreso de la fase 0

| # | Módulo | Estado |
|---|---|---|
| 0.1 | Esqueleto de distribución | Hecho |
| 0.2 | Chasis (placas laterales, bastidor 4040) | Hecho, falta validar con proveedor |
| 0.3 | Viga X (guías MGN12, motor, tensor, correa) | Primera versión |
| 0.4 | Carro impreso con ajuste de altura | Primera versión, faltan cotas reales del XP600 |
| 0.5 | Mesa de vacío (4 zonas con ventilador) | Primera versión |
| 0.6 | Arrastre Y (rodillo, presión con levante, motor 4:1) | Primera versión |
| 0.7 | Rollos, mandriles, freno y guías | Primera versión |
| 0.8 | Estación de servicio (base y volúmenes reservados) | Primera versión |

## Cómo es

| | |
|---|---|
| ![Sección lateral](docs/img/lateral.png) | ![Vista trasera](docs/img/general_trasera.png) |
| **Sección lateral**: rollo de entrada, guía y mesa de entrada, rodillo con presión, mesa de vacío, guía delantera y rollo de recogida | **Vista trasera**: viga 4080 con guías MGN12, motor X y correa |
| ![Carro](docs/img/carro.png) | ![Mesa de vacío](docs/img/mesa.png) |
| **Carro impreso** con dos XP600 (maqueta) y ajuste de altura | **Mesa de vacío**: placa perforada sobre 4 cámaras con ventilador |
| ![Unidad de presión](docs/img/presion.png) | ![Motor Y](docs/img/motor_y.png) |
| **Unidad de presión** con leva de levante | **Motor Y** con reducción 4:1 |

El modelo 3D completo está en [`docs/model/openprinter.glb`](docs/model/openprinter.glb)
(GitHub lo muestra en 3D al abrirlo) y en la [web del proyecto](https://worktechlabs.github.io/OpenPrinter/).

## Lista de compra

La [lista de compra de la fase 0](docs/compra_fase0.md) se calcula a partir del
modelo: perfiles con sus longitudes, placas, guías, correas, rodamientos, ejes,
tornillería y gramos de filamento. Una primera estimación orientativa ronda los
**700 €** de material y filamento, sin cabezales ni electrónica. También está en
[CSV](docs/compra_fase0.csv).

## Medidas principales (film de 600 mm)

| | |
|---|---|
| Ancho imprimible | 580 mm |
| Recorrido del carro | 820 mm |
| Dimensiones exteriores | ~1160 × 690 × 455 mm (sobremesa) |
| Guías | 2 × MGN12, 1000 mm |
| Placas laterales | 2 × aluminio de 10 mm, 690 × 430 mm |

## Cómo generar el modelo

Requiere Python 3.11.

```
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python cad\layout.py      # STEP, GLB, DXF, STL, lista de corte
.venv\Scripts\python cad\bom.py         # lista de compra (docs/)
.venv\Scripts\python cad\render_pv.py   # renders de presentación (docs/img/)
.venv\Scripts\python cad\web.py         # modelo 3D de la web (docs/model/)
.venv\Scripts\python cad\render.py      # vistas rápidas de trabajo (out/)
```

En Linux o macOS se usa `.venv/bin/` en lugar de `.venv\Scripts\`.

Se genera en `out/` (no se versiona):

| Archivo | Contenido |
|---|---|
| `layout.step`, `layout.glb` | Ensamblaje completo, para FreeCAD, Fusion, etc. |
| `placa_lateral.dxf` | Placa lateral, lista para cortar |
| `mesa_placa.dxf` | Placa perforada de la mesa de vacío |
| `lista_corte.csv` | Perfiles con longitudes y mecanizados |
| `stl/*.stl` | Piezas impresas |
| `layout_*.png` | Vistas rápidas |

## Estructura

```
cad/
├── params.py     cotas globales (lo único que hay que tocar para escalar)
├── lib.py        perfil serie 40, escuadras, patas, utilidades
├── layout.py     ensamblaje general y exportación
├── chassis.py    chasis (0.2)
├── xaxis.py      viga X (0.3)
├── carriage.py   carro (0.4)
├── platen.py     mesa de vacío (0.5)
├── yfeed.py      arrastre Y (0.6)
├── rolls.py      rollos y guías (0.7)
├── service.py    estación de servicio (0.8)
├── bom.py        lista de compra
├── render_pv.py  renders de presentación
├── web.py        modelo 3D de la web
└── render.py     vistas rápidas de trabajo
docs/
├── index.html    web del proyecto (GitHub Pages)
├── compra_fase0.md / .csv
├── img/          renders
└── model/        openprinter.glb
```

## Seguridad

- **Polvo adhesivo y curado**: al calentarse desprende humos. Trabaja con
  extracción o filtro de carbón y nunca cures en un espacio cerrado sin
  ventilación.
- **Tintas**: usa guantes y gafas, y consulta la ficha de seguridad de la tinta
  que compres.
- **Driver del cabezal**: trabaja con tensiones de 30–40 V y corrientes de pico
  altas. Cuando se publique, sigue sus instrucciones.
- **Partes móviles**: el carro se mueve rápido. Durante las pruebas, mantén las
  manos fuera de su recorrido.

## Contribuir

Se aceptan issues y pull requests. Especialmente útil ahora:

- Mediciones reales del cabezal XP600: cuerpo, pestaña, tornillos y altura de
  las boquillas.
- Revisión del diseño mecánico: rigidez, fabricabilidad, costes.

No subas documentación, firmware ni archivos con copyright de fabricantes.
Las mediciones, fotos y análisis propios sí son bienvenidos.

## Licencias

- **Hardware** (modelos CAD, planos, DXF, STL): CERN-OHL-S v2, en
  [LICENSE-HARDWARE](LICENSE-HARDWARE).
- **Software y firmware**: GPL-3.0, en [LICENSE](LICENSE).

---

## English summary

OpenPrinter is an open source **DTF (Direct To Film) printer** designed from
scratch for makers:

- 600 mm roll film, configurable to 330 mm (A3+).
- CMYK + white with two Epson XP600 piezo heads.
- 4040 aluminium extrusion frame, laser or waterjet-cut side plates and
  3D-printed carriage and brackets.
- Parametric CAD in Python (CadQuery), exported to STEP, STL and DXF.
- Planned: open electronics (Raspberry Pi + RP2040/STM32), an open RIP, an
  open XP600 head driver, white ink recirculation, and powder/curing modules.

**Status:** phase 0, mechanical design only. Nothing has been built or tested
yet. Licences: CERN-OHL-S v2 for hardware, GPL-3.0 for software.
