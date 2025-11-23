# 🏠 IoT Smart Home Control System

<div align="center">

![IoT](https://img.shields.io/badge/IoT-Enabled-blue)
![ESP32](https://img.shields.io/badge/ESP32-Supported-green)
![ESP8266](https://img.shields.io/badge/ESP8266-Supported-green)
![MQTT](https://img.shields.io/badge/MQTT-TLS%2FSSL-orange)
![Python](https://img.shields.io/badge/Python-3.8+-yellow)
![Flask](https://img.shields.io/badge/Flask-2.3.3-red)

**A secure, real-time IoT control system for smart home automation using ESP32/ESP8266 microcontrollers, MQTT protocol, and modern web technologies.**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Hardware Setup](#-hardware-setup) • [Usage](#-usage) • [API](#-api-endpoints)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Technologies Used](#-technologies-used)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Hardware Setup](#-hardware-setup)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [Troubleshooting](#-troubleshooting)
- [Security Features](#-security-features)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

This IoT Smart Home Control System is a comprehensive solution for home automation that enables real-time monitoring and control of IoT devices through a secure MQTT broker. The system supports both ESP32 and ESP8266 microcontrollers, providing flexibility in hardware choices while maintaining a unified control interface.

### 🌟 Key Highlights

- **Multi-Board Support**: Control multiple ESP32 and ESP8266 devices simultaneously
- **Real-time Monitoring**: Live sensor data from DHT11 (temperature/humidity), PIR (motion), and LDR (light) sensors
- **Secure Communication**: TLS/SSL encrypted MQTT communication via EMQX Cloud
- **Modern Web Interface**: Responsive, real-time dashboard built with Flask
- **Data Persistence**: SQLite database for sensor data logging and device status
- **Simulator Tool**: Test the system without physical hardware using the included GUI simulator

---

## ✨ Features

### 🔐 Security
- ✅ **TLS/SSL Encryption**: All MQTT traffic encrypted using port 8883
- ✅ **CA Certificate Verification**: Validates EMQX broker identity
- ✅ **HTTPS Support**: Web dashboard served over HTTPS
- ✅ **Credential Management**: Secure environment variable configuration

### 📊 Monitoring
- 🌡️ **Temperature Monitoring**: Real-time temperature readings (DHT11)
- 💧 **Humidity Monitoring**: Ambient humidity tracking
- 🚶 **Motion Detection**: PIR sensor integration for presence detection
- 💡 **Light Level Sensing**: LDR-based ambient light monitoring

### 🎛️ Control
- 💡 **Device Control**: Remote on/off control for multiple devices
- 🔄 **Status Synchronization**: Real-time device status updates
- 📱 **Multi-Device Support**: Control ESP32 and ESP8266 boards independently
- 🌐 **Web-Based Interface**: Access from any device with a browser

### 📈 Data Management
- 💾 **Data Logging**: SQLite database for historical data
- 📉 **Sensor History**: Track sensor readings over time
- 🔄 **Status Persistence**: Device states saved across restarts

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Browser (Client)                    │
│                  https://localhost:5000                     │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Flask Web Server                          │
│            (app.py - Python Backend)                        │
│  • REST API Endpoints                                       │
│  • Real-time Data Processing                               │
│  • SQLite Database Management                              │
└────────────────────────┬────────────────────────────────────┘
                         │ MQTT TLS/SSL (Port 8883)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              EMQX Cloud MQTT Broker                         │
│            vdd11821.ala.us-east-1.emqxsl.com               │
│  • Topic: esp32/sensors, esp32/control/*, esp32/status/*  │
│  • Topic: esp8266/sensors, esp8266/control/*, ...         │
└────────────────────────┬────────────────────────────────────┘
                         │ MQTT TLS/SSL
         ┌───────────────┴───────────────┐
         ▼                               ▼
┌──────────────────┐            ┌──────────────────┐
│   ESP32 Board    │            │  ESP8266 Board   │
│  • DHT11 Sensor  │            │  • DHT11 Sensor  │
│  • PIR Sensor    │            │  • PIR Sensor    │
│  • LDR Sensor    │            │  • LDR Sensor    │
│  • LED/Relay x2  │            │  • LED/Relay x2  │
└──────────────────┘            └──────────────────┘
```

---

## 🛠️ Technologies Used

### Backend
- **Python 3.8+**: Core programming language
- **Flask 2.3.3**: Web framework for API and dashboard
- **Paho MQTT**: MQTT client library
- **SQLite**: Lightweight database for data persistence
- **python-dotenv**: Environment variable management

### Frontend
- **HTML5/CSS3**: Modern web interface
- **JavaScript (Vanilla)**: Real-time data updates
- **Responsive Design**: Mobile-friendly interface

### IoT Hardware
- **ESP32/ESP8266**: Microcontrollers with WiFi capability
- **DHT11**: Temperature and humidity sensor
- **PIR**: Motion detection sensor
- **LDR**: Light-dependent resistor
- **LEDs/Relays**: Output devices for control

### Communication
- **MQTT Protocol**: Lightweight pub/sub messaging
- **EMQX Cloud**: Managed MQTT broker with TLS/SSL
- **TLS/SSL**: Encrypted communication

---

## 📋 Prerequisites

### Software Requirements
- Python 3.8 or higher
- Arduino IDE (for programming ESP32/ESP8266)
- Git (for version control)

### Hardware Requirements
- ESP32 or ESP8266 development board
- DHT11 temperature/humidity sensor
- PIR motion sensor
- LDR (Light Dependent Resistor)
- LEDs or relay modules
- Jumper wires and breadboard
- USB cable for programming

### MQTT Broker
- EMQX Cloud account (free tier available)
- Or any other MQTT broker with TLS/SSL support

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/nmihtuna204/IoT-Smart-Home-Control-System.git
cd iot-smart-home
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy the example config file
cp config.env.example config.env

# Edit config.env with your MQTT broker credentials
# Use a text editor to update:
#   - MQTT_BROKER
#   - MQTT_USERNAME
#   - MQTT_PASSWORD
#   - CA_CERT_PATH (if using EMQX Cloud)
```

### 5. Generate SSL Certificates (for HTTPS)

```bash
# Generate self-signed certificate for development
openssl req -x509 -newkey rsa:4096 -nodes -out self_signed_cert.pem -keyout private_key.pem -days 365
```

### 6. Download CA Certificate (for EMQX Cloud)

- Log in to your EMQX Cloud console
- Navigate to your deployment
- Download the CA certificate file
- Save it as `emqxsl-ca.crt` in the project root

---

## 🔌 Hardware Setup

### ESP32 Wiring Diagram

See [ESP32_WIRING_GUIDE.md](ESP32_WIRING_GUIDE.md) for detailed wiring instructions.

**Quick Reference:**

```
DHT11:
  - VCC → 3.3V
  - GND → GND
  - DATA → GPIO 4

PIR Sensor:
  - VCC → 5V
  - GND → GND
  - OUT → GPIO 5

LDR:
  - One leg → 3.3V
  - Other leg → GPIO 34 (ADC) + 10kΩ resistor to GND

LED 1 (Light 1):
  - Anode → GPIO 2 (via 220Ω resistor)
  - Cathode → GND

LED 2 (Light 2):
  - Anode → GPIO 15 (via 220Ω resistor)
  - Cathode → GND
```

### ESP8266 Wiring Diagram

See [ESP8266_WIRING_GUIDE.md](ESP8266_WIRING_GUIDE.md) for detailed wiring instructions.

### Arduino Library Installation

Required libraries (install via Arduino Library Manager):

1. **WiFiClientSecure** (built-in)
2. **PubSubClient** by Nick O'Leary
3. **DHT sensor library** by Adafruit
4. **Adafruit Unified Sensor** (dependency)
5. **ArduinoJson** by Benoit Blanchon

### Upload Arduino Code

1. Open `esp32_sensor_debug.ino` or `esp8266_iot_control.ino` in Arduino IDE
2. Update the following in `arduino_config.h`:
   - WiFi SSID and password
   - MQTT broker address
   - MQTT username and password
3. Select the correct board and port
4. Upload the code

---

## ⚙️ Configuration

### config.env File

```env
# MQTT Broker Configuration
MQTT_BROKER=your-broker.emqxsl.com
MQTT_PORT=8883
MQTT_USERNAME=your_username
MQTT_PASSWORD=your_password

# TLS/SSL Configuration
CA_CERT_PATH=emqxsl-ca.crt

# Database Configuration
DATABASE_PATH=iot_data.db

# Flask Configuration
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=True

# SSL Certificate paths
SSL_CERT=self_signed_cert.pem
SSL_KEY=private_key.pem
```

### Arduino Configuration (arduino_config.h)

Update your WiFi and MQTT credentials:

```cpp
// WiFi credentials
const char* ssid = "Your_WiFi_SSID";
const char* password = "Your_WiFi_Password";

// MQTT Broker settings
const char* mqtt_broker = "your-broker.emqxsl.com";
const int mqtt_port = 8883;
const char* mqtt_username = "your_username";
const char* mqtt_password = "your_password";
```

---

## 💻 Usage

### Start the Web Application

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Run the Flask app
python app.py
```

The web dashboard will be available at: **https://localhost:5000**

### Using the Simulator (Without Hardware)

For testing without physical hardware:

```bash
python simulator.py
```

The simulator provides:
- GUI for monitoring sensor data
- Device control interface
- MQTT connection testing
- Simulated sensor data generation

### Web Dashboard Features

1. **Real-time Monitoring**
   - View live sensor data from all connected boards
   - Motion detection alerts
   - Temperature, humidity, and light level readings

2. **Device Control**
   - Toggle lights on/off
   - Control multiple devices per board
   - Instant status feedback

3. **Connection Status**
   - MQTT connection indicator
   - Last sensor update timestamp

---

## 📁 Project Structure

```
iot-smart-home/
│
├── app.py                      # Flask web application (main server)
├── simulator.py                # GUI simulator for testing
├── requirements.txt            # Python dependencies
├── config.env.example          # Example configuration file
├── .gitignore                  # Git ignore rules
│
├── arduino_config.h            # Arduino configuration header
├── esp32_sensor_debug.ino     # ESP32 Arduino code
├── esp32_test_led.ino         # ESP32 LED test code
├── esp8266_iot_control.ino    # ESP8266 Arduino code  
├── esp8266_sensor_debug.ino   # ESP8266 sensor debug code
├── esp8266_test_led.ino       # ESP8266 LED test code
│
├── templates/
│   └── index.html             # Web dashboard HTML
│
├── ESP32_WIRING_GUIDE.md      # ESP32 hardware setup guide
├── ESP8266_WIRING_GUIDE.md    # ESP8266 hardware setup guide
├── SENSOR_DEBUG_GUIDE.md      # Sensor troubleshooting guide
│
└── README.md                  # This file
```

---

## 🔗 API Endpoints

### GET Endpoints

#### `/`
- **Description**: Web dashboard home page
- **Returns**: HTML page

#### `/sensor_data`
- **Description**: Get current sensor readings from all boards
- **Returns**: JSON
```json
{
  "esp32": {
    "motion": false,
    "temperature": 25.5,
    "humidity": 60.0,
    "light_level": 450,
    "timestamp": "2024-11-21T10:30:00"
  },
  "esp8266": {
    "motion": true,
    "temperature": 26.0,
    "humidity": 55.0,
    "light_level": 380,
    "timestamp": "2024-11-21T10:30:00"
  }
}
```

#### `/device_status`
- **Description**: Get current status of all devices
- **Returns**: JSON
```json
{
  "esp32": {
    "light": "on",
    "light2": "off"
  },
  "esp8266": {
    "light": "off",
    "light2": "on"
  }
}
```

#### `/mqtt_status`
- **Description**: Check MQTT connection status
- **Returns**: JSON
```json
{
  "connected": true,
  "broker": "vdd11821.ala.us-east-1.emqxsl.com",
  "port": 8883,
  "message": "MQTT Connected"
}
```

### POST Endpoints

#### `/control/<board>`
- **Description**: Control devices on a specific board
- **Parameters**:
  - `board`: "esp32" or "esp8266"
- **Body**: JSON
```json
{
  "device": "light",
  "action": "on"
}
```
- **Returns**: JSON
```json
{
  "status": "success",
  "action": "on",
  "board": "esp32",
  "device": "light"
}
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. MQTT Connection Failed

**Problem**: Cannot connect to MQTT broker

**Solutions**:
- ✅ Check `config.env` credentials
- ✅ Verify CA certificate path
- ✅ Ensure port 8883 is not blocked by firewall
- ✅ Check EMQX Cloud deployment status

#### 2. No Sensor Data Received

**Problem**: Web dashboard shows "No data received"

**Solutions**:
- ✅ Verify ESP32/ESP8266 is connected to WiFi
- ✅ Check Arduino Serial Monitor for connection status
- ✅ Confirm MQTT topics match in Arduino code and Flask app
- ✅ Test sensors individually using debug sketches
- ✅ See [SENSOR_DEBUG_GUIDE.md](SENSOR_DEBUG_GUIDE.md)

#### 3. Certificate Errors

**Problem**: SSL/TLS certificate validation fails

**Solutions**:
- ✅ Re-download CA certificate from EMQX Cloud
- ✅ Ensure certificate file is in project root
- ✅ Check certificate is not expired
- ✅ Verify file permissions

#### 4. Device Control Not Working

**Problem**: Clicking buttons doesn't control devices

**Solutions**:
- ✅ Check MQTT connection status indicator
- ✅ Verify ESP board is subscribed to control topics
- ✅ Check Arduino Serial Monitor for received messages
- ✅ Ensure GPIO pins are correctly wired
- ✅ Test LED/relay with test sketches

### Debug Mode

Enable verbose logging in `config.env`:

```env
FLASK_DEBUG=True
```

Check Flask console for detailed MQTT messages and errors.

---

## 🔒 Security Features

### Implemented Security Measures

1. **Transport Layer Security**
   - TLS/SSL encryption for all MQTT traffic
   - Port 8883 (secure MQTT) instead of 1883
   - CA certificate verification

2. **Credential Management**
   - Environment variables for sensitive data
   - `.gitignore` prevents credential leaks
   - Example config file for easy setup

3. **HTTPS Web Interface**
   - SSL certificates for web dashboard
   - Encrypted browser-server communication

4. **Database Security**
   - SQLite file excluded from version control
   - Parameterized queries prevent SQL injection

### Security Best Practices

⚠️ **Important Reminders**:

1. **Never commit sensitive files**:
   - `config.env`
   - `*.pem`, `*.key`, `*.crt`
   - `iot_data.db`

2. **Use strong passwords** for MQTT broker

3. **Regenerate certificates** for production use

4. **Restrict firewall rules** to necessary ports only

5. **Keep dependencies updated**:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

---

## 🚀 Future Enhancements

### Planned Features

- [ ] **User Authentication**: Login system for web dashboard
- [ ] **Historical Charts**: Visualize sensor data trends
- [ ] **Email/SMS Alerts**: Notifications for critical events
- [ ] **Mobile App**: Native iOS/Android application
- [ ] **Voice Control**: Amazon Alexa / Google Home integration
- [ ] **Automation Rules**: IF-THEN logic for smart automations
- [ ] **Multi-Room Support**: Organize devices by rooms/zones
- [ ] **Energy Monitoring**: Track power consumption
- [ ] **Cloud Database**: Store data in cloud (MongoDB/PostgreSQL)
- [ ] **Docker Support**: Containerized deployment
- [ ] **REST API Documentation**: Swagger/OpenAPI specification

### Contributions Welcome!

See [Contributing](#-contributing) section below.

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Bugs

1. Check if the issue already exists
2. Create a detailed bug report with:
   - System information
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages/logs

### Suggesting Features

1. Open an issue with the `enhancement` label
2. Describe the feature and its benefits
3. Provide examples or mockups if applicable

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Comment complex logic
- Update documentation for new features

---

## 📄 License

This project is licensed under the MIT License.

### MIT License Summary

```
MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software.
```

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- **EMQX Cloud** - Managed MQTT broker service
- **Adafruit** - Arduino sensor libraries
- **Flask** - Web framework
- **Paho MQTT** - Python MQTT client
- **Arduino Community** - ESP32/ESP8266 support

---

## 📞 Support

Need help? Here's how to get support:

1. **Documentation**: Check the guides in this repository
2. **Issues**: Open an issue on GitHub
3. **Discussions**: Start a discussion for questions
4. **Email**: Contact the maintainer

---

## ⭐ Show Your Support

If you found this project helpful, please consider:

- ⭐ **Starring** the repository
- 🍴 **Forking** for your own projects
- 📢 **Sharing** with others
- 💬 **Providing feedback**

---

<div align="center">

**Made with ❤️ for the IoT Community**

[⬆ Back to Top](#-iot-smart-home-control-system)

</div>
