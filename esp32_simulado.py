from flask import Flask, jsonify

app = Flask(__name__)
rele={"estado": "apagado"} #con esto simulamos el estado del rele

@app.route("/on")
def on():
    rele["estado"] = "encendido"
    return jsonify(estado=rele["estado"])

@app.route("/off")
def off():
    rele["estado"] = "apagado"
    return jsonify(estado=rele["estado"])

@app.route("/estado")
def estado():
    return jsonify(estado=rele["estado"])

if __name__ == "__main__":
    app.run(port=5001)