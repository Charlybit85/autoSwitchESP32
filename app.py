import os
from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)
ESP32_URL = os.getenv("ESP32_URL", "http://127.0.0.1:5001")
TIMEOUT = 3  # Tiempo de espera para las solicitudes al ESP32 LO CAMBIE COMO VARIABLE DE ENTORNO PARA QUE SEA MAS FACIL DE CAMBIAR

#ESP32_IP = "http://Colocare el ip del esp32(pendiente)" 
#estado = {"switch": "apagado"}

def pedir_al_esp32(ruta):
    try:
        respuesta = requests.get(f"{ESP32_URL}{ruta}", timeout=TIMEOUT)
        respuesta.raise_for_status()  # Lanza un error si la respuesta no es 200
        estadoReal=respuesta.json().get("estado", "desconocido")
        return jsonify(ok=True, estado=estadoReal)
    except requests.RequestException as e:
        return jsonify(ok=False, estado="desconocido", error="error no se puede conectatr al ESP32"), 502

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/estado")
def estado():
    return pedir_al_esp32("/estado")

@app.route("/encender", methods=["POST"])
def encender():
    return pedir_al_esp32("/on")

@app.route("/apagar", methods=["POST"])
def apagar():
    return pedir_al_esp32("/off")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)