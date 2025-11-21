// Test LED ESP8266 - Simple blink test
void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("ESP8266 LED Test Starting...");
  
  // Initialize LED pins for ESP8266 (using D pin notation)
  pinMode(D0, OUTPUT);  // Light 1 - D0 (GPIO16)
  pinMode(D3, OUTPUT);  // Light 2 - D3 (GPIO0)
  
  Serial.println("Testing LEDs with ESP8266 pins...");
  Serial.println("Light 1: D0 (GPIO16)");
  Serial.println("Light 2: D3 (GPIO0)");
}

void loop() {
  // Test Light 1 (D0 - GPIO16)
  Serial.println("Light 1 ON (D0/GPIO16)");
  digitalWrite(D0, HIGH);
  delay(2000);
  
  Serial.println("Light 1 OFF (D0/GPIO16)");
  digitalWrite(D0, LOW);
  delay(1000);
  
  // Test Light 2 (D3 - GPIO0)
  Serial.println("Light 2 ON (D3/GPIO0)");
  digitalWrite(D3, HIGH);
  delay(2000);
  
  Serial.println("Light 2 OFF (D3/GPIO0)");
  digitalWrite(D3, LOW);
  delay(1000);
  
  // Test both LEDs
  Serial.println("Both LEDs ON");
  digitalWrite(D0, HIGH);
  digitalWrite(D3, HIGH);
  delay(2000);
  
  Serial.println("Both LEDs OFF");
  digitalWrite(D0, LOW);
  digitalWrite(D3, LOW);
  delay(2000);
  
  Serial.println("=== Test cycle complete ===\n");
}
