#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* WIFI_SSID  = "Samsung123";
const char* WIFI_PASS  = "12345678";
const char* SERVER_URL = "http://10.55.252.87:5000";
#define RELAY_PIN 13

// const int PIN_LED = 2;  
const bool RELAY_ACTIVE_LOW =false;

bool relevadorActivo = false;
unsigned long ultimaConsulta = 0;
const unsigned long INTERVALO_MS = 2000;    // preguntar cada 2 segundos

void aplicar_estado(bool encendido){
  relevadorActivo=encendido;
  bool nivelGPIO = RELAY_ACTIVE_LOW ? !encendido : encendido;
  digitalWrite(RELAY_PIN, nivelGPIO ? HIGH : LOW);
  Serial.println(encendido ? "RELEVADOR ACTIVADO" : "RELEVADOR DESACTIVADO");
}
void reportarEstado() {
  if(WiFi.status()!=WL_CONNECTED) return;
  HTTPClient http;
  http.begin(String(SERVER_URL) + "/api/esp32/estado");
  http.addHeader("Content-Type", "application/json");
  http.setTimeout(3000);
  JsonDocument doc;
  doc["led"] = relevadorActivo ? "on" : "off";
  String cuerpo;
  serializeJson(doc,cuerpo);


  // String cuerpo = String("{\"led\":\"") + (ledEncendido ? "on" : "off") + "\"}";
  int codigo = http.POST(cuerpo);

  Serial.printf("POST estado -> codigo %d\n", codigo);
  if (codigo<0){
    Serial.println(http.errorToString(codigo));
  }
  http.end();
}

// El get aqui toma los datos y recibe el orden del servidor
void consultarServidor() {
  if(WiFi.status()!=WL_CONNECTED) return;
  HTTPClient http;
  http.begin(String(SERVER_URL) + "/api/esp32/config");
  http.setTimeout(3000);

  int codigo = http.GET();
  bool huboCambio=false;

  if (codigo == HTTP_CODE_OK) {
    String respuesta = http.getString(); 
    Serial.println("Respuesta: " + respuesta);

    JsonDocument doc;
    DeserializationError error = deserializeJson(doc, respuesta);

    if (!error) {
      const char* valor =doc["led"]|"off";
      // String deseado = doc["led"] | "off";
      // bool encender = (deseado == "on");

  //     if (encender != ledEncendido) {
  //       ledEncendido = encender;
  //       digitalWrite(RELAY_PIN, ledEncendido ? HIGH : LOW);
  //       Serial.println(ledEncendido ? "LED encendido" : "LED apagado");
  //     }
  //     http.end();
  //     reportarEstado();
  //     return;
  //   }
  // } else {
  //   Serial.printf("GET config -> error %d\n", codigo);
  // }
  // http.end();
  if (strcmp(valor, "on") == 0) {
        if (!relevadorActivo) {
          aplicar_estado(true);
          huboCambio = true;
        }
      } else if (strcmp(valor, "off") == 0) {
        if (relevadorActivo) {
          aplicar_estado(false);
          huboCambio = true;
        }
      } else {
        Serial.println("Orden desconocida; se conserva el estado.");
      }
    } else {
      Serial.print("Error JSON: ");
      Serial.println(error.c_str());
    }
  } else {
    Serial.printf("GET config -> error %d\n", codigo);
    if (codigo < 0) Serial.println(http.errorToString(codigo));
  }

  http.end();

  if (huboCambio) reportarEstado();
}
void setup() {
  Serial.begin(115200);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, RELAY_ACTIVE_LOW ? HIGH:LOW);

  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("Conectando a WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("IP del ESP32: ");
  Serial.println(WiFi.localIP());
  reportarEstado();
}

// El post manda el estado del servidor


void loop() {
  if (WiFi.status() != WL_CONNECTED){
    WiFi.reconnect();
    delay(500);
    return;
  }
  if(millis() -ultimaConsulta>=INTERVALO_MS){
    ultimaConsulta = millis();
    consultarServidor();
  }
}