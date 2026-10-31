# Firmware y configuración (fase 1)

Configuración de Klipper para mover la máquina, controlar el vacío y rellenar
la tinta, menú de la pantalla táctil y monitor de encoders en el Pico. **Sin probar todavía en la máquina**:
revisa los pines con tu placa antes de conectar motores.

| Archivo | Qué hace |
|---|---|
| [`klipper/printer.cfg`](klipper/printer.cfg) | Placa SKR Mini E3 V3.0, ejes X e Y, vacío, sensores y la Raspberry Pi como segunda MCU |
| [`klipper/macros.cfg`](klipper/macros.cfg) | Vacío, carro, film, inicio y fin de trabajo, pausa y pruebas de la fase 1 |
| [`klipper/tinta.cfg`](klipper/tinta.cfg) | Bombas y flotadores: relleno automático de los subdepósitos con avisos |
| [`klipper/KlipperScreen.conf`](klipper/KlipperScreen.conf) | Menú "OpenPrinter" en la pantalla táctil |
| [`pico_encoder/main.py`](pico_encoder/main.py) | Pico con MicroPython: cuenta el encoder X con el PIO y lee el AS5047P del eje Y |
| [`pico_encoder/registro.py`](pico_encoder/registro.py) | En la Raspberry Pi: registra los encoders en CSV y analiza las pruebas 1 y 2 |

## Ejes en Klipper

- **X** es el carro: 0 en el extremo izquierdo del recorrido y 820 en el
  derecho. El centro del film está en 405 y la estación de servicio, donde se
  hace home, en 810.
- **Y** es el avance del film. No tiene final, así que no hace home: se pone a
  0 al empezar cada trabajo (`G92 Y0`).
- **Z** no existe, pero Klipper lo exige: se declara en el driver Z libre, sin
  motor, y nunca se mueve.

## Instalación

1. **Raspberry Pi**: graba Raspberry Pi OS Lite (64 bits) e instala con
   [KIAUH](https://github.com/dw-0/kiauh) Klipper, Moonraker, Mainsail y
   KlipperScreen.
2. **Firmware de la SKR Mini E3 V3.0**: en `~/klipper`, `make menuconfig` con:
   - Micro-controller: STM32, procesador STM32G0B1.
   - Bootloader offset: 8 KiB.
   - Clock reference: 8 MHz crystal.
   - Communication interface: USB (on PA11/PA12).

   Después, `make`. Copia `out/klipper.bin` a una tarjeta SD como
   `firmware.bin`, métela en la placa y enciéndela.
3. **La Raspberry Pi como MCU** (para los GPIO de la tinta):
   - Compila: `make menuconfig` con "Linux process", y luego `make` y
     `make flash`.
   - Activa el servicio: `sudo cp scripts/klipper-mcu.service /etc/systemd/system/`
     y `sudo systemctl enable --now klipper-mcu`.

   Está explicado en la guía de Klipper *RPi microcontroller*.
4. **Configuración**: copia los cuatro archivos de `klipper/` a
   `~/printer_data/config/`. En `printer.cfg`, cambia el `serial` de `[mcu]` por
   el que da `ls /dev/serial/by-id/`.
5. **Pantalla de 7" HDMI**: si no detecta la resolución sola, añade en
   `/boot/firmware/config.txt`:

   ```
   hdmi_group=2
   hdmi_mode=87
   hdmi_cvt=1024 600 60 6 0 0 0
   hdmi_drive=1
   ```

   El táctil va por USB y no necesita controlador.

## Conexiones

### Placa SKR Mini E3 V3.0

| Conector | Señal |
|---|---|
| X | Motor X |
| Y | Motor Y (arrastre) |
| Z | Libre (eje ficticio) |
| E | Libre: circulación del blanco en la fase 4 |
| X-STOP (PC0) | Sensor de horquilla del home X |
| Y-STOP (PC1) | Microinterruptor de la palanca de presión (cerrado con la palanca bajada) |
| E0-STOP (PC15) | Sensor de film TCRT5000 |
| HE0 (PC8) | Ventiladores de vacío del centro (24 V) |
| HB (PC9) | Ventiladores de vacío de los lados (24 V) |
| FAN0 (PC6) | Ventiladores 4010 de la caja (12 V desde el convertidor, o ventiladores de 24 V directos) |

La seta de emergencia corta los 24 V de los drivers por hardware; no pasa por
Klipper.

### GPIO de la Raspberry Pi (tinta)

| Color | Bomba (al módulo MOSFET) | Flotador |
|---|---|---|
| C | GPIO 17 | GPIO 5 |
| M | GPIO 27 | GPIO 6 |
| Y | GPIO 22 | GPIO 13 |
| K | GPIO 23 | GPIO 19 |
| W | GPIO 24 | GPIO 26 |

- **Bombas**: cada GPIO va a la entrada de su canal del módulo MOSFET (o
  ULN2803). Las bombas se alimentan a 12 V desde el convertidor de 24 a 12 V. Con
  un ULN2803 o un módulo sin diodo, pon un diodo 1N4007 en paralelo con cada
  bomba.
- **Flotadores**: cada uno entre su GPIO y GND, con una resistencia de 10 kΩ
  del GPIO a 3,3 V. Nunca a 5 V: los GPIO de la Pi son de 3,3 V.
- **Masas**: la de la Pi, la del módulo MOSFET y la del convertidor de 12 V,
  unidas.

## Primer arranque

1. **Sin correas** y con la seta pulsada, enciende y comprueba en Mainsail que
   Klipper conecta con las dos MCU.
2. **Sentido de los motores**: suelta la seta y mueve X 10 mm. Si va al revés,
   cambia el `!` de `dir_pin`. Haz lo mismo con Y: el film debe avanzar hacia
   delante.
3. **Home X**: `QUERY_ENDSTOPS` con la bandera dentro y fuera de la horquilla.
   Después, `G28` y ajusta `position_endstop` para que `IR_SERVICIO` deje las
   boquillas sobre las tapas.
4. **Avance Y**: `PRUEBA_AVANCE N=100 PASO=6.35` y mide la marca del film. Si
   no salen 635 mm, corrige `rotation_distance` multiplicándolo por medido ÷
   ordenado.
5. **Tinta**: con las botellas llenas, `TINTA_ESTADO`. Sube y baja cada flotador
   con la mano y comprueba que su bomba arranca y para. Sube `max_s` en
   `tinta.cfg` si el primer llenado tarda más de 90 s.
6. **Pruebas de la fase 1**: las de
   [fase1_movimiento.md](../docs/fase1_movimiento.md#pruebas-de-la-fase-1), con
   `PRUEBA_PASADAS` y `PRUEBA_AVANCE`.

## Monitor de encoders (Raspberry Pi Pico)

Klipper no lee encoders de cuadratura, así que en la fase 1 los lee un Pico
aparte y los manda por USB a la Raspberry Pi. Sirve para medir las pruebas de
movimiento; en la fase 3 el mismo Pico dará la posición para disparar el
cabezal.

- **Encoder X**: un state machine del PIO cuenta los flancos del canal A (x2).
  Son 14,17 cuentas por mm (0,07 mm), y no pierde ninguna aunque Python vaya
  lento.
- **Encoder Y**: el AS5047P se lee por SPI y se suman las vueltas del rodillo:
  5,8 µm de film por cuenta.
- **Salida**: líneas `t_us,x_cuentas,y_cuentas`, a 500 muestras por segundo
  por defecto.

La lógica del contador está comprobada en un simulador con avances, retrocesos
y temblores en un flanco. Falta probarla en un Pico real.

### Instalación

1. Graba MicroPython en el Pico: mantén BOOTSEL al enchufarlo y copia el `.uf2`
   de micropython.org.
2. Copia el programa: `mpremote cp firmware/pico_encoder/main.py :main.py` (o
   con Thonny).
3. En la Raspberry Pi: `sudo apt install python3-serial` y copia
   `registro.py`.

### Conexiones del Pico

| Pico | Va a |
|---|---|
| GP2 | Encoder X, canal A |
| GP3 | Encoder X, canal B |
| GP18 (SCK) | AS5047P CLK |
| GP19 (MOSI) | AS5047P MOSI |
| GP16 (MISO) | AS5047P MISO |
| GP17 | AS5047P CSn |
| 3V3 (OUT) | AS5047P VDD y VDD3V3 (puenteados, modo 3,3 V) |
| GND | Masa de los dos sensores |
| USB | Raspberry Pi |

- **Sensor del encoder X a 5 V** (la mayoría de los H9730): sus salidas no
  pueden ir directas al Pico. Pon un divisor en cada canal (10 kΩ en serie y
  20 kΩ a GND) o un 74LVC245. Si tu sensor funciona a 3,3 V, conéctalo directo.
- **Cables**: los dos encoders, con cable apantallado y la malla a GND solo en
  el lado del Pico.

### Pruebas

Con el Pico conectado, lanza el registro y, mientras corre, la macro de Klipper:

```
python3 registro.py pasadas --segundos 120        # y en Klipper: PRUEBA_PASADAS N=100 VEL=600
python3 registro.py avance --ordenado 635          # y en Klipper: PRUEBA_AVANCE N=100 PASO=6.35
python3 registro.py analizar pasadas_*.csv --prueba-csv pasadas
```

- **Pasadas**: da la velocidad media en la mitad central del recorrido, en
  cada sentido, con su rizado (objetivo por debajo del 1 %). También da la
  dispersión de los puntos de inversión (objetivo ±1 cuenta).
- **Avance**: compara el avance medido por el AS5047P con el ordenado
  (objetivo por debajo del 0,05 %) y dice por cuánto multiplicar
  `rotation_distance`.

## Pendiente

- **Disparo del cabezal** (fase 3) y RIP (fase 2).
- Pasar el monitor de encoders a C (Pico SDK) cuando haga falta dar la
  posición en tiempo real al disparo del cabezal.
