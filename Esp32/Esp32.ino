#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>


const char* WIFI_SSID  = "TU_WIFI";
const char* WIFI_PASS  = "TU_CONTRASENA";
const char* SERVER_URL = "http://IP_DE_TU_COMPUTADORA:5000";

const int PIN_LED = 13;  

bool ledEncendido = false;
unsigned long ultimaConsulta = 0;
const unsigned long INTERVALO_MS = 2000;    // preguntar cada 2 segundos

void setup() {
  Serial.begin(115200);
  pinMode(PIN_LED, OUTPUT);
  digitalWrite(PIN_LED, LOW);

  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("Conectando a WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("IP del ESP32: ");
  Serial.println(WiFi.localIP());
}

// El post manda el estado del servidor
void reportarEstado() {
  HTTPClient http;
  http.begin(String(SERVER_URL) + "/api/esp32/estado");
  http.addHeader("Content-Type", "application/json");

  String cuerpo = String("{\"led\":\"") + (ledEncendido ? "on" : "off") + "\"}";
  int codigo = http.POST(cuerpo);

  Serial.printf("POST estado -> codigo %d\n", codigo);
  http.end();
}

// El get aqui toma los datos y recibe el orden del servidor
void consultarServidor() {
  HTTPClient http;
  http.begin(String(SERVER_URL) + "/api/esp32/config");
  int codigo = http.GET();

  if (codigo == 200) {
    String respuesta = http.getString(); 
    Serial.println("Respuesta: " + respuesta);

    JsonDocument doc;
    DeserializationError error = deserializeJson(doc, respuesta);

    if (!error) {
      String deseado = doc["led"] | "off";
      bool encender = (deseado == "on");

      if (encender != ledEncendido) {
        ledEncendido = encender;
        digitalWrite(PIN_LED, ledEncendido ? HIGH : LOW);
        Serial.println(ledEncendido ? "LED encendido" : "LED apagado");
      }
      http.end();
      reportarEstado();
      return;
    }
  } else {
    Serial.printf("GET config -> error %d\n", codigo);
  }
  http.end();
}

void loop() {
  if (WiFi.status() == WL_CONNECTED &&
      millis() - ultimaConsulta >= INTERVALO_MS) {
    ultimaConsulta = millis();
    consultarServidor();
  }
}