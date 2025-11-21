// Test LED ESP32 - Simple blink test
void setup() {
  Serial.begin(115200);
  Serial.println("ESP32 LED Test Starting...");
  
  // Initialize LED pins (CORRECTED)
  pinMode(17, OUTPUT);  // Light 1 - GPIO17
  pinMode(16, OUTPUT);  // Light 2 - GPIO16
  
  Serial.println("Testing LEDs with correct pins...");
}

void loop() {
  // Test Light 1 (GPIO17)
  Serial.println("Light 1 ON (GPIO17)");
  digitalWrite(17, HIGH);
  delay(2000);
  
  Serial.println("Light 1 OFF (GPIO17)");
  digitalWrite(17, LOW);
  delay(1000);
  
  // Test Light 2 (GPIO16)
  Serial.println("Light 2 ON (GPIO16)");
  digitalWrite(16, HIGH);
  delay(2000);
  
  Serial.println("Light 2 OFF (GPIO16)");
  digitalWrite(16, LOW);
  delay(1000);
  
  // Test both LEDs
  Serial.println("Both LEDs ON");
  digitalWrite(17, HIGH);
  digitalWrite(16, HIGH);
  delay(2000);
  
  Serial.println("Both LEDs OFF");
  digitalWrite(17, LOW);
  digitalWrite(16, LOW);
  delay(2000);
}
