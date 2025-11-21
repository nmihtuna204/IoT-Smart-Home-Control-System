import tkinter as tk
from tkinter import ttk
import random
import threading
import time
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

# MQTT Configuration
mqttBroker = os.getenv('MQTT_BROKER', 'vdd11821.ala.us-east-1.emqxsl.com')
mqttPort = int(os.getenv('MQTT_PORT', 8883))
mqttUser = os.getenv('MQTT_USERNAME', 'octiu123')
mqttPassword = os.getenv('MQTT_PASSWORD', 'octiu123')
caCertPath = os.getenv('CA_CERT_PATH', 'emqxsl-ca.crt')

class IoTSimulator:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_data()
        self.setup_mqtt()
        self.setup_gui()
        self.start_background_tasks()

    def setup_data(self):
        # Sensor data for both boards
        self.sensor_data = {
            'esp32': {
                'motion': False,
                'humidity': 45.0,
                'light_level': 300,
                'temperature': 25.0
            },
            'esp8266': {
                'motion': False,
                'temperature': 25.0,
                'humidity': 50.0,
                'light_level': 250
            }
        }
        
        # Device status for both boards
        self.device_status = {
            'esp32': {
                'light': 'off',
                'light2': 'off'
            },
            'esp8266': {
                'light': 'off',
                'light2': 'off'
            }
        }
        
        # GUI Variables
        self.sensor_vars = {
            'esp32': {
                'motion': tk.StringVar(value="No Motion"),
                'humidity': tk.StringVar(value="--"),
                'light': tk.StringVar(value="--"),
                'temperature': tk.StringVar(value="--")
            },
            'esp8266': {
                'motion': tk.StringVar(value="No Motion"),
                'temperature': tk.StringVar(value="--"),
                'humidity': tk.StringVar(value="--"),
                'light': tk.StringVar(value="--")
            }
        }
        
        self.status_vars = {
            'esp32': {
                'light': tk.StringVar(value="OFF"),
                'light2': tk.StringVar(value="OFF")
            },
            'esp8266': {
                'light': tk.StringVar(value="OFF"),
                'light2': tk.StringVar(value="OFF")
            }
        }

    def setup_mqtt(self):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.username_pw_set(mqttUser, mqttPassword)
        self.mqtt_client.on_connect = self.on_mqtt_connect
        self.mqtt_client.on_message = self.on_mqtt_message
        self.mqtt_client.on_disconnect = self.on_mqtt_disconnect
        self.mqtt_connected = False
        
        # Connection status
        self.connection_status = tk.StringVar(value="Disconnected")
        
    def on_mqtt_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("✅ Connected to MQTT broker successfully!")
            self.mqtt_connected = True
            self.connection_status.set("Connected ✓")
            
            # Subscribe to control topics (to receive commands from web)
            boards = ['esp32', 'esp8266']
            for board in boards:
                client.subscribe(f"{board}/control/light")
                client.subscribe(f"{board}/control/light2")
                print(f"📡 Subscribed to {board} control topics")
                
        else:
            print(f"❌ Failed to connect to MQTT broker. Code: {rc}")
            self.mqtt_connected = False
            self.connection_status.set("Failed ✗")

    def on_mqtt_disconnect(self, client, userdata, rc):
        print("🔄 Disconnected from MQTT broker. Attempting to reconnect...")
        self.mqtt_connected = False
        self.connection_status.set("Reconnecting...")

    def on_mqtt_message(self, client, userdata, msg):
        try:
            topic = msg.topic
            payload = msg.payload.decode()
            print(f"📨 Received: {topic} -> {payload}")
            
            # Parse topic: board/control/device
            topic_parts = topic.split('/')
            if len(topic_parts) == 3 and topic_parts[1] == 'control':
                board = topic_parts[0]  # esp32 or esp8266
                device = topic_parts[2]  # light, light2
                
                if board in self.device_status and device in self.device_status[board]:
                    # Update internal status
                    self.device_status[board][device] = payload.lower()
                    
                    # Update GUI
                    self.status_vars[board][device].set(payload.upper())
                    self.update_status_label_color(board, device, payload.upper())
                    
                    # Publish status back to web
                    status_topic = f"{board}/status/{device}"
                    self.mqtt_client.publish(status_topic, payload.lower())
                    print(f"📤 Published status: {status_topic} -> {payload.lower()}")
                    
        except Exception as e:
            print(f"❌ Error processing MQTT message: {e}")

    def setup_gui(self):
        self.root.title("🚀 IoT Multi-Board Simulator")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f2f5")
        
        # Main title
        title_frame = tk.Frame(self.root, bg="#f0f2f5")
        title_frame.pack(pady=20)
        
        title = tk.Label(title_frame, text="🔬 IoT Multi-Board Simulator", 
                        font=("Arial", 24, "bold"), bg="#f0f2f5", fg="#2c3e50")
        title.pack()
        
        subtitle = tk.Label(title_frame, text="ESP32 & ESP8266 Real-time Control & Monitoring", 
                           font=("Arial", 12), bg="#f0f2f5", fg="#7f8c8d")
        subtitle.pack()
        
        # Connection status
        status_frame = tk.Frame(self.root, bg="#f0f2f5")
        status_frame.pack(pady=10)
        
        tk.Label(status_frame, text="MQTT Status:", font=("Arial", 12, "bold"), 
                bg="#f0f2f5", fg="#34495e").pack(side=tk.LEFT)
        
        self.status_label = tk.Label(status_frame, textvariable=self.connection_status, 
                                    font=("Arial", 12, "bold"), bg="#e74c3c", fg="white", 
                                    padx=10, pady=5, relief=tk.RAISED)
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#f0f2f5")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
        
        # Left side - Sensor Data
        self.create_sensor_panel(main_frame)
        
        # Right side - Device Controls
        self.create_control_panels(main_frame)

    def create_sensor_panel(self, parent):
        sensor_frame = tk.LabelFrame(parent, text="📊 Real-time Sensor Data", 
                                   font=("Arial", 14, "bold"), bg="white", fg="#2c3e50",
                                   relief=tk.RAISED, bd=2)
        sensor_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # ESP32 Sensors
        esp32_frame = tk.LabelFrame(sensor_frame, text="🔲 ESP32 Sensors", 
                                   font=("Arial", 12, "bold"), bg="white", fg="#3498db")
        esp32_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.create_sensor_display(esp32_frame, "🚶 Motion", self.sensor_vars['esp32']['motion'], "#e74c3c", 0)
        self.create_sensor_display(esp32_frame, "🌡️ Temperature", self.sensor_vars['esp32']['temperature'], "#e67e22", 1)
        self.create_sensor_display(esp32_frame, "💧 Humidity", self.sensor_vars['esp32']['humidity'], "#3498db", 2)
        self.create_sensor_display(esp32_frame, "💡 Light Level", self.sensor_vars['esp32']['light'], "#f39c12", 3)
        
        # ESP8266 Sensors  
        esp8266_frame = tk.LabelFrame(sensor_frame, text="🔳 ESP8266 Sensors", 
                                     font=("Arial", 12, "bold"), bg="white", fg="#e67e22")
        esp8266_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.create_sensor_display(esp8266_frame, "🔍 Motion (PIR)", self.sensor_vars['esp8266']['motion'], "#9b59b6", 0)
        self.create_sensor_display(esp8266_frame, "🌡️ Temperature", self.sensor_vars['esp8266']['temperature'], "#e74c3c", 1)
        self.create_sensor_display(esp8266_frame, "💧 Humidity", self.sensor_vars['esp8266']['humidity'], "#3498db", 2)
        self.create_sensor_display(esp8266_frame, "💡 Light Level", self.sensor_vars['esp8266']['light'], "#f39c12", 3)

    def create_sensor_display(self, parent, label, var, color, row):
        tk.Label(parent, text=label, font=("Arial", 11, "bold"), 
                bg="white", fg="#34495e").grid(row=row, column=0, sticky="w", padx=10, pady=5)
        
        tk.Label(parent, textvariable=var, font=("Arial", 14, "bold"), 
                bg="white", fg=color, width=15).grid(row=row, column=1, padx=10, pady=5)

    def create_control_panels(self, parent):
        control_frame = tk.Frame(parent, bg="#f0f2f5")
        control_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # ESP32 Controls
        self.create_board_controls(control_frame, "ESP32", "esp32", "#3498db", 0)
        
        # ESP8266 Controls  
        self.create_board_controls(control_frame, "ESP8266", "esp8266", "#e67e22", 1)

    def create_board_controls(self, parent, board_name, board_id, color, row):
        board_frame = tk.LabelFrame(parent, text=f"🎛️ {board_name} Device Controls", 
                                   font=("Arial", 14, "bold"), bg="white", fg=color,
                                   relief=tk.RAISED, bd=2)
        board_frame.grid(row=row, column=0, sticky="ew", padx=5, pady=10)
        parent.grid_columnconfigure(0, weight=1)
        
        devices = [
            ("💡 Light 1", "light", "#f39c12"),
            ("💡 Light 2", "light2", "#9b59b6")
        ]
        
        for i, (device_name, device_key, device_color) in enumerate(devices):
            self.create_device_control(board_frame, device_name, board_id, device_key, device_color, i)

    def create_device_control(self, parent, device_name, board_id, device_key, color, row):
        # Device label
        tk.Label(parent, text=device_name, font=("Arial", 12, "bold"), 
                bg="white", fg="#2c3e50").grid(row=row, column=0, sticky="w", padx=10, pady=8)
        
        # ON button
        on_btn = tk.Button(parent, text="ON", font=("Arial", 10, "bold"), 
                          bg="#27ae60", fg="white", width=8, relief=tk.RAISED,
                          command=lambda: self.control_device(board_id, device_key, "on"))
        on_btn.grid(row=row, column=1, padx=5, pady=5)
        
        # OFF button
        off_btn = tk.Button(parent, text="OFF", font=("Arial", 10, "bold"), 
                           bg="#e74c3c", fg="white", width=8, relief=tk.RAISED,
                           command=lambda: self.control_device(board_id, device_key, "off"))
        off_btn.grid(row=row, column=2, padx=5, pady=5)
        
        # Status label
        status_label = tk.Label(parent, textvariable=self.status_vars[board_id][device_key], 
                               font=("Arial", 11, "bold"), bg="#95a5a6", fg="white", 
                               width=12, relief=tk.RAISED, pady=5)
        status_label.grid(row=row, column=3, padx=10, pady=5)
        
        # Store reference for color updates
        if not hasattr(self, 'status_labels'):
            self.status_labels = {}
        if board_id not in self.status_labels:
            self.status_labels[board_id] = {}
        self.status_labels[board_id][device_key] = status_label

    def control_device(self, board, device, action):
        """Send control command to MQTT and update local status"""
        if self.mqtt_connected:
            # Publish control command
            topic = f"{board}/control/{device}"
            self.mqtt_client.publish(topic, action)
            print(f"📤 Control sent: {topic} -> {action}")
            
            # Update local status immediately
            self.device_status[board][device] = action
            self.status_vars[board][device].set(action.upper())
            self.update_status_label_color(board, device, action.upper())
            
            # Publish status update
            status_topic = f"{board}/status/{device}"
            self.mqtt_client.publish(status_topic, action)
            print(f"📤 Status published: {status_topic} -> {action}")
        else:
            print("❌ MQTT not connected. Cannot send command.")

    def update_status_label_color(self, board, device, status):
        """Update status label color based on status"""
        if hasattr(self, 'status_labels'):
            label = self.status_labels[board][device]
            if status == "ON":
                label.config(bg="#27ae60")  # Green
            else:
                label.config(bg="#e74c3c")  # Red

    def start_background_tasks(self):
        """Start background threads for MQTT and sensor data"""
        # Start MQTT connection
        threading.Thread(target=self.mqtt_connection_loop, daemon=True).start()
        
        # Start sensor data publishing
        threading.Thread(target=self.publish_sensor_data_loop, daemon=True).start()
        
        # Start GUI updates
        threading.Thread(target=self.update_gui_loop, daemon=True).start()

    def mqtt_connection_loop(self):
        """Handle MQTT connection and reconnection"""
        while True:
            try:
                if not self.mqtt_connected:
                    print("🔄 Attempting to connect to MQTT broker...")
                    self.connection_status.set("Connecting...")
                    
                    # Enable TLS with CA certificate for EMQX
                    if os.path.exists(caCertPath):
                        self.mqtt_client.tls_set(ca_certs=caCertPath)
                        print(f"Using CA certificate: {caCertPath}")
                    else:
                        self.mqtt_client.tls_set()
                        print("Using default TLS (no CA certificate)")
                        
                    self.mqtt_client.connect(mqttBroker, mqttPort, 60)
                    self.mqtt_client.loop_start()
                time.sleep(5)  # Check connection every 5 seconds
            except Exception as e:
                print(f"❌ MQTT connection error: {e}")
                self.mqtt_connected = False
                self.connection_status.set("Error ✗")
                time.sleep(10)  # Wait longer on error

    def publish_sensor_data_loop(self):
        """Continuously publish sensor data"""
        while True:
            try:
                if self.mqtt_connected:
                    # Generate ESP32 data (motion,humidity,light)
                    self.sensor_data['esp32']['motion'] = random.choice([True, False])
                    self.sensor_data['esp32']['humidity'] = round(random.uniform(40, 70), 1)
                    self.sensor_data['esp32']['light_level'] = random.randint(200, 800)
                    self.sensor_data['esp32']['temperature'] = round(random.uniform(20, 35), 1)  # ESP32 có temperature
                    
                    # Generate ESP8266 data (motion,temperature,humidity,light) - Updated to match ESP32
                    self.sensor_data['esp8266']['motion'] = random.choice([True, False])
                    self.sensor_data['esp8266']['temperature'] = round(random.uniform(20, 35), 1)
                    self.sensor_data['esp8266']['humidity'] = round(random.uniform(45, 75), 1)
                    self.sensor_data['esp8266']['light_level'] = random.randint(150, 600)
                    
                    # Publish ESP32 sensors (motion,humidity,light)
                    esp32_payload = f"{self.sensor_data['esp32']['motion']},{self.sensor_data['esp32']['humidity']},{self.sensor_data['esp32']['light_level']}"
                    self.mqtt_client.publish("esp32/sensors", esp32_payload)
                    
                    # Publish ESP8266 sensors (motion,temperature,humidity,light) - Updated format
                    esp8266_payload = f"{int(self.sensor_data['esp8266']['motion'])},{self.sensor_data['esp8266']['temperature']},{self.sensor_data['esp8266']['humidity']},{self.sensor_data['esp8266']['light_level']}"
                    self.mqtt_client.publish("esp8266/sensors", esp8266_payload)
                    
                    print(f"📡 ESP32 sensors: {esp32_payload}")
                    print(f"📡 ESP8266 sensors: {esp8266_payload}")
                    
                time.sleep(3)  # Publish every 3 seconds
                
            except Exception as e:
                print(f"❌ Error publishing sensor data: {e}")
                time.sleep(5)

    def update_gui_loop(self):
        """Update GUI with latest sensor data"""
        while True:
            try:
                # Update ESP32 GUI
                motion_text = "Motion Detected" if self.sensor_data['esp32']['motion'] else "No Motion"
                self.sensor_vars['esp32']['motion'].set(motion_text)
                self.sensor_vars['esp32']['temperature'].set(f"{self.sensor_data['esp32']['temperature']:.1f}°C")
                self.sensor_vars['esp32']['humidity'].set(f"{self.sensor_data['esp32']['humidity']:.1f}%")
                self.sensor_vars['esp32']['light'].set(f"{self.sensor_data['esp32']['light_level']}")
                
                # Update ESP8266 GUI
                motion_text_esp8266 = "🔴 Motion Detected!" if self.sensor_data['esp8266']['motion'] else "🟢 No Motion"
                self.sensor_vars['esp8266']['motion'].set(motion_text_esp8266)
                self.sensor_vars['esp8266']['temperature'].set(f"{self.sensor_data['esp8266']['temperature']:.1f}°C")
                self.sensor_vars['esp8266']['humidity'].set(f"{self.sensor_data['esp8266']['humidity']:.1f}%")
                self.sensor_vars['esp8266']['light'].set(f"{self.sensor_data['esp8266']['light_level']}")
                
                # Update connection status color
                if self.mqtt_connected:
                    self.status_label.config(bg="#27ae60")  # Green
                else:
                    self.status_label.config(bg="#e74c3c")  # Red
                    
                time.sleep(1)  # Update GUI every second
                
            except Exception as e:
                print(f"❌ Error updating GUI: {e}")
                time.sleep(2)

    def run(self):
        """Start the simulator"""
        print("🚀 Starting IoT Multi-Board Simulator...")
        print(f"🌐 MQTT Broker: {mqttBroker}:{mqttPort}")
        print("📱 GUI starting...")
        
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("🛑 Simulator stopped by user")
        finally:
            if self.mqtt_connected:
                self.mqtt_client.disconnect()
                print("🔌 MQTT connection closed")

if __name__ == "__main__":
    simulator = IoTSimulator()
    simulator.run()
