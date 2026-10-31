#!/usr/bin/env python3
"""OpenPrinter - registro y análisis de los encoders (en la Raspberry Pi).

Lee lo que manda el Pico (main.py), lo guarda en CSV en milímetros y analiza
las dos pruebas de la fase 1 (docs/fase1_movimiento.md):

  pasadas  prueba 1: velocidad del carro en la zona central (rizado) y
           repetibilidad de los puntos de inversión.
  avance   prueba 2: avance de film medido por el AS5047P frente al ordenado.

Ejemplos (con Klipper lanzando la prueba a la vez desde Mainsail o la pantalla):
  python3 registro.py pasadas --segundos 120          # y PRUEBA_PASADAS N=100 VEL=600
  python3 registro.py avance --ordenado 635            # y PRUEBA_AVANCE N=100 PASO=6.35
  python3 registro.py analizar datos.csv --prueba-csv pasadas

Necesita pyserial: sudo apt install python3-serial
"""
import argparse
import csv
import glob
import statistics
import sys
import time

X_CUENTAS_MM = 180 / 25.4 * 2
Y_CUENTAS_VUELTA = 16384
Y_MM_VUELTA = 3.14159265 * 30


def puerto_pico():
    candidatos = glob.glob("/dev/serial/by-id/usb-MicroPython*")
    return candidatos[0] if candidatos else "/dev/ttyACM0"


def registrar(puerto, segundos, salida, hz):
    import serial

    filas = []
    with serial.Serial(puerto, 115200, timeout=1) as s:
        s.write(b"p\n")
        time.sleep(0.2)
        s.reset_input_buffer()
        s.write(b"f %d\nr\nc\n" % hz)
        print(f"Registrando {segundos} s a {hz} Hz desde {puerto}. Lanza ahora la prueba en Klipper.")
        fin = time.time() + segundos
        while time.time() < fin:
            linea = s.readline().decode(errors="replace").strip()
            if not linea or linea.startswith("#"):
                if linea:
                    print(linea)
                continue
            try:
                t_us, x, y = (int(v) for v in linea.split(","))
            except ValueError:
                continue
            filas.append((t_us / 1e6, x / X_CUENTAS_MM, y / Y_CUENTAS_VUELTA * Y_MM_VUELTA))
        s.write(b"p\n")
    with open(salida, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t_s", "x_mm", "y_mm"])
        w.writerows((f"{t:.6f}", f"{x:.4f}", f"{y:.4f}") for t, x, y in filas)
    print(f"{len(filas)} muestras en {salida}")
    return filas


def leer_csv(ruta):
    with open(ruta) as f:
        r = csv.reader(f)
        next(r)
        return [tuple(float(v) for v in fila) for fila in r]


def analizar_pasadas(filas, ventana=5):
    """Velocidad en la zona central de cada pasada y puntos de inversión."""
    if len(filas) < 3 * ventana:
        print("Muy pocas muestras")
        return
    vel = []
    for i in range(ventana, len(filas) - ventana):
        t0, x0, _ = filas[i - ventana]
        t1, x1, _ = filas[i + ventana]
        vel.append((filas[i][1], (x1 - x0) / (t1 - t0)))
    v_max = max(abs(v) for _, v in vel)
    xs = [x for x, _ in vel]
    x_min, x_max = min(xs), max(xs)
    centro = (x_min + x_max) / 2
    zona = (x_max - x_min) * 0.25            # mitad central del recorrido
    tramos = {+1: [], -1: []}
    for x, v in vel:
        if abs(x - centro) < zona and abs(v) > 0.5 * v_max:
            tramos[1 if v > 0 else -1].append(abs(v))

    # Inversiones: el extremo de X entre dos tramos de sentido contrario
    inv_izq, inv_der = [], []
    sentido, extremo = 0, None
    for x, v in vel:
        s = 1 if v > 0.05 * v_max else (-1 if v < -0.05 * v_max else 0)
        if s and sentido and s != sentido and extremo is not None:
            (inv_izq if s > 0 else inv_der).append(extremo)
            extremo = None
        if s:
            sentido = s
        extremo = x if extremo is None else (max(extremo, x) if sentido > 0 else min(extremo, x))

    print(f"Recorrido medido: {x_min:.2f} a {x_max:.2f} mm")
    for sentido, nombre in ((1, "hacia la derecha"), (-1, "hacia la izquierda")):
        v = tramos[sentido]
        if len(v) > 2:
            media = statistics.mean(v)
            rizado = statistics.pstdev(v) / media * 100
            estado = "OK" if rizado < 1 else "ALTO (objetivo < 1 %)"
            print(f"Velocidad {nombre}: {media:.1f} mm/s, rizado {rizado:.2f} % -> {estado}")
    cuenta = 1 / X_CUENTAS_MM
    for nombre, puntos in (("izquierda", inv_izq), ("derecha", inv_der)):
        if len(puntos) > 1:
            dispersion = max(puntos) - min(puntos)
            estado = "OK" if dispersion <= 2 * cuenta else "revisar (objetivo ±1 cuenta)"
            print(f"Inversión {nombre}: {len(puntos)} veces, dispersión {dispersion:.3f} mm "
                  f"({dispersion / cuenta:.1f} cuentas) -> {estado}")


def analizar_avance(filas, ordenado):
    medido = filas[-1][2] - filas[0][2]
    print(f"Avance medido por el encoder Y: {medido:.3f} mm")
    if ordenado:
        error = (medido - ordenado) / ordenado * 100
        estado = "OK" if abs(error) < 0.05 else "revisar (objetivo < 0,05 %)"
        print(f"Ordenado: {ordenado:.3f} mm, error {error:+.3f} % -> {estado}")
        print("Compara también con la marca del film medida con calibre: si el encoder "
              "y el calibre coinciden pero no con lo ordenado, corrige rotation_distance "
              f"multiplicándolo por {medido / ordenado:.5f}.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prueba", choices=["pasadas", "avance", "analizar"])
    ap.add_argument("csv", nargs="?", help="con 'analizar': archivo ya registrado")
    ap.add_argument("--prueba-csv", dest="tipo", choices=["pasadas", "avance"], default="pasadas",
                    help="con 'analizar': qué prueba contiene el archivo")
    ap.add_argument("--puerto", default=None)
    ap.add_argument("--segundos", type=float, default=60)
    ap.add_argument("--hz", type=int, default=500)
    ap.add_argument("--ordenado", type=float, default=0, help="avance ordenado en mm (prueba avance)")
    ap.add_argument("--salida", default=None)
    a = ap.parse_args()

    if a.prueba == "analizar":
        if not a.csv:
            sys.exit("Falta el archivo CSV")
        filas, tipo = leer_csv(a.csv), a.tipo
    else:
        salida = a.salida or time.strftime(f"{a.prueba}_%Y%m%d_%H%M%S.csv")
        filas, tipo = registrar(a.puerto or puerto_pico(), a.segundos, salida, a.hz), a.prueba
    if not filas:
        sys.exit("Sin datos: ¿está el Pico conectado y con main.py?")
    if tipo == "pasadas":
        analizar_pasadas(filas)
    else:
        analizar_avance(filas, a.ordenado)


if __name__ == "__main__":
    main()
