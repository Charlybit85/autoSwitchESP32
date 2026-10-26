const indicator = document.getElementById("indicator");
const estadoText = document.getElementById("estadoText");
const errorText = document.getElementById("error");
const buttons = [
  document.getElementById("btn-encender"),
  document.getElementById("btn-apagar")
];

function mostrarEstado(estado) {
  const estados = {
    encendido: "Encendido",
    apagado: "Apagado"
  };
  const estadoValido = Object.hasOwn(estados, estado) ? estado : "desconocido";

  indicator.className = `indicador ${estadoValido}`;
  estadoText.textContent = estados[estadoValido] || "Desconocido";
}

function mostrarError(mensaje) {
  errorText.textContent = mensaje;
  errorText.hidden = !mensaje;
}

async function solicitarEstado(ruta, metodo = "GET") {
  const respuesta = await fetch(ruta, { method: metodo });
  if (respuesta.status === 401) {
  window.location.href = "/login";
  throw new Error("Sesión caducada.");
}
  const datos = await respuesta.json();

  if (!respuesta.ok || datos.ok === false) {
    throw new Error(datos.error || "No se pudo completar la solicitud.");
  }
  if (typeof datos.estado !== "string") {
    throw new Error("La respuesta del servidor no contiene un estado válido.");
  }

  return datos.estado;
}

async function actualizarEstado() {
  try {
    mostrarEstado(await solicitarEstado("/estado"));
    mostrarError("");
  } catch (error) {
    mostrarEstado("desconocido");
    mostrarError(error.message || "No se pudo consultar el estado del interruptor.");
  }
}

async function cambiarEstado(ruta) {
  buttons.forEach((button) => {
    button.disabled = true;
  });
  mostrarError("");

  try {
    mostrarEstado(await solicitarEstado(ruta, "POST"));
  } catch (error) {
    mostrarError(error.message || "No se pudo cambiar el estado del interruptor.");
  } finally {
    buttons.forEach((button) => {
      button.disabled = false;
    });
  }
}

buttons[0].addEventListener("click", () => cambiarEstado("/encender"));
buttons[1].addEventListener("click", () => cambiarEstado("/apagar"));
actualizarEstado();
setInterval(actualizarEstado, 2000);
