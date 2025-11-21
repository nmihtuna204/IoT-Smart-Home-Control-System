#ifndef ARDUINO_CONFIG_H
#define ARDUINO_CONFIG_H

// WiFi Configuration
#define WIFI_SSID "your_wifi_ssid"
#define WIFI_PASSWORD "your_wifi_password"

// MQTT Broker Configuration
#define MQTT_BROKER "vdd11821.ala.us-east-1.emqxsl.com"
#define MQTT_PORT 8883
#define MQTT_USERNAME "octiu123"
#define MQTT_PASSWORD "octiu123"

// MQTT Topics
#define TOPIC_SENSORS "home/sensors"
#define TOPIC_LIGHT_CONTROL "home/control/light"
#define TOPIC_FAN_CONTROL "home/control/fan"
#define TOPIC_MOTOR_CONTROL "home/control/motor"
#define TOPIC_LIGHT_STATUS "home/status/light"
#define TOPIC_FAN_STATUS "home/status/fan"
#define TOPIC_MOTOR_STATUS "home/status/motor"

// Device Configuration
#define DEVICE_ID "esp8266_001"
#define SENSOR_UPDATE_INTERVAL 5000  // 5 seconds

// Pin Definitions
#define LIGHT_PIN 2
#define FAN_PIN 4
#define MOTOR_FORWARD_PIN 5
#define MOTOR_BACKWARD_PIN 6
#define DHT_PIN 7
#define LIGHT_SENSOR_PIN A0

#endif 