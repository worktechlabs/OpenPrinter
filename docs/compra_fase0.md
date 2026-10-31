# Lista de compra: fase 0

Generada por `cad/bom.py` a partir del modelo (film de 600 mm). Si cambias `params.py`, vuelve a generarla.

> Los precios son **orientativos**, para hacerse una idea del presupuesto y
> comparar opciones. No son un presupuesto: compruébalos con tu proveedor.


## Estructura

| Artículo | Especificación | Cant. | € aprox. | Notas |
|---|---|---:|---:|---|
| Perfil 4040 ranura 8 | 690 mm, larguero lateral | 2 | 17 | tuercas en T para placa y patas |
| Perfil 4040 ranura 8 | 1060 mm, larguero delantero/trasero | 2 | 25 | unión con escuadras |
| Perfil 4040 ranura 8 | 1060 mm, travesaño central | 1 | 13 | unión con escuadras |
| Perfil 4040 ranura 8 | 1140 mm, travesaño de mesa | 2 | 27 | roscar M8 en ambas testas |
| Perfil 4040 ranura 8 | 1140 mm, tirante superior trasero | 1 | 14 | roscar M8 en ambas testas |
| Perfil 4080 ranura 8 | 1140 mm, viga x | 1 | 27 | roscar M8 x2 en cada testa; corte a escuadra ±0,1 |
| Placa lateral aluminio 5083/6082 | 10 mm, 690 x 430 mm | 2 | 140 | corte láser o agua con placa_lateral.dxf |
| Escuadra interior serie 40 | 40 x 40 mm con tornillería | 8 | 12 |  |
| Pata niveladora | M8, base Ø40 | 4 | 10 |  |

## Movimiento X

| Artículo | Especificación | Cant. | € aprox. | Notas |
|---|---|---:|---:|---|
| Guía lineal MGN12 | 1000 mm | 2 | 60 | comprar con los patines |
| Patín MGN12H |  | 4 | 32 | incluido a veces con la guía |
| Correa GT2 10 mm | 2500 mm (abierta) | 1 | 8 | fibra de vidrio o acero; para la fase 1 vale una de 6 mm reutilizada |
| Polea GT2 20T, 10 mm | eje 5 mm | 1 | 3 | o de 6 mm reutilizada |
| Polea loca GT2 20T lisa, 10 mm | eje 5 mm | 1 | 3 | o de 6 mm reutilizada |

## Arrastre Y

| Artículo | Especificación | Cant. | € aprox. | Notas |
|---|---|---:|---:|---|
| Eje acero calibrado Ø12 h6 | 1200 mm | 1 | 12 | eje del rodillo de arrastre |
| Rodillo Ø30 | 640 mm | 1 | 25 | barra de aluminio taladrada a Ø12, o tubo Ø30 con tapones; recubrir con lija adhesiva o goma |
| Rodamiento 6001-2RS | 12 x 28 x 8 | 2 | 3 | en las placas laterales |
| Eje acero Ø8 | 1250 mm | 1 | 6 | eje de levante |
| Rodamiento 625ZZ | 5 x 16 x 5 | 6 | 4 | ruedas de presión |
| Muelle de compresión | Ø6 x 12 mm, hilo 0,6-0,8 | 6 | 2 | ajustar la fuerza probando |
| Polea GT2 80T, 6 mm | eje 12 mm | 1 | 8 | en el rodillo |
| Polea GT2 20T, 6 mm | eje 5 mm | 1 | 2 | en el motor Y |
| Correa GT2 6 mm cerrada | ~250 mm | 1 | 3 | cálculo 245 mm; los colisos del soporte dan ±4 mm |

## Rollos y guías

| Artículo | Especificación | Cant. | € aprox. | Notas |
|---|---|---:|---:|---|
| Tubo aluminio Ø25 | 1200 mm | 2 | 20 | ejes de los rollos |
| Barra aluminio Ø25 | 1140 mm | 2 | 24 | guías delantera y trasera; roscar M6 en las testas |
| Rodamiento 6005-2RS | 25 x 47 x 12 | 4 | 12 | mandriles |
| Fieltro adhesivo | 3 mm | 1 | 3 | freno del rollo de entrada |

## Mesa de vacío

| Artículo | Especificación | Cant. | € aprox. | Notas |
|---|---|---:|---:|---|
| Placa aluminio perforada | 3 mm, 640 x 225 mm | 1 | 45 | corte láser con mesa_placa.dxf |
| Ventilador 80 mm 24 V | alta presión estática | 4 | 24 | 24 V para alimentarlos de la misma fuente |
| Cinta de espuma | 3 x 10 mm, 5 m | 1 | 5 | juntas de cámaras y placa |

## Tornillería

| Artículo | Especificación | Cant. | € aprox. | Notas |
|---|---|---:|---:|---|
| Tuerca en T M8 ranura 8 |  | 26 | 6 |  |
| Tornillo M8 | 16 y 20 mm | 36 | 7 | 10 de ellos a la testa de los perfiles entre placas |
| Tuerca en T M5 ranura 8 |  | 30 | 6 |  |
| Tornillo M5 | 10-16 mm | 41 | 4 | incluye ejes de ruedas y polea loca |
| Tuerca en T M3 ranura 8 |  | 40 | 6 | fijación de guías MGN12 |
| Tornillo M3 | 8-25 mm | 76 | 4 | guías, patines, motores, cabezales, pasadores |
| Tornillo M3 avellanado | 8 mm | 24 | 1 | placa de la mesa |
| Inserto térmico M3 |  | 26 | 3 |  |
| Inserto térmico M4 + tornillo M4 | 16 mm | 4 | 1 | ajuste de altura de la bandeja |
| Tornillo M4 + tuerca | 20-35 mm | 25 | 2 | collarines, tensor X, ventiladores |
| Tornillo M6 | 16 mm | 4 | 1 | guías de film |
| Prisionero M3 | 6 mm | 7 | 1 | levas y palanca |

## Piezas impresas

Masa estimada con PETG al ~60% del sólido. STL en `out/stl/`.

| Pieza | Cant. | g/ud | g total |
|---|---:|---:|---:|
| `soporte_motor_x` | 1 | 44 | 44 |
| `soporte_tensor_x` | 1 | 44 | 44 |
| `carro_placa` | 1 | 173 | 173 |
| `carro_bandeja` | 1 | 229 | 229 |
| `carro_pinza_correa` | 1 | 14 | 14 |
| `mesa_camara` | 4 | 161 | 645 |
| `presion_soporte` | 6 | 11 | 64 |
| `presion_brazo` | 6 | 5 | 29 |
| `presion_rueda_tpu` | 6 | 1 | 7 |
| `presion_leva` | 6 | 1 | 7 |
| `presion_palanca` | 1 | 5 | 5 |
| `soporte_motor_y` | 1 | 57 | 57 |
| `rollo_mandril` | 4 | 102 | 408 |
| `rollo_collarin` | 8 | 10 | 82 |
| `mesa_entrada_segmento` | 4 | 36 | 142 |
| `servicio_base` | 1 | 109 | 109 |
| **Total** | | | **2058 g** |

## Resumen

| Concepto | € aprox. |
|---|---:|
| Material comprado | 631 |
| Filamento (~2.1 kg a 20 €/kg) | 41 |
| **Total fase 0** | **672** |

No incluye motores, electrónica (fase 1), cabezales, tintas ni herramientas.
