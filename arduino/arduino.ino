void setup() {
  Serial.begin(9600);
  Serial.println("ARDUINO_PRONTO");
}

void loop() {
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();

    if (comando == "PING") {
      Serial.println("PONG");
    }
  }
}