# ESP8266 SENSOR DEBUG WIRING GUIDE

## 🔌 PIN CONFIGURATION

### ESP8266 NodeMCU Pin Mapping
```
ESP8266 GPIO   NodeMCU Pin   Function
GPIO2          D4            DHT11 Data
GPIO5          D1            Light 1 Control
GPIO4          D2            Light 2 Control  
GPIO14         D5            PIR Motion Sensor
A0             A0            Light Sensor (LDR)
3.3V           3V3           Power for sensors
GND            GND           Ground
```

## 🛠️ SENSOR CONNECTIONS

### 1. DHT11 Temperature & Humidity Sensor
```
DHT11 Pin    ESP8266 Pin
VCC          3V3
GND          GND  
DATA         D4 (GPIO2)
```

### 2. PIR Motion Sensor
```
PIR Pin      ESP8266 Pin
VCC          3V3
GND          GND
OUT          D5 (GPIO14)
```

### 3. Light Sensor (LDR with 10kΩ resistor)
```
Circuit:
3V3 ----[LDR]----[A0]----[10kΩ resistor]---- GND
                  |
              ESP8266 A0
```

### 4. LED Controls (Optional)
```
LED 1:
D1 (GPIO5) ----[220Ω resistor]----[LED+]----[LED-]---- GND

LED 2:  
D2 (GPIO4) ----[220Ω resistor]----[LED+]----[LED-]---- GND
```

## 📊 EXPECTED SERIAL OUTPUT

```
🚀 ESP8266 SENSOR DEBUG TEST 🚀
==============================
🔍 Testing sensors at startup...
📱 Motion Sensor (D5): LOW
💡 Light Sensor (A0): 512
==============================
🌐 Connecting to WiFi....
✅ WiFi connected
📶 IP Address: 192.168.1.100
🔌 Attempting MQTT connection...✅ MQTT connected
📡 Subscribed to control topics
✅ ESP8266 sensor debug setup completed!
📊 Starting sensor monitoring...

=== 📊 SENSOR READING ===
🌡️  Temperature: 25.0°C
💧 Humidity: 60.0%
📱 Motion (D5): CLEAR (State: NONE)
💡 Light (A0): 512 raw (500 lux)
📡 JSON Payload: {"temperature":25,"humidity":60,"motion":0,"light_level":500}
📡 CSV Payload: 0,60.0,500,25.0
📤 JSON Published: ✅ SUCCESS
📤 CSV Published: ✅ SUCCESS
========================
```

## 🔧 TROUBLESHOOTING

### WiFi Connection Issues
- Check SSID and password in code
- Ensure 2.4GHz WiFi network
- Check signal strength

### MQTT Connection Issues  
- Verify MQTT credentials
- Check certificate settings
- Use `espClient.setInsecure()` for testing

### Sensor Issues
- **DHT11**: Check wiring and 3.3V power
- **PIR**: Ensure proper trigger sensitivity
- **LDR**: Check 10kΩ pull-down resistor
- **LEDs**: Check resistor values and polarity

### Libraries Required
```
ESP8266WiFi
PubSubClient  
DHT sensor library
ArduinoJson
```

## 📡 MQTT TOPICS

### ESP8266 Publishes:
- `esp8266/sensors` - JSON sensor data
- `esp8266/sensors_csv` - CSV sensor data
- `esp8266/status/light` - Light 1 status
- `esp8266/status/light2` - Light 2 status

### ESP8266 Subscribes:
- `esp8266/control/light` - Light 1 control
- `esp8266/control/light2` - Light 2 control
