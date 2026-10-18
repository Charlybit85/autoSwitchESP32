import os
import time

import requests

SERVER_URL = os.getenv("SERVER_URL", "http://127.0.0.1:5000")
TIMEOUT = 3
INTERVALO = 2
rele = {"estado": "apagado"}


def simular_ciclo():
    respuesta = requests.get(
        f"{SERVER_URL}/api/esp32/config",
        timeout=TIMEOUT,
    )
    respuesta.raise_for_status()
    led_deseado = respuesta.json().get("led")
    if led_deseado not in ("on", "off"):
        raise ValueError("La API devolvió un estado de LED no válido.")

    estado_nuevo = "encendido" if led_deseado == "on" else "apagado"
    if rele["estado"] != estado_nuevo:
        rele["estado"] = estado_nuevo
        print(f"LED {estado_nuevo}")

    respuesta = requests.post(
        f"{SERVER_URL}/api/esp32/estado",
        json={"led": led_deseado},
        timeout=TIMEOUT,
    )
    respuesta.raise_for_status()


def main():
    print(f"Simulador conectado a {SERVER_URL}")
    while True:
        try:
            simular_ciclo()
        except requests.RequestException as error:
            print(f"No se pudo comunicar con la aplicación: {error}")
        time.sleep(INTERVALO)


if __name__ == "__main__":
    main()
