# Compra en Reino Unido: Amazon, eBay y AliExpress (fases 0 y 1)

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
| Perfiles de 1060–1140 mm (4040, 4080 o V-slot) | Solo hay barras de hasta 1000 mm, y caras (4040 1000 mm x2: £80) | Proveedor que corte a medida (ver "Perfiles" abajo) |
| Ejes de acero Ø12 y Ø8 de ~1,2 m | £49 el de Ø12 y £52 dos de Ø8 | Barra calibrada (*bright mild steel*, EN1A) cortada a medida en un almacén de metal (p. ej. Metals4U): unas pocas libras |
| Tubo de aluminio Ø25 de ~1,2 m (ejes de rollos y guías) | Solo tramos cortos | Almacén de metal o tienda de bricolaje |
| MDF de 19 mm | — | B&Q, Wickes o almacén de madera (lo cortas tú) |
| Cinta de encoder 180 LPI y AS5047P | No aparecen en Amazon UK | eBay o AliExpress; la cinta y el sensor también se sacan de impresoras rotas |

## Decisión: guías MGN12 sobre perfil de la serie 40

Se descartan las ruedas en V para el carro. En DTF cualquier holgura del carro
se ve como bandas, y el POM se desgasta y se aplana si la máquina está parada.
Las MGN12 cuestan poco en Amazon UK, así que la diferencia es de unas £35. El
V-slot 2020 y sus escuadras del inventario se usarán en la estructura de la
cubierta.

## Perfiles (fuera de Amazon)

Hacen falta unos 8 m de 4040 (2 × 690, 3 × 1060 y 3 × 1140 mm, ver
`out/lista_corte.csv`) y 1 × 1140 mm de 4080. Precio de referencia: Matara UK
vende 40 × 40 a £12,19/m sin IVA, así que el 4040 rondaría las £100 más el
4080, el corte y el envío. Ese perfil es de **ranura 6**; también vale, pero
entonces la tornillería pasa a M5 con tuercas en T de ranura 6 en lugar de M8 de
ranura 8. Pide presupuesto de corte a medida a:

- [Matara UK](https://matara.com/product/aluminium-extrusion-profiles/aluminium-profile/pg20-aluminium-profile/pg20-40x40-8-slots/)
- [Benchdogs](https://benchdogs.co.uk/products/becnhdogs-workststion-extrusion.oembed) (4040 y 8040 cortados a medida)
- Ally Extrusions (eBay)

Lo más crítico: los 4 perfiles de 1140 mm que van entre placas deben medir lo
mismo y estar cortados a escuadra (±0,1 mm).

## Estructura

| Pieza | Cant. necesaria | Producto | Precio |
|---|---:|---|---:|
| Escuadras 4040 en L | 8 | [12 uds, 4040, 90°](https://www.amazon.co.uk/dp/B0FR48JBXX) | £12.49 |
| Tuercas en T M8, serie 40 | ~30 | [TA-VIGOR M8 con muelle](https://www.amazon.co.uk/dp/B0FHHM3DDB) | £8.13 |
| Tuercas en T M5, serie 40 | ~30 | [TA-VIGOR M5 con muelle](https://www.amazon.co.uk/dp/B0FHHQHTV8) | £7.29 |

## Movimiento X

| Pieza | Cant. necesaria | Producto | Precio |
|---|---:|---|---:|
| Guía MGN12 1000 mm + patín MGN12H | 2 | [CNCMANS MGN12 1000 mm con MGN12H](https://www.amazon.co.uk/dp/B0C8MKJP59) | £18.33 c/u |
| Patines MGN12H extra | 2 | [2 guías MGN12 de 100 mm con 2 patines](https://www.amazon.co.uk/dp/B0D752N1YF) | £19.89 |
| Correa GT2 10 mm + poleas 20T y locas | 1 kit | [5 m GT2 10 mm + 6 poleas 20T + 4 locas](https://www.amazon.co.uk/dp/B0C54ZXM88) | £22.99 |

Cada guía larga trae un patín y el diseño lleva dos por guía. El juego de guías
cortas con 2 patines sale más barato que comprar los patines sueltos. Para
pasar un patín de una guía a otra, pon las dos guías en línea, testa contra
testa, y deslízalo sin sacarlo al aire: si se sale de la guía se le caen las
bolas.

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

## Tinta a granel y pantalla (fase 1)

Aún sin producto concreto elegido: los enlaces son búsquedas, para comparar
medidas y precios. Lo que hay que mirar está en la columna de la derecha.

| Pieza | Cant. | Dónde buscar | Qué comprobar |
|---|---:|---|---|
| Caja de plástico con tapa | 1 | [Amazon UK: Really Useful Box 9 L](https://www.amazon.co.uk/s?k=really+useful+box+9+litre) | Exterior 395 × 255 × 155 mm o mayor (interior 335 × 210 mm caben 5 botellas de 1 L). Si es más grande, cambia `INK_BOX` en `params.py` |
| Bomba peristáltica 12 V | 5 | [Amazon UK](https://www.amazon.co.uk/s?k=12v+peristaltic+pump) · [AliExpress](https://www.aliexpress.com/w/wholesale-12v-peristaltic-pump.html) | Tubo de silicona de 2 × 4 mm o similar, ~0,3 A |
| Subdepósito de tinta con sensor | 5 | [AliExpress: DTF sub ink tank sensor](https://www.aliexpress.com/w/wholesale-dtf-sub-ink-tank-sensor.html) | Con flotador; si no, depósito pequeño + interruptor de flotador vertical |
| Módulo MOSFET o ULN2803 | 1 | [Amazon UK](https://www.amazon.co.uk/s?k=mosfet+module+4+channel+3.3v) | Que dispare con 3,3 V (GPIO de la Raspberry Pi) |
| Pantalla táctil de 7" HDMI + USB | 1 | [Amazon UK](https://www.amazon.co.uk/s?k=7+inch+hdmi+touchscreen+raspberry+pi) | 1024 × 600 va bien con KlipperScreen. Al comprarla, mide el módulo y ajusta `SCREEN_SIZE` |
| Agitador magnético mini | 1 | [Amazon UK](https://www.amazon.co.uk/s?k=mini+magnetic+stirrer) | De perfil bajo (~25 mm) y con imán incluido |

## Opciones en eBay UK

Búsqueda del 31/10/2026. En eBay muchos anuncios muestran el precio de la
variante más corta: elige la longitud en el anuncio antes de comparar.

| Pieza | Producto | Precio | Nota |
|---|---|---:|---|
| **Cinta de encoder 180 LPI** | [180 LPI, 4200 × 15 mm](https://www.ebay.co.uk/itm/277741169799) | £11.99 | Sobra para varias máquinas. **Recórtala a 12 mm de ancho** (las líneas van de lado a lado, así que se puede): entre los patines hay 13 mm |
| Cinta de encoder 180 LPI (alternativa) | [180 LPI, 5000 × 15 mm](https://www.ebay.co.uk/itm/196506685389) | £28.80 | |
| Perfil 4040 ranura 8 cortado a medida | [4040 T-slot, 100–6000 mm](https://www.ebay.co.uk/itm/404798095657) | desde £47.50 | Vendedor con pocas valoraciones: pide antes confirmación de corte a escuadra |
| Perfil 4040 ranura 8 (hasta 1100 mm) | [4040 T-slot, 100–1100 mm](https://www.ebay.co.uk/itm/303522567590) | desde £3.50 | Vale para los largueros de 690 y 1060 mm, no para los de 1140 |
| Perfil 4040 compatible Item | [4040 negro anodizado](https://www.ebay.co.uk/itm/303727531954) | desde £3.60 | Comprobar la longitud máxima |
| Perfil 4080 ranura 8 | [4080 T-slot + accesorios](https://www.ebay.co.uk/itm/305167168603) | desde £4.00 | Comprobar que corte 1140 mm |
| Barra de acero calibrada Ø12 y Ø8 (EN1A) | [Bright mild steel 4–40 mm, cortada](https://www.ebay.co.uk/itm/271621202226) | desde £4.54 | **Solo hasta 1000 mm**: para los ejes de 1,2 m hace falta un almacén de metal (Metals4U o similar) |

## Opciones en AliExpress

Más barato y tarda 1–3 semanas. AliExpress cobra el IVA en el precio final
para Reino Unido. Los precios que muestra la búsqueda son los de la variante
más corta.

| Pieza | Dónde mirar | Nota |
|---|---|---|
| Guías MGN12 1000 mm + patín | [MGN12 1000 mm + 2 patines](https://www.aliexpress.com/item/1005002762351926.html) · [MGN12 + MGN12H, 800–1100 mm](https://www.aliexpress.com/item/1005004553699955.html) | Elige 1000 mm y patín H, ya montado en la guía |
| AS5047P + imán | [Buscar AS5047P](https://www.aliexpress.com/w/wholesale-AS5047P-encoder.html) | Que traiga el imán diametral de 6 mm |
| Sensor de encoder 180 LPI | [Buscar H9730](https://www.aliexpress.com/w/wholesale-H9730-encoder-sensor-180-lpi.html) | Misma resolución que la cinta (180 LPI) |
| Polea GT2 80T eje 12, rodamientos, insertos, tuercas en T, tornillería | Búsqueda directa | Suele salir a la mitad que en Amazon |

## Orden de compra recomendado

1. **Ya:** perfiles cortados a medida y MDF, para montar el chasis.
2. **Ya, desde AliExpress:** guías y patines MGN12, AS5047P, sensor de
   encoder. La cinta de encoder, en eBay UK.
3. **Al montar:** rodamientos, poleas, ventiladores, tornillería y el resto,
   donde salga mejor de precio.

## Resumen orientativo

Lo encontrado en Amazon UK suma unas **£280** con las guías y los patines
extra, sin perfiles, ejes, tubos ni MDF (la fuente ya la tienes). Con los
perfiles cortados a medida (~£130) y el resto de metal y MDF (~£30), la fase 0
completa ronda las **£450**.
