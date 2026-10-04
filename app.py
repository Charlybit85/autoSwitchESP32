from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

ESP32_IP = "http://Colocare el ip del esp32(pendiente)" 
estado = {"switch": "apagado"}

@app.route("/")
def index():
    return render_template("index.html", estado=estado["switch"])

@app.route("/encender", methods=["POST"])
def encender():
    try:
        requests.get(f"{ESP32_IP}/on", timeout=3)
        estado["switch"] = "encendido"
        return jsonify(ok=True, estado=estado["switch"])
    except requests.RequestException:
        return jsonify(ok=False, error="No se pudo contactar al ESP32"), 502

@app.route("/apagar", methods=["POST"])
def apagar():
    try:
        requests.get(f"{ESP32_IP}/off", timeout=3)
        estado["switch"] = "apagado"
        return jsonify(ok=True, estado=estado["switch"])
    except requests.RequestException:
        return jsonify(ok=False, error="No se pudo contactar al ESP32"), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)