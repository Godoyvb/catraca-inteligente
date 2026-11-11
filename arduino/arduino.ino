#include <Servo.h>

const int SERVO_PIN = 9;
const int ANGULO_FECHADO = 0;
const int ANGULO_ABERTO = 90;
const unsigned long TEMPO_ABERTO_MS = 3000;

Servo catraca;
bool aberta = false;
unsigned long abertaEm = 0;

void abrirCatraca() {
  catraca.write(ANGULO_ABERTO);
  aberta = true;
  abertaEm = millis();
}

void fecharCatraca() {
  catraca.write(ANGULO_FECHADO);
  aberta = false;
}

void setup() {
  Serial.begin(9600);
  catraca.attach(SERVO_PIN);
  catraca.write(ANGULO_FECHADO);
  Serial.println("PRONTO");
}

void loop() {
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();

    if (comando == "PING") {
      Serial.println("PONG");
    }
    else if (comando == "AUTORIZADO") {
      abrirCatraca();
      Serial.println("CONFIRMADO: AUTORIZADO");
    }
    else if (comando == "NEGADO") {
      fecharCatraca();  // servo fica parado em 0°
      Serial.println("CONFIRMADO: NEGADO");
    }
    // comandos do backend/arduino.py novo
    else if (comando == "LIBERADO") {
      abrirCatraca();
      Serial.println("ESTADO:ABERTA");
    }
    else if (comando == "BLOQUEADO") {
      fecharCatraca();
      Serial.println("ESTADO:FECHADA");
    }
    else if (comando == "STATUS") {
      Serial.println(aberta ? "ESTADO:ABERTA" : "ESTADO:FECHADA");
    }
  }

  // fecha sozinha depois do tempo, sem travar o loop
  if (aberta && millis() - abertaEm >= TEMPO_ABERTO_MS) {
    fecharCatraca();
    Serial.println("ESTADO:FECHADA");
  }
}