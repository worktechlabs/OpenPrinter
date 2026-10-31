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
| Motor NEMA17 | 40 mm | 1 | 0 | recogida (fase 1.5); reutilizable de impresora 3D |

## Sensores

| Artículo | Especificación | Cant. | € aprox. | Notas |
|---|---|---:|---:|---|
| Cinta de encoder 180 LPI | 1200 mm | 1 | 15 | recambio de plóter de gran formato, o de impresoras rotas |
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
| Placa de montaje de la electrónica | MDF 10 mm, 480 x 160 mm | 1 | 3 | de un recorte del tablero de las placas |
| Separadores M3 de nylon | 6 mm | 16 | 2 |  |
| Tuerca en T M5 + tornillo M5 |  | 11 | 3 | placa de electrónica y bandeja |
| Inserto térmico M3 + tornillo M3 |  | 12 | 2 | soportes de sensores y brazo |

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
| `cadena_bandeja` | 2 | 58 | 116 |
| `cadena_brazo` | 1 | 18 | 18 |
| **Total** | | | **167 g** |

## Resumen

| Concepto | € aprox. |
|---|---:|
| Material comprado | 98 |
| Filamento (~0.2 kg a 20 €/kg) | 3 |
| **Total fase 1** | **101** |

Las placas, la Raspberry Pi, los motores y las correas se cuentan a 0 € porque se reutilizan de impresoras 3D. No incluye cabezales ni tintas.
