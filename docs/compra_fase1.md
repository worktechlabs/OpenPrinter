# Lista de compra: fase 1

Generada por `cad/bom.py` a partir del modelo (film de 600 mm). Si cambias `params.py`, vuelve a generarla.

> Los precios son **orientativos**, para hacerse una idea del presupuesto y
> comparar opciones. No son un presupuesto: compruébalos con tu proveedor.


## Control

| Artículo | Especificación | Cant. | € aprox. | Notas |
|---|---|---:|---:|---|
| BTT SKR Mini E3 V3.0 | 4 x TMC2209, Klipper | 1 | 0 | del inventario |
| Raspberry Pi 3 o superior | con tarjeta microSD de 16 GB | 1 | 0 | ya disponible |
| Raspberry Pi Pico | RP2040 | 1 | 5 | monitor del encoder X |

## Motores

| Artículo | Especificación | Cant. | € aprox. | Notas |
|---|---|---:|---:|---|
| Motor NEMA17 | 40 mm | 2 | 0 | X e Y; del inventario (Creality 42-40, 42HD4041) |

## Sensores

| Artículo | Especificación | Cant. | € aprox. | Notas |
|---|---|---:|---:|---|
| Cinta de encoder 180 LPI | 1200 mm | 1 | 15 | recambio de plóter de gran formato, o de impresoras rotas |
| Resistencias 10 kΩ y 20 kΩ | divisor 5 V a 3,3 V | 2 | 0 | canales A y B del encoder X hacia el Pico, si el sensor es de 5 V |
| Sensor de encoder de cuadratura | tipo H9730/H9740, 180 LPI | 1 | 6 | o sacado de una impresora rota |
| Placa AS5047P + imán diametral | imán 6 x 2,5 mm | 1 | 15 | encoder Y |
| Sensor óptico de horquilla | tipo TCST2103, módulo | 1 | 2 | final de carrera X |
| Sensor reflexivo TCRT5000 | módulo | 1 | 1 | detección de film |
| Microinterruptor | con palanca | 1 | 1 | palanca de presión |

## Cableado

| Artículo | Especificación | Cant. | € aprox. | Notas |
|---|---|---:|---:|---|
| Cadena portacables | 10 x 20 mm, 600 mm | 1 | 8 |  |
| Cable apantallado 4 hilos | 2 m | 2 | 4 | encoders |
| Alargadores de motor y conectores JST |  | 1 | 10 |  |

## Alimentación

| Artículo | Especificación | Cant. | € aprox. | Notas |
|---|---|---:|---:|---|
| Fuente 24 V | de impresora 3D, 200 W o más | 1 | 0 | del inventario |
| Convertidor 24 V a 5 V | 5 A | 1 | 8 | Raspberry Pi y Pico |
| Seta de emergencia NC | 22 mm, con caja | 1 | 8 | corta los 24 V de los motores |
| Conector IEC con interruptor y fusible |  | 1 | 5 |  |

## Montaje

| Artículo | Especificación | Cant. | € aprox. | Notas |
|---|---|---:|---:|---|
| Bandeja inferior de electrónica | MDF 10 mm, 1100 x 160 mm | 1 | 4 | apoya en los largueros laterales y el central |
| Convertidor 24 V a 12 V | 5 A | 1 | 6 | ventiladores 4010 y bombas de tinta |
| Tapa de ranura 8 mm | 2 m | 1 | 6 | cables de sensores por las ranuras de la viga |
| Bridas y portabridas adhesivos |  | 1 | 4 |  |
| Separadores M3 de nylon | 6 mm | 16 | 2 |  |
| Tuerca en T M5 + tornillo M5 |  | 11 | 3 | placa de electrónica y bandeja |
| Inserto térmico M3 + tornillo M3 |  | 12 | 2 | soportes de sensores y brazo |

## Pantalla

| Artículo | Especificación | Cant. | € aprox. | Notas |
|---|---|---:|---:|---|
| Pantalla táctil 7" HDMI + USB | 1024 x 600, KlipperScreen | 1 | 35 | medir la que se compre y ajustar SCREEN_SIZE |
| Cable HDMI fino + USB | 1,5 m | 1 | 6 | por las canaletas hasta la Raspberry Pi |

## Tinta

| Artículo | Especificación | Cant. | € aprox. | Notas |
|---|---|---:|---:|---|
| Caja de plástico con tapa | 395 x 255 x 155 mm o mayor | 1 | 9 | tipo Really Useful Box 9 L; bandeja antiderrames de las botellas |
| Repisa | MDF 12 mm, 420 x 300 mm | 1 | 3 |  |
| Tapón de botella con 2 racores | salida de tubo + respiradero | 5 | 15 | para las botellas de 1 L del fabricante |
| Filtro de aire para respiradero |  | 5 | 5 |  |
| Bomba peristáltica 12 V | tubo de silicona 2 x 4 mm | 5 | 35 | rellena los subdepósitos; parada, cierra el tubo |
| Subdepósito de tinta con sensor de nivel | ~100 ml, flotador | 5 | 30 | recambio de DTF/UV, o depósito + interruptor de flotador |
| Módulo MOSFET 4 + 1 canales o placa ULN2803 | entrada 3,3 V | 1 | 6 | bombas desde los GPIO de la Raspberry Pi |
| Agitador magnético mini + imán |  | 1 | 12 | bajo la botella de blanco |
| Tubo de tinta 3 x 2 mm | 10 m | 1 | 10 | botella, bomba, subdepósito y carro |
| Racores y uniones para tubo de 3 mm |  | 1 | 5 |  |
| Resistencias 10 kΩ + diodos 1N4007 |  | 5 | 1 | pull-up de los flotadores y diodo de cada bomba (firmware/README.md) |

## Piezas impresas

Masa estimada con PETG al ~60% del sólido. STL en `out/stl/`.

| Pieza | Cant. | g/ud | g total |
|---|---:|---:|---:|
| `encoder_soporte_cinta_izq` | 1 | 9 | 9 |
| `encoder_soporte_cinta_der` | 1 | 11 | 11 |
| `encoder_soporte_sensor` | 1 | 2 | 2 |
| `final_x_bandera` | 1 | 1 | 1 |
| `final_x_soporte` | 1 | 3 | 3 |
| `encoder_y_soporte` | 1 | 7 | 7 |
| `cadena_bandeja` | 2 | 68 | 136 |
| `cadena_brazo` | 1 | 18 | 18 |
| `tinta_escuadra_repisa` | 2 | 71 | 141 |
| `tinta_pata_repisa` | 1 | 79 | 79 |
| `tinta_base_botellas` | 1 | 177 | 177 |
| `tinta_soporte_bombas` | 1 | 118 | 118 |
| `tinta_soporte_subdepositos` | 1 | 198 | 198 |
| `tinta_caja_driver` | 1 | 21 | 21 |
| `tinta_clip_tubos` | 2 | 2 | 5 |
| `electronica_caja` | 1 | 109 | 109 |
| `electronica_brida_fuente` | 2 | 9 | 18 |
| `panel_iec` | 1 | 21 | 21 |
| `panel_seta` | 1 | 25 | 25 |
| `canaleta_tramo_200` | 13 | 46 | 594 |
| `pantalla_carcasa` | 1 | 185 | 185 |
| `pantalla_soporte` | 1 | 40 | 40 |
| **Total** | | | **1920 g** |

## Resumen

| Concepto | € aprox. |
|---|---:|
| Material comprado | 287 |
| Filamento (~1.9 kg a 20 €/kg) | 38 |
| **Total fase 1** | **325** |

Las placas, la Raspberry Pi, los motores y las correas se cuentan a 0 € porque se reutilizan de impresoras 3D. No incluye cabezales ni tintas.
