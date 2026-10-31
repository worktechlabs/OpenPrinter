# Cabezales: análisis y decisión

> Precios orientativos (octubre de 2026). Varían mucho entre vendedores:
> compara presupuestos antes de comprar.

## Resumen

El coste no lo marca solo el cabezal, sino también la placa que lo dispara. Un
XP600 es barato, pero sin un driver no imprime. Por eso cabezal y placa se
eligen juntos.

**Decisión**: la primera máquina lleva **un solo XP600 con CMYK + WW** (dos
canales de blanco). El carro y el recorrido se dimensionan para dos cabezales
(`HEAD_SLOTS = 2` en `cad/params.py`), así que el segundo XP600, dedicado al
blanco, se añade más adelante sin tocar el chasis. El cabezal montado ocupa el
hueco del lado −X.

**Todas las pruebas se hacen directamente en DTF**: XP600, tinta DTF y film.
No hay etapa intermedia en papel ni con cabezales térmicos.

## Opciones

| Opción | Coste aprox. | ¿DTF? | Encaje con OpenPrinter |
|---|---|---|---|
| 1× XP600, CMYK + WW | 150–300 € original nuevo; 20–40 € reacondicionado | Sí | Configuración DTF de sobremesa más común. **Elegida** |
| 2× XP600 (CMYK + blanco dedicado) | el doble | Sí | Mejor capa de blanco. Ampliación futura |
| Impresora donante (Epson XP-600/700/800, ET-8550) | 20–80 € de segunda mano | No | Cabezal XP600 y una placa Epson que funciona, para medir la forma de onda (fase 3) |
| Epson i1600 | 150–300 € | Sí | Más duradero, pero exagerado para la primera máquina |
| Epson i3200 | 375–625 € | Sí | Descartado por precio |
| HP45 y otros térmicos | 30–60 € | No | Descartados: la tinta DTF, y sobre todo el blanco, necesita un piezoeléctrico |
| Xaar 128 y similares | 50–150 € usados | No | Boquillas gruesas, tintas de solvente o UV. Descartado |

Los XP600 de 20–40 € suelen ser reacondicionados o usados, a menudo con
boquillas muertas. No sirven para una máquina DTF fiable.

## Ruta por etapas

1. **Fase 3: impresora donante.** Una Epson XP-600/700/800 rota lleva el
   cabezal F1080 (XP600) y una placa que lo dispara. Con un osciloscopio se
   mide la señal sin usar nada propietario, solo mediciones propias.
2. **Primera máquina DTF: 1× XP600 CMYK + WW.** Un cabezal, una placa, menos
   dampers y tubos. El blanco va más lento (2 de 6 canales). Las primeras
   impresiones ya son sobre film con tinta DTF.
3. **Segundo XP600** para el blanco cuando el resto funcione.
4. **i1600/i3200** solo si un driver propio los justifica.

## Placa: cerrada o abierta

- **Kit chino (Hoson, Senyang…) para 1× XP600**, unos 150–300 €. Permite
  imprimir pronto, pero su placa principal suele controlar ella misma los motores
  y el encoder (sustituiría a la SKR Mini y a parte de la
  [fase 1](fase1_movimiento.md)). Además ata a su RIP con licencia y a cabezales
  "bloqueados" o "desbloqueados".
- **Driver abierto (fase 3)**: pocas piezas, meses de trabajo y tensiones de
  30–40 V con picos de corriente altos.

Sin etapa de pruebas en papel, la primera impresión depende de tener un driver.
Si hace falta imprimir antes de que el driver abierto esté listo, el kit cerrado
es la vía rápida.

## Qué buscar para el XP600

- **Nombre y referencias**: *Epson XP600 printhead*, cabezal **F1080-A1**.
  - Los números de pieza de Epson son de la serie **FA09xxx** (por ejemplo
    **FA09121**). También se le llama **DX11**.
  - Búsquedas útiles: `XP600 printhead F1080-A1` y `Epson FA09121`.
  - Ejemplo de referencia (octubre de 2026): [Digiprint Supplies](https://www.digiprint-supplies.com/en/epson-xp600-dx11-printhead-f1080-a1-fa09121-fa09xxx), 218 € el
    original con holograma, sin devolución una vez montado. Si se compra desde
    Reino Unido, hay que sumar el IVA de importación.
- **Datos del vendedor** (pendientes de comprobar con un cabezal real):
  - Medidas totales: 84,9 × 57,2 × 42,6 mm, bastante más que la maqueta de
    `HEAD_SIZE`. Hay que medir el cabezal antes de imprimir la bandeja.
  - Frecuencia de disparo: 11,52 kHz en modo multigota (46 kHz con gota única).
  - Gotas de 4,5 a 40 pl, viscosidad de tinta de 3 a 5 mPa·s.
  - Cable de datos de 29 pines. El vendedor recomienda cables nuevos con cada
    cabezal nuevo.
- **Original nuevo**: busca "original" o "genuine" y "new". Evita "refurbished",
  "rebuilt" y "compatible".
- **Bloqueado o desbloqueado**: solo importa con placas chinas. "First locked"
  se casa con la primera placa en la que se monta; "unlocked" sirve en
  cualquiera. Para un driver abierto da igual.
- **Impresoras que lo llevan** (para la donante): Epson Expression Premium
  XP-600, XP-605, XP-700, XP-750, XP-800 y XP-850.
- **Accesorios**: colector (*manifold*) para dampers, 6 dampers para XP600 y
  los dos cables planos del cabezal.

## Otros costes del XP600

- Colector (*manifold*) para dampers en lugar de cartuchos.
- Dampers.
- Cables planos.
- Estación de capping.

El XP600 no recircula por dentro, así que la circulación del blanco va por los
tubos y el depósito (fase 4).

## Fuentes

- [myprint.ua: comparativa XP600, i1600 e i3200](https://myprint.ua/en/news/dtf-printer-comparison-xp600-i1600-i3200-printheads-complete-analysis)
- [Xinflying: XP600 frente a i3200](https://xinflyinggroup.com/xp600-vs-i3200-printhead-differences)
- [KingdomDTF: XP600, compatible con ET-8550](https://kingdomdtf.com/products/xp600-printhead)
- [BCH: XP600/XP7100 para conversiones DTF baratas](https://bchtechnologies.com/blogs/questions-and-answers/can-the-xp600-xp7100-printhead-be-used-for-a-low-cost-dtf-or-pigment-ink-conversion)
