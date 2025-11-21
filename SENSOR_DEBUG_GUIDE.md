# ESP32 Sensor Debug Instructions

## 🔧 Cài đặt Library cần thiết:

1. **Mở Arduino IDE**
2. **Tools -> Manage Libraries**
3. **Tìm và cài đặt:**
   - `ArduinoJson` by Benoit Blanchon
   - `DHT sensor library` by Adafruit (nếu chưa có)
   - `PubSubClient` by Nick O'Leary (nếu chưa có)

## 📱 Upload Code Debug:

1. **Upload file `esp32_sensor_debug.ino` lên ESP32**
2. **Mở Serial Monitor (115200 baud)**
3. **Quan sát output debug**

## 🔍 Kiểm tra kết nối Sensor:

### Motion Sensor (PIR):
- **GPIO33** -> PIR OUT pin
- **3.3V** -> PIR VCC
- **GND** -> PIR GND

### Light Sensor (LDR):
- **GPIO36** -> One leg of LDR
- **3.3V** -> Other leg of LDR through 10kΩ resistor
- **GND** -> Junction of LDR and resistor

### DHT11:
- **GPIO15** -> DHT11 Data pin
- **3.3V** -> DHT11 VCC
- **GND** -> DHT11 GND

## 📊 Expected Serial Output:

```
🚀 ESP32 SENSOR DEBUG TEST 🚀
==============================
🔍 Testing sensors at startup...
📱 Motion Sensor (GPIO33): LOW
💡 Light Sensor (GPIO36): 1234
==============================
🌐 Connecting to WiFi.....
✅ WiFi connected
📶 IP Address: 192.168.1.xxx
🔌 Attempting MQTT connection...✅ MQTT connected
📡 Subscribed to control topics
✅ ESP32 sensor debug setup completed!
📊 Starting sensor monitoring...

=== 📊 SENSOR READING ===
🌡️  Temperature: 25.4°C
💧 Humidity: 60.2%
📱 Motion (GPIO33): CLEAR (State: NONE)
💡 Light (GPIO36): 1234 raw (300 lux)
📡 JSON Payload: {"temperature":25.4,"humidity":60.2,"motion":0,"light_level":300}
📡 CSV Payload: 0,60.2,300,25.4
📤 JSON Published: ✅ SUCCESS
📤 CSV Published: ✅ SUCCESS
========================
```

## ⚠️ Troubleshooting:

### Nếu Motion Sensor không hoạt động:
- Kiểm tra wiring GPIO33
- Đảm bảo PIR có nguồn 3.3V
- PIR cần 30-60 giây để warm up

### Nếu Light Sensor không hoạt động:
- Kiểm tra LDR và resistor
- Thử che/chiếu sáng để test

### Nếu DHT11 lỗi:
- Kiểm tra wiring GPIO15
- Đảm bảo DHT11 có nguồn 3.3V (không phải 5V)

## 🎯 Mục tiêu:
- Tất cả sensors đều có readings
- MQTT publish thành công
- Web app nhận được real sensor data
