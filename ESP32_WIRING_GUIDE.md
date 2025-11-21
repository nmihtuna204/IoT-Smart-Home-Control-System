# ESP32 IoT Control System - Wiring Guide

## Hardware Components Needed:
- ESP32 WROOM development board
- DHT11 temperature & humidity sensor
- Light sensor (LDR/Photoresistor)
- LED for light control
- DC motor with L298N driver
- Small DC fan
- Breadboard and jumper wires

## Pin Connections:

### Sensors:
- **DHT11** → GPIO4 (Pin 4)
  - VCC → 3.3V
  - GND → GND
  - DATA → GPIO4

- **Light Sensor (LDR)** → GPIO36 (ADC1_CH0)
  - One terminal → 3.3V
  - Other terminal → GPIO36
  - Add 10kΩ resistor between GPIO36 and GND

### Actuators:
- **LED (Light Control)** → GPIO14
  - Anode (+) → GPIO14
  - Cathode (-) → GND (via 220Ω resistor)

- **Fan Control** → GPIO12
  - Connect to relay module or transistor circuit
  - Relay IN → GPIO12
  - VCC → 5V
  - GND → GND

- **DC Motor** → L298N Driver
  - Motor Pin1 → GPIO13 (Forward)
  - Motor Pin2 → GPIO15 (Backward)
  - L298N ENA → 3.3V (or PWM pin for speed control)
  - L298N VCC → 12V (for motor power)
  - L298N GND → GND

## Circuit Diagram:
```
ESP32 WROOM
┌─────────────────┐
│                 │
│ 3.3V ──┬─── DHT11 VCC
│         │
│ GPIO4 ──┴─── DHT11 DATA
│
│ 3.3V ──┬─── LDR ── GPIO36
│         │
│         └─── 10kΩ ── GND
│
│ GPIO14 ──┬─── LED(+) ── 220Ω ── GND
│
│ GPIO12 ──┴─── Relay IN
│
│ GPIO13 ──┴─── L298N IN1
│ GPIO15 ──┴─── L298N IN2
│
│ GND ────────── GND
└─────────────────┘
```

## Libraries Required:
1. **WiFi** (built-in)
2. **PubSubClient** (install via Library Manager)
3. **DHT sensor library** (install via Library Manager)

## Installation Steps:
1. Open Arduino IDE
2. Go to Tools → Board → ESP32 Arduino → ESP32 WROOM Module
3. Install required libraries:
   - Sketch → Include Library → Manage Libraries
   - Search and install:
     - "PubSubClient" by Nick O'Leary
     - "DHT sensor library" by Adafruit

## Upload Instructions:
1. Connect ESP32 to computer via USB
2. Select correct COM port
3. Open `esp32_iot_control.ino`
4. Update WiFi credentials if needed
5. Click Upload

## Testing:
1. Open Serial Monitor (115200 baud)
2. Check WiFi connection
3. Check MQTT connection
4. Test sensor readings
5. Test actuator controls via web interface

## Troubleshooting:
- **WiFi not connecting**: Check SSID and password
- **MQTT connection failed**: Check internet connection and EMQX credentials
- **Sensors not reading**: Check wiring and power supply
- **Actuators not responding**: Check GPIO pins and power supply

## Notes:
- GPIO14 is used for light control (LED)
- All sensors and actuators are properly isolated
- TLS is configured for secure MQTT communication
- Status feedback is sent back to web interface 