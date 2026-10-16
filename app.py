from flask import Flask, jsonify, request

app = Flask(__name__)

datos = {
    "led_deseado": "off",
    "led_reportado": None,
}

@app.route("/api/led", methods=["POST"])
def cambiar_led():
    cuerpo = request.get_json()
    nuevo = cuerpo.get("estado") 

    if nuevo not in ("on", "off"):
        return jsonify(error="estado debe ser 'on' u 'off'"), 400

    datos["led_deseado"] = nuevo
    return jsonify(ok=True, led_deseado=nuevo)

@app.route("/api/led", methods=["GET"])
def consultar_led():
    return jsonify(
        led_deseado=datos["led_deseado"],
        led_reportado=datos["led_reportado"],
    )


# Esto es del esp32
@app.route("/api/esp32/config", methods=["GET"])
def esp32_config():
    return jsonify(led=datos["led_deseado"])

@app.route("/api/esp32/estado", methods=["POST"])
def esp32_estado():
    cuerpo = request.get_json()
    datos["led_reportado"] = cuerpo.get("led")
    return jsonify(ok=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)