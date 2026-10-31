# Compra en Amazon UK (fases 0 y 1)

Búsqueda hecha en amazon.co.uk el 31/10/2026. Los precios cambian a diario y
son los que mostraba la página ese día; compruébalos antes de comprar. No
incluye lo que ya tienes de impresoras 3D: placa SKR Mini E3 V3.0, Raspberry
Pi 3, motores NEMA17, fuente de 24 V, correas de 6 mm, poleas de 20 dientes,
ruedas en V y rodamientos 608 (ver [inventario.md](inventario.md)).

Las cantidades salen de las listas generadas desde el modelo
([fase 0](compra_fase0.md), [fase 1](compra_fase1.md)).

## Lo que conviene NO comprar en Amazon

| Pieza | Problema en Amazon | Alternativa en Reino Unido |
|---|---|---|
| Perfiles de 1060–1140 mm (4040, 4080 o V-slot) | Solo hay barras de hasta 1000 mm, y caras (4040 1000 mm x2: £80) | Proveedores que cortan a medida: **KJN** (perfil 40 de ranura 8) u **Ooznest** (V-slot, ruedas y excéntricas) |
| Ejes de acero Ø12 y Ø8 de ~1,2 m | £49 el de Ø12 y £52 dos de Ø8 | Barra calibrada (*bright mild steel*, EN1A) cortada a medida en un almacén de metal (p. ej. Metals4U): unas pocas libras |
| Tubo de aluminio Ø25 de ~1,2 m (ejes de rollos y guías) | Solo tramos cortos | Almacén de metal o tienda de bricolaje |
| MDF de 19 mm | — | B&Q, Wickes o almacén de madera (lo cortas tú) |
| Cinta de encoder 180 LPI y AS5047P | No aparecen en Amazon UK | eBay o AliExpress; la cinta y el sensor también se sacan de impresoras rotas |

## Estructura

| Pieza | Cant. necesaria | Producto | Precio |
|---|---:|---|---:|
| Escuadras 4040 en L | 8 | [12 uds, 4040, 90°](https://www.amazon.co.uk/dp/B0FR48JBXX) | £12.49 |
| Tuercas en T M8, serie 40 | ~30 | [TA-VIGOR M8 con muelle](https://www.amazon.co.uk/dp/B0FHHM3DDB) | £8.13 |
| Tuercas en T M5, serie 40 | ~30 | [TA-VIGOR M5 con muelle](https://www.amazon.co.uk/dp/B0FHHQHTV8) | £7.29 |

## Movimiento X (si se usan guías lineales)

| Pieza | Cant. necesaria | Producto | Precio |
|---|---:|---|---:|
| Guía MGN12 1000 mm + patín MGN12H | 2 guías, 4 patines | [CNCMANS MGN12 1000 mm con MGN12H](https://www.amazon.co.uk/dp/B0C8MKJP59) | £18.33 c/u |
| Correa GT2 10 mm + poleas 20T y locas | 1 kit | [5 m GT2 10 mm + 6 poleas 20T + 4 locas](https://www.amazon.co.uk/dp/B0C54ZXM88) | £22.99 |

Con ruedas en V no hacen falta las guías: ver la pregunta del perfil más abajo.
Cada guía de ese enlace trae **un** patín; el diseño lleva dos por guía, así que
habría que comprar 2 patines sueltos o adaptar el carro a uno por guía.

## Arrastre Y y rollos

| Pieza | Cant. necesaria | Producto | Precio |
|---|---:|---|---:|
| Polea GT2 80 dientes, eje 12 mm | 1 | [2 uds 80T, eje 12, correa 6 mm](https://www.amazon.co.uk/dp/B0DDB876RG) | £10.39 |
| Correa GT2 cerrada 250 mm, 6 mm | 1 | [5 uds 250 mm](https://www.amazon.co.uk/dp/B0GVKNWVHH) | £6.69 |
| Rodamiento 6001-2RS (12×28×8) | 2 | [HiPicco 4 uds](https://www.amazon.co.uk/dp/B0CH2XZGMW) | £6.64 |
| Rodamiento 6005-2RS (25×47×12) | 4 | [HiPicco 4 uds](https://www.amazon.co.uk/dp/B0CH2X1NFJ) | £10.44 |
| Rodamiento 625ZZ (5×16×5) | 6 | [TA-VIGOR 5 uds](https://www.amazon.co.uk/dp/B0F5XBKZSH) (x2), o los de ruedas en V que tengas | £5.69 |
| Tubo Ø30 para el rodillo | 640 mm | [Tubo Ø30 × 2,5 mm, 1 m](https://www.amazon.co.uk/dp/B0FQTYM1NL) | £16.15 |

## Mesa de vacío

| Pieza | Cant. necesaria | Producto | Precio |
|---|---:|---|---:|
| Ventilador 80 mm 24 V | 4 | [ANVISION 2 uds, 8025, 24 V](https://www.amazon.co.uk/dp/B0C18G953Z) (x2) | £15.98 |

## Electrónica (fase 1)

| Pieza | Cant. necesaria | Producto | Precio |
|---|---:|---|---:|
| Convertidor 24 V → 5 V 5 A | 1 | [Step-down 12/24 V a 5 V 5 A](https://www.amazon.co.uk/dp/B09X1XJYB6) | £10.99 |
| Raspberry Pi Pico | 1 | [Raspberry Pi Pico](https://www.amazon.co.uk/dp/B0B5H2LNL2) | £5.42 |
| Cadena portacables 10×20, 1 m | 1 | [Cadena 10×20 mm 1 m](https://www.amazon.co.uk/dp/B0DY5BWNW3) | £14.78 |

Pendientes de buscar: sensor óptico de horquilla, TCRT5000, seta de emergencia,
conector IEC con fusible, insertos térmicos y surtido de tornillería
M3/M4/M5/M8.

## Resumen orientativo

Con guías MGN12, lo encontrado en Amazon UK suma unas **£260**, sin perfiles,
ejes, tubos ni MDF (la fuente ya la tienes). Con ruedas en V se ahorran unas
£75 de guías y patines.
