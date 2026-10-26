import os
import secrets
import sqlite3
from flask import Flask, jsonify, render_template, request,session, redirect, url_for
from werkzeug.security import check_password_hash
from functools import wraps
app = Flask(__name__)
DB= os.path.join(os.path.dirname(os.path.abspath(__file__)), "usuarios.db")
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)
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
def buscar_usuario(nombre):
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row   # permite leer columnas por nombre
    try:
        return con.execute(
            "SELECT id, usuario, password_hash FROM usuarios WHERE usuario = ?",
            (nombre,),
        ).fetchone()
    finally:
        con.close()

def login_required(vista):
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if "usuario_id" not in session:
            # El JavaScript del dashboard espera JSON, no una página HTML
            if request.path.startswith("/api/") or request.method == "POST" \
               or request.path == "/estado":
                return jsonify(ok=False, error="Sesión no iniciada."), 401
            return redirect(url_for("login"))
        return vista(*args, **kwargs)
    return envoltura

@app.route("/templates/login.html", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        nombre = request.form.get("usuario", "").strip()
        password = request.form.get("password", "")
        fila = buscar_usuario(nombre)
        if fila and check_password_hash(fila["password_hash"], password):
            session.clear()
            session["usuario_id"] = fila["id"]
            session["usuario_nombre"] = fila["usuario"]
            return redirect(url_for("index"))
        error = "Credenciales inválidas."
    return render_template("login.html", error=error)

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))
@app.route("/")
@login_required
def index():
    return render_template("index.html", usuario=session["usuario_nombre"])

@app.route("/estado")
@login_required
def estado():
    return jsonify(ok=True, estado=estado_actual())

@app.route("/encender", methods=["POST"])
@login_required
def encender():
    return solicitar_estado("on")

@app.route("/apagar", methods=["POST"])
@login_required
def apagar():
    return solicitar_estado("off")


@app.route("/api/led", methods=["GET", "POST"])
@login_required
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