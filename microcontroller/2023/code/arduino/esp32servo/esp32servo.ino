#include <ESP32Servo.h>

Servo servo;

int ledPin =27;
int buttonPin = 13;
int servoPWM = 12;


void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(buttonPin, OUTPUT);
  servo.setPeriodHertz(50);
  servo.attach(servoPWM, 500, 2400);
}

void loop() {
  digitalWrite(buttonPin, HIGH);
  if (digitalRead(buttonPin)) {
    servo.write(0);
    digitalWrite(ledPin, LOW);
  } else {
    servo.write(90);
    digitalWrite(ledPin, HIGH);
  }
}