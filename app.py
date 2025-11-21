# Flask backend for IoT Control
from flask import Flask, render_template, jsonify, request
import paho.mqtt.client as mqtt
import sqlite3
from datetime import datetime
import threading
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

app = Flask(__name__)

# MQTT setup from environment variables
mqttBroker = os.getenv('MQTT_BROKER', 'vdd11821.ala.us-east-1.emqxsl.com')
mqttPort = int(os.getenv('MQTT_PORT', 8883))
mqttUser = os.getenv('MQTT_USERNAME', 'octiu123')
mqttPassword = os.getenv('MQTT_PASSWORD', 'octiu123')
caCertPath = os.getenv('CA_CERT_PATH', 'emqxsl-ca.crt')
mqttClient = mqtt.Client()

# Global device status with persistent storage (Multi-board)
device_status = {
    'esp32': {
        'light': 'off',
        'light2': 'off'
    },
    'esp8266': {
        'light': 'off', 
        'light2': 'off'
    }
}

# Global sensor data for real-time updates (Multi-board) - REAL DATA ONLY
sensor_data = {
    'esp32': {
        'motion': False,
        'humidity': 0.0,
        'light_level': 0,
        'temperature': 0.0,
        'timestamp': 'No data received'
    },
    'esp8266': {
        'motion': False,
        'humidity': 0.0,
        'light_level': 0,
        'temperature': 0.0,
        'timestamp': 'No data received'
    }
}

# Initialize device status from database or default values
def initialize_device_status():
    try:
        conn = sqlite3.connect('iot_data.db')
        cursor = conn.cursor()
        
        # Create device_status table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS device_status (
                device_name TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert default values if table is empty
        cursor.execute('SELECT COUNT(*) FROM device_status')
        if cursor.fetchone()[0] == 0:
            # ESP32 devices
            cursor.execute('INSERT INTO device_status (device_name, status) VALUES (?, ?)', ('esp32_light', 'off'))
            cursor.execute('INSERT INTO device_status (device_name, status) VALUES (?, ?)', ('esp32_light2', 'off'))
            # ESP8266 devices
            cursor.execute('INSERT INTO device_status (device_name, status) VALUES (?, ?)', ('esp8266_light', 'off'))
            cursor.execute('INSERT INTO device_status (device_name, status) VALUES (?, ?)', ('esp8266_light2', 'off'))
        
        # Load current status from database
        cursor.execute('SELECT device_name, status FROM device_status')
        for row in cursor.fetchall():
            parts = row[0].split('_')
            if len(parts) == 2:
                board, device = parts[0], parts[1]
                if board in device_status:
                    device_status[board][device] = row[1]
        
        conn.commit()
        conn.close()
        print("Device status initialized from database")
    except Exception as e:
        print(f"Error initializing device status: {e}")
        # Use default values if database fails
        for board in ['esp32', 'esp8266']:
            device_status[board] = {'light': 'off', 'light2': 'off'}

# Global MQTT connection flag
mqtt_connected = False

def on_connect(client, userdata, flags, rc):
    """Callback for when MQTT client connects"""
    global mqtt_connected
    if rc == 0:
        print("✅ MQTT Connected successfully")
        mqtt_connected = True
        # Subscribe to all relevant topics for both boards
        boards = ['esp32', 'esp8266']
        for board in boards:
            client.subscribe(f"{board}/sensors")
            client.subscribe(f"{board}/status/light")
            client.subscribe(f"{board}/status/light2")
        print("📡 Subscribed to all MQTT topics")
    else:
        print(f"❌ MQTT Connection failed with code {rc}")
        mqtt_connected = False

def on_disconnect(client, userdata, rc):
    """Callback for when MQTT client disconnects"""
    global mqtt_connected
    mqtt_connected = False
    print(f"🔌 MQTT Disconnected with code {rc}")
    if rc != 0:
        print("🔄 Unexpected disconnection. Will auto-reconnect...")

def on_message(client, userdata, msg):
    global device_status, sensor_data
    print(f"📡 Received MQTT message: {msg.topic} -> {msg.payload.decode()}")
    try:
        payload = msg.payload.decode()
        topic_parts = msg.topic.split('/')
        
        # Handle multi-board status updates (board/status/device)
        if len(topic_parts) == 3 and topic_parts[1] == 'status':
            board = topic_parts[0]  # esp32 or esp8266
            device = topic_parts[2]  # light, light2
            if board in device_status and device in device_status[board]:
                device_status[board][device] = payload.lower()
                update_device_status_in_db(f"{board}_{device}", payload.lower())
                print(f"✅ Updated {board} {device} status: {payload.lower()}")
        
        # Handle sensor data (board/sensors)
        elif len(topic_parts) == 2 and topic_parts[1] == 'sensors':
            board = topic_parts[0]  # esp32 or esp8266
            timestamp = datetime.now().isoformat()
            
            print(f"🔍 DEBUG: Received sensor data from {board}: {payload}")
            
            # Try JSON format first
            try:
                import json
                sensor_json = json.loads(payload)
                print(f"📋 JSON format detected: {sensor_json}")
                
                # Extract values from JSON
                motion = sensor_json.get('motion', 0) == 1
                humidity = float(sensor_json.get('humidity', 0))
                light_level = int(sensor_json.get('light_level', 0))
                temperature = float(sensor_json.get('temperature', 0))
                
                # Update real sensor data
                sensor_data[board]['motion'] = motion
                sensor_data[board]['humidity'] = humidity
                sensor_data[board]['light_level'] = light_level
                sensor_data[board]['temperature'] = temperature
                sensor_data[board]['timestamp'] = timestamp
                
                print(f"🌡️ JSON {board.upper()} Sensors - Motion: {motion}, Temp: {temperature}°C, Humidity: {humidity}%, Light: {light_level}")
                
                # Store to database
                store_sensor_data(board, timestamp, motion, humidity, light_level, temperature)
                
            except json.JSONDecodeError:
                # Fallback to CSV format
                print(f"🔄 JSON failed, trying CSV format: {payload}")
                parts = payload.split(",")
                
                if board in ['esp32', 'esp8266'] and len(parts) == 4:
                    # Both boards: motion,humidity,light_level,temperature
                    motion = int(parts[0]) == 1
                    humidity = float(parts[1])
                    light_level = int(parts[2])
                    temperature = float(parts[3])
                    
                    # Update real sensor data
                    sensor_data[board]['motion'] = motion
                    sensor_data[board]['humidity'] = humidity
                    sensor_data[board]['light_level'] = light_level
                    sensor_data[board]['temperature'] = temperature
                    sensor_data[board]['timestamp'] = timestamp
                    
                    print(f"🌡️ CSV {board.upper()} Sensors - Motion: {motion}, Temp: {temperature}°C, Humidity: {humidity}%, Light: {light_level}")
                    
                    # Store to database
                    store_sensor_data(board, timestamp, motion, humidity, light_level, temperature)
                else:
                    print(f"⚠️ Invalid CSV sensor data format from {board}: {payload}")
                
    except Exception as e:
        print(f"❌ Error processing MQTT message: {e}")

def update_device_status_in_db(device_name, status):
    """Update device status in database"""
    try:
        conn = sqlite3.connect('iot_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO device_status (device_name, status, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (device_name, status))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error updating device status in database: {e}")

def store_sensor_data(board, timestamp, motion, humidity, light_level, temperature):
    try:
        db_path = os.getenv('DATABASE_PATH', 'iot_data.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Store motion data with simplified schema (backwards compatible)
        if motion is not None:
            try:
                cursor.execute(
                    "INSERT INTO motion_sensor_data (timestamp, motion_detected) VALUES (?, ?)",
                    (timestamp, motion)
                )
            except sqlite3.OperationalError:
                # Fallback for different schema
                cursor.execute(
                    "INSERT INTO motion_sensor_data (device_id, timestamp, motion_detected) VALUES (?, ?, ?)",
                    (1, timestamp, motion)
                )
        
        # Store temperature data with simplified schema
        if temperature is not None and temperature != 0:
            try:
                cursor.execute(
                    "INSERT INTO temperature_data (timestamp, temperature) VALUES (?, ?)",
                    (timestamp, temperature)
                )
            except sqlite3.OperationalError:
                # Fallback for different schema
                cursor.execute(
                    "INSERT INTO temperature_data (device_id, timestamp, temperature) VALUES (?, ?, ?)",
                    (1, timestamp, temperature)
                )
        
        # Store humidity data
        if humidity is not None and humidity != 0:
            try:
                cursor.execute(
                    "INSERT INTO humidity_data (timestamp, humidity) VALUES (?, ?)",
                    (timestamp, humidity)
                )
            except sqlite3.OperationalError:
                # Fallback for different schema  
                cursor.execute(
                    "INSERT INTO humidity_data (device_id, timestamp, humidity) VALUES (?, ?, ?)",
                    (1, timestamp, humidity)
                )
        
        # Store light sensor data
        if light_level is not None:
            try:
                cursor.execute(
                    "INSERT INTO light_sensor_data (timestamp, light_level) VALUES (?, ?)",
                    (timestamp, light_level)
                )
            except sqlite3.OperationalError:
                # Fallback for different schema
                cursor.execute(
                    "INSERT INTO light_sensor_data (device_id, timestamp, light_level) VALUES (?, ?, ?)",
                    (1, timestamp, light_level)
                )
        
        conn.commit()
        conn.close()
    except Exception as e:
        print("Error storing sensor data:", e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control/<board>', methods=['POST'])
def control_board(board):
    if board not in device_status:
        print(f"🔍 DEBUG: Invalid board '{board}', available: {list(device_status.keys())}")
        return jsonify({'status': 'error', 'message': 'Invalid board'})
    
    action = request.json.get('action', '').lower()
    device = request.json.get('device', 'light')
    
    print(f"🔍 DEBUG: Control request - Board: {board}, Device: {device}, Action: {action}")
    
    if action in ['on', 'off'] and device in device_status[board]:
        topic = f"{board}/control/{device}"
        print(f"🔍 DEBUG: Publishing to MQTT topic: {topic} with message: {action}")
        
        result = mqttClient.publish(topic, action)
        print(f"🔍 DEBUG: MQTT publish result - rc: {result.rc}, mid: {result.mid}")
        
        # Update local status immediately for web interface
        device_status[board][device] = action
        update_device_status_in_db(f"{board}_{device}", action)
        
        print(f"🔍 DEBUG: Updated {board}_{device} status to: {action}")
        return jsonify({'status': 'success', 'action': action, 'board': board, 'device': device})
    else:
        print(f"🔍 DEBUG: Invalid action '{action}' or device '{device}' for board '{board}'")
        print(f"🔍 DEBUG: Available devices for {board}: {list(device_status[board].keys())}")
        return jsonify({'status': 'error', 'message': 'Invalid action or device'})

@app.route('/control', methods=['POST'])
def control():
    # Backward compatibility - defaults to esp8266
    action = request.json.get('action', '').lower()
    if action in ['on', 'off']:
        topic = f"esp8266/control/light"
        mqttClient.publish(topic, action)
        
        # Update local status immediately for web interface
        device_status['esp8266']['light'] = action
        update_device_status_in_db('esp8266_light', action)
        
        return jsonify({'status': 'success', 'action': action})
    return jsonify({'status': 'error', 'message': 'Invalid action'})

@app.route('/control_light2', methods=['POST'])
def control_light2():
    # Backward compatibility - defaults to esp8266
    action = request.json.get('action', '').lower()
    if action in ['on', 'off']:
        topic = f"esp8266/control/light2"
        mqttClient.publish(topic, action)
        
        # Update local status immediately for web interface
        device_status['esp8266']['light2'] = action
        update_device_status_in_db('esp8266_light2', action)
        
        return jsonify({'status': 'success', 'action': action})
    return jsonify({'status': 'error', 'message': 'Invalid action'})

@app.route('/device_status')
def get_device_status():
    return jsonify(device_status)

@app.route('/mqtt_status')
def get_mqtt_status():
    """Get MQTT connection status"""
    try:
        # Use our global flag instead of is_connected() which can be unreliable
        print(f"🔍 DEBUG: mqtt_connected flag: {mqtt_connected}")
        print(f"🔍 DEBUG: mqttClient.is_connected(): {mqttClient.is_connected()}")
        
        return jsonify({
            'connected': mqtt_connected,
            'broker': mqttBroker,
            'port': mqttPort,
            'last_sensor_update': sensor_data.get('esp32', {}).get('timestamp', 'No data'),
            'message': 'MQTT Connected' if mqtt_connected else 'MQTT Disconnected - Check ESP32 connection'
        })
    except Exception as e:
        print(f"🔍 DEBUG: Error in mqtt_status: {e}")
        return jsonify({
            'connected': False,
            'error': str(e),
            'message': 'MQTT Connection Error'
        })

@app.route('/sensor_data')
def get_sensor_data():
    """Get real-time sensor data from ESP32/ESP8266 hardware only"""
    try:
        return jsonify({
            'esp32': {
                'motion': sensor_data['esp32']['motion'],
                'humidity': sensor_data['esp32']['humidity'],
                'light_level': sensor_data['esp32']['light_level'],
                'temperature': sensor_data['esp32']['temperature'],
                'timestamp': sensor_data['esp32']['timestamp']
            },
            'esp8266': {
                'motion': sensor_data['esp8266']['motion'],
                'humidity': sensor_data['esp8266']['humidity'],
                'light_level': sensor_data['esp8266']['light_level'],
                'temperature': sensor_data['esp8266']['temperature'],
                'timestamp': sensor_data['esp8266']['timestamp']
            }
        })
    except Exception as e:
        print(f"❌ Error fetching sensor data: {e}")
        return jsonify({
            'esp32': {'motion': False, 'humidity': 0, 'light_level': 0, 'temperature': 0, 'timestamp': 'Error'},
            'esp8266': {'motion': False, 'humidity': 0, 'light_level': 0, 'temperature': 0, 'timestamp': 'Error'}
        })

@app.route('/simulate_sensors')
def simulate_sensors():
    """Manual test simulation - only for testing without hardware"""
    import random
    
    # Update ESP32 data (manual test only)
    sensor_data['esp32']['motion'] = random.choice([True, False])
    sensor_data['esp32']['humidity'] = round(random.uniform(40, 70), 1)
    sensor_data['esp32']['light_level'] = random.randint(200, 800)
    sensor_data['esp32']['temperature'] = round(random.uniform(20, 35), 1)
    sensor_data['esp32']['timestamp'] = datetime.now().isoformat()
    
    # Update ESP8266 data (manual test only)
    sensor_data['esp8266']['motion'] = random.choice([True, False])
    sensor_data['esp8266']['humidity'] = round(random.uniform(45, 75), 1)
    sensor_data['esp8266']['light_level'] = random.randint(150, 600)
    sensor_data['esp8266']['temperature'] = round(random.uniform(20, 35), 1)
    sensor_data['esp8266']['timestamp'] = datetime.now().isoformat()
    
    print("🧪 Manual test simulation triggered")
    return jsonify({"status": "success", "message": "Manual test data generated"})

if __name__ == '__main__':
    # Initialize device status from database
    initialize_device_status()
    
    # Setup MQTT callbacks
    mqttClient.username_pw_set(mqttUser, mqttPassword)
    mqttClient.on_connect = on_connect
    mqttClient.on_message = on_message
    mqttClient.on_disconnect = on_disconnect
    
    # Enable TLS with CA certificate for EMQX - always for secure MQTT
    if os.path.exists(caCertPath):
        mqttClient.tls_set(ca_certs=caCertPath)
        print(f"Using CA certificate: {caCertPath}")
    else:
        mqttClient.tls_set()
        print("Using default TLS (no CA certificate)")
    
    # Connect to MQTT broker
    try:
        print(f"🔌 Connecting to MQTT broker: {mqttBroker}:{mqttPort}")
        mqttClient.connect(mqttBroker, mqttPort, 60)
        mqttClient.loop_start()
        print("📡 MQTT client started")
    except Exception as e:
        print(f"❌ MQTT connection error: {e}")
    
    # Flask configuration from environment
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print("🌐 IoT Web Control System Started!")
    print(f"📱 Web interface: https://{host}:{port}")
    print("💾 Device status loaded from database")
    
    # Real sensor data only - no simulation
    print("📡 Waiting for real sensor data from ESP32/ESP8266...")
    
    # Enable HTTPS
    ssl_context = (os.getenv('SSL_CERT', 'self_signed_cert.pem'), os.getenv('SSL_KEY', 'private_key.pem'))
    app.run(host=host, port=port, debug=debug, ssl_context=ssl_context)
