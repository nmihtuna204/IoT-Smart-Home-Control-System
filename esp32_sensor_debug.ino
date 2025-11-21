// ESP32 Sensor Debug Test - Upload này lên ESP32 để test sensors
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>

// Paste your CA certificate here
const char* ca_cert = R"EOF(
-----BEGIN CERTIFICATE-----
MIIDrzCCApegAwIBAgIQCDvgVpBCRrGhdWrJWZHHSjANBgkqhkiG9w0BAQUFADBh
MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3
d3cuZGlnaWNlcnQuY29tMSAwHgYDVQQDExdEaWdpQ2VydCBHbG9iYWwgUm9vdCBD
QTAeFw0wNjExMTAwMDAwMDBaFw0zMTExMTAwMDAwMDBaMGExCzAJBgNVBAYTAlVT
MRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMxGTAXBgNVBAsTEHd3dy5kaWdpY2VydC5j
b20xIDAeBgNVBAMTF0RpZ2lDZXJ0IEdsb2JhbCBSb290IENBMIIBIjANBgkqhkiG
9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4jvhEXLeqKTTo1eqUKKPC3eQyaKl7hLOllsB
CSDMAZOnTjC3U/dDxGkAV53ijSLdhwZAAIEJzs4bg7/fzTtxRuLWZscFs3YnFo97
nh6Vfe63SKMI2tavegw5BmV/Sl0fvBf4q77uKNd0f3p4mVmFaG5cIzJLv07A6Fpt
43C/dxC//AH2hdmoRBBYMql1GNXRor5H4idq9Joz+EkIYIvUX7Q6hL+hqkpMfT7P
T19sdl6gSzeRntwi5m3OFBqOasv+zbMUZBfHWymeMr/y7vrTC0LUq7dBMtoM1O/4
gdW7jVg/tRvoSSiicNoxBN33shbyTApOB6jtSj1etX+jkMOvJwIDAQABo2MwYTAO
BgNVHQ8BAf8EBAMCAYYwDwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQUA95QNVbR
TLtm8KPiGxvDl7I90VUwHwYDVR0jBBgwFoAUA95QNVbRTLtm8KPiGxvDl7I90VUw
DQYJKoZIhvcNAQEFBQADggEBAMucN6pIExIK+t1EnE9SsPTfrgT1eXkIoyQY/Esr
hMAtudXH/vTBH1jLuG2cenTnmCmrEbXjcKChzUyImZOMkXDiqw8cvpOp/2PV5Adg
06O/nVsJ8dWO41P0jmP6P6fbtGbfYmbW0W5BjfIttep3Sp+dWOIrWcBAI+0tKIJF
PnlUkiaY4IBIqDfv8NZ5YBberOgOzW6sRBc4L0na4UU+Krk2U886UAb3LujEV0ls
YSEY1QSteDwsOoBrp+uvFRTp2InBuThs4pFsiv9kuXclVzDAGySj4dzp30d8tbQk
CAUw7C29C79Fv1C5qfPrmAESrciIxpg0X40KPMbp1ZWVbd4=
-----END CERTIFICATE-----
)EOF";

// WiFi credentials
const char* ssid = "LittleBoiz";
const char* password = "10102004";

// MQTT broker (EMQX - Your secure broker)
const char* mqttServer = "vdd11821.ala.us-east-1.emqxsl.com";
const int mqttPort = 8883;
const char* mqttUser = "octiu123";
const char* mqttPassword = "octiu123";

// DHT setup for ESP32
#define DHTPIN 15  // GPIO15 on ESP32 (DHT11)
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// ESP32 Pin Configuration
const int lightPin = 17;           // GPIO17 (Light 1 control)
const int light2Pin = 16;          // GPIO16 (Light 2 control)
const int lightSensorPin = 32;     // GPIO36 (Light sensor - LDR)
const int motionSensorPin = 33;    // GPIO33 (PIR motion sensor)

WiFiClientSecure Tuan_1;
PubSubClient client(Tuan_1);

// Variables
bool motionDetected = false;
unsigned long lastMotionTime = 0;
unsigned long sensorInterval = 2000; // Reduced from 3000ms to 2000ms - send sensor data every 2 seconds
unsigned long lastSensorRead = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n\n🚀 ESP32 SENSOR DEBUG TEST 🚀");
  Serial.println("==============================");

  // Initialize pins
  pinMode(lightPin, OUTPUT);
  pinMode(light2Pin, OUTPUT);
  pinMode(lightSensorPin, INPUT);
  pinMode(motionSensorPin, INPUT);

  // Set initial states
  digitalWrite(lightPin, LOW);
  digitalWrite(light2Pin, LOW);

  // Test light sensors at startup
  Serial.println("🔍 Testing sensors at startup...");
  
  // Test motion sensor
  Serial.print("📱 Motion Sensor (GPIO33): ");
  Serial.println(digitalRead(motionSensorPin) ? "HIGH" : "LOW");
  
  // Test light sensor
  Serial.print("💡 Light Sensor (GPIO36): ");
  Serial.println(analogRead(lightSensorPin));
  
  Serial.println("==============================");

  // Initialize DHT sensor
  dht.begin();
  delay(500); // Reduced from 2000ms to 500ms
  
  // Setup WiFi and MQTT
  setupWiFi();
  Tuan_1.setCACert(ca_cert);
  client.setServer(mqttServer, mqttPort);
  client.setCallback(mqttCallback);
  
  Serial.println("✅ ESP32 sensor debug setup completed!");
  Serial.println("📊 Starting sensor monitoring...");
}

void setupWiFi() {
  Serial.print("🌐 Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(250);  // Reduced from 500ms to 250ms
    Serial.print(".");
  }
  Serial.println("\n✅ WiFi connected");
  Serial.print("📶 IP Address: ");
  Serial.println(WiFi.localIP());
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  String msg;
  for (unsigned int i = 0; i < length; i++) {
    msg += (char)payload[i];
  }
  
  Serial.print("📡 MQTT [");
  Serial.print(topic);
  Serial.print("]: ");
  Serial.println(msg);

  // ESP32 Light Controls - Process immediately for fast response
  if (String(topic) == "esp32/control/light") {
    bool isOn = (msg == "on");
    digitalWrite(lightPin, isOn ? HIGH : LOW);
    client.publish("esp32/status/light", isOn ? "on" : "off");
    Serial.print("💡 Light 1 (GPIO17): ");
    Serial.println(isOn ? "ON" : "OFF");
    
  } else if (String(topic) == "esp32/control/light2") {
    bool isOn = (msg == "on");
    digitalWrite(light2Pin, isOn ? HIGH : LOW);
    client.publish("esp32/status/light2", isOn ? "on" : "off");
    Serial.print("💡 Light 2 (GPIO16): ");
    Serial.println(isOn ? "ON" : "OFF");
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("🔌 Attempting MQTT connection...");
    if (client.connect("ESP32_SensorDebug", mqttUser, mqttPassword)) {
      Serial.println("✅ MQTT connected");
      
      // Subscribe to control topics
      client.subscribe("esp32/control/light");
      client.subscribe("esp32/control/light2");
      
      Serial.println("📡 Subscribed to control topics");
    } else {
      Serial.print("❌ MQTT failed, rc=");
      Serial.print(client.state());
      Serial.println(". Retrying in 2s");
      delay(2000);  // Reduced from 5000ms to 2000ms
    }
  }
}

void readSensors() {
  Serial.println("\n=== 📊 SENSOR READING ===");
  
  // Read DHT11 sensor
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  
  // Read light sensor with fewer samples for faster response
  long lightSum = 0;
  for(int i = 0; i < 3; i++) {  // Reduced from 5 to 3 samples
    lightSum += analogRead(lightSensorPin);
    delay(5);  // Reduced from 10ms to 5ms
  }
  int lightLevel = lightSum / 3; // Average of 3 readings
  int lightLux = map(lightLevel, 0, 4095, 0, 1000); // Convert to lux approximation
  
  // Read motion sensor with improved detection
  bool currentMotion = digitalRead(motionSensorPin);
  if (currentMotion && !motionDetected) {
    motionDetected = true;
    lastMotionTime = millis();
    Serial.println("🚶 MOTION DETECTED!");
  } else if (!currentMotion && (millis() - lastMotionTime > 5000)) {
    // Clear motion after 5 seconds of no detection
    if (motionDetected) {
      Serial.println("👻 Motion cleared");
    }
    motionDetected = false;
  }
  
  // Debug sensor readings
  Serial.print("🌡️  Temperature: ");
  if (!isnan(temperature)) {
    Serial.print(temperature);
    Serial.println("°C");
  } else {
    Serial.println("ERROR - Check DHT11 wiring!");
  }
  
  Serial.print("💧 Humidity: ");
  if (!isnan(humidity)) {
    Serial.print(humidity);
    Serial.println("%");
  } else {
    Serial.println("ERROR - Check DHT11 wiring!");
  }
  
  Serial.print("📱 Motion (GPIO33): ");
  Serial.print(currentMotion ? "TRIGGERED" : "CLEAR");
  Serial.print(" (State: ");
  Serial.print(motionDetected ? "DETECTED" : "NONE");
  Serial.println(")");
  
  Serial.print("💡 Light (GPIO36): ");
  Serial.print(lightLevel);
  Serial.print(" raw (");
  Serial.print(lightLux);
  Serial.println(" lux)");
  
  // Create JSON payload with both formats for compatibility
  StaticJsonDocument<200> doc;
  doc["temperature"] = isnan(temperature) ? 0 : temperature;
  doc["humidity"] = isnan(humidity) ? 0 : humidity;
  doc["motion"] = motionDetected ? 1 : 0;
  doc["light_level"] = lightLux;
  
  String jsonPayload;
  serializeJson(doc, jsonPayload);
  
  // Also create CSV format for backup compatibility
  String csvPayload = String(motionDetected ? 1 : 0) + "," + 
                     String(isnan(humidity) ? 0 : humidity) + "," + 
                     String(lightLux) + "," + 
                     String(isnan(temperature) ? 0 : temperature);
  
  // Publish both formats
  bool jsonPublished = client.publish("esp32/sensors", jsonPayload.c_str());
  bool csvPublished = client.publish("esp32/sensors_csv", csvPayload.c_str());
  
  Serial.print("📡 JSON Payload: ");
  Serial.println(jsonPayload);
  Serial.print("📡 CSV Payload: ");
  Serial.println(csvPayload);
  Serial.print("📤 JSON Published: ");
  Serial.println(jsonPublished ? "✅ SUCCESS" : "❌ FAILED");
  Serial.print("📤 CSV Published: ");
  Serial.println(csvPublished ? "✅ SUCCESS" : "❌ FAILED");
  Serial.println("========================");
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Read and publish sensor data every 2 seconds
  if (millis() - lastSensorRead >= sensorInterval) {
    readSensors();
    lastSensorRead = millis();
  }
  
  delay(50); // Reduced from 100ms to 50ms for faster response
}
