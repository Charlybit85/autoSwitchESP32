from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
datos = {
    "led_deseado": "off",
    "led_reportado": None,
}


def estado_actual():
    estados = {"on": "encendido", "off": "apagado"}
    return estados.get(datos["led_reportado"], "desconocido")


def solicitar_estado(led):
    datos["led_deseado"] = led
    return jsonify(
        ok=True,
        estado=estado_actual(),
        led_deseado=led,
    ), 202

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/estado")
def estado():
    return jsonify(ok=True, estado=estado_actual())

@app.route("/encender", methods=["POST"])
def encender():
    return solicitar_estado("on")

@app.route("/apagar", methods=["POST"])
def apagar():
    return solicitar_estado("off")


@app.route("/api/led", methods=["GET", "POST"])
def led():
    if request.method == "GET":
        return jsonify(
            led_deseado=datos["led_deseado"],
            led_reportado=datos["led_reportado"],
        )

    cuerpo = request.get_json(silent=True)
    nuevo = cuerpo.get("estado") if isinstance(cuerpo, dict) else None
    if nuevo not in ("on", "off"):
        return jsonify(error="estado debe ser 'on' u 'off'"), 400

    return solicitar_estado(nuevo)


@app.route("/api/esp32/config")
def esp32_config():
    return jsonify(led=datos["led_deseado"])


@app.route("/api/esp32/estado", methods=["POST"])
def esp32_estado():
    cuerpo = request.get_json(silent=True)
    reportado = cuerpo.get("led") if isinstance(cuerpo, dict) else None
    if reportado not in ("on", "off"):
        return jsonify(error="led debe ser 'on' u 'off'"), 400

    datos["led_reportado"] = reportado
    return jsonify(ok=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)