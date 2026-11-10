
#include <Servo.h>

Servo catraca;

const int PINO_SERVO = 9;

void setup() {
  Serial.begin(9600);
  catraca.attach(PINO_SERVO);
  catraca.write(0);

  Serial.println("CATRACA_PRONTA");
}

void loop() {
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();

    if (comando == "ABRIR") {
      catraca.write(45);
      Serial.println("CATRACA_ABERTA");
    }

    else if (comando == "FECHAR") {
      catraca.write(0);
      Serial.println("CATRACA_FECHADA");
    }
  }
}
