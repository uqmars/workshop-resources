int ledPin = 14;
int buttonPin = 13

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(buttonPin, OUTPUT);
}

void loop() {
  digitalWrite(buttonPin, HIGH);
  if (digitalRead(buttonPin)) {
    digitalWrite(ledPin, LOW);
  } else {
    digitalWrite(ledPin, HIGH);
  }
}
