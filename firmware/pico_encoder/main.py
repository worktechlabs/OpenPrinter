"""OpenDTF - monitor de encoders en un Raspberry Pi Pico (MicroPython).

Lee los dos encoders de la fase 1 y manda sus cuentas por USB a la Raspberry Pi
para las pruebas de movimiento (registro.py las guarda y las analiza):

- Encoder X: cinta de 180 LPI y sensor óptico de cuadratura (tipo H9730). Lo
  cuenta un state machine del PIO, así que no pierde pasos aunque Python vaya
  lento. Cuenta los flancos de subida y bajada del canal A (x2): 14,17 cuentas
  por mm, 0,07 mm por cuenta.
- Encoder Y: AS5047P por SPI frente al imán del eje del rodillo. 14 bits por
  vuelta; aquí se suman las vueltas para dar la posición del film.

Salida: una línea por muestra, "t_us,x_cuentas,y_cuentas". Las líneas que
empiezan por "#" son informativas.

Órdenes por USB (terminadas en salto de línea):
  r        pone a cero las dos cuentas
  f 500    muestras por segundo (10 a 2000)
  p / c    pausa / continúa el envío
  i        información y escalas

Se instala copiando este archivo como main.py en el Pico con MicroPython (con
Thonny o con "mpremote cp main.py :main.py").
"""
import select
import sys
import time

import rp2
from machine import SPI, Pin

# Pines (GPxx del Pico)
X_A, X_B = 2, 3                          # canales A y B del sensor del encoder X
SPI_SCK, SPI_MOSI, SPI_MISO, SPI_CS = 18, 19, 16, 17   # AS5047P en SPI0

X_CUENTAS_MM = 180 / 25.4 * 2            # 180 LPI, flancos de A
Y_CUENTAS_VUELTA = 16384
Y_MM_VUELTA = 3.14159265 * 30            # rodillo de arrastre de Ø30
VERSION = 1


@rp2.asm_pio()
def cuadratura_x2():
    """Cuenta los flancos del canal A según el nivel de B.

    Avance: A sube con B bajo, o A baja con B alto. El PIO solo sabe restar, y
    sumar con trucos de varias instrucciones daría lecturas falsas si Python lee
    a mitad. Por eso cada flanco es una sola resta: los avances restan en X y
    los retrocesos en Y. Posición = Y - X.
    """
    wrap_target()
    label("inicio")
    wait(1, pin, 0)                      # A sube
    jmp(pin, "sube_b_alto")
    jmp(x_dec, "bajada")                 # B bajo: avance
    label("bajada")
    wait(0, pin, 0)                      # A baja
    jmp(pin, "baja_b_alto")
    jmp(y_dec, "inicio")                 # B bajo: retroceso (si no salta, vuelve por el wrap)
    wrap()
    label("sube_b_alto")
    jmp(y_dec, "sube_fin")               # B alto al subir: retroceso
    label("sube_fin")
    jmp("bajada")
    label("baja_b_alto")
    jmp(x_dec, "baja_fin")               # B alto al bajar: avance
    label("baja_fin")
    jmp("inicio")


sm = rp2.StateMachine(0, cuadratura_x2, freq=125_000_000,
                      in_base=Pin(X_A, Pin.IN, Pin.PULL_UP),
                      jmp_pin=Pin(X_B, Pin.IN, Pin.PULL_UP))
sm.active(1)


def _registro(nombre):
    """Copia X o Y al FIFO con instrucciones forzadas; el programa sigue contando."""
    sm.exec("in_(%s, 32)" % nombre)
    sm.exec("push()")
    return sm.get()


def leer_x():
    """Posición del encoder X en cuentas (avances - retrocesos)."""
    v = (_registro("y") - _registro("x")) & 0xFFFFFFFF
    return v - (1 << 32) if v & 0x80000000 else v


def poner_x_a_cero():
    sm.exec("set(x, 0)")
    sm.exec("set(y, 0)")


spi = SPI(0, baudrate=2_000_000, polarity=0, phase=1, bits=8,
          sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI), miso=Pin(SPI_MISO))
cs = Pin(SPI_CS, Pin.OUT, value=1)
LEER_ANGULO = b"\xff\xff"                 # lectura de ANGLECOM (0x3FFF) con bit de paridad
_buf = bytearray(2)


def leer_angulo():
    """Ángulo de 14 bits del AS5047P, o None si la trama trae error.

    Cada trama devuelve la respuesta a la orden anterior; como siempre se pide
    lo mismo, la respuesta es el ángulo de hace una muestra.
    """
    cs(0)
    spi.write_readinto(LEER_ANGULO, _buf)
    cs(1)
    v = (_buf[0] << 8) | _buf[1]
    unos = 0
    w = v
    while w:
        unos += w & 1
        w >>= 1
    if unos & 1 or v & 0x4000:           # paridad impar o bit de error
        return None
    return v & 0x3FFF


class Vueltas:
    """Suma las vueltas del rodillo a partir del ángulo de 14 bits."""

    def __init__(self):
        self.ultimo = None
        self.total = 0
        self.errores = 0

    def actualizar(self, angulo):
        if angulo is None:
            self.errores += 1
            return self.total
        if self.ultimo is not None:
            d = angulo - self.ultimo
            if d > Y_CUENTAS_VUELTA // 2:
                d -= Y_CUENTAS_VUELTA
            elif d < -Y_CUENTAS_VUELTA // 2:
                d += Y_CUENTAS_VUELTA
            self.total += d
        self.ultimo = angulo
        return self.total

    def a_cero(self):
        self.total = 0


def info(periodo_us, vy):
    print("# OpenDTF encoders v%d x_cuentas_mm=%.4f y_cuentas_vuelta=%d y_mm_vuelta=%.4f "
          "hz=%d errores_spi=%d" % (VERSION, X_CUENTAS_MM, Y_CUENTAS_VUELTA, Y_MM_VUELTA,
                                    1_000_000 // periodo_us, vy.errores))


def main():
    vy = Vueltas()
    periodo_us = 2000                    # 500 muestras por segundo
    enviando = True
    entrada = select.poll()
    entrada.register(sys.stdin, select.POLLIN)
    t0 = time.ticks_us()
    siguiente = t0
    info(periodo_us, vy)
    while True:
        ahora = time.ticks_us()
        if time.ticks_diff(ahora, siguiente) >= 0:
            siguiente = time.ticks_add(siguiente, periodo_us)
            if time.ticks_diff(ahora, siguiente) > periodo_us:
                siguiente = time.ticks_add(ahora, periodo_us)      # no acumular retraso
            y = vy.actualizar(leer_angulo())
            if enviando:
                print("%d,%d,%d" % (time.ticks_diff(ahora, t0), leer_x(), y))
        if entrada.poll(0):
            orden = sys.stdin.readline().strip().split()
            if not orden:
                continue
            if orden[0] == "r":
                poner_x_a_cero()
                vy.a_cero()
                t0 = time.ticks_us()
                print("# cero")
            elif orden[0] == "f" and len(orden) > 1:
                hz = max(10, min(2000, int(orden[1])))
                periodo_us = 1_000_000 // hz
                print("# hz=%d" % hz)
            elif orden[0] == "p":
                enviando = False
            elif orden[0] == "c":
                enviando = True
            elif orden[0] == "i":
                info(periodo_us, vy)


main()
